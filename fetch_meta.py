"""
Meta Ads API + YouTube (GAS) + MyASP CV — FrancDirect専用
YouTube データは Google Apps Script Web App から取得
"""

import os, json, csv, io, re, requests
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

ACCESS_TOKEN      = os.environ["META_ACCESS_TOKEN"]
AD_ACCOUNT_ID     = os.environ["META_AD_ACCOUNT_ID"]
CAMPAIGN_ID       = os.environ["META_CAMPAIGN_ID"]
CV_ACTION         = os.environ.get("META_CV_ACTION", "lead")
SHEET_CSV_URL     = os.environ.get("SHEET_CSV_URL", "")
GAS_YOUTUBE_URL   = os.environ.get("GAS_YOUTUBE_URL", "")
API_VER           = "v21.0"
BASE              = f"https://graph.facebook.com/{API_VER}/act_{AD_ACCOUNT_ID}/insights"
CAMP_FILTER       = f'[{{"field":"campaign.id","operator":"EQUAL","value":"{CAMPAIGN_ID}"}}]'
FIELDS            = "spend,reach,impressions,clicks,cpm,ctr,cpc,actions"
ADSET_FIELDS      = "adset_name,spend,reach,impressions,clicks,cpm,ctr,cpc,actions"
JST               = ZoneInfo("Asia/Tokyo")
META_CV_SPREADSHEET_ID = os.environ.get("META_CV_SPREADSHEET_ID", "1SsfV2nELpb_dZJy9HEXjUIpewx-oy0Zp5rnjRiS0UiU")
META_CV_SHEET_GIDS = {
    "normal": "1453222225",  # ブロード(normal)_画像01~03
    "thank":  "1220836676",  # ブロード(thank)_画像01~03
    "total":  "1728626971",  # Meta報告ブロック
}

def meta(params):
    r = requests.get(BASE, params={**params, "access_token": ACCESS_TOKEN}, timeout=30)
    r.raise_for_status()
    body = r.json()
    if "error" in body:
        raise RuntimeError(f"Meta API: {body['error']['message']}")
    data = body.get("data", [])
    next_url = body.get("paging", {}).get("next")
    while next_url:
        r = requests.get(next_url, timeout=30)
        r.raise_for_status()
        body = r.json()
        if "error" in body:
            raise RuntimeError(f"Meta API: {body['error']['message']}")
        data.extend(body.get("data", []))
        next_url = body.get("paging", {}).get("next")
    return data

def cv_from_actions(actions, atype=CV_ACTION):
    for a in (actions or []):
        if a.get("action_type") == atype:
            return int(float(a.get("value", 0)))
    return 0

def row_to_summary(s):
    return {
        "spend":       round(float(s.get("spend", 0))),
        "reach":       int(s.get("reach", 0)),
        "impressions": int(s.get("impressions", 0)),
        "clicks":      int(s.get("clicks", 0)),
        "cpm":         round(float(s.get("cpm", 0)), 2),
        "ctr":         round(float(s.get("ctr", 0)), 2),
        "cpc":         round(float(s.get("cpc", 0)), 2),
        "cv_meta":     cv_from_actions(s.get("actions")),
        "cv_myasp":    0,
    }

def num(value):
    text = str(value or "").replace(",", "").replace("¥", "").replace("%", "").strip()
    if text in ("", "-"):
        return 0
    try:
        return int(float(text))
    except ValueError:
        return 0

def norm_key(value):
    return re.sub(r"\s+", "", str(value or "").replace("\n", "")).lower()

def parse_sheet_date(value):
    text = str(value or "").strip()
    if not text or text == "合計" or "合計" in text:
        return ""
    if re.match(r"^\d{4}-\d{1,2}-\d{1,2}$", text):
        return text
    m = re.match(r"^(?:\d{4}年)?(\d{1,2})月(\d{1,2})日", text)
    if not m:
        return ""
    year = today.year if "today" in globals() else datetime.now(JST).year
    return f"{year}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"

def spreadsheet_id_from_url(url):
    m = re.search(r"/spreadsheets/d/([A-Za-z0-9_-]{20,})", url or "")
    return m.group(1) if m else ""

def csv_url_for_gid(spreadsheet_id, gid):
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"

