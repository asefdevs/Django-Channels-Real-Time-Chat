# Use the official Python image as a base
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .

# Copy entrypoint.sh into a directory included in the $PATH
COPY entrypoint.sh /usr/local/bin/

# Set execute permissions on entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set entrypoint to execute the entrypoint.sh script directly
ENTRYPOINT ["entrypoint.sh"]

# Expose the port your Django app runs on
EXPOSE 8000
