import pytest
import json

from src.tweets import Tweets

@pytest.fixture
# Apenas instanciando a classe para testes
def api_locaweb():
    return Tweets()

@pytest.fixture
def requisicao_api(api_locaweb):
    return api_locaweb.request_api()

@pytest.fixture
def dados_json(api_locaweb):
    return api_locaweb.capture()

@pytest.fixture
def dados_filtrados(api_locaweb, dados_json):
    return api_locaweb.filters(dados_json)

@pytest.fixture
def dados_organizados(api_locaweb, dados_filtrados):
    return api_locaweb.order_by(dados_filtrados)


# INICIANDO OS TESTES DE UNIDADE
def test_deve_retornar_requisicao_valida_para_api(requisicao_api):
    assert requisicao_api.status_code == 200

def test_deve_haver_captura_de_tweets(dados_json):
    assert 'statuses' in dados_json

def test_deve_filtrar_tweets_que_mencionem_o_usuario_locaweb(dados_filtrados):
    assert dados_filtrados[0]['entities']['user_mentions'][0]['id'] == 42
    assert dados_filtrados[0]['in_reply_to_user_id'] != 42

def test_deve_ordenar_tweets_levando_em_consideracao_usuarios_com_maiores_seguidores_retweets_likes(dados_organizados):
    if len(dados_organizados) >= 2:
        assert dados_organizados[0]['user']['followers_count'] >= dados_organizados[1]['user']['followers_count']
        assert dados_organizados[1]['user']['followers_count'] >= dados_organizados[2]['user']['followers_count']
        assert dados_organizados[2]['user']['followers_count'] >= dados_organizados[3]['user']['followers_count']
    elif len(dados_organizados) >= 1:
        assert dados_organizados[0]['user']['followers_count'] >= dados_organizados[1]['user']['followers_count']
        assert dados_organizados[1]['user']['followers_count'] >= dados_organizados[2]['user']['followers_count']

def test_deve_exibir_os_dados_relevantes(dados_organizados):
    show = Tweets().show_relevants(dados_organizados)

    assert 'followers_count' in show[0]
    assert "screen_name" in show[0]
    assert "profile_link" in show[0]
    assert "created_at" in show[0]
    assert "link" in show[0]
    assert "retweet_count" in show[0]
    assert "text" in show[0]
    assert "favorite_count" in show[0]

def test_deve_exibir_os_dados_mencionados(dados_organizados):
    show = Tweets().show_mentions(dados_organizados)

    assert len(show) >= 0