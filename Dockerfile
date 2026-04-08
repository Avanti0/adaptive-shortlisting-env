FROM python:3.10-slim

WORKDIR /app

# Copy the entire project to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the OpenEnv server using the correct module path
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
