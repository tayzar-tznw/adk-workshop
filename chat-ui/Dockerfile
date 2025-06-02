FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port that Cloud Run expects (8080)
EXPOSE 8080

# Command to run the application
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
