from mastodon import Mastodon
from datetime import datetime, timedelta, timezone
import os

# === Configuration ===
MASTODON_API_BASE_URL = 'https://gts.invisibleparade.com'
ACCESS_TOKEN = os.getenv('GTS_TOKEN')

# === Time Ranges ===
now = datetime.now(timezone.utc)
two_weeks_ago = now - timedelta(weeks=2)
one_week_ago = now - timedelta(weeks=1)

# === Set up Mastodon client ===
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=MASTODON_API_BASE_URL
)

# === Get current user's ID ===
me = mastodon.account_verify_credentials()
my_id = me['id']

# === Pagination through statuses ===
def get_recent_statuses():
    recent_statuses = []
    for status in mastodon.account_statuses(my_id, limit=40):
        created_at = status['created_at']
        if created_at < two_weeks_ago:
            break
        recent_statuses.append(status)
    return recent_statuses

# === Main Logic ===
statuses = get_recent_statuses()

for status in statuses:
    if status['reblog'] is not None:  # This is a reboost
        reboost_time = status['created_at']
        if reboost_time < one_week_ago:
            print(f"Unboosting: {status['reblog']['url']} (reboosted on {reboost_time})")
            try:
                mastodon.status_unreblog(status['reblog']['id'])
            except Exception as e:
                print(f"Error unboosting: {e}")
