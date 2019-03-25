import json

from flask import Flask, render_template
from flask_restful import Api, Resource

from src.tweets import Tweets

app = Flask(__name__)
api = Api(app)

def refreshData():
    # Chama o método de captura
    c = tweets.capture()
    # Chama o método para filtrar os tweets para usuários locaweb
    f = tweets.filters(c)
    # Método para Ordenar: 1) Usuários com mais seguidores. 2) Tweets que tenham mais retweets. 3) Tweet com mais likes.
    return tweets.order_by(f)

@app.route('/')
def index():
    # Pagina com interface ao usuario
    return render_template('index.html')

class MostRelevants(Resource):
    def get(self):
        r = refreshData()
        return tweets.show_relevants(r)

class MostMentions(Resource):
    def get(self):
        r = refreshData()
        return tweets.show_mentions(r)


if __name__ == '__main__':
    # Instância a classe Tweets
    tweets = Tweets()

api.add_resource(MostRelevants, '/most_relevants')
api.add_resource(MostMentions, '/most_mentions')

app.run(debug=True, host='0.0.0.0', port=3333)