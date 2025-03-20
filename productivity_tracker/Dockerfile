From python:3.10

WORKDIR /app
 
COPY . .

RUN pip install -r requirements.txt .

COPY .env .

CMD ["python", "agent.py"]
