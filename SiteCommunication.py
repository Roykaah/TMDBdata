import requests
from urllib.parse import urlencode
from urllib.parse import quote
import json
import csv

Usuario = [{
    'login':
    "Royka",
    'senha':
    "ProjetoPython555",
    'api_key':
    "9f0b4f14fa986dec0ae942392adc2de4",
    'access_token':
    "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZjBiNGYxNGZhOTg2ZGVjMGFlOTQyMzkyYWRjMmRlNCIsInN1YiI6IjVmYWQyOWU0ZGUxMWU1MDA0MTE2YjA5YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.a9yTBggzSveyZp6hgbV_ZMFcJaEgu39SoOd7femE4yg"
}, {
    'login':
    "Henricao",
    'senha':
    "ProjetoPython555",
    'api_key':
    "755147259a28b56fe733907e9acdc0a2",
    'access_token':
    "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3NTUxNDcyNTlhMjhiNTZmZTczMzkwN2U5YWNkYzBhMiIsInN1YiI6IjVmYjU1ZDczZTk0MmVlMDAzZmNkOTFlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YY1a3U3AsXErTxhjBjtrCisrMnW1wcRQmjCd0iDQYgg"
}]


# Coleta um dado específico do filme pesquisado
def get_Alguma_Coisa_do_TMDB(url_link, headers, append_item):
    resposta = requests.get(url_link, headers=headers)
    resposta_em_dict = resposta.json()
    final_list = resposta_em_dict['results']
    try:
        atributo_desejado = final_list[0][f'{append_item}']
    except Exception:
        return None
    print(atributo_desejado)
    return str(atributo_desejado)


#Gera um request token (necessario para o login)
def generate_Request_Token(str_before_api_key, api_key, headers):
    url_base = "https://api.themoviedb.org/3/authentication/token/new"
    url_link = f"{url_base}{str_before_api_key}{api_key}"
    resposta = requests.get(url_link, headers=headers)
    resposta_em_dict = resposta.json()
    return resposta_em_dict['request_token']


#Faz o login
def validando_com_login(str_before_api_key, Usuario, headers):
    request_token = generate_Request_Token(str_before_api_key,
                                           Usuario['api_key'], headers)
    print(request_token)
    url_base = "https://api.themoviedb.org/3/authentication/token/validate_with_login?"
    url_link = f"{url_base}{str_before_api_key}{Usuario['api_key']}&request_token={request_token}&username={Usuario['login']}&password={Usuario['senha']}"
    #Uso o token para logar.
    requests.post(url_link, headers=headers).json()
    url_link = f"https://api.themoviedb.org/3/authentication/session/new?api_key={Usuario['api_key']}"
    params = {
        "request_token": f"{request_token}",
        "Content-Type": "application/json;charset=utf-8"
    }
    #Uso o token já logado para criar id da sessao
    session_id_json = requests.post(url_link, headers=headers,
                                    params=params).json()
    print(session_id_json)
    return session_id_json["session_id"]


# Com o id do filme e com o login efetuado, dá nota ao filme
def rate_movie(session_id, api_key, headers):
    with open(f"json_ratings{Numero_Usuario}.json", 'r') as jsonFile:
        dicionario_letterbox = json.load(jsonFile)
        lista_nome = []
        for key in dicionario_letterbox:
            lista_nome.append(key)
    lista_com_ratings = []
    for nome_da_key in lista_nome:
        rating_em_float = float(dicionario_letterbox[nome_da_key]['Rating'])
        rating_do_filme = rating_em_float * 2
        lista_com_ratings.append(rating_do_filme)
    with open(f"movie_IDs{Numero_Usuario}.txt", "r") as IDs:
        IDs = IDs.read()
        lista_ids = IDs.split(',')
        print(lista_ids)
        for i in range(0, len(lista_com_ratings)):
            print(lista_ids[i], lista_com_ratings[i], i)
            params = {"value": f"{lista_com_ratings[i]}"}
            url_base = "https://api.themoviedb.org/3/movie/"
            url_link = f"{url_base}{lista_ids[i]}/rating?api_key={api_key}&session_id={session_id}"
            try:
                print(
                    requests.post(url_link, params=params,
                                  headers=headers).json())
            except Exception:
                pass


