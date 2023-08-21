import pygame


def collision_sprite(player, obstacle_group, t, name):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        with open("lista_uczestnikow", "a") as myfile:
            myfile.write(name + ": wynik " + str((t // 100 / 10)) + "\n")
        return False
    return True


def display_score(time, game_active, start_t, test_font, screen):
    if game_active:
        time = pygame.time.get_ticks() - start_t
    score_surf = test_font.render(f"Wynik: {time // 100 / 10}s", True, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(960, 50))
    screen.blit(score_surf, score_rect)
    return time
