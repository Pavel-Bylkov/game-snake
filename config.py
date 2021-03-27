import pygame

# play.screen.width = 800
# play.screen.height = 600

UP_BRD = 225  # Крайня верхняя координата Y
LEFT_BRD = -325  # Координата X левая
RIGHT_BRD = 1425  # Координата X правая
DOWN_BRD = -725  # Крайня нижняя координата Y
SIZE = 50  # Размер ячейки сетки

WIN_WIDTH = 1920
WIN_HEIGHT = 1080

def full_screen():
    global screen, state_screen
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.init()
    state_screen = 'FULL'

def normal_screen():
    global screen, state_screen
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.init()
    state_screen = 'NORMAL'

def switch_screen():
    if state_screen == 'NORMAL':
        full_screen()
    else:
        normal_screen()

full_screen()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

sound_eat = pygame.mixer.Sound('Bite.wav')
sound_eat.set_volume(0.2)
sound_game_over = pygame.mixer.Sound('Bite.wav')
pygame.mixer.music.load('bethoven.ogg')
pygame.mixer.music.set_volume(0.2)

run = True  # для движения головы
pause = False
STARTSPEED = 0.4
speed = STARTSPEED
is_elecsir = False
show_eleksir = False
apples = 0
help_text = 'W - turn up   A - turn left   S - turn down   D - turn right   H - help   P - pause   L - exit'
help_text2 = 'SPACE - show holl winners  L - exit'
handle = None
body_clone_list = []  # создаем список пустой, в который потом будем добавлять клоны хвоста
bodies_positions = []  # здесь будем хранить координаты каждого клона хвоста
box_list = []  # список с препятствиями
lines = []  # список линий - сетка
borders = []  # список линий - границы, за которые выходить нельзя
stars = []  # Список для отображения звезд
apples_lst = []