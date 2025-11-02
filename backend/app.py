# ============================================================
# 📰 News Aggregator + 🐇 RabbitMQ + 🤖 AI Healer Integration
# ============================================================

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import pika
import json
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================================
# 🔧 Configuration
# ============================================================
NEWS_API_KEY = "fe1e6bcbbf384b3e9220a7a1138805e0"
RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'news_exchange'
EXCHANGE_TYPE = 'direct'
ANOMALY_QUEUE = "anomalies_queue"
LOG_FILE = "news_activity.log"

# ============================================================
# 🪵 Utility — Log Activity
# ============================================================
def log_activity(message):
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

# ============================================================
# 🐇 Publish Message to RabbitMQ (Normal News)
# ============================================================
def publish_message(topic, message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE, durable=True)

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=topic,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        log_activity(f"✅ [Publisher] Sent to topic '{topic}': {message['title']}")
        connection.close()
    except Exception as e:
        log_activity(f"❌ [Publisher] Error publishing message: {e}")

# ============================================================
# 🐇 Consume Messages (Subscribers)
# ============================================================
def consume_messages(topic):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        queue_name = f"{topic}_queue"

        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE, durable=True)
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=topic)

        def callback(ch, method, properties, body):
            msg = json.loads(body)
            log_activity(f"📩 [Subscriber] Received from '{topic}': {msg['title']}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        log_activity(f"🔔 [Subscriber] Listening on topic '{topic}' ...")
        channel.start_consuming()

    except Exception as e:
        log_activity(f"❌ [Subscriber] Error for topic '{topic}': {e}")

# ============================================================
# 🚦 Routes
# ============================================================

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "News Aggregator running", "RabbitMQ": RABBITMQ_HOST}), 200

@app.route("/news", methods=["GET"])
def get_news():
    topic = request.args.get("topic", "general")
    url = f"https://newsapi.org/v2/top-headlines?category={topic}&apiKey={NEWS_API_KEY}"

    log_activity(f"🌐 Fetching news for topic: {topic}")
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return jsonify({"articles": data.get("articles", [])})
        else:
            return jsonify({"error": "News API failed", "message": data.get("message", "Unknown error")}), 500
    except Exception as e:
        log_activity(f"❌ [News API] Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/subscribe", methods=["POST"])
def subscribe():
    topic = request.json.get("topic")
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    thread = threading.Thread(target=consume_messages, args=(topic,), daemon=True)
    thread.start()

    log_activity(f"👂 Subscribed to topic: {topic}")
    return jsonify({"message": f"Subscribed to {topic} successfully!"}), 200

# ============================================================
# 🧠 Publish News + Detect Anomalies
# ============================================================
@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    topic = data.get("topic")
    title = data.get("title")
    content = data.get("content", "")
    timestamp = data.get("timestamp", datetime.utcnow().isoformat())

    if not topic or not title or not content:
        return jsonify({"error": "Topic, title, and content are required"}), 400

    msg = {"title": title, "content": content, "timestamp": timestamp}

    # Step 1️⃣ Publish normal news
    publish_message(topic, msg)

    # Step 2️⃣ Detect anomalies
    anomaly_type = None
    details = {}

    if len(content.strip()) < 30:
        anomaly_type = "workflow_delay"
        details = {"reason": "Short or empty content"}
    elif any(x in title.lower() for x in ["error", "fail", "outage", "crash"]):
        anomaly_type = "api_failure"
        details = {"reason": f"Detected keyword in title: {title}"}
    elif not title[0].isupper():
        anomaly_type = "data_error"
        details = {"reason": "Title not properly formatted"}

    # Step 3️⃣ Publish anomaly to healer queue
    if anomaly_type:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=ANOMALY_QUEUE, durable=True)

            anomaly = {
                "workflow": "news_pipeline",
                "anomaly": anomaly_type,
                "details": details,
                "source": topic,
                "timestamp": timestamp
            }

            channel.basic_publish(
                exchange="",
                routing_key=ANOMALY_QUEUE,
                body=json.dumps(anomaly),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            connection.close()

            log_activity(f"🚨 [Anomaly] Sent → {anomaly_type}: {details}")

        except Exception as e:
            log_activity(f"❌ [Anomaly] Failed to send anomaly: {e}")

    else:
        log_activity(f"🟢 [OK] No anomaly detected for '{title}'")

    return jsonify({
        "status": "ok",
        "topic": topic,
        "anomaly": anomaly_type or "none",
        "message": "Published successfully"
    }), 200

# ============================================================
# 🚀 Start Server
# ============================================================
if __name__ == "__main__":
    log_activity("🚀 News Aggregator started")
    app.run(debug=True, host="0.0.0.0", port=5000)
