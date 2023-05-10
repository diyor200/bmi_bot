# Use official Python image as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container to /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application into container att /app
COPY . /app

# Run the to start bot
CMD ["python", "app.py"]
