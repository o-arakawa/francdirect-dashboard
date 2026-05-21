"""
Meta Ads API + YouTube (GAS) + MyASP CV — FrancDirect専用
YouTube データは Google Apps Script Web App から取得
"""

import os, json, csv, io, requests
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

# ── Google Sheet から MyASP CV ─────────────────────────────────────────
cv_by_date = {}
if SHEET_CSV_URL:
    try:
        print("📊 Google Sheet から CV データを取得中...")
        r = requests.get(SHEET_CSV_URL, timeout=10)
        r.raise_for_status()
        reader = csv.DictReader(io.StringIO(r.text))
        for row in reader:
            d = (row.get("日付") or row.get("date") or "").strip()
            if not d:
                continue
            myasp = int(float(row.get("MyASP_CV") or row.get("myasp_cv") or 0))
            line  = int(float(row.get("LINE_CV")  or row.get("line_cv")  or 0))
            cv_by_date[d] = {"myasp": myasp, "line": line}
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

# ── YouTube データ（GAS Web App）─────────────────────────────────────
youtube_data = {"daily": [], "yesterday": None, "this_month": None}
if GAS_YOUTUBE_URL:
    try:
        print("📺 YouTube データを GAS から取得中...")
        r = requests.get(GAS_YOUTUBE_URL, timeout=30)
        r.raise_for_status()
        youtube_data = r.json()
        if "error" in youtube_data:
            print(f"⚠️ GAS エラー: {youtube_data['error']}")
            youtube_data = {"daily": [], "yesterday": None, "this_month": None}
        else:
