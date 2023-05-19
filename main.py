import numpy as np
import random
import pygame
import math


ROWS = 6
COLUMNS = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AGENT_PIECE = 2

WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def isValidLocation(board, col):
    return board[ROWS - 1][col] == 0

def get_next_open_row(board, col):
    r = 0
    while r < ROWS:
        if board[r][col] == 0:
            return r
        r += 1

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations
    c = 0
    while c < COLUMNS - 3:
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True
        c += 1

    # Check vertical locations
    c = 0
    while c < COLUMNS:
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True
        c += 1

    # Check positively sloped diaganols
    c = 0
    while c < (COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True
        c += 1

    # Check negatively sloped diaganols
    c = 0
    while c < (COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True
        c += 1


def evaluate_window(window, piece):
    score = 0
    opponent = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent = AGENT_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    r = 0
    while r < (ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
        r += 1

    ## Score Vertical
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AGENT_PIECE) or len(get_valid_moves(board)) == 0


def get_valid_moves(board):
    valid_moves = []
    for col in range(COLUMNS):
        if isValidLocation(board, col):
            valid_moves.append(col)
    return valid_moves


def pick_best_move(board, piece):
    valid_moves = get_valid_moves(board)
    best_score = -10000
    best_col = random.choice(valid_moves)
    for col in valid_moves:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col



board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 80

width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("arial", 75)

turn = random.randint(PLAYER, AI)


# Create window

window = tk.Tk()
window.title("Choose game difficulty and algorithm")
window.geometry("500x400")

# Difficulty selection
tk.Label(window, text="Choose difficulty:").pack()
diff_var = tk.StringVar(value="easy")
tk.Radiobutton(window, text="Easy", variable=diff_var, value="easy").pack()
tk.Radiobutton(window, text="Medium", variable=diff_var, value="medium").pack()
tk.Radiobutton(window, text="Hard", variable=diff_var, value="hard").pack()

# Algorithm selection
tk.Label(window, text="Choose algorithm:").pack()
tk.Button(window, text="MiniMax", command=algo1).pack()
tk.Button(window, text="Alpha Beta", command=algo2).pack()

# Submit button
tk.Button(window, text="start game", command=lambda: set_difficulty(diff_var.get())).pack()

window.mainloop()

if(Algo==1):

    print(" \n Hello from minimax with difficulty  ", difficulty)


elif(Algo==2):

    print(" \n Hello from alpha beta with difficulty  ", difficulty)

while not game_over:

    pygame.display.update()

    if turn == PLAYER:

        pygame.time.wait(800)

        col=random.randint(0,6)

        if isValidLocation(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)



    if winning_move(board, PLAYER_PIECE):
        label = myfont.render("Player 1 WON ..", 1, (255,0,0))
        screen.blit(label, (40, 10))
        game_over = True

    turn += 1
    turn = turn % 2

    print_board(board)

    print("\n")
    draw_board(board)


    if turn == AI and not game_over:

        pygame.time.wait(800)


        if(Algo==1):

            col, score = minimax(board, difficulty, True)
        elif(Algo==2):

            col, minimax_score = minimax_alpha_beta(board, difficulty, -math.inf, math.inf, True)



        if isValidLocation(board, col):

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AGENT_PIECE)

            if winning_move(board, AGENT_PIECE):
                label = myfont.render("AI WON..", 1, (0,0,255))

                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            print("\n")
            draw_board(board)

            turn += 1
            turn = turn % 2


    if game_over:
        pygame.time.wait(3000)
    
def minimax(board, depth, maximizingPlayer):

    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AGENT_PIECE):
                return None, 100000000000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -10000000000000
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, AGENT_PIECE)
    if maximizingPlayer:
        value = -math.inf
        column = None
        for col in valid_moves:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AGENT_PIECE)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = None
        for col in valid_moves:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value    

def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, (255,255,0), (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, (255,255,255) , (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, (255,0,0), (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AGENT_PIECE:
                pygame.draw.circle(screen, (0,0,255), (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 80

width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("arial", 75)

turn = random.randint(PLAYER, AI)

def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AGENT_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AGENT_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AGENT_PIECE)
            new_score = minimax_alpha_beta(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax_alpha_beta(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
