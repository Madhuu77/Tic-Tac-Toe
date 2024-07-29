import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 400
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
RED = (255, 0, 0)
BG_COLOR = (50, 50, 50)  # Dark background
LINE_COLOR = (200, 200, 200)  # Light lines for contrast
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BUTTON_COLOR = (180, 180, 180)
BUTTON_HOVER_COLOR = (150, 150, 150)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Draw lines
def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)

# Draw figures
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Check winner
def check_winner(player):
    # Vertical
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # Horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # Asc diagonal
    if board[2][0] == board[1][1] == board[0][2] == player:
        draw_asc_diagonal(player)
        return True

    # Desc diagonal
    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_desc_diagonal(player)
        return True

    return False

# Draw winning lines
def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2

    if player == 'X':
        color = CROSS_COLOR
    elif player == 'O':
        color = CIRCLE_COLOR

    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 100 - 15), WIN_LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2

    if player == 'X':
        color = CROSS_COLOR
    elif player == 'O':
        color = CIRCLE_COLOR

    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH)

def draw_asc_diagonal(player):
    if player == 'X':
        color = CROSS_COLOR
    elif player == 'O':
        color = CIRCLE_COLOR

    pygame.draw.line(screen, color, (15, HEIGHT - 100 - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH)

def draw_desc_diagonal(player):
    if player == 'X':
        color = CROSS_COLOR
    elif player == 'O':
        color = CIRCLE_COLOR

    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 100 - 15), WIN_LINE_WIDTH)

# Restart game
def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    global board, player, game_over
    player = 'X'
    game_over = False
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Computer move
def computer_move():
    available_moves = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] is None]
    if available_moves:
        row, col = random.choice(available_moves)
        board[row][col] = 'O'
        if check_winner('O'):
            return True
    return False

# Draw button
def draw_button():
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(WIDTH // 4, HEIGHT - 80, WIDTH // 2, 50)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Restart", True, (0, 0, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

# Main loop
player = 'X'
game_over = False
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            if not game_over:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if clicked_row < 3 and board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player
                    if check_winner(player):
                        game_over = True
                    player = 'O'
                    if not game_over and computer_move():
                        game_over = True
                    player = 'X'
            # Check if reset button is clicked
            elif draw_button().collidepoint(mouseX, mouseY):
                restart()

    draw_figures()
    draw_button()
    pygame.display.update()
