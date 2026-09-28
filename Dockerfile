# Use an official Python runtime as a parent image
FROM python:3.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy dependency definition file to working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy current directory contents into container at /app
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Command to run the application binding to all interfaces
CMD ["python", "app.py"]