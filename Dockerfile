# Base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install JupyterHub
RUN pip install jupyterhub

# Copy the JupyterHub configuration file
COPY . .

# Expose the JupyterHub port
EXPOSE 8000

# Start JupyterHub
CMD ["jupyterhub", "--config=jupyterhub_config.py"]
