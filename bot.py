import discord
from time import time
import asyncio
from discord.ext import commands
from mpmath import *
import numpy as np
import cmath as c
from math import *
from scipy.special import *
from sympy import primerange
from connect4 import Game as connect4game
import pygame as py
from arithmetic import ArithmeticGame
import itertools

# CONNECT 4 GAMES
connect4games = {}

# ARITHMETIC GAMES
arithmetic_games = {}

# PLOTTING QUERIES
current_query = {}

# PENDING FOR HELP
people = {}
messages = {
    "main": f'Game commands help: ,helpme game\nNormal commands help: ,helpme normal',
    "game": f'For more info input ,helpme name\n All the available game command names are: connect4 and ar',
    "normal": f'For more info input ,helpme name\nAll the available command names are: fap, fer, prod, sum, pef), and int',
    "fap": f'The fap command is the functional inverse of the gamma function, the function accepts 1 argument, x>1.461632.\nThe function can be used like this: ,fap number',
    "fer": f'The fer command is the factorial, the function accepts 1 argument, x>-1.\nThe function can be used like this: ,fer number',
    "prod": f'The prod command is the mathematical product, the function accepts 3 arguments:\nthe lower bound, upper bound and the function you want to apply the product on(Note: the function must be in function of x).\nThe function can be called like this: ,prod lower upper function',
    "sum": f'The sum command is the mathematical sum, the functions accepts 3 arguments:\nthe lower bound, upper bound and the function you want to apply the product on(Note: the function must be in function of x).\nThe function can be called like this: ,sum lower upper function',
    "pef)": f'The pef) function is a calculator, you can give it any mathematical expression and it will calculate it for you(Note: you can\'t use spaces).\n The function can be used like this: ,pef) (5+5)*2+5^6',
    "int": f'The int function is a numerical integral calculator, the function accepts 3 arguments:\nthe lower bound, upper bound and the function you want to integrate(Note: the function must be in function of x).\nThe function can be called like this: ,int 0 5 x^2',
    "connect4": f'The first players creates a game by calling: ,connect4.\nThe second can then join by doing exactly the same, and to place a coin use the command: ,connect4 number (number being a valid column number)',
    "ar": f'The ar game is a simple addition game, you can call it with ,ar (by default 6 seconds of time for numbers ranging from 0 to 10k)\n or with ,ar time lowerbound upperbound which will initialize a game with the time limit and numbers you like.'
}


# HELPER FUNCTIONS
def lo(x):
    return np.log((x + 0.036534) / (sqrt(2 * pi)))


def lambert(x):
    return lambertw(x)


def inversegamma(x):
    return lo(x) / lambert(lo(x) / e) - 0.5


def factorial(x):
    res = 1
    for i in range(2, x + 1):
        res *= i
    return res


def process_message(message):
    to_check = message.lower()
    not_valid = ['import', 'ctx', 'exec', 'sys', 'join', 'eval', 'if', '\'', 'while', 'for', 'from', 'os.', 'chr',
                 'ord', 'str', 'int', 'not', 'float', 'list', 'dict', 'set', '{', '}']
    if message == None:
        return None

    for i in not_valid:
        if i in to_check:
            return False
    return message.replace('^', '**').strip()


def check_if_integer(num):
    try:
        int(num)
        return True
    except:
        return False


client = commands.Bot(command_prefix=',')


# COMMAND FUNCTIONS
@client.command(aliases=['fap!'])
async def fap(ctx, message):
    try:
        channel = ctx.channel
        num = process_message(message)
        if not num:
            raise Exception('I know Python!')
        else:
            num = float(num)

        if num > 1.461632:
            to_send = inversegamma(num).real
            await channel.send(to_send)
        else:
            await channel.send('The domain of the inverse gamma is x > 1.461632.')
    except:
        pass


@client.command(aliases=['fer?'])
async def fer(ctx, message):
    try:
        channel = ctx.channel
        num = process_message(message)

        if not num:
            raise Exception('I know Python!')
        else:
            num = int(num)

        if -1 < num < 10001:
            to_send = format(factorial(num), 'd')
            while len(to_send) > 2000:
                await channel.send(to_send[:2000])
                to_send = to_send[2000:]
            await channel.send(to_send)
    except:
        pass