def adset_key(name):
    text = str(name or "").lower()
    if "thank" in text:
        return "thank"
    if "normal" in text:
        return "normal"
    return ""

def csv_rows_to_cv_by_date(rows):
    if not rows:
        return {}
    headers = [norm_key(h) for h in rows[0]]
    date_idx = next((i for i, h in enumerate(headers) if h in ("日付", "date", "")), 0)
    cv_idx = next((i for i, h in enumerate(headers) if h in ("myasp_cv", "myaspcv", "メルマガ登録者")), None)
    if cv_idx is None:
        return {}
    values = {}
    for row in rows[1:]:
        d = parse_sheet_date(row[date_idx] if date_idx < len(row) else "")
        if not d:
            continue
        values[d] = num(row[cv_idx]) if cv_idx < len(row) else 0
    return values

def cv_from_csv_text(text):
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return {}
    headers = [norm_key(h) for h in rows[0]]
    cv_idx = next((i for i, h in enumerate(headers) if h in ("myasp_cv", "myaspcv", "メルマガ登録者")), None)
    if cv_idx is not None:
        return csv_rows_to_cv_by_date(rows)

    # Some Google Sheets CSV exports can include leading blank rows/columns.
    # Detect the actual header row containing メルマガ登録者, then parse below it.
    for i, row in enumerate(rows[:20]):
        normalized = [norm_key(c) for c in row]
        if "メルマガ登録者" in normalized:
            return csv_rows_to_cv_by_date(rows[i:])
    return {}

# ── Google Sheet から CV データ ─────────────────────────────────────────
cv_by_date = {}
cv_by_adset_key_date = {}
if SHEET_CSV_URL or META_CV_SPREADSHEET_ID:
    try:
        print("📊 Google Sheet から CV データを取得中...")
        spreadsheet_id = spreadsheet_id_from_url(SHEET_CSV_URL) or META_CV_SPREADSHEET_ID
        sources = [(key, csv_url_for_gid(spreadsheet_id, gid)) for key, gid in META_CV_SHEET_GIDS.items()]

        for key, url in sources:
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                by_date = cv_from_csv_text(r.text)
            except Exception as e:
                print(f"⚠️ {key} CV 読み込み失敗: {e}")
                by_date = {}
            cv_by_adset_key_date[key] = by_date
            print(f"   {key}: {len(by_date)} 日分")

        if cv_by_adset_key_date.get("total"):
            for d, cv in cv_by_adset_key_date["total"].items():
                cv_by_date[d] = {"myasp": cv, "line": 0}
        else:
            for key in ("normal", "thank"):
                for d, cv in cv_by_adset_key_date.get(key, {}).items():
                    current = cv_by_date.setdefault(d, {"myasp": 0, "line": 0})
                    current["myasp"] += cv

        if not cv_by_date and SHEET_CSV_URL:
            print("   normal/thank が読めないため、SHEET_CSV_URL の合計CVを使用します")
            r = requests.get(SHEET_CSV_URL, timeout=10)
            r.raise_for_status()
            by_date = cv_from_csv_text(r.text)
            cv_by_adset_key_date["total"] = by_date
            for d, cv in by_date.items():
                cv_by_date[d] = {"myasp": cv, "line": 0}

        print(f"   {len(cv_by_date)} 日分取得")
    except Exception as e:
        print(f"⚠️ Sheet 読み込み失敗（スキップ）: {e}")

def cv_myasp_for(date_str):
    e = cv_by_date.get(date_str, {})
    return e.get("myasp", 0) + e.get("line", 0)

def cv_myasp_range(start, end):
    return sum(
        v.get("myasp", 0) + v.get("line", 0)
        for d, v in cv_by_date.items() if start <= d <= end
    )

def cv_myasp_for_adset(name, date_str):
    key = adset_key(name)
    if not key:
        return 0
    return cv_by_adset_key_date.get(key, {}).get(date_str, 0)

def cv_myasp_range_for_adset(name, start, end):
    key = adset_key(name)
    if not key:
        return 0
    return sum(cv for d, cv in cv_by_adset_key_date.get(key, {}).items() if start <= d <= end)

