# Use an official Python runtime as a parent image
FROM python:3.12

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the working directory in the container
WORKDIR /app

# First, copy only the requirements.txt file to leverage Docker cache
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Now, copy the rest of your application's code into the container
COPY . .

# Command to run the application
CMD ["/bin/bash", "docker-entrypoint.sh"]
