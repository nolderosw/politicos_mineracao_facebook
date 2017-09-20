#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import re
import nltk
import string
import sys
import datetime
import pprint
import unicodedata
from textblob import TextBlob
from textblob import TextBlob as tb
from datetime import datetime
from translate import translator
import tweepy
import numpy as np
from tqdm import tqdm
from time import sleep
import matplotlib.pyplot as plt
import networkx as nx

arq = open("base_dados.txt", "w")

#nltk.download() //baixar e instalar as coisas do ntlk

now = datetime.now() # instanciando datetime para pegar a hora que minerei tal coisa

cliente = MongoClient('localhost', 27017)
banco = cliente.Politicos_Pages
politico = ''
def Seleciona_Banco():
    global politico
    politico1 = 'Aecio'+' '+'Neves'
    politico2 = 'Alvaro'+' '+'Dias'
    politico3 = 'Ciro'+' '+'Gomes'
    politico4 = 'Geraldo'+' '+'Alkmin'
    politico5 = 'Jair'+' '+'Bolsonaro'
    politico6 = 'Joao'+' '+'Doria'
    politico7 = 'Lula'
    politico8 = 'Marina'+' '+'Silva'
    politico9 = 'Michel'+' '+'Temer'

    a = int(input("Selecione um político de 1-9: "))
    if a == 1:
        print('Politico Selecionado: Aécio Neves!')
        politico = politico1
    elif a == 2:
        print("Político Selecionado: Álvaro Dias!")
        politico = politico2
    elif a == 3:
        print("Político Selecionado: Ciro Gomes!")
        politico = politico3
    elif a == 4:
        print("Político Selecionado: Geraldo Alkmin!")
        politico = politico4
    elif a == 5:
        print("Político Selecionado: Jair Bolsonaro!")
        politico = politico5
    elif a == 6:
        print("Político Selecionado: João Doria!")
        politico = politico6
    elif a == 7:
        print("Político Selecionado: Lula!")
        politico = politico7
    elif a == 8:
        print("Político Selecionado: Marina Silva!")
        politico = politico8
    elif a == 9:
        print("Político Selecionado: Michel Temer!")
        politico = politico9

Seleciona_Banco()
twitters_BD = banco[politico]
print("Número de Posts:", twitters_BD.count())

variavelzona = ''

def removendo_hashtags(texto):
    words = texto.split()

    for i in words:
        if i.startswith('#'):
            words.remove(i)

    texto = ' '.join(words)

    return texto

def removendo_URLS(texto):
    clean_text = re.match('(.*?)http.*?\s?(.*?)', texto)
    if clean_text:
        return clean_text.group(1)
    else:
        return texto

def removendo_stopwords(texto):
    regex = re.compile('[%s]' %re.escape(string.punctuation))
    vetor =[]
    palavras = texto.split()
    for i in palavras:
        new_token = regex.sub(u'',i)
        if not new_token == u'':
            vetor.append(new_token)


    stopwords = nltk.corpus.stopwords.words('portuguese')
    content = [w for w in vetor if w.lower().strip() not in stopwords]

    clean_text = []
    for word in content:
        nfkd = unicodedata.normalize('NFKD',word)
        Palavras_SemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

        q = re.sub('[^a-zA-Z0-9 \\\]', ' ', Palavras_SemAcento)
        clean_text.append(q.lower().strip())

    tokens = [t for t in clean_text if len(t)>2 and not t.isdigit()]
    ct = ' '.join(tokens)

    return ct

def minerando_banco():
    contador_posts = 0
    global variavelzona  #Variável que irá armazenar os posts
    for i in range(twitters_BD.count()): #FOR UTILIZADO PARA EXTRAIR DO BANCO DE DADOS OS POSTS
    #for i in range(15):
        for j in range(len(twitters_BD.find()[i]['Comentarios'])):
            comentario = twitters_BD.find()[i]['Comentarios'][j]['Mensagem']
            contador_posts += 1
            print("POST: %i | COMENTÁRIO: %i"%(i,contador_posts))


            #print("Data:", twitters_BD.find()[i]['Data'])
            print("TWEET ORIGINAL:",comentario)
            doc_word = removendo_stopwords(str(comentario))
            doc_word = removendo_hashtags(doc_word)
            doc_word = removendo_URLS(doc_word)

            variavelzona += doc_word #VARIÁVEL PARA ARMAZENAR TODOS OS POSTS EM UMA UNICA VARIAVEL
            variavelzona += '$$' #VALOR DE SPLIT

    return variavelzona

