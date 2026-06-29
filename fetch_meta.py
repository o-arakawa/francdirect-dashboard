"""
Meta Ads API + Google Sheets CSV + MyASP CV — FrancDirect専用
GAS が使えない場合でも、Google Sheets CSV からCV/YouTube数値を取得する
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
YOUTUBE_SHEET_GIDS = {
    "normal": "631616865",   # Yt_LP▶︎NAH(通常)
    "thank":  "823916960",   # Yt_LP▶︎NAH(thank[ムック])
    "total":  "1747543527",  # YouTube報告ブロック
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
    text = (
        str(value or "")
        .replace(",", "")
        .replace("¥", "")
        .replace("￥", "")
        .replace("Â", "")
        .replace("%", "")
        .strip()
    )
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

def fetch_csv_text(url):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    # Google Sheets CSV は charset が付かず requests.text が文字化けすることがあるため固定で読む
    return r.content.decode("utf-8-sig")

def adset_key(name):
    text = str(name or "").lower()
    if "thank" in text:
        return "thank"
    if "normal" in text:
        return "normal"
    return ""

def csv_rows_from_text(text):
    return list(csv.reader(io.StringIO(text or "")))

def find_sheet_header_index(rows):
    for i, row in enumerate(rows[:20]):
        normalized = [norm_key(c) for c in row]
        if (
            "メルマガ登録者" in normalized
            or "消化金額" in normalized
            or "クリック数" in normalized
        ):
            return i
    return 0

def header_index(headers, candidates, fallback):
    for candidate in candidates:
        if candidate in headers:
            return headers.index(candidate)
    return fallback

def cell(row, idx):
    return row[idx] if idx is not None and idx < len(row) else ""

def csv_rows_to_sheet_metrics(rows):
    if not rows:
        return {"mail_by_date": {}, "koza_by_date": {}, "daily": []}

    header_i = find_sheet_header_index(rows)
    headers = [norm_key(h) for h in rows[header_i]]
    date_idx = header_index(headers, ("日付", "date"), 0)
    spend_idx = header_index(headers, ("消化金額", "spend"), 1)
    imp_idx = header_index(headers, ("表示回数", "impressions"), 2)
    cpm_idx = header_index(headers, ("cpm",), 5)
    click_idx = header_index(headers, ("クリック数", "clicks"), 6)
    ctr_idx = header_index(headers, ("表示回数ctr", "ctr"), 7)
    cpc_idx = header_index(headers, ("cpc",), 9)
    mail_idx = header_index(headers, ("myasp_cv", "myaspcv", "メルマガ登録者"), 13)
    koza_idx = header_index(headers, ("講座購入者",), 18)

    mail_by_date = {}
    koza_by_date = {}
    daily = []

    for row in rows[header_i + 1:]:
        d = parse_sheet_date(row[date_idx] if date_idx < len(row) else "")
        if not d:
            continue
        spend = num(cell(row, spend_idx))
        impressions = num(cell(row, imp_idx))
        clicks = num(cell(row, click_idx))
        mail = num(cell(row, mail_idx))
        koza = num(cell(row, koza_idx))
        cpm = num(cell(row, cpm_idx)) or (round(spend / impressions * 1000) if impressions > 0 else 0)
        cpc = num(cell(row, cpc_idx)) or (round(spend / clicks) if clicks > 0 else 0)

        mail_by_date[d] = mail
        koza_by_date[d] = koza
        if spend or impressions or clicks or mail or koza:
            daily.append({
                "date": d,
                "spend": spend,
                "impressions": impressions,
                "clicks": clicks,
                "cpm": cpm,
                "ctr": num(cell(row, ctr_idx)),
                "cpc": cpc,
                "mail": mail,
                "koza": koza,
                "cpa": round(spend / mail) if mail > 0 else None,
            })

    daily.sort(key=lambda r: r["date"])
    return {"mail_by_date": mail_by_date, "koza_by_date": koza_by_date, "daily": daily}

def sheet_metrics_from_csv_text(text):
    return csv_rows_to_sheet_metrics(csv_rows_from_text(text))

def cv_from_csv_text(text):
    return sheet_metrics_from_csv_text(text)["mail_by_date"]

def sum_date_values(dicts):
    result = {}
    for data in dicts:
        for d, v in data.items():
            result[d] = result.get(d, 0) + v
    return result

def sum_metric_rows(rows):
    rows = rows or []
    spend = sum(r.get("spend", 0) for r in rows)
    impressions = sum(r.get("impressions", 0) for r in rows)
    clicks = sum(r.get("clicks", 0) for r in rows)
    mail = sum(r.get("mail", 0) for r in rows)
    koza = sum(r.get("koza", 0) for r in rows)
    return {
        "spend": spend,
        "impressions": impressions,
        "clicks": clicks,
        "mail": mail,
        "koza": koza,
        "cpm": round(spend / impressions * 1000) if impressions > 0 else 0,
        "cpc": round(spend / clicks) if clicks > 0 else 0,
        "cpa": round(spend / mail) if mail > 0 else None,
    }

def build_youtube_data_from_daily(daily_rows):
    current = datetime.now(JST).date()
    yday = (current - timedelta(days=1)).strftime("%Y-%m-%d")
    month_start_local = current.strftime("%Y-%m-01")
    today_local = current.strftime("%Y-%m-%d")
    month_rows = [r for r in daily_rows if month_start_local <= r.get("date", "") <= today_local]
    return {
        "daily": daily_rows,
        "yesterday": next((r for r in daily_rows if r.get("date") == yday), None),
        "this_month": sum_metric_rows(month_rows) if month_rows else None,
    }

# ── Google Sheet から CV データ ─────────────────────────────────────────
cv_by_date = {}
cv_by_adset_key_date = {}
koza_meta_date = {}
koza_meta_adset_key_date = {}
koza_yt_date = {}
youtube_data = {"daily": [], "yesterday": None, "this_month": None}

if SHEET_CSV_URL or META_CV_SPREADSHEET_ID:
    try:
        print("📊 Google Sheet から CV / YouTube データを取得中...")
        spreadsheet_id = spreadsheet_id_from_url(SHEET_CSV_URL) or META_CV_SPREADSHEET_ID
        sources = [(key, csv_url_for_gid(spreadsheet_id, gid)) for key, gid in META_CV_SHEET_GIDS.items()]

        for key, url in sources:
            try:
                metrics = sheet_metrics_from_csv_text(fetch_csv_text(url))
                by_date = metrics["mail_by_date"]
                koza_by_date = metrics["koza_by_date"]
            except Exception as e:
                print(f"⚠️ {key} CV 読み込み失敗: {e}")
                by_date = {}
                koza_by_date = {}
            cv_by_adset_key_date[key] = by_date
            koza_meta_adset_key_date[key] = koza_by_date
            print(f"   Meta {key}: mail {sum(by_date.values())}件 / 講座 {sum(koza_by_date.values())}件 / {len(by_date)}日分")

        if cv_by_adset_key_date.get("total"):
            for d, cv in cv_by_adset_key_date["total"].items():
                cv_by_date[d] = {"myasp": cv, "line": 0}
            koza_meta_date = dict(koza_meta_adset_key_date.get("total", {}))
        else:
            for key in ("normal", "thank"):
                for d, cv in cv_by_adset_key_date.get(key, {}).items():
                    current = cv_by_date.setdefault(d, {"myasp": 0, "line": 0})
                    current["myasp"] += cv
            koza_meta_date = sum_date_values([
                koza_meta_adset_key_date.get("normal", {}),
                koza_meta_adset_key_date.get("thank", {}),
            ])

        if not cv_by_date and SHEET_CSV_URL:
            print("   normal/thank が読めないため、SHEET_CSV_URL の合計CVを使用します")
            metrics = sheet_metrics_from_csv_text(fetch_csv_text(SHEET_CSV_URL))
            by_date = metrics["mail_by_date"]
            cv_by_adset_key_date["total"] = by_date
            for d, cv in by_date.items():
                cv_by_date[d] = {"myasp": cv, "line": 0}
            koza_meta_date = metrics["koza_by_date"]

        try:
            yt_total_metrics = sheet_metrics_from_csv_text(
                fetch_csv_text(csv_url_for_gid(spreadsheet_id, YOUTUBE_SHEET_GIDS["total"]))
            )
            youtube_data = build_youtube_data_from_daily(yt_total_metrics["daily"])
            koza_yt_date = yt_total_metrics["koza_by_date"]
            yt_m = youtube_data.get("this_month") or {}
            print(
                f"   YouTube total: {len(youtube_data.get('daily', []))}日分 / "
                f"今月 mail {yt_m.get('mail', 0)}件 / 講座 {yt_m.get('koza', 0)}件"
            )
        except Exception as e:
            print(f"⚠️ YouTube CSV 読み込み失敗: {e}")

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

def koza_range_for_adset(name, start, end):
    key = adset_key(name)
    if not key:
        return 0
    return sum(v for d, v in koza_meta_adset_key_date.get(key, {}).items() if start <= d <= end)

# ── GAS から YouTube + Meta CV + 講座購入者(koza) データ ──────────────
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
                gas_youtube_data = gas_resp.get("youtube", {})
                if gas_youtube_data.get("daily"):
                    youtube_data = gas_youtube_data
                print(f"   YouTube: {len(youtube_data.get('daily', []))} 日分取得")

                # ── YouTube CV (by_adset) ─────────────────────────────
                yt_cv = gas_resp.get("youtube_cv", {})
                if yt_cv:
                    gas_koza_yt = yt_cv.get("koza_by_date", {})
                    if gas_koza_yt:
                        koza_yt_date = gas_koza_yt
                    # by_adset は今後 dashboard で使えるよう保持
                    by_adset_yt = yt_cv.get("by_adset", {})
                    print(f"   YouTube CV: {len(yt_cv.get('by_date',{}))} 日分")

                # ── Meta CV (N列・S列) ────────────────────────────────
                meta_cv = gas_resp.get("meta_cv", {})
                if meta_cv:
                    by_date  = meta_cv.get("by_date", {})
                    by_adset = meta_cv.get("by_adset", {})
                    gas_koza_meta = meta_cv.get("koza_by_date", {})
                    if gas_koza_meta:
                        koza_meta_date = gas_koza_meta
                    if by_date:
                        cv_by_date.clear()
                        for d, cv in by_date.items():
                            # by_adset の mail/koza 形式にも対応
                            cv_val = cv if isinstance(cv, int) else (cv.get("mail", 0) if isinstance(cv, dict) else int(cv))
                            cv_by_date[d] = {"myasp": cv_val, "line": 0}
                    for key in ("normal", "thank"):
                        raw = by_adset.get(key, {})
                        if not raw:
                            continue
                        # 各日の値が {mail, koza} dict の場合は mail だけ抽出
                        cv_by_adset_key_date[key] = {
                            d: (v.get("mail", 0) if isinstance(v, dict) else int(v or 0))
                            for d, v in raw.items()
                        }
                        koza_meta_adset_key_date[key] = {
                            d: (v.get("koza", 0) if isinstance(v, dict) else 0)
                            for d, v in raw.items()
                        }
                    total_cv = sum(v.get("myasp", 0) for v in cv_by_date.values())
                    total_koza = sum(koza_meta_date.values())
                    print(f"   Meta CV (GAS): {len(cv_by_date)} 日分, mail合計={total_cv}, 講座購入者合計={total_koza}")
                else:
                    print("   Meta CV: GAS レスポンスに meta_cv なし（CSV フォールバック使用）")
            else:
                # 旧フォーマット（YouTube データのみ、後方互換）
                if gas_resp.get("daily"):
                    youtube_data = gas_resp
                print(f"   YouTube: {len(youtube_data.get('daily', []))} 日分取得")
    except Exception as e:
        print(f"⚠️ GAS データ取得失敗（スキップ）: {e}")
else:
    print("ℹ️ GAS_YOUTUBE_URL 未設定 — Google Sheet CSV データを使用します")

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
            koza = koza_range_for_adset(name, start, end)
        else:
            cv_myasp = 0
            koza = 0
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
            "koza":        koza,
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
