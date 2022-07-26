FROM python:3.10.5

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD evoker /evoker

CMD ["python", "evoker", "predict", "a", "beautiful"]