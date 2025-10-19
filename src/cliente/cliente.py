import socket
import hashlib
import time
import threading
from testes import teste_sequencial, teste_concorrente


def gerar_hash():
        chave = '20239019558 Rayssa Alves'
        sha1_hash = hashlib.sha1(chave.encode()).hexdigest()
        print(sha1_hash)
        return sha1_hash

ID_CLIENTE = gerar_hash()
MAX_THREADS = 5
NUM_REQUISICOES_SEQ = 5
NUM_REQ_CONCORRENTE = 2
 
class Cliente():
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
    
    def enviar_requisicao(self, metodo='GET', caminho = '/', corpo=None):
        
        try:
            tempo_inicial = time.time()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect((self.host, self.porta))
            
            cabecalhos = [f"Host: {self.host}", f"X-Custom-ID: {ID_CLIENTE}", "Connection: close"]
            corpo_texto = ""
            if corpo:
                corpo_texto = str(corpo)
                cabecalhos.append(f"Content-Length: {len(corpo_texto.encode('utf-8'))}")
            
            cabecalhos_str = "\r\n".join(cabecalhos)
            request = f"{metodo} {caminho} HTTP/1.1\r\n{cabecalhos_str}\r\n\r\n"
            
            if corpo_texto:
                request += corpo_texto
            
            client_socket.sendall(request.encode())
            
            resposta = client_socket.recv(4096)
            tempo_final = time.time()
            
            client_socket.close()
            
            response_time = tempo_final - tempo_inicial
            success = b"200 OK" in resposta
            
            return success, response_time, resposta.decode()
        except Exception as e:
            print(f"Error: {e}")
            return False, 0, str(e)
        
# def aguardar_servidor(host, porta, max_tentativas=30, intervalo=1):
#     """Aguarda o servidor estar disponivel antes de prosseguir"""
#     print(f"Aguardando servidor {host}:{porta} ficar disponivel...")
    
#     for tentativa in range(1, max_tentativas + 1):
#         try:
#             test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             test_socket.settimeout(2)
#             test_socket.connect((host, porta))
#             test_socket.close()
#             print(f"Servidor {host}:{porta} esta disponivel!")
#             return True
#         except (socket.error, socket.timeout):
#             print(f"  Tentativa {tentativa}/{max_tentativas} - Aguardando...")
#             time.sleep(intervalo)
    
#     print(f"Nao foi possivel conectar ao servidor {host}:{porta}")
#     return False
   

if __name__ == "__main__":
    # Aguarda os servidores ficarem disponiveis
    servidor_host_sincrono = 'servidor-sincrono'
    servidor_porta_sincrono = 8080
    
    servidor_host_assincrono = 'servidor-assincrono' 
    servidor_porta_assincrono = 8080
    
    cenarios_teste = [
        {'metodo':'GET', 'caminho':'/'},
        {'metodo':'POST', 'caminho':'/dados'},
    ]
    
    resultados_sincrono = []
    resultados_assincrono = []
    
    
    print('=======================TESTE DO SERVIDOR SINCRONO=======================')
    # if aguardar_servidor(servidor_host_sincrono, servidor_porta_sincrono):
    print('-----------Teste inicial-----------')
    cliente = Cliente(servidor_host_sincrono, servidor_porta_sincrono)
    success, response_time, resposta = cliente.enviar_requisicao(metodo='GET', caminho='/')
    print(f"\nSuccess: {success}, Response Time: {response_time}")
    print(resposta)
    for cenario in cenarios_teste:
        print(f'------------------------------ Cenario {cenario["metodo"]} ------------------------------')
        resultado_sincrono = teste_sequencial(metodo=cenario['metodo'], caminho=cenario['caminho'], cliente=cliente)
        resultados_sincrono.append(resultado_sincrono)
    # else:
    #     print("Falha ao conectar ao servidor")
    
    print(resultados_sincrono[0])   
        
    print('======================TESTE DO SERVIDOR ASSINCRONO======================')
    #if aguardar_servidor(servidor_host_assincrono, servidor_porta_assincrono):
    print('-----------Teste inicial-----------')
    cliente = Cliente(servidor_host_assincrono, servidor_porta_assincrono)
    success, response_time, resposta = cliente.enviar_requisicao(metodo='GET', caminho='/')
    print(f"\nSuccess: {success}, Response Time: {response_time}")
    print(resposta)
    for cenario in cenarios_teste:
        print(f'------------------------------ Cenario {cenario["metodo"]} ------------------------------')
        resultado_assincrono = teste_concorrente(metodo=cenario['metodo'], caminho=cenario['caminho'], cliente=cliente)
        resultados_assincrono.append(resultado_assincrono)
    # else:
    #     print("Falha ao conectar ao servidor")
        
    print(resultados_assincrono[0]) 