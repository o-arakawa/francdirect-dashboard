"""
Meta Ads API データ取得スクリプト — FrancDirect
GitHub Actions から 6時間おきに実行される
"""

import os
import json
import requests
from datetime import datetime, timezone

ACCESS_TOKEN   = os.environ["META_ACCESS_TOKEN"]
AD_ACCOUNT_ID  = os.environ["META_AD_ACCOUNT_ID"]    # 727273939454651
CAMPAIGN_ID    = os.environ["META_CAMPAIGN_ID"]       # 120243061348860707
CV_ACTION_TYPE = os.environ.get("META_CV_ACTION", "lead")
API_VER        = "v21.0"

ACCOUNT_URL  = f"https://graph.facebook.com/{API_VER}/act_{AD_ACCOUNT_ID}/insights"
CAMPAIGN_URL = f"https://graph.facebook.com/{API_VER}/{CAMPAIGN_ID}/insights"
FIELDS       = "spend,reach,impressions,clicks,cpm,ctr,cpc,actions,action_values"

def get_action_value(actions_list, action_type):
    if not actions_list:
        return 0
    for a in actions_list:
        if a.get("action_type") == action_type:
            return float(a.get("value", 0))
    return 0

def fetch(url, params):
    r = requests.get(url, params={**params, "access_token": ACCESS_TOKEN})
    r.raise_for_status()
    body = r.json()
    if "error" in body:
        raise RuntimeError(f"Meta API エラー: {body['error'].get('message','')}")
    return body

# ── 対象キャンペーンのサマリー（過去 30 日） ─────────────────────────
print(f"📡 キャンペーン {CAMPAIGN_ID} のデータを取得中...")

sum_raw = fetch(CAMPAIGN_URL, {
    "fields": FIELDS,
    "date_preset": "last_30d",
})
s = sum_raw.get("data", [{}])[0]

summary = {
    "spend":       round(float(s.get("spend", 0))),
    "reach":       int(s.get("reach", 0)),
    "impressions": int(s.get("impressions", 0)),
    "clicks":      int(s.get("clicks", 0)),
    "cpm":         round(float(s.get("cpm", 0)), 2),
    "ctr":         round(float(s.get("ctr", 0)), 2),
    "cpc":         round(float(s.get("cpc", 0)), 2),
    "conversions": int(get_action_value(s.get("actions"), CV_ACTION_TYPE)),
}
summary["cpa"] = (
    round(summary["spend"] / summary["conversions"])
    if summary["conversions"] > 0 else None
)

# ── 日次内訳（過去 30 日） ───────────────────────────────────────────
daily_raw = fetch(CAMPAIGN_URL, {
    "fields": FIELDS,
    "date_preset": "last_30d",
    "time_increment": 1,
})
daily = []
for d in daily_raw.get("data", []):
    daily.append({
        "date":        d.get("date_start"),
        "spend":       round(float(d.get("spend", 0))),
        "reach":       int(d.get("reach", 0)),
        "impressions": int(d.get("impressions", 0)),
        "clicks":      int(d.get("clicks", 0)),
        "cpm":         round(float(d.get("cpm", 0)), 2),
        "conversions": int(get_action_value(d.get("actions"), CV_ACTION_TYPE)),
    })

# ── 広告セット別内訳 ─────────────────────────────────────────────────
adset_raw = fetch(CAMPAIGN_URL, {
    "fields": "adset_name," + FIELDS,
    "date_preset": "last_30d",
    "level": "adset",
})
adsets = []
for a in adset_raw.get("data", []):
    adsets.append({
        "name":        a.get("adset_name", "—"),
        "spend":       round(float(a.get("spend", 0))),
        "reach":       int(a.get("reach", 0)),
        "impressions": int(a.get("impressions", 0)),
        "clicks":      int(a.get("clicks", 0)),
        "ctr":         round(float(a.get("ctr", 0)), 2),
        "cpc":         round(float(a.get("cpc", 0)), 2),
        "conversions": int(get_action_value(a.get("actions"), CV_ACTION_TYPE)),
    })

# ── 出力 ─────────────────────────────────────────────────────────────
output = {
    "last_updated":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "campaign_id":   CAMPAIGN_ID,
    "cv_action":     CV_ACTION_TYPE,
    "summary":       summary,
    "daily":         daily,
    "adsets":        adsets,
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ data.json を更新しました")
print(f"   広告費: ¥{summary['spend']:,}  CV: {summary['conversions']}件  CPA: ¥{summary['cpa'] or '—'}")
