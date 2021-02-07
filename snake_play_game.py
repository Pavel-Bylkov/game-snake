#!/usr/bin/python
# -*- coding: utf-8 -*-
import play
import pygame

# https://github.com/replit/play  - описание библиотеки Play

# pip3 install replit-play - сразу устанавливает и библиотеку play и pygame

# Todo 1 Добавить зелье для ускорения и замедления
# Todo 2 Условие Победы
# Todo 3 Добавить препятствия - если врезаешься, уменьшать змейку или геймовер
# ToDo 4 Разбить игру на файлы для удобства чтения
# TODO 5 Исправить чтение и сохранние рекордов в файл, в зашифрованном виде - защита от Читинга


# play.screen.width = 800
# play.screen.height = 600
head = play.new_image(image="голова.png", x=0, y=0, size=10, angle=90)

apple = play.new_image(image="Apple.png", x=0, y=0, size=3, angle=0)
score = play.new_text(words='', x=350, y=280, angle=0, font=None, font_size=45, color='white', transparency=100)
player_name = play.new_text(words='', x=-350, y=280, angle=0, font=None, font_size=45, color='white', transparency=100)

finish = play.new_image(image="gameover.jpeg", x=0, y=0, size=120, angle=0)
# gameover = play.new_text(words='GAME OVER', x=0, y=0, angle=0, font=None, font_size=180, color='green', transparency=100)

sound_eat = pygame.mixer.Sound('Bite.wav')
sound_eat.set_volume(0.5)
sound_game_over = pygame.mixer.Sound('Bite.wav')
pygame.mixer.music.load('bethoven.ogg')
pygame.mixer.music.set_volume(0.5)

UP_BRD = 270  # Крайня верхняя координата Y
LEFT_BRD = -390  # Координата X
RIGHT_BRD = 390  # Координата X
DOWN_BRD = -290  # Крайня нижняя координата Y

screen = pygame.display.set_mode((800, 600))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

run = True  # для движения головы
speed = 0.4
apples = 0
all_sprites = [head, apple, score, player_name, finish]
body_clone_list = []  # создаем список пустой, в который потом будем добавлять клоны хвоста
bodies_positions = []  # здесь будем хранить координаты каждого клона хвоста
lines = []  # список линий - сетка
borders = []  # список линий - границы, за которые выходить нельзя
stars = []  # Список для отображения звезд

#  Создаем алфавит словари для шифрования
alf_dict_back = {'и': '0', 'Н': '1', 'С': '2', 'о': '3', 'р': '4', 't': '5', 'z': '6', 'h': '7', 'е': '8', ';': '9',
                 'з': 'a', 'А': 'b', 'п': 'c', 'ц': 'd', 'v': 'e', 's': 'f', 'p': 'g', '№': 'h', 'F': 'i', 'ы': 'j',
                 'J': 'k', 'ю': 'l', 'ш': 'm', 'Х': 'n', 'l': 'o', 'ъ': 'p', 'Л': 'q', 'Ю': 'r', 'Ь': 's', 'й': 't',
                 'i': 'u', '?': 'v', 'O': 'w', 'a': 'x', '0': 'y', '"': 'z', '_': 'A', 'в': 'B', '-': 'C', 'ж': 'D',
                 'н': 'E', '4': 'F', 'Ъ': 'G', 'Ж': 'H', 'Д': 'I', 'A': 'J', 'И': 'K', 'W': 'L', 'д': 'M', 'g': 'N',
                 '+': 'O', 'Ш': 'P', 'Ф': 'Q', 'P': 'R', 'R': 'S', 'Z': 'T', ':': 'U', 'b': 'V', 'w': 'W', 'c': 'X',
                 'Ч': 'Y', 'S': 'Z', '%': ' ', 'n': 'а', 'ё': 'б', '5': 'в', 'м': 'г', 'К': 'д', 'B': 'е', 'L': 'ё',
                 'О': 'ж', 'Б': 'з', '6': 'и', '!': 'й', 'f': 'к', 'I': 'л', 'N': 'м', 'Г': 'н', 'H': 'о', 'Р': 'п',
                 ' ': 'р', 'y': 'с', 'U': 'т', 'D': 'у', 'ь': 'ф', '9': 'х', 'r': 'ц', 'e': 'ч', 'г': 'ш', '1': 'щ',
                 'т': 'ъ', 'Я': 'ы', '7': 'ь', 'В': 'э', 'X': 'ю', 'б': 'я', 'Ц': 'А', 'o': 'Б', "'": 'В', 'Т': 'Г',
                 '3': 'Д', 'j': 'Е', 'щ': 'Ё', '2': 'Ж', 'K': 'З', 'q': 'И', 'Э': 'Й', 'd': 'К', 'Q': 'Л', 'а': 'М',
                 'x': 'Н', 'G': 'О', 'T': 'П', 'Ы': 'Р', '8': 'С', '(': 'Т', 'к': 'У', 'Й': 'Ф', 'л': 'Х', 'k': 'Ц',
                 'Е': 'Ч', 'E': 'Ш', 'Щ': 'Щ', 'х': 'Ъ', 'Y': 'Ы', 'с': 'Ь', 'ф': 'Э', 'П': 'Ю', 'У': 'Я', '=': '!',
                 'ч': '"', 'u': "'", 'я': '№', 'М': ';', 'у': '%', 'M': ':', 'C': '?', 'V': '*', 'Ё': '(', 'm': ')',
                 ')': '_', '*': '+', 'э': '-', 'З': '='}

