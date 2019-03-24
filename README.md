# Problema da listagem de Tweets

Você deve assumir o seguinte problema hipotético:

```
A Locaweb está planejando uma maneira de prover suporte e iniciar
protocolos para quem reclamar de seus produtos via Twitter. A idéia é prover
uma forma para listar os tweets atuais mais relevantes e os usuários que mais
mencionam a Locaweb em tempo real.
```

## Regras

### Tweets elegíveis

Para um tweet ser elegível para a lista, ele deve atender a todos os seguintes critérios:

* tweet que mencione o usuário da Locaweb
* tweet que não é reply para tweets da Locaweb

Os tweets que não seguirem os critérios acima **não** devem estar na lista.

### Informações e Ordenação

Considerando os padrões de urgência para o problema, os tweets devem
ser ordenados de acordo com as seguintes prioridades:

1. Usuários com mais seguidores
2. Tweets que tenham mais retweets
3. Tweet com mais likes

Os resultados ordenados devem conter as seguintes informações:

* screen_name (@usuario) que fez o tweet
* Número de seguidores do autor
* Número de retweets
* Número favorites do tweet
* Conteúdo do tweet
* Data e hora
* Link para o perfil
* Link para o tweet

## Implementação

Para simplificar a autenticação do Twitter e evitar limites, você **deve**
usar as respostas mockadas da API de busca do Twitter nesta URL:

http://tweeps.locaweb.com.br/tweeps

Essa API segue o mesmo formato descrito na documentação do Twitter em:

https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html

Esta API não aceita os mesmos filtros via query string que a API verdadeira
aceita.

Para autenticar, envie um header HTTP chamado `Username` com o seu e-mail.
O valor desse header deve ser configurável através da variável de ambiente
`HTTP_USERNAME`.

Considere apenas os tweets retornados em um request para a API, ou seja, não é
necessário varrer os links das próximas páginas.

Para efeito de testes, considere que o usuário da Locaweb no Twitter tem o ID 42.

### Recursos do sistema

O sistema deve expor os recursos **em formato JSON**.

Para mostrar os tweets mais relevantes, use a URL `/most_relevants`
**com o seguinte formato**:

```
[
   {
      "followers_count" : 840,
      "screen_name" : "vandervort_raven_i",
      "profile_link" : "https://twitter.com/vandervort_raven_i",
      "created_at" : "Mon Sep 24 03:35:21 +0000 2012",
      "link" : "https://twitter.com/vandervort_raven_i/status/812382",
      "retweet_count" : 0,
      "text" : "We need to naviga @locaweb ",
      "favorite_count" : 175
   },
   {
      "followers_count" : 834,
      "screen_name" : "deja_eichmann",
      "profile_link" : "https://twitter.com/deja_eichmann",
      "favorite_count" : 0,
      "text" : "Try to reboot the @locaweb ndex the virtual alarm!",
      "link" : "https://twitter.com/deja_eichmann/status/517664",
      "created_at" : "Mon Sep 24 03:35:21 +0000 2012",
      "retweet_count" : 6
   },

   ...
]
```

Para mostrar os usuários que mais mencionaram a locaweb, use a URL
`/most_mentions` **com o seguinte formato**:

```
[
   {
      "nolan_dorris" : [
         {
            "created_at" : "Mon Sep 24 03:35:21 +0000 2012",
            "profile_link" : "https://twitter.com/nolan_dorris",
            "favorite_count" : 274,
            "screen_name" : "nolan_dorris",
            "followers_count" : 951,
            "link" : "https://twitter.com/nolan_dorris/status/574184",
            "text" : "Use the multi-byte AGP system, then you can calculate t @locaweb ",
            "retweet_count" : 0
         }
      ]
   },
   {
      "imogene_kovacek" : [
         {
            "screen_name" : "imogene_kovacek",
            "profile_link" : "https://twitter.com/imogene_kovacek",
            "created_at" : "Mon Sep 24 03:35:21 +0000 2012",
            "favorite_count" : 140,
            "followers_count" : 735,
            "text" : "You can't hack the hard drive without backing up the optical @locaweb ",
            "link" : "https://twitter.com/imogene_kovacek/status/823386",
            "retweet_count" : 0
         }
      ]
   },

   ...
]
```

Adicionar mais campos é opcional, mas todos os campos mostrados nos exemplos
**devem** estar presentes.

O recurso `most_mentions` deve retornar os tweets agregados por usuário,
aplicando os mesmos critérios de ordenação dos mais relevantes.

Lembre-se que escrever testes automatizados é indispensável.

## Entrega do projeto

O projeto deve ser entregue em link (recomendamos o uso do https://wetransfer.com)
para um único arquivo compactado (zip, tar.gz, etc), contendo seu código e
versionamento (diretório .git). É imprescindível que seu repositório tenha
instruções sobre como o projeto deve ser executado, incluindo versões e
bibliotecas.

Não envie seu projeto via github ou algum outro repositório publico, pois desse
jeito ele poderá ser copiado por outra pessoa.

Você pode usar a linguagem que estiver mais confortável. Na Locaweb
usamos bastante Ruby e um pouco de muitas coisas, como: Go, Python,
Elixir e Java, por exemplo.

### Opcionais (mas dá pontos extras)

+ Vir com um Dockerfile para que sua aplicação possa ser executada com
  apenas um comando
+ Escrever porque você decidiu utilizar tais ferramentas para resolver
  esse problema
+ Escrever o código que resolve o problema utilizando apenas a
  biblioteca padrão da linguagem, sem adicionar libs externas (não tem
  problema usar lib para os testes)
+ Construir uma interface que leia o JSON e mostre uma versão
  apresentável para o usuário final
