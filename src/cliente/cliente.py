import socket
import hashlib
import time
import threading


def gerar_hash():
        chave = '20239019558 Rayssa Alves'
        sha1_hash = hashlib.sha1(chave.encode()).hexdigest()
        print(sha1_hash)
        return sha1_hash

ID_CLIENTE = gerar_hash()
MAX_THREADS = 5
NUM_REQUISICOES = 5
 
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
            print(f"Servidor {host}:{porta} está disponível!")
            return True
        except (socket.error, socket.timeout):
            print(f"  Tentativa {tentativa}/{max_tentativas} - Aguardando...")
            time.sleep(intervalo)
    
    print(f"Não foi possível conectar ao servidor {host}:{porta}")
    return False

def teste_sequencial(metodo, caminho, num_requisicoes=NUM_REQUISICOES, cliente = None):
    print(f"Realizando {num_requisicoes} requisições sequenciais para {cliente.host}:{cliente.porta}")
    
    tempos = []
    falhas = []
    tempo_inicial = time.time()
    for i in range(num_requisicoes):
        ok, response_time, resposta = cliente.enviar_requisicao(metodo, caminho)
        if ok:
            print(f'------------------------------ Requisição {i+1} ------------------------------')
            print(resposta)
            tempos.append(response_time)
            print(f'\t[{i+1}]  \t {response_time*1000:.2f} ms')
        else:
            falhas.append(resposta)
            print(f'\t[{i+1}]  \t Falha na requisição: {resposta}')
    
    tempo_total = time.time()-tempo_inicial
    media_tempos = sum(tempos)/num_requisicoes if tempos else 0
    sucesso = len(tempos)
    throughput = sucesso/tempo_total if tempo_total > 0 else 0
    
    print(f'Taxa de sucesso: {len(tempos)}/{num_requisicoes}')
    print(f'Tempo total = {tempo_total:.2f} s')
    print(f'Tempo medio = {media_tempos*1000:.2f} ms\n')
    print(f'Throughput = {throughput:.2f} req/s\n')
    
    
    return {'Tempo Total': tempo_total,
            'Tempo Medio':media_tempos,
            'Throughput (req/s)': throughput,
            'Requisições Bem Sucedidas': sucesso,
            'Falhas': len(falhas)
            }
  
  
def executar_cliente_concorrente(num_requisicoes=NUM_REQUISICOES, cliente = None, id_thread=0, metodo='GET', caminho='/', tempos=[], lock=None, falhas=[]):
    
    for i in range(num_requisicoes):
        ok, response_time, resposta = cliente.enviar_requisicao(metodo, caminho)
        with lock:
            if ok:
                tempos.append(response_time)
                print(f'\tThread[{id_thread}]  Req - {i+1}\t {response_time*1000:.2f} ms')
            else:
                falhas.append(resposta)
                print(f'\tThread[{id_thread}]  Req - {i+1}\t Falha na requisição: {resposta}')
    
  
def teste_concorrente(num_requisicoes=NUM_REQUISICOES, num_threads=MAX_THREADS, cliente = None, metodo='GET', caminho='/'):
    print(f"Realizando {num_requisicoes} requisições concorrentes para {cliente.host}:{cliente.porta} com {num_threads} threads")
    
    tempos = []
    falhas = []
    tempo_inicial = time.time()
    lock = threading.Lock()
    threads = []
    
    for i in range(num_threads):
        thread = threading.Thread(target=executar_cliente_concorrente, args=(num_requisicoes, cliente, i+1, metodo, caminho, tempos, lock, falhas))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
        
    tempo_total = time.time()-tempo_inicial
    total_requisicoes = num_requisicoes * num_threads
    sucesso = len(tempos)
    media_tempos = sum(tempos)/sucesso if sucesso else 0
    throughput = sucesso/tempo_total if tempo_total > 0 else 0
    
    print(f'Taxa de sucesso: {len(tempos)}/{num_requisicoes}')
    print(f'Tempo total = {tempo_total:.2f} s')
    print(f'Tempo medio = {media_tempos*1000:.2f} ms\n')
    print(f'Throughput = {throughput:.2f} req/s\n')
    print(f'Falhas: {len(falhas)}\n')
    print(f'Total de requisições: {total_requisicoes}\n')
    
    
    return {'Tempo Total': tempo_total,
            'Tempo Medio':media_tempos,
            'Throughput (req/s)': throughput,
            'Requisições Bem Sucedidas': sucesso,
            'Falhas': len(falhas)
            }
       
        
    

if __name__ == "__main__":
    # Aguarda os servidores ficarem disponíveis
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
    if aguardar_servidor(servidor_host_sincrono, servidor_porta_sincrono):
        print('-----------Teste inicial-----------')
        cliente = Cliente(servidor_host_sincrono, servidor_porta_sincrono)
        success, response_time, resposta = cliente.enviar_requisicao(metodo='GET', caminho='/')
        print(f"\nSuccess: {success}, Response Time: {response_time}")
        print(resposta)
        for cenario in cenarios_teste:
            resultado_sincrono = teste_sequencial(metodo=cenario['metodo'], caminho=cenario['caminho'], cliente=cliente)
            resultados_sincrono.append(resultado_sincrono)
    else:
        print("Falha ao conectar ao servidor")
    
    print(resultados_sincrono[0])   
        
    print('======================TESTE DO SERVIDOR ASSINCRONO======================')
    if aguardar_servidor(servidor_host_assincrono, servidor_porta_assincrono):
        print('-----------Teste inicial-----------')
        cliente = Cliente(servidor_host_assincrono, servidor_porta_assincrono)
        success, response_time, resposta = cliente.enviar_requisicao(metodo='GET', caminho='/')
        print(f"\nSuccess: {success}, Response Time: {response_time}")
        print(resposta)
        for cenario in cenarios_teste:
            resultado_assincrono = teste_concorrente(metodo=cenario['metodo'], caminho=cenario['caminho'], cliente=cliente)
            resultados_assincrono.append(resultado_assincrono)
    else:
        print("Falha ao conectar ao servidor")
        
    print(resultados_assincrono[0]) 