alf_dict = {'0': 'и', '1': 'Н', '2': 'С', '3': 'о', '4': 'р', '5': 't', '6': 'z', '7': 'h', '8': 'е', '9': ';',
            'a': 'з', 'b': 'А', 'c': 'п', 'd': 'ц', 'e': 'v', 'f': 's', 'g': 'p', 'h': '№', 'i': 'F', 'j': 'ы',
            'k': 'J', 'l': 'ю', 'm': 'ш', 'n': 'Х', 'o': 'l', 'p': 'ъ', 'q': 'Л', 'r': 'Ю', 's': 'Ь', 't': 'й',
            'u': 'i', 'v': '?', 'w': 'O', 'x': 'a', 'y': '0', 'z': '"', 'A': '_', 'B': 'в', 'C': '-', 'D': 'ж',
            'E': 'н', 'F': '4', 'G': 'Ъ', 'H': 'Ж', 'I': 'Д', 'J': 'A', 'K': 'И', 'L': 'W', 'M': 'д', 'N': 'g',
            'O': '+', 'P': 'Ш', 'Q': 'Ф', 'R': 'P', 'S': 'R', 'T': 'Z', 'U': ':', 'V': 'b', 'W': 'w', 'X': 'c',
            'Y': 'Ч', 'Z': 'S', ' ': '%', 'а': 'n', 'б': 'ё', 'в': '5', 'г': 'м', 'д': 'К', 'е': 'B', 'ё': 'L',
            'ж': 'О', 'з': 'Б', 'и': '6', 'й': '!', 'к': 'f', 'л': 'I', 'м': 'N', 'н': 'Г', 'о': 'H', 'п': 'Р',
            'р': ' ', 'с': 'y', 'т': 'U', 'у': 'D', 'ф': 'ь', 'х': '9', 'ц': 'r', 'ч': 'e', 'ш': 'г', 'щ': '1',
            'ъ': 'т', 'ы': 'Я', 'ь': '7', 'э': 'В', 'ю': 'X', 'я': 'б', 'А': 'Ц', 'Б': 'o', 'В': "'", 'Г': 'Т',
            'Д': '3', 'Е': 'j', 'Ё': 'щ', 'Ж': '2', 'З': 'K', 'И': 'q', 'Й': 'Э', 'К': 'd', 'Л': 'Q', 'М': 'а',
            'Н': 'x', 'О': 'G', 'П': 'T', 'Р': 'Ы', 'С': '8', 'Т': '(', 'У': 'к', 'Ф': 'Й', 'Х': 'л', 'Ц': 'k',
            'Ч': 'Е', 'Ш': 'E', 'Щ': 'Щ', 'Ъ': 'х', 'Ы': 'Y', 'Ь': 'с', 'Э': 'ф', 'Ю': 'П', 'Я': 'У', '!': '=',
            '"': 'ч', "'": 'u', '№': 'я', ';': 'М', '%': 'у', ':': 'M', '?': 'C', '*': 'V', '(': 'Ё', ')': 'm',
            '_': ')', '+': '*', '-': 'э', '=': 'З'}

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    name = self.text if self.text != "" else "Player"  # - стандартное имя
                    return True, name
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        return False, "Player"

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def input_text():
    clock = pygame.time.Clock()
    x, y = 250, 350
    input_box1 = InputBox(x, y, 140, 32)
    done = False

    name = "Player"
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            else:
                done, name = input_box1.handle_event(event)

        input_box1.update()

        screen.fill((30, 30, 30))

        fontObj = pygame.font.Font('freesansbold.ttf', 40)
        textSurfaceObj = fontObj.render('Введите имя:', True, "yellow", "blue")
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (300, 300)  # координаты х и у Надписи - начало в левом верхнем углу

        screen.blit(textSurfaceObj, textRectObj)

        input_box1.draw(screen)

        pygame.display.flip()
        clock.tick(30)
    return name

