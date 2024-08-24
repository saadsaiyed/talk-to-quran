# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port specified in the .env file
EXPOSE $PORT

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port", "$PORT"]
