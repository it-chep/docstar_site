FROM python:3.9
WORKDIR /home/maxim/PycharmProjects/new_site/new_site
COPY requirements.txt .
RUN apt-get -y update
RUN apt-get -y install vim nano
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]