def apple_random():
    """ Эта функция (подпрограмма) для перемещения спрайта яблоко в случайное положение"""
    apple.x = play.random_number(lowest=-19, highest=19) * 20
    apple.y = play.random_number(lowest=-14, highest=13) * 20

def borders_and_lines():
    for Y in range(-270, 270, 20):
        line = play.new_line(color='lightgreen', x=-390, y=Y, length=780, angle=0, thickness=1, x1=None, y1=None)
        all_sprites.append(line)
        lines.append(line)
    for X in range(-370, 390, 20):
        line = play.new_line(color='lightgreen', x=X, y=270, length=560, angle=-90, thickness=1, x1=None, y1=None)
        lines.append(line)
        all_sprites.append(line)
    # создаем линии для рамки
    line = play.new_line(color='red', x=LEFT_BRD, y=UP_BRD, length=560, angle=-90, thickness=1, x1=None, y1=None)
    borders.append(line)
    all_sprites.append(line)
    line = play.new_line(color='red', x=RIGHT_BRD, y=UP_BRD, length=560, angle=-90, thickness=1, x1=None, y1=None)
    borders.append(line)
    all_sprites.append(line)
    line = play.new_line(color='red', x=LEFT_BRD, y=UP_BRD, length=780, angle=0, thickness=1, x1=None, y1=None)
    borders.append(line)
    all_sprites.append(line)
    line = play.new_line(color='red', x=LEFT_BRD, y=DOWN_BRD, length=780, angle=0, thickness=1, x1=None, y1=None)
    borders.append(line)
    all_sprites.append(line)

def update_bodies_position():
    bodies_positions.clear()
    for index in range(0, len(body_clone_list)):
        position = body_clone_list[index].x, body_clone_list[index].y, body_clone_list[index].angle
        bodies_positions.append(position)

def move_bodies_to_new_position():
    body_clone_list[0].go_to(head)
    body_clone_list[0].angle = head.angle
    body_clone_list[0].show()
    for index in range(1, len(body_clone_list)):
        new_x, new_y, new_angle = bodies_positions[index - 1]
        body_clone_list[index].go_to(new_x, new_y)
        body_clone_list[index].angle = new_angle
        body_clone_list[index].show()

def deshifr(string):
    str1 = []
    for symbol in string:
        if symbol in alf_dict_back:
            str1.append(alf_dict_back[symbol])  # заменяем зашифрованные символы
        else:
            str1.append(symbol)
    return "".join(str1)

def shifr(string):
    str1 = []
    for symbol in string:
        if symbol in alf_dict:
            str1.append(alf_dict[symbol])  # заменяем на зашифрованные символы
        else:
            str1.append(symbol)
    return "".join(str1)

def get_winners():
    """Функция возвращает словарь с Именами и значениями очков Победителей"""
    try:
        file_win = open("winners.win", "r", encoding="utf-8")
        dict_winners = {}  # создаем словарь для расшифровки победителей из файла
        try:
            text = file_win.read()
            text = deshifr(text)  # расшифровываем файл
            list_win = text.split(" ; ")  # создаем список из имени и значения рекорда каждого победителя
            for win in list_win:
                winer = win.split("_;_")
                dict_winners[winer[0]] = int(winer[1])  # записываем пары Имя победителя и его рекорд в словарь
        except:
            print("Файл winners.win содержит ошибки")
            file_win.close()
            exit()
        file_win.close()
        return dict_winners
    except:
        print("file open error")
        return {}

def save_winners(winners):
    file_win = open("winners.win", "w", encoding="utf-8")
    string = ""
    for name in winners:
        string += name + "_;_" + str(winners[name]) + " ; "# достаем из словаря нужные значения
    file_win.write(shifr(string))
    file_win.close()

def setWinner(winners):
    """Функция для добавления текущего значения в словарь победителей и удаление минимального,
        если количество Победителей больше 10"""
    # Условие для обновления или добавления Нашего текущего достижения
    if player_name.words in winners:
        if int(score.words) > winners[player_name.words]:
            winners[player_name.words] = int(score.words)
    else:
        winners[player_name.words] = int(score.words)

    min_score = int(score.words)
    name_min = player_name.words
    for name_win, score_win in winners.items():
        if score_win < min_score:
            min_score = score_win
            name_min = name_win
    if len(winners.keys()) > 10:
        del winners[name_min]
    return winners

