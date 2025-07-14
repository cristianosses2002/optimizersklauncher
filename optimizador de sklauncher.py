#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimizador de SKlauncher - Mejora el rendimiento del launcher de Minecraft
Autor: Asistente IA
Fecha: 2025
"""

import os
import sys
import subprocess
import psutil
import platform
from pathlib import Path

class SKlauncherOptimizer:
    def __init__(self):
        self.java_path = r"C:\Users\osses\AppData\Roaming\sklauncher\jre\bin\javaw.exe"
        self.jar_path = r"C:\Users\osses\AppData\Roaming\sklauncher\SKlauncher.jar"
        self.system_ram_gb = round(psutil.virtual_memory().total / (1024**3))
        
    def verificar_archivos(self):
        """Verifica que los archivos necesarios existan"""
        if not os.path.exists(self.java_path):
            print(f"❌ Error: No se encontró Java en {self.java_path}")
            return False
            
        if not os.path.exists(self.jar_path):
            print(f"❌ Error: No se encontró SKlauncher en {self.jar_path}")
            return False
            
        print("✅ Archivos verificados correctamente")
        return True
    
    def calcular_memoria_optima(self):
        """Calcula la cantidad óptima de RAM para asignar"""
        # Reservamos RAM para el sistema operativo y otros procesos
        if self.system_ram_gb <= 4:
            ram_asignada = min(1024, self.system_ram_gb * 256)  # 1GB máximo
        elif self.system_ram_gb <= 8:
            ram_asignada = 2048  # 2GB
        elif self.system_ram_gb <= 16:
            ram_asignada = 4096  # 4GB
        else:
            ram_asignada = 6144  # 6GB para sistemas con más de 16GB
            
        return ram_asignada
    
    def detectar_version_java(self):
        """Detecta la versión de Java para usar parámetros compatibles"""
        try:
            resultado = subprocess.run(
                [self.java_path, "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Extraer número de versión principal
            version_text = resultado.stderr if resultado.stderr else resultado.stdout
            if "21." in version_text:
                return 21
            elif "17." in version_text:
                return 17
            elif "11." in version_text:
                return 11
            elif "1.8" in version_text:
                return 8
            else:
                return 21  # Asumir versión moderna por defecto
        except:
            return 21  # Asumir versión moderna por defecto

    def obtener_parametros_optimizados(self):
        """Genera los parámetros JVM optimizados según la versión de Java"""
        ram_mb = self.calcular_memoria_optima()
        java_version = self.detectar_version_java()
        
        # Parámetros básicos de memoria (compatibles con todas las versiones)
        params = [
            self.java_path,
            f"-Xmx{ram_mb}M",  # Memoria máxima
            f"-Xms{ram_mb//2}M",  # Memoria inicial (50% del máximo)
        ]
        
        # Parámetros según la versión de Java
        if java_version >= 17:
            # Java 17+ (incluye Java 21) - Parámetros conservadores y estables
            params.extend([
                "-XX:+UseG1GC",  # G1 Garbage Collector
                "-XX:MaxGCPauseMillis=50",  # Pausa máxima de GC
                "-XX:+UseStringDeduplication",  # Deduplicación de strings
                "-XX:+ParallelRefProcEnabled",  # Procesamiento paralelo de referencias
                "-XX:+UseCompressedOops",  # Punteros comprimidos
                "-XX:+UseCompressedClassPointers",  # Punteros de clase comprimidos
            ])
        elif java_version >= 11:
            # Java 11-16 - Con parámetros experimentales habilitados
            params.extend([
                "-XX:+UnlockExperimentalVMOptions",  # Debe ir ANTES de los parámetros experimentales
                "-XX:+UseG1GC",
                "-XX:G1NewSizePercent=20",
                "-XX:G1ReservePercent=20",
                "-XX:MaxGCPauseMillis=50",
                "-XX:G1HeapRegionSize=32M",
                "-XX:+UseStringDeduplication",
                "-XX:+UseFastAccessorMethods",
                "-XX:+OptimizeStringConcat",
            ])
        else:
            # Java 8 y anteriores
            params.extend([
                "-XX:+UnlockExperimentalVMOptions",
                "-XX:+UseG1GC",
                "-XX:G1NewSizePercent=20",
                "-XX:G1ReservePercent=20",
                "-XX:MaxGCPauseMillis=50",
                "-XX:G1HeapRegionSize=32M",
                "-XX:+UseFastAccessorMethods",
                "-XX:+OptimizeStringConcat",
                "-XX:+AggressiveOpts",
                "-XX:+UseBiasedLocking",
            ])
        
        # Parámetros universales (compatibles con todas las versiones)
        params.extend([
            "-Dfml.ignorePatchDiscrepancies=true",
            "-Dfml.ignoreInvalidMinecraftCertificates=true",
            "-Djava.net.preferIPv4Stack=true",
            "-Dfile.encoding=UTF-8",
        ])
        
        # Parámetros específicos para Windows
        if platform.system() == "Windows":
            params.extend([
                "-Dsun.stdout.encoding=UTF-8",
                "-Dsun.stderr.encoding=UTF-8",
            ])
        
        # Jar del launcher
        params.extend(["-jar", self.jar_path])
        
        return params, ram_mb, java_version
    
    def mostrar_informacion_sistema(self):
        """Muestra información del sistema"""
        print("=" * 50)
        print("INFORMACIÓN DEL SISTEMA")
        print("=" * 50)
        print(f"Sistema Operativo: {platform.system()} {platform.release()}")
        print(f"Arquitectura: {platform.architecture()[0]}")
        print(f"RAM Total: {self.system_ram_gb} GB")
        print(f"RAM Disponible: {round(psutil.virtual_memory().available / (1024**3), 2)} GB")
        print(f"CPU: {platform.processor()}")
        print(f"Núcleos: {psutil.cpu_count()}")
        print()
    
    def ejecutar_optimizado(self, mostrar_comando=True):
        """Ejecuta SKlauncher con parámetros optimizados"""
        if not self.verificar_archivos():
            return False
            
        params, ram_asignada, java_version = self.obtener_parametros_optimizados()
        
        self.mostrar_informacion_sistema()
        print("CONFIGURACIÓN OPTIMIZADA")
        print("=" * 50)
        print(f"Versión de Java: {java_version}")
        print(f"RAM Asignada: {ram_asignada} MB ({ram_asignada/1024:.1f} GB)")
        print(f"Garbage Collector: G1GC")
        print(f"Optimizaciones: Activadas (compatibles con Java {java_version})")
        print()
        if mostrar_comando:
            print("COMANDO COMPLETO:")
            print("=" * 50)
            comando_str = " ".join(f'"{param}"' if " " in param else param for param in params)
            print(comando_str)
            print()
        try:
            print("Iniciando SKlauncher optimizado...")
            print("=" * 50)
            proceso = subprocess.Popen(
                params,
                cwd=os.path.dirname(self.jar_path)
            )
            print(f"SKlauncher iniciado (PID: {proceso.pid})")
            print("Esperando a que se abra la ventana...")
            import time
            time.sleep(3)
            if proceso.poll() is None:
                print("SKlauncher se está ejecutando correctamente")
                print("Si no ves la ventana, revisa la barra de tareas")
            else:
                print("SKlauncher se cerró inesperadamente")
                print("Revisando errores...")
                try:
                    stdout, stderr = proceso.communicate(timeout=5)
                    if stderr:
                        print(f"Error capturado: {stderr.decode('utf-8', errors='ignore')}")
                except:
                    pass
                return False
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar SKlauncher: {e}")
            return False
        except KeyboardInterrupt:
            print("\nProceso interrumpido por el usuario")
            return False
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False
    
    def ejecutar_con_debug(self):
        """Ejecuta SKlauncher con información de debug detallada"""
        if not self.verificar_archivos():
            return False
            
        params, ram_asignada, java_version = self.obtener_parametros_optimizados()
        
        print("MODO DEBUG - DIAGNÓSTICO COMPLETO")
        print("=" * 50)
        
        # Verificar versión de Java
        try:
            java_version_output = subprocess.run(
                [self.java_path, "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            print(f"Java encontrado: Versión {java_version}")
            print(f"Parámetros optimizados para Java {java_version}")
        except Exception as e:
            print(f"❌ Error al verificar Java: {e}")
            return False
        
        # Verificar permisos del archivo JAR
        jar_size = os.path.getsize(self.jar_path) / (1024*1024)
        print(f"Tamaño del JAR: {jar_size:.1f} MB")
        
        # Intentar ejecución con salida visible
        print("\nEjecutando con salida completa...")
        print("=" * 50)
        
        try:
            # Cambiar al directorio del launcher
            os.chdir(os.path.dirname(self.jar_path))
            
            # Ejecutar con salida visible
            resultado = subprocess.run(
                params,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print(f"Código de salida: {resultado.returncode}")
            
            if resultado.stdout:
                print("\nSALIDA ESTÁNDAR:")
                print(resultado.stdout)
            
            if resultado.stderr:
                print("\nERRORES/ADVERTENCIAS:")
                print(resultado.stderr)
            
            if resultado.returncode == 0:
                print("\nEl comando se ejecutó sin errores")
            else:
                print(f"\nEl comando falló con código: {resultado.returncode}")
                
        except subprocess.TimeoutExpired:
            print("El proceso tardó más de 30 segundos, puede estar funcionando")
        except Exception as e:
            print(f"Error durante la ejecución: {e}")
            
        return True

    def generar_bat(self):
        """Genera un archivo .bat para Windows con la configuración optimizada"""
        params, ram_asignada, _ = self.obtener_parametros_optimizados()
        bat_content = f"""@echo off
        title SKlauncher Optimizado - {ram_asignada}MB RAM
        echo ======================================
        echo    SKlauncher Optimizado
        echo    RAM Asignada: {ram_asignada}MB
        echo ======================================
        echo.
        echo Iniciando SKlauncher...
        echo.
        cd /d \"C:\\Users\\osses\\AppData\\Roaming\\sklauncher\"
        \"{self.java_path}\" {' '.join(params[1:])}
        if errorlevel 1 (
            echo.
            echo Error al iniciar SKlauncher
            pause
        ) else (
            echo.
            echo SKlauncher cerrado correctamente
        )
        """
        bat_path = "sklauncher_optimizado.bat"
        try:
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            print(f"Archivo .bat generado: {os.path.abspath(bat_path)}")
            print("Puedes usar este archivo para iniciar SKlauncher optimizado")
            return True
        except Exception as e:
            print(f"Error al generar archivo .bat: {e}")
            return False

def main():
    """Función principal"""
    print("OPTIMIZADOR DE SKLAUNCHER")
    print("=" * 50)
    
    optimizer = SKlauncherOptimizer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--generar-bat":
            optimizer.generar_bat()
            return
        elif sys.argv[1] == "--info":
            optimizer.mostrar_informacion_sistema()
            return
    
    print("Opciones disponibles:")
    print("1. Ejecutar SKlauncher optimizado")
    print("2. Generar archivo .bat optimizado")
    print("3. Mostrar información del sistema")
    print("4. Ejecutar con diagnóstico completo (DEBUG)")
    print("5. Salir")
    print()
    
    while True:
        try:
            opcion = input("Selecciona una opción (1-5): ").strip()
            
            if opcion == "1":
                optimizer.ejecutar_optimizado()
                break
            elif opcion == "2":
                optimizer.generar_bat()
                break
            elif opcion == "3":
                optimizer.mostrar_informacion_sistema()
            elif opcion == "4":
                optimizer.ejecutar_con_debug()
                break
            elif opcion == "5":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Por favor, selecciona 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
