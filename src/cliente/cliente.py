import socket
import hashlib
import time


def gerar_hash():
        chave = '20239019558 Rayssa Alves'
        sha1_hash = hashlib.sha1(chave.encode()).hexdigest()
        print(sha1_hash)
        return sha1_hash

ID_CLIENTE = gerar_hash()
 
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