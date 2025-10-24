import statistics
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
 
import csv
import os
from datetime import datetime


def salvar_execucoes_csv(resultados, nome_servidor, arquivo='resultados/execucoes.csv'):
    
    os.makedirs(os.path.dirname(arquivo) if os.path.dirname(arquivo) else '.', exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    linhas = []
    for cenario, execucoes in resultados.items():
        for i, execucao in enumerate(execucoes, start=1):
            linha = {
                "timestamp": timestamp,
                "servidor": nome_servidor,
                "cenario": cenario,
                "execucao": i,
            }
            # Adiciona todas as métricas do dicionario de execuçao
            linha.update(execucao)
            linhas.append(linha)
    
    if not linhas:
        print("Nenhuma execuçao para salvar")
        return
    
    # Determinar todas as colunas: timestamp, servidor, cenario, execucao + chaves das métricas
    campos_base = ['timestamp', 'servidor', 'cenario', 'execucao']
    campos_metrica = set()
    for linha in linhas:
        campos_metrica.update(k for k in linha.keys() if k not in campos_base)
    campos = campos_base + sorted(campos_metrica)
    
    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(linhas)
    

def salvar_estatisticas_csv(estatisticas, nome_servidor, arquivo='resultados/estatisticas.csv'):
   
    os.makedirs(os.path.dirname(arquivo) if os.path.dirname(arquivo) else '.', exist_ok=True)

    linhas = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for cenario, metricas in estatisticas.items():
        for metrica_nome, valores in metricas.items():
            linha = {
                "timestamp": timestamp,
                "servidor": nome_servidor,
                "cenario": cenario,
                "metrica": metrica_nome,
                "media": valores['Media'],
                "desvio_padrao": valores['Desvio Padrao']
            }
            linhas.append(linha)

    if not linhas:
        print("Nenhuma estatística para salvar")
        return

    campos = ['timestamp', 'servidor', 'cenario', 'metrica', 'media', 'desvio_padrao']
    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(linhas)


def calcular_estatisticas(resultados):
    
    resultados_estatisticas = {}
    
    for cenario, execucoes in resultados.items():
        resultados_estatisticas[cenario] = {}
        # execucoes == {'Tempo Total': , 'Tempo Medio': , 'Throughput (req/s)': , 
        #  'Requisicões Bem Sucedidas': , 'Falhas': }
        campos = execucoes[0].keys()
        
        for campo in campos:
            valores = []
            
            for execucao in execucoes:
                valores.append(execucao[campo])
            media = statistics.mean(valores)
            desvio = statistics.stdev(valores)
            resultados_estatisticas[cenario][campo] = {'Media': media, 'Desvio Padrao': desvio}
        
    return resultados_estatisticas


def mostrar_resultados(estatisticas):
    
    print('================================= RESULTADOS DAS ESTATÍSTICAS =================================')
    
    for cenario, metricas in estatisticas.items():
        
        for metrica, valores in metricas.items():
            media = valores['Media']
            desvio = valores['Desvio Padrao']
            print(f"  {metrica:.<40} Média: {media:>10.2f} | Desvio: {desvio:>10.2f}")

def grafico_vazao_execucoes(arquivo_sincrono='resultados_sincrono.csv', arquivo_assincrono='resultados_assincrono.csv', output='../../graficos/vazao_execucoes.png'):
    
    # Diretório base e criaçao da pasta graficos
    os.makedirs(os.path.dirname(output) if os.path.dirname(output) else '.', exist_ok=True)

    # Carregar dados
    df_sincrono = pd.read_csv(arquivo_sincrono)
    df_assincrono = pd.read_csv(arquivo_assincrono)

    # Obter lista da coluna Throughput
    vazao_sincrono = df_sincrono['Throughput (req/s)'].tolist()
    vazao_assincrono = df_assincrono['Throughput (req/s)'].tolist()

    # Criar figura
    plt.figure(figsize=(14, 8))
    plt.plot(range(1, len(vazao_sincrono) + 1), vazao_sincrono, marker='o', label='Servidor Sequencial')
    plt.plot(range(1, len(vazao_assincrono) + 1), vazao_assincrono, marker='s', label='Servidor Concorrente')

    plt.xlabel('Número da Execuçao')
    plt.ylabel('Vazao (req/s)')
    plt.title('Comparaçao de Vazao: Sequencial vs Concorrente')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    
def grafico_tempo_execucoes(arquivo_sincrono='resultados_sincrono.csv', arquivo_assincrono='resultados_assincrono.csv', output='../../graficos/tempo_execucoes.png'):
    # Diretório base e criaçao da pasta graficos
    os.makedirs(os.path.dirname(output) if os.path.dirname(output) else '.', exist_ok=True)

    # Carregar dados
    df_sincrono = pd.read_csv(arquivo_sincrono)
    df_assincrono = pd.read_csv(arquivo_assincrono)

    # Obter lista da coluna de tempo
    tempo_sincrono = df_sincrono['Tempo Total'].tolist()
    tempo_assincrono = df_assincrono['Tempo Total'].tolist()

    # Criar figura
    plt.figure(figsize=(14, 8))
    plt.plot(range(1, len(tempo_sincrono) + 1), tempo_sincrono, marker='o', label='Servidor Sequencial')
    plt.plot(range(1, len(tempo_assincrono) + 1), tempo_assincrono, marker='s', label='Servidor Concorrente')

    plt.xlabel('Número da Execuçao')
    plt.ylabel('Tempo de Execuçao (s)')
    plt.title(f'Comparaçao de Tempo de Execuçao: Sequencial vs Concorrente')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    
    
def grafico_barras_throughput(arquivo_sincrono='resultados_sincrono.csv', arquivo_assincrono='resultados_assincrono.csv', output='../../graficos/barras_throughput.png'):

    # Diretório base e criaçao da pasta graficos
    os.makedirs(os.path.dirname(output) if os.path.dirname(output) else '.', exist_ok=True)

    # Carregar dados
    df_sincrono = pd.read_csv(arquivo_sincrono)
    df_assincrono = pd.read_csv(arquivo_assincrono)

    # Filtrar apenas a métrica Throughput
    tp_sincrono = df_sincrono.loc[df_sincrono['metrica'] == 'Throughput (req/s)', 'media'].values[0]
    tp_assincrono = df_assincrono.loc[df_assincrono['metrica'] == 'Throughput (req/s)', 'media'].values[0]

    # Criar grafico de barras
    servidores = ['Sequencial', 'Concorrente']
    valores = [tp_sincrono, tp_assincrono]

    plt.figure(figsize=(8, 6))
    barras = plt.bar(servidores, valores, color=['skyblue', 'salmon'])
    
    plt.ylabel('Throughput (req/s)')
    plt.title('Comparaçao de Média de Throughput')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adicionar valores no topo das barras
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, altura + altura*0.01, f"{altura:.2f}", 
                 ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
