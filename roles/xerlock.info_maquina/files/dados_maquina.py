#!/usr/bin/env python3

import sys
import platform
import shutil
import os
import json
import socket
import datetime
from pymongo import MongoClient
from ast import literal_eval
import os 
from dotenv import load_dotenv


def converte_input(input):
    try:
        return literal_eval(input)
    except:
        return input
    
load_dotenv()
cliente = MongoClient(
    f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}@{os.environ['MONGO_HOST_PORT']}/"
)
banco = cliente.portalseguranca
collec = banco.maquina_dados

os.system("df -x tmpfs -x devtmpfs -HP --total -T | tail -1 | awk '{print $3,$4,$5}' > /tmp/sys_info.txt")
arquivo = open('/tmp/sys_info.txt', 'r')
arquivo = arquivo.readlines()[0].rstrip("\n").split(" ")

# Remove ultimo caractere
tamanho_disco = [converte_input(tamanho[:-1]) for tamanho in arquivo]

size = tamanho_disco[0] * 1024
used = tamanho_disco[1] * 1024
free = tamanho_disco[2] * 1024


collec.find_one_and_update(
        {
                "nome_maquina": socket.getfqdn() },
        {
                "$set": {
                        'hora_insert': str(datetime.datetime.now()),
                        'info_extras': platform.platform(),
                        'sistema_operacional': platform.system(),
                        'nome_maquina': socket.getfqdn(),
                        'espaco_disco_total': size,
                        'espaco_disco_usado': used,
                        'espaco_disco_disponivel': free
                }
        },
        upsert=True
)
     
