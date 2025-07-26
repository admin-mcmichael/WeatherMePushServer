from flask import Flask, request, jsonify
from apns2.client import APNsClient
from apns2.credentials import TokenCredentials
from apns2.payload import Payload
import os

app = Flask(__name__)

# Load credentials
AUTH_KEY_PATH = os.getenv('APNS_KEY_PATH', 'AuthKey_85QQ4DK39M.p8')
AUTH_KEY_ID = os.getenv('APNS_KEY_ID', '85QQ4DK39M')
TEAM_ID = os.getenv('TEAM_ID', 'V7DXMMX52T')
BUNDLE_ID = os.getenv('BUNDLE_ID', 'au.com.mcmichael.weatherme')

credentials = TokenCredentials(
    auth_key_path=AUTH_KEY_PATH,
    auth_key_id=AUTH_KEY_ID,
    team_id=TEAM_ID
)

# ⚠️ Set use_sandbox to False unless testing with dev builds
apns_client = APNsClient(
    credentials,
    use_sandbox=False
)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    device_token = data.get('device_token')
    alert = data.get('alert', 'Rain alert!')

    payload = Payload(alert=alert, sound="default", badge=1)

   import traceback  # Add at the top if not present

...

try:
    response = apns_client.send_notification(device_token, payload, topic=BUNDLE_ID)
    print("APNs Response:", response.__dict__)
    return jsonify({'status': 'sent'}), 200
except Exception as e:
    print("APNs Error:", str(e))
    traceback.print_exc()  # <- this prints the full error details
    return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
