import scrapping as scr
import os
import sys

if __name__ == "__main__":
    scr.baixa_pagina(sys.argv[1])
    url = scr.recupera_json()
    urls = scr.converte_json_em_dicionario(url)
    nome_pasta = scr.produz_nome_pasta()
    os.mkdir(nome_pasta)
    scr.baixa_musicas(urls, nome_pasta)
    os.remove("temp.txt")
