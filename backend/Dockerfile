# =============================================
# 🐍 Flask Backend - Render Deployment
# =============================================
FROM python:3.11-slim

WORKDIR /backend

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose Flask port
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
