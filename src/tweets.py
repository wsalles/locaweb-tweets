import os
import json
import requests

def _id_user_locaweb(id_user_mentions):
    return id_user_mentions == 42


def _not_reply_to_user_locaweb(id_reply_to_user):
    return id_reply_to_user != 42


def _total_tweets(tweets):
    return len(tweets['statuses'])

class Tweets:
    def __init__(self):
        self.tweets = {}
        self.__filter_tweets = []
        self.most_relevants = []
        self.most_mentions = {}
        self.orderBy = []

    @property
    def filter_tweets(self):
        self.__filter_tweets = self.filters()
        return self.__filter_tweets

    def request_api(self):
        url = 'http://tweeps.locaweb.com.br/tweeps'
        HTTP_USERNAME = os.environ['HTTP_USERNAME']
        headers = {'username': HTTP_USERNAME}

        response = requests.request('GET', url=url, headers=headers)

        return response

    def capture(self):
        return json.loads(self.request_api().text)

    def filters(self, tweets):
        if tweets:
            # Para efeito de testes, considere que o usuário da Locaweb no Twitter tem o ID 42
            for x in range(_total_tweets(tweets)):
                try:
                    id_user_mentions = tweets['statuses'][x]['entities']['user_mentions'][0]['id']
                    id_reply_to_user = tweets['statuses'][x]['in_reply_to_user_id']

                    if _id_user_locaweb(id_user_mentions) and _not_reply_to_user_locaweb(id_reply_to_user):
                        self.__filter_tweets.append(tweets['statuses'][x])
                except IndexError:
                    pass #print(f'user_mentions.0.id not found in array {x}')
            return self.__filter_tweets
        else:
            return 'No captures were found'

    def order_by(self, data):
        self.orderBy = sorted(data,
                         key=lambda x: (x['user']['followers_count'], x['retweet_count'], x['favorite_count']),
                         reverse=True)
        return self.orderBy

    def show_relevants(self, data):
        self.most_relevants = []
        for pointer in range(len(data)):
            relevants = {
                "followers_count": data[pointer]['user']['followers_count'],
                "screen_name": data[pointer]['user']['screen_name'],
                "profile_link": "https://twitter.com/" + data[pointer]['user']['screen_name'],
                "created_at": data[pointer]['created_at'],
                "link": "https://twitter.com/" + data[pointer]['user']['screen_name'] + "/status/" +
                        data[pointer]['id_str'],
                "retweet_count": data[pointer]['retweet_count'],
                "text": data[pointer]['text'],
                "favorite_count": data[pointer]['favorite_count']
            }
            self.most_relevants.append(relevants)
        return self.most_relevants

    def show_mentions(self, data):
        self.most_mentions = {}
        for pointer in range(len(data)):
            self.most_mentions[data[pointer]['user']['screen_name']] = []
            mentions = {
                "screen_name": data[pointer]['user']['screen_name'],
                "profile_link": "https://twitter.com/" + data[pointer]['user']['screen_name'],
                "created_at": data[pointer]['created_at'],
                "favorite_count": data[pointer]['favorite_count'],
                "followers_count": data[pointer]['user']['followers_count'],
                "text": data[pointer]['text'],
                "link": "https://twitter.com/" + data[pointer]['user']['screen_name'] + "/status/" +
                        data[pointer]['id_str'],
                "retweet_count": data[pointer]['retweet_count']
            }
            self.most_mentions[data[pointer]['user']['screen_name']].append(mentions)
        return self.most_mentions
