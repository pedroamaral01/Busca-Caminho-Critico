import csv
import networkx as nx
import matplotlib.pyplot as plt

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
    nomesDisciplinas = {}
       
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
        nomesDisciplinas[codigo] = nome
        
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

    return G, nomesDisciplinas

def calcularCaminhoMaximoBellmanFord(G, s):
    # Inicializa distâncias e predecessores
    dist = {v: float('-inf') for v in G.nodes}
    pred = {v: None for v in G.nodes}
    dist[s] = 0
    
    for _ in range(len(G.nodes) - 1):      
        for u, v in G.edges:
            if dist[v] < dist[u] + G.edges[u, v]['peso']:
                dist[v] = dist[u] + G.edges[u, v]['peso']
                pred[v] = u
        
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

def desenharGrafo(G, nomesDisciplinas, caminho:None):
    pos = nx.spring_layout(G, seed=42)  # Layout padrão para outros nós
    pos["s"] = [-1, 0]  # Posiciona 's' na esquerda
    pos["t"] = [1, 0]   # Posiciona 't' na direita
    
    # Cria listas de nós e arestas para colorir
    node_colors = ['lightblue'] * len(G.nodes)
    edge_colors = ['gray'] * len(G.edges)
    
    if caminho:
        # Destaca os nós do caminho
        for node in caminho:
            if node in G.nodes:
                node_colors[list(G.nodes).index(node)] = 'lightgreen'
        
        # Destaca as arestas do caminho
        caminho_edges = list(zip(caminho[:-1], caminho[1:]))
        for edge in caminho_edges:
            if edge in G.edges or (edge[1], edge[0]) in G.edges:
                edge_colors[list(G.edges).index(edge)] = 'red'
    
    plt.figure(figsize=(10, 6))  # Ajusta o tamanho da figura
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold', edge_color=edge_colors)
    
     # Adiciona texto ao gráfico
    if caminho:
        caminho_nomes = [nomesDisciplinas.get(node, node) for node in caminho if node not in ("s", "t")]
        caminho_texto = "Caminho Crítico:\n" + "\n".join(caminho_nomes)
        tempo_minimo = len(caminho_nomes)
        texto = f"{caminho_texto}\n\nTempo Mínimo: {tempo_minimo}"
        plt.text(-1.2, -0.8, texto, ha='left', va='bottom', fontsize=12, bbox=dict(facecolor='white', alpha=0.8), zorder=10)
    
    plt.title("Grafo de Disciplinas")
    plt.show()

def main():
    while True:
        file = input("Informe o caminho para o arquivo (0 para sair): ")
        if file == '0':
            break

        try:
            dados = leArquivo(file)
            grafo, nomesDisciplinas = criaGrafoDeDisciplinas(dados)
            
            
            print("\nArestas do grafo com peso (duração):")
            for u, v, data in grafo.edges(data=True):  # Acessa o dicionário 'data' das arestas
                print(f"Aresta de {u} para {v}, peso: {data['peso']}")   
                        
            pred = calcularCaminhoMaximoBellmanFord(grafo, s = "s")
            
            caminho = reconstruirCaminho(pred,s = "s",t = "t")
            
            # Convertendo códigos para nomes das disciplinas
            caminho_nomes = [nomesDisciplinas.get(node, node) for node in caminho if node not in ("s", "t")]
                
            print("\nCaminho Crítico:")
            for nome in caminho_nomes:
                print(nome)
            
            print("\nTempo Mínimo: ", len(caminho_nomes))
            
            # Desenhar o grafo com o caminho destacado
            desenharGrafo(grafo, nomesDisciplinas,caminho)
            
        except FileNotFoundError:
            print("Arquivo não encontrado. Tente novamente.")

if __name__ == "__main__":  
    main()
