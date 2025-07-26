from flask import Flask, request, jsonify
from apns2.client import APNsClient
from apns2.payload import Payload
from apns2.credentials import TokenCredentials
import os

app = Flask(__name__)

# Load environment variables (or replace with actual values)
TEAM_ID = os.getenv("APNS_TEAM_ID")
KEY_ID = os.getenv("APNS_KEY_ID")
BUNDLE_ID = os.getenv("APNS_BUNDLE_ID")
AUTH_KEY_PATH = . ("APNS_AUTH_KEY_PATH", "AuthKey.p8")

# Initialize APNs client
credentials = TokenCredentials(
    auth_key_path=AUTH_KEY_PATH,
    auth_key_id=KEY_ID,
    team_id=TEAM_ID
)
apns_client = APNsClient(
    credentials,
    use_sandbox=True,  # Set to False for production
    use_alternative_port=False
)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    print("Received notification request:", data)

    token = data.get("token")
    lat = data.get("lat")
    lon = data.get("lon")

    if not token or lat is None or lon is None:
        return jsonify({"error": "Missing required fields"}), 400

    payload = Payload(alert=f"Rain alert at {lat}, {lon}", sound="default", badge=1)
    topic = BUNDLE_ID

    try:
        result = apns_client.send_notification(token, payload, topic)
        print("Push sent result:", result)
        return jsonify({"status": "Push sent"}), 200
    except Exception as e:
        print("Push error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
