FROM python:3.9.5

WORKDIR /app

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt

COPY ./src .
RUN chmod +x /app/entrypoint.sh

CMD ["entrypoint.sh"]