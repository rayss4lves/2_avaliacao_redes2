import time
import threading

# MAX_THREADS = 5
# NUM_REQUISICOES_SEQ = 5
# NUM_REQ_CONCORRENTE = 2

def teste_sequencial(metodo, caminho, num_requisicoes, cliente = None):
    tempos = []
    falhas = []
    tempo_inicial = time.time()
    for i in range(num_requisicoes):
        ok, response_time, resposta = cliente.enviar_requisicao(metodo, caminho)
        if ok:
            # print(f'------------------------------ Requisicao {i+1} ------------------------------')
            # print(resposta)
            tempos.append(response_time)
            # print(f'\t[{i+1}]  \t {response_time*1000:.2f} ms')
        else:
            falhas.append(resposta)
            print(f'\t[{i+1}]  \t Falha na requisicao: {resposta}')
    
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
            'Requisicões Bem Sucedidas': sucesso,
            'Falhas': len(falhas)
            }
  
  
def executar_cliente_concorrente(num_requisicoes, cliente = None, id_thread=0, metodo='GET', caminho='/', tempos=[], lock=None, falhas=[]):
    
    for i in range(num_requisicoes):
        ok, response_time, resposta = cliente.enviar_requisicao(metodo, caminho)
        with lock:
            if ok:
                # print(f'---------------- Thread[{id_thread}] ----------------')
                # print(resposta)
                tempos.append(response_time)
                # print(f'\tThread[{id_thread}]  Req - {i+1}\t {response_time*1000:.2f} ms')
            else:
                falhas.append(resposta)
                print(f'\tThread[{id_thread}]  Req - {i+1}\t Falha na requisicao: {resposta}')
    
  
def teste_concorrente(metodo, caminho, num_requisicoes, num_threads, cliente = None, ):
    print(f"Realizando {num_requisicoes} requisicões concorrentes para {cliente.host}:{cliente.porta} com {num_threads} threads")
    
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
    print(f'Total de requisicões: {total_requisicoes}\n')
    
    
    return {'Tempo Total': tempo_total,
            'Tempo Medio':media_tempos,
            'Throughput (req/s)': throughput,
            'Requisicões Bem Sucedidas': sucesso,
            'Falhas': len(falhas)
            }
 