FROM shenweimin/alpine-py3:3.6
COPY ./requirements.txt /tmp/
WORKDIR /mnt/

RUN pip install -r /tmp/requirements.txt
ENTRYPOINT ["python"]
CMD ["flaskapp.py"]
