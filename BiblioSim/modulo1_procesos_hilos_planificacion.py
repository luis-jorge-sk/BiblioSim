import copy
import os
import subprocess
import sys
import threading
import time


# ---------- Procesos ----------

class Proceso:
    """Una solicitud de préstamo de la biblioteca (un proceso del SO)."""

    def __init__(self, pid, llegada, rafaga, prioridad=0):
        if rafaga <= 0:
            raise ValueError("La ráfaga debe ser mayor que 0")
        if llegada < 0:
            raise ValueError("La llegada no puede ser negativa")
        self.pid = pid
        self.llegada = llegada
        self.rafaga = rafaga
        self.prioridad = prioridad  # menor número = mayor prioridad
        self.restante = rafaga
        self.inicio = None          # primer instante en que usa la CPU
        self.fin = None
        self.espera = 0
        self.respuesta = 0
        self.retorno = 0

    def calcular_metricas(self):
        self.retorno = self.fin - self.llegada
        self.espera = self.retorno - self.rafaga
        self.respuesta = self.inicio - self.llegada


def procesos_biblioteca():
    """Datos de ejemplo: solicitudes que llegan al bibliotecario.
    Prioridad: 1 = docente, 2 = estudiante de último ciclo, 3 = estudiante regular."""
    return [
        Proceso("S1", 0, 8, 3),
        Proceso("S2", 1, 4, 1),
        Proceso("S3", 2, 9, 3),
        Proceso("S4", 3, 5, 2),
        Proceso("S5", 4, 2, 2),
    ]


# ---------- Planificador ----------

def ejecutar_fcfs(procesos):
    ordenados = sorted(copy.deepcopy(procesos), key=lambda p: p.llegada)
    tiempo_actual = 0
    gantt = []

    for proceso in ordenados:
        if tiempo_actual < proceso.llegada:
            tiempo_actual = proceso.llegada

        proceso.inicio = tiempo_actual
        proceso.fin = tiempo_actual + proceso.rafaga
        tiempo_actual = proceso.fin

        proceso.calcular_metricas()
        gantt.append((proceso.pid, proceso.inicio, proceso.fin))

    return gantt, ordenados


def ejecutar_sjf(procesos):
    pendientes = copy.deepcopy(procesos)
    terminados = []
    gantt = []
    tiempo_actual = 0

    while pendientes:
        listos = [p for p in pendientes if p.llegada <= tiempo_actual]
        if not listos:
            tiempo_actual = min(p.llegada for p in pendientes)
            continue

        proceso = min(listos, key=lambda p: p.rafaga)
        proceso.inicio = tiempo_actual
        proceso.fin = tiempo_actual + proceso.rafaga
        tiempo_actual = proceso.fin

        proceso.calcular_metricas()
        gantt.append((proceso.pid, proceso.inicio, proceso.fin))
        pendientes.remove(proceso)
        terminados.append(proceso)

    return gantt, terminados


def ejecutar_prioridad(procesos):
    pendientes = copy.deepcopy(procesos)
    terminados = []
    gantt = []
    tiempo_actual = 0

    while pendientes:
        listos = [p for p in pendientes if p.llegada <= tiempo_actual]
        if not listos:
            tiempo_actual = min(p.llegada for p in pendientes)
            continue

        proceso = min(listos, key=lambda p: (p.prioridad, p.llegada))
        proceso.inicio = tiempo_actual
        proceso.fin = tiempo_actual + proceso.rafaga
        tiempo_actual = proceso.fin

        proceso.calcular_metricas()
        gantt.append((proceso.pid, proceso.inicio, proceso.fin))
        pendientes.remove(proceso)
        terminados.append(proceso)

    return gantt, terminados