@client.command()
async def data(ctx, eerste=0.0, tweede=0.0, derde=0.0, vierde=0.0, vijfde=0.0, zesde=0.0, project=0.0, extra=0.0):
    try:
        channel = ctx.channel
        eerste = float(eerste)
        tweede = float(tweede)
        derde = float(derde)
        vierde = float(vierde)
        vijfde = float(vijfde)
        zesde = float(zesde)
        project = float(project)
        extra = float(extra)
        if eerste > 4:
            eerste = 4
        if eerste < 0:
            eerste = 0
        if tweede > 4:
            tweede = 4
        if tweede < 0:
            tweede = 0
        if derde > 4:
            derde = 4
        if derde < 0:
            derde = 0
        if vierde > 4:
            vierde = 4
        if vierde < 0:
            vierde = 0
        if vijfde > 4:
            vijfde = 4
        if vijfde < 0:
            vijfde = 0
        if zesde > 3:
            zesde = 3
        if zesde < 0:
            zesde = 0
        if project > 100:
            project = 100
        if project < 0:
            project = 0
        if extra > 1:
            extra = 1
        if extra < 0:
            extra = 0
        totaal = ((eerste + tweede + derde + vierde) * 10 / 4 + vijfde * 15 / 4 + zesde * 15 / 3 + project * 30 / 100) / 5
        totaal = totaal + extra
        if totaal > 20:
            await channel.send('20/20')
        else:
            await channel.send(f'{totaal:.2f}/20')
    except:
        await channel.send('Gij dikke mongool stuur met deze formaat:,data 4 4 4 4 4 3 100 1')


@client.command()
async def prod(ctx, lower, upper, function):
    try:
        function = process_message(function)
        lower = process_message(lower)
        upper = process_message(upper)

        if not function or not lower or not upper:
            raise Exception('I know Python!')
        else:
            lower = int(lower)
            upper = int(upper)

        channel = ctx.channel
        f = lambda x: eval(function)
        if lower < upper:
            if abs(upper - lower) > 10000:
                upper = lower + 10000
            res = 1
            for i in range(lower, upper + 1):
                new = f(i)
                if abs(f(i)) < 10 ** (-10) and new != 0:
                    break
                res *= new
            await channel.send(res)

    except:
        pass


@client.command(aliases=['pef)', 'f'])
async def pef(ctx, message):
    try:
        channel = ctx.channel
        message = process_message(message)

        if not message:
            raise Exception('I know Python!')
        else:
            await channel.send(eval(message))
    except:
        await channel.send('an error occured')


@client.command(aliases=['sum'])
async def som(ctx, lower, upper, function):
    try:
        function = process_message(function)
        lower = process_message(lower)
        upper = process_message(upper)

        if not function or not lower or not upper:
            raise Exception('I know Python!')
        else:
            lower = int(lower)
            upper = int(upper)

        channel = ctx.channel
        f = lambda x: eval(function)
        if lower < upper:
            if abs(upper - lower) > 10000:
                upper = lower + 10000
            res = 0
            for i in range(lower, upper + 1):
                new = f(i)
                if abs(new) < 10 ** (-10) and new != 0:
                    break
                res += new
            await channel.send(res)
    except:
        pass


@client.command(aliases=['int'])
async def integral(ctx, lower, upper, function=None):
    try:
        channel = ctx.channel
        lower = process_message(lower)
        upper = process_message(upper)
        function = process_message(function)

        lower = eval(lower)
        upper = eval(upper)

        f = lambda x: eval(function)
        run = True
        res = 0
        if lower < upper:
            if abs(lower - upper) > 10000:
                upper = lower + 10000
            start = lower + 0.0001
            end = upper - 0.0001

            dx = (upper - lower) / 10000
            lst = [0, 0]
            while start + dx < end and run:
                lst[0] += f(start) * dx
                start += dx
                new = f(start) * dx
                lst[1] += f(start) * dx
                if abs(new) < 10 ** (-280):
                    break
            if run:
                res = sum(lst) / 2
                if abs(res) < 10 ** -3:
                    res = 0

            await channel.send(res)
    except:
        pass


