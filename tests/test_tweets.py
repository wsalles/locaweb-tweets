import pytest
import json
import requests

@pytest.fixture
def api_locaweb():
    url = 'http://tweeps.locaweb.com.br/tweeps'
    headers = {'username': 'wallace_robinson@hotmail.com'}
    return requests.request('GET', url=url, headers=headers)

def test_deve_retornar_http_200_usando_api_locaweb(api_locaweb):
    assert api_locaweb.status_code == 200

def test_deve_capturar_os_tweets_usando_api_locaweb(api_locaweb):
    dados_json = json.loads(api_locaweb.text)
    assert 'statuses' in dados_json

def test_se_vai_filtrar_o_usuario_da_locaweb(api_locaweb):
    dados_json = json.loads(api_locaweb.text)
    filtros = []
    if dados_json:
        # Para efeito de testes, considere que o usuário da Locaweb no Twitter tem o ID 42
        for x in range(len(dados_json['statuses'])):
            try:
                id_user_mentions = dados_json['statuses'][x]['entities']['user_mentions'][0]['id']
                id_reply_to_user = dados_json['statuses'][x]['in_reply_to_user_id']

                if (id_user_mentions == 42) and (id_reply_to_user != 42):
                    filtros.append(dados_json['statuses'][x])
            except IndexError:
                pass

        assert filtros[0]['entities']['user_mentions'][0]['id'] == 42
        assert filtros[1]['entities']['user_mentions'][0]['id'] == 42

def test_deve_ordenar_os_tweets_levando_em_consideracao_os_usuarios_com_maiores_seguidores_retweets_likes(api_locaweb):
    dados_json = json.loads(api_locaweb.text)
    ordem = sorted(dados_json['statuses'],
                          key=lambda x: (x['user']['followers_count'], x['retweet_count'], x['favorite_count']),
                          reverse=True)
    assert ordem[0]['user']['followers_count'] >= ordem[1]['user']['followers_count']