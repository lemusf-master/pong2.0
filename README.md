# Pong 2.0

**Autor:** Fernando de Jesus Lemus Martinez

**Curso:** Logica de Programacion

## Descripción
Pong 2.0 es una versión del clásico juego Pong desarrollada con Python y Pygame. La versión 2 incorpora el modo JcJ (jugador contra jugador) y sonidos.

## Objetivo general
Desarrollar el juego de forma modular y por versiones durante el curso, aplicando los temas vistos en clase.

## Investigación sobre Pygame

### ¿Qué es Pygame y para qué se utiliza?
Pygame es una biblioteca de Python para crear videojuegos y aplicaciones multimedia en 2D. Se encarga de crear la ventana, dibujar gráficos, reproducir sonidos y capturar el teclado y el mouse, para que el programador se concentre en la lógica del juego.

### Relación con los temas vistos en clase
- **Ciclos:** el bucle principal (`while running:`) repite en cada fotograma el proceso de leer eventos, actualizar el juego y dibujar la pantalla.
- **Eventos y condicionales:** con `pygame.event.get()` y estructuras `if/elif` se detecta cuándo se presiona una tecla, se cierra la ventana o la pelota choca con una paleta.
- **Estructuras de datos:** las posiciones y colores se guardan en tuplas, y se pueden usar listas y diccionarios para marcadores o configuraciones.
- **Funciones:** se separa la lógica en funciones (por ejemplo, mover paletas, mover pelota, detectar colisiones, dibujar), lo que hace el código más ordenado y reutilizable.
- **Programación modular:** el proyecto se puede dividir en partes independientes que se van mejorando por versiones.

### ¿Qué significa "tomar mucho o poco" de la librería?
Pygame no obliga a usar todas sus herramientas. Se puede usar solo lo básico (ventana, dibujo de formas, teclado) o añadir módulos más avanzados (sonido con `mixer`, texto con `font`, sprites, manejo del tiempo). Cada versión del juego puede tomar más de la librería: la versión 1 usa lo esencial y la versión 2 suma, por ejemplo, el sonido y el modo de dos jugadores.

## Organización del trabajo con ramas
| Rama | Propósito |
|------|-----------|
| `main` | Versión estable del proyecto |
| `v01` | Rama de trabajo; desde aquí se integra a `main` con merge |
| `actividad1` | Versión 1 del juego (primera actividad de Pygame) |
| `actividad2` | Versión 2 del juego (modo JcJ y sonidos) |

Flujo de trabajo: cada avance se desarrolla en su propia rama, se integra en `v01` mediante pull request y, cuando está estable, se hace merge a `main`. Las nuevas versiones seguirán el mismo patrón.