def Traduzindo_Termos(string):
    print("SIZE BEFORE TRANSLATE:", len(string))
    frase = TextBlob(string)  # Tratando para Traduzir
    traducao = TextBlob(str(frase.translate(to='en')))  # Traduzindo para inglês.
    print("SIZE AFTER TRANSLATE:",len(traducao))

    return traducao

def Analisando_Sentimentos(string_original, string_traduzida):
    contador_posts = 0
    analysis = None
    cont_Neutro = 0
    cont_Pos = 0
    cont_Neg = 0
    string_original = string_original.split('$$')
    string_traduzida = string_traduzida.split('$$')
    print("QTD DE POSTS TRADUZIDOS:", len(string_traduzida))
    for i in range(len(string_traduzida)):  # FOR UTILIZADO PARA CLASSIFICAR CADA POST COMO POSITIVO OU NEGATIVO

        variavel_atribuicao = ''
        analysis = tb(str(string_traduzida[i]))
        print('\n')
        contador_posts += 1
        print('Tweet: {0} - Sentimento: \n{1}'.format(string_traduzida[i], analysis.sentiment))
        parada = analysis.sentiment.polarity
        if parada == 0:
            cont_Neutro += 1
            variavel_atribuicao = 'neutro'
        elif parada > 0:
            cont_Pos += 1
            variavel_atribuicao = 'positivo'
        else:
            cont_Neg += 1
            variavel_atribuicao = 'negativo'

        a = string_original[i].replace('\n', ' ')
        print("POLARITY:", parada)
        print("CONT POSTS:", contador_posts)
        print("HORA:%i:%i" % (now.hour, now.minute))
        Escrevendo_BaseDados(a,variavel_atribuicao)
    Salvando_BaseDados()
    return print("POSITIVOS: %i | NEGATIVOS: %i | NEUTROS: %i "%(cont_Pos,cont_Neg,cont_Neutro))

def Salvando_BaseDados():
    arq.close()
    return print('Arquivo Salvo com Sucesso!')

def Escrevendo_BaseDados(texto,status):
    global arq
    arq.write('\"%s\", %s\n' % (texto, status))
    return print('Salvo!')

def Frequencia_Comentarios():
    lista_autores = []
    arq2 = open("usuarios_comentados.txt", "w")

    conta_total=0
    for i in range(twitters_BD.count()): #FOR UTILIZADO PARA EXTRAIR DO BANCO DE DADOS OS POSTS
    #for i in range(30):
        for j in range(len(twitters_BD.find()[i]['Comentarios'])):
            usuario = twitters_BD.find()[i]['Comentarios'][j]['Usuario']
            if len(lista_autores) != 0:
                for k in range(len(lista_autores)):
                    if usuario not in lista_autores[k]:
                        estrutura = [str(usuario),1]
                        arq2.write(str(estrutura)+str('\n'))
                        conta_total += 1

                    else:
                        arq2.write(str(estrutura)+str('\n'))
                        conta_total += 1

            else:
                estrutura = [str(usuario),1]
                arq2.write(str(estrutura) + str('\n'))
                conta_total += 1
        print(conta_total)
    arq2.close()

def Lendo_Arquivo_Usuarios():
    arquivo = open("usuarios_comentados.txt", "r")
    arquivo2 = open("objetos_estudo.txt", "w")
    # linhas2 = arquivo2.readlines()
    linhas = arquivo.readlines()

    usuarios = []
    adds = []
    for linha in linhas:
        a = linha
        a = a.split('\'')
        b = a[1]
        usuarios.append(b)

    for linha in linhas:
        d = linha
        d = d.split('\'')
        e = d[1]

        if usuarios.count(str(e)) > 10 and str(e) not in adds:
            arquivo2.write(str(e) + str('\n'))
            adds.append(str(e))
        print(len(adds))
    arquivo.close()
    arquivo2.close()

def Plotando_Grafos():
    arquivo_x = open("objetos_estudo.txt", "r")
    linhas = arquivo_x.readlines()
    G = nx.Graph()
    for linha in linhas:
        G.add_node(linha)

        G.add_edge('Lula',linha)

    nx.draw(G, with_labels=True)
    plt.draw()
    plt.show()

def main():
    Analisando_Sentimentos(minerando_banco(), Traduzindo_Termos(variavelzona))
    Frequencia_Comentarios()
    Lendo_Arquivo_Usuarios()
    Plotando_Grafos()
main()