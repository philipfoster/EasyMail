FROM python:3

COPY . /app
WORKDIR /APP

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["src/main.py"]
