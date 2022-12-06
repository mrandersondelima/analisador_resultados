import os
from time import sleep
from telegram_bot import TelegramBot

NUMERO_JOGOS_AMARELOS = 3
numero_jogos_amarelos_atual = 0
ultimo_jogo = dict()
telegram_bot = TelegramBot()
atingiu_jogos_amarelos = False
primeira_execucao = True

ultima_lista = ''

while True:
    saida = os.popen('../monkeybet/results.sh').read()
    if saida.split('\n')[0] == '' or 'PLAYNOW!' not in saida:
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

                if primeira_execucao:
                    primeira_execucao = False
                    print('primeira execução')
                    for placar in resultados:
                        gols_casa = placar.split('x')[0]
                        gols_fora = placar.split('x')[1]
                        if int(gols_casa) + int(gols_fora) < 3:
                            print('jogo com menos de 2,5')
                            numero_jogos_amarelos_atual += 1
                        else:
                            break
                else:
                    gols_casa = int(resultados[0].split('x')[0])
                    gols_fora = int(resultados[0].split('x')[1])
                    if int(gols_casa) + int(gols_fora) < 3:
                        print('jogo com menos de 2,5')
                        numero_jogos_amarelos_atual += 1
                    else:
                        numero_jogos_amarelos_atual = 0
                        atingiu_jogos_amarelos = False

                print(numero_jogos_amarelos_atual)

                if numero_jogos_amarelos_atual >= NUMERO_JOGOS_AMARELOS and not atingiu_jogos_amarelos:
                    TelegramBot().envia_mensagem('HORA DE APOSTAR!!!')
                    atingiu_jogos_amarelos = True

                if len(ultimo_jogo) == 2:
                    del ultimo_jogo[ultima_lista]
                # adiciona a nova lista no dicionário
                ultimo_jogo[lista_resultados] = True         

                ultima_lista = lista_resultados   

    sleep(15)

