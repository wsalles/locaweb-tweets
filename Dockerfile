FROM python

ENV HTTP_USERNAME='wallace_robinson@hotmail.com'

RUN mkdir locaweb-tweets
WORKDIR /locaweb-tweets

COPY ./src/ ./src
COPY ./tests/ ./tests
COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["python3", "/locaweb-tweets/src/app.py"]
