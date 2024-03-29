import discord
from discord.ext import commands
import random
import functions
import asyncio
import math

COLUMN_COUNT = 7
ROW_COUNT = 6
WINDOW_COUNT = 4 # amount in a row required to win (typically 4)

DEPTH = 6

def botembed(title):
    embed = functions.embed("Connect 4 - " + title, color=0x8f0000)
    return embed

def create_board():
    board = []
    for _ in range(ROW_COUNT):
        line = []
        for _ in range(COLUMN_COUNT):
            line.append(0)
        board.append(line)
    return board

def error(errormsg):
    embed = functions.error("Connect 4", errormsg)
    return embed

def score_window(window, piece):
    score = 0
    opp_piece = (1 if piece == 2 else 2)
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def print_board(board):
   
    b = board[::-1]
    strboard = ""
    for line in b:
        prline = "`"
        c = 0
        for char in line:
            if char == 0:
                prline = prline + " "
            elif char == 1:
                prline = prline + "●"
            else:
                prline = prline + "○"
            if c < 6:
                prline = prline + " "
            c += 1
        prline = prline + "`\n"
        strboard = strboard + prline
    strboard = strboard.strip()
    strboard = "`1 2 3 4 5 6 7`\n" + strboard
    
    return strboard

def is_tie(board):
    valid_locations = get_valid_locations(board)
    if len(valid_locations) == 0:
        return True
    return False



def drop_piece(board, row, col, piece):
    board[row][col] = piece
    return board


def is_valid_location(board, col):
    try:
        return board[ROW_COUNT - 1][col] == 0
    except:
        return False


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


def winning_move(board, piece):
    for r in range(ROW_COUNT):
        row_array = [i for i in list(board[r][:])]
        for c in range(COLUMN_COUNT - (WINDOW_COUNT - 1)):
            window = row_array[c:c+WINDOW_COUNT]
            if window.count(piece) == 4:
                return True

    for c in range(COLUMN_COUNT):
        col_array = []
        for row in board:
            col_array.append(row[c])
        for r in range(ROW_COUNT - (WINDOW_COUNT - 1)):
            window = col_array[r:r+WINDOW_COUNT]
            if window.count(piece) == 4:
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_COUNT)]
            if window.count(piece) == 4:
                return True

    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_COUNT)]
            if window.count(piece) == 4:
                return True
    return False


def random_move():
    return random.randint(0, COLUMN_COUNT-1)


def score_window(window, piece):
    score = 0
    opp_piece = (1 if piece == 2 else 2)
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0
    for r in range(ROW_COUNT):
        row_array = [i for i in list(board[r][:])]
        for c in range(COLUMN_COUNT - (WINDOW_COUNT - 1)):
            window = row_array[c:c+WINDOW_COUNT]
            score += score_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = []
        for row in board:
            col_array.append(row[c])
        for r in range(ROW_COUNT - (WINDOW_COUNT - 1)):
            window = col_array[r:r+WINDOW_COUNT]
            score += score_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_COUNT)]
            score += score_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_COUNT)]
            score += score_window(window, piece)

    return score


def copy(board):
    new = []
    for row in board:
        line = []
        for item in row:
            line.append(item)
        new.append(line)
    return new


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_column = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = copy(board)
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_column = col
    return best_column

def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or is_tie(board)


def minimax(board, depth, alpha, beta, maximizingplayer, piece):
    board = board.copy()
    opp_piece = (1 if piece == 2 else 2)
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, piece):
                return (None, 10000000000000)
            elif winning_move(board, opp_piece):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, piece))
    if maximizingplayer:
        column = random.choice(valid_locations)
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            bcopy = copy(board)
            drop_piece(bcopy, row, col, piece)
            new_score = minimax(bcopy, depth - 1, alpha, beta, False, piece)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        column = random.choice(valid_locations)
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            bcopy = copy(board)
            drop_piece(bcopy, row, col, opp_piece)
            new_score = minimax(bcopy, depth - 1, alpha, beta, True, piece)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

