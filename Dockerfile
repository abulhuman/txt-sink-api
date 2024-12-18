# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . /app/

# Expose port 80
EXPOSE 80

# Run the Django development server
CMD ["python", "./cisco_test_project/manage.py", "runserver", "0.0.0.0:80"]