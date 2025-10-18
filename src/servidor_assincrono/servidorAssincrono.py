import hashlib
import socket
import time
import datetime
import json
from http import HTTPStatus
import threading

PORT = 8080
HOST = '0.0.0.0'
MAX_CONEXOES = 10

class ServidorConcorrente():
    def __init__(self, host = HOST, porta = PORT):
        self.host = host
        self.porta = porta
        self.servidor_socket = None
        self.contador_requisicoes = 0
        self.lock = threading.Lock()
        self.conexoes_ativas = 0
    
    def iniciar_servidor(self):
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.servidor_socket.bind((self.host, self.porta))
            self.servidor_socket.listen(MAX_CONEXOES)
            print(f'Servidor iniciado em {self.host}:{self.porta}')
            while True:
                cliente, endereco = self.servidor_socket.accept()
                thread_cliente = threading.Thread(target=self.gerenciar_cliente, args=(cliente, endereco))
                thread_cliente.daemon = True
                thread_cliente.start()
        except Exception as e:
            print(f"Erro no servidor: {e}")
        finally:
            self.parar()
            
    def gerenciar_cliente(self, cliente, endereco):
        with self.lock:
            self.conexoes_ativas += 1
            id_conexao = self.conexoes_ativas
            
        print(f'Conexao {id_conexao} estabelecida com {endereco}')
        
        try:
            self.tratar_cliente(cliente, endereco, id_conexao)
        finally:
            with self.lock:
                self.conexoes_ativas-=1
            cliente.close()
            print(f'conexao {id_conexao} finalizada')
    
    # Separa a primeira linha (ex: GET /status HTTP/1.1)
    def dividir_requisicao(self, requisicao):
        cabecalhos = {}
        metodo_requisicao = None
        caminho_requisicao = None
        try:
            linhas_requisicao = requisicao.decode('utf-8', errors='ignore').split('\r\n')
            if linhas_requisicao or linhas_requisicao[0]:
                campos_requisicao = linhas_requisicao[0].split()

                if len(campos_requisicao) >= 3:
                    metodo_requisicao, caminho_requisicao, _ = campos_requisicao[0], campos_requisicao[1], campos_requisicao[2] 
                
                for linha in linhas_requisicao[1:]:
                    if ':' in linha:
                        chave, valor = linha.split(':', 1)
                        cabecalhos[chave.strip()] = valor.strip()
            
            
        except Exception as e:
            print(f"Error parsing request: {e}")
        
        return metodo_requisicao, caminho_requisicao, cabecalhos
            
    def tratar_cliente(self, cliente, endereco, id_conexao):
        
        try:
            tempo_inicial = time.time()
            requisicao = cliente.recv(1024)

            metodo_requisicao, caminho_requisicao, cabecalhos = self.dividir_requisicao(requisicao) 
            
            id_cliente = cabecalhos.get('id_cliente', '')
            
            with self.lock:  
                self.contador_requisicoes+=1
                requisicao_atual = self.contador_requisicoes
            
            resposta = self.construir_resposta(metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial, requisicao_atual, id_conexao)
            
            cliente.sendall(resposta.encode('utf-8'))
            
            tempo_final = time.time() - tempo_inicial
            
            print(f'Requisicao {requisicao_atual} (conexao {id_conexao}) Tempo total {tempo_final}')
        except:
            resposta_erro = self.mensagem_erro(500, id_conexao)
            corpo = json.dumps(resposta_erro, indent=2)
            resposta = self.montar_mensagem_http(500, corpo, id_cliente, id_conexao)
            cliente.sendall(resposta.encode('utf-8'))
            
            
    def construir_resposta(self, metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial, requisicao_atual, id_conexao):
        status_code = 200
        resposta, delay = self.montar_resposta_base(metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial, requisicao_atual, id_conexao)
        conteudo = ''
        caminhos_validos = ['/rapido', '/medio', '/lento']
        
        if metodo_requisicao == 'GET':
            if caminho_requisicao == '/':
                conteudo = f'Bem vindo ao servidor Concorrente!'
                observacao = f'Metodo GET realizado na raiz'
                

            elif caminho_requisicao in caminhos_validos:
                conteudo = f'Rota {caminho_requisicao}'
                observacao = f'Tempo de resposta {delay}'
            
            elif caminho_requisicao == '/status':
                conteudo = {"Status":"Ativo",
                            "Tipo":"Concorrente",
                            "Quantidade de requisicoes": self.contador_requisicoes
                            }
                observacao = f'Status consultado'
            else:
                status_code = 404
                conteudo = f'Caminho nao encontrado'
                observacao = f'Erro'
        elif metodo_requisicao == 'POST':
            if caminho_requisicao == '/dados':
                conteudo = f'Dados recebidos com sucesso!'
                observacao = f'POST executado.'
            else:
                status_code = 404
                conteudo = f'Caminho nao encontrado'
                observacao = f'Erro'
        else:
            status_code = 404
            conteudo = f'Caminho nao encontrado'
            observacao = f'Erro'
            
        
        resposta.update({
            'Mensagem': observacao,
            'Conteudo': conteudo
        })
        
        corpo = json.dumps(resposta, indent=2)
        resposta_http = self.montar_mensagem_http(status_code, corpo, id_cliente, id_conexao)
        
        
        return resposta_http

    def montar_resposta_base(self, metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial, requisicao_atual, id_conexao):
        delays = {'/medio':1, '/lento':2}
        delay = delays.get(caminho_requisicao, 0)
        time.sleep(delay)

        resposta = {
            'Servidor': 'Concorrente',
            'Metodo': metodo_requisicao, 
            'Caminho': caminho_requisicao,
            'Numero da Requisicao': requisicao_atual,
            'Id_conexao': id_conexao,
            'Data-Hora': datetime.datetime.now().strftime('%d/%m/%m/%Y %H:%M:%S'),
            'ID_Recebido': id_cliente,
            'ID_thread': threading.current_thread().ident,
            'Duracao': round(time.time() - tempo_inicial, 4)
        }

        return resposta, delay
    
    def mensagem_erro(self, status_code, id_conexao):
        corpo_erro ={
            'erro': status_code,
            'mensagem': HTTPStatus(status_code).phrase,
            'timestamp':datetime.datetime.now().isoformat(),
            'tipo_servidor': 'concorrente',
            'id_conexao': id_conexao,
            'id_thread': threading.current_thread().ident
        }
        return corpo_erro
    
        

    def montar_mensagem_http(self, status_code, corpo, id_cliente, id_conexao):
        mensagem_requisicao = HTTPStatus(status_code).phrase
        resposta_http = (
            f'HTTP/1.1 {status_code} {mensagem_requisicao}\r\n'
            'Content-Type: application/json\r\n'
            f'Content-Length: {len(corpo.encode("utf-8"))}\r\n'
            'Server: Servidor Concorrente\r\n'
            f'ID-Recebido: {id_cliente}\r\n'
            f'ID-Thread: {threading.current_thread().ident}\r\n'
            f'ID-Conexao: {id_conexao}\r\n'
            'Connection: close\r\n\r\n'
            f'{corpo}'
            )

        return resposta_http
    
    def parar(self):
        #Para o servidor
        if self.servidor_socket:
            self.servidor_socket.close()
            print("Servidor Concorrente parado")

if __name__ == "__main__":
    servidor = ServidorConcorrente()
    servidor.iniciar_servidor()


