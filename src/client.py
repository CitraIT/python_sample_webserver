# -*- coding: utf-8 -*-

from threading import Thread
import requests
import time


def request_page(req):
    print(f'requesting page {req}')
    req = requests.get('http://localhost:8000/index.html')
    print(f'requisicao {req} finalizada')
    



if __name__ == '__main__':
    threads = []
    for i in range(5):
        print(f'criando thread n {i}')
        threads.append(Thread(target=request_page, args=(i,)))
        threads[i].start()
    time.sleep(1)
    
    for i in range(5, 10, 1):
        print(f'criando thread n {i}')
        threads.append(Thread(target=request_page, args=(i,)))
        threads[i].start()
    
    