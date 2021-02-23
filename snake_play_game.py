#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import play

from config import *
from shifrovka import shifr, deshifr

# https://github.com/replit/play  - описание библиотеки Play

# pip3 install replit-play - сразу устанавливает и библиотеку play и pygame

# Todo 1 Условие Победы
# Todo 2 Добавить препятствия - если врезаешься, уменьшать змейку или геймовер
# ToDo 3 Разбить игру на файлы для удобства чтения
# TODO 4 Исправить чтение и сохранние рекордов в файл, в зашифрованном
# # виде - защита от Читинга

head = play.new_image(image="голова.png", x=0, y=0, size=10, angle=90)

apple = play.new_image(image="Apple.png", x=0, y=0, size=3, angle=0)
elecsir_speed = play.new_image(image="green.png", x=0, y=0, size=3, angle=0)
elecsir_slow = play.new_image(image="red.png", x=0, y=0, size=2, angle=0)
score = play.new_text(
    words='',
    x=350,
    y=280,
    angle=0,
    font=None,
    font_size=45,
    color='white',
    transparency=100)
player_name = play.new_text(
    words='',
    x=-350,
    y=280,
    angle=0,
    font=None,
    font_size=45,
    color='white',
    transparency=100)

finish = play.new_image(image="gameover.jpeg", x=0, y=0, size=120, angle=0)
# gameover = play.new_text(words='GAME OVER', x=0, y=0, angle=0, font=None,
# font_size=180, color='green', transparency=100)

all_sprites = [
    head,
    apple,
    score,
    player_name,
    finish,
    elecsir_speed,
    elecsir_slow]


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
        # координаты х и у Надписи - начало в левом верхнем углу
        textRectObj.center = (300, 300)

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
        line = play.new_line(
            color='lightgreen',
            x=-390,
            y=Y,
            length=780,
            angle=0,
            thickness=1,
            x1=None,
            y1=None)
        all_sprites.append(line)
        lines.append(line)
    for X in range(-370, 390, 20):
        line = play.new_line(
            color='lightgreen',
            x=X,
            y=270,
            length=560,
            angle=-90,
            thickness=1,
            x1=None,
            y1=None)
        all_sprites.append(line)
        lines.append(line)
    # создаем линии для рамки
    line = play.new_line(
        color='red',
        x=LEFT_BRD,
        y=UP_BRD,
        length=560,
        angle=-90,
        thickness=1,
        x1=None,
        y1=None)
    borders.append(line)
    all_sprites.append(line)
    line = play.new_line(
        color='red',
        x=RIGHT_BRD,
        y=UP_BRD,
        length=560,
        angle=-90,
        thickness=1,
        x1=None,
        y1=None)
    borders.append(line)
    all_sprites.append(line)
    line = play.new_line(
        color='red',
        x=LEFT_BRD,
        y=UP_BRD,
        length=780,
        angle=0,
        thickness=1,
        x1=None,
        y1=None)
    borders.append(line)
    all_sprites.append(line)
    line = play.new_line(
        color='red',
        x=LEFT_BRD,
        y=DOWN_BRD,
        length=780,
        angle=0,
        thickness=1,
        x1=None,
        y1=None)
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


def get_winners():
    """Функция возвращает словарь с Именами и значениями очков Победителей"""
    try:
        file_win = open("winners.win", "r", encoding="utf-8")
        dict_winners = {}  # создаем словарь для расшифровки победителей из файла
        try:
            text = file_win.read()
            text = deshifr(text)[:-3]  # расшифровываем файл
            # создаем список из имени и значения рекорда каждого победителя
            list_win = text.split(" ; ")
            for win in list_win:
                winer = win.split("_;_")
                # записываем пары Имя победителя и его рекорд в словарь
                dict_winners[winer[0]] = int(winer[1])
        except BaseException:
            print("Файл winners.win содержит ошибки")
            file_win.close()
            sys.exit(0)
        file_win.close()
        return dict_winners
    except BaseException:
        print("file open error")
        return {}


def save_winners(winners):
    file_win = open("winners.win", "w", encoding="utf-8")
    string = ""
    for name in winners:
        # достаем из словаря нужные значения
        string += name + "_;_" + str(winners[name]) + " ; "
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
    list_winners = [
        play.new_text(
            words=f'{"№"}  {"ИМЯ ИГРОКА".center(30)} {"ОЧКИ"}',
            x=-100,
            y=170,
            angle=0,
            font=None,
            font_size=30,
            color='gold',
            transparency=100)]
    sorted_winners = list(winners.items())
    sorted_winners.sort(key=lambda i: i[1])
    sorted_winners = sorted_winners[::-1]
    for i in range(1, 11):
        if i - 1 < len(sorted_winners):
            win = play.new_text(
                words=f'{i:02} {sorted_winners[i - 1][0].ljust(30,".")}'
                f' {sorted_winners[i - 1][1]:04}',
                x=-100,
                y=140 - i * 30,
                angle=0,
                font=None,
                font_size=30,
                color='gold',
                transparency=100)
        else:
            win = play.new_text(
                words=f'{i:02} {" "*30} {" "*4}',
                x=-100,
                y=140 - i * 30,
                angle=0,
                font=None,
                font_size=30,
                color='gold',
                transparency=100)
        list_winners.append(win)


