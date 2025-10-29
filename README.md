# Segunda Avaliação de Redes de Computadores II - 2025-2

**UFPI - CSHNB | Sistemas de Informação | Trabalho Individual**

- **Autor**: Rayssa dos Santos Alves
- **Matrícula**: 20239019558
- **Entrega**: 29/10/2025
- [Link para o vídeo do YouTube] (https://youtu.be/BOhxza3uXfM?si=KPgu8P8ZaCOK4N_W)

## 🎯 Projeto
Este projeto implementa uma simulação de sistemas cliente-servidor para uma comparação de desempenho entre os servidores sequencial e concorrente, usando sockets TCP/IP com protocolo HTTP. O objetivo é avaliar métricas como throughput, tempo de resposta.

## 🏗️ Estrutura

```
.
├── graficos/                          # Gráficos gerados das análises
│   ├── barras_throughput.png
│   ├── tempo_execucoes.png
│   └── vazao_execucoes.png
├── src/
│   ├── cliente/                       # Implementação do cliente
│   │   ├── cliente.py
│   │   ├── dockerfile.cliente
│   │   ├── resultados.py
│   │   └── testes.py
│   ├── servidor_assincrono/           # Servidor assíncrono
│   │   ├── dockerfile.assincrono
│   │   └── servidorAssincrono.py
│   └── servidor_sincrono/             # Servidor síncrono
│       ├── dockerfile.sincrono
│       └── servidorSincrono.py
├── docker-compose.yaml                # Orquestração dos containers
├── comandos_docker.txt                # Comandos úteis do Docker
└── Avaliacao Redes 2 2025-2.pdf      # Especificação do trabalho

```

## Descrição dos Módulos

## 📁 `graficos/`
Contém os gráficos gerados automaticamente após a execução dos testes, apresentando comparações visuais entre os dois servidores.

## 📁 `src/cliente/`
- **cliente.py**: Classe que implementa o cliente HTTP, responsável por enviar requisições 
- **testes.py**: Arquivo de testes automatizados que executa múltiplas requisições e medir tempos de resposta
- **resultados.py**: Processa dados coletados, calcula estatísticas (média, desvio padrão) e gera gráficos
- **dockerfile.cliente**: Configuração do container Ubuntu para o cliente

## 📁 `src/servidor_sincrono/`
- **servidorSincrono.py**: Implementação do servidor sequencial que processa uma requisição por vez
- **dockerfile.sincrono**: Configuração do container Ubuntu para o servidor síncrono

## 📁 `src/servidor_assincrono/`
- **servidorAssincrono.py**: Implementação do servidor concorrente usando threading para processar múltiplas requisições simultaneamente
- **dockerfile.assincrono**: Configuração do container Ubuntu para o servidor assíncrono

## 🔧 Tecnologias
- **Python 3.12**: Linguagem de programação
- **Sockets TCP/IP**: Comunicação de rede de baixo nível
- **Protocolo HTTP**: Estruturação manual de mensagens
- **Docker**: Virtualização e isolamento de containers
- **Threading**: Implementação de paralelismo no servidor concorrente

## 🌐 Configuração de Rede

- **IPs baseados na matrícula**: Últimos 4 dígitos da matricula
- Subrede: `95.58.0.0/24`
- IP dos containers:
    - Servidor-Sequêncial: `95.58.0.2`,
    - Servidor-Concorrente: `95.58.0.3`,
    - Cliente: `95.58.0.4`
- **Cabeçalho obrigatório** [Matricula + Nome]:
  ```
    - `X-Custom-ID: [HASH_SHA1(20239019558 + Rayssa Alves)]`
  ```
- **Porta**: Os dois servidores escutam na porta **80**

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados

### Execução

```bash
# 1. Clonar repositório
git clone <https://github.com/rayss4lves/2_avaliacao_redes2.git>
cd 2_avaliacao_redes2

# 2. Iniciar containers
docker-compose up --build           #inicia tos os containers e executa os testes

```

## 📊 Implementação

### Servidor Sequencial
Processa uma requisição por vez na porta 80 com mensagens HTTP validadas.

### Servidor Concorrente
Utiliza threads para processar múltiplas requisições simultaneamente na porta 80.

### Primitivas HTTP Implementadas
- **GET**: Recuperação de recursos do servidor
    - Optei por implementar apenas a primitiva GET, porque no contexto deste projeto, as demais primitivas HTTP não apresentariam diferenças sigificativas na lógica do tratamento. A escolha visou simplificr a estrutura sem comprometer a análise de desempenho entre os servidores.

## 📈 Métricas Avaliadas

- **Throughput**
- **Tempo de Resposta**
- **Tempo Total**
- **Taxa de sucesso**
  
### Metodologia Estatística
- **20 execuções** por teste dos servidores
- **10** Threads para o servidor Assíncrono (Concorrente)
- **50** Requisições em cada execução dos testes
- Cálculo de **média e desvio padrão** para cada métrica
- Análise comparativa entre servidores sequencial e concorrente


**Professor**: Rayner Gomes 

---
