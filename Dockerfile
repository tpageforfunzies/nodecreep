FROM python:3

ADD ./creep.py ./creep.py
ADD ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

CMD ["python",  "creep.py"]