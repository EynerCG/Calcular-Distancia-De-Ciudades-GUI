import pandas as pd
from tkinter import *
from tkinter.ttk import Notebook
from tkinter import messagebox
import networkx as nx
from Util import VistaTabla
import Util

iconos = ["./iconos/Play.png"]
textoBoton = ["Calcular la distancia"]
df = None

def obtenerNombre():
    global df
    df = pd.read_csv("ciudades.csv")
    ciudades = pd.concat([df["Origen"], df["Destino"]]).drop_duplicates().tolist()
    return [[ciudad] for ciudad in ciudades]

def obtenerNodos():
    global df
    df = pd.read_csv("ciudades.csv")
    nodos = df[["Origen", "Destino", "Distancia"]].values.tolist()
    return nodos

def ciudades():
    global df
    df = pd.read_csv("ciudades.csv")
    nombres_ciudades = pd.concat([df["Origen"], df["Destino"]]).drop_duplicates().tolist()
    return nombres_ciudades

def rutaMasCorta(origen, destino):
    df = pd.read_csv("ciudades.csv")
    grafo = nx.from_pandas_edgelist(df, source="Origen", target="Destino", edge_attr="Distancia", create_using=nx.Graph())
    try:
        ruta = nx.dijkstra_path(grafo, source=origen, target=destino, weight="Distancia")
    except nx.NetworkXNoPath:
        return None

    distancias_acumuladas = [[origen, 0]]
    distancia_total = 0

    for i in range(len(ruta) - 1):
        distancia_segmento = grafo[ruta[i]][ruta[i + 1]]['Distancia']
        distancia_total += distancia_segmento
        distancias_acumuladas.append([ruta[i + 1], distancia_total])  

    return distancias_acumuladas

def mostrar_distancia():
    origen = ciudad_origen_lista.get() 
    destino = ciudad_destino_lista.get()  
    
    if destino and not origen:
        messagebox.showwarning("Advertencia", "Por favor selecciona una ciudad de origen para calcular la distancia.")
    elif origen and not destino:
        messagebox.showwarning("Advertencia", "Por favor selecciona una ciudad de destino para calcular la distancia.")
    elif origen and destino:
        recorrido = rutaMasCorta(origen, destino)
        if recorrido is not None:
            tabla_distancia.delete(*tabla_distancia.get_children())  # Limpiar la tabla
            for item in recorrido:
                tabla_distancia.insert("", "end", values=item)  # Insertar cada recorrido en la tabla
        else:
            messagebox.showerror("Error", "No se encontró una ruta entre las ciudades seleccionadas.")
    else:
        messagebox.showwarning("Advertencia", "Por favor selecciona ambas ciudades.")
        

v = Util.crearVentana("Tobi GPS", "600x600")
boton = Util.agregarBarra(v, iconos, textoBoton)

main_frame = Frame(v, bg='#e6f7ff')  
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

tabla_frame = Frame(main_frame, bg='#e6f7ff')
tabla_frame.pack(side=TOP, fill=X, pady=10)

tabla_nombre_frame = Frame(tabla_frame, bg='#e6f7ff')
tabla_nombre_frame.pack(side=LEFT, fill=X, padx=10)
encabezado = ["Nombre"]
nombre = obtenerNombre()
tabla_nombre = Util.mostrarTabla(tabla_nombre_frame, encabezado, nombre)

tabla_nodos_frame = Frame(tabla_frame, bg='#e6f7ff')
tabla_nodos_frame.pack(side=LEFT, fill=X, padx=10)
encabezado_2 = ["Nodo 1", "Nodo 2", "Valor"]
nodos = obtenerNodos()
tabla_nodos = Util.mostrarTabla(tabla_nodos_frame, encabezado_2, nodos)

seleccion_frame = Frame(main_frame, bg='#e6f7ff')
seleccion_frame.pack(side=TOP, fill=X, pady=10)

origen_frame = Frame(seleccion_frame, bg='#e6f7ff')
origen_frame.pack(side=LEFT, padx=10)
Util.agregarEtiqueta(origen_frame, "Origen", 0, 0)
nombres_ciudades = ciudades()
ciudad_origen_lista = Util.agregarLista(origen_frame, nombres_ciudades, 1, 0)
destino_frame = Frame(seleccion_frame, bg='#e6f7ff')
destino_frame.pack(side=LEFT, padx=10)
Util.agregarEtiqueta(destino_frame, "Destino", 0, 0)
nombres_ciudades = ciudades()
ciudad_destino_lista = Util.agregarLista(destino_frame, nombres_ciudades, 1, 0)


recorrido_frame = Frame(seleccion_frame, bg='#e6f7ff')
recorrido_frame.pack(side=LEFT,fill=X, padx=10)
encabezado_recorrido = ["Nombre", "Valor"]
recorrido_data = []
tabla_distancia = Util.mostrarTabla(recorrido_frame, encabezado_recorrido, recorrido_data)
tabla_distancia.column("Nombre", width=90)
tabla_distancia.column("Valor", width=90)


boton[0].config(command=lambda: mostrar_distancia())

v.mainloop()