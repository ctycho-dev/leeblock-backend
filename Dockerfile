FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure the start script is executable
RUN chmod +x start.sh

# Expose port 80
EXPOSE 8000

CMD ["./start.sh"]
