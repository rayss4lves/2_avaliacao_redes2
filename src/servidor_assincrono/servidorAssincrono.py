import hashlib
import socket

PORT = 80
HOST = '0.0.0.0'

class servidor_assincrono():

    def gerar_hash():
        chave = '20239019558 Rayssa Alves'
        sha1_hash = hashlib.sha1(chave.encode()).hexdigest()
        print(sha1_hash)
        return sha1_hash
    
    def iniciar_servidor():
        pass


