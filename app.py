from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    print("Received request:", data)
    return jsonify({"status": "OK", "message": "Received"}), 200

if __name__ == '__main__':
    app.run(debug=True)
