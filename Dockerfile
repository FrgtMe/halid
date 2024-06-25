# Base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY . .

# Expose the JupyterHub port
ENTRYPOINT ["python", "m.py"]
