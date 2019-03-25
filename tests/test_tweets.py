import pytest
import json
import requests

from src.tweets import Tweets


@pytest.fixture
# Apenas instanciando a classe para testes
def api_locaweb():
    return Tweets()

@pytest.fixture
def dados_capturados():
    return Tweets().capture()

@pytest.fixture
def dados_json(dados_capturados):
    return json.loads(dados_capturados.text)

def test_deve_retornar_requisicao_valida_para_api(dados_capturados):
    assert dados_capturados.status_code == 200

def test_deve_haver_captura_de_tweets(dados_json):
    assert 'statuses' in dados_json

def test_deve_filtrar_tweets_que_mencionem_o_usuario_locaweb(api_locaweb, dados_json):
    filtros = api_locaweb.filters(dados_json)

    assert filtros[0]['entities']['user_mentions'][0]['id'] == 42
    assert filtros[0]['in_reply_to_user_id'] != 42












# @pytest.fixture
# def api_locaweb():
#     url = 'http://tweeps.locaweb.com.br/tweeps'
#     headers = {'username': 'wallace_robinson@hotmail.com'}
#     return requests.request('GET', url=url, headers=headers)
# @pytest.fixture
# def resposta_api_json(api_locaweb):
#     return json.loads(api_locaweb.text)
#
#
# def test_deve_retornar_http_200_usando_api_locaweb(api_locaweb):
#     assert api_locaweb.status_code == 200
#
# def test_deve_capturar_os_tweets_usando_api_locaweb(resposta_api_json):
#     assert 'statuses' in resposta_api_json
#
# def test_se_vai_filtrar_o_usuario_da_locaweb(resposta_api_json):
#     filtros = []
#     if resposta_api_json:
#         # Para efeito de testes, considere que o usuário da Locaweb no Twitter tem o ID 42
#         for x in range(len(resposta_api_json['statuses'])):
#             try:
#                 id_user_mentions = resposta_api_json['statuses'][x]['entities']['user_mentions'][0]['id']
#                 id_reply_to_user = resposta_api_json['statuses'][x]['in_reply_to_user_id']
#
#                 if (id_user_mentions == 42) and (id_reply_to_user != 42):
#                     filtros.append(resposta_api_json['statuses'][x])
#             except IndexError:
#                 pass
#
#         assert filtros[0]['entities']['user_mentions'][0]['id'] == 42
#         assert filtros[1]['entities']['user_mentions'][0]['id'] == 42
#
# def test_deve_ordenar_tweets_levando_em_consideracao_usuarios_com_maiores_seguidores_retweets_likes(resposta_api_json):
#     ordem = sorted(resposta_api_json['statuses'],
#                           key=lambda x: (x['user']['followers_count'], x['retweet_count'], x['favorite_count']),
#                           reverse=True)
#     if len(ordem) >= 2:
#         assert ordem[0]['user']['followers_count'] >= ordem[1]['user']['followers_count']
#         assert ordem[1]['user']['followers_count'] >= ordem[2]['user']['followers_count']
#         assert ordem[2]['user']['followers_count'] >= ordem[3]['user']['followers_count']
#     elif len(ordem) >= 1:
#         assert ordem[0]['user']['followers_count'] >= ordem[1]['user']['followers_count']
#         assert ordem[1]['user']['followers_count'] >= ordem[2]['user']['followers_count']
#     else:
#         pass
#
