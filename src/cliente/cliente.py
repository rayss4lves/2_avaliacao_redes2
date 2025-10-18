import socket
import hashlib
import time


def gerar_hash():
        chave = '20239019558 Rayssa Alves'
        sha1_hash = hashlib.sha1(chave.encode()).hexdigest()
        print(sha1_hash)
        return sha1_hash

ID_CLIENTE = gerar_hash()
MAX_THREADS = 10
NUM_REQUISICOES = 5
 
class Cliente():
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
    
    def send_http_request(self, metodo='GET', caminho = '/', corpo=None):
        
        try:
            tempo_inicial = time.time()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect((self.host, self.porta))
            
            cabecalhos = [f"Host: {self.host}", f"id_cliente: {ID_CLIENTE}", "Connection: close"]
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
        
def aguardar_servidor(host, porta, max_tentativas=30, intervalo=1):
    """Aguarda o servidor estar disponível antes de prosseguir"""
    print(f"Aguardando servidor {host}:{porta} ficar disponível...")
    
    for tentativa in range(1, max_tentativas + 1):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(2)
            test_socket.connect((host, porta))
            test_socket.close()
            print(f"✓ Servidor {host}:{porta} está disponível!")
            return True
        except (socket.error, socket.timeout):
            print(f"  Tentativa {tentativa}/{max_tentativas} - Aguardando...")
            time.sleep(intervalo)
    
    print(f"✗ Não foi possível conectar ao servidor {host}:{porta}")
    return False

def teste_sequencial(host, porta, num_requisicoes=NUM_REQUISICOES, cliente = None):
    print(f"Realizando {num_requisicoes} requisições sequenciais para {host}:{porta}")
    
    tempos = []
    tempo_inicial = time.time()
    for i in range(num_requisicoes):
        ok, response_time, resposta = cliente.send_http_request(metodo='GET', caminho='/status')
        if ok:
            tempos.append(response_time)
            print(f'\t[{i+1}]  \t {response_time*1000:.2f} ms')
        else:
            print(f'\t[{i+1}]  \t Falha na requisição: {resposta}')
    
    tempo_total = time.time()-tempo_inicial
    media_tempos = sum(tempos)/num_requisicoes if tempos else 0
    
    print(f'Taxa de sucesso: {len(tempos)}/{num_requisicoes}')
    print(f'Tempo total = {tempo_total:.2} s')
    print(f'Tempo medio = {media_tempos*1000:.2} ms\n')
    
    return {'Tempo Total': tempo_total,
            'Tempo Medio':media_tempos}
  
  
# def teste_concorrente(host, porta, num_requisicoes=NUM_REQUISICOES, num_threads=MAX_THREADS, cliente = None):
#     print(f"Realizando {num_requisicoes} requisições sequenciais para {host}:{porta}")
    
#     tempos = []
#     tempo_inicial = time.time()
    
#     with ThreadPoolExecutor(max_conexoes=num_threads) as pool:
#         futures = []
        
    

if __name__ == "__main__":
    # Aguarda os servidores ficarem disponíveis
    servidor_host = 'servidor-sincrono'  # Ou 'servidor-assincrono'
    servidor_porta = 8080
    
    servidor_host_s = 'servidor-assincrono'  # Ou 'servidor-assincrono'
    servidor_porta_s = 8080
    
    if aguardar_servidor(servidor_host, servidor_porta):
        cliente = Cliente(servidor_host, servidor_porta)
        success, response_time, resposta = cliente.send_http_request(metodo='GET', caminho='/status')
        print(f"\nSuccess: {success}, Response Time: {response_time}")
        print(resposta)
    else:
        print("Falha ao conectar ao servidor")
        
    if aguardar_servidor(servidor_host_s, servidor_porta_s):
        cliente = Cliente(servidor_host_s, servidor_porta_s)
        success, response_time, resposta = cliente.send_http_request(metodo='GET', caminho='/status')
        print(f"\nSuccess: {success}, Response Time: {response_time}")
        print(resposta)
    else:
        print("Falha ao conectar ao servidor")