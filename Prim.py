#Justificación: El algoritmo de Prim es un algoritmo para encontrar el árbol parcial mínimo, por lo que
#en este programa se aplica a encontrar el árbol parcial mínimo partiendo del nodo entrada para encontrar 
#el camino con mejor tiempo para visitar todas las áreas de colomos

import matplotlib.pyplot as plt
import networkx as nx

import heapq

def prim(grafo, inicio):
    print(f"• Nodo inicial: {inicio}\n")

    # Conjunto de nodos ya incluidos en el APM
    visitados = set()

    # Cola de prioridad de aristas: (peso, desde, hacia)
    pq = []

    # Agregamos todas las aristas desde el nodo inicial
    visitados.add(inicio)
    for vecino, peso in grafo[inicio]:
        heapq.heappush(pq, (peso, inicio, vecino))

    # Lista del árbol parcial mínimo (las aristas seleccionadas)
    apm = []
    costo_total = 0

    paso = 1

    # Mientras existan aristas candidatas
    while pq and len(visitados) < len(grafo):

        peso, u, v = heapq.heappop(pq)

        print(f"\nPaso {paso}:")
        paso += 1

        print(f"- Considerando arista: {u} --{peso}--> {v}")

        # Si el nodo destino ya está visitado, ignoramos esta arista (evita ciclos)
        if v in visitados:
            print("Esta arista se DESCARTA (crearía un ciclo).")
            continue

        # Si llegamos aquí significa que es la mejor arista válida
        print("Esta arista SE AGREGA al APM.")

        visitados.add(v)
        apm.append((u, v, peso))
        costo_total += peso

        # Añadimos las nuevas aristas que salen desde el nodo recién integrado
        for vecino, p in grafo[v]:
            if vecino not in visitados:
                heapq.heappush(pq, (p, v, vecino))
                print(f"Nueva arista candidata añadida: {v} --{p}--> {vecino}")

    print("\nRESULTADO FINAL")
    print("Aristas del Árbol Parcial Mínimo:")
    for u, v, w in apm:
        print(f"  {u} -- {w} --> {v}")

    print(f"\nCosto total del APM: {costo_total}\n")

    return apm, costo_total

def dibujar_prim(grafo, inicio):
    mst, costo = prim(grafo, inicio)

    #Convertimos tu grafo al formato de NetworkX
    G = nx.Graph()
    for nodo in grafo:
        for vecino, peso in grafo[nodo]:
            G.add_edge(nodo, vecino, weight=peso)

    #Creamos un grafo SOLO con las aristas del MST
    MST = nx.Graph()
    for u, v, peso in mst:
        MST.add_edge(u, v, weight=peso)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 7))
    plt.title(f"Árbol Parcial Mínimo (Prim) – Costo total: {costo}", fontsize=14)

    #Dibujar todas las aristas en gris
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", width=1.5)

    #Dibujar las aristas del MST en verde
    nx.draw_networkx_edges(
        G, pos,
        edgelist=MST.edges(),
        width=3,
        edge_color="green"
    )

    #Dibujar pesos
    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)

    plt.show()


graph = {
    'Entrada': [('Fuente', 7), ('Jardin', 9), ('Lago', 14)],
    'Fuente': [('Entrada', 7), ('Jardin', 10), ('Mirador', 15)],
    'Jardin': [('Entrada', 9), ('Fuente', 10), ('Mirador', 11), ('Lago', 2)],
    'Mirador': [('Fuente', 15), ('Jardin', 11), ('Puente', 6)],
    'Puente': [('Mirador', 6), ('Lago', 9)],
    'Lago': [('Entrada', 14), ('Jardin', 2), ('Puente', 9)],
}

prim(graph, 'Entrada')
dibujar_prim(graph, "Entrada")