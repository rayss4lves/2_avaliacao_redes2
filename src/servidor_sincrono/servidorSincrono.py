import hashlib
import socket
import time
import datetime
import json
from http import HTTPStatus

PORT = 8080
HOST = '0.0.0.0'

def gerar_hash():
    chave = '20239019558 Rayssa Alves'
    sha1_hash = hashlib.sha1(chave.encode()).hexdigest()
    return sha1_hash

ID_ESPERADO = gerar_hash()

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
            self.servidor_socket.bind((HOST, PORT))
            self.servidor_socket.listen(5)
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
                        cabecalhos[chave.strip()] = valor.strip()
            
            
        except Exception as e:
            print(f"Error parsing request: {e}")
        
        return metodo_requisicao, caminho_requisicao, cabecalhos
            
    def tratar_cliente(self, cliente, endereco):
        
        try:
            tempo_inicial = time.time()
            requisicao = cliente.recv(1024)

            metodo_requisicao, caminho_requisicao, cabecalhos = self.dividir_requisicao(requisicao) 
            
            id_cliente = cabecalhos.get('X-Custom-ID', '')
            
            if id_cliente != ID_ESPERADO:
                resposta_erro = self.mensagem_erro(401, id_cliente)
                corpo = json.dumps(resposta_erro, indent=2)
                resposta = self.montar_mensagem_http(401, corpo, id_cliente)
                cliente.sendall(resposta.encode('utf-8'))
            else:
                self.contador_requisicoes+=1
            
                resposta = self.construir_resposta(metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial)
                
                cliente.sendall(resposta.encode('utf-8'))
            
        except:
            resposta_erro = self.mensagem_erro(500)
            corpo = json.dumps(resposta_erro, indent=2)
            resposta = self.montar_mensagem_http(500, corpo, id_cliente)
            cliente.sendall(resposta.encode('utf-8'))

        finally:
            cliente.close()
            print(f'Conexão com {endereco} encerrada')
            
            
    def construir_resposta(self, metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial):
        status_code = 200
        resposta = self.montar_resposta_base(metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial)
        conteudo = ''
        
        if metodo_requisicao == 'GET':
            if caminho_requisicao == '/':
                conteudo = f'Bem vindo ao servidor sequencial!'
                observacao = f'Metodo GET realizado na raiz'
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
        resposta_http = self.montar_mensagem_http(status_code, corpo, id_cliente)
        
        
        return resposta_http

    def montar_resposta_base(self, metodo_requisicao, caminho_requisicao, id_cliente, tempo_inicial):
        
        resposta = {
            'Servidor': 'Sequencial',
            'Metodo': metodo_requisicao, 
            'Caminho': caminho_requisicao,
            'Data-Hora': datetime.datetime.now().strftime('%d/%m/%m/%Y %H:%M:%S'),
            'X-Custom-ID': id_cliente,
            'Duracao': round(time.time() - tempo_inicial, 4)
        }

        return resposta
    
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
            f'Content-Length: {len(corpo)}\r\n'
            'Server: Servidor Sequencial/2.0\r\n'
            f'ID-Recebido: {id_cliente}\r\n'
            'Connection: close\r\n\r\n'
            f'{corpo}'
        )
        
        return resposta_http
    
    def parar(self):
        #Para o servidor
        if self.servidor_socket:
            self.servidor_socket.close()
            print("Servidor sequencial parado")

if __name__ == "__main__":
    servidor = ServidorSequencial()
    servidor.iniciar_servidor()
