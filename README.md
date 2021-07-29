# TMDBdata

    Tendo em vista que o meu hobbie mais vigorante do momento é o cinema, resolvi desenvolver um projeto para manipulação de dados
    relacionados aos filmes que já assisti.
    Há muito tempo comecei a registrar todos os filmes que assisto com sua devida nota arbitrária em um aplicativo (letterboxd), o 
    qual permite que extraiamos um arquivo csv com todas os filmes e que o usuário deu nota, disponibilizando seu respectivo nome, 
    ano de lançamento e nota.
    Para obter mais dados sobre os filmes, eu precisei colocá-los em uma outra plataforma de filmes (TMDB), a qual, ao contrário do 
    letterboxd, apresentava uma API. (Todo esse processo foi desenvolvido em SiteCommunication.py)
    Depois de extrair os dados completos dos filmes, manipulei-os para que eu vizualizasse graficamente as relações que estabeleci.
    (Processo feito em MovieDataAnalysis.ipynb)

Rodando o programa:
    1. Rode o arquivo SiteCommunication.py
    2. Espere pouco mais ou menos 5 minutos
    3. Quando o processo finalizar, execute MovieDataAnalysis
    Para a primeira parte, estarei disponibilizando apenas o ratings0 e ratings1 (csv do letterboxd) na pasta geral para que tente 
    ser realizado o processo inteiro. Caso aconteça algum tipo de erro ou problema com alguns módulos não instalados, um rapido pip 
    install deve resolver.
    Se ainda não for o suficiente para funcionar, estarei disponibilizando os arquivos que eram para ter sido gerados na pasta 
    "ArqQueEramParaTeremSidoGerados". Apenas coloque eles no diretorio geral e siga para a parte 3.

Como Funciona?
    1. Extrai dados do csv
    2. Pesquisa utilizando os nomes na plataforma TMDB para coleta de IDs dos filmes
    3. Cria uma sessão de usuário
    4. Dá nota ao filme no TMDB
    5. Coleta os dados dos filmes os quais foram dadas as notas
    6. Analisa graficamente os dados coletados

OBS: 
    1. Eu sou o Royka (ratings0) mencionado nos programas, Henrique (ratings1) é um amigo que compartilha do mesmo hobbie.
    2. Eu comecei o programa logo após a aula 9 e assisti a aula 10 apenas depois de encerrá-lo, ou seja, não tinha o conhecimento
    de dataframe (que teria me poupado muito tempo).
    3. Para uso próprio (duvido que alguém um dia faça isso), extraia os dados de seu letterboxd, copie o csv "ratings", renomeie para "ratings0" e siga o passo a passo.
