# -*- coding: utf-8 -*-

import requests
import re

# Obter o ip pela api do dyndns
req = requests.get('http://checkip.dyndns.org')

# extrair somente o ip da resposta http
ip_addr = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', req.text)[0]

html = """<!DOCTYPE html>
<html>
    <head>
    <meta charset="utf-8">
    </head>
    <body>
        <h1>Seu endereço IP é: {{IP}}</h1>
    </body>
</html>
"""
html = html.replace('{{IP}}', ip_addr)
print(html)