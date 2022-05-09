# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5005
EXPOSE 5005/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY server.py .
RUN mkdir templates
RUN mkdir static
COPY templates/ ./templates
COPY static/ ./static
COPY secret.txt .

# Specify the command to run on container start
CMD [ "python", "./server.py" ]