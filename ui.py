import pygame

from config import (
    BLACK,
    FONT_LARGE,
    FONT_MEDIUM,
    FONT_SMALL,
    GREEN,
    HEIGHT,
    PURPLE,
    RED,
    UPGRADES,
    WHITE,
    WIDTH,
    YELLOW,
)


def draw_hud(screen, player_stats, wave_info, show_level_up=False):
    """Отрисовка интерфейса (обновленная)"""
    # Фон для HUD
    pygame.draw.rect(
        screen, (30, 30, 30, 180), (0, 0, WIDTH, 120), border_radius=10
    )
    pygame.draw.rect(
        screen, (60, 60, 60), (0, 0, WIDTH, 120), 2, border_radius=10
    )

    # Статистика игрока слева
    draw_player_stats(screen, player_stats, 10, 10)

    # Информация о волне справа
    draw_wave_info(screen, wave_info, WIDTH - 250, 10)

    # Управление внизу слева
    draw_controls(screen, 10, HEIGHT - 100)

    # Статистика улучшений внизу справа
    draw_upgrade_stats(screen, player_stats, WIDTH - 250, HEIGHT - 100)

    # Сообщение о повышении уровня
    if show_level_up:
        draw_level_up_message(screen)


def draw_player_stats(screen, stats, x, y):
    """Отрисовка статистики игрока"""
    # Уровень и опыт
    level_text = FONT_SMALL.render(f"Уровень: {stats['level']}", True, WHITE)
    exp_text = FONT_SMALL.render(
        f"Опыт: {stats['exp']}/{stats['exp_to_next_level']}", True, WHITE
    )

    # Здоровье
    health_text = FONT_SMALL.render(
        f"Здоровье: {stats['health']}/{stats['max_health']}", True, WHITE
    )

    # Урон и скорость атаки
    damage_text = FONT_SMALL.render(f"Урон: {stats['damage']}", True, WHITE)
    attack_speed_text = FONT_SMALL.render(
        f"Скорость атаки: {1000 / stats['shoot_delay']:.1f}/сек", True, WHITE
    )

    # Отображение текста
    screen.blit(level_text, (x, y))
    screen.blit(exp_text, (x, y + 25))
    screen.blit(health_text, (x, y + 50))
    screen.blit(damage_text, (x, y + 75))
    screen.blit(attack_speed_text, (x, y + 100))


def draw_wave_info(screen, wave_info, x, y):
    """Отрисовка информации о волне"""
    wave_text = FONT_SMALL.render(
        f"Волна: {wave_info['current_wave']}", True, WHITE
    )
    enemies_text = FONT_SMALL.render(
        f"Врагов: {wave_info['enemies_remaining']}/{wave_info['total_enemies']}",
        True,
        WHITE,
    )

    screen.blit(wave_text, (x, y))
    screen.blit(enemies_text, (x, y + 25))

    # Прогресс волны
    if wave_info["total_enemies"] > 0:
        progress = 1 - (
            wave_info["enemies_remaining"] / wave_info["total_enemies"]
        )
        bar_width = 200
        bar_height = 10
        pygame.draw.rect(screen, RED, (x, y + 55, bar_width, bar_height))
        pygame.draw.rect(
            screen, GREEN, (x, y + 55, bar_width * progress, bar_height)
        )


def draw_controls(screen, x, y):
    """Отрисовка управления"""
    controls = [
        "Управление:",
        "WASD/Стрелки - Движение",
        "ESC - Выход",
        "R - Перезапуск (после смерти)",
    ]

    for i, text in enumerate(controls):
        control_text = FONT_SMALL.render(text, True, WHITE)
        screen.blit(control_text, (x, y + i * 25))


def draw_level_up_message(screen):
    """Отрисовка сообщения о повышении уровня"""
    message = FONT_LARGE.render("УРОВЕНЬ ПОВЫШЕН!", True, PURPLE)

    # Полупрозрачный фон
    s = pygame.Surface((message.get_width() + 40, message.get_height() + 20))
    s.set_alpha(200)
    s.fill(BLACK)

    screen.blit(
        s, (WIDTH // 2 - message.get_width() // 2 - 20, HEIGHT // 2 - 100)
    )
    screen.blit(
        message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 90)
    )


def draw_game_over(screen, player_stats, wave_info):
    """Отрисовка экрана окончания игры"""
    # Затемнение экрана
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Заголовок
    game_over_text = FONT_LARGE.render("GAME OVER", True, RED)
    screen.blit(
        game_over_text,
        (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100),
    )

    # Статистика
    stats_text = [
        f"Достигнут уровень: {player_stats['level']}",
        f"Пройдено волн: {wave_info['current_wave'] - 1}",
        f"Собрано опыта: {player_stats['exp'] + player_stats['level'] * 100}",
    ]

    for i, text in enumerate(stats_text):
        stat_text = FONT_MEDIUM.render(text, True, WHITE)
        screen.blit(
            stat_text,
            (
                WIDTH // 2 - stat_text.get_width() // 2,
                HEIGHT // 2 - 30 + i * 40,
            ),
        )

    restart_text = FONT_SMALL.render("Нажмите R для перезапуска", True, WHITE)
    screen.blit(
        restart_text,
        (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100),
    )


def draw_wave_complete(screen, wave_number):
    """Отрисовка сообщения о завершении волны"""
    message = FONT_MEDIUM.render(
        f"Волна {wave_number} завершена! Готовьтесь к следующей...",
        True,
        YELLOW,
    )

    # Полупрозрачный фон
    s = pygame.Surface((message.get_width() + 40, message.get_height() + 20))
    s.set_alpha(150)
    s.fill((0, 50, 0))

    screen.blit(s, (WIDTH // 2 - message.get_width() // 2 - 20, 150))
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, 160))


def draw_upgrade_stats(screen, player_stats, x, y):
    """Отрисовка статистики улучшений"""
    upgrades = player_stats.get("upgrades", {})

    if any(upgrades.values()):  # Если есть хотя бы одно улучшение
        title = FONT_SMALL.render("Улучшения:", True, WHITE)
        screen.blit(title, (x, y))

        y_offset = 25
        for upgrade_type, level in upgrades.items():
            if level > 0:
                upgrade_info = UPGRADES.get(upgrade_type, {})
                upgrade_text = FONT_SMALL.render(
                    f"{upgrade_info.get('icon', '')}: {level}",
                    # f"{upgrade_info.get('icon', '')} {upgrade_info.get('name', upgrade_type)}: {level}",
                    True,
                    upgrade_info.get("color", WHITE),
                )
                screen.blit(upgrade_text, (x + 10, y + y_offset))
                y_offset += 20
