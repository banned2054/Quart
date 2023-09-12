# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /quart

# Add the current directory contents into the container at /app
ADD . /quart

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt

# Run run.sh when the container launches
CMD ["./run.sh"]