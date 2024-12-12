# Use a Linux base image with Python
FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Fabric AI
RUN curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-linux-amd64 > /usr/local/bin/fabric && \
    chmod +x /usr/local/bin/fabric

# Set environment variables
ENV FABRIC_OUTPUT_PATH=/app/output

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Make both scripts executable
RUN chmod +x /app/scripts/yt_extract_and_save.sh /app/scripts/web_extract_and_save.sh

# Verify permissions
RUN ls -l /app/scripts/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit will run on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app/app.py"]