# ── GAS から YouTube + Meta CV + 講座購入者(koza) データ ──────────────
youtube_data   = {"daily": [], "yesterday": None, "this_month": None}
koza_meta_date = {}   # Meta 講座購入者 by date
koza_yt_date   = {}   # YouTube 講座購入者 by date

if GAS_YOUTUBE_URL:
    try:
        print("📺 GAS から YouTube + Meta CV データを取得中...")
        r = requests.get(GAS_YOUTUBE_URL, timeout=30)
        r.raise_for_status()
        gas_resp = r.json()

        if "error" in gas_resp:
            print(f"⚠️ GAS エラー: {gas_resp['error']}")
        else:
            if "youtube" in gas_resp:
                # ── YouTube ──────────────────────────────────────────
                youtube_data = gas_resp.get("youtube", youtube_data)
                print(f"   YouTube: {len(youtube_data.get('daily', []))} 日分取得")

                # ── YouTube CV (by_adset) ─────────────────────────────
                yt_cv = gas_resp.get("youtube_cv", {})
                if yt_cv:
                    koza_yt_date = yt_cv.get("koza_by_date", {})
                    # by_adset は今後 dashboard で使えるよう保持
                    by_adset_yt = yt_cv.get("by_adset", {})
                    print(f"   YouTube CV: {len(yt_cv.get('by_date',{}))} 日分")

                # ── Meta CV (N列・S列) ────────────────────────────────
                meta_cv = gas_resp.get("meta_cv", {})
                if meta_cv:
                    by_date  = meta_cv.get("by_date", {})
                    by_adset = meta_cv.get("by_adset", {})
                    koza_meta_date = meta_cv.get("koza_by_date", {})
                    if by_date:
                        cv_by_date.clear()
                        for d, cv in by_date.items():
                            # by_adset の mail/koza 形式にも対応
                            cv_val = cv if isinstance(cv, int) else (cv.get("mail", 0) if isinstance(cv, dict) else int(cv))
                            cv_by_date[d] = {"myasp": cv_val, "line": 0}
                    for key in ("normal", "thank"):
                        raw = by_adset.get(key, {})
                        # 各日の値が {mail, koza} dict の場合は mail だけ抽出
                        cv_by_adset_key_date[key] = {
                            d: (v.get("mail", 0) if isinstance(v, dict) else int(v or 0))
                            for d, v in raw.items()
                        }
                    total_cv = sum(v.get("myasp", 0) for v in cv_by_date.values())
                    total_koza = sum(koza_meta_date.values())
                    print(f"   Meta CV (GAS): {len(cv_by_date)} 日分, mail合計={total_cv}, 講座購入者合計={total_koza}")
                else:
                    print("   Meta CV: GAS レスポンスに meta_cv なし（CSV フォールバック使用）")
            else:
                # 旧フォーマット（YouTube データのみ、後方互換）
                youtube_data = gas_resp
                print(f"   YouTube: {len(youtube_data.get('daily', []))} 日分取得")
    except Exception as e:
        print(f"⚠️ GAS データ取得失敗（スキップ）: {e}")
else:
    print("⚠️ GAS_YOUTUBE_URL 未設定 — YouTube / Meta CV データなし")

# ── Meta: 各期間サマリー ──────────────────────────────────────────────
today       = datetime.now(JST).date()
today_str   = today.strftime("%Y-%m-%d")
month_start = today.strftime("%Y-%m-01")
day30_start = (today - timedelta(days=29)).strftime("%Y-%m-%d")

def fetch_summary(preset):
    rows = meta({
        "fields": FIELDS, "date_preset": preset,
        "level": "campaign", "filtering": CAMP_FILTER,
    })
    if not rows:
        return row_to_summary({})
    merged = {
        "spend": sum(float(r.get("spend",0)) for r in rows),
        "reach": sum(int(r.get("reach",0)) for r in rows),
        "impressions": sum(int(r.get("impressions",0)) for r in rows),
        "clicks": sum(int(r.get("clicks",0)) for r in rows),
        "cpm": 0, "ctr": 0, "cpc": 0, "actions": [],
    }
    total_imp = merged["impressions"]
    if total_imp > 0:
        merged["cpm"] = round(merged["spend"] / total_imp * 1000, 2)
        merged["ctr"] = round(merged["clicks"] / total_imp * 100, 2)
    if merged["clicks"] > 0:
        merged["cpc"] = round(merged["spend"] / merged["clicks"], 2)
    cv = sum(cv_from_actions(r.get("actions")) for r in rows)
    merged["cv_meta"] = cv
    merged["cv_myasp"] = 0
    return {k: merged[k] for k in ["spend","reach","impressions","clicks","cpm","ctr","cpc","cv_meta","cv_myasp"]}

