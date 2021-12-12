# -*- coding: utf-8 -*-

import sys
import socket
from threading import Thread
import subprocess


SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8000

tipo_arquivo_binario = ['png', 'jpeg', 'bmp']
tipo_arquivo_text = ['html', 'css', 'js']
tipo_arquivo_executable = ['php', 'py', 'pl']



def processa_solicitacao(socket_cliente, cliente_addr):
    # debug 
    print(f'cliente conectado com sucesso. {cliente_addr[0]}:{cliente_addr[1]}')

    # receber dados do cliente
    dado_recebido = socket_cliente.recv(1024)
    dado_recebido = dado_recebido.decode()

    # parsing do cabeçalho
    headers = dado_recebido.split('\r\n')
    header_get = headers[0]

    # obtendo o arquivo solicitado
    arquivo_solicitado = header_get.split(' ')[1][1:]
    print(f'arquivo solicitado: {arquivo_solicitado}')
    
    # obtendo a extensao
    extensao = arquivo_solicitado.split('.')[-1]
    
    arquivo_binario = False
    arquivo_executavel = False
    
    if extensao in ['py']:
        arquivo_executavel = True
    if extensao in tipo_arquivo_binario:
        arquivo_binario = True
    
    
    

    # abrir o arquivo e 
    try:
        if arquivo_executavel:
            processo = subprocess.run(['python', arquivo_solicitado], stdout=subprocess.PIPE, 
                text=True)
            stdout = processo.stdout
            # stdout = stdout
            headers = f'HTTP/1.1 200 OK\r\n\r\n'
            answer = headers + stdout
            socket_cliente.sendall(answer.encode('utf-8'))
            return True
        elif arquivo_binario:
            file = open(arquivo_solicitado, 'rb')
        else:
            file = open(arquivo_solicitado, 'r', encoding='utf-8')
        conteudo_arquivo = file.read()
    except FileNotFoundError:
        print(f'arquivo nao existe {arquivo_solicitado}')
        socket_cliente.sendall(b'HTTP/1.1 404 File not found\r\n\r\nFound file not found')
        socket_cliente.close()
        return False


    # resposta ao browser
    cabecalho_resposta = f'HTTP/1.1 200 OK\r\n\r\n'
    corpo_resposta = conteudo_arquivo

    if arquivo_binario:
        resposta_final = bytes(cabecalho_resposta, 'utf-8') + corpo_resposta
        socket_cliente.sendall(resposta_final)
    else:
        resposta_final = cabecalho_resposta + corpo_resposta
        socket_cliente.sendall(resposta_final.encode('utf-8'))

    # encerrar a conexão
    socket_cliente.close()



# criando o objeto socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# solicitar ao windows para ouvir na porta 8000
socket_servidor.bind((SERVER_ADDRESS, SERVER_PORT))
socket_servidor.listen(10)


while True:
    # aguardo uma conexão cliente
    # debug
    print(f'Servidor ouvindo em {SERVER_ADDRESS}:{SERVER_PORT} pronto para receber conexões...')
    socket_cliente, cliente_addr = socket_servidor.accept()
    
    # despachando a requisicao para a thread processa-la.
    Thread(target=processa_solicitacao, args=(socket_cliente, cliente_addr)).start()
    


socket_servidor.close()

