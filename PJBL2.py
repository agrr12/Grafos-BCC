import random
import numpy as np
def randomNonDirected(vertices, arestas):
    grafo = GrafoLista(False, False)
    for vertice in range(vertices):
        grafo.addVertice(vertice) #Popula o grafo. Números inteiros são os rótulos dos vértices
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

def randomFreeScale(vertices, arestas):
    GrafoBase = randomNonDirected(10, 10)
    #Dicionário onde cada chave é um grau e cada valor é uma lista dos vértices com aquele grau
    listaGraus = {}
    #{0:[1,2,3} ; 1:["Luis","Bea","Andre"] ;

    #Preenche listaGraus com chaves de 1-10 com listas vazias
    for vertice in GrafoBase.lista.keys():
        listaGraus[vertice]=[]

    #Popula listaGrau alocando os vértices do Grafo a seus respectivos graus em listaGraus
    for verticeBase in GrafoBase.lista.keys():
        grau = GrafoBase.grau(verticeBase)
        if grau in listaGraus.keys():
            listaGraus.get(grau).append(verticeBase)
        else:
            listaGraus[grau]=[verticeBase]

    verticesNoGrafo = 10
    arestasNoGrafo = 10
    while(verticesNoGrafo<vertices and arestasNoGrafo<arestas):
        novoVerticeRotulo = verticesNoGrafo #começa em 10
        probDistribuicao = np.linspace(0.1, 1, len(listaGraus)) # Distribuição de probabalidades
        #probDistribuicao = np.power(probDistribuicaoBase, 5)


        verticeSorteado = random.choice(list(GrafoBase.lista.keys())) #2 (1)
        grauVerticeSorteado = GrafoBase.grau(verticeSorteado)
        sorteio = random.uniform(0.01,1.2)
        if sorteio < probDistribuicao[grauVerticeSorteado]:
            GrafoBase.addVertice(novoVerticeRotulo)  # Adiciona o novo vértice
            GrafoBase.addAresta(novoVerticeRotulo, verticeSorteado)  # Conecta com o vértice do Grafo
            listaGraus.get(1).append(novoVerticeRotulo)  # Adiciona o novo vértice à lista de graus 1
            # Atualiza a posição do vértice que recebeu a conexão na lista de graus
            listaGraus.get(grauVerticeSorteado).remove(verticeSorteado)  # Remove ele da lista em que estava
            if grauVerticeSorteado + 1 in listaGraus.keys():  # Se não existe uma lista equivalente ao seu novo grau, cria uma
                listaGraus.get(grauVerticeSorteado + 1).append(verticeSorteado)
            else:
                listaGraus[grauVerticeSorteado + 1] = [verticeSorteado]
            verticesNoGrafo+=1
            arestasNoGrafo+=1

    #Caso sejam inseridos mais vértices que arestas, insere os vértices remanescentes
    if(verticesNoGrafo<vertices):
        for number in range(verticesNoGrafo,vertices):
            GrafoBase.addVertice(number)

    #Caso sejam inseridas mais arestas que vértices, insere as arestas remanescentes
    if(arestasNoGrafo<arestas):
        while arestasNoGrafo<arestas:
            probDistribuicao = np.linspace(0.1, 1, len(listaGraus))  # Distribuição de probabalidades
            #probDistribuicao = np.power(probDistribuicaoBase, 5)
            #Sorteia dois vértices
            vertice1= random.choice(list(GrafoBase.lista.keys()))
            vertice2= random.choice(list(GrafoBase.lista.keys()))
            #Se os vértices são iguais, ou já existe uma aresta entre eles, refaz o sorteio de vértices
            if vertice1==vertice2 or GrafoBase.isAresta(vertice1, vertice2):
                continue
            #Sorteia um número aleatório
            sorteio= random.uniform(0.01,1.2)
            #Obtém os graus dos vértices
            grauVertice1= GrafoBase.grau(vertice1)
            grauVertice2= GrafoBase.grau(vertice2)
            #Simula a probabilidade de criação de aresta relacionada ao grau do vértice
            if sorteio>probDistribuicao[grauVertice1] or sorteio>probDistribuicao[grauVertice2]:
                continue

            #Atualiza ListaGraus para o Vértice 1
            listaGraus.get(grauVertice1).remove(vertice1)  # Remove ele da lista em que estava
            if grauVertice1 + 1 in listaGraus.keys():  # Se não existe uma lista equivalente ao seu novo grau, cria uma
                listaGraus.get(grauVertice1 + 1).append(vertice1)
            else:
                listaGraus[grauVertice1 + 1] = [vertice1]

            #Atualiza ListaGraus para o Vértice 2
            listaGraus.get(grauVertice2).remove(vertice2)  # Remove ele da lista em que estava
            if grauVertice2 + 1 in listaGraus.keys():  # Se não existe uma lista equivalente ao seu novo grau, cria uma
                listaGraus.get(grauVertice2 + 1).append(vertice2)
            else:
                listaGraus[grauVertice2 + 1] = [vertice2]
            GrafoBase.addAresta(vertice1, vertice2)  # Conecta com o vértice do Grafo
            arestasNoGrafo+=1


    return GrafoBase

