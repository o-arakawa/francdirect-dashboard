import os
import json
import requests
from datetime import datetime, timezone

ACCESS_TOKEN   = os.environ["META_ACCESS_TOKEN"]
AD_ACCOUNT_ID  = os.environ["META_AD_ACCOUNT_ID"]
CAMPAIGN_ID    = os.environ["META_CAMPAIGN_ID"]
CV_ACTION_TYPE = os.environ.get("META_CV_ACTION", "lead")
API_VER        = "v21.0"
BASE_URL       = f"https://graph.facebook.com/{API_VER}/act_{AD_ACCOUNT_ID}/insights"
FIELDS         = "spend,reach,impressions,clicks,cpm,ctr,cpc,actions,campaign_name"

def get_cv(actions_list, action_type):
    if not actions_list:
        return 0
    for a in actions_list:
        if a.get("action_type") == action_type:
            return int(float(a.get("value", 0)))
    return 0

def fetch(params):
    r = requests.get(BASE_URL, params={**params, "access_token": ACCESS_TOKEN})
    body = r.json()
    if "error" in body:
        raise RuntimeError(f"Meta API Error: {body['error']['message']}")
    return body

print("📡 Meta Ads データを取得中...")

# サマリー（キャンペーン絞り込み）
sum_raw = fetch({
    "fields": FIELDS,
    "date_preset": "last_30d",
    "level": "campaign",
    "filtering": f'[{{"field":"campaign.id","operator":"EQUAL","value":"{CAMPAIGN_ID}"}}]',
})

rows = sum_raw.get("data", [])
if not rows:
    # フィルタが効かない場合はアカウント全体を取得
    print("⚠️ キャンペーン絞り込み結果なし → アカウント全体で取得")
    sum_raw = fetch({
        "fields": "spend,reach,impressions,clicks,cpm,ctr,cpc,actions",
        "date_preset": "last_30d",
        "level": "account",
    })
    rows = sum_raw.get("data", [{}])

s = rows[0] if rows else {}
summary = {
    "spend":       round(float(s.get("spend", 0))),
    "reach":       int(s.get("reach", 0)),
    "impressions": int(s.get("impressions", 0)),
    "clicks":      int(s.get("clicks", 0)),
    "cpm":         round(float(s.get("cpm", 0)), 2),
    "ctr":         round(float(s.get("ctr", 0)), 2),
    "cpc":         round(float(s.get("cpc", 0)), 2),
    "conversions": get_cv(s.get("actions"), CV_ACTION_TYPE),
}
summary["cpa"] = (
    round(summary["spend"] / summary["conversions"])
    if summary["conversions"] > 0 else None
)

# 日次
daily_raw = fetch({
    "fields": "spend,reach,impressions,clicks,cpm,actions",
    "date_preset": "last_30d",
    "level": "account",
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
        "conversions": get_cv(d.get("actions"), CV_ACTION_TYPE),
    })

# 広告セット別
adset_raw = fetch({
    "fields": "adset_name,spend,reach,impressions,clicks,cpm,ctr,cpc,actions",
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
        "conversions": get_cv(a.get("actions"), CV_ACTION_TYPE),
    })

output = {
    "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "campaign_id":  CAMPAIGN_ID,
    "cv_action":    CV_ACTION_TYPE,
    "summary":      summary,
    "daily":        daily,
    "adsets":       adsets,
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ 完了 | 広告費: ¥{summary['spend']:,}  CV: {summary['conversions']}件")