@client.command()
async def filtz(ctx, lower, upper):
    try:
        channel = ctx.channel
        lower = process_message(lower)
        upper = process_message(upper)

        if not lower or not upper:
            raise Exception('I know Python!')
        else:
            upper = int(upper)
            lower = int(lower)

        if lower >= 0 and upper >= 0 and upper > lower:
            filtz = []
            for i in range(lower, upper + 1):
                getal = []
                num = i
                while num != 0:
                    getal.append(num % 10)
                    num //= 10

                som = sum(getal)
                prod = 1
                for j in getal:
                    prod *= j

                if prod * som == i:
                    filtz.append(i)
            if len(filtz):
                await channel.send('The Filtz numbers are:\n' + ' '.join(list(map(str, filtz))))
            else:
                await channel.send('There are no Filtz numbers.')
        else:
            await channel.send("Give valid bounds please.")

    except:
        await channel.send("Give valid bounds please.")


@client.command()
async def prime(ctx, a, b):
    try:
        channel = ctx.channel
        a = process_message(a)
        b = process_message(b)

        if not a or not b:
            raise Exception('I know Python!')
        else:
            a = int(a)
            b = int(b)
        if b > 1000000:
            b = 1000000

        await channel.send(list(primerange(a, b)))

    except:
        pass


@client.command()
async def helpme(ctx, command=None):
    try:
        author = ctx.author
        channel = ctx.channel

        if command is None and author not in people:
            await channel.send('```' + messages['main'] + '```')
            people[author] = time()
        elif command is not None and author in people:
            people[author] = time()
            if command in messages:
                await channel.send('```' + messages[command.strip()] + '```')
    except:
        pass


