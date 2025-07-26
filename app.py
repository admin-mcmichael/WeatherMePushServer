from flask import Flask, request, jsonify
from apns2.client import APNsClient
from apns2.credentials import TokenCredentials
from apns2.payload import Payload
import os
import traceback  # ✅ Place here at top level (no indentation)

app = Flask(__name__)

# Load credentials from environment variables or hardcoded fallback
AUTH_KEY_PATH = os.getenv('APNS_KEY_PATH', 'AuthKey_85QQ4DK39M.p8')
AUTH_KEY_ID = os.getenv('APNS_KEY_ID', '85QQ4DK39M')  # From Apple Developer Portal
TEAM_ID = os.getenv('TEAM_ID', 'V7DXMMX52T')          # Your Apple Developer Team ID
BUNDLE_ID = os.getenv('BUNDLE_ID', 'au.com.mcmichael.weatherme')  # Your app's Bundle ID

# Set up TokenCredentials
credentials = TokenCredentials(
    auth_key_path=AUTH_KEY_PATH,
    auth_key_id=AUTH_KEY_ID,
    team_id=TEAM_ID,
)

# Set up APNsClient
apns_client = APNsClient(
    credentials,
    use_sandbox=True  # ✅ Set to False for production
)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    device_token = data.get('device_token')
    alert = data.get('alert', 'Rain alert!')

    payload = Payload(alert=alert, sound="default", badge=1)

    try:
        response = apns_client.send_notification(device_token, payload, topic=BUNDLE_ID)
        print("APNs Response:", response.__dict__)
        return jsonify({'status': 'sent'}), 200
    except Exception as e:
        print("APNs Error:", str(e))
        traceback.print_exc()  # ✅ Show full stack trace
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
