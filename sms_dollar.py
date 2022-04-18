##########################################
# IMPORTAÇÃO DAS BIBLIIOTECAS UTILIZADAS #
##########################################

import time
import requests as rq
import json
from twilio.rest import Client

####################
# INICIANDO O LOOP #
####################

while True:

    ############################################
    # DEFINIÇÃO DAS VARIÁVEIS DE TEMPO VALORES #
    ############################################

    hora = int(time.strftime('%H', time.localtime()))
    hora -= 3
    min = int(time.strftime('%M', time.localtime()))
    seg = int(time.strftime('%S', time.localtime()))
    ctime = time.ctime()
    semana = ctime.split()[0]
    fds = ['Sun', 'Sat']
    cotacoes = rq.get("https://economia.awesomeapi.com.br/json/last/USD-BRL") #API DA COTACAO DO DOLAR
    cotacoes = cotacoes.json()
    dolar = float(cotacoes['USDBRL']['bid'])

    ###################################################################
    # PARÂMETRO PARA O LOOP WHILE (DE SEGUNDA A SEXTA E DE 8H ÀS 18H) #
    ###################################################################
 
    while semana not in fds and hora >= 8 and hora < 18:

        hora = int(time.strftime('%H', time.localtime()))
        hora -= 3 #GMT BRASIL
        min = int(time.strftime('%M', time.localtime()))
        seg = int(time.strftime('%S', time.localtime()))
        ctime = time.ctime()
        semana = ctime.split()[0]
        fds = ['Sun', 'Sat']
        cotacoes = rq.get("https://economia.awesomeapi.com.br/json/last/USD-BRL") #API DA COTACAO DO DOLAR
        cotacoes = cotacoes.json()
        dolar = float(cotacoes['USDBRL']['bid'])

        ###############################################################
        # ACIONANDO A API DO TWILIO SE O DOLAR ESTIVER MENOS DE R$4.5 #
        ###############################################################

        texto = f'O dolar está custando R${dolar} às {hora}:{min}:{seg}'    #MENSAGEM

        if dolar <= 4.500:
            account_sid = "TWILIO_ACCOUNT_SID"   #SEU ACCOUNT_SID
            auth_token = "TWILIO_AUTH_TOKEN"     #SEU AUTH_TOKEN

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                to="+15558675310",      #TELEFONE QUE VAI RECEBER A MENSAGEM
                from_="+15017122661",   #TELEFONE DA TWILIO QUE VAI ENVIAR A MENSAGEM
                body=texto)

            print(message.sid)
            print(texto)
            time.sleep(15)
            break

        #######################################
        # DOLAR MAIOR QUE R$4.5 NÃO MANDA SMS #
        #######################################

        else:
            print(f'Ainda ta caro! {texto}')
            time.sleep(15)

    ########################################################
    # LOOP SÓ RODA DURANTE A SEMANA E EM HORÁRIO COMERCIAL #
    ########################################################
    if dolar <= 4.500:
        break

    if semana in fds:
        if semana == 'Sat':
            print(f'Hoje é sábado. A última cotação do dolar foi R${dolar}')
            time.sleep(3600)
        if semana == 'Sun':
            print(f'Hoje é domingo. A última cotação do dolar foi R${dolar}')
            time.sleep(3600)
    elif hora < 11:
        print(f'Ainda não abriu o pregão, são {hora}:{min}:{seg}. A última cotação do dolar foi R${dolar}')
        time.sleep(3600)
    elif hora >= 21:
        print(f'Já passou da hora do pregão, são {hora}:{min}:{seg}. A última cotação do dolar foi R${dolar}')
        time.sleep(3600)
