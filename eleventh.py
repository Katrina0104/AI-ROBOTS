import pygame
import random
from collections import deque
import algorithms  # 引入演算法集合

# --- Parameters ---
GRID_SIZE = 10
CELL_SIZE = 50
INFO_HEIGHT = 100
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE + INFO_HEIGHT
POINT_COUNT = 12
DEFAULT_TOTAL_ROUNDS = 20

# --- Theme Colors ---
CARD_COLOR = (44, 52, 82)
CARD_BORDER = (100, 180, 255)
GRID_LINE_COLOR = (0, 0, 0)
TITLE_COLOR = (230, 230, 255)
SCORE_FONT_COLOR = (255, 255, 255)
POINT_COLOR = (255, 210, 70)
BTN_BG = (36, 40, 60)
BTN_BG_HOVER = (77, 88, 120)
BTN_TEXT = (255, 255, 255)

STRATEGIES = [
    ("Random", algorithms.random_strategy),
    ("Greedy", algorithms.greedy_strategy),
    ("Rule-based", algorithms.rule_based_strategy),
    ("BFS", algorithms.bfs_strategy),
    ("A*", algorithms.a_star_strategy),
    ("JPS", algorithms.jps_strategy),
    ("RRT", algorithms.rrt_strategy),
    ("Hybrid", algorithms.hybrid_strategy),
    ("Best-First Search", algorithms.best_first_strategy),
    ("Weighted A*", algorithms.weighted_a_star_strategy),
    ("Wall Follower", algorithms.wall_follower_strategy),
]

# --- Bot Class ---
class Bot:
    def __init__(self, x, y, color, strategy, name):
        self.x = x
        self.y = y
        self.color = color
        self.strategy = strategy
        self.name = name
        self.score = 0
        self.total_score = 0
        self.wins = 0
        self.turns_taken = 0

    def move(self, grid, points, bots):
        dx, dy = self.strategy(self, grid, points, bots)
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            if not any(bot.x == nx and bot.y == ny for bot in bots if bot is not self):
                self.x, self.y = nx, ny

def generate_points():
    points = set()
    corners = {(0,0), (GRID_SIZE-1,0), (0,GRID_SIZE-1), (GRID_SIZE-1,GRID_SIZE-1)}
    while len(points) < POINT_COUNT:
        p = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        points.add(p)
        points -= corners
    while len(points) < POINT_COUNT:
        p = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if p not in corners:
            points.add(p)
    return list(points)

def draw_button(screen, rect, text, font, is_hover):
    pygame.draw.rect(screen, BTN_BG_HOVER if is_hover else BTN_BG, rect, border_radius=8)
    pygame.draw.rect(screen, CARD_BORDER, rect, 2, border_radius=8)
    label = font.render(text, True, BTN_TEXT)
    screen.blit(label, (
        rect.x + (rect.width - label.get_width()) // 2,
        rect.y + (rect.height - label.get_height()) // 2
    ))

