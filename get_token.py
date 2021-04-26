# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:00:05 2021

@author: CRIBE2
"""

import json
import requests

# =============================================================================
# INITIAL VARIABLES
# =============================================================================
USER = 'usuario@gmail.com'
PASSWORD = '00000'

URL_PREFIX = 'https://app.tecnofit.com.br'


# =============================================================================
# Requesting to get a list of box availables and their token
# =============================================================================
EndpointToken = '/ws/app-login'
PostData = {
    "wsEmail": USER,
    "wsSenha": PASSWORD,
    "wsCadastro": "1",
    }
print ("Fazendo Login... \n")
rGetToken = requests.post(URL_PREFIX + EndpointToken, data=PostData)
jToken = json.loads(rGetToken.text)

if (jToken["result"]):
    
    print ("Pegando dados dos box que há cadastro... \n")
    for empresa in jToken["dados_empresas"]:
        print ("Box: "+ empresa["empresa"])
        print ("Token: "+ empresa["token"])
        print ("")
else:
    print ("Login falhou!")