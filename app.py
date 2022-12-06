import os
from time import sleep
from telegram_bot import TelegramBot

NUMERO_JOGOS_AMARELOS = 3
numero_jogos_amarelos_atual = 0
ultimo_jogo = dict()
telegram_bot = TelegramBot()

ultima_lista = ''

while True:
    saida = os.popen('../monkeybet/results.sh').read()
    if saida.split('\n')[0] == '':
        print('JOGO EM ANDAMENTO...')
    else:
        lista_resultados = saida.split('\n')[2]

        if '_' not in lista_resultados:
            # essa lista já foi capturado
            if ultimo_jogo.get(lista_resultados) == True:
                print('Lista já capturada...')
                pass
            else:
                print('Nova lista: ', lista_resultados)

                resultados = lista_resultados.split(' ')

                numero_jogos_amarelos_atual = 0

                for placar in resultados:
                    gols_casa = placar.split('x')[0]
                    gols_fora = placar.split('x')[1]
                    if int(gols_casa) + int(gols_fora) < 3:
                        numero_jogos_amarelos_atual += 1
                    else:
                        numero_jogos_amarelos_atual = -10
                    if numero_jogos_amarelos_atual >= NUMERO_JOGOS_AMARELOS:
                        TelegramBot().envia_mensagem('HORA DE APOSTAR!!!')
                        break

                if len(ultimo_jogo) == 2:
                    del ultimo_jogo[ultima_lista]
                # adiciona a nova lista no dicionário
                ultimo_jogo[lista_resultados] = True         

                ultima_lista = lista_resultados   

    sleep(15)