def show_winners(winners):
    global list_winners
    list_winners = [play.new_text(words=f'{"№"}  {"ИМЯ ИГРОКА".center(30)} {"ОЧКИ"}', x=-100, y=170, angle=0,
                           font=None, font_size=30, color='gold', transparency=100)]
    sorted_winners = list(winners.items())
    sorted_winners.sort(key=lambda i: i[1])
    sorted_winners = sorted_winners[::-1]
    for i in range(1, 11):
        if i - 1 < len(sorted_winners):
            win = play.new_text(words=f'{i:2} {sorted_winners[i - 1][0].ljust(30,"_")} {sorted_winners[i - 1][1]:4}', x=-100,
                                y=140 - i * 30, angle=0, font=None, font_size=30, color='gold', transparency=100)
        else:
            win = play.new_text(words=f'{i:2} {"_"*30} {"_"*4}', x=-100, y=140 - i * 30, angle=0,
                                font=None, font_size=30, color='gold', transparency=100)
        list_winners.append(win)

def show_hall_winners():
    global handle, your_score
    for sprite in all_sprites:
        sprite.hide()
    handle = play.new_text(words='Лучшие результаты', x=-100, y=200, angle=0,
                           font=None, font_size=45, color='gold', transparency=100)
    winners = get_winners()  # Читаем файл с победителями
    winners = setWinner(winners)
    save_winners(winners)
    show_winners(winners)
    your_score = play.new_text(words="Ваш текущий результат: " + player_name.words + " - " + score.words,
                               x=-100, y=-250, angle=0, font=None, font_size=30, color='red', transparency=100)

def game_over():
    pygame.mixer.music.stop()
    finish.show()
    sound_game_over.play()
    return False

def check_stars():
    if apples % 10 == 0:
        new_x = -200 + 30 * len(stars)  # Каждый раз когда получаем звезду смещаем ее вправо
        star = play.new_image(image="star.png", x=new_x, y=285, size=2, angle=0)
        stars.append(star)
        all_sprites.append(star)

player_name.words = input_text()  # вызываем ввод имени  # пекредаем имя текстовому спрайту


@play.when_program_starts
def start():
    borders_and_lines()  # вызываем подпрограмму для отрисовки линий и рамки
    head.angle = 0
    score.words = str(apples)
    apple_random()
    play.set_backdrop(color_or_image_name='black')
    finish.hide()
    # gameover.hide()


@play.when_key_pressed('up', 'down', 'right', 'left', 'w', 's', 'a', 'd')
def pres_keys(key):
    if key == 'up' or key == 'w':
        head.angle = 90
    if key == 'down' or key == 's':
        head.angle = -90
    if key == 'right' or key == 'd':
        head.angle = 0
    if key == 'left' or key == 'a':
        head.angle = 180


@play.repeat_forever
async def do():
    global apples, head, speed, run  # разрешаем редактировать глобальную переменную внутри функции

    # Условие для перемещения хвоста
    if len(body_clone_list):
        update_bodies_position()
        move_bodies_to_new_position()

    if run:
        head.move(20)  # постоянное движение вперед спрайта - head

    # Условие Проигрыша - выход за рамки
    if head.x >= RIGHT_BRD or head.x <= LEFT_BRD or head.y >= UP_BRD or head.y <= DOWN_BRD:
        head.x, head.y = 0, 0
        run = game_over()
        await play.timer(seconds=2)
        show_hall_winners()
        await play.timer(seconds=5)
        exit()


    # Условие касания яблока
    if head.is_touching(apple):
        apples = apples + 1
        check_stars()  # Проверяем нужно добавлять и показывать звезды
        score.words = str(apples)  # для отображения кол-ва съеденных яблок на экране
        body_clone = play.new_image(image="тело.png", x=0, y=0, size=20, angle=90)  # Создаем клон нашего хвоста
        body_clone_list.append(body_clone)  # Добавляем клон в список
        all_sprites.append(body_clone)
        body_clone.hide()
        apple_random()
        sound_eat.play()
        # ускорение движения змейки
        speed -= 0.001

    # Условие Проигрыша - касания хвоста
    for body_clone in body_clone_list:
        if head.is_touching(body_clone):
            run = game_over()
            await play.timer(seconds=2)
            show_hall_winners()
            await play.timer(seconds=5)
            exit()


    # пауза между шагами - для создания эффекта сокрости
    await play.timer(seconds=speed)


# для повтора фоновой мелодии
@play.repeat_forever
async def music_play():
    pygame.mixer.music.play()
    await play.timer(seconds=194)


play.start_program()
