import statistics
# import matplotlib.pyplot as plt
# import numpy as np
 
 
import csv
import os
from datetime import datetime

def salvar_estatisticas_csv(estatisticas, nome_servidor, arquivo='resultados/estatisticas.csv'):
    """
    Salva as ESTATÍSTICAS (médias e desvios) em CSV
    
    Args:
        estatisticas: dicionário retornado por calcular_estatisticas()
        nome_servidor: 'sincrono' ou 'assincrono'
        arquivo: caminho do arquivo
    """
    os.makedirs(os.path.dirname(arquivo) if os.path.dirname(arquivo) else '.', exist_ok=True)
    arquivo_existe = os.path.exists(arquivo)

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
        print("⚠️ Nenhuma estatística para salvar")
        return

    campos = ['timestamp', 'servidor', 'cenario', 'metrica', 'media', 'desvio_padrao']
    with open(arquivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if not arquivo_existe:
            writer.writeheader()
        writer.writerows(linhas)

    print(f"✓ Estatísticas salvas em {arquivo} - {len(linhas)} linhas")
 

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
    """
    Exibe os resultados das estatísticas de forma formatada
    """
    print("=" * 80)
    print("RESULTADOS DAS ESTATÍSTICAS")
    print("=" * 80)
    
    for cenario, metricas in estatisticas.items():
        print(f"\n{cenario}:")
        print("-" * 80)
        
        for metrica, valores in metricas.items():
            media = valores['Media']
            desvio = valores['Desvio Padrao']
            print(f"  {metrica:.<40} Média: {media:>10.2f} | Desvio: {desvio:>10.2f}")