def round_robin(procesos, quantum):
    if quantum <= 0:
        raise ValueError("El quantum debe ser mayor que 0")

    todos = sorted(copy.deepcopy(procesos), key=lambda p: p.llegada)
    cola = []
    terminados = []
    gantt = []
    tiempo = 0
    i = 0

    while len(terminados) < len(todos):
        while i < len(todos) and todos[i].llegada <= tiempo:
            cola.append(todos[i])
            i += 1
        if not cola:
            tiempo = todos[i].llegada
            continue

        actual = cola.pop(0)
        if actual.inicio is None:
            actual.inicio = tiempo
        ejecutar = min(quantum, actual.restante)
        gantt.append((actual.pid, tiempo, tiempo + ejecutar))
        tiempo += ejecutar
        actual.restante -= ejecutar

        while i < len(todos) and todos[i].llegada <= tiempo:
            cola.append(todos[i])
            i += 1

        if actual.restante > 0:
            cola.append(actual)
        else:
            actual.fin = tiempo
            actual.calcular_metricas()
            terminados.append(actual)

    return gantt, terminados


# ---------- Resultados ----------

def mostrar_resultados(nombre, gantt, procesos):
    print(f"\n=== {nombre} ===")
    print("Gantt: " + " ".join(f"[{pid} {ini}-{fin}]" for pid, ini, fin in gantt))
    print(f"{'PID':<6}{'Llegada':<9}{'Ráfaga':<8}{'Espera':<8}{'Respuesta':<11}{'Retorno':<8}")
    for p in sorted(procesos, key=lambda p: p.pid):
        print(f"{p.pid:<6}{p.llegada:<9}{p.rafaga:<8}{p.espera:<8}{p.respuesta:<11}{p.retorno:<8}")

    n = len(procesos)
    prom_espera = sum(p.espera for p in procesos) / n
    prom_respuesta = sum(p.respuesta for p in procesos) / n
    prom_retorno = sum(p.retorno for p in procesos) / n
    print(f"Promedios -> espera: {prom_espera:.2f} | respuesta: {prom_respuesta:.2f} | retorno: {prom_retorno:.2f}")


def probar_algoritmos(procesos, quantum=3):
    resultados = [
        ("FCFS", ejecutar_fcfs(procesos)),
        ("SJF", ejecutar_sjf(procesos)),
        (f"Round Robin (q={quantum})", round_robin(procesos, quantum)),
        ("Prioridad", ejecutar_prioridad(procesos)),
    ]
    for nombre, (gantt, terminados) in resultados:
        mostrar_resultados(nombre, gantt, terminados)


def probar_algoritmo_individual(procesos, opcion, quantum=3):
    if opcion == "1":
        gantt, terminados = ejecutar_fcfs(procesos)
        mostrar_resultados("FCFS (First-Come, First-Served)", gantt, terminados)
    elif opcion == "2":
        gantt, terminados = ejecutar_sjf(procesos)
        mostrar_resultados("SJF (Shortest Job First)", gantt, terminados)
    elif opcion == "3":
        gantt, terminados = round_robin(procesos, quantum)
        mostrar_resultados(f"Round Robin (Quantum = {quantum})", gantt, terminados)
    elif opcion == "4":
        gantt, terminados = ejecutar_prioridad(procesos)
        mostrar_resultados("Prioridad", gantt, terminados)


# ---------- Hilos y procesos ----------

def tarea(nombre, duracion):
    for i in range(duracion):
        print(f"{nombre}: ejecutando {i + 1}/{duracion}")
        time.sleep(0.1)


def demo_hilos(procesos):
    print("\n--- Demo de hilos (threading) ---")
    hilos = []
    for p in procesos:
        hilo = threading.Thread(target=tarea, args=(p.pid, min(p.rafaga, 3)))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()
    print("Todos los hilos terminaron")


def demo_procesos():
    print("\n--- Demo de procesos (fork/exec) ---")
    if hasattr(os, "fork"):
        sys.stdout.flush()
        pid_hijo = os.fork()
        if pid_hijo == 0:
            os.execvp("echo", ["echo", "Hijo: atendiendo solicitud de préstamo"])
        else:
            os.waitpid(pid_hijo, 0)
            print(f"Padre: el proceso hijo {pid_hijo} terminó")
    else:
        subprocess.run(["cmd", "/c", "echo Hijo: atendiendo solicitud de préstamo"])
        print("Padre: el proceso hijo terminó")