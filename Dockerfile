FROM python:3.6

ENV PYTHONPATH /facenet/src

ADD . datasets/ facenet/ models/ /

RUN pip3 install -r ./requirements.txt && \
    rm ./requirements.txt 

