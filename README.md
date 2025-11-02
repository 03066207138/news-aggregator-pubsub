# 📰 News Aggregator — Pub/Sub System

This project implements a real-time **Publisher-Subscriber News Aggregator** using **RabbitMQ**, **Flask**, and **React**.

## 🚀 Features
- Publishers post news articles based on topics.
- Subscribers receive real-time updates.
- Supports topic-based subscriptions (sports, tech, politics, etc.).
- RabbitMQ message broker for communication.
- REST APIs for publishing and subscribing.

## 🧱 Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** React.js
- **Message Broker:** RabbitMQ
- **Database:** (optional) PostgreSQL / MongoDB

## 🛠️ Setup
### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
