# -*- coding: utf-8 -*-                                                     
# CITRA IT - CONSULTORIA EM TI
# SCRIPT PARA DEMONSTRAR COMO WEBSERVERS SÃO CONSTRUÍDOS, UTILIZANDO PYTHON
# Author: luciano@citrait.com.br
# Date: 30/10/2021
# Version: 1.0

import socket


def processa_requisicao(socket_client, addr):

    # Debug
    print("recebido conexão do cliente: " + str(addr))


    # Receber o texto (em bytes) do cliente de socket
    dados_recebidos = socket_client.recv(1024)

    # Transformar os bytes em text ascii
    dados_texto = dados_recebidos.decode('utf-8')
    
    # Organizar os cabeçalhos
    headers = dados_texto.split("\r\n")
    cabecalho_get = headers[0]                    # GET /pagina.html HTTP/1.1
    if cabecalho_get is None:
        print(f"Requisição vazia...")
        socket_client.close()
    else:    
        cabecalho_divido = cabecalho_get.split(" ")   # array 0=> GET, 1=> /pagina.html, 2=> Method (http/1.1)

    # Obtendo a página solicita através do cabeçalho
    try:
        pagina = cabecalho_divido[1]                      # /pagina.html
        pagina = pagina[1:]                               # pagina.html remove a / do início.
    except IndexError:
        print(f"debug: erro ao obter cabecalhos da requisicao")
        return
    

    # Lendo o conteúdo do arquivo solicitado
    try:
        print(f"tentando abrir o arquivo: {pagina}")
        arquivo = open(pagina, "r")
        conteudo_arquivo = arquivo.read()
    except:
        print("arquivo nao encontrado no servidor")
        conteudo_arquivo = "404 CUSTOM MESSAGE PAGE NOT FOUND"


    # Enviar resposta para o cliente
    socket_client.sendall(bytes("HTTP/1.1 200 OK\r\n\r\n" + str(conteudo_arquivo), 'utf-8'))
    socket_client.close()




#---------------------------------------------------------------------------------------
# MAIN ENTRY POINT
#---------------------------------------------------------------------------------------

# Criar o socket
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Perguntar ao sistema opeacional se a porta 8000 está disponível para usá-la
socket_server.bind(("0.0.0.0", 8000))

# Pedir ao S.O tudo que ele receber na porta 8000, ele vai repassar para nossa aplicação
socket_server.listen(10)


# Aguardar infinitamente por conexões na porta 8000.
while True:
    socket_client, addr = socket_server.accept()
    processa_requisicao(socket_client, addr)
    # Encerrar a conexão
    socket_client.close()



sys.exit(0)








