FROM python:3

WORKDIR /usr/src/app

COPY ./Docker/requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY .. .

RUN pip install "apache-airflow[celery]==2.7.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.1/constraints-3.8.txt"

RUN chmod +x ./
#RUN docker-compose up
RUN airflow db init
CMD ["airflow", "scheduler"]

#CMD ["airflow", "webserver"]
CMD ["airflow", "dags", "-h"]
CMD ["airflow", "dags", "trigger", "./dags/main_airflow.py"]

#CMD ["ls"]
#CMD ["docker-compose", "up"]
#CMD ["python", "./dags/main_airflow.py"]