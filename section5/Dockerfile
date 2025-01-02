FROM python:3.12

EXPOSE 5001

WORKDIR /app

RUN pip install flask

COPY . /app/

CMD ["flask","run", "--host", "0.0.0.0"]