from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import json
import os

def baixa_pagina(url):
    html = urlopen(url)
    res = BeautifulSoup(html.read(), "html.parser")
    arquivo = "".join([p.text for p in res.findAll("script")])
    arquivo = arquivo.splitlines(True)
    with open("temp.txt", "w", encoding="utf-8") as temp:
        for linha in arquivo:
            temp.write(linha)


def recupera_json():
    with open("temp.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if "trackinfo:" in linha:
                return linha.replace('trackinfo:', "").replace(" ", "")[:-2]


def converte_json_em_dicionario(url):
    arquivo = json.loads(url)
    urls = {}

    for dicionario in arquivo:
        if dicionario['file'] is None:
            continue

        titulo = dicionario['title'].replace("/", "")
        id = str(dicionario['id']) + '.mp3'
        path = dicionario['file']['mp3-128']

        urls[id] = [path, titulo]

    return urls

def baixa_musicas(urls, nome_pasta):
    opener = urllib.request.build_opener()
    firefox = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
    apple = 'AppleWebKit/537.36 (KHTML, like Gecko)'
    chrome = 'Chrome/36.0.1941.0 Safari/537.36'
    browsers = " ".join([firefox, apple, chrome])
    opener.addheaders = [('User-Agent', browsers)]
    urllib.request.install_opener(opener)
    for nome, url in urls.items():
        print("baixando faixa", url[1] + "...")
        urllib.request.urlretrieve(url[0], nome)
        os.rename(nome, nome_pasta + "/" + url[1] + ".mp3")

    print("Fim :)")


def produz_nome_pasta():
    with open("temp.txt", "r", encoding="utf-8") as temp:
        for linha in temp:
            if "album_title:" in linha:
                album = linha.split('"')[1]
            elif "artist:" in linha:
                banda = linha.split('"')[1]
                nome_pasta = banda + " - " + album
                return nome_pasta.replace("/", "")