def fetch_adsets(preset):
    rows = meta({
        "fields": ADSET_FIELDS, "date_preset": preset,
        "level": "adset", "filtering": CAMP_FILTER,
    })
    start, end = None, None
    if preset == "today":
        start = end = today_str
    elif preset == "yesterday":
        start = end = yesterday_str
    elif preset == "this_month":
        start, end = month_start, today_str
    elif preset == "last_30d":
        start, end = day30_start, today_str
    return normalize_adsets(rows, start, end)

def fetch_adsets_range(start, end):
    rows = meta({
        "fields": ADSET_FIELDS,
        "time_range": json.dumps({"since": start, "until": end}),
        "level": "adset",
        "filtering": CAMP_FILTER,
    })
    return normalize_adsets(rows, start, end)

def normalize_adsets(rows, start=None, end=None):
    result = []
    for a in rows:
        name = a.get("adset_name", "—")
        if start and end:
            cv_myasp = cv_myasp_range_for_adset(name, start, end)
        else:
            cv_myasp = 0
        result.append({
            "name":        name,
            "spend":       round(float(a.get("spend", 0))),
            "reach":       int(a.get("reach", 0)),
            "impressions": int(a.get("impressions", 0)),
            "clicks":      int(a.get("clicks", 0)),
            "cpm":         round(float(a.get("cpm", 0)), 2),
            "ctr":         round(float(a.get("ctr", 0)), 2),
            "cpc":         round(float(a.get("cpc", 0)), 2),
            "cv_meta":     cv_from_actions(a.get("actions")),
            "cv_myasp":    cv_myasp,
        })
    return sorted(result, key=lambda x: x["spend"], reverse=True)

print(f"📡 Meta (キャンペーンID: {CAMPAIGN_ID}) のデータを取得中...")

s_today  = fetch_summary("today")
s_month  = fetch_summary("this_month")
s_30d    = fetch_summary("last_30d")
s_total  = fetch_summary("maximum")
yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
last_week_start = (today - timedelta(days=7)).strftime("%Y-%m-%d")

s_today["cv_myasp"] = cv_myasp_for(today_str)
s_month["cv_myasp"] = cv_myasp_range(month_start, today_str)
s_30d["cv_myasp"]   = cv_myasp_range(day30_start, today_str)
s_total["cv_myasp"] = sum(v.get("myasp",0)+v.get("line",0) for v in cv_by_date.values())

for s in [s_today, s_month, s_30d, s_total]:
    cv = s["cv_myasp"] or s["cv_meta"]
    s["cpa"] = round(s["spend"] / cv) if cv > 0 else None

adsets_today = fetch_adsets("today")
adsets_yesterday = fetch_adsets("yesterday")
adsets_last_week = fetch_adsets_range(last_week_start, yesterday_str)
adsets_month = fetch_adsets("this_month")
adsets_30d   = fetch_adsets("last_30d")

# Meta 日次データ
daily_raw = meta({
    "fields": FIELDS, "date_preset": "last_90d",
    "level": "campaign", "filtering": CAMP_FILTER,
    "time_increment": 1,
})
daily = []
for d in daily_raw:
    ds = d.get("date_start", "")
    daily.append({
        "date":        ds,
        "spend":       round(float(d.get("spend", 0))),
        "reach":       int(d.get("reach", 0)),
        "impressions": int(d.get("impressions", 0)),
        "clicks":      int(d.get("clicks", 0)),
        "cpm":         round(float(d.get("cpm", 0)), 2),
        "cv_meta":     cv_from_actions(d.get("actions")),
        "cv_myasp":    cv_myasp_for(ds),
    })

# ── 昨日の合算データ ──────────────────────────────────────────────────
meta_yday = next((d for d in daily if d["date"] == yesterday_str), None)
yt_yday   = youtube_data.get("yesterday")