async def get_next_move(ctx, board, turn):
    await ctx.trigger_typing()
    nb = board.copy()
    col, _ = minimax(nb, DEPTH, -math.inf, math.inf, True, turn + 1)
    invalid = not is_valid_location(board, col)
    while invalid:
        nb = board.copy()
        col, _ = minimax(nb, DEPTH, -math.inf, math.inf, True, turn + 1)
        invalid = not is_valid_location(board, col)
    return col

class Connect4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playing = False
        self.config = None

    @commands.command(aliases=["c4"])
    async def connect4(self, ctx):
        
        if self.playing:
            embed = error("🚫 " + self.bot.response(2) + " we're already playing a game of Connect 4 right now!")
            return await ctx.send(embed=embed)
        self.playing = True

        order = ["You", "Me"]
        random.shuffle(order)

        embed = botembed("Game Started")
        if order[0] == "Me":
            piece = "🟡"
        else:
            piece = "🔴"
        desc = f"{piece} " + self.bot.response(1) + " I started a game of Connect 4 for us.\n"
        f = order[0]
        aimove = False
        if f == "Me":
            f = "I"
            aimove = True
        desc = desc + "{}'ll go first. Good luck!\nType `start` to start.".format(f)

        embed.description = desc

        await ctx.send(embed=embed)
        await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.message.author and m.content.strip().lstrip().lower() == "start")

        turn = 0
        winner = ""
        win = False
        piece = "●" if aimove else "○"

        board = create_board()
        t = 0
        if not aimove:
            turn = 1
            embed = botembed("Your Turn")
            desc = "```Turn {} // You are {}```\n".format(t, piece)
            desc = desc + print_board(board) + "\nIt's your turn.\nChoose a column `1-7` to place a piece."
            embed.description = desc
            await ctx.send(embed=embed)
        while not win:
            if aimove:
                
                t += 1
                embed = botembed("My Turn")
                desc = "```Turn {} // You are {}```\n".format(t, piece)
                desc = desc + print_board(board) + "\nIt's my turn. Let me think..."
                embed.description = desc
                message = await ctx.send(embed=embed)
                
                col = await get_next_move(ctx, board, turn)
            
                row = get_next_open_row(board, col)
                board = drop_piece(board, row, col, turn + 1)

            else:
            
                def check(message):
                    if message.author == ctx.message.author and message.channel == ctx.channel:
                        content = message.content.strip().lstrip().lower()
                        if content.isdigit():
                            col = int(content)
                            if is_valid_location(board, col-1):
                                return True

                message = await self.bot.wait_for("message", check=check)
                col = int(message.content) - 1
                
                row = get_next_open_row(board, col)
                board = drop_piece(board, row, col, turn + 1)
                


            if winning_move(board, turn + 1):
                embed = botembed("Game Over")
                desc = "```Turn {} // {}```\n".format(t, "Win" if not aimove else "Loss")
                desc = desc + print_board(board) + "\n{} won! {}\nGood game! I hope I can play with you again!".format("You" if not aimove else "I", self.bot.response(5) if not aimove else "")
                embed.description = desc
                await ctx.send(embed=embed)
                break
            elif is_tie(board):
                embed = botembed("Game Over")
                desc = "```Turn {} // Tie```\n".format(t)
                desc = desc + print_board(board) + "\nWe tied! {}\nGood game! I hope I can play with you again!".format(self.bot.response(5))
                embed.description = desc
                await ctx.send(embed=embed)
                break
            elif aimove:
                t += 1
            
                embed = botembed("Your Turn")
                desc = "```Turn {} // You are {}```\n".format(t, piece)
                desc = desc + print_board(board) + "\nIt's your turn.\nChoose a column `1-7` to place a piece."
                embed.description = desc
                await message.edit(embed=embed)
            turn = (turn + 1) % 2
            if aimove is not None:
                aimove = not(aimove)
        self.playing = False



def setup(bot):
    bot.add_cog(Connect4(bot))
