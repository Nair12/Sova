FROM ubuntu:latest
LABEL authors="nairp"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

ENTRYPOINT ["top", "-b"]