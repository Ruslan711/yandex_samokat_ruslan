FROM mcr.microsoft.com/playwright/python:v1.62.0
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["pytest", "--browser", "chromium"]