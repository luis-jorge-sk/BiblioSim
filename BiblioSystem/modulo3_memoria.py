import math

UNIDAD = 4
TOTAL_MEMORIA = 120


class MemoriaContigua:
    def __init__(self, total):
        self.total = total
        self.bloques = [[0, total, None, 0]]

    def asignar(self, pid, pedido, estrategia):
        if pedido <= 0:
            raise ValueError("El tamaño pedido debe ser mayor que 0")
        tam = math.ceil(pedido / UNIDAD) * UNIDAD
        huecos = [b for b in self.bloques if b[2] is None and b[1] >= tam]
        if not huecos:
            return None

        if estrategia == "primer":
            hueco = huecos[0]
        elif estrategia == "mejor":
            hueco = min(huecos, key=lambda b: b[1])
        elif estrategia == "peor":
            hueco = max(huecos, key=lambda b: b[1])
        else:
            raise ValueError("Estrategia no válida")

        indice = self.bloques.index(hueco)
        inicio = hueco[0]
        sobra = hueco[1] - tam
        self.bloques[indice] = [inicio, tam, pid, pedido]
        if sobra > 0:
            self.bloques.insert(indice + 1, [inicio + tam, sobra, None, 0])
        return inicio

    def liberar(self, pid):
        for bloque in self.bloques:
            if bloque[2] == pid:
                bloque[2] = None
                bloque[3] = 0
                self.unir_huecos()
                return True
        return False

    def unir_huecos(self):
        i = 0
        while i < len(self.bloques) - 1:
            actual = self.bloques[i]
            siguiente = self.bloques[i + 1]
            if actual[2] is None and siguiente[2] is None:
                actual[1] += siguiente[1]
                self.bloques.pop(i + 1)
            else:
                i += 1

    def fragmentacion_externa(self):
        huecos = [b[1] for b in self.bloques if b[2] is None]
        if len(huecos) <= 1:
            return 0
        return sum(huecos) - max(huecos)

    def fragmentacion_interna(self):
        return sum(b[1] - b[3] for b in self.bloques if b[2] is not None)

    def mostrar(self):
        partes = []
        for inicio, tam, pid, pedido in self.bloques:
            nombre = pid if pid else "libre"
            partes.append(f"[{inicio}-{inicio + tam - 1} {nombre}]")
        print(" ".join(partes))


OPERACIONES = [
    ("A", "P1", 8), ("A", "P2", 16), ("A", "P3", 8), ("A", "P4", 12),
    ("A", "P5", 8), ("A", "P6", 20), ("A", "P7", 8),
    ("L", "P2"), ("L", "P4"), ("L", "P6"),
    ("A", "P8", 12), ("A", "P9", 18), ("A", "P10", 16), ("A", "P11", 30),
]


def ejecutar_estrategia_contigua(estrategia):
    memoria = MemoriaContigua(TOTAL_MEMORIA)
    fallidas = []
    for op in OPERACIONES:
        if op[0] == "A":
            if memoria.asignar(op[1], op[2], estrategia) is None:
                fallidas.append(op[1])
        else:
            memoria.liberar(op[1])

    print(f"\n=== Estrategia: {estrategia.upper()} AJUSTE ===")
    memoria.mostrar()
    externa = memoria.fragmentacion_externa()
    interna = memoria.fragmentacion_interna()
    print(f"Fragmentación externa: {externa} | interna: {interna} | Sin espacio para: {fallidas}")


def demo_contigua():
    print("\n--- Comparativa de Estrategias de Asignación Contigua ---")
    for est in ("primer", "mejor", "peor"):
        ejecutar_estrategia_contigua(est)


# ---------- Parte B: paginación ----------

class MemoriaPaginada:
    def __init__(self, num_marcos, tam_pagina):
        self.tam_pagina = tam_pagina
        self.marcos = [None] * num_marcos
        self.tablas = {}
        self.tamanos = {}

    def cargar(self, pid, tamano):
        paginas = math.ceil(tamano / self.tam_pagina)
        libres = [i for i, m in enumerate(self.marcos) if m is None]
        if len(libres) < paginas:
            return False
        tabla = {}
        for pagina in range(paginas):
            marco = libres[pagina]
            self.marcos[marco] = (pid, pagina)
            tabla[pagina] = marco
        self.tablas[pid] = tabla
        self.tamanos[pid] = tamano
        return True

    def liberar(self, pid):
        if pid not in self.tablas:
            return False
        for marco in self.tablas[pid].values():
            self.marcos[marco] = None
        del self.tablas[pid]
        del self.tamanos[pid]
        return True

    def traducir(self, pid, direccion_logica):
        if pid not in self.tablas:
            raise ValueError(f"El proceso {pid} no está cargado")
        if direccion_logica < 0 or direccion_logica >= self.tamanos[pid]:
            raise ValueError(f"Dirección {direccion_logica} fuera de límites")
        pagina = direccion_logica // self.tam_pagina
        desplazamiento = direccion_logica % self.tam_pagina
        marco = self.tablas[pid][pagina]
        return marco * self.tam_pagina + desplazamiento

    def mostrar(self):
        for pid, tabla in self.tablas.items():
            print(f"Tabla de páginas de {pid}: {tabla}")
        print("Estado de Marcos:", [m[0] if m else "libre" for m in self.marcos])


