import traceback

import modulo1_procesos_hilos_planificacion as m1
import modulo2_sincronizacion as m2
import modulo3_memoria as m3


def menu_modulo1(procesos):
    while True:
        print("\n--- Módulo 1: Planificación, Hilos y Procesos ---")
        print("1. Ejecutar FCFS")
        print("2. Ejecutar SJF")
        print("3. Ejecutar Round Robin")
        print("4. Ejecutar Prioridad")
        print("5. Ver TODOS los algoritmos de planificación")
        print("6. Simular Hilos y Procesos (fork/exec)")
        print("0. Volver al menú principal")
        op = input("Selecciona una opción: ").strip()

        if op in ("1", "2", "3", "4"):
            m1.probar_algoritmo_individual(procesos, op)
        elif op == "5":
            m1.probar_algoritmos(procesos)
        elif op == "6":
            m1.demo_hilos(procesos)
            m1.demo_procesos()
        elif op == "0":
            return
        else:
            print("Opción no válida.")


def menu_modulo2():
    """Adapta el menú a las funciones disponibles en el archivo del módulo 2."""
    version_integral = (
        callable(getattr(m2, "demo_condicion_carrera", None))
        and callable(getattr(m2, "demo_productor_consumidor", None))
    )
    version_independiente = (
        callable(getattr(m2, "ejecutar_sin_sincronizacion", None))
        and callable(getattr(m2, "ejecutar_con_sincronizacion", None))
    )

    if version_integral:
        while True:
            print("\n--- Módulo 2: Sincronización y Exclusión Mutua ---")
            print("1. Condición de carrera SIN mutex")
            print("2. Contador CON mutex")
            print("3. Comparar ambas ejecuciones")
            print("4. Productor–Consumidor (carrito de libros)")
            print("0. Volver al menú principal")
            op = input("Selecciona una opción: ").strip()

            if op == "1":
                m2.demo_condicion_carrera(con_mutex=False)
            elif op == "2":
                m2.demo_condicion_carrera(con_mutex=True)
            elif op == "3":
                m2.demo_condicion_carrera(con_mutex=False)
                m2.demo_condicion_carrera(con_mutex=True)
            elif op == "4":
                m2.demo_productor_consumidor()
            elif op == "0":
                return
            else:
                print("Opción no válida.")

    elif version_independiente:
        while True:
            print("\n--- Módulo 2: Sincronización de Procesos ---")
            print("1. SIN sincronización (desborde y condición de carrera)")
            print("2. CON sincronización (productor–consumidor)")
            print("3. Ejecutar ambas demostraciones")
            print("0. Volver al menú principal")
            op = input("Selecciona una opción: ").strip()

            if op == "1":
                m2.ejecutar_sin_sincronizacion()
            elif op == "2":
                m2.ejecutar_con_sincronizacion()
            elif op == "3":
                m2.ejecutar_sin_sincronizacion()
                m2.ejecutar_con_sincronizacion()
            elif op == "0":
                return
            else:
                print("Opción no válida.")

    elif callable(getattr(m2, "ejecutar_modulo2", None)):
        
        while True:
            print("\n--- Módulo 2: Sincronización de Procesos ---")
            print("1. Ejecutar la simulación completa")
            print("0. Volver al menú principal")
            op = input("Selecciona una opción: ").strip()
            if op == "1":
                m2.ejecutar_modulo2()
            elif op == "0":
                return
            else:
                print("Opción no válida.")
    else:
        print("\nNo se reconocen las funciones del módulo 2.")
        print("Revisa que modulo2_sincronizacion.py esté junto a main.py.")
        print("Archivo cargado:", getattr(m2, "__file__", "desconocido"))


def menu_modulo3():
    while True:
        print("\n--- Módulo 3: Gestión de Memoria ---")
        print("1. Primer Ajuste (Asignación Contigua)")
        print("2. Mejor Ajuste (Asignación Contigua)")
        print("3. Peor Ajuste (Asignación Contigua)")
        print("4. Comparar las tres estrategias contiguas")
        print("5. Simulación de Paginación")
        print("6. Simulación de Segmentación")
        print("7. Reemplazo de Páginas (FIFO, LRU, Óptimo)")
        print("0. Volver al menú principal")
        op = input("Selecciona una opción: ").strip()

        if op == "1":
            m3.ejecutar_estrategia_contigua("primer")
        elif op == "2":
            m3.ejecutar_estrategia_contigua("mejor")
        elif op == "3":
            m3.ejecutar_estrategia_contigua("peor")
        elif op == "4":
            m3.demo_contigua()
        elif op == "5":
            m3.demo_paginacion()
        elif op == "6":
            m3.demo_segmentacion()
        elif op == "7":
            m3.demo_reemplazo()
        elif op == "0":
            return
        else:
            print("Opción no válida.")


def main():
    procesos = m1.procesos_biblioteca()
    while True:
        print("\n===== BiblioSim - Simulador de SO =====")
        print("1. Módulo 1: Planificación, Hilos y Procesos")
        print("2. Módulo 2: Sincronización y Exclusión Mutua")
        print("3. Módulo 3: Gestión de Memoria")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            menu_modulo1(procesos)
        elif opcion == "2":
            menu_modulo2()
        elif opcion == "3":
            menu_modulo3()
        elif opcion == "0":
            print("¡Hasta luego!")
            return
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        pass
    except KeyboardInterrupt:
        print("\nEjecución interrumpida.")
    except Exception:
        print("\nOcurrió un error. Detalles para identificarlo:")
        traceback.print_exc()
    finally:
        try:
            input("\nPresiona ENTER para cerrar la ventana...")
        except (EOFError, KeyboardInterrupt):
            pass