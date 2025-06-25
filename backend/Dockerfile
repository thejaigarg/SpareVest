# 1. Start from the official Python 3.11 image
FROM python:3.11-slim

# 2. Set environment variables for safer Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set a working directory INSIDE the container (will be called /app)
WORKDIR /app

# 4. Copy only requirements first (for efficient Docker caching)
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy the rest of your project code into /app
COPY . .

# 6. Expose the port (so outside can access your app)
EXPOSE 8000

# 7. Command to run your app (adjust path to your main.py if different)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]