def demo_paginacion():
    print("\n--- Simulación de Paginación ---")
    memoria = MemoriaPaginada(num_marcos=8, tam_pagina=4)
    memoria.cargar("S1", 10)
    memoria.cargar("S2", 14)
    memoria.liberar("S1")
    memoria.cargar("S3", 16)
    memoria.mostrar()

    for pid, direccion in [("S3", 13), ("S2", 5)]:
        fisica = memoria.traducir(pid, direccion)
        pagina, desp = direccion // 4, direccion % 4
        print(f"{pid}: dir_lógica {direccion} -> Pág {pagina}, Desplazamiento {desp} -> Dir_física {fisica}")


# ---------- Parte C: segmentación ----------

class ErrorSegmentacion(Exception):
    pass


class MemoriaSegmentada:
    def __init__(self, total):
        self.memoria = MemoriaContigua(total)
        self.tablas = {}

    def cargar(self, pid, segmentos, estrategia="primer"):
        tabla = {}
        for nombre, tam in segmentos.items():
            base = self.memoria.asignar(f"{pid}-{nombre}", tam, estrategia)
            if base is None:
                for anterior in tabla:
                    self.memoria.liberar(f"{pid}-{anterior}")
                return False
            tabla[nombre] = (base, tam)
        self.tablas[pid] = tabla
        return True

    def traducir(self, pid, segmento, desplazamiento):
        if pid not in self.tablas or segmento not in self.tablas[pid]:
            raise ErrorSegmentacion(f"Segmento {segmento} de {pid} no existe")
        base, limite = self.tablas[pid][segmento]
        if desplazamiento < 0 or desplazamiento >= limite:
            raise ErrorSegmentacion(f"Fallo de Segmentación: desplazamiento {desplazamiento} >= límite {limite}")
        return base + desplazamiento

    def mostrar(self):
        for pid, tabla in self.tablas.items():
            print(f"Tabla de segmentos de {pid}:")
            for nombre, (base, limite) in tabla.items():
                print(f"   {nombre:<11} Base={base:<4} Límite={limite}")


def demo_segmentacion():
    print("\n--- Simulación de Segmentación ---")
    memoria = MemoriaSegmentada(64)
    memoria.cargar("S1", {"novelas": 20, "ciencia": 12, "referencia": 8})
    memoria.cargar("S2", {"novelas": 10, "ciencia": 6})
    memoria.mostrar()

    print("Dir. física (S1, ciencia, 5):", memoria.traducir("S1", "ciencia", 5))
    print("Dir. física (S2, novelas, 3):", memoria.traducir("S2", "novelas", 3))


# ---------- Parte D: reemplazo de páginas ----------

def paso(pagina, memoria, fallo):
    marca = "FALLO" if fallo else "OK"
    print(f"   página {pagina} -> {memoria} {marca}")


def fifo(referencias, marcos, mostrar=False):
    memoria = []
    fallos = 0
    for pagina in referencias:
        fallo = pagina not in memoria
        if fallo:
            fallos += 1
            if len(memoria) == marcos:
                memoria.pop(0)
            memoria.append(pagina)
        if mostrar:
            paso(pagina, memoria, fallo)
    return fallos


def lru(referencias, marcos, mostrar=False):
    memoria = []
    fallos = 0
    for pagina in referencias:
        fallo = pagina not in memoria
        if fallo:
            fallos += 1
            if len(memoria) == marcos:
                memoria.pop(0)
        else:
            memoria.remove(pagina)
        memoria.append(pagina)
        if mostrar:
            paso(pagina, memoria, fallo)
    return fallos


def optimo(referencias, marcos, mostrar=False):
    memoria = []
    fallos = 0
    for i, pagina in enumerate(referencias):
        fallo = pagina not in memoria
        if fallo:
            fallos += 1
            if len(memoria) < marcos:
                memoria.append(pagina)
            else:
                futuras = referencias[i + 1:]
                victima = None
                mas_lejos = -1
                for p in memoria:
                    if p in futuras:
                        distancia = futuras.index(p)
                    else:
                        distancia = len(futuras) + 1
                    if distancia > mas_lejos:
                        mas_lejos = distancia
                        victima = p
                memoria[memoria.index(victima)] = pagina
        if mostrar:
            paso(pagina, memoria, fallo)
    return fallos


def demo_reemplazo():
    print("\n--- Reemplazo de Páginas ---")
    referencias = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    marcos = 3
    print(f"Cadena de referencia: {referencias}")
    print(f"Marcos disponibles: {marcos}")
    print(f"FIFO:   {fifo(referencias, marcos)} fallos")
    print(f"LRU:    {lru(referencias, marcos)} fallos")
    print(f"Óptimo: {optimo(referencias, marcos)} fallos")