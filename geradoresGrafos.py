from ListaAdjacencias import  GrafoLista

def randomNonDirected(vertices, arestas):
    grafo = GrafoLista(False, False)
    for vertice in range(vertices):
        grafo.addVertice(vertice) #Popula o grafo. Números inteiros são os rótulos dos vértices
    import random
    arestasAdicionadas = 0 #Controla a adição de arestas
    while arestasAdicionadas <= arestas:
        # Sorteia dois inteiros dentre os rótulos do grafo
        origem = random.randint(0,vertices-1)
        destino = random.randint(0,vertices-1)
        #Se não existe uma aresta entre eles, adiciona a aresta e atualiza o contador de arestas.
        if not grafo.isAresta(origem, destino):
            grafo.addAresta(origem, destino)
            arestasAdicionadas += 1
    return grafo

def randomErdosRenyi(vertices, p):
    grafo = GrafoLista(False, False)
    for vertice in range(vertices):
        grafo.addVertice(vertice) #Popula o grafo. Números inteiros são os rótulos dos vértices
    import random
    for verticeOrigem in range(vertices): #Itera por todas as possíveis origens
        for verticeDestino in range(vertices): #Itera por todos os possíveis destinos
            if verticeOrigem!=verticeDestino: #Se a origem é diferente do destino
                a = random.random() #gera um numero real entre 0 e 1
                if a< p: #se é menor que a probabilidade parâmetro, adiciona a aresta
                    grafo.addAresta(verticeOrigem, verticeDestino)
    return grafo
