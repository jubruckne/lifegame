import pygame

board_width = 100
board_height = 60

pygame.init()

screen = pygame.display.set_mode([board_width * 9, board_height * 9])
running = True
paused = True
pygame.display.set_caption("Paused - press space to continue")

class Tile(pygame.sprite.Sprite):
    x: int = 0
    y: int = 0
    alive: int = 0

    def __init__(self, x, y):
        super(Tile, self).__init__()
        self.surf = pygame.Surface((8, 8))

        if(x != 0 and y!= 0 and x < (board_width - 1) * 9 and y < (board_height - 1) * 9):
            self.surf.fill((222,222,222))
        else:
            self.surf.fill((255, 255, 255))

        self.rect = self.surf.get_rect()
        self.x = x
        self.y = y

    def set_alive(self, a):
        self.alive = a
        if(a == 0):
            self.surf.fill((222, 222, 222))
        else:
            self.surf.fill((222, 50, 50))

board = {}

for x in range(board_width):
    for y in range(board_height):
        t = Tile(x * 9, y * 9)
        board[x, y] = t

cycle = 0
clock = pygame.time.Clock()

while (running):
    event_list = pygame.event.get()

    for event in event_list:
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_ESCAPE):
                running = False
            if(event.key == pygame.K_SPACE):
                paused = not paused
                if(paused):
                    pygame.display.set_caption("Paused - press space to continue")

        if event.type == pygame.MOUSEMOTION:
            if (pygame.mouse.get_pressed()[0]):
                for t in board.values():
                    r = pygame.Rect(t.x, t.y, 9, 9)

                    if r.collidepoint(event.pos):
                        t.set_alive(1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for t in board.values():
                r = pygame.Rect(t.x, t.y, 9, 9)

                if r.collidepoint(event.pos):
                    t.set_alive(1)

        elif (event.type == pygame.QUIT):
            running = False

# Any live cell with two or three live neighbours survives.
# Any dead cell with three live neighbours becomes a live cell.
# All other live cells die in the next generation. Similarly, all other dead cells stay dead.

    if(not paused):
        cycle = cycle + 1

        kill_list = []
        revive_list = []

        for x in range(board_width):
            for y in range(board_height):
                t = board[x, y]

                alive_neighbors = 0

                if(x != 0 and y!= 0 and x < board_width - 1 and y < board_height - 1):
                    alive_neighbors = alive_neighbors + board[x + 1, y].alive   # right
                    alive_neighbors = alive_neighbors + board[x - 1, y].alive   # left
                    alive_neighbors = alive_neighbors + board[x, y + 1].alive   # top
                    alive_neighbors = alive_neighbors + board[x, y - 1].alive   # bottom
                    alive_neighbors = alive_neighbors + board[x + 1, y + 1].alive   # top right
                    alive_neighbors = alive_neighbors + board[x + 1, y - 1].alive       # bottom right
                    alive_neighbors = alive_neighbors + board[x - 1, y + 1].alive
                    alive_neighbors = alive_neighbors + board[x - 1, y - 1].alive

                if(t.alive == 1):
                    # Any live cell with two or three live neighbours survives.
                    if alive_neighbors < 2 or alive_neighbors == 4:
                        kill_list.append(t)
                else:
                    # cell is dead, if it has three neighbors, it will be alive now
                    if(alive_neighbors == 3):
                        revive_list.append(t);

        for t in kill_list:
            t.set_alive(0)

        for t in revive_list:
            t.set_alive(1)

    screen.fill((255, 255, 255))

    for p in board.values():
        screen.blit(p.surf, (p.x, p.y))

    pygame.display.flip()

    fps = clock.tick(60)
    if(not paused):
        pygame.display.set_caption("Cycle {0:n} - FPS: {1:3.1f}".format(cycle, clock.get_fps()))


pygame.quit()
