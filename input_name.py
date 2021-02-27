from config import *


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

