FROM python

ENV HTTP_USERNAME='wallace_robinson@hotmail.com'

RUN mkdir locaweb-tweets
WORKDIR /locaweb-tweets

COPY ./src/ ./src
COPY ./templates/ ./templates
COPY ./tests/ ./tests
COPY ./requirements.txt .
COPY ./app.py .

RUN pip3 install -r requirements.txt

CMD [ "python3", "./app.py" ]
