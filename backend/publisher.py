# backend/app/publisher.py
import pika, json, time, requests
from datetime import datetime

RABBITMQ_HOST = "localhost"
ANOMALY_QUEUE = "anomalies_queue"

def send_anomaly_to_rabbitmq(workflow, anomaly):
    """Send detected anomaly from News Aggregator to RabbitMQ for healing."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
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

        print(f"🚨 Published REAL anomaly → {msg}")
        connection.close()
    except Exception as e:
        print(f"⚠️ [RabbitMQ Error] {e}")


def fetch_news(topic):
    """Example of real API integration (detect anomalies based on response)."""
    try:
        url = f"https://newsapi.org/v2/top-headlines?category={topic}&apiKey=YOUR_NEWS_API_KEY"
        r = requests.get(url)
        data = r.json()

        # 🧩 detect anomalies
        if r.status_code != 200:
            send_anomaly_to_rabbitmq(topic, "api_failure")
        elif not data.get("articles"):
            send_anomaly_to_rabbitmq(topic, "data_error")
        else:
            print(f"✅ {topic}: fetched {len(data['articles'])} articles")

    except Exception as e:
        print(f"❌ {topic}: {e}")
        send_anomaly_to_rabbitmq(topic, "api_failure")


def monitor_topics():
    """Continuously monitor topics for anomalies (real data-driven)."""
    topics = ["business", "technology", "sports", "entertainment"]
    while True:
        for topic in topics:
            fetch_news(topic)
        time.sleep(60)  # check every minute


if __name__ == "__main__":
    print("🚀 Monitoring News API for anomalies...")
    monitor_topics()
