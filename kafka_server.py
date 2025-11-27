from flask import Flask, jsonify, request
from collections import defaultdict

app = Flask(__name__)
messages = defaultdict(list)

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    messages['youtube-stats'].append(data)
    print(f"✅ SENT: {data['title'][:30]} | Views: {data['views']:,}")
    return 'OK', 200

@app.route('/consume')
def consume():
    return jsonify(messages['youtube-stats'])

if __name__ == '__main__':
    print("🚀 Kafka Server running on http://10.178.7.241:5000")
    app.run(host='0.0.0.0', port=5000)