def make_combined(m, y):
    if not m and not y:
        return None
    m = m or {}
    y = y or {}
    spend = m.get("spend",0) + y.get("spend",0)
    imp   = m.get("impressions",0) + y.get("impressions",0)
    clk   = m.get("clicks",0) + y.get("clicks",0)
    mail  = m.get("cv_myasp",0) + y.get("mail",0)
    return {
        "spend":       spend,
        "impressions": imp,
        "clicks":      clk,
        "mail":        mail,
        "cpm":         round(spend / imp * 1000) if imp > 0 else 0,
        "cpc":         round(spend / clk)        if clk > 0 else 0,
        "cpa":         round(spend / mail)        if mail > 0 else None,
    }

combined_yesterday = make_combined(meta_yday, yt_yday)

# ── 合算日次（チャート用）────────────────────────────────────────────
yt_daily_map = {d["date"]: d for d in youtube_data.get("daily", [])}
combined_daily = []
all_dates = sorted(set([d["date"] for d in daily] + list(yt_daily_map.keys())))
for ds in all_dates:
    m = next((d for d in daily if d["date"] == ds), {})
    y = yt_daily_map.get(ds, {})
    spend = m.get("spend",0) + y.get("spend",0)
    imp   = m.get("impressions",0) + y.get("impressions",0)
    clk   = m.get("clicks",0) + y.get("clicks",0)
    mail  = m.get("cv_myasp",0) + y.get("mail",0)
    combined_daily.append({
        "date":       ds,
        "spend":      spend,
        "impressions":imp,
        "clicks":     clk,
        "mail":       mail,
        "meta_spend": m.get("spend",0),
        "yt_spend":   y.get("spend",0),
    })

# ── 出力 ─────────────────────────────────────────────────────────────

# 講座購入者 今月合算
def koza_range(koza_dict, start, end):
    return sum(v for d, v in koza_dict.items() if start <= d <= end)

koza_meta_month  = koza_range(koza_meta_date, month_start, today_str)
koza_yt_month    = koza_range(koza_yt_date,   month_start, today_str)
koza_meta_today  = koza_meta_date.get(today_str, 0)
koza_yt_today    = koza_yt_date.get(today_str, 0)
koza_meta_yday_v = koza_meta_date.get(yesterday_str, 0)
koza_yt_yday_v   = koza_yt_date.get(yesterday_str, 0)

output = {
    "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "campaign_id":  CAMPAIGN_ID,
    "today":        s_today,
    "this_month":   s_month,
    "last_30d":     s_30d,
    "total":        s_total,
    "adsets": {
        "today":     adsets_today,
        "yesterday": adsets_yesterday,
        "last_week": adsets_last_week,
        "this_month":adsets_month,
        "last_30d":  adsets_30d,
    },
    "daily":          daily,
    "cv_log":         [{"date": k, **v} for k, v in sorted(cv_by_date.items())],
    "youtube":        youtube_data,
    "yesterday": {
        "date":     yesterday_str,
        "meta":     meta_yday,
        "youtube":  yt_yday,
        "combined": combined_yesterday,
    },
    "combined_daily": combined_daily,
    # 講座購入者 (S列) サマリー
    "koza": {
        "meta": {
            "today":      koza_meta_today,
            "yesterday":  koza_meta_yday_v,
            "this_month": koza_meta_month,
            "by_date":    koza_meta_date,
        },
        "youtube": {
            "today":      koza_yt_today,
            "yesterday":  koza_yt_yday_v,
            "this_month": koza_yt_month,
            "by_date":    koza_yt_date,
        },
        "combined": {
            "today":      koza_meta_today + koza_yt_today,
            "yesterday":  koza_meta_yday_v + koza_yt_yday_v,
            "this_month": koza_meta_month + koza_yt_month,
        },
    },
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("✅ 完了")
print(f"   Meta今月  : ¥{s_month['spend']:,}  MyASP CV:{s_month['cv_myasp']}")
yt_m = youtube_data.get("this_month")
if yt_m:
    print(f"   YouTube今月: ¥{yt_m.get('spend',0):,}  メルマガ:{yt_m.get('mail',0)}")
if combined_yesterday:
    print(f"   昨日合算  : ¥{combined_yesterday['spend']:,}  メール:{combined_yesterday.get('mail',0)}")
