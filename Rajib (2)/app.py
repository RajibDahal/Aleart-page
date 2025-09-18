from flask import Flask, render_template, request, jsonify
from pywebpush import webpush, WebPushException
import json

app = Flask(__name__)

# VAPID keys (replace with your own)
VAPID_PUBLIC_KEY = "YOUR_PUBLIC_KEY"
VAPID_PRIVATE_KEY = "YOUR_PRIVATE_KEY"
VAPID_CLAIMS = {"sub": "mailto:you@example.com"}

# Store subscriptions
subscriptions = []

@app.route("/")
def index():
    return render_template("index.html", vapid_public_key=VAPID_PUBLIC_KEY)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    subscription = request.json
    subscriptions.append(subscription)
    return jsonify({"status": "subscribed"})

@app.route("/send_notification", methods=["POST"])
def send_notification():
    data = request.json
    payload = {"title": data.get("title", "🚨 Alert"), "body": data.get("body", "")}
    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
        except WebPushException as ex:
            print("Error sending notification:", repr(ex))
    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
