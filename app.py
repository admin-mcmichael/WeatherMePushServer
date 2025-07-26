from flask import Flask, request, jsonify
from apns2.client import APNsClient
from apns2.payload import Payload
import os

app = Flask(__name__)

# Load from environment
APNS_KEY_PATH = 'AuthKey.p8'
APNS_KEY_ID = os.getenv('APNS_KEY_ID')
TEAM_ID = os.getenv('TEAM_ID')
BUNDLE_ID = os.getenv('BUNDLE_ID')
DEVICE_TOKEN = os.getenv('DEVICE_TOKEN')

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    alert = data.get("alert", "Rain alert!")

    try:
        # Prepare push notification payload
        payload = Payload(alert=alert, sound="default", badge=1)
        
        # Connect to APNs
        client = APNsClient(APNS_KEY_PATH, use_sandbox=True, team_id=TEAM_ID, key_id=APNS_KEY_ID)
        
        # Send notification
        result = client.send_notification(DEVICE_TOKEN, payload, topic=BUNDLE_ID)
        print("Push sent result:", result)
        return jsonify({"status": "Push sent"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
