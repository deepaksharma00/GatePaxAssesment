# Use the official Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# COPY .env /app/.env

# Copy the application code and environment file
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start the Flask application
CMD ["functions-framework", "--target=handler", "--port=8080"]


