import pygame

# play.screen.width = 800
# play.screen.height = 600

UP_BRD = 270  # Крайня верхняя координата Y
LEFT_BRD = -390  # Координата X
RIGHT_BRD = 390  # Координата X
DOWN_BRD = -290  # Крайня нижняя координата Y

screen = pygame.display.set_mode((800, 600))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

sound_eat = pygame.mixer.Sound('Bite.wav')
sound_eat.set_volume(0.5)
sound_game_over = pygame.mixer.Sound('Bite.wav')
pygame.mixer.music.load('bethoven.ogg')
pygame.mixer.music.set_volume(0.5)

run = True  # для движения головы
STARTSPEED = 0.4
speed = STARTSPEED
is_elecsir = False
show_eleksir = False
apples = 0

body_clone_list = []  # создаем список пустой, в который потом будем добавлять клоны хвоста
bodies_positions = []  # здесь будем хранить координаты каждого клона хвоста
lines = []  # список линий - сетка
borders = []  # список линий - границы, за которые выходить нельзя
stars = []  # Список для отображения звезд