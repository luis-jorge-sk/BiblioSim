"""BiblioSim - Modulo 2: sincronizacion de procesos"""

import random
import threading
import time

CAPACIDAD = 3


carrito = []
mutex = threading.Lock()
vacios = threading.Semaphore(CAPACIDAD)
llenos = threading.Semaphore(0)
depositados = []
retirados = []


def usuario(nombre, cantidad):
    """Productor: devuelve libros al carrito."""
    for i in range(cantidad):
        libro = f"libro{i + 1} de {nombre}"
        vacios.acquire()  # Espera un espacio libre.
        with mutex:       # Solo un hilo modifica el carrito a la vez.
            carrito.append(libro)
            depositados.append(libro)
            print(f"{nombre} deposita {libro} | En carrito: {len(carrito)}/{CAPACIDAD}")
        llenos.release()   # Avisa que hay otro libro disponible.


def bibliotecario(nombre, cantidad):
    """Consumidor: retira libros del carrito."""
    for _ in range(cantidad):
        llenos.acquire()  # Espera hasta que haya un libro.
        with mutex:
            libro = carrito.pop(0)
            retirados.append(libro)
            print(f"{nombre} retira {libro} | En carrito: {len(carrito)}/{CAPACIDAD}")
        vacios.release()   # Libera un espacio en el carrito.
        time.sleep(random.uniform(0.1, 0.3))


def ejecutar_sin_sincronizacion():
    print("\n--- SIN SINCRONIZACION ---")
    carrito_sin_control = []

    def devolver_sin_control(nombre, cantidad):
        for i in range(cantidad):
            carrito_sin_control.append(f"libro{i + 1} de {nombre}")

    productores = [
        threading.Thread(target=devolver_sin_control, args=("Usuario A", 5)),
        threading.Thread(target=devolver_sin_control, args=("Usuario B", 5)),
    ]
    for hilo in productores:
        hilo.start()
    for hilo in productores:
        hilo.join()
    print(f"Sin control de cupos: {len(carrito_sin_control)}/{CAPACIDAD} libros (desborde)")

    # Forzamos una pausa entre leer y escribir para ilustrar una condicion de carrera.
    contador = 0

    def contar_sin_mutex():
        nonlocal contador
        for _ in range(50):
            valor_anterior = contador
            time.sleep(0.0001)
            contador = valor_anterior + 1

    trabajadores = [threading.Thread(target=contar_sin_mutex) for _ in range(4)]
    for hilo in trabajadores:
        hilo.start()
    for hilo in trabajadores:
        hilo.join()
    print(f"Contador sin mutex: {contador} (esperado: 200; resultado variable)")


def ejecutar_con_sincronizacion():
    """Ejecuta dos productores y dos consumidores, con capacidad maxima de 3."""
    global carrito, mutex, vacios, llenos, depositados, retirados
    carrito = []
    mutex = threading.Lock()
    vacios = threading.Semaphore(CAPACIDAD)
    llenos = threading.Semaphore(0)
    depositados = []
    retirados = []

    print("\n CON SINCRONIZACION ")
    hilos = [
        threading.Thread(target=usuario, args=("Usuario A", 5)),
        threading.Thread(target=usuario, args=("Usuario B", 5)),
        threading.Thread(target=bibliotecario, args=("Encargado 1", 5)),
        threading.Thread(target=bibliotecario, args=("Encargado 2", 5)),
    ]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()

    print(f"\nDepositados: {len(depositados)} | Retirados: {len(retirados)}")
    print(f"Carrito al terminar: {len(carrito)} libros")
    print("Todos los libros se retiraron una sola vez:",
          len(depositados) == len(retirados) == 10 and
          sorted(depositados) == sorted(retirados))


def ejecutar_modulo2():
    ejecutar_sin_sincronizacion()
    ejecutar_con_sincronizacion()


if __name__ == "__main__":
    ejecutar_modulo2()
