import json
from typing import List, Dict
import tkinter as tk
from tkinter import filedialog, messagebox

# Definição da classe Movie para representar os dados de um filme
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

# Função para construir o grafo de relacionamentos entre atores
def build_graph(data: List[Dict]) -> dict:
    graph = {}
    for movie_data in data:
        movie = Movie(id=movie_data['id'], title=movie_data['title'], cast=movie_data['cast'])
        actors = movie.cast
        for i in range(len(actors)):
            for j in range(i+1, len(actors)):
                actor1 = actors[i]
                actor2 = actors[j]
                # Adiciona relação entre atores
                if actor1 not in graph:
                    graph[actor1] = []
                if actor2 not in graph:
                    graph[actor2] = []
                graph[actor1].append(actor2)
                graph[actor2].append(actor1)
    return graph

# Algoritmo BFS para encontrar um dos caminhos menores entre dois atores relacionados
def bfs_shortest_path(graph, start, end):
    visited = set()
    queue = [(start, [])]

    while queue:
        node, path = queue.pop(0)
        if node == end:
            return path + [node]  # Retorna o caminho encontrado
        visited.add(node)
        for adjacent in graph[node]:
            if adjacent not in visited:
                queue.append((adjacent, path + [node]))  # Adiciona o nó atual ao caminho
    return None  # Retorna None se não houver caminho encontrado

# Função para exibir o resultado
def show_result():
    source_actor = source_entry.get()
    destination_actor = destination_entry.get()
    shortest_path = bfs_shortest_path(graph, source_actor, destination_actor)
    if shortest_path:
        result_label.config(text=f"Um dos caminhos mais curtos entre {source_actor} e {destination_actor}: {' -> '.join(shortest_path)}")
    else:
        result_label.config(text=f"Não há um relacionamento entre {source_actor} e {destination_actor}.")

    # Contagem de caminhos possíveis com comprimento máximo de 6
    possible_paths = 0
    visited = set()
    queue = [(source_actor, [])]

    while queue:
        node, path = queue.pop(0)
        visited.add(node)
        if len(path) <= 6:
            if node == destination_actor:
                possible_paths += 1
            for adjacent in graph[node]:
                if adjacent not in visited:
                    queue.append((adjacent, path + [node]))

    result_label2.config(text=f"Quantidade de caminhos possíveis com comprimento máximo de 6: {possible_paths}")

# Função para selecionar o arquivo JSON
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            data = load_data(file_path)
            global graph
            graph = build_graph(data)
            messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")

# Cria a janela principal
root = tk.Tk()
root.title("6 Graus de Network")

# Cria um frame para o menu
menu_frame = tk.Frame(root)
menu_frame.pack(pady=10)

# Botão para selecionar o arquivo JSON
select_button = tk.Button(menu_frame, text="Selecionar Arquivo", command=select_file)
select_button.grid(row=0, column=0, padx=10)

# Entrada para o nome do ator de origem
source_label = tk.Label(menu_frame, text="Ator de Origem:")
source_label.grid(row=0, column=1)
source_entry = tk.Entry(menu_frame)
source_entry.grid(row=0, column=2)

# Entrada para o nome do ator de destino
destination_label = tk.Label(menu_frame, text="Ator de Destino:")
destination_label.grid(row=0, column=3)
destination_entry = tk.Entry(menu_frame)
destination_entry.grid(row=0, column=4)

# Botão para exibir o resultado
result_button = tk.Button(menu_frame, text="Exibir Resultado", command=show_result)
result_button.grid(row=0, column=5, padx=10)

# Frame para exibir o resultado
result_frame = tk.Frame(root)
result_frame.pack(pady=10)

# Label para exibir o resultado
result_label = tk.Label(result_frame, text="")
result_label.pack()
result_label2 = tk.Label(result_frame, text="")
result_label2.pack()

# Executa o loop da aplicação
root.mainloop()
