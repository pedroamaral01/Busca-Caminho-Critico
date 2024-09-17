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
    
def criaGrafoDeDisciplinas(dados):
    G = nx.DiGraph() # Grafo direcionado
    
    # Adiciona os nós de s e t
    G.add_node("s")
    G.add_node("t")
    
    duracoes = {}
       
    for row in dados:
        codigo = row['Código']
        nome = row['Nome']
        periodo = int(row['Período'])
        duracao = int(row['Duração'])
        dependencias = row['Dependências'].split(',') if row['Dependências'] else []
        
        
        G.add_node(codigo, name=nome, periodo = periodo)
        duracoes[codigo] = duracao # armazena a duracao de cada curso
        
        has_dependencies = False
        
         # Adiciona arestas com base nas dependências
        for dep in dependencias:
            if dep.strip():  # Adiciona uma aresta apenas se a dependência não estiver vazia
                G.add_edge(dep, codigo, peso=duracoes[dep])
                has_dependencies = True
        
        # Se a tarefa não tiver dependências, conecta ao nó de s
        if not has_dependencies:
            G.add_edge("s", codigo, peso = 0)  
            
        G.add_edge(codigo,"t", peso = duracao) # conecta todos os nós a t   
                
    return G
            
def main():
    while True:
        file = input("Informe o caminho para o arquivo (0 para sair): ")
        if file == '0':
            break

        try:
            dados = leArquivo(file)
            grafo = criaGrafoDeDisciplinas(dados)
            
            print(grafo)
            print("\nNós do grafo:")
            for node in grafo.nodes(data=True):
                print(node)
            
            print("\nArestas do grafo com peso (duração):")
            for u, v, data in grafo.edges(data=True):  # Acessa o dicionário 'data' das arestas
                print(f"Aresta de {u} para {v}, peso: {data['peso']}")   
                
            print("Nós no grafo:", grafo.nodes())          

        except FileNotFoundError:
            print("Arquivo não encontrado. Tente novamente.")

if __name__ == "__main__":
    main()
