import csv
import networkx as nx

def leArquivo(file):  
    linhas = []  # Lista para armazenar cada linha do arquivo CSV
    with open(file, 'r', encoding='utf-8') as file_obj:
        reader = csv.DictReader (file_obj) # Usando DictReader para ler como dicionários
        print("Arquivo recebido: ")
        for row in reader:
            print(row)
            linhas.append(row)  # Adiciona cada linha lida à lista
    return linhas  # Retorna a lista de linhas após ler todas elas
    
import networkx as nx

def criaGrafoDeDisciplinas(dados):
    G = nx.DiGraph()  # Grafo direcionado
    
    # Adiciona os nós de s e t
    G.add_node("s")
    G.add_node("t")
    
    duracoes = {}
       
    for row in dados:
        codigo = row['Código']
        nome = row['Nome']
        periodo = int(row['Período'])
        duracao = int(row['Duração'])
        dependencias = row['Dependências'].replace(';', ',').split(',') if row['Dependências'] else []
        
        # Remove espaços em branco e entradas vazias
        dependencias = [dep.strip() for dep in dependencias if dep.strip()]
        
        G.add_node(codigo, name=nome, periodo=periodo)
        duracoes[codigo] = duracao  # Armazena a duração de cada curso
        
        has_dependencies = False
        
        # Adiciona arestas com base nas dependências
        for dep in dependencias:
            if dep in duracoes:  # Verifica se a dependência está presente no dicionário
                G.add_edge(dep, codigo, peso=duracoes[dep])
                has_dependencies = True
        
        # Se a tarefa não tiver dependências, conecta ao nó de s
        if not has_dependencies:
            G.add_edge("s", codigo, peso=0)
            
        G.add_edge(codigo, "t", peso=duracao)  # Conecta todos os nós a t
    
    return G

def calcularCaminhoMaximoBellmanFord(G, s):
    # Inicializa distâncias e predecessores
    dist = {v: float('-inf') for v in G.nodes}
    pred = {v: None for v in G.nodes}
    dist[s] = 0

    # Relaxamento das arestas
    for _ in range(len(G.nodes) - 1):
        trocou = False
        for u, v in G.edges:
            if dist[v] < dist[u] + G.edges[u, v]['peso']:
                dist[v] = dist[u] + G.edges[u, v]['peso']
                pred[v] = u
                trocou = True
        
        # Se não houve troca, encerra prematuramente
        if not trocou:
            break
    
    return pred

def reconstruirCaminho(pred, s, t):
    caminho = []
    atual = t
    while atual is not None:
        caminho.append(atual)
        if atual == s:
            break
        atual = pred[atual]
    caminho.reverse()  # O caminho está em ordem reversa, então invertemos
    return caminho

def main():
    while True:
        file = input("Informe o caminho para o arquivo (0 para sair): ")
        if file == '0':
            break

        try:
            dados = leArquivo(file)
            grafo = criaGrafoDeDisciplinas(dados)
            
            print(grafo)
            
            print("\nArestas do grafo com peso (duração):")
            for u, v, data in grafo.edges(data=True):  # Acessa o dicionário 'data' das arestas
                print(f"Aresta de {u} para {v}, peso: {data['peso']}")   
                
            print("Nós no grafo:", grafo.nodes())          
            
            pred = calcularCaminhoMaximoBellmanFord(grafo, s = "s")
            
            caminho = reconstruirCaminho(pred,s = "s",t = "t")
            print("Caminho encontrado")
            print(caminho)
            
        except FileNotFoundError:
            print("Arquivo não encontrado. Tente novamente.")

if __name__ == "__main__":  
    main()
