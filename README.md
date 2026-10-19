# 📚 BiblioSim - Simulador de un Sistema Operativo

**BiblioSim** es un simulador educacional interactivo desarrollado en Python que modela los componentes fundamentales de un Sistema Operativo utilizando la metáfora del sistema de gestión, préstamos y almacén de una biblioteca universitaria. 

El proyecto fue diseñado como parte del trabajo práctico del curso **Sistemas Operativos (SW407)** de la **Universidad Nacional de Ingeniería (UNI)**, cubriendo los requerimientos teóricos y prácticos de gestión de procesos, sincronización y administración de memoria.

---

## Propósito del Proyecto

El objetivo principal de BiblioSim es llevar la teoría de los sistemas operativos a la práctica mediante código ejecutable, permitiendo analizar métricas de rendimiento, comparar algoritmos clásicos de planificación y reemplazo, y visualizar fenómenos como las condiciones de carrera y la fragmentación de memoria en tiempo real.

---

## Funcionalidades Principales

El simulador está organizado en **tres módulos principales**:

### 1. Módulo 1: Planificación de CPU y Concurrencia
* **Algoritmos de Planificación:** Simulación y métricas detalladas (espera, respuesta y retorno) para **FCFS**, **SJF**, **Round Robin** y **Prioridades**.
* **Concurrencia:** Modelado de hilos mediante `threading` y creación de procesos hijo utilizando llamadas del sistema (`fork`/`exec` o `subprocess`).

### 2. Módulo 2: Sincronización y Exclusión Mutua
* **Condición de Carrera:** Demostración de solapamiento de hilos y su resolución mediante cerrojos (`Lock` / Mutex).
* **Productor-Consumidor:** Simulación del problema del búfer acotado (carrito de reposición de libros) utilizando **semáforos** (`threading.Semaphore`) para coordinar la entrega entre profesores y encargados.

### 3. Módulo 3: Gestión de Memoria y Memoria Virtual
* **Asignación Contigua y Fragmentación:** Implementación y comparación de las estrategias **Primer Ajuste (First-Fit)**, **Mejor Ajuste (Best-Fit)** y **Peor Ajuste (Worst-Fit)** con cálculo de fragmentación interna y externa.
* **Paginación:** División en páginas/marcos de tamaño fijo, generación de tablas de páginas y traducción de direcciones lógicas a físicas.
* **Segmentación:** Organización en zonas lógicas con protección por base y límite.
* **Algoritmos de Reemplazo de Páginas:** Evaluación paso a paso y recuento de fallos de página para **FIFO**, **LRU** y el **Óptimo**.

---