def main_menu(screen, background_img):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
    font = pygame.font.SysFont('Segoe UI', max(20, SCREEN_HEIGHT//36))
    big_font = pygame.font.SysFont('Segoe UI', max(34, SCREEN_HEIGHT//20), bold=True)
    title_font = pygame.font.SysFont('Segoe UI', max(52, SCREEN_HEIGHT//14), bold=True)

    total_rounds = DEFAULT_TOTAL_ROUNDS
    bot_colors = [(255, 0, 0), (0, 128, 255), (0, 200, 0), (255, 128, 0)]
    selected_strategies = [0, 1, 2, 3]  # 預設

    running = True
    while running:
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
        bg_scaled = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bg_scaled, (0, 0))

        title = title_font.render("AI Battle Bots", True, TITLE_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))

        rounds_label = big_font.render("Rounds:", True, (220, 220, 255))
        screen.blit(rounds_label, (SCREEN_WIDTH//2 - 180, 150))
        rounds_box = pygame.Rect(SCREEN_WIDTH//2, 150, 90, 44)
        pygame.draw.rect(screen, BTN_BG, rounds_box, border_radius=8)
        pygame.draw.rect(screen, CARD_BORDER, rounds_box, 2, border_radius=8)
        rounds_val = big_font.render(str(total_rounds), True, (255,255,255))
        screen.blit(rounds_val, (rounds_box.centerx - rounds_val.get_width()//2, rounds_box.y + 5))

        minus_rect = pygame.Rect(SCREEN_WIDTH//2 - 40, 150, 40, 44)
        plus_rect = pygame.Rect(SCREEN_WIDTH//2 + 90, 150, 40, 44)
        draw_button(screen, minus_rect, "-", big_font, minus_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button(screen, plus_rect, "+", big_font, plus_rect.collidepoint(pygame.mouse.get_pos()))

        bot_titles = ["Bot 1", "Bot 2", "Bot 3", "Bot 4"]
        for i in range(4):
            y = 240 + i*78
            bot_box = pygame.Rect(SCREEN_WIDTH//2 - 220, y, 440, 62)
            pygame.draw.rect(screen, CARD_COLOR, bot_box, border_radius=10)
            pygame.draw.rect(screen, bot_colors[i], bot_box, 2, border_radius=10)
            name = bot_titles[i]
            name_label = big_font.render(name, True, bot_colors[i])
            screen.blit(name_label, (bot_box.x + 16, bot_box.y + 10))
            strat_idx = selected_strategies[i]
            strat_name = STRATEGIES[strat_idx][0]
            strat_label = font.render(f"Algorithm: {strat_name}", True, BTN_TEXT)
            screen.blit(strat_label, (bot_box.x + 160, bot_box.y + 20))

            left_rect = pygame.Rect(bot_box.x + 140, bot_box.y + 21, 22, 22)
            right_rect = pygame.Rect(bot_box.x + 370, bot_box.y + 21, 22, 22)
            draw_button(screen, left_rect, "<", font, left_rect.collidepoint(pygame.mouse.get_pos()))
            draw_button(screen, right_rect, ">", font, right_rect.collidepoint(pygame.mouse.get_pos()))

        start_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 110, 200, 56)
        draw_button(screen, start_btn_rect, "Start Game", big_font, start_btn_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); exit()
                elif event.key == pygame.K_f:
                    if screen.get_flags() & pygame.FULLSCREEN:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
            elif event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if minus_rect.collidepoint(mx, my):
                    total_rounds = max(1, total_rounds - 1)
                elif plus_rect.collidepoint(mx, my):
                    total_rounds = min(100, total_rounds + 1)
                elif start_btn_rect.collidepoint(mx, my):
                    strategies = [STRATEGIES[idx][1] for idx in selected_strategies]
                    strategy_names = [STRATEGIES[idx][0] for idx in selected_strategies]
                    return total_rounds, strategies, strategy_names
                for i in range(4):
                    y = 240 + i*78
                    left = SCREEN_WIDTH//2 - 220 + 140
                    right = SCREEN_WIDTH//2 - 220 + 370
                    top = y + 21
                    if pygame.Rect(left, top, 22, 22).collidepoint(mx, my):
                        selected_strategies[i] = (selected_strategies[i] - 1) % len(STRATEGIES)
                    elif pygame.Rect(right, top, 22, 22).collidepoint(mx, my):
                        selected_strategies[i] = (selected_strategies[i] + 1) % len(STRATEGIES)

# 其餘程式碼與之前範例相同
# ... render_game_screen, show_final_results, run_game, main ...

def render_game_screen(screen, background_img, bots, points, round_num, turn, 
                      font, big_font, GRID_SIZE, CELL_SIZE, INFO_HEIGHT, 
                      SCREEN_WIDTH, SCREEN_HEIGHT, CARD_COLOR, CARD_BORDER, 
                      TITLE_COLOR, SCORE_FONT_COLOR, GRID_LINE_COLOR, POINT_COLOR):
    bg_scaled = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg_scaled, (0, 0))

    info_rect = pygame.Rect(0, 0, SCREEN_WIDTH, INFO_HEIGHT)
    pygame.draw.rect(screen, CARD_COLOR, info_rect)
    pygame.draw.line(screen, CARD_BORDER, (0, INFO_HEIGHT), (SCREEN_WIDTH, INFO_HEIGHT), 3)

    round_text = big_font.render(f"Round {round_num} - Turn {turn}", True, TITLE_COLOR)
    screen.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, 10))

    score_card = pygame.Rect(SCREEN_WIDTH // 2 - 260, 54, 520, 36)
    pygame.draw.rect(screen, CARD_COLOR, score_card, border_radius=12)
    pygame.draw.rect(screen, CARD_BORDER, score_card, 2, border_radius=12)
    bot_scores = [f"{bot.name}: {bot.score}" for bot in bots]
    scores_text = font.render("   ".join(bot_scores), True, SCORE_FONT_COLOR)
    screen.blit(scores_text, (SCREEN_WIDTH // 2 - scores_text.get_width() // 2, 60))

    grid_surface = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE), pygame.SRCALPHA)
    grid_surface.fill((0, 0, 0, 0))
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(grid_surface, GRID_LINE_COLOR, rect, 1)

    for px, py in points:
        pygame.draw.circle(grid_surface, POINT_COLOR, (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

    available_height = SCREEN_HEIGHT - INFO_HEIGHT
    scale_factor = min(SCREEN_WIDTH / (GRID_SIZE * CELL_SIZE), available_height / (GRID_SIZE * CELL_SIZE))
    scaled_width = int(GRID_SIZE * CELL_SIZE * scale_factor)
    scaled_height = int(GRID_SIZE * CELL_SIZE * scale_factor)
    scaled_grid = pygame.transform.scale(grid_surface, (scaled_width, scaled_height))
    grid_x = (SCREEN_WIDTH - scaled_width) // 2
    grid_y = INFO_HEIGHT + (available_height - scaled_height) // 2
    screen.blit(scaled_grid, (grid_x, grid_y))

    cell_scale = scale_factor
    for bot in bots:
        cx = int(bot.x * CELL_SIZE * cell_scale + CELL_SIZE * cell_scale // 2) + grid_x
        cy = int(bot.y * CELL_SIZE * cell_scale + CELL_SIZE * cell_scale // 2) + grid_y
        pygame.draw.circle(screen, (255,255,255), (cx, cy), int(CELL_SIZE * cell_scale // 3 + 2))
        pygame.draw.circle(screen, bot.color, (cx, cy), int(CELL_SIZE * cell_scale // 3))

    pygame.display.flip()

def show_final_results(screen, bots, performance, total_rounds, background_img):
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
    base_font_size = max(SCREEN_HEIGHT // 40, 18)
    font = pygame.font.SysFont("Segoe UI", base_font_size)
    big_font = pygame.font.SysFont("Segoe UI", base_font_size + 6)
    title_font = pygame.font.SysFont("Segoe UI", base_font_size + 14, bold=True)

    bg_scaled = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg_scaled, (0, 0))

    box_margin_x = int(SCREEN_WIDTH * 0.07)
    box_margin_y = int(SCREEN_HEIGHT * 0.15)
    box_width = SCREEN_WIDTH - 2 * box_margin_x
    box_height = SCREEN_HEIGHT - 2 * box_margin_y
    box_x = box_margin_x
    box_y = box_margin_y

    table_box = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(screen, (30, 30, 30), table_box, border_radius=16)
    pygame.draw.rect(screen, (200, 200, 200), table_box, 2, border_radius=16)

    title = title_font.render("Final Tournament Results", True, TITLE_COLOR)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, box_y + 10))

    headers = ["Bot", "Wins", "Avg Score", "Efficiency"]
    col_widths = [0.25, 0.15, 0.3, 0.3]
    col_positions = [box_x + int(sum(col_widths[:i]) * box_width) + 20 for i in range(len(headers))]

    header_y = box_y + 60
    for i, text in enumerate(headers):
        header = big_font.render(text, True, (200, 200, 255))
        screen.blit(header, (col_positions[i], header_y))

    pygame.draw.line(screen, (100, 100, 150), (box_x + 20, header_y + base_font_size + 10),
                     (box_x + box_width - 20, header_y + base_font_size + 10), 2)

    row_y = header_y + base_font_size + 20
    row_height = base_font_size + 14
    row_spacing = 10

    for bot in bots:
        stats = performance[bot.name]
        avg_score = stats['total_score'] / total_rounds
        efficiency = 100 * stats['wins'] / total_rounds

        row_rect = pygame.Rect(box_x + 20, row_y, box_width - 40, row_height)
        pygame.draw.rect(screen, CARD_COLOR, row_rect, border_radius=8)
        pygame.draw.rect(screen, bot.color, row_rect, 2, border_radius=8)

        values = [
            font.render(bot.name, True, bot.color),
            font.render(str(stats['wins']), True, SCORE_FONT_COLOR),
            font.render(f"{avg_score:.2f}", True, SCORE_FONT_COLOR),
            font.render(f"{efficiency:.1f}%", True, SCORE_FONT_COLOR)
        ]

        for i, text in enumerate(values):
            screen.blit(text, (col_positions[i], row_y + 6))

        row_y += row_height + row_spacing

    instructions = font.render("Press F for fullscreen | ESC to quit | M or Click for main menu", True, (0, 0, 0))
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); exit()
                elif event.key == pygame.K_f:
                    if screen.get_flags() & pygame.FULLSCREEN:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                elif event.key == pygame.K_m:
                    return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return "menu"

def run_game(screen, total_rounds, strategies, strategy_names, background_img):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    font = pygame.font.SysFont('Segoe UI', 22, bold=False)
    big_font = pygame.font.SysFont('Segoe UI', 32, bold=True)
    title_font = pygame.font.SysFont('Segoe UI', 40, bold=True)
    clock = pygame.time.Clock()

    bots_template = [
        (0, 0, (255, 0, 0), strategies[0], strategy_names[0]),
        (GRID_SIZE-1, 0, (0, 128, 255), strategies[1], strategy_names[1]),
        (0, GRID_SIZE-1, (0, 200, 0), strategies[2], strategy_names[2]),
        (GRID_SIZE-1, GRID_SIZE-1, (255, 128, 0), strategies[3], strategy_names[3])
    ]
    bots = [Bot(*args) for args in bots_template]
    performance = {bot.name: {'wins': 0, 'total_score': 0, 'total_turns': 0} for bot in bots}

    for round_num in range(1, total_rounds+1):
        for i, args in enumerate(bots_template):
            bots[i].x, bots[i].y = args[0], args[1]
            bots[i].score = 0
            bots[i].turns_taken = 0

        points = generate_points()
        turn = 0
        max_turns = 100
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                elif event.type == pygame.VIDEORESIZE:
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if screen.get_flags() & pygame.FULLSCREEN:
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        else:
                            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

            if turn == 0:
                render_game_screen(
                    screen, background_img, bots, points, round_num, turn,
                    font, big_font, GRID_SIZE, CELL_SIZE, INFO_HEIGHT,
                    SCREEN_WIDTH, SCREEN_HEIGHT, CARD_COLOR, CARD_BORDER,
                    TITLE_COLOR, SCORE_FONT_COLOR, GRID_LINE_COLOR, POINT_COLOR
                )
                pygame.time.wait(350)
                turn += 1
                continue

            for bot in bots:
                bot.move(None, points, bots)
                if (bot.x, bot.y) in points:
                    bot.score += 1
                    points.remove((bot.x, bot.y))
                    
            render_game_screen(
                screen, background_img, bots, points, round_num, turn,
                font, big_font, GRID_SIZE, CELL_SIZE, INFO_HEIGHT,
                SCREEN_WIDTH, SCREEN_HEIGHT, CARD_COLOR, CARD_BORDER,
                TITLE_COLOR, SCORE_FONT_COLOR, GRID_LINE_COLOR, POINT_COLOR
            )
            pygame.time.wait(350)
            clock.tick(60)
            turn += 1

            if not points or turn > max_turns:
                running = False

        winner_bot = max(bots, key=lambda b: b.score)
        performance[winner_bot.name]['wins'] += 1
        for bot in bots:
            performance[bot.name]['total_score'] += bot.score
            performance[bot.name]['total_turns'] += turn

    result = show_final_results(
        screen, bots, performance, total_rounds, background_img
    )

    if result == "menu":
        return  # 回主選單

def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("AI Battle Bots")
    background_img = pygame.image.load("image/background.png").convert()

    while True:
        total_rounds, strategies, strategy_names = main_menu(screen, background_img)
        run_game(screen, total_rounds, strategies, strategy_names, background_img)

if __name__ == "__main__":
    main()