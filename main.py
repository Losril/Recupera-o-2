#HELENA KUCHINSKI FERREIRA
#1. A E B

import random
import string

'----------------GRAFO----------------'  
# classe de vértice
class Vertex:
  def __init__(self, node):
    # atributo de valor do vértice
    self.id = node
    # dicionário de vértices adjacentes a este
    self.adjacent = {}
    self.currCost = 0

  def __str__(self):
    my_str = ""
    for i in self.adjacent:
      my_str += "[" + str(i.id) + "] -> "
    return my_str

  def add_neighbor(self, neighbor, weight=0):
    self.adjacent[neighbor] = weight

  def get_connections(self):
    return self.adjacent.keys()  

  def get_id(self):
    return self.id

  def get_weight(self, neighbor):
    return self.adjacent[neighbor]

  def does_it_point_to(self, dest):
    return dest in self.adjacent

class Graph:
  def __init__(self, vertices):
    self.vertices = vertices
    self.vert_dict = {}
    self.num_vertices = 0

    # laço para iterar n vezes - input do usuário
    for i in range(vertices):
      # gera string aleatória
      str = self.gen_random_string()
      # condicional para saber se o grafo não possui a string gerada como vértice
      if self.get_vertex(str) is None:
        # caso não exista, adiciona novo vértice
        self.add_vertex(str)
        # declara randomicamente quantidade de areas a que o respectivo vértice deve possuir
        a = random.randint(1, 3)
        for i in range(a):
          x = self.get_vertex(str)
          # print(len(x.adjacent))
          if(len(x.adjacent) < 3):
            rand_vert = self.get_random_vertex()
            if(len(rand_vert[1].adjacent) < 3):
              # print("rand_vert:", rand_vert[0])
              p = random.randint(1, 10)
              self.add_edge(x.id, rand_vert[0], p)

  def __iter__(self):
    return iter(self.vert_dict.values())

  def add_vertex(self, node):
    # incrementa a variável que monitora a quantidade de vértices
    self.num_vertices = self.num_vertices + 1
    # cria nova classe com valor do parâmetro
    new_vertex = Vertex(node)
    self.vert_dict[node] = new_vertex
    return new_vertex

  def get_vertex(self, n):
    if n in self.vert_dict:
        return self.vert_dict[n]
    else:
        return None

  def add_edge(self, frm, to, cost = 0):
    if frm not in self.vert_dict:
        self.add_vertex(frm)
    if to not in self.vert_dict:
        self.add_vertex(to)

    self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
    self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

  def get_vertices(self):
    return self.vert_dict.keys()

  def get_random_vertex(self):
    return random.choice(list(self.vert_dict.items()))

  def gen_random_string(self):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters)  for i in range(random.randint(2, 2)))
    
    return result_str

  def print_graph(self):
    for i in self:
      print(i.get_id(), "[] ->", self.vert_dict[i.get_id()])

  def print_edge_values(self):
    for i in self:
      for w in i.get_connections():
        vid = i.get_id()
        wid = w.get_id()
        print('(',vid,',',wid,',', i.get_weight(w),')')

  def get_all_paths(self, start, end):
    return self.dfs(start, end, [], [], [])

  def dfs(self, currVertex, destVertex, visited, path, fullPath):
    # recebe objeto referente ao valor inicial do caminho
    vertex = self.vert_dict[currVertex]

    # adiciona a string do valor inicial na lista visited
    visited.append(currVertex)

    # adiciona atributo id do vértice na lista path
    path.append(vertex.id)

    # condicional para saber se o caminho destino é o próprio vértice
    if currVertex == destVertex:
      fullPath.append({"path": list(path), "cost": vertex.currCost})
    
    for i in vertex.get_connections():
      if i.id not in visited:
        self.vert_dict[i.id].currCost = vertex.get_weight(i) + vertex.currCost
        self.dfs(i.id, destVertex, visited, path, fullPath)
  
    path.pop()
    visited.pop()

    if not path:
      return fullPath