def pajekIntoGrafo(arquivo):
    f = open(arquivo, "r")
    linhas = f.readlines() #Cria Array com as linhas do arquivo
    f.close()


    rotulos = [] #Lista que armazena todos os rótulos
    nrVertices = int(linhas[0].split(" ")[1]) #['*vertices', '8']
    linhaAtual = 1 #Registra a linha que está sendo processada no momento

    G = GrafoLista(False, False)
    #Itera pelos vértices
    while linhaAtual< nrVertices+1:
        primeiraAspaIndex = linhas[linhaAtual].index('"') #Usa a primeira aspa pra determinar o início do rótulo do vértice
        rotulo = linhas[linhaAtual][primeiraAspaIndex::].replace('"', "").replace("\n", "") #Recupera o rótulo
        rotulos.append(rotulo) #Adiciona à lista de rótulos
        linhaAtual+=1 #Avança para próxima linha
        G.addVertice(rotulo) #Adiciona um vértice ao grafo com o rótulo encontrado
    #print(linhas[linhaAtual])


    #Se a palavra arcs aparece aqui, trata-se de um grafo direcionado.
    if "arcs" in linhas[linhaAtual].lower():
        G.direcionado=True
    linhaAtual+=1
    #Itera pelas arestas
    while linhaAtual<len(linhas): #daqui até o final, só há arestas
        dadosAresta = linhas[linhaAtual].split(" ") #Separa os dois (ou três) números (em str) da aresta
        dadosAresta[1]=dadosAresta[1].replace("\n","") #Remove o Enter

        if len(dadosAresta)>2: #Se a linha tem três números, é um grafo ponderado
            G.ponderado=True
            verticeOrigem = rotulos[int(dadosAresta[0])-1]
            verticeDestino = rotulos[int(dadosAresta[1])-1]
            peso = rotulos[int(dadosAresta[2])-1]
            G.addAresta(verticeOrigem, verticeDestino, peso)
        else:

            verticeOrigem = rotulos[int(dadosAresta[0])-1]
            verticeDestino = rotulos[int(dadosAresta[1])-1]
            G.addAresta(verticeOrigem, verticeDestino)
        linhaAtual+=1

    return G

