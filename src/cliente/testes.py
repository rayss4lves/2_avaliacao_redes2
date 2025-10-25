import time
import threading

# Função que realiza testes sequenciais em um servidor HTTP
def teste_sequencial(metodo, caminho, num_requisicoes, cliente = None):
    tempos = []
    falhas = []
    tempo_inicial = time.time()
    for i in range(num_requisicoes):
        ok, response_time, resposta = cliente.enviar_requisicao(metodo, caminho)
        if ok:
            print(f'------------------------------ Requisicao {i+1} ------------------------------')
            # print(resposta)
            tempos.append(response_time)
            # print(f'\t[{i+1}]  \t {response_time*1000:.2f} ms')
        else:
            falhas.append(resposta)
            print(f'\t[{i+1}]  \t Falha na requisicao: {resposta}')
    
    tempo_total = time.time()-tempo_inicial
    tempo_medio_resposta = sum(tempos)/num_requisicoes if tempos else 0
    sucesso = len(tempos)
    throughput = sucesso/tempo_total if tempo_total > 0 else 0
    
    # Retorna resultados em formato de dicionário
    return {'Tempo_Total': tempo_total,
            'Tempo_Medio_Resposta':tempo_medio_resposta,
            'Throughput': throughput,
            'Requisicões Bem Sucedidas': sucesso,
            'Falhas': len(falhas)
            }
  
# Essa função executa cada thread no teste concorrente
# Realiza um conjunto de requisições para cada thread 
def executar_cliente_concorrente(num_requisicoes, cliente = None, id_thread=0, metodo='GET', caminho='/', tempos=[], lock=None, falhas=[]):
    
    for i in range(num_requisicoes):
        ok, response_time, resposta = cliente.enviar_requisicao(metodo, caminho)
        with lock:
            if ok:
                print(f'---------------- Thread[{id_thread}] Req - {i+1}\t ----------------')
                # print(resposta)
                tempos.append(response_time)
                # print(f'\tThread[{id_thread}]  Req - {i+1}\t {response_time*1000:.2f} ms')
            else:
                falhas.append(resposta)
                print(f'\tThread[{id_thread}]  Req - {i+1}\t Falha na requisicao: {resposta}')
    
# Função que realiza testes concorrentes usando múltiplas threads 
def teste_concorrente(metodo, caminho, num_requisicoes, num_threads, cliente = None, ):
    # print(f"Realizando {num_requisicoes} requisicões concorrentes para {cliente.host}:{cliente.porta} com {num_threads} threads")
    
    tempos = []
    falhas = []
    tempo_inicial = time.time()
    lock = threading.Lock()
    threads = []
    
    # Cria e inicia múltiplas threads para enviar requisições simultâneas, sem bloqueio ou espera
    for i in range(num_threads):
        thread = threading.Thread(target=executar_cliente_concorrente, args=(num_requisicoes, cliente, i+1, metodo, caminho, tempos, lock, falhas))
        threads.append(thread)
        thread.start()
    
    #aguarda todas as threads terminarem  
    for thread in threads:
        thread.join()
        
    tempo_total = time.time()-tempo_inicial
    total_requisicoes = num_requisicoes * num_threads
    sucesso = len(tempos)
    tempo_medio_resposta = sum(tempos)/sucesso if sucesso else 0
    throughput = sucesso/tempo_total if tempo_total > 0 else 0
    
    # Retorna resultados em formato de dicionário
    return {'Tempo_Total': tempo_total,
            'Tempo_Medio_Resposta':tempo_medio_resposta,
            'Throughput': throughput,
            'Requisicões Bem Sucedidas': sucesso,
            'Falhas': len(falhas)
            }
 