class Node:
  def __init__(self, data, cost):
    self.data = data
    self.next = None
    self.cost = cost
    
  def __repr__(self):
    return '%s -> %s' % (self.data, self.next)

  def get_data(self):
    return self.data

  def get_cost(self):
    return self.cost

'----------------LISTA LINKADA----------------'  
class LinkedList:
  def __init__(self):
    self.head = None
    self.size = 0

  def __repr__(self):
    return str(self.head)
  
  def insert(self, vertex, cost):
    node = Node(vertex, cost) 
    self.size += 1
    if self.head == None: 
      self.head = node
    else:
      temp = self.head
      
      while temp.next: 
          temp = temp.next 
      temp.next = node 

  def getNth(self, index):
    current = self.head  
    count = 0  
    
    while (current):
        if (count == index):
            return current
        count += 1
        current = current.next
    return 0

def floyd_warshall(g):
  distance = {v:dict.fromkeys(g, float('inf')) for v in g}
  next_v = {v:dict.fromkeys(g, None) for v in g}

  for v in g:
      for n in v.get_connections():
          distance[v][n] = v.get_weight(n)
          next_v[v][n] = n

  for v in g:
       distance[v][v] = 0
       next_v[v][v] = None

  for p in g: 
      for v in g:
          for w in g:
              if distance[v][w] > distance[v][p] + distance[p][w]:
                  distance[v][w] = distance[v][p] + distance[p][w]
                  next_v[v][w] = next_v[v][p]

  return distance, next_v
  
def print_path(next_v, u, v):
    p = u
    while (next_v[p][v]):
        print('{} -> '.format(p.get_id()), end='')
        p = next_v[p][v]
    print('{} '.format(v.get_id()), end='')

def serialize(g):
  l = []
  for i in g:
    adjlist = LinkedList()
    adjlist.insert(i.id, 0)
    for j in i.adjacent:
      adjlist.insert(j.id, i.get_weight(j))
    l.append(adjlist)
  return l

def deserialize(arr):
  # cria novo grafo vazio
  graph = Graph(0)
  
  # adiciona os vértices primeiro
  for i in arr:
    x = i.getNth(0).get_data()
    graph.add_vertex(x)

  for j in arr:
    x = j.getNth(0).get_data()
    for n in range(1, j.size):
      y = j.getNth(n).get_data()
      graph.add_edge(x, y, j.getNth(n).get_cost())
  
  return graph

'----------------MAIN----------------'  
if __name__ == "__main__":
  print('Informe o n° de Vertices:')
  x = int(input())

  print("\nLista de adjacências do seu grafo:")
  g = Graph(x)
  g.print_graph()
  
  print("\nCaminho entre dois vértices:")
  g.print_edge_values()
  vert = [i.get_id() for i in g]
  print(str([i.get_id() for i in g]) + "\n")
  print("Escolha o vértice inicial: ")
  a = input()
  while(a not in vert):
    print("Escolha o vértice inicial novamente: ")
    a = input()
  print("Escolha o vértice final: ")
  b = input()
  while(b not in vert):
    print("Escolha o vértice final novamente: ")
    b = input()
  print("\n")
  
  distance, next_v = floyd_warshall(g)
  print('Distância mais curta utilizando Floyd Warshall:')
  x = g.get_vertex(a)
  y = g.get_vertex(b)
  print('De {} até {}: '.format(x.get_id(), y.get_id()), end = '')
  print_path(next_v, x, y)
  print('(Distância {})'.format(distance[x][y]))
  
  print('\nTodos os caminhos:')
  res = g.get_all_paths(a, b)

  x = 1
  for i in res:
    print("Caminho", x, ": [", end='')
    for j in i["path"]:
      print(j, "-> ", end='')
    print("] Distância: ", i["cost"])
    x += 1

  print("\nGrafo serializado para um array de linked lists: ")
  serial = serialize(g)
  print(serial)

  print("\nGrafo deserializado: ")
  o = deserialize(serial)
  o.print_graph()
  o.print_edge_values()