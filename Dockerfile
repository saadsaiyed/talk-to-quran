# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt first to leverage Docker caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Expose the port the app will run on
EXPOSE 8000

# Run the Flask app using Waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "app:app"]
