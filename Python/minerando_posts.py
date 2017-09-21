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

#nltk.download() //baixar e instalar as coisas do ntlk

now = datetime.now() # instanciando datetime para pegar a hora que minerei tal coisa
'''INICIANDO CONEXÃO COM O BANCO DE DADOS MONGO DB'''
cliente = MongoClient('localhost', 27017)
banco = cliente.Politicos_Pages
politico = ''
twitters_BD = ''

variavelzona = '' #Variável que auxiliará a tradução
qtd = 10 #Quantidade de posts a serem minerados.

'''Determina qual banco de dados vai percorrer no momento'''
def Seleciona_Banco(a):
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

    #a = int(input("Selecione um político de 1-9: "))
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

'''Trata o comentário tirando as hashtags'''
def removendo_hashtags(texto):
    words = texto.split()

    for i in words:
        if i.startswith('#'):
            words.remove(i)

    texto = ' '.join(words)

    return texto

'''Trata o comentário tirando as URLS'''
def removendo_URLS(texto):
    clean_text = re.match('(.*?)http.*?\s?(.*?)', texto)
    if clean_text:
        return clean_text.group(1)
    else:
        return texto

'''Trata o comentário tirando as Stopwords (Palavras Desnecessárias)'''
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

'''Recebe os comentários do banco de dados MONGODB'''
def minerando_banco():

    global qtd,politico
    contador_posts = 0
    global variavelzona  #Variável que irá armazenar os posts
    #for i in range(twitters_BD.count()): #FOR UTILIZADO PARA EXTRAIR DO BANCO DE DADOS OS POSTS
    for i in range(qtd):
        for j in range(len(twitters_BD.find()[i]['Comentarios'])):
            comentario = twitters_BD.find()[i]['Comentarios'][j]['Mensagem']
            contador_posts += 1
            print("POLÍTICO: %s | POST: %i | COMENTÁRIO: %i | TAMANHO: %i"%(politico,i,contador_posts,len(variavelzona)))


            #print("Data:", twitters_BD.find()[i]['Data'])
            print("TWEET ORIGINAL:",comentario)
            doc_word = removendo_stopwords(str(comentario))
            doc_word = removendo_hashtags(doc_word)
            doc_word = removendo_URLS(doc_word)

            variavelzona += doc_word #VARIÁVEL PARA ARMAZENAR TODOS OS POSTS EM UMA UNICA VARIAVEL
            variavelzona += '$$' #VALOR DE SPLIT
            if len(variavelzona)>500000:
                break
        if len(variavelzona)>500000:
            continue

    return variavelzona

'''Traduz o comentário para Inglês para ser tratado sentimentalmente'''
def Traduzindo_Termos(string):
    print("SIZE BEFORE TRANSLATE:", len(string))
    frase = TextBlob(string)  # Tratando para Traduzir
    traducao = TextBlob(str(frase.translate(to='en')))  # Traduzindo para inglês.
    print("SIZE AFTER TRANSLATE:",len(traducao))

    return traducao

'''Analisa os sentimentos do texto, de acordo com o conteúdo'''
def Analisando_Sentimentos(string_original, string_traduzida):
    arq = open("base_dados.txt", "w")

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
        Escrevendo_BaseDados(arq, a, variavel_atribuicao)
    Salvando_BaseDados(arq)
    return print("POSITIVOS: %i | NEGATIVOS: %i | NEUTROS: %i "%(cont_Pos,cont_Neg,cont_Neutro))

'''Salva um arquivo de base de dados'''
def Salvando_BaseDados(arq):
    arq.close()
    return print('Arquivo Salvo com Sucesso!')

'''Escreve na base de dados'''
def Escrevendo_BaseDados(arquivo,texto,status):
    arquivo.write('\"%s\", %s\n' % (texto, status))
    return print('Salvo!')

'''Determina se um usuário comentou mais de n vezes na página do candidato e o armazena em um arquivo.'''
def Frequencia_Comentarios():
    global qtd
    lista_autores = []
    arq2 = open("usuarios_comentados.txt", "w")

    conta_total=0
    #for i in range(twitters_BD.count()): #FOR UTILIZADO PARA EXTRAIR DO BANCO DE DADOS OS POSTS
    for i in range(qtd):
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

