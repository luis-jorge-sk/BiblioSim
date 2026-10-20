import unittest

import modulo1_procesos_hilos_planificacion as m1
import modulo2_sincronizacion as m2
import modulo3_memoria as m3


def promedio_espera(procesos):
    return sum(p.espera for p in procesos) / len(procesos)


class Pruebas(unittest.TestCase):

    # --- Pruebas del Módulo 1 ---
    def test_fcfs(self):
        gantt, terminados = m1.ejecutar_fcfs(m1.procesos_biblioteca())
        self.assertEqual([g[0] for g in gantt], ["S1", "S2", "S3", "S4", "S5"])
        self.assertAlmostEqual(promedio_espera(terminados), 11.4)

    def test_sjf(self):
        gantt, terminados = m1.ejecutar_sjf(m1.procesos_biblioteca())
        self.assertEqual([g[0] for g in gantt], ["S1", "S5", "S2", "S4", "S3"])
        self.assertAlmostEqual(promedio_espera(terminados), 8.2)

    # --- Pruebas del Módulo 2 ---
    def test_mutex(self):
        esperado = 4 * 20
        # Sin mutex debe haber una pérdida de actualizaciones por condición de carrera
        self.assertLess(m2.probar(m2.reponer_sin_mutex, 4, 20), esperado)
        # Con mutex debe dar el valor exacto esperado
        self.assertEqual(m2.probar(m2.reponer_con_mutex, 4, 20), esperado)

    # --- Pruebas del Módulo 3 ---
    def test_fragmentacion(self):
        mem = m3.MemoriaContigua(40)
        mem.asignar("A", 10, "primer")
        mem.asignar("B", 10, "primer")
        mem.asignar("C", 10, "primer")
        mem.liberar("B")
        self.assertEqual(mem.fragmentacion_externa(), 4)
        self.assertIsNone(mem.asignar("D", 16, "primer"))  # Hay espacio libre total, pero no contiguo

    def test_reemplazo_paginas(self):
        refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
        self.assertEqual(m3.fifo(refs, 3), 15)
        self.assertEqual(m3.lru(refs, 3), 12)
        self.assertEqual(m3.optimo(refs, 3), 9)


if __name__ == "__main__":
    unittest.main()