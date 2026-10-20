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

    print("\n--- CON SINCRONIZACION ---")
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
    input("\nSimulacion terminada. Presiona ENTER para cerrar...")
