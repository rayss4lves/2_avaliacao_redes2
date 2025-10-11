import hashlib
import socket
import time
import datetime
import json
from http import HTTPStatus

PORT = 80
HOST = '0.0.0.0'

def gerar_hash():
        chave = '20239019558 Rayssa Alves'
        sha1_hash = hashlib.sha1(chave.encode()).hexdigest()
        print(sha1_hash)
        return sha1_hash

class ServidorSequencial():
    def __init__(self, host = HOST, porta = PORT):
        self.host = host
        self.porta = porta
        self.servidor_socket = None
        self.contador_requisicoes = 0
    
    def iniciar_servidor(self):
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.servidor_socket.bind((self.host, self.porta))
            self.servidor_socket.listen(1)
            print(f'Servidor iniciado em {self.host}:{self.porta}')
            while True:
                cliente, endereco = self.servidor_socket.accept()
                print(f'Conexão estabelecida com {endereco}')
                self.tratar_cliente(cliente, endereco)
        except Exception as e:
            print(f"Erro no servidor: {e}")
        finally:
            self.parar()
    
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
                        cabecalhos[chave] = valor
            
            
        except Exception as e:
            print(f"Error parsing request: {e}")
        
        return metodo_requisicao, caminho_requisicao, cabecalhos
            
    def tratar_cliente(self, cliente, endereco):
        
        try:
            tempo_inicial = time.time()
            requisicao = cliente.recv(1024)

            metodo_requisicao, caminho_requisicao, cabecalhos = self.dividir_requisicao(requisicao) 
            
            id_cliente = cabecalhos.get('id_cliente', '')
                
            self.contador_requisicoes+=1
            
            resposta = self.construir_resposta(metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial)
            
            cliente.send(resposta.encode('utf-8'))
            
            tempo_final = time.time() - tempo_inicial
            
            print(f'Tempo total {tempo_final}')
        except:
            resposta = self.mensagem_erro(500)
            corpo = json.dumps(resposta, indent=2)
            return self.montar_mensagem_http(corpo, 500, id_cliente) 
            
            
    def construir_resposta(self, metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial):
        status_code = 200
        resposta, delay = self.montar_resposta_base(metodo_requisicao, caminho_requisicao, id_cliente)
        conteudo = ''
        caminhos_validos = ['/rapido', '/medio', '/lento']
        
        if metodo_requisicao == 'Get':
            if caminho_requisicao == '/':
                conteudo = f'Bem vindo ao servidor sequencial!'
                observacao = f'Metodo GET realizado na raiz'
                

            elif caminho_requisicao in caminhos_validos:
                conteudo = f'Rota {caminho_requisicao}'
                observacao = f'Tempo de resposta {delay}'
            
            elif caminho_requisicao == '/status':
                conteudo = {"Status":"Ativo",
                            "Tipo":"Sequencial",
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
        resposta_http = self.montar_mensagem_http(corpo, status_code, id_cliente)
        
        
        return resposta_http

    def montar_resposta_base(self, metodo_requisicao, caminho_requisicao, id_cliente):
        inicio = time.time()
        delays = {'/medio':1, '/lento':2}
        delay = delays.get(caminho_requisicao, 0)
        time.sleep(delay)

        resposta = {
            'Servidor': 'Sequencial',
            'Metodo': metodo_requisicao, 
            'Caminho': caminho_requisicao,
            'Data-Hora': datetime.now().strftime('%d/%m/%m/%Y %H:%M:%S'),
            'ID_Recebido': id_cliente,
            'Duracao': round(time.time() - inicio, 4)
        }

        return resposta, delay
    
    def mensagem_erro(self, status_code):
        corpo_erro ={
            'erro': status_code,
            'mensagem': HTTPStatus(status_code).phrase,
            'timestamp':datetime.datetime.now().isoformat()
        }
        return corpo_erro
    
        

    def montar_mensagem_http(self, status_code, corpo, id_cliente):
        mensagem_requisicao = HTTPStatus(status_code).phrase
        resposta_http = (
            f'HTTP/1.1 {status_code} {mensagem_requisicao}\r\n'
            'Content-Type: application/json\r\n'
            f'Content-Length: {len(corpo)}'
            'Server: Servidor Sequencial/2.0\r\n'
            f'ID-Recebido: {id_cliente}\r\n'
            'Connection: close\r\n\r\n'
            f'{corpo}'
        )
        
        return resposta_http
    
    def parar(self):
        #Para o servidor
        if self.socket_servidor:
            self.socket_servidor.close()
            print("Servidor sequencial parado")

if __name__ == "__main__":
    servidor = ServidorSequencial()
    servidor.iniciar()


