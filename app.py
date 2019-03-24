import requests, json

url = 'http://tweeps.locaweb.com.br/tweeps'
headers = {'username': 'wallace_robinson@hotmail.com'}

response = requests.request('GET', url=url, headers=headers).text

tweets = json.loads(response)

# Para efeito de testes, considere que o usuário da Locaweb no Twitter tem o ID 42
filter_tweets = []
for x in range(len(tweets['statuses'])):
    try:
        id_user_mentions = tweets['statuses'][x]['entities']['user_mentions'][0]['id']
        id_reply_to_user = tweets['statuses'][x]['in_reply_to_user_id']

        if (id_user_mentions == 42) and (id_reply_to_user != 42):
            filter_tweets.append(tweets['statuses'][x])
    except IndexError as e:
        pass #print(e)

"""
Considerando os padrões de urgência para o problema, os tweets devem ser ordenados de acordo com as seguintes prioridades:
1) Usuários com mais seguidores
2) Tweets que tenham mais retweets
3) Tweet com mais likes
"""

orderBy = sorted(filter_tweets, key=lambda x: (x['user']['followers_count'], x['retweet_count'], x['favorite_count']),
                                reverse=True)


most_relevants = []
for x in range(len(orderBy)):
    relevants = {
                "followers_count": orderBy[x]['user']['followers_count'],
                "screen_name": orderBy[x]['user']['screen_name'],
                "profile_link": "https://twitter.com/" + orderBy[x]['user']['screen_name'],
                "created_at": orderBy[x]['created_at'],
                "link": "https://twitter.com/" + orderBy[x]['user']['screen_name'] + "/status/" + orderBy[x]['id_str'],
                "retweet_count": orderBy[x]['retweet_count'],
                "text": orderBy[x]['text'],
                "favorite_count": orderBy[x]['favorite_count']
    }
    most_relevants.append(relevants)


most_mentions = []
for x in range(len(orderBy)):
    mentions = {orderBy[x]['user']['screen_name']: [{
                "screen_name": orderBy[x]['user']['screen_name'],
                "profile_link": "https://twitter.com/" + orderBy[x]['user']['screen_name'],
                "created_at": orderBy[x]['created_at'],
                "favorite_count": orderBy[x]['favorite_count'],
                "followers_count": orderBy[x]['user']['followers_count'],
                "text": orderBy[x]['text'],
                "link": "https://twitter.com/" + orderBy[x]['user']['screen_name'] + "/status/" + orderBy[x]['id_str'],
                "retweet_count": orderBy[x]['retweet_count']
                }]
    }
    most_mentions.append(mentions)

#ul = {'statuses': orderBy}
ul = json.dumps({'statuses': orderBy})
mr = json.dumps(most_relevants)
mm = json.dumps(most_mentions)

print(ul)
print(mr)
print(mm)





#print(tweets['statuses'][0]['entities']['user_mentions'][0])
#print(tweets['statuses'][1]['entities']['user_mentions'][0])


# d = {'status': [
#     {'name': 'locaweb', 'id': 0, 'setup': [{'status': 'running', 'process': 'ragnarok.exe'}]},
#     {'name': 'locaweb', 'id': 1, 'setup': [{'status': 'running', 'process': 'ragnarok.exe'}]},
#     {'name': 'Lucas', 'id': 2, 'setup': []},
#     {'name': 'locaweb', 'id': 3, 'setup': [{'status': 'crashed', 'process': 'grandchase.exe'}]},
#     {'name': 'locaweb', 'id': 4, 'setup': [{'status': 'running', 'process': 'cabal.exe'}]},
#     {'name': 'Wallace', 'id': 5, 'setup': [{'status': 'running', 'process': 'ragnarok.exe'}]},
#     {'name': 'locaweb', 'id': 6, 'setup': []},
#     ]
#     }
# print(d['status'])
#
# n = []
# for x in range(len(d['status'])):
#     try:
#         if d['status'][x]['setup'][0]['process']:
#             n.append(d['status'][x])
#     except:
#         pass
#
# #n = [x for x in d['status'] if x['setup'][0]['process'] == 'locaweb']
#
# ln = json.dumps(n)
#
# print(ln)