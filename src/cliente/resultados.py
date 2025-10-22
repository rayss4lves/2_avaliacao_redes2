import statistics
# import matplotlib.pyplot as plt
# import numpy as np
  

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


def calcular_estatisticas(resultados):
    resultados_estatisticas = {}
    
    for cenario, execucoes in resultados.items():
        resultados_estatisticas[cenario] = {}
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


import matplotlib.pyplot as plt

