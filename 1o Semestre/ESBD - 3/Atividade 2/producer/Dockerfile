# Use a base image with Python installed
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Python scripts and any necessary files to the container
COPY producer.py requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
# Set the command to run for the container
CMD ["python", "producer.py"]
