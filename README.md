# 🎮 Optimizador de SKlauncher

> Herramienta en Python para optimizar y ejecutar el launcher de Minecraft [SKlauncher] con la mejor configuración según tu sistema.

## 🚀 Características

- Detección automática de RAM y CPU.
- Configuración dinámica de parámetros JVM según la versión de Java (8, 11, 17, 21).
- Parámetros avanzados de rendimiento y Garbage Collection (G1GC).
- Generación automática de archivo `.bat` para ejecución directa en Windows.
- Diagnóstico con salida completa y modo debug.
- Interfaz interactiva en consola.

---

## 📦 Requisitos

- **Sistema operativo:** Windows 10/11
- **Python:** 3.6 o superior
- **Dependencias:** Se instalan automáticamente si usas `pip install -r requirements.txt`

```bash
pip install psutil
