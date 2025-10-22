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

def comparar_estatisticas(stats_sinc, stats_assinc, plotar=True):
    """
    Compara estatísticas síncronas e assíncronas.
    
    stats_sinc / stats_assinc: dicionários no formato
        { 'cenario1': {'media': x, 'desvio': y}, ... }
    
    plotar: se True, gera gráfico de barras com médias e desvios.
    
    Retorna um dicionário com a comparação.
    """
    comparacao = {}

    for cenario in stats_sinc:
        media_sinc = stats_sinc[cenario]['media']
        desvio_sinc = stats_sinc[cenario]['desvio']
        media_assinc = stats_assinc[cenario]['media']
        desvio_assinc = stats_assinc[cenario]['desvio']

        diff_percent = ((media_assinc - media_sinc) / media_sinc) * 100
        melhor = 'Assíncrono' if media_assinc < media_sinc else 'Síncrono'

        comparacao[cenario] = {
            'media_sinc': media_sinc,
            'desvio_sinc': desvio_sinc,
            'media_assinc': media_assinc,
            'desvio_assinc': desvio_assinc,
            'diff_percent': diff_percent,
            'melhor': melhor
        }

    # Exibir tabela
    print(f"{'Cenário':<15} {'Síncrono':<20} {'Assíncrono':<20} {'Diferença (%)':<15} {'Melhor'}")
    for cenario, dados in comparacao.items():
        print(f"{cenario:<15} "
              f"{dados['media_sinc']:.3f}s ± {dados['desvio_sinc']:.3f}s   "
              f"{dados['media_assinc']:.3f}s ± {dados['desvio_assinc']:.3f}s   "
              f"{dados['diff_percent']:+.2f}%       {dados['melhor']}")

    # Gerar gráfico se necessário
    if plotar:
        cenarios = list(comparacao.keys())
        media_sinc_vals = [comparacao[c]['media_sinc'] for c in cenarios]
        media_assinc_vals = [comparacao[c]['media_assinc'] for c in cenarios]
        desvio_sinc_vals = [comparacao[c]['desvio_sinc'] for c in cenarios]
        desvio_assinc_vals = [comparacao[c]['desvio_assinc'] for c in cenarios]

        x = range(len(cenarios))
        plt.bar(x, media_sinc_vals, yerr=desvio_sinc_vals, width=0.4, label='Síncrono', align='center')
        plt.bar([i + 0.4 for i in x], media_assinc_vals, yerr=desvio_assinc_vals, width=0.4, label='Assíncrono', align='center')
        plt.xticks([i + 0.2 for i in x], cenarios)
        plt.ylabel('Tempo médio (s)')
        plt.title('Comparação Síncrono vs Assíncrono')
        plt.legend()
        plt.show()

    return comparacao

