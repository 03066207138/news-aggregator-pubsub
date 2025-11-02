# ============================================================
# 🌍 News Aggregator Publisher — Anomaly Publisher to RabbitMQ
# ============================================================

import pika
import json
import time
import requests
import os
from datetime import datetime

# ------------------------------------------------------------
# 🔹 Environment Configuration
# ------------------------------------------------------------
# RabbitMQ connection (local for dev, Render for prod)
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")

# NewsAPI key (securely loaded)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWS_API_KEY")

# RabbitMQ Queue for anomalies
ANOMALY_QUEUE = "anomalies_queue"


# ------------------------------------------------------------
# 🔹 Helper: Connect to RabbitMQ
# ------------------------------------------------------------
def get_connection():
    """Create and return a RabbitMQ connection."""
    try:
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        print("🐇 [Connected] RabbitMQ connection established.")
        return connection
    except Exception as e:
        print(f"❌ [Connection Failed] RabbitMQ not reachable → {e}")
        return None


# ------------------------------------------------------------
# 🔹 Send anomaly to RabbitMQ
# ------------------------------------------------------------
def send_anomaly_to_rabbitmq(workflow, anomaly):
    """Send detected anomaly message to RabbitMQ."""
    connection = get_connection()
    if not connection:
        print("⚠️ Skipping publish because RabbitMQ connection failed.")
        return

    try:
        channel = connection.channel()
        channel.queue_declare(queue=ANOMALY_QUEUE, durable=True)

        msg = {
            "workflow": workflow,
            "anomaly": anomaly,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        channel.basic_publish(
            exchange="",
            routing_key=ANOMALY_QUEUE,
            body=json.dumps(msg),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f"🚨 [Published Anomaly] → {msg}")
        connection.close()

    except Exception as e:
        print(f"⚠️ [Publish Error] {e}")
        try:
            connection.close()
        except:
            pass


# ------------------------------------------------------------
# 🔹 Fetch and analyze news from API
# ------------------------------------------------------------
def fetch_news(topic):
    """Fetch latest news using NewsAPI and detect anomalies."""
    try:
        url = f"https://newsapi.org/v2/top-headlines?category={topic}&apiKey={NEWS_API_KEY}&country=us"
        print(f"🌐 Fetching news for topic: {topic}")
        r = requests.get(url, timeout=10)
        data = r.json()

        # 🧠 Detect anomalies
        if r.status_code != 200:
            print(f"❌ API error {r.status_code} for topic: {topic}")
            send_anomaly_to_rabbitmq(topic, "api_failure")

        elif not data.get("articles"):
            print(f"⚠️ No articles found for {topic}")
            send_anomaly_to_rabbitmq(topic, "empty_articles")

        else:
            count = len(data["articles"])
            print(f"✅ {topic}: {count} articles fetched successfully.")
            # Optional: publish a 'health' message here later

    except requests.exceptions.RequestException as e:
        print(f"🌐 [Timeout/Error] {topic}: {e}")
        send_anomaly_to_rabbitmq(topic, "api_timeout")

    except Exception as e:
        print(f"❌ Unexpected error for {topic}: {e}")
        send_anomaly_to_rabbitmq(topic, "api_exception")


# ------------------------------------------------------------
# 🔹 Continuous Monitoring Loop
# ------------------------------------------------------------
def monitor_topics():
    """Continuously monitor NewsAPI for anomalies."""
    topics = ["business", "technology", "sports", "entertainment"]

    print("🚀 Monitoring News API for anomalies...\n")

    while True:
        for topic in topics:
            fetch_news(topic)
            # short delay to avoid NewsAPI rate limit
            time.sleep(2)
        print("⏳ Sleeping for 60 seconds before next cycle...\n")
        time.sleep(60)


# ------------------------------------------------------------
# 🔹 Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    print("🔧 Starting News Aggregator Publisher...")
    connection = get_connection()
    if connection:
        connection.close()
    monitor_topics()
