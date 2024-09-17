FROM python:3.12-alpine3.20
LABEL maintainer="smartcrackerprezents@gmail.com"
LABEL maintainer_telegram="@aaurorin"

WORKDIR /usr/src/compliments-bot

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "./main.py"]
