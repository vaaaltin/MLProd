FROM python:3.7

COPY requirements.txt requirements.txt

RUN wget https://s3.amazonaws.com/content.udacity-data.com/courses/nd188/flower_data.zip
RUN apt-get update
RUN apt-get install unzip -y

RUN unzip flower_data.zip
RUN rm flower_data.zip

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "main.py"]
