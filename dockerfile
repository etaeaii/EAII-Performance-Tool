FROM python:3.11-slim

RUN apt-get update && apt-get install -y nginx supervisor

# Copy your app
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy Nginx config (route /locust/ to localhost:8089)
COPY nginx.conf /etc/nginx/nginx.conf

# Copy supervisor config to run all three processes
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
