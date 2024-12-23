# Use the official Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Run Functions Framework with hot-reloading
CMD ["functions-framework", "--target=handler", "--debug", "--port=8080"]
