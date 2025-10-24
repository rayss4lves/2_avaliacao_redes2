import socket
import hashlib
import time
import threading
from testes import teste_sequencial, teste_concorrente
from resultados import calcular_estatisticas, mostrar_resultados, salvar_execucoes_csv
from resultados import salvar_estatisticas_csv, grafico_vazao_execucoes, grafico_barras_throughput, grafico_tempo_execucoes


def gerar_hash():
        chave = '20239019558 Rayssa Alves'
        sha1_hash = hashlib.sha1(chave.encode()).hexdigest()
        print(sha1_hash)
        return sha1_hash

X_CUSTOM_ID = gerar_hash()
MAX_THREADS = 2
NUM_REQUISICOES_SEQ = 2
NUM_REQ_CONCORRENTE = 2
NUM_EXECUCOES = 5
 
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
            
            cabecalhos = [f"Host: {self.host}", f"X-Custom-ID: {X_CUSTOM_ID}", "Connection: close"]
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
        

if __name__ == "__main__":
    # Aguarda os servidores ficarem disponiveis
    servidor_host_sincrono = 'servidor-sincrono'
    servidor_porta_sincrono = 8080
    
    servidor_host_assincrono = 'servidor-assincrono' 
    servidor_porta_assincrono = 8080
    
    # cenarios_teste = [
    #     {'metodo':'GET', 'caminho':'/'}
    # ]
    # cenario1 = cenarios_teste[0]
    # chave1 = f"{cenario1['metodo']} - {cenario1['caminho']}"
    
    resultados_sincrono = {}
    resultados_assincrono = {}
    
    
    print('=======================TESTE DO SERVIDOR SINCRONO=======================')
    # if aguardar_servidor(servidor_host_sincrono, servidor_porta_sincrono):
    print('-----------Teste inicial-----------')
    cliente = Cliente(servidor_host_sincrono, servidor_porta_sincrono)
    success, response_time, resposta = cliente.enviar_requisicao(metodo='GET', caminho='/')
    print(f"\nSuccess: {success}, Response Time: {response_time}")
    print(resposta)
    
    resultados_sincrono['GET - /'] = []
    for i in range(NUM_EXECUCOES):
        print(f'------------------ Execucao {i+1} ------------------')
        resultado_sincrono = teste_sequencial(metodo='GET', caminho='/', cliente=cliente)
        resultados_sincrono['GET - /'].append(resultado_sincrono)
    
    
    print(resultados_sincrono['GET - /'])   
        
    print('======================TESTE DO SERVIDOR ASSINCRONO======================')
    
    print('-----------Teste inicial-----------')
    cliente = Cliente(servidor_host_assincrono, servidor_porta_assincrono)
    success, response_time, resposta = cliente.enviar_requisicao(metodo='GET', caminho='/')
    print(f"\nSuccess: {success}, Response Time: {response_time}")
    print(resposta)
    resultados_assincrono['GET - /'] = []
    for i in range(NUM_EXECUCOES):
        print(f'------------------ Execucao {i+1} ------------------')
        resultado_assincrono = teste_sequencial(metodo='GET', caminho='/', cliente=cliente)
        resultados_assincrono['GET - /'].append(resultado_assincrono)
        
    salvar_execucoes_csv(resultados_sincrono, 'sequencial', arquivo='resultados/sincrono.csv')
    salvar_execucoes_csv(resultados_assincrono, 'concorrente', arquivo='resultados/assincrono.csv')
 
    print(resultados_assincrono['GET - /'])
    
    # AGORA SALVA OS CSVs (DEPOIS DE COLETAR TODOS OS DADOS)
    print('\n======================SALVANDO RESULTADOS EM CSV======================')
    
    
    
    print('======================ESTATISTICAS DO SERVIDOR SINCRONO======================')
    # Calcular estatísticas
    stats_sinc = calcular_estatisticas(resultados_sincrono)
    
    # Mostrar resultados
    mostrar_resultados(stats_sinc)
    
    print('======================ESTATISTICAS DO SERVIDOR ASSINCRONO======================')
    # Calcular estatísticas
    stats_assinc = calcular_estatisticas(resultados_assincrono)
    
    salvar_estatisticas_csv(stats_sinc, nome_servidor='sincrono', arquivo='resultados/resultados_sincrono.csv')
    salvar_estatisticas_csv(stats_assinc, nome_servidor='assincrono', arquivo='resultados/resultados_assincrono.csv')
    
    
    print('\n======================GERANDO GRÁFICOS======================')

    grafico_vazao_execucoes('resultados/sincrono.csv', 'resultados/assincrono.csv', 'graficos/vazao_execucoes.png')
    
    grafico_barras_throughput('resultados/resultados_sincrono.csv', 'resultados/resultados_assincrono.csv', 'graficos/barras_throughput.png')
    grafico_tempo_execucoes('resultados/sincrono.csv', 'resultados/assincrono.csv', 'graficos/tempo_execucoes.png')

    
    for i in stats_assinc:
        print(i, stats_assinc[i])
    mostrar_resultados(stats_assinc)
 