def pajekIntoGrafoPAJEKSRUINS(arquivo):
    f = open(arquivo, "r")
    linhasBasico = f.readlines() #Cria Array com as linhas do arquivo
    f.close()
    linhas = []
    for linha in linhasBasico:
        linhaParsed = linha.replace("\n", "").replace("  ", " ").replace("  ", " ").replace("  ", " ")
        linhas.append(linhaParsed)

    rotulos = [] #Lista que armazena todos os rótulos
    nrVertices = int(linhas[0].split(" ")[1]) #['*vertices', '8']
    linhaAtual = 1 #Registra a linha que está sendo processada no momento

    G = GrafoLista(False, False)
    #Itera pelos vértices
    while linhaAtual< nrVertices+1:
        primeiraAspaIndex = linhas[linhaAtual].index('"') #Usa a primeira aspa pra determinar o início do rótulo do vértice
        rotulo = linhas[linhaAtual][primeiraAspaIndex::].replace('"', "").replace("\n", "") #Recupera o rótulo
        rotulos.append(rotulo) #Adiciona à lista de rótulos
        linhaAtual+=1 #Avança para próxima linha
        G.addVertice(rotulo) #Adiciona um vértice ao grafo com o rótulo encontrado


    #Se a palavra arcs aparece aqui, trata-se de um grafo direcionado.
    if "arcs" in linhas[linhaAtual].lower():
        G.direcionado=True
    linhaAtual+=1
    #Itera pelas arestas

    while linhaAtual<len(linhas): #daqui até o final, só há arestas
        dadosAresta = linhas[linhaAtual].split(" ") #Separa os dois (ou três) números (em str) da aresta
        if "" in dadosAresta: dadosAresta.remove("")
        #print(dadosAresta)
        dadosAresta[1]=dadosAresta[1].replace("\n","") #Remove o Enter
        if len(dadosAresta)>2: #Se a linha tem três números, é um grafo ponderado
            G.ponderado=True
            verticeOrigem = rotulos[int(dadosAresta[0])-1]
            verticeDestino = rotulos[int(dadosAresta[1])-1]
            peso = rotulos[int(dadosAresta[2])-1]
            G.addAresta(verticeOrigem, verticeDestino, peso)
        else:
            verticeOrigem = rotulos[int(dadosAresta[0])-1]
            verticeDestino = rotulos[int(dadosAresta[1])-1]
            G.addAresta(verticeOrigem, verticeDestino)
        linhaAtual+=1

    return G

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
            if self.direcionado:
                return self.grauEntrada(rotulo) + self.grauSaida(rotulo)
            else:
                #return int((self.grauEntrada(rotulo) + self.grauSaida(rotulo))/2)
                return self.grauEntrada(rotulo)


    def ordem(self):
        return len(self.lista)

    #Retorna a versão transposta do grafo passado
    def gerarTransposto(self):
        grafoTransposto = GrafoLista(False, self.ponderado)
        #Adiciona os vértices
        for vertice in self.lista.keys():
            grafoTransposto.addVertice(vertice)
        #Itera pelas arestas, adicionando suas formas reversas
        for verticeOrigem in self.lista.keys():
            for verticeDestino in self.lista.get(verticeOrigem):
                if self.ponderado:
                    peso = self.lista.get(verticeOrigem).get(verticeDestino)
                    grafoTransposto.addAresta(verticeDestino, verticeOrigem, peso)
                else:
                    grafoTransposto.addAresta(verticeDestino, verticeOrigem)
        return grafoTransposto

    def is_Connected(self):
        verticeAleatorio = random.choice(list(self.lista.keys()))
        verticeNaoIncluso="asfsafjasjf980jf38fn3=9n3f30fn"
        #Roda um BFS buscando por um vértice que não existe para atravessar todo o grafo
        return (len(self.lista.keys())==self.BFS(verticeAleatorio,verticeNaoIncluso))

    #Apenas para grafos direcionados
    def is_stronglyConnected(self):
        #Etapa 1 - Verifica se o grafo é conectado.
        verticeAleatorio = random.choice(list(self.lista.keys()))
        verticeNaoIncluso="asfsafjasjf980jf38fn3=9n3f30fn"
        if not len(self.lista.keys())==self.BFS(verticeAleatorio,verticeNaoIncluso):
            return False
        #Etapa 2 - Reverte o grafo e refaz o teste
        else:
            gTransposto = self.gerarTransposto()
            if not len(gTransposto.lista.keys()) == gTransposto.BFS(verticeAleatorio, verticeNaoIncluso):
                return False
            else:
                return True

    #Função que verifica se um Grafo é Euleriano
    def is_Eulerian(self):
        #Caso 1: Grafo é direcionado
        if self.direcionado:
            #1 - Verifica se todos os vértices possuem grau de entrada e saída iguais
            for vertice1 in self.lista.keys():
                if self.grauEntrada(vertice1)!= self.grauSaida(vertice1):
                    return False
            #2 - Verifica se o grafo é fortemente conectado
            if not self.is_stronglyConnected():
                return False

            return True
        #Caso 2: Grafo não é direcionado
        else:
            # Iteração por todos os vértices
            for vertice1 in self.lista.keys():
                #Verifica se todos os graus são pares
                if self.grau(vertice1)%2!=0:
                    return False
            #Verifica se o Grafo é conectado
            if not self.is_Connected():
                return False
            return True

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

    def calcularGrauMedio(self):
        grauMedio = 0
        for vertice in self.lista.keys():
            grauMedio+=self.grau(vertice)
        return grauMedio/self.ordem()

    #BFS para retornar o caminho mais curto em um grafo não-direcionado e não ponderado
    #Funciona apenas para grafos cujos vértices são números inteiros em sequência a partir do 0
    def BFS_CAMINHO(self,origem,destino):
        anteriores = {} #Dicionário que armazena os vértices anteriores de cada vértice.
        fila = []
        #Visitados
        visitados = [origem]
        fila.append(origem)
        #BFS padrão
        while fila!=[]:
            verticeAtual = fila.pop(0)
            for verticeAdjacente in self.retornaAdjacentes(verticeAtual):
                if verticeAdjacente not in visitados:
                    visitados.append(verticeAdjacente)
                    fila.append(verticeAdjacente)
                    anteriores[verticeAdjacente] = verticeAtual #DIFERENÇA - Registra o anterior de cada adjacente
                    if verticeAdjacente == destino:
                        return anteriores
        return {}

    #Função que determina o menor caminho entre dois vértices a partir do caminho retornado
    #Pela função acima
    def determinarMenorCaminho(self,origem,destino):
        caminho = self.BFS_CAMINHO(origem,destino)
        if caminho == {}:
            return []
        vertice = destino #Começa do destino
        caminhoMaisCurto = []
        #O vértice original é o único que não terá um antecessor
        #Itera até chegar a um vértice sem antecessor (a origem)
        while vertice!=None:
            caminhoMaisCurto.append(vertice) #Adiciona vértice ao caminho
            vertice = caminho.get(vertice) #Procede para o pai do vértice adicionado
        caminhoMaisCurto.reverse() # Até agora, o caminho era destino -> origem. Reverte-se a ordem.
        return caminhoMaisCurto

    #REtorna uma lista com todos os menores caminhos de um grafo
    def retornarMenoresCaminhos(self): #Serve apenas para Grafos não-direcionados e não-ponderados
        #SE O GRAFO CONTER VÉRTICES COM RÓTULOS IDÊNTICOS, A FUNÇÃO PODE GERAR ERROS
        # PARTE 1 - Variáveis importantes
        ordem = self.ordem()
        matrizRegistro = np.zeros((ordem, ordem)) #Matriz que registra se um caminho entre dois vértices já foi computado (0 nao, 1 sim)
        rotulosEmInteiros = list(self.lista.keys()) #Lista que associa cada vértice a um número inteiro (necessária para usar a matrizRegistro)
        tamanhosMenoresCaminhos = [] #Armazena todos os tamanhos de todos os menores caminhos

        #PARTE 2 - Laço pelas Origens e Laço aninhado pelos Destinos
        for verticeOrigem in self.lista.keys(): #Itera por todas as origens possíveis
            if self.grauSaida(verticeOrigem) > 0: #Se o grau de saída é maior que zero, então o vértice tem arestas e, portanto, deve ser computado
                for verticeDestino in self.lista.keys(): #Itera por todos os destinos possíveis

                    # PARTE 3 - CONDIÇÕES PARA INICIAR A COMPUTAÇÃO DO CAMINHO
                    #Para computar o caminho, as seguintes condições devem obter
                    #1 - Destino e Origem são diferentes, 2 - O caminho entre origem e destino não ter sido computado ainda, 3 - O destino ter arestas
                    if verticeOrigem != verticeDestino and matrizRegistro[rotulosEmInteiros.index(verticeOrigem)][rotulosEmInteiros.index(verticeDestino)] == 0 and self.grauSaida(verticeDestino) > 0:

                        # PARTE 4 - COMPUTAR O CAMINHO
                        caminho = self.determinarMenorCaminho(verticeOrigem, verticeDestino) #Obtém o menor caminho entre a origem e o destino
                        #PARTE 5 - OTIMIZAÇÂO
                        #Para reduzir o número de BFSs, já armazena os caminhos entre todos os nós no caminho
                        #FUNCIONAMENTO
                        # - Remove o primeiro elemento do caminho e armazena o caminho entre ele e cada um dos outros elementos no caminho
                        #- A distância entre um dois elementos no caminho é sempre a diferença entre os seus indexes
                        while len(caminho)>1:
                            verticeAtual = caminho.pop(0)
                            for index in range(len(caminho)):
                                verticeNoCaminho = caminho[index]
                                # Se o caminho entre o vértice e o destino não foi computado ainda, registra
                                if matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] == 0:
                                    # como o grafo sempre é não-direcionado, marca como computado o caminho em ambas as direções
                                    matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] = 1
                                    matrizRegistro[rotulosEmInteiros.index(verticeNoCaminho)][rotulosEmInteiros.index(verticeAtual)] = 1
                                    #Calcula-se sempre a distância a partir do vértice que era o index 0 e foi removido no início
                                    #Por isso, a distância entre o removido e cada um dos restantes é sempre o index do restante +1
                                    tamanhosMenoresCaminhos.append(index+1)
                                    print(str(verticeAtual) + " | " + str(verticeNoCaminho) + " | Caminho: " + str(
                                        caminho) + " | Tamanho: " + str(index+1))

        return tamanhosMenoresCaminhos

    #Função que transforma um grafo em uma String conforme o padrão .net (PAJEK)
    def gerarTextoPajek(self):
        tamanho = self.ordem() #armazena o tamanho do grafo
        texto = "*Vertices "+str(tamanho)+"\n" #Variável que armazena o texto que será gravado. Já contém a parte inicial.
        rotulos = list(self.lista.keys()) #Lista com todos os rótulos do grafo
        termoArestas = "" #Variável que terá arcs ou edges
        if self.direcionado:
            termoArestas="Arcs"
        else:
            termoArestas="Edges"
        contador = 1
        #Laço para preencher a parte Número "Rótulo" do arquivo
        while contador<tamanho+1:
            texto = texto + str(contador)+' "'+str(rotulos[contador-1])+'"'+"\n"
            contador+=1
        #Adiciona a parte inicial da seção de arestas
        texto = texto +"*"+ termoArestas + "\n"
        #Adiciona as arestas
        for vertice in self.lista.keys():
            for verticeDestino in self.lista.get(vertice).keys():
                texto = texto + str(rotulos.index(vertice)+1)+" "+str(rotulos.index(verticeDestino)+1)
                if self.ponderado:
                    texto = texto + " "+str(self.lista.get(vertice).get(verticeDestino))+"\n"
                else:
                    texto = texto +"\n"

        return texto

    #Função que criar um arquivo .net a partir do grafo
    def gravarPajek(self, nomeArquivo):
        textoPajek = self.gerarTextoPajek()
        f = open(nomeArquivo+".net", "w")
        f.write(textoPajek)
        f.close()

    #Apenas para grafos não ponderados e não-direcionados
    def calcularExcentricidade(self, origem):
        # SE O GRAFO CONTER VÉRTICES COM RÓTULOS IDÊNTICOS, A FUNÇÃO PODE GERAR ERROS
        ordem = self.ordem()  # Número de vértices
        listaRegistro = [False for x in range(ordem)] # Lista que registra se um caminho entre dois vértices já foi computado (0 nao, 1 sim)
        rotulosEmInteiros = list(self.lista.keys())  # Lista que associa cada vértice a um número inteiro (necessária para usar a matrizRegistro)
        tamanhosMenoresCaminhos = []  # Armazena todos os tamanhos de todos os menores caminhos
        #Laço pelos Destinos
        for verticeDestino in self.lista.keys():  # Itera por todos os destinos possíveis
            print("EXCENTRICIDADE | Origem: "+str(origem)+" | Destino: "+str(verticeDestino))
            if origem != verticeDestino and listaRegistro[rotulosEmInteiros.index(verticeDestino)] == False:
                caminho = self.determinarMenorCaminho(origem, verticeDestino)  # Obtém o menor caminho entre a origem e o destino
                if caminho == []:
                    tamanhosMenoresCaminhos.append(np.Inf) #Se o caminho não existe (grafo deconexo), a distância é infinita
                else:
                # Para reduzir o número de BFSs, já armazena os caminhos entre a origem e todos os nós no caminho
                    for indexVertice in range(1,len(caminho)):  # Itera pelos vértices no caminho ignorando a origem
                        verticeDestino = caminho[indexVertice]
                        listaRegistro[rotulosEmInteiros.index(verticeDestino)]=True
                        #Como o grafo é não-ponderado, a distância da origem até ele é o valor do index do destino na lista caminho
                        tamanhosMenoresCaminhos.append(indexVertice)
        return max(tamanhosMenoresCaminhos)

    def calcularRaio(self): #Serve apenas para Grafos não-direcionados e não-ponderados
        excentricidades = []
        for verticeOrigem in self.lista.keys():
            ex = self.calcularExcentricidade(verticeOrigem)
            excentricidades.append(ex)
        return min(excentricidades)

    #Versão otimizada do Raio usando a Matriz de Registros
    def calcularRaioOtimizado(self): #Serve apenas para Grafos não-direcionados e não-ponderados
        excentricidades = {vertice:0 for vertice in self.lista.keys()}
        #SE O GRAFO CONTER VÉRTICES COM RÓTULOS IDÊNTICOS, A FUNÇÃO PODE GERAR ERROS
        # PARTE 1 - Variáveis importantes
        ordem = self.ordem()
        matrizRegistro = np.zeros((ordem, ordem)) #Matriz que registra se um caminho entre dois vértices já foi computado (0 nao, 1 sim)
        rotulosEmInteiros = list(self.lista.keys()) #Lista que associa cada vértice a um número inteiro (necessária para usar a matrizRegistro)

        #PARTE 2 - Laço pelas Origens e Laço aninhado pelos Destinos
        for verticeOrigem in self.lista.keys(): #Itera por todas as origens possíveis
            if self.grauSaida(verticeOrigem) > 0: #Se o grau de saída é maior que zero, então o vértice tem arestas e, portanto, deve ser computado
                for verticeDestino in self.lista.keys(): #Itera por todos os destinos possíveis

                    # PARTE 3 - CONDIÇÕES PARA INICIAR A COMPUTAÇÃO DO CAMINHO
                    #Para computar o caminho, as seguintes condições devem obter
                    #1 - Destino e Origem são diferentes, 2 - O caminho entre origem e destino não ter sido computado ainda, 3 - O destino ter arestas
                    if verticeOrigem != verticeDestino \
                            and matrizRegistro[rotulosEmInteiros.index(verticeOrigem)][rotulosEmInteiros.index(verticeDestino)] == 0 \
                            and self.grauSaida(verticeDestino) > 0:
                        # PARTE 4 - COMPUTAR O CAMINHO
                        caminho = self.determinarMenorCaminho(verticeOrigem, verticeDestino) #Obtém o menor caminho entre a origem e o destino
                        if caminho==[]:
                            matrizRegistro[rotulosEmInteiros.index(verticeOrigem)][rotulosEmInteiros.index(verticeDestino)] = 1
                            matrizRegistro[rotulosEmInteiros.index(verticeDestino)][rotulosEmInteiros.index(verticeOrigem)] = 1
                            excentricidades[verticeOrigem] = np.Inf
                            excentricidades[verticeDestino] = np.Inf
                        else:
                            #PARTE 5 - OTIMIZAÇÂO
                            #Para reduzir o número de BFSs, já armazena os caminhos entre todos os nós no caminho
                            #FUNCIONAMENTO
                            # - Remove o primeiro elemento do caminho e armazena o caminho entre ele e cada um dos outros elementos no caminho
                            #- A distância entre um dois elementos no caminho é sempre a diferença entre os seus indexes
                            while len(caminho)>1:
                                verticeAtual = caminho.pop(0)
                                for index in range(len(caminho)):
                                    verticeNoCaminho = caminho[index]
                                    if matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] == 0: #Se o caminho entre o vértice e o destino não foi computado ainda, registra
                                        # como o grafo sempre é não-direcionado, marca como computado o caminho em ambas as direções
                                        matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] = 1
                                        matrizRegistro[rotulosEmInteiros.index(verticeNoCaminho)][rotulosEmInteiros.index(verticeAtual)] = 1
                                        # Incrementa a contagem de betweeness para o vertice buscado se ele estiver entre as extremidades no caminho
                                        # LEMBRAR: O VÉRTICE NO INÍCIO DO CAMINHO COMPUTADO FOI RETIRADO. O index 0, portanto, NÃO É o início do caminho
                                        # A Cada iteração, processa-se o caminho entre o vértice retirado e o que está no INDEX atual
                                        if excentricidades.get(verticeAtual)<=index+1:
                                            excentricidades[verticeAtual]=index+1
                                        if excentricidades.get(verticeNoCaminho)<=index+1:
                                            excentricidades[verticeNoCaminho]=index+1

                                        print("RAIO GRAFO | " + str(verticeAtual) + " | " + str(
                                            verticeNoCaminho) + " | Caminho: " + str(
                                            caminho) + " | Tamanho: " + str(index + 1))
        return min(list(excentricidades.values()))

    def calcularDiametro(self): #Serve apenas para Grafos não-direcionados e não-ponderados
        excentricidades = []
        for verticeOrigem in self.lista.keys():
            print("DIÂMETRO | ORIGEM: "+verticeOrigem)
            ex = self.calcularExcentricidade(verticeOrigem)
            if ex==np.inf:
                return np.inf
            else:
                excentricidades.append(ex)
        return max(excentricidades)

    #Versão otimizada do Diametro usando a Matriz de Registros
    def calcularDiametroOtimizado(self):
        excentricidades = {vertice:0 for vertice in self.lista.keys()}
        #SE O GRAFO CONTER VÉRTICES COM RÓTULOS IDÊNTICOS, A FUNÇÃO PODE GERAR ERROS
        # PARTE 1 - Variáveis importantes
        ordem = self.ordem()
        matrizRegistro = np.zeros((ordem, ordem)) #Matriz que registra se um caminho entre dois vértices já foi computado (0 nao, 1 sim)
        rotulosEmInteiros = list(self.lista.keys()) #Lista que associa cada vértice a um número inteiro (necessária para usar a matrizRegistro)

        #PARTE 2 - Laço pelas Origens e Laço aninhado pelos Destinos
        for verticeOrigem in self.lista.keys(): #Itera por todas as origens possíveis
            if self.grauSaida(verticeOrigem) > 0: #Se o grau de saída é maior que zero, então o vértice tem arestas e, portanto, deve ser computado
                for verticeDestino in self.lista.keys(): #Itera por todos os destinos possíveis

                    # PARTE 3 - CONDIÇÕES PARA INICIAR A COMPUTAÇÃO DO CAMINHO
                    #Para computar o caminho, as seguintes condições devem obter
                    #1 - Destino e Origem são diferentes, 2 - O caminho entre origem e destino não ter sido computado ainda, 3 - O destino ter arestas
                    if verticeOrigem != verticeDestino \
                            and matrizRegistro[rotulosEmInteiros.index(verticeOrigem)][rotulosEmInteiros.index(verticeDestino)] == 0 \
                            and self.grauSaida(verticeDestino) > 0:
                        # PARTE 4 - COMPUTAR O CAMINHO
                        caminho = self.determinarMenorCaminho(verticeOrigem, verticeDestino) #Obtém o menor caminho entre a origem e o destino
                        if caminho==[]:
                            matrizRegistro[rotulosEmInteiros.index(verticeOrigem)][rotulosEmInteiros.index(verticeDestino)] = 1
                            matrizRegistro[rotulosEmInteiros.index(verticeDestino)][rotulosEmInteiros.index(verticeOrigem)] = 1
                            excentricidades[verticeOrigem] = np.Inf
                            excentricidades[verticeDestino] = np.Inf
                        else:
                            #PARTE 5 - OTIMIZAÇÂO
                            #Para reduzir o número de BFSs, já armazena os caminhos entre todos os nós no caminho
                            #FUNCIONAMENTO
                            # - Remove o primeiro elemento do caminho e armazena o caminho entre ele e cada um dos outros elementos no caminho
                            #- A distância entre um dois elementos no caminho é sempre a diferença entre os seus indexes
                            while len(caminho)>1:
                                verticeAtual = caminho.pop(0)
                                for index in range(len(caminho)):
                                    verticeNoCaminho = caminho[index]
                                    if matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] == 0: #Se o caminho entre o vértice e o destino não foi computado ainda, registra
                                        # como o grafo sempre é não-direcionado, marca como computado o caminho em ambas as direções
                                        matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] = 1
                                        matrizRegistro[rotulosEmInteiros.index(verticeNoCaminho)][rotulosEmInteiros.index(verticeAtual)] = 1
                                        # Incrementa a contagem de betweeness para o vertice buscado se ele estiver entre as extremidades no caminho
                                        # LEMBRAR: O VÉRTICE NO INÍCIO DO CAMINHO COMPUTADO FOI RETIRADO. O index 0, portanto, NÃO É o início do caminho
                                        # A Cada iteração, processa-se o caminho entre o vértice retirado e o que está no INDEX atual
                                        if excentricidades.get(verticeAtual)<=index+1:
                                            excentricidades[verticeAtual]=index+1
                                        if excentricidades.get(verticeNoCaminho)<=index+1:
                                            excentricidades[verticeNoCaminho]=index+1

                                        print("DIAMETRO GRAFO | " + str(verticeAtual) + " | " + str(
                                            verticeNoCaminho) + " | Caminho: " + str(
                                            caminho) + " | Tamanho: " + str(index + 1))
        return max(list(excentricidades.values()))

    #Gera um gráfico com a distribuição de graus e de caminhos mais curtos
    def plotGrauCam(self):
        import matplotlib.pyplot as plt
        graus = []
        for vertice in self.lista.keys():
            graus.append(self.grau(vertice))
        caminhos = self.retornarMenoresCaminhos()
        fig, ax = plt.subplots(1, 2)
        fig.suptitle('Distribuição de Graus e de Caminhos mais Curtos')
        ax[0].hist(graus, alpha=0.5, color='g')
        ax[1].hist(caminhos, alpha=0.5, color='b')
        plt.show()

    def betweenessVertice(self, vertice):
        # SE O GRAFO CONTER VÉRTICES COM RÓTULOS IDÊNTICOS, A FUNÇÃO PODE GERAR ERROS
        # PARTE 1 - Variáveis importantes
        ordem = self.ordem()  # Número de vértices
        matrizRegistro = np.zeros((ordem, ordem))  # Matriz que registra se um caminho entre dois vértices já foi computado (0 nao, 1 sim)
        rotulosEmInteiros = list(self.lista.keys())  # Lista que associa cada vértice a um número inteiro (necessária para usar a matrizRegistro)
        caminhosComVertice = 0  # Armazena todos os tamanhos de todos os menores caminhos

        # PARTE 2 - Laço pelas Origens e Laço aninhado pelos Destinos
        for verticeOrigem in self.lista.keys():  # Itera por todas as origens possíveis
            if self.grauSaida(verticeOrigem) > 0 and verticeOrigem!=vertice:  # Se o grau de saída é maior que zero, então o vértice tem arestas e, portanto, deve ser computado
                for verticeDestino in self.lista.keys():  # Itera por todos os destinos possíveis
                    #Se o caminho já foi computado, ou o destino é idêntico ao vértice buscado, ou origem e destino são iguais, ignora essa iteração
                    if matrizRegistro[rotulosEmInteiros.index(verticeOrigem)][rotulosEmInteiros.index(verticeDestino)] == 1 or verticeDestino==vertice or verticeOrigem == verticeDestino:
                        continue
                    else:
                        caminho = self.determinarMenorCaminho(verticeOrigem, verticeDestino)
                    # Computação otimizada do caminho
                    while len(caminho) > 1:
                        verticeAtual = caminho.pop(0)  # Destaca o vértice que será a origem dos caminhos na iteração
                        for index in range(len(caminho)):  # Itera pelos indexes restantes no caminho
                            verticeNoCaminho = caminho[index]
                            if matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] == 0:  # Se o caminho entre o vértice e o destino não foi computado ainda, registra
                                # como o grafo sempre é não-direcionado, marca como computado o caminho em ambas as direções
                                matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] = 1
                                matrizRegistro[rotulosEmInteiros.index(verticeNoCaminho)][rotulosEmInteiros.index(verticeAtual)] = 1
                                # Incrementa a contagem de betweeness para o vertice buscado se ele estiver entre as extremidades no caminho
                                # LEMBRAR: O VÉRTICE NO INÍCIO DO CAMINHO COMPUTADO FOI RETIRADO. O index 0, portanto, NÃO É o início do caminho
                                # A Cada iteração, processa-se o caminho entre o vértice retirado e o que está no INDEX atual
                                if vertice in caminho[0:index]:
                                    caminhosComVertice += 1
                                print("BETWEENESS VERTICE" +str(vertice)+"| " + str(verticeAtual) + " | " + str(
                                    verticeNoCaminho) + " | Caminho: " + str(
                                    caminho) + " | Tamanho: " + str(index + 1))
        return caminhosComVertice

    #Retorna o vértice com a maior centralidade de intermediação, e o valor da centralidade
    def betweenessTodoGrafo(self):
        retorno = [-1, "1"]
        for vertice in self.lista.keys():
            bet = self.betweenessVertice(vertice)
            if bet>retorno[0]:
                retorno[0]=bet
                retorno[1]=vertice
        return retorno

    #Versão otimizada do Betweeness usando a Matriz de Registros
    def betweenessTodoGrafoOTIMIZADO(self):
        ordem = self.ordem()
        dict = {vertice:0 for vertice in range(ordem)} #Dicionário que registra o valor de betweeness para cada vértice
        matrizRegistro = np.zeros((ordem, ordem))  # Matriz que registra se um caminho entre dois vértices já foi computado (0 nao, 1 sim)
        rotulosEmInteiros = list(self.lista.keys()) #Lista que associa cada vértice a um número inteiro (necessária para usar a matrizRegistro)
        for vertice1 in self.lista.keys():
            for vertice2 in self.lista.keys():
                #Se o caminho já foi computado, passa para o próximo caminho
                if matrizRegistro[rotulosEmInteiros.index(vertice1)][rotulosEmInteiros.index(vertice2)] == 1:
                    continue
                else:
                    caminho = self.determinarMenorCaminho(vertice1, vertice2)
                    #Computação otimizada do caminho
                    while len(caminho) > 1:
                        verticeAtual = caminho.pop(0)  #Destaca o vértice que será a origem dos caminhos na iteração
                        for index in range(len(caminho)): #Itera pelos indexes restantes no caminho
                            verticeNoCaminho = caminho[index]
                            if matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] == 0:  # Se o caminho entre o vértice e o destino não foi computado ainda, registra
                                # como o grafo sempre é não-direcionado, marca como computado o caminho em ambas as direções
                                matrizRegistro[rotulosEmInteiros.index(verticeAtual)][rotulosEmInteiros.index(verticeNoCaminho)] = 1
                                matrizRegistro[rotulosEmInteiros.index(verticeNoCaminho)][rotulosEmInteiros.index(verticeAtual)] = 1
                                #Incrementa a contagem de betweeness para todos os vértices entre o início e o final do caminho
                                #LEMBRAR: O VÉRTICE NO INÍCIO DO CAMINHO COMPUTADO FOI RETIRADO. O index 0, portanto, NÃO É o início do caminho
                                #A Cada iteração, computa-se o caminho entre o vértice retirado e o que está no INDEX atual
                                for verticeBetween in caminho[0:index]:
                                    dict[verticeBetween]+=1
                                print("BETWEENESS GRAFO | "+str(verticeAtual) + " | " + str(verticeNoCaminho) + " | Caminho: " + str(
                                    caminho) + " | Tamanho: " + str(index + 1))
        retorno = [-1, "1"] #Lista que será retornada, primeiro valor é a centralidade de intermediação, o segundo é o vértice
        for vertice in dict:
            #Itera pelo dicionário buscando o vértice com o maior valor de intermediação
            if dict.get(vertice)>retorno[0]:
                retorno[0]=dict.get(vertice)
                retorno[1]=vertice
        return retorno



    def proximidadeVertice(self, vertice):
        # SE O GRAFO CONTER VÉRTICES COM RÓTULOS IDÊNTICOS, A FUNÇÃO PODE GERAR ERROS
        ordem = self.ordem()  # Número de vértices
        listaRegistro = [False for x in range(ordem)] # Matriz que registra se um caminho entre dois vértices já foi computado (0 nao, 1 sim)
        rotulosEmInteiros = list(self.lista.keys())  # Lista que associa cada vértice a um número inteiro (necessária para usar a matrizRegistro)
        tamanhosMenoresCaminhos = []  # Armazena todos os tamanhos de todos os menores caminhos
        #Laço pelos Destinos
        for verticeDestino in self.lista.keys():  # Itera por todos os destinos possíveis
            if vertice != verticeDestino and listaRegistro[rotulosEmInteiros.index(verticeDestino)] == False:
                caminho = self.determinarMenorCaminho(vertice, verticeDestino)  # Obtém o menor caminho entre a origem e o destino
                if caminho != []:
                # Para reduzir o número de BFSs, já armazena os caminhos entre a origem e todos os nós no caminho
                    for indexVertice in range(1,len(caminho)):  # Itera pelos vértices no caminho ignorando a origem
                        verticeDestino = caminho[indexVertice]
                        listaRegistro[rotulosEmInteiros.index(verticeDestino)]=True
                        #Como o grafo é não-ponderado, a distância da origem até ele é o valor do index do destino na lista caminho
                        tamanhosMenoresCaminhos.append(indexVertice)
        if len(tamanhosMenoresCaminhos)>0:
            return (self.ordem()-1)/sum(tamanhosMenoresCaminhos)
        else:
            return 0

    def proximidadeTodoGrafo(self):
        retorno = [0.0, "1"]
        for vertice in self.lista.keys():
            print("PROXIMIDADE | Checado: " + str(vertice))
            prox = self.proximidadeVertice(vertice)
            if prox>retorno[0]:
                retorno[0]=prox
                retorno[1]=vertice
        return retorno



if __name__ == '__main__':
    #G = randomFreeScale(500,700)
    #G.gravarPajek("grafo1")
    #G.plotGrauCam()
    G2 = pajekIntoGrafoPAJEKSRUINS('foldoc.net')
    G2.imprimeLista()

    #G = pajekIntoGrafoPAJEKSRUINS('foldoc.net')
    #print(G.calcularExcentricidade(1))

