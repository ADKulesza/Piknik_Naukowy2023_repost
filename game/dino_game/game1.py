import random
from pathlib import Path
from random import choice

import pygame

from common.base_game import BaseGame
from common.utils import singleton
from game.dino_game.objects import Obstacle, Player
from game.dino_game.utils import collision_sprite, display_score


@singleton
class Game1(BaseGame):
    name = "Podbój Marsa"

    def __init__(self):
        super().__init__()

    def run(self):
        from common.components.core.app import App

        pygame.display.set_caption("Dinozaur")

        bg_music = pygame.mixer.Sound(Path(__file__).parent / "assets/music.wav")
        bg_music.play(loops=True)
        bg_music.set_volume(0.04)

        app = App()
        screen = app.canvas
        font_color = app.theme.secondary_color
        font_path = app.theme.font_name

        font = pygame.font.Font(font_path, 50)

        time = 0
        t = 0
        game_active = False
        start_t = 0

        # GROUPS
        player = pygame.sprite.GroupSingle()
        player.add(Player())

        obstacle_group = pygame.sprite.Group()

        sky_surface = pygame.image.load(
            Path(__file__).parent / "assets/mars.png"
        ).convert()
        sky_surface = pygame.transform.scale(sky_surface, screen.get_size())
        background = sky_surface
        """ground_surface = pygame.image.load(
            Path(__file__).parent / "assets/ground.png"
        ).convert()"""
        # ground_surface = pygame.transform.scale(ground_surface, screen.get_size())
        # text_surface = font.render("Dinozaur", False, (139, 195, 74))
        # text_rect = text_surface.get_rect(topleft=(50, 50))
        v = 30

        # timer
        obstacle_times = []
        for i, j in enumerate([1500, 900, 700, 550]):
            obstacle_time = pygame.USEREVENT + i
            pygame.time.set_timer(obstacle_time, j)
            obstacle_times.append(obstacle_time)

        # intro screen
        player_stand = pygame.image.load(
            Path(__file__).parent / "assets/player_stand.png"
        ).convert_alpha()
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rec = player_stand.get_rect(center=(screen.get_width() // 2, 150))

        player_name = font.render(f"Witaj {app.player.name}!", True, font_color)
        player_name = pygame.transform.rotozoom(player_name, 0, 1.5)
        player_name_rec = player_name.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2 - 75)
        )

        welcome = font.render("Jesteś gotowy na podbój kosmosu?", True, font_color)
        welcome = pygame.transform.rotozoom(welcome, 0, 0.8)
        welcome_rec = welcome.get_rect(center=screen.get_rect().center)

        text_enter = font.render(
            "Aby rozpoczac gre nacisnij przycisk SPACJI", True, font_color
        )
        text_enter = pygame.transform.rotozoom(text_enter, 0, 0.5)
        # print(text_enter.get_width())
        text_enter_rect = text_enter.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2 + 50)
        )
        # print(text_enter.get_width())
        # text_enter_rect = text_enter.get_rect(center=(400, 375))
        # print(text_enter.get_width())
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    run = False
                if game_active:
                    if 30 >= (t // 100 / 10):
                        if event.type == obstacle_times[0]:
                            obstacle_group.add(
                                Obstacle(choice(["fly", "snail", "snail"]))
                            )
                    elif 50 > (t // 100 / 10) > 30:
                        # print(i)
                        # obstacle_timer(i)
                        if event.type == obstacle_times[1]:
                            obstacle_group.add(
                                Obstacle(choice(["fly", "snail", "snail"]))
                            )
                    elif 110 > (t // 100 / 10) >= 50:
                        if event.type == obstacle_times[2]:
                            obstacle_group.add(
                                Obstacle(choice(["fly", "snail", "snail"]))
                            )
                    else:
                        if event.type == obstacle_times[3]:
                            obstacle_group.add(
                                Obstacle(choice(["fly", "snail", "snail"]))
                            )

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_active = True
                        start_t = pygame.time.get_ticks()
            if game_active:
                v += 0.001
                screen.blit(sky_surface, (0, 0))
                # screen.blit(ground_surface, (0, 72))
                # pygame.draw.rect(screen, (64, 64, 64), text_rect)
                # screen.blit(text_surface, text_rect)
                # pygame.draw.line(screen,'Gold',(0,0),pygame.mouse.get_pos(),10)
                # pygame.draw.ellipse(screen,'Brown',pygame.Rect(50,200,100,100))
                t = display_score(time, game_active, start_t, font, screen)
                # PLAYER
                player.draw(screen)
                player.update()

                # OBSTACLES
                obstacle_group.draw(screen)

                obstacle_group.update(v)

                # collisions
                game_active = collision_sprite(
                    player, obstacle_group, t, app.player.name
                )
            else:
                screen.fill((94, 129, 162))
                screen.blit(background, (0, 0))

                percent = 1 / app.FPS
                player_stand_rec_jitter = []
                for _ in range(2):
                    random_value = random.random()
                    if random_value < percent:
                        player_stand_rec_jitter.append(-1)
                    elif random_value > 1 - percent:
                        player_stand_rec_jitter.append(1)
                    else:
                        player_stand_rec_jitter.append(0)
                player_stand_rec = [
                    jitter + pos
                    for jitter, pos in zip(player_stand_rec_jitter, player_stand_rec)
                ]
                screen.blit(player_stand, player_stand_rec)
                screen.blit(text_enter, text_enter_rect)
                v = 6
                if t != 0:
                    # text_surface = font.render("Dinozaur", False, (139, 195, 74))
                    display_score(t, game_active, start_t, font, screen)
                    # screen.blit(text_surface, text_rect)
                else:
                    screen.blit(welcome, welcome_rec)
                screen.blit(player_name, player_name_rec)
            pygame.display.update()
            app.tick()
        bg_music.stop()
