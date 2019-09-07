FROM python:3.7
RUN apt-get -qq update && apt-get -qq install netcat

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "run.py"]
