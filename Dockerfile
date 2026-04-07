FROM python:3.10-slim

WORKDIR /app

# Copy the entire project to the container
COPY . /app

# Install any dependencies (currently none but included for future use)
RUN pip install --no-cache-dir -r requirements.txt

# Run the inference script by default
CMD ["python", "inference.py"]