@client.command(aliases=['ploot'])
async def plot(ctx, first=None, second=None, third=None, fourth=None):
    try:
        comms = [first, second, third, fourth]
        channel = ctx.channel
        py.font.init()

        def draw_grid(screen, width, height):
            block = 50
            for i in range(width // block):
                for j in range(height // block):
                    py.draw.rect(screen, (200, 200, 200), (i * block, j * block, block, block), 1)

        def draw_axis(screen, width, height):
            py.draw.line(screen, (0, 0, 0), (width // 2, 0), (width // 2, height), 3)
            py.draw.line(screen, (0, 0, 0), (0, height // 2), (width, height // 2), 3)
            block = 50
            font = py.font.Font('freesansbold.ttf', 15)
            for i in range(1, 20):
                py.draw.line(screen, (0, 0, 0), (width // 2 - 5, i * block), (width // 2 + 5, i * block), 3)
                if i != 10:
                    number = font.render(f'{10 - i}', True, (0, 0, 0))
                    screen.blit(number, (width // 2 + 10, i * block - 8))
                py.draw.line(screen, (0, 0, 0), (i * block, height // 2 - 5), (i * block, height // 2 + 5), 3)
                if i != 10:
                    number = font.render(f'{- 10 + i}', True, (0, 0, 0))
                    screen.blit(number, (i * block - 4, height // 2 - 20))

        def plot_function(screen, points):
            for i in points:
                if len(i) < 10:
                    continue
                old_x = i[0][0]
                old_y = i[0][1]
                yes_no = i[-1]
                point = i[1:-1]
                for x, y in point:
                    if not yes_no:
                        if ((x - old_x) ** 2 + (y - old_y) ** 2) ** 0.5 < 100:
                            py.draw.line(screen, (0, 0, 255), (int(old_x), int(old_y)), (int(x), int(y)), 2)
                        old_x = x
                        old_y = y
                    else:
                        py.draw.circle(screen, (0, 0, 255), (int(x), int(y)), 0)

        points = []
        run = True
        for index, el in enumerate(comms):
            if el == None:
                if index == 0:
                    run = False
                    break
                else:
                    break
            point = []
            i = el.replace('^', '**')
            if i.count('..') == 0 and i.count('=') == 0:
                dx = 0.001
                x = -10
                function = lambda x: eval(i.strip())
                while x < 10:
                    x = x + dx
                    shifted_x = x * 50.0 + 500.0
                    y = (-function(x) * 50.0 + 500.0)
                    if isinstance(y, float):
                        if 0 <= y <= 1000:
                            point.append((shifted_x, y))
                point.append(False)
            if i.count('..') == 3 and i[0] != 's':
                new = i.split('..')
                funcx = lambda x: eval(new[0])
                funcy = lambda x: eval(new[1])
                x = eval(new[2])
                dx = 0.001
                lim = eval(new[3])
                while x < lim:
                    x = x + dx
                    x_coord = (funcx(x) * 50.0 + 500.0)
                    y_coord = (-funcy(x) * 50.0 + 500.0)
                    if isinstance(x_coord, float) and isinstance(y_coord, float):
                        if 0 <= y_coord <= 1000 and 0 <= x_coord <= 1000:
                            point.append((x_coord, y_coord))
                point.append(False)

            if i.count('..') == 3 and i[0] == 's':
                new = i.split('..')
                x = int(new[1])
                lim = int(new[2])
                if abs(lim - x) > 20:
                    lim = x + 20
                func = ''
                for i in range(x, lim + 1):
                    f = new[3]
                    func += f.replace('I', f'{(i)}') + '+'
                function = lambda x: eval(func[:-1])
                dx = 0.001
                x = -10
                while x < 10:
                    x = x + dx
                    shifted_x = x * 50.0 + 500.0
                    y = (-function(x) * 50.0 + 500.0)
                    if isinstance(y, float):
                        if 0 <= y <= 1000:
                            point.append((shifted_x, y))
                point.append(False)

            if i.count('=') == 1:
                new = i.split('=')
                f = new[0] + '-' + '(' + new[1] + ')'
                function = lambda x, y: eval(f)
                dx = 0.02
                x = -10
                while x + dx < 10:
                    x += dx
                    y = -10 + dx
                    while y + dx < 10:
                        res = function(x, -y) * 1.0
                        if isinstance(res, float):
                            if abs(res) < 0.1:
                                x_shifted = x * 50.0 + 500
                                y_shifted = y * 50.0 + 500
                                point.append((x_shifted, y_shifted))
                        y += dx
                point.append(True)
            points.append(point)
        if run:
            WIDTH = 1000
            HEIGHT = 1000
            screen = py.display.set_mode((WIDTH, HEIGHT))
            screen.fill((255, 255, 255))
            draw_grid(screen, WIDTH, HEIGHT)
            draw_axis(screen, WIDTH, HEIGHT)
            plot_function(screen, points)
            py.image.save(screen, "screenshot.jpg")
            py.quit()
            await channel.send(file=discord.File("screenshot.jpg"))
    except:
        pass


@client.command(aliases=['successor'])
async def succ(ctx, num):
    try:
        channel = ctx.channel
        num = int(num)
        s = ''
        if 0 < num < 241:
            for i in range(num):
                s += 'succ(0)+'
            s = s[:-1]
            await channel.send(f"{num} = {s} = {num}*succ(0)")

        else:
            await channel.send(
                "Are you trying to break discord with a number as long as my dick? try something smaller lmao.")
    except:
        pass


# GAME FUNCTIONS
@client.command()
async def connect4(ctx, move=None):
    try:
        channel = ctx.channel
        author = ctx.author
        draw = False
        if channel not in connect4games and move is None:
            connect4games[channel] = connect4game(author)
            await channel.send(f"```Player 1 joined: {author}\n Waiting on Player 2 ...```")
        elif channel in connect4games:
            game = connect4games[channel]

            if game.player2.name is None and move is None and author != game.player1.name:
                game.player2.name = author
                game.reset_time()
                game.run = True
                await channel.send(f"```Player 2 joined: {author}\n Game launching...```")
                await asyncio.sleep(2)
                await channel.send("```\n" + game.return_grid() + f"\n{game.player1.name}'s turn\n```")

            elif author == game.player1.name and game.player2.name is None and move is None:
                await channel.send("```You can't join a game twice, you dummy lmao```")

            elif author == game.player1.name and game.player2.name is None and move == "stop":
                await channel.send(f"```Game has been stopped```")
                del connect4games[channel]

            elif author == game.player1.name and game.player2.name is None and move is not None:
                await channel.send("```Wait for an other person to join before trying moves out, you dummy lmao```")

            if game.run:
                if game.check_player(author):
                    if move == 'stop':
                        del connect4games[channel]
                    elif move is not None:
                        if check_if_integer(move):
                            move = int(move) - 1
                            if author == game.player1.name and game.player1.turn == 1:
                                valid = game.change(move, game.player1.sign)
                                if valid:
                                    draw = True
                                    game.change_status()
                                    game.reset_time()
                            elif author == game.player2.name and game.player2.turn == 1:
                                valid = game.change(move, game.player2.sign)
                                if valid:
                                    draw = True
                                    game.change_status()
                                    game.reset_time()
                            has_won = game.check()
                            if draw and not has_won:
                                await channel.send(
                                    "```\n" + game.return_grid() + f"\n{game.player1.name if game.player1.turn == 1 else game.player2.name}'s turn```")
                            elif has_won:
                                await channel.send(f'```\n{game.winner} has won!\n' + game.return_grid() + "\n```")
                                del connect4games[channel]
                        else:
                            pass
                else:
                    pass
            else:
                pass
    except:
        pass


@client.command()
async def ar(ctx, first=None, second=None, third=None):
    try:
        channel = ctx.channel
        author = ctx.author
        if channel not in arithmetic_games and first is None and second is None and third is None:
            arithmetic_games[channel] = ArithmeticGame(author)
            await channel.send(arithmetic_games[channel].give_question())

        elif channel not in arithmetic_games and check_if_integer(first) and check_if_integer(
                second) and check_if_integer(third):
            if int(second) < int(third):
                arithmetic_games[channel] = ArithmeticGame(author, first, second, third)
                print(arithmetic_games)
                await channel.send(arithmetic_games[channel].give_question())
            else:
                await channel.send(f'```Give a valid range you dummy, lmao```')

        else:
            game = arithmetic_games[channel]
            if author == game.player:
                if first is not None and second is None and third is None:
                    if first == "stop":
                        del arithmetic_games[channel]
                        await channel.send(f'```Game was deleted.```')

                    if first.isdigit():
                        first_condition = game.valid_time()
                        second_condition = game.valid_num(first)
                        if first_condition and second_condition:
                            del arithmetic_games[channel]
                            await channel.send(f'```Congratulations, you got it right!```')

                        elif first_condition and not second_condition:
                            del arithmetic_games[channel]
                            await channel.send(f'```You got it wrong dummy, the answer is {game.res}```')

                        elif not first_condition and second_condition:
                            del arithmetic_games[channel]
                            await channel.send(f'```You\'re as slow as my grandma, but you got it right tho...```')

                        elif not first_condition and not second_condition:
                            del arithmetic_games[channel]
                            await channel.send(
                                f'```You\'re as slow as my grandma, and you got it wrong lmao, sucks to suck...```')
    except:
        pass


# EVENT FUNCTIONS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send('Gij dikke mongool stuur met deze formaat: ,data 4 4 4 4 4 3 100 1')


@client.event
async def on_message(message):
    try:
        author = str(message.author).strip()
        content = message.content.split()
        content = [str(i).lower() for i in content]
        if any(i for i in content if 'lol' in (''.join(i for i, _ in itertools.groupby(i))).lower()):
            await message.add_reaction('❤')
        if any(i for i in content if
               'gay' in ''.join(list(dict.fromkeys(list(i.lower()))))) and author != 'FerFap#2972':
            await message.add_reaction('🏳️‍🌈')
    except:
        pass
    await client.process_commands(message)


@client.event
async def on_ready():
    activity = discord.Game(name=",helpme")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot logged in.")


# CHECKING FOR GAMES THAT STOPPED
async def check_timout():
    await client.wait_until_ready()
    while not client.is_closed():
        need_to_delete = []

        for channel, game in connect4games.items():
            if time() - game.time > 120:
                need_to_delete.append(channel)

        for i in need_to_delete:
            del connect4games[i]

        for channel, game in arithmetic_games.items():
            if (time() - game.time) > game.limit + 60:
                need_to_delete.append(channel)

        for i in need_to_delete:
            del arithmetic_games[i]

        for someone, elapsed in people.items():
            if time() - elapsed > 30:
                need_to_delete.append(someone)

        for i in need_to_delete:
            del people[i]

        await asyncio.sleep(10)


TOKEN = ""
client.run(TOKEN)