#Coleta todas as informacoes dos filmes registrados como 'rated' na conta logada na plataforma TMDB
def coletando_dados_dos_rated_movies(api_key, session_id, headers):
    account_id = "account_id"
    url_base = f"https://api.themoviedb.org/3/account/{account_id}/rated/movies?api_key="
    a = 0
    with open(f"MovieDataInTXT{Numero_Usuario}.txt", 'w') as MovieDataInTXT:
        for page in range(1, 40, 1):
            url_link = f"{url_base}{api_key}&session_id={session_id}&sort_by=created_at.asc&page={page}"
            a = 0
            try:
                DadosDaPagina = requests.get(url_link, headers=headers).json()
                for movies in range(0, 20):
                    json.dump(DadosDaPagina['results'][movies], MovieDataInTXT)
                    a = a + 1
                    MovieDataInTXT.write("\n")
            except Exception:
                pass
            print(a)


#  URL
str_before_api_key = "?api_key="
append_item = "id"


#  Pesquisa e coleta o ID de cada filme que foi extraido do csv
def CRIA_IDS_LIST(api_key, headers, append_item, str_before_api_key):
    url_base = "https://api.themoviedb.org/3/search/movie"
    with open(f"json_ratings{Numero_Usuario}.json", 'r') as jsonFile:
        dicionario_letterbox = json.load(jsonFile)
        lista_nome = []
        for key in dicionario_letterbox:
            lista_nome.append(key)
    IDs_coletados = []
    for nome_da_key in lista_nome:
        nome_do_filme_para_URL = quote(
            dicionario_letterbox[nome_da_key]['Name'])
        ano_do_filme_para_URL = (dicionario_letterbox[nome_da_key]['Year'])
        query = f"&query={nome_do_filme_para_URL}&year={ano_do_filme_para_URL}"
        url_link = (f"{url_base}{str_before_api_key}{api_key}{query}")
        print(dicionario_letterbox[nome_da_key]["Name"])
        IDs_coletados.append(
            get_Alguma_Coisa_do_TMDB(url_link, headers, append_item))
    with open(f'movie_IDs{Numero_Usuario}.txt', 'w') as arqTXT:
        for strings in IDs_coletados:
            if strings is not None:
                arqTXT.write(strings)
                arqTXT.write(',')
            else:
                arqTXT.write("-1")
                arqTXT.write(',')


#Extrai as informacoes uteis do arquivo csv
def extract_from_letterbox_csv(Numero_Usuario):
    dict_ratings = {}
    with open(f'ratings{Numero_Usuario}.csv', 'r') as my_ratings:
        my_ratings = csv.DictReader(my_ratings)
        for movie in my_ratings:
            id = movie["Name"]
            dict_ratings[id] = movie

    with open(f'json_ratings{Numero_Usuario}.json', 'w') as jsonFile:
        jsonFile.write(json.dumps(dict_ratings, indent=4))


for Numero_Usuario in range(0, 1):
    headers = {
        "Authorization": f"Bearer {Usuario[Numero_Usuario]['access_token']}",
        "Content-Type": "application/json;charset=utf-8"
    }

    extract_from_letterbox_csv(Numero_Usuario)

    CRIA_IDS_LIST(Usuario[Numero_Usuario]['api_key'], headers, append_item,
                  str_before_api_key)

    session_id = validando_com_login(
        str_before_api_key,
        Usuario[Numero_Usuario],
        headers,
    )

    rate_movie(session_id, Usuario[Numero_Usuario]['api_key'], headers)
    coletando_dados_dos_rated_movies(Usuario[Numero_Usuario]['api_key'],
                                     session_id, headers)