'''Separa a incidência de comentários de acordo com o político'''
def Lendo_Arquivo_Usuarios():
    arquivo = open("usuarios_comentados.txt", "r")
    global politico
    nome_arquivo = str(politico)+str('.txt')
    arquivo2 = open(nome_arquivo, "w")
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

'''Plota Grafos'''
def Plotando_Grafos():
    arquivo_x = open("suspeitos.txt", "r")
    linhas = arquivo_x.readlines()
    G = nx.Graph()
    suspeitos = []
    for linha in linhas:
        a = linha.strip().split('$')
        b = a[1].split('\'')
        # print(b)
        print(a[0])
        print(b[0])
        G.add_edge(a[0], b[0])

    d = nx.degree(G)

    pos = nx.spring_layout(G)

    nx.draw_networkx_labels(G, pos)
    nx.draw(G, pos, nodelist=d.keys(), node_size=[v * 500 for v in d.values()])

    plt.show()

'''Verifica se o usuário armazenado (por comentar muito na pagina do politico) comentou muitas vezes
    na página de outro político também'''
def Verifica_Suspeitos():
    suspeitos = open('suspeitos.txt', "w")
    politico1 = 'Aecio' + ' ' + 'Neves'
    politico2 = 'Alvaro' + ' ' + 'Dias'
    politico3 = 'Ciro' + ' ' + 'Gomes'
    politico4 = 'Geraldo' + ' ' + 'Alkmin'
    politico5 = 'Jair' + ' ' + 'Bolsonaro'
    politico6 = 'Joao' + ' ' + 'Doria'
    politico7 = 'Lula'
    politico8 = 'Marina' + ' ' + 'Silva'
    politico9 = 'Michel' + ' ' + 'Temer'
    lista = [politico1,politico2,politico3,
             politico4,politico5,politico6,
             politico7,politico8,politico9]
    for i in range(9):
        print('Comparando Arquivo do Político: %s'%(lista[i]))
        nome_arquivo = str(lista[i])+str('.txt')
        abre_arquivo = open(nome_arquivo, "r")
        y = abre_arquivo.readlines()
        for j in range(i+1,9):
            print('Comparando Arquivo do Político: %s com o do Político: %s'%(lista[i],lista[j]))
            nome_arquivo2 = str(lista[j]) + str('.txt')
            abre_arquivo2 = open(nome_arquivo2, "r")
            x = abre_arquivo2.readlines()
            for k in x:
                nome_atual = k
                #print("NOME 1:",nome_atual)

                for l in y:
                    nome_atual2 = l
                    #print("NOME 2:",nome_atual2)
                    if nome_atual.strip() == nome_atual2.strip():
                        suspeitos.write(str(nome_atual.strip())+str('$%s\n'%(lista[i])))
                        print('Possível Suspeito:%s'%(str(nome_atual.strip())))


            abre_arquivo2.close()
        abre_arquivo.close()
    suspeitos.close()

    print("TODOS OS SUSPEITOS FORAM ANALISADOS COM SUCESSO!")

'''Determina o looping de mineração por político'''
def Ciclo(politic):
    global twitters_BD
    Seleciona_Banco(politic)
    twitters_BD = banco[politico]
    print("Número de Posts:", twitters_BD.count())
    Analisando_Sentimentos(minerando_banco(), Traduzindo_Termos(variavelzona))
    Frequencia_Comentarios()
    Lendo_Arquivo_Usuarios()

'''Main :)'''
def main():
    hora_inicio = now.hour
    minuto_inicio = now.minute
    segundo_inicio = now.second
    Ciclo(1) #AecioNeves
    Ciclo(2) #AlvaroDias
    Ciclo(3) #CiroGomes
    Ciclo(4) #GeraldoAlkmin
    Ciclo(5) #JairBolsonaro
    Ciclo(6) #JoaoDoria
    Ciclo(7) #Lula
    Ciclo(8) #MarinaSilva
    Ciclo(9) #MichelTemer
    Verifica_Suspeitos()
    hora_fim = now.hour
    minuto_fim = now.minute
    segundo_fim = now.second
    print("HORA DE INÍCIO DA MINERAÇÃO: %i:%i:%i"%(hora_inicio,minuto_inicio,segundo_inicio))
    print("HORA DE TÉRMINO DA MINERAÇÂO: %i:%i:%i"%(hora_fim,minuto_fim,segundo_fim))

    if int(input("Deseja Plotar Grafo? (1) Para Sim: ")) == 1:
        Plotando_Grafos()

main()
