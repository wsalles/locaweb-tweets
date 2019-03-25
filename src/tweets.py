import json
import requests

def _id_user_locaweb(id_user_mentions):
    return id_user_mentions == 42


def _not_reply_to_user_locaweb(id_reply_to_user):
    return id_reply_to_user != 42


class Tweets:
    def __init__(self):
        self.tweets = {}
        self.__filter_tweets = []
        self.most_relevants = []
        self.most_mentions = {}
        self.orderBy = []

    @property
    def filter_tweets(self):
        return self.__filter_tweets

    def capture(self):
        url = 'http://tweeps.locaweb.com.br/tweeps'
        headers = {'username': 'wallace_robinson@hotmail.com'}

        response = requests.request('GET', url=url, headers=headers).text

        self.tweets = json.loads(response)

        return self.tweets

    def filters(self):
        if self.tweets:
            # Para efeito de testes, considere que o usuário da Locaweb no Twitter tem o ID 42
            for x in range(len(self.tweets['statuses'])):
                try:
                    id_user_mentions = self.tweets['statuses'][x]['entities']['user_mentions'][0]['id']
                    id_reply_to_user = self.tweets['statuses'][x]['in_reply_to_user_id']

                    if _id_user_locaweb(id_user_mentions) and _not_reply_to_user_locaweb(id_reply_to_user):
                        self.__filter_tweets.append(self.tweets['statuses'][x])
                except IndexError:
                    print(f'user_mentions.0.id not found in array {x}')
            return self.__filter_tweets
        else:
            return 'No captures were found'

    def order_by(self):
        self.orderBy = sorted(self.__filter_tweets,
                         key=lambda x: (x['user']['followers_count'], x['retweet_count'], x['favorite_count']),
                         reverse=True)
        return self.orderBy

    def show_relevants(self):
        self.most_relevants = []
        for x in range(len(self.orderBy)):
            relevants = {
                "followers_count": self.orderBy[x]['user']['followers_count'],
                "screen_name": self.orderBy[x]['user']['screen_name'],
                "profile_link": "https://twitter.com/" + self.orderBy[x]['user']['screen_name'],
                "created_at": self.orderBy[x]['created_at'],
                "link": "https://twitter.com/" + self.orderBy[x]['user']['screen_name'] + "/status/" +
                        self.orderBy[x]['id_str'],
                "retweet_count": self.orderBy[x]['retweet_count'],
                "text": self.orderBy[x]['text'],
                "favorite_count": self.orderBy[x]['favorite_count']
            }
            self.most_relevants.append(relevants)
        return self.most_relevants

    def show_mentions(self):
        self.most_mentions = {}
        for x in range(len(self.orderBy)):
            self.most_mentions[self.orderBy[x]['user']['screen_name']] = []
            mentions = {
                "screen_name": self.orderBy[x]['user']['screen_name'],
                "profile_link": "https://twitter.com/" + self.orderBy[x]['user']['screen_name'],
                "created_at": self.orderBy[x]['created_at'],
                "favorite_count": self.orderBy[x]['favorite_count'],
                "followers_count": self.orderBy[x]['user']['followers_count'],
                "text": self.orderBy[x]['text'],
                "link": "https://twitter.com/" + self.orderBy[x]['user']['screen_name'] + "/status/" +
                        self.orderBy[x]['id_str'],
                "retweet_count": self.orderBy[x]['retweet_count']
            }
            self.most_mentions[self.orderBy[x]['user']['screen_name']].append(mentions)
        return self.most_mentions
