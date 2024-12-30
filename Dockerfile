FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN apt-get -y update
RUN apt-get -y install vim nano
RUN pip install -r requirements.txt
COPY . .
RUN ["python", "manage.py", "collectstatic", "--noinput"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]