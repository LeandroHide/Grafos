from queue import Queue 

class Grafos:
    def __init__(self):
        self.vertices = []
        self.arestas = []
        self.pesos = []
        self.vetorArestas = []

    def qtdVertices(self):
        return len(self.vertices)

    def qtdArestas(self):
        somatorio = 0
        for i in range(1, len(self.arestas)):
            somatorio += len(self.arestas[i])
        return somatorio

    def grau(self, v):
        return len(self.arestas[v])

    def rotulo(self, v):
        return self.vertices[v-1][1]

    def haAresta(self, u, v):
        if self.pesos[u][v] == 0:
            return False
        else:
            return True

    def peso(self, u, v):
        return self.pesos[u][v]
    
    def ler(self, arquivo):
        f = open(arquivo, "r")
        contador = 0
        block = 0
        edgesArcs = 0
        listaVertices = []
        listaArestas = []
        matrizPesos = []
        listaArestasParaCiclos = []

        for x in f:
            if x[0] == "*":
                contador += 1
                if x[1] == "e":
                    edgesArcs = 1
                else:
                    edgesArcs = 2
                if block == 0:
                    v = int(x[10:])+1
                    for _ in range(v):
                        listaArestas.append([])
                    matrizPesos = [[float('inf') for x in range(v)] for y in range(v)] 
                    block = 1
            if contador == 1 and x[0] != "*":
                listaVertices.append(x.split())
            if contador == 2 and x[0] != "*" and edgesArcs == 1:
                temp = x.split()
                listaArestas[int(temp[0])].append(int(temp[1]))
                listaArestas[int(temp[1])].append(int(temp[0]))
                listaArestasParaCiclos.append([int(temp[0])] + [int(temp[1])])

                matrizPesos[int(temp[0])][int(temp[1])] = temp[2]
                matrizPesos[int(temp[1])][int(temp[0])] = temp[2]
            if contador == 2 and x[0] != "*" and edgesArcs == 2:
                temp = x.split()
                listaArestas[int(temp[0])].append(int(temp[1]))
                matrizPesos[int(temp[0])][int(temp[1])] = temp[2]

        self.vertices = listaVertices
        self.arestas = listaArestas
        self.pesos = matrizPesos
        self.vetorArestas = listaArestasParaCiclos


    def buscaLargura(self, s):
        c = []
        d = []
        a = []
        for _ in range(len(self.vertices)+1):
            c.append(False)
            d.append(float('inf'))
            a.append(None)
        c[s] = True
        d[s] = 0

        q = Queue()
        q.put(s)
        while q.empty() == False:
            u = q.get()
            for v in self.arestas[u]:
                if c[v] == False:
                    c[v] = True
                    d[v] = d[u] + 1
                    a[v] = u
                    q.put(v)

        niveis = []
        for _ in range(max(d[1:])+1):
            niveis.append([])
        cont = 0
        for i in d[1:]:
            cont += 1
            niveis[i].append(cont)
        cont1 = 0
        for j in niveis:
            print(str(cont1) + ": ", end = "")
            print (*j, sep = ",")
            cont1 += 1
        return [d[1:],a[1:]]


    def ciclosEulerianos(self):
        c = dict()
        for x in range(len(self.arestas)):
            for e in self.arestas[x]:
                c[x,e] = False
        
        v = int(self.vertices[0][0])

        result = self.buscarSubcicloEuleriano(self.vertices, self.arestas, v, c)

        if result[0] == False:
            print(0)
        else:
            for x in range(len(self.arestas)):
                for e in self.arestas[x]:
                    if c[x,e] == False:
                        print(0)
                        return
            print(1)
            print (*result[1], sep = ",")



    def buscarSubcicloEuleriano(self, vertices, arestas, v, c):
        ciclo = [v]
        t = v

        while True:
            continua = 0
            for u in arestas[v]:
                if c[u,v] == False:
                    c[u,v] = True
                    c[v,u] = True
                    v = u
                    ciclo.append(v)
                    continua = 1
                    break

            if continua == 0:
                return (False, None)

            if v == t:
                break

        for x in ciclo:
            for e in arestas[x]:
                if c[x,e] == False:
                    result = self.buscarSubcicloEuleriano(vertices, arestas, x, c)
                    
                    if result[0] == False:
                        return (False, None)

                    ciclo = ciclo[:ciclo.index(x)] + result[1] + ciclo[ciclo.index(x)+1:]
                    
        return (True, ciclo)

                    

            

grafo = Grafos()
grafo.ler("C:\\Programmer\\Python\\Grafos\\pequenas\\karate.net")
grafo.buscaLargura(8)

    