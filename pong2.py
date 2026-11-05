"""
Pong con Pygame - Prototipo funcional para la investigacion de Pygame.

Evidencia el uso de:
  - pygame.sprite (Sprite y Group) y colisiones
  - pygame.event / pygame.key (input)
  - pygame.mixer (sonidos generados por codigo, no requiere archivos)
  - pygame.font (marcador y mensajes)
  - pygame.time.Clock (control de FPS y delta time)

Controles:
  Jugador izquierdo: W / S
  Jugador derecho:   Flecha arriba / Flecha abajo
  M: activar/desactivar CPU para el jugador derecho
  F: mostrar/ocultar FPS (util para pruebas de rendimiento)
  R: reiniciar partida     ESC: salir

Requisito: pip install pygame
"""
import array
import math
import random
import sys

import pygame

# ----------------------------- Configuracion -----------------------------
WIDTH, HEIGHT = 800, 500
FPS = 60
WIN_SCORE = 7

BG = (20, 24, 38)
FG = (240, 240, 240)
LEFT_COLOR = (90, 170, 255)
RIGHT_COLOR = (255, 130, 90)

BALL_SPEED = 380          # pixeles por segundo (velocidad inicial)
BALL_MAX_SPEED = 720
PADDLE_SPEED = 420


# ------------------------------- Sonido ----------------------------------
def make_beep(freq=440, ms=80, volume=0.4):
    """Genera un 'beep' (onda senoidal) sin necesidad de archivos de audio."""
    sample_rate = 44100
    n = int(sample_rate * ms / 1000)
    samples = array.array(
        "h",
        (int(volume * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
         for i in range(n)),
    )
    return pygame.mixer.Sound(buffer=samples.tobytes())


# ------------------------------- Sprites ---------------------------------
class Paddle(pygame.sprite.Sprite):
    """Paleta: un Sprite con una Surface rectangular y un Rect para colisiones."""

    def __init__(self, x, color):
        super().__init__()
        self.image = pygame.Surface((14, 90))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, HEIGHT // 2))
        self.y = float(self.rect.centery)  # posicion real (float) para movimiento suave

    def move(self, direction, dt):
        """direction: -1 (arriba), 0 (quieto), 1 (abajo). dt en segundos."""
        self.y += direction * PADDLE_SPEED * dt
        half = self.rect.height / 2
        self.y = max(half, min(HEIGHT - half, self.y))  # no salir de la pantalla
        self.rect.centery = round(self.y)


class Ball(pygame.sprite.Sprite):
    """Pelota: se mueve con un vector de velocidad y rebota en techo y piso."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, FG, (8, 8), 8)
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2()
        self.vel = pygame.Vector2()
        self.reset()

    def reset(self, direction=None):
        self.pos.update(WIDTH / 2, HEIGHT / 2)
        angle = random.uniform(-0.4, 0.4)
        d = direction if direction else random.choice((-1, 1))
        self.vel = pygame.Vector2(d * math.cos(angle), math.sin(angle)) * BALL_SPEED
        self.rect.center = self.pos

    def update(self, dt):
        """Mueve la pelota. Devuelve True si rebota contra techo o piso."""
        self.pos += self.vel * dt
        bounced = False
        if self.pos.y <= 8:
            self.pos.y = 8
            self.vel.y = abs(self.vel.y)
            bounced = True
        elif self.pos.y >= HEIGHT - 8:
            self.pos.y = HEIGHT - 8
            self.vel.y = -abs(self.vel.y)
            bounced = True
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        return bounced


# ------------------------------ Funciones --------------------------------
def draw_text(screen, font, text, center, color=FG):
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=center))


def main():
    pygame.init()
    try:
        pygame.mixer.init(44100, -16, 1)
        snd_paddle = make_beep(660, 70)
        snd_wall = make_beep(330, 50)
        snd_score = make_beep(220, 250)
    except pygame.error:
        # Sin dispositivo de audio: el juego sigue funcionando sin sonido.
        snd_paddle = snd_wall = snd_score = None

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong - Prototipo Pygame")
    clock = pygame.time.Clock()
    font_big = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 28)

    left = Paddle(30, LEFT_COLOR)
    right = Paddle(WIDTH - 30, RIGHT_COLOR)
    ball = Ball()
    paddles = pygame.sprite.Group(left, right)
    all_sprites = pygame.sprite.Group(left, right, ball)

    score = [0, 0]
    cpu_mode = False
    show_fps = False
    game_over = False

    def play(sound):
        if sound:
            sound.play()

    running = True
    while running:
        # dt: segundos transcurridos desde el frame anterior (y limita a FPS)
        dt = clock.tick(FPS) / 1000

        # 1) EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_m:
                    cpu_mode = not cpu_mode
                elif event.key == pygame.K_f:
                    show_fps = not show_fps
                elif event.key == pygame.K_r:
                    score = [0, 0]
                    game_over = False
                    ball.reset()

        # 2) ACTUALIZAR LOGICA
        if not game_over:
            keys = pygame.key.get_pressed()
            left.move(keys[pygame.K_s] - keys[pygame.K_w], dt)
            if cpu_mode:
                # CPU sencilla: sigue la pelota con un pequeno margen
                diff = ball.rect.centery - right.rect.centery
                right.move(0 if abs(diff) < 12 else (1 if diff > 0 else -1), dt)
            else:
                right.move(keys[pygame.K_DOWN] - keys[pygame.K_UP], dt)

            if ball.update(dt):
                play(snd_wall)

            # Colision pelota-paletas (pygame.sprite)
            hit = pygame.sprite.spritecollideany(ball, paddles)
            if hit:
                is_left = hit is left
                # Reposicionar fuera de la paleta para evitar "pegarse"
                ball.pos.x = hit.rect.right + 9 if is_left else hit.rect.left - 9
                # El angulo depende de donde golpea la paleta
                offset = (ball.rect.centery - hit.rect.centery) / (hit.rect.height / 2)
                speed = min(ball.vel.length() * 1.06, BALL_MAX_SPEED)
                direction = 1 if is_left else -1
                ball.vel = pygame.Vector2(direction, offset * 0.8).normalize() * speed
                play(snd_paddle)

            # Puntos
            if ball.pos.x < 0:
                score[1] += 1
                play(snd_score)
                ball.reset(direction=1)
            elif ball.pos.x > WIDTH:
                score[0] += 1
                play(snd_score)
                ball.reset(direction=-1)

            if max(score) >= WIN_SCORE:
                game_over = True

        # 3) DIBUJAR
        screen.fill(BG)
        for y in range(0, HEIGHT, 30):  # linea central
            pygame.draw.rect(screen, (60, 66, 90), (WIDTH // 2 - 2, y, 4, 16))
        all_sprites.draw(screen)
        draw_text(screen, font_big, str(score[0]), (WIDTH // 2 - 70, 45))
        draw_text(screen, font_big, str(score[1]), (WIDTH // 2 + 70, 45))
        mode = "CPU" if cpu_mode else "2 jugadores"
        draw_text(screen, font_small, f"Modo: {mode}  |  M: CPU  F: FPS  R: reiniciar",
                  (WIDTH // 2, HEIGHT - 20), (140, 148, 175))
        if show_fps:
            draw_text(screen, font_small, f"FPS: {clock.get_fps():.1f}", (60, 20))
        if game_over:
            winner = "izquierdo" if score[0] > score[1] else "derecho"
            draw_text(screen, font_big, f"Gana el jugador {winner}", (WIDTH // 2, HEIGHT // 2))
            draw_text(screen, font_small, "Presiona R para jugar de nuevo",
                      (WIDTH // 2, HEIGHT // 2 + 50))

        # 4) MOSTRAR (doble buffering)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()