# -*- coding: utf-8 -*-
# Microproyecto: Pong de un jugador contra la computadora (Pygame)
# Controles: W/S o flechas arriba/abajo para mover tu paleta.
# Gana el primero en llegar a 5 puntos. ESPACIO reinicia al terminar.

import random
import pygame

# ---------- CONSTANTES DEL JUEGO ----------
ANCHO, ALTO = 800, 500
FPS = 60
PUNTOS_PARA_GANAR = 5
VEL_JUGADOR = 7      # velocidad de la paleta del jugador
VEL_CPU = 5          # la computadora es un poco mas lenta (se le puede ganar)
VEL_INICIAL = 5      # velocidad horizontal inicial de la pelota
VEL_MAXIMA = 12      # limite de velocidad de la pelota

# Colores (RGB)
COLOR_FONDO = (15, 15, 35)
COLOR_JUGADOR = (80, 200, 120)
COLOR_CPU = (230, 90, 90)
COLOR_PELOTA = (255, 255, 255)
COLOR_LINEA = (70, 70, 110)


def crear_objetos():
    """Crea las dos paletas y la pelota como rectangulos (pygame.Rect)."""
    jugador = pygame.Rect(30, ALTO // 2 - 40, 14, 80)
    cpu = pygame.Rect(ANCHO - 44, ALTO // 2 - 40, 14, 80)
    pelota = pygame.Rect(ANCHO // 2 - 8, ALTO // 2 - 8, 16, 16)
    return jugador, cpu, pelota


def reiniciar_pelota(pelota, direccion):
    """Centra la pelota y devuelve su velocidad [vx, vy] (direccion: -1 o 1)."""
    pelota.center = (ANCHO // 2, ALTO // 2)
    return [VEL_INICIAL * direccion, random.choice([-4, -3, -2, 2, 3, 4])]


def manejar_eventos():
    """Lee los eventos. Devuelve (salir, reiniciar)."""
    salir = False
    reiniciar = False
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            salir = True
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            reiniciar = True
    return salir, reiniciar


def mover_jugador(jugador):
    """Mueve la paleta del jugador con W/S o con las flechas."""
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        jugador.y -= VEL_JUGADOR
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        jugador.y += VEL_JUGADOR
    # La paleta no puede salir de la ventana
    jugador.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))


def mover_cpu(cpu, pelota):
    """La computadora sigue la altura de la pelota con velocidad limitada."""
    if pelota.centery < cpu.centery - 10:
        cpu.y -= VEL_CPU
    elif pelota.centery > cpu.centery + 10:
        cpu.y += VEL_CPU
    cpu.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))


def mover_pelota(pelota, vel, jugador, cpu):
    """Avanza la pelota y maneja los rebotes en techo, piso y paletas."""
    pelota.x += vel[0]
    pelota.y += vel[1]

    # Rebote en el techo y en el piso
    if pelota.top <= 0:
        pelota.top = 0
        vel[1] = abs(vel[1])
    elif pelota.bottom >= ALTO:
        pelota.bottom = ALTO
        vel[1] = -abs(vel[1])

    # Rebote en la paleta del jugador: sube la velocidad y cambia el angulo
    if pelota.colliderect(jugador) and vel[0] < 0:
        pelota.left = jugador.right
        vel[0] = min(abs(vel[0]) + 1, VEL_MAXIMA)
        vel[1] = (pelota.centery - jugador.centery) // 6
    # Rebote en la paleta de la computadora
    elif pelota.colliderect(cpu) and vel[0] > 0:
        pelota.right = cpu.left
        vel[0] = -min(abs(vel[0]) + 1, VEL_MAXIMA)
        vel[1] = (pelota.centery - cpu.centery) // 6


def revisar_punto(pelota):
    """Devuelve 'jugador', 'cpu' o None segun la pelota salga por un lado."""
    if pelota.right < 0:
        return "cpu"
    if pelota.left > ANCHO:
        return "jugador"
    return None


def dibujar(pantalla, fuente, fuente_peq, jugador, cpu, pelota,
            puntos_j, puntos_c, mensaje):
    """Dibuja toda la escena y actualiza la pantalla."""
    pantalla.fill(COLOR_FONDO)
    pygame.draw.line(pantalla, COLOR_LINEA, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)
    pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador)
    pygame.draw.rect(pantalla, COLOR_CPU, cpu)
    pygame.draw.ellipse(pantalla, COLOR_PELOTA, pelota)

    # Marcador
    marcador = fuente.render(f"{puntos_j}   {puntos_c}", True, COLOR_PELOTA)
    pantalla.blit(marcador, marcador.get_rect(center=(ANCHO // 2, 35)))

    # Mensaje de fin de partida
    if mensaje:
        texto = fuente.render(mensaje, True, COLOR_PELOTA)
        pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 30)))
        ayuda = fuente_peq.render("Presiona ESPACIO para jugar de nuevo",
                                  True, COLOR_PELOTA)
        pantalla.blit(ayuda, ayuda.get_rect(center=(ANCHO // 2, ALTO // 2 + 15)))

    pygame.display.flip()


def main():
    # ---------- INICIALIZACION ----------
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()              # Controla los FPS
    fuente = pygame.font.SysFont("arial", 36)
    fuente_peq = pygame.font.SysFont("arial", 22)

    jugador, cpu, pelota = crear_objetos()
    vel = reiniciar_pelota(pelota, random.choice([-1, 1]))
    puntos_j = 0
    puntos_c = 0
    mensaje = ""                             # Vacio mientras se juega

    # ---------- BUCLE PRINCIPAL ----------
    corriendo = True
    while corriendo:
        reloj.tick(FPS)
        pygame.display.set_caption(f"Pong - FPS: {reloj.get_fps():.0f}")

        # 1) Eventos
        salir, reiniciar = manejar_eventos()
        if salir:
            corriendo = False
        if reiniciar and mensaje:            # Nueva partida
            puntos_j = 0
            puntos_c = 0
            mensaje = ""
            vel = reiniciar_pelota(pelota, random.choice([-1, 1]))

        # 2) Actualizacion del estado (solo si la partida sigue)
        if not mensaje:
            mover_jugador(jugador)
            mover_cpu(cpu, pelota)
            mover_pelota(pelota, vel, jugador, cpu)

            quien = revisar_punto(pelota)
            if quien is not None:
                if quien == "jugador":
                    puntos_j += 1
                    vel = reiniciar_pelota(pelota, 1)
                else:
                    puntos_c += 1
                    vel = reiniciar_pelota(pelota, -1)

                if puntos_j >= PUNTOS_PARA_GANAR:
                    mensaje = "¡Ganaste!"
                elif puntos_c >= PUNTOS_PARA_GANAR:
                    mensaje = "La computadora ganó"

        # 3) Renderizado
        dibujar(pantalla, fuente, fuente_peq, jugador, cpu, pelota,
                puntos_j, puntos_c, mensaje)

    # ---------- CIERRE ----------
    pygame.quit()


if __name__ == "__main__":
    main()