#Justifiación: EL algoritmo de Dijkstra es un algoritmo para encontrar el camino más corto, por lo que
#en este programa se aplica a encontrar el camino más caorto hacia la universidad partiendo del nodo casa

#Importación de librerías necesarias
import math
import heapq
import matplotlib.pyplot as plt

#Definición del grafo con vecinos y pesos
graph = {
    'Casa': [('Av_Patria', 6), ('Av_Lopez_Mateos', 9)],
    'Av_Patria': [('Casa', 6), ('Av_Montevideo', 5), ('Av_Americas', 7)],
    'Av_Lopez_Mateos': [('Casa', 9), ('Av_Americas', 4)],
    'Av_Americas': [('Av_Lopez_Mateos', 4), ('Av_Patria', 7), ('Pablo_Neruda', 6)],
    'Av_Montevideo': [('Av_Patria', 5), ('Pablo_Neruda', 8)],
    'Pablo_Neruda': [('Av_Americas', 6), ('Av_Montevideo', 8)]
}

#Defición del nodo origen y destino
source = 'Casa'
target = 'Pablo_Neruda'  

def dijkstra_verbose(graph, source, target=None):
    dist = {node: math.inf for node in graph} #distancias iniciales
    prev = {node: None for node in graph} #predecesores iniciales
    dist[source] = 0 #distancia al origen es 0

    pq = [(0, source)]
    visited = set() #nodos visitados

    step = 0 #contador de pasos

    print()
    print("*"*60)
    print(f"SIMULACIÓN: Algoritmo de Dijkstra — origen = {source}")
    print("*"*60, "\n")
    print("Paso 0: inicialización")
    print_state(step, dist, visited, pq, prev) #estado inicial
    print()

    # Bucle principal del algoritmo
    while pq:
        step += 1 #incremento del paso
        d, u = heapq.heappop(pq) #extraer nodo con menor distancia

        # Si ya fue visitado, se ignora
        if u in visited:
            print(f"[Paso {step}] Se extrae {u} del PQ con distancia {d} (ignorado, ya visitado).")
            continue
        
        #Nodo actual marcado como visitado
        print(f"[Paso {step}] Se extrae {u} del PQ con distancia {d}. Marcando como visitado.")
        visited.add(u)

        # Si se alcanza el nodo destino, se termina
        if target is not None and u == target:
            print(f"  -> Nodo destino '{target}' alcanzado. Terminando.")
            break

        # Relajación de los vecinos
        for v, w in graph[u]:
            old = dist[v] #distancia antigua al vecino

            #si ya fue visitado, no se relaja
            if v in visited:
                print(f"    - Vecino {v} (peso {w}): ya visitado, no se relaja.")
                continue
            new = dist[u] + w #nueva distancia posible
            print(f"    - Vecino {v} (peso {w}): dist[{v}] = {old} -> posible {new}", end='')
            
            #si la nueva distancia es mejor, se actualiza
            if new < old:
                dist[v] = new
                prev[v] = u
                heapq.heappush(pq, (new, v)) #empujar al PQ
                print("  => actualizado y empujado al PQ.")
            else:
                print("  => no mejora.")

        # se muestra el estado después del paso
        print_state(step, dist, visited, pq, prev)
        print()

    #Resultados finales
    print()
    print("*"*60)
    print("Resultado final: distancias mínimas desde", source)
    print("*"*60)
    print()
    for node in sorted(dist):
        d = dist[node]
        path = reconstruct_path(prev, source, node)
        d_str = f"{d}" if d != math.inf else "∞"
        print(f"  - {source} -> {node}: {d_str}\t Ruta: {path}")
    print("*"*60)
    print()
    return dist, prev

#Función para imprimir el estado actual del algoritmo
def print_state(step, dist, visited, pq, prev):
    print(f"Estado después del paso {step}:")
    print("  Distancias:", ", ".join(f"{n}:{'∞' if d==math.inf else d}" for n,d in sorted(dist.items())))
    print("  Visitados:", sorted(list(visited)) if visited else "[]")
    print("  PQ:", [(d,n) for d,n in pq])
    print("  Predecesores:", ", ".join(f"{n}:{prev[n]}" for n in sorted(prev)))

#Función para reconstruir el camino desde el origen hasta el destino
def reconstruct_path(prev, source, target):
    # Si no hay camino
    if prev.get(target) is None and target != source:
        if target == source:
            return [source]
        if target not in prev:
            return []
        
    # Reconstrucción del camino
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        if cur == source:
            break
        cur = prev[cur]
    path.reverse() #reversar el camino
    if path and path[0] == source:
        return path
    return []

#Ejecutución del algoritmo
distances, predecessors = dijkstra_verbose(graph, source, target)

#Visualización de la parte gráfica
nodes = sorted(graph.keys())
n = len(nodes)
#Posiciones circulares para los nodos
pos = {nodes[i]: (math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)}
plt.figure(figsize=(6,6))

#Dibujar las aristas con pesos
for u in graph:
    ux, uy = pos[u]
    for v, w in graph[u]:
        #Para evitar dibujar dos veces la misma arista
        if u < v:
            vx, vy = pos[v]
            plt.plot([ux, vx], [uy, vy])
            #Mostrar el peso en el medio de la arista
            mx, my = (ux+vx)/2, (uy+vy)/2
            plt.text(mx, my, str(w), fontsize=10, ha='center', va='center')

#Dibujar los nodos
for node, (x,y) in pos.items():
    plt.scatter([x], [y])
    plt.text(x, y+0.08, node, fontsize=12, ha='center')

plt.axis('off')
plt.title('Grafica de algoritmo Dijkstra, nodo inical: ' + source)
plt.show() #Mostrar la gráfica