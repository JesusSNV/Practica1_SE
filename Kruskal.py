#Justificación: El algoritmo de Kruskal es un algoritmo para encontrar el árbol parcial mínimo y máximo, por lo que
#en el caso del mínimo se aplic apara encontrar el arbol para visitar todas las áreas de colomos en el menor tiempo posible,
#mientras que el máximo se orienta a encontrar el arbol para visitar todas las áreas de colomos en el mayor tiempo posible.

import matplotlib.pyplot as plt
import networkx as nx

def kruskal(grafo, modo="min"):
    print(f"\nALGORITMO DE KRUSKAL \n({'MÍNIMO' if modo=='min' else 'MÁXIMO'} COSTE)\n")

    #Convertir el grafo en una lista de aristas
    aristas = []
    for u in grafo:
        for v, peso in grafo[u]:
            # Evita duplicar aristas (A-B y B-A)
            if (v, u, peso) not in aristas:
                aristas.append((u, v, peso))

    #Ordenar aristas por peso
    aristas.sort(key=lambda x: x[2], reverse=(modo=="max"))

    print("Aristas ordenadas:")
    for u, v, p in aristas:
        print(f"  {u} -- {p} -- {v}")

    print("\n")

    #Estructura union-find
    padre = {nodo: nodo for nodo in grafo}

    def encontrar(nodo):
        #Encuentra la raíz del conjunto del nodo
        while padre[nodo] != nodo:
            nodo = padre[nodo]
        return nodo

    def unir(a, b):
        #Une los conjuntos de los nodos a y b
        raizA = encontrar(a)
        raizB = encontrar(b)
        if raizA != raizB:
            padre[raizB] = raizA


    #Se recorren las aristas en orden
    mst = []
    costo_total = 0
    paso = 1

    for u, v, peso in aristas:
        print(f"Paso {paso}: Considerando arista {u} -- {peso} -- {v}")
        paso += 1

        raiz_u = encontrar(u)
        raiz_v = encontrar(v)

        if raiz_u != raiz_v:
            #Si no forman ciclo -> se agrega
            print("Se agrega al árbol (no forma ciclo).")
            mst.append((u, v, peso))
            costo_total += peso
            unir(u, v)
        else:
            #Si forman ciclo -> se descarta
            print("Se descarta (formaría un ciclo).")

        print()

        #Si ya tenemos n-1 aristas, se da por concluido
        if len(mst) == len(grafo) - 1:
            break

    #Resultados
    print("\nRESULTADO FINAL: ")
    print("Aristas del árbol generado:")
    for u, v, p in mst:
        print(f"  {u} -- {p} -- {v}")

    print(f"\nCosto total del árbol: {costo_total}\n")

    return mst, costo_total

def dibujar_kruskal(grafo, modo="min"):
    mst, costo = kruskal(grafo, modo)

    #Convertimos el grafo original a NetworkX
    G = nx.Graph()
    for nodo in grafo:
        for vecino, peso in grafo[nodo]:
            G.add_edge(nodo, vecino, weight=peso)

    #Grafo SOLO con aristas del MST de Kruskal
    MST = nx.Graph()
    for u, v, peso in mst:
        MST.add_edge(u, v, weight=peso)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 7))
    titulo = "Árbol de Costo Mínimo (Kruskal)" if modo == "min" else "Árbol de Costo Máximo (Kruskal)"
    plt.title(f"{titulo} - Costo total: {costo}", fontsize=14)

    #Dibujar grafo original en gris
    nx.draw(G, pos, with_labels=True, node_color="lightcyan", edge_color="gray", width=1.5)

    #Dibujar las aristas del MST en azul o rojo según modo
    color = "blue" if modo == "min" else "red"
    nx.draw_networkx_edges(
        G, pos,
        edgelist=MST.edges(),
        width=3,
        edge_color=color
    )

    #Dibujar pesos
    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)

    plt.show()

graph1 = {
    'Entrada': [('Fuente', 7), ('Jardin', 9), ('Lago', 14)],
    'Fuente': [('Entrada', 7), ('Jardin', 10), ('Mirador', 15)],
    'Jardin': [('Entrada', 9), ('Fuente', 10), ('Mirador', 11), ('Lago', 2)],
    'Mirador': [('Fuente', 15), ('Jardin', 11), ('Puente', 6)],
    'Puente': [('Mirador', 6), ('Lago', 9)],
    'Lago': [('Entrada', 14), ('Jardin', 2), ('Puente', 9)],
}

graph2 = {
    'Entrada': [('Fuente', 4), ('Jardin', 6), ('Lago', 8)],
    'Fuente': [('Entrada', 4), ('Jardin', 7), ('Mirador', 3)],
    'Jardin': [('Entrada', 6), ('Fuente', 7), ('Mirador', 5), ('Lago', 9)],
    'Mirador': [('Fuente', 3), ('Jardin', 5), ('Puente', 2)],
    'Puente': [('Mirador', 2), ('Lago', 6)],
    'Lago': [('Entrada', 8), ('Jardin', 9), ('Puente', 6)],
}

kruskal(graph1, modo="min") #Árbol de costo mínimo
kruskal(graph2, modo="max") #Árbol de costo máximo
dibujar_kruskal(graph1, modo="min") #Árbol de costo mínimo
dibujar_kruskal(graph2, modo="max") #Árbol de costo máximo