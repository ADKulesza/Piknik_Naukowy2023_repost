import time
from pathlib import Path

import pygame

from amplifiers.drivers.debug.debug_amplifier import DummyAmplfier
from common.base_game import BaseGame
from common.components.core.app import App
from common.utils import singleton
from game.game3.objects import Player, Rock, Score

app = App()
fort_size = 50
font_name = app.theme.font_name
font = pygame.font.Font(font_name, fort_size)


@singleton
class Game3(BaseGame):
    name = "Podbój Kosmosu"

    def run(self):
        from common.components.core.app import App

        app = App()
        screen = app.canvas

        # przeszkody
        num_of_rocks_init = 3
        num_of_rocks = num_of_rocks_init

        rock_time = 10

        width, height = screen.get_size()

        # Background
        background = pygame.image.load(
            Path(__file__).parent.parent.parent / "grafika/tła/kosmos.png"
        )
        background = pygame.transform.scale(background, screen.get_size())

        # Background sound
        pygame.mixer.music.load(Path(__file__).parent / "assets/background.wav")
        pygame.mixer.music.play(-1)

        # Caption and Icon
        pygame.display.set_caption(self.name)
        icon = pygame.image.load(Path(__file__).parent / "assets/ufo_icon.png")
        pygame.display.set_icon(icon)

        player = Player()
        rocks = [Rock() for _ in range(num_of_rocks)]
        score = Score()

        # Game Loop
        running = True
        collision = False
        start_time = time.time()
        while running and not collision:
            screen.blit(background, (0, 0))

            for rock in rocks:
                rock.update(screen)
            player.update(screen)
            score.update(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.move = player.speed_right
                    if event.key == pygame.K_p:
                        running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        player.move = player.speed_left

            # move with muscles
            if not isinstance(app.amplifier.amp, DummyAmplfier):
                val = app.get_emg_value()
                if val < app.player.mean:
                    move_val = player.speed_left
                if val >= app.player.mean:
                    move_val = player.speed_right
                player.move = move_val

            # player in boundaries
            player.rect.right += player.move
            if player.rect.left <= 0:
                player.rect.left = 0
            elif player.rect.right >= width:
                player.rect.right = width

            # update rocks
            for rock in rocks:
                if rock.rect.top > screen.get_height():
                    score.value += 10
                    rock.regenerate()
                rock.rect.bottom += rock.move

                # Collision
                if pygame.Rect.colliderect(player.rect, rock.rect):
                    # pixel collision
                    rock_mask = pygame.mask.from_surface(rock.img)
                    player_mask = pygame.mask.from_surface(player.img)
                    mask_collision = player_mask.overlap(
                        rock_mask,
                        (rock.rect.x - player.rect.x, rock.rect.y - player.rect.y),
                    )
                    if not mask_collision:
                        continue

                    if not collision:
                        explosion_sound = pygame.mixer.Sound(
                            Path(__file__).parent / "assets/explosion.wav"
                        )
                        explosion_sound.play()
                    collision = True

            # add extra enemies
            current_time = time.time()
            if int(current_time - start_time) >= rock_time:
                rocks.append(Rock())
                num_of_rocks += 1
                rock_time += 10

            app.tick()

        if running:
            self.game_over(screen)
            screen.blit(background, (0, 0))
            for rock in rocks:
                rock.update(screen)
            player.update(screen)
            score.update(screen)
            pygame.display.update()

            self.save_score(score.value)

            time.sleep(2)

        pygame.mixer.music.stop()
        pygame.event.get()

    def game_over(self, screen):
        over_text = font.render("GAME OVER", True, (255, 255, 255))
        rect = over_text.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )
        screen.blit(over_text, rect)
