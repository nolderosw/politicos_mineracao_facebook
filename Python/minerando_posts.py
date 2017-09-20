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
#from translate import translator
import tweepy
import numpy as np

#nltk.download() #baixar e instalar as coisas do ntlk

now = datetime.now() # instanciando datetime para pegar a hora que minerei tal coisa

cliente = MongoClient('localhost', 27017)
banco = cliente.Politicos_Pages
string1 = 'Lula'
string2 ='Marina'+' '+'Silva'

#twitters_BD = banco.Lula
twitters_BD = banco[string1]

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

variavelzona = '' #Variável que irá armazenar os posts
analysis = None
cont_Neutro = 0
cont_Pos = 0
cont_Neg = 0
contador_posts = 0

for i in range(twitters_BD.count()): #FOR UTILIZADO PARA EXTRAIR DO BANCO DE DADOS OS POSTS
#for i in range(1):
    texto = twitters_BD.find()[i]['Mensagem']
    #print("Data:", twitters_BD.find()[i]['Data'])
    print("TWEET ORIGINAL:",texto)
    doc_word = removendo_stopwords(str(texto))
    doc_word = removendo_hashtags(doc_word)
    doc_word = removendo_URLS(doc_word)

    variavelzona += doc_word #VARIÁVEL PARA ARMAZENAR TODOS OS POSTS EM UMA UNICA VARIAVEL
    variavelzona += '$$' #VALOR DE SPLIT
    

print("TAMANHO ANTES DA TRADUÇÃO:",len(variavelzona))
frase = TextBlob(variavelzona) #Tratando para Traduzir
traducao = TextBlob(str(frase.translate(to='en'))) #Traduzindo para inglês.
print("TAMANHO DEPOIS DA TRADUÇÃO:",len(traducao))
traducao = traducao.split('$$')
print("QUANTIDADE DE POSTS:",len(traducao))

for i in range(len(traducao)): #FOR UTILIZADO PARA CLASSIFICAR CADA POST COMO POSITIVO OU NEGATIVO

    
            #print('Tweet: {0} - Sentimento: \n{1}'.format(doc_word, traducao.sentiment))
            analysis = tb(str(traducao[i]))
            valor = analysis.sentiment.polarity
            print("ANALISE AVULSA:",valor)
            print('\n')
            if valor == 0:
                cont_Neutro +=1
            elif valor>0:
                cont_Pos +=1
            else:
                cont_Neg +=1
            contador_posts += 1
            print("CONT POSTS:",contador_posts)
            print("HORA:%i:%i"%(now.hour,now.minute))

    
print("POSITIVOS: %i | NEGATIVOS: %i | NEUTROS: %i "%(cont_Pos,cont_Neg,cont_Neutro))
    
