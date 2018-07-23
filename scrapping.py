from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import os
import json
import sys


def baixa_pagina(url):
    html = urlopen(url)
    res = BeautifulSoup(html.read(), "html.parser")
    arquivo = "".join([p.text for p in res.findAll("script")])
    arquivo = arquivo.splitlines(True)
    with open("temp.txt", "w", encoding='utf-8') as temp:
        for linha in arquivo:
            temp.write(linha)


def recupera_json():
    with open("temp.txt", "r") as arquivo:
        for linha in arquivo:
            if "trackinfo:" in linha:
                return linha.replace('trackinfo:', "").replace(" ", "")[:-2]


def converte_json_em_dicionario(url):
    titulo = ""
    id = ""
    urls = {}

    arquivo = json.loads(url)
    for linha in arquivo:
        for chave, valor in linha.items():
            if chave == "title":
                titulo = valor.replace("/", "")
            elif chave == "id":
                id = str(valor) + ".mp3"
            elif chave == "file":
                if valor is None:
                    continue
                urls[id] = [valor["mp3-128"], titulo]
    return urls


def baixa_musicas(urls, nome_pasta):
    opener = urllib.request.build_opener()
    browsers = 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
    browsers.join('AppleWebKit/537.36 (KHTML, like Gecko)')
    browsers.join(' Chrome/36.0.1941.0 Safari/537.36')

    opener.addheaders = [('User-Agent', browsers)]
    urllib.request.install_opener(opener)
    for nome, url in urls.items():
        urllib.request.urlretrieve(url[0], nome)
        os.rename(nome, nome_pasta + "/" + url[1] + ".mp3")


def produz_nome_pasta():
    validador_linha = False
    album = ""
    banda = ""
    nome_pasta = ""

    with open("temp.txt", "r") as temp:
        for linha in temp:
            if "EmbedData" in linha:
                validador_linha = True
            elif "album_title:" in linha and validador_linha:
                album = linha.replace("album_title: ", "").replace(",", "")
                album = album.replace('"', '').strip()
            elif "artist:" in linha and validador_linha:
                banda = linha.replace("artist: ", "").replace(",", "")
                banda.replace('"', '').strip()
                nome_pasta = banda + " - " + album
                return nome_pasta.replace("/", "")


if ("bandcamp" in sys.argv[1]):
    baixa_pagina(sys.argv[1])
    url = recupera_json()
    urls = converte_json_em_dicionario(url)
    nome_pasta = produz_nome_pasta()
    os.mkdir(nome_pasta)
    baixa_musicas(urls, nome_pasta)
    os.remove("temp.txt")
else:
    print("Digite um arquivo")