def show_hall_winners():
    global handle, your_score
    for sprite in all_sprites:
        sprite.hide()
    handle = play.new_text(
        words='Лучшие результаты',
        x=-100,
        y=200,
        angle=0,
        font=None,
        font_size=45,
        color='gold',
        transparency=100)
    winners = get_winners()  # Читаем файл с победителями
    winners = setWinner(winners)
    save_winners(winners)
    show_winners(winners)
    your_score = play.new_text(
        words="Ваш текущий результат: " +
        player_name.words +
        " - " +
        score.words,
        x=-
        100,
        y=-
        250,
        angle=0,
        font=None,
        font_size=30,
        color='red',
        transparency=100)


def game_over():
    pygame.mixer.music.stop()
    finish.show()
    sound_game_over.play()
    return False


def check_stars():
    if apples % 10 == 0:
        # Каждый раз когда получаем звезду смещаем ее вправо
        new_x = -200 + 30 * len(stars)
        star = play.new_image(
            image="star.png",
            x=new_x,
            y=285,
            size=2,
            angle=0)
        stars.append(star)
        all_sprites.append(star)


# вызываем ввод имени  # пекредаем имя текстовому спрайту
player_name.words = input_text()


@play.when_program_starts
def start():
    finish.hide()
    elecsir_speed.hide()
    elecsir_slow.hide()
    borders_and_lines()  # вызываем подпрограмму для отрисовки линий и рамки
    head.angle = 0
    score.words = str(apples)
    apple_random()
    play.set_backdrop(color_or_image_name='black')

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
    # разрешаем редактировать глобальную переменную внутри функции
    global apples, head, speed, run, curent_speed, is_elecsir
    global show_eleksir

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
        sys.exit(0)

    # Условие касания яблока
    if head.is_touching(apple):
        apples = apples + 1
        check_stars()  # Проверяем нужно добавлять и показывать звезды
        # для отображения кол-ва съеденных яблок на экране
        score.words = str(apples)
        body_clone = play.new_image(
            image="тело.png",
            x=0,
            y=0,
            size=20,
            angle=90)  # Создаем клон нашего хвоста
        body_clone_list.append(body_clone)  # Добавляем клон в список
        all_sprites.append(body_clone)
        body_clone.hide()
        apple_random()
        sound_eat.play()
        # ускорение движения змейки
        speed -= 0.001

    # Условие касания элексира
    if show_eleksir and head.is_touching(elecsir_slow):
        show_eleksir = False
        is_elecsir = True
        elecsir_slow.hide()
        sound_eat.play()
        # Замедление движения змейки
        curent_speed = speed
        speed += 0.1

    if show_eleksir and head.is_touching(elecsir_speed):
        show_eleksir = False
        elecsir_speed.hide()
        is_elecsir = True
        sound_eat.play()
        # ускорение движения змейки
        curent_speed = speed
        speed -= 0.1

    # Условие Проигрыша - касания хвоста
    for body_clone in body_clone_list:
        if head.is_touching(body_clone):
            run = game_over()
            await play.timer(seconds=2)
            show_hall_winners()
            await play.timer(seconds=5)
            sys.exit(0)

    # пауза между шагами - для создания эффекта сокрости
    await play.timer(seconds=speed)


# для повтора фоновой мелодии
@play.repeat_forever
async def music_play():
    pygame.mixer.music.play()
    await play.timer(seconds=194)


@play.repeat_forever
async def return_speed():
    global speed, curent_speed, is_elecsir
    if is_elecsir:
        is_elecsir = False
        await play.timer(seconds=10)
        speed = curent_speed


@play.repeat_forever
async def surprize():
    global show_eleksir

    await play.timer(seconds=1)
    if play.random_number(lowest=0, highest=1) > 0:
        temp = elecsir_speed
    else:
        temp = elecsir_slow
    temp.x = play.random_number(lowest=-19, highest=19) * 20
    temp.y = play.random_number(lowest=-14, highest=13) * 20
    temp.show()
    show_eleksir = True
    await play.timer(seconds=10)
    temp.hide()
    temp.go_to(400, 400)
    show_eleksir = False
    await play.timer(seconds=5)

play.start_program()
