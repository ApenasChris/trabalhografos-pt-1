import json
from typing import List, Dict

# Definindo tipo do dado
class Movie:
    def __init__(self, id: int, title: str, cast: List[str]):
        self.id = id
        self.title = title
        self.cast = cast

# Função para carregar os dados do arquivo JSON
def load_data(file_path: str) -> List[Dict]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Grafo - Dados Relação
def build_graph(data: List[Dict]) -> dict:
    graph = {}
    for movie_data in data:
        movie = Movie(id=movie_data['id'], title=movie_data['title'], cast=movie_data['cast'])
        actors = movie.cast
        for i in range(len(actors)):
            for j in range(i+1, len(actors)):
                actor1 = actors[i]
                actor2 = actors[j]
                # Adicionando relação entre atores
                if actor1 not in graph:
                    graph[actor1] = []
                if actor2 not in graph:
                    graph[actor2] = []
                graph[actor1].append(actor2)
                graph[actor2].append(actor1)
    return graph

# Algoritmo BFS adaptado para encontrar caminhos mínimos até uma profundidade máxima
def bfs_max_depth(graph, start, max_depth):
    visited = set()
    queue = [(start, [])]

    while queue:
        node, path = queue.pop(0)
        visited.add(node)
        # Se a profundidade do caminho atual for maior que max_depth, ignora
        if len(path) > max_depth:
            continue
        if path:
            print(f"Caminho: {' -> '.join(path)}, Comprimento: {len(path)}")
        for adjacent in graph[node]:
            if adjacent not in visited:
                queue.append((adjacent, path + [adjacent]))

# Interface do usuário
def start_bfs(graph):
    source_actor = input("Digite o nome do ator de origem: ")
    destination_actor = input("Digite o nome do ator de destino: ")
    print(f"Buscando caminhos mínimos entre {source_actor} e {destination_actor} com comprimento máximo de 6...")
    bfs_max_depth(graph, source_actor, 6)

# Path até diretório do JSON
file_path = 'latest_movies.json'

# Carrega o JSON
data = load_data(file_path)

# Constructor do Grafo
graph = build_graph(data)

# Iniciar a busca BFS
start_bfs(graph)