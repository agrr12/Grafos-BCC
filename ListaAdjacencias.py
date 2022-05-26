class GrafoLista:
    def __init__(self, direcionado, ponderado):
        self.lista ={}
        self.direcionado = direcionado
        self.ponderado = ponderado

    def isVertice(self, rotulo):
        return rotulo in self.lista.keys()

    def isAresta(self,origem, destino):
        if self.isVertice(origem) and self.isVertice(destino):
            return destino in self.lista.get(origem).keys()
        else:
            print("Os rótulos passados não existem no grafo.")

    def addVertice(self, rotulo):
        if not self.isVertice(rotulo):
            self.lista[rotulo]={}

    def addAresta(self, origem, destino, peso=1):
        if self.isVertice(origem) and self.isVertice(destino):
            if self.direcionado and self.ponderado:
                self.lista.get(origem)[destino]=peso #também substitui aresta
            elif not(self.direcionado) and self.ponderado:
                self.lista.get(origem)[destino] = peso  # também substitui aresta
                self.lista.get(destino)[origem] = peso  # também substitui aresta
            elif self.direcionado and not(self.ponderado):
                self.lista.get(origem)[destino] = 1  # também substitui aresta
            else:
                self.lista.get(origem)[destino] = 1  # também substitui aresta
                self.lista.get(destino)[origem] = 1  # também substitui aresta
        else:
            print("Os rótulos passados não existem no grafo.")

    def removerAresta(self, origem, destino):
        if self.isVertice(origem) and self.isVertice(destino) and self.isAresta(origem, destino):
            if self.direcionado:
                self.lista.get(origem).pop(destino)
            else:
                self.lista.get(origem).pop(destino)
                self.lista.get(destino).pop(origem)
        else:
            print("Parâmetros errados.")

    def removerVertice(self, rotulo):
        if self.isVertice(rotulo):
            self.lista.pop(rotulo)
            for vertice in self.lista.keys():
                self.lista.get(vertice).pop(rotulo, None)
        else:
            print("Parâmetro incorreto.")

    def imprimeLista(self):
        for x in self.lista.keys():
            print("Vértice:",x, end=" - Arestas: ")
            for y in self.lista.get(x).keys():
                if self.ponderado:
                    print(y,"-", self.lista.get(x).get(y), end =" | ")
                else:
                    print(y, end=" | ") #Se não for ponderado, não imprime arestas
            print("")

    def grauEntrada(self, rotulo):
        if self.isVertice(rotulo):
            grauEntrada = 0
            for vertice in self.lista.keys():
                if rotulo in self.lista.get(vertice).keys():
                    grauEntrada +=1
            return grauEntrada

    def grauSaida(self, rotulo):
        if self.isVertice(rotulo):
            return len(self.lista.get(rotulo).keys())

    def grau(self, rotulo):
        if self.isVertice(rotulo):
            return self.grauEntrada(rotulo) + self.grauSaida(rotulo)

    def ordem(self):
        return len(self.lista)

    def retornaAdjacentes(self, rotulo):
        if self.isVertice(rotulo):
            adj = []
            for vertice in self.lista.get(rotulo).keys():
                adj.append(vertice)
            return adj

    def DFS(self,v,u):
        pilha = []
        pilha.append(v)
        visitados = []
        while pilha!=[]:
            n = pilha.pop()
            if n not in visitados: visitados.append(n)
            if(n==u): return visitados
            adj = self.retornaAdjacentes(n)
            for vertice in adj:
                if vertice not in visitados:
                    pilha.append(vertice)
        return visitados

    def BFS(self, v, u):
        fila = []
        fila.append(v)
        visitados = []
        while len(fila)>0:
            n = fila.pop(0)
            if n not in visitados: visitados.append(n)
            if(n==u): return visitados
            adj = self.retornaAdjacentes(n)
            for vertice in adj:
                if vertice not in visitados:
                    fila.append(vertice)
        return visitados

    def Dijkstra(self, origem, alvo):
        import numpy as np
        if (self.isVertice(origem)) and (self.isVertice(alvo)):
            visitados = []
            ListaCustoAnterior = {}
            visitaveis = []
            for vertice in self.lista.keys():
                if (self.grauSaida(vertice) == 0 or self.grauEntrada(vertice) == 0) and vertice != alvo and vertice != origem:
                    continue
                elif vertice == origem:
                    ListaCustoAnterior[vertice] = [vertice, 0]
                    visitaveis.append(vertice)
                else:
                    ListaCustoAnterior[vertice] = [vertice, np.inf]
                    visitaveis.append(vertice)
            nodeAtual = origem
            while len(visitados) < len(visitaveis):
                # Obtém os nós adjacentes do nó atual
                adjacent_nodes = self.retornaAdjacentes(nodeAtual)
                # Itera por cada nó adjacente
                for adj in adjacent_nodes:
                    if adj in visitaveis and adj not in visitados:
                        # Caso o nó ainda não tenha sido visitado, verifica o caminho
                        # if adj not in visitados:
                        # Obtém o peso da distância do nó de origem até o nó adjacente
                        acc_cost = ListaCustoAnterior.get(nodeAtual)[1] + self.lista.get(nodeAtual).get(adj)
                        # Se o peso é menor que o peso nele registrado, registra o novo peso e o nó de origem
                        if ListaCustoAnterior.get(adj)[1] > acc_cost:
                            ListaCustoAnterior.get(adj)[1] = acc_cost
                            ListaCustoAnterior.get(adj)[0] = nodeAtual
                # Iteração concluída, adiciona o Nó à lista de visitados
                visitados.append(nodeAtual)
                # Separação dos nós visitados dos não visitados
                non_visted = [item for item in visitaveis if item not in visitados]
                if non_visted != []:
                    # Busca pelo nó não visitado com o menor peso acumulado
                    nodeAtual = non_visted[0]
                    for vertice in non_visted:
                        if ListaCustoAnterior.get(vertice)[1] < ListaCustoAnterior.get(nodeAtual)[1]:
                            nodeAtual = vertice
            # Processo para encontrar o caminho
            print(ListaCustoAnterior)
            caminho = [alvo]
            custo = ListaCustoAnterior.get(alvo)[1]
            contador = 0
            # Busca inicia a partir do destino, e vai retornando pelos caminhos mais leves até a origem
            passo = ListaCustoAnterior.get(alvo)[0]
            while contador < len(visitaveis):
                caminho.insert(0, passo)
                if passo == origem:
                    return caminho, custo
                passo = ListaCustoAnterior.get(passo)[0]
                contador += 1

        else:
            print("Parâmetros incorretos")

    #Lógica Utilizada:
    #1. Se há um Ciclo, há um caminho que começa em um vértice X e retorna ao vértice X
    #2. Se não há um ciclo em um caminhos que começam em X, só é possível haver ciclos em caminhos que começam em nós em níveis mais altos que X
    #3. Se não há ciclo em um caminho X, não haverá ciclos em nenhum sub-caminho do caminho X
    def isCyclic(self):
        visitadosSemCiclo = [] #Otimização. Armazena os vértices que apareceram em caminhos sem ciclo para não serem reexaminados
        for verticeOrigem in self.lista.keys():
            if verticeOrigem in visitadosSemCiclo: #Se o nó já esteve em um caminho sem ciclo, não precisa ser analisado
                continue
            #Verifica se há nós em todos os caminhos a partir do nó analisado
            else:
                nivelAnterior = [] #Lista para uso no caso de grafos não-direcionados, registra o nível anterior ao que está sendo processado
                nivel = [verticeOrigem]  # Nível zero inicia na origem
                visitados = []
                while nivel!=[]: #Enquanto não alcança um nível vazio, há caminhos a serem explorados
                    novoNivel = []  # Array que vai reunir todos os vértices que compõem o próximo nível
                    for vertice in nivel:
                        visitados.append(vertice)
                        adjacentes = self.retornaAdjacentes(vertice)  # Os adjacentes do vértice compõem, com os dos outros, o próximo nível
                        for verticeAdjacente in adjacentes:
                            if self.direcionado==False: #Caso o grafo não seja direcionado
                                #Controla a conexão recíproca do adjacente com a origem
                                if verticeAdjacente not in nivelAnterior and verticeAdjacente in visitados:
                                    return True
                            else:
                                if verticeAdjacente in visitados: #Se algum dos vértices adjacentes estiver nos visitados, então há um ciclo
                                    return True
                        #Monta o novo nível. Se o código chegou até aqui, ainda não foi encontrado um ciclo, e só vértices novos comporão o novo nível
                        for elemento in adjacentes:
                            #Caso o grafo seja direcionado
                            if self.direcionado == False:
                                #Elimina do próximo nível as conexões recíprocas entre adjacente e origem
                                if elemento not in nivelAnterior:
                                    novoNivel.append(elemento)
                            else:
                                novoNivel.append(elemento)
                        nivelAnterior = []
                        for verticeAntigo in nivel:
                            nivelAnterior.append(verticeAntigo)
                        nivel = novoNivel
            #Se o código chegou até aqui, todos os caminhos partindo da origem não incluem ciclos
            #Adiciona todos os vértices encontrados à lista de vértices que não precisam mais ser examinados
            for vertice in visitados:
                visitadosSemCiclo.append(vertice)
        return False


    def topologicalSortKahn(self):
        listaOrdenada = []
        while self.ordem()>0: #Loop principal para esvaziar o grafo e montar a lista ordenada
            for vertice in self.lista.keys(): #Encontra vértice com grau de saída 0
                if self.grauEntrada(vertice)==0:
                    listaOrdenada.append(vertice) #adiciona na lista
                    self.removerVertice(vertice) #remove o vértice do grafo
                    break
        return listaOrdenada

    def topologicalSortTarjan(self):
        pilhaDFS = []
        pilhaTS = []
        visitados = []
        #Itera pelos vértices do grafo, realizando DFS a partir daqueles que ainda não foram visitados
        for verticeInicial in self.lista.keys():
            if verticeInicial not in visitados:#Só analisa os que não foram visitados
                pilhaDFS.append(verticeInicial)
                while pilhaDFS!=[]:
                    n = pilhaDFS.pop() #Pega o primemiro da pilha
                    pilhaDFS.append(n) #Coloca de volta para garantir o backtrack
                    if n not in visitados: visitados.append(n) #Coloca na lista de visitados
                    adj = self.retornaAdjacentes(n) #Lista de adj
                    #Caso 1 - É uma folha
                    if adj==[]:
                        pilhaTS.append(n) #Coloca a folha na pilha ordenada topologicamente
                        pilhaDFS.pop() #Remove a folha da pilhaDFS, pois o algoritmo nunca voltará a aela
                    #Caso 2 - Não é uma folha
                    else:
                        todosVisitados = True #Tag para controlar se todos os filhos já foram percorridos
                        for vertice1 in adj: #Itera pelos filhos em busca de algum não visitado
                            if vertice1 not in visitados:
                                todosVisitados=False
                        if todosVisitados==True: #Se já visitou todos os filhos, nãp há mais backtrack a partir daqui
                            pilhaDFS.pop() #Remove do DFS
                            pilhaTS.append(n) #Adiciona à lista topológica ordenada
                    for vertice in adj:
                        if vertice not in visitados:
                            pilhaDFS.append(vertice)
        return pilhaTS[::-1] #Retorna a pilha montada ao contrário

    def numberOfComponents(self): #Só funciona para Grafos NÃO-direcionados
        visitados = [] #Armazena os nós que já foram visitados
        componentes = 0 #Conta o número de componentes
        pilhaDFS = [] #Pilha usada no DFS
        # Itera pelos vértices do grafo, realizando DFS a partir daqueles que ainda não foram visitados
        for verticeInicial in self.lista.keys():
            if verticeInicial not in visitados:  # Só analisa os que não foram visitados
                pilhaDFS.append(verticeInicial)
                while pilhaDFS != []: #DFS padrão
                    n = pilhaDFS.pop()  # Pega o primeiro da pilha
                    if n not in visitados: visitados.append(n)  # Coloca na lista de visitados
                    adj = self.retornaAdjacentes(n)  # Lista de adj
                    for vertice in adj:
                        if vertice not in visitados:
                            pilhaDFS.append(vertice)
                componentes+=1 #Se terminou o caminho, percorreu um componente inteiro

        return componentes

    #Algoritmo de Prim (Não funciona para grafos não conexos)
    def Prim(self):
        import random
        import numpy as np
        origem = random.choice([x for x in self.lista.keys()]) #Seleciona a raiz da árvore aleatoriamente
        #Parte 1 - Algoritmo de Dijkstra modificado
        visitados = []
        ListaCustoAnterior = {}
        for vertice in self.lista.keys():
            if vertice == origem:
                ListaCustoAnterior[vertice] = [vertice, 0]
            else:
                ListaCustoAnterior[vertice] = [vertice, np.inf]
        nodeAtual = origem
        while len(visitados) < self.ordem():
            # Obtém os nós adjacentes do nó atual
            adjacent_nodes = self.retornaAdjacentes(nodeAtual)
            # Itera por cada nó adjacente
            for adj in adjacent_nodes:
                if adj not in visitados: # Caso o nó ainda não tenha sido visitado, verifica o caminho
                    custo = self.lista.get(nodeAtual).get(adj) #DIFERENÇA - Custo NÃO é o custo acumulado
                    if ListaCustoAnterior.get(adj)[1] > custo: # Se o peso é menor que o peso nele registrado, registra o novo peso e o nó de origem
                        ListaCustoAnterior.get(adj)[1] = custo
                        ListaCustoAnterior.get(adj)[0] = nodeAtual
            visitados.append(nodeAtual) # Iteração concluída, adiciona o Nó à lista de visitados
            non_visted = [item for item in self.lista.keys() if item not in visitados] # Separação dos nós visitados dos não visitados
            if non_visted != []:
                # Busca pelo nó não visitado com o menor peso acumulado
                nodeAtual = non_visted[0]
                for vertice in non_visted:
                    if ListaCustoAnterior.get(vertice)[1] < ListaCustoAnterior.get(nodeAtual)[1]:
                        nodeAtual = vertice
        #Parte 2 - Construção da árvore do Algoritmo de Prim
        arvorePrim = GrafoLista(self.direcionado,self.ponderado) #Instancia a árvore como um grafo
        for vertice1 in self.lista.keys(): #Popula a árvore com todos os vértices
            arvorePrim.addVertice(vertice1)
        for vertice2 in self.lista.keys(): #Conecta todos os vértices com as menores arestas encontradas
            if vertice2==origem: #Se a raiz é encontrada, pula-se. Por ser raiz, seu grau de entrada é sempre zero.
                continue
            else: #Se não é a raiz, insere a aresta especificada pelo Algoritmo de Dijkstra
                verticeOrigem = ListaCustoAnterior.get(vertice2)[0]
                arestaMenorPeso = ListaCustoAnterior.get(vertice2)[1]
                arvorePrim.addAresta(vertice2,verticeOrigem,arestaMenorPeso)
        return arvorePrim

    def Kruskal(self):
        #1 - Criação e população da árvore
        arvoreKruskal = GrafoLista(self.direcionado, self.ponderado)
        for vertice in self.lista.keys():
            arvoreKruskal.addVertice(vertice)
        #2 - Montagem e ordenação de uma lista com todas as arestas
        listaArestas = [] #lista com cada aresta no grafo
        for verticeOrigem in self.lista.keys():
            for verticeDestino in self.lista.get(verticeOrigem).keys():
                peso = self.lista.get(verticeOrigem).get(verticeDestino)
                listaArestas.append([verticeOrigem, verticeDestino, peso])
        listaArestas.sort(key = lambda x: x[2]) #Ordena a lista de arestas do menor pro maior
        #3 - Inclusão e testagem das arestas
        arestasAdicionadas=0 #controla a quantidade de arestas adicionadas
        arestasIndex = 0 #controla a iteração por listaArestas
        while arestasAdicionadas<self.ordem()-1:
            #print(listaArestas)
            aresta = listaArestas[arestasIndex] #Recupera a aresta da lista ordenada
            #Caso 1 - Grafo Direcionado
            if self.direcionado:
                arvoreKruskal.addAresta(aresta[0], aresta[1], aresta[2])
                # Caso 1.1 - A aresta cria um ciclo e, por isso, é removida
                if (arvoreKruskal.isCyclic()):
                    arvoreKruskal.removerAresta(aresta[0], aresta[1])
                # Caso 1.2 - A aresta não cria um ciclo
                else:
                    arestasAdicionadas += 1
            #Caso 2 - Grafo Não-Direcionado
            else:
                #Adiciona só se a aresta ainda não existe (evita a repetição nos grafos não-direcionados)
                if not arvoreKruskal.isAresta(aresta[0], aresta[1]):
                    arvoreKruskal.addAresta(aresta[0], aresta[1], aresta[2]) #Adiciona a aresta
                    #Caso 1 - A aresta cria um ciclo e, por isso, é removida
                    if(arvoreKruskal.isCyclic()):
                        arvoreKruskal.removerAresta(aresta[0],aresta[1])
                    #Caso 2 - A aresta não cria um ciclo
                    else:
                        arestasAdicionadas+=1
            arestasIndex+=1 #Avança para a próxima aresta
        return arvoreKruskal


if __name__ == '__main__':
    #Teste 1 - Grafo K5
    gPentagrama = GrafoLista(False, True)
    for letra in "ABCDE": gPentagrama.addVertice(letra) #popula o grafo
    gPentagrama.addAresta("A", "B", 1)
    gPentagrama.addAresta("A", "C", 2)
    gPentagrama.addAresta("A", "D", 3)
    gPentagrama.addAresta("A", "E", 4)
    gPentagrama.addAresta("B", "C", 5)
    gPentagrama.addAresta("B", "D", 6)
    gPentagrama.addAresta("B", "E", 7)
    gPentagrama.addAresta("C", "D", 8)
    gPentagrama.addAresta("C", "E", 9)
    gPentagrama.addAresta("D", "E", 10)
    print("Árvore por Kruskal: ", end="")
    print(gPentagrama.Kruskal().lista)
    print("Árvore por Prim: ", end="")
    print(gPentagrama.Prim().lista)

    #Teste2 -Grafo do Slide18, Aula 11
    g18 = GrafoLista(False, True)
    for letra in "ABCDEFGHI": g18.addVertice(letra)  # popula o grafo
    g18.addAresta("A", "B", 10)
    g18.addAresta("A", "C", 12)
    g18.addAresta("B", "C", 9)
    g18.addAresta("B", "D", 8)
    g18.addAresta("C", "F", 1)
    g18.addAresta("C", "E", 3)
    g18.addAresta("D", "E", 7)
    g18.addAresta("D", "H", 5)
    g18.addAresta("D", "G", 8)
    g18.addAresta("E", "F", 3)
    g18.addAresta("F", "H", 6)
    g18.addAresta("G", "H", 9)
    g18.addAresta("G", "I", 2)
    g18.addAresta("H", "I", 11)
    print("Árvore por Kruskal: ", end="")
    print(g18.Kruskal().lista)
    print("Árvore por Prim: ", end="")
    print(g18.Prim().lista)

    #Teste3 - Grafo Triângulo
    gTriangulo = GrafoLista(True, True)
    for letra in "ABC": gTriangulo.addVertice(letra)  # popula o grafo
    gTriangulo.addAresta("A", "B", 1)
    gTriangulo.addAresta("B", "C", 2)
    gTriangulo.addAresta("C", "A", 3)
    print("Árvore por Kruskal: ", end="")
    print(gTriangulo.Kruskal().lista)
    print("Árvore por Prim: ", end="")
    print(gTriangulo.Prim().lista)


