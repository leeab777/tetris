import pygame
import sys
import random

pygame.init()  #initialize pygame

screen_width = 300                #define constants
screen_height = 600
grid_size = 30    #each block will be 30 px
COLUMNS =screen_width // grid_size
ROWS = screen_height // grid_size

white = (255, 255, 255)    # colors
black = (0, 0, 0)
font_colors = (200, 200, 200)
        
SHAPES = [                               #define shapes
    [[(0, 0), (1, 0), (2, 0), (3, 0)], [(1, 0), (1, 1), (1, 2), (1,3)]],    #I
    [[(0, 0), (0, 1), (1, 0),  (1, 1)]],  #O
    [[(1, 0), (0, 1), (1, 1), (2,1)], [(1, 0), (1, 1), (1, 2), (2, 1)], [(0, 1), (1, 1), (2, 1), (1, 2)], [(1, 0), (1, 1), (1, 2), (0, 1)]],    #T
    [[(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (0,1), (1, 1), (1, 2)]],    # S
    [[(0, 0), (1, 0), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (0, 2)]],     # Z
    [[(0, 0), (1, 0), (2, 0), (2, 1)], [(1,0), (1, 1), (1, 2), (0, 2)], [(0, 0), (0, 1), (1, 1), (2, 1)], [(0, 0), (1, 0), (1, 1), (1, 2)]],    #J
    [[(0, 2), (0, 1), (0, 0), (1, 0)], [(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (1, 0), (1, 1), (1, 2)], [(0, 0), (0, 1), (1, 1), (2, 1)]]    #L
    ]

class tetshape:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.x = COLUMNS // 2 - 1          #start in center of screen
        self.y = 0            #start at top of screen
        self.color = random.choice([(0, 128, 255), (255, 255, 0), (255, 51, 153), (0, 204, 0), (255, 51, 51), (51, 51, 255), (255, 128, 0)])

    def get_coordinates(self):    #get coordinates of current shape
        return [(x + self.x, y + self.y) for (x, y) in self.shape[self.rotation]]

    def rotate(self, grid):                                                    #rotate 90 deg 
        original_rotation = self.rotation
        self.rotation = (self.rotation + 1 ) % len(self.shape)
        if check_collision(self, grid):       #shift left or right to fit rotation
            for shift in [-1, 1]:
                self.x += shift
                if not check_collision(self, grid):
                    return
                self.x -= shift
            self.rotation = original_rotation       #undo rotation if no valid position

    def draw(self, screen):         #draw shapes on screen
        for (x, y) in self.get_coordinates():
            rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, self.color, rect)

    def get_bounding_box(self):                 #binding box for shapes
        coordinates = self.get_coordinates()
        min_x = min([x for x, y in coordinates])
        max_x = max([x for x, y in coordinates])
        min_y = min([y for x, y in coordinates])
        max_y = max([y for x, y in coordinates])
        return min_x, max_x, min_y, max_y

pygame.init()     #initialize pygame

def draw_grid(screen, grid):     #draw the grid and locked blockes
    for y in range(ROWS):
        for x in range(COLUMNS):
            rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, grid[y][x], rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)       #draw grid lines

def check_collision(tetshape, grid):    #check for collisions
    for x, y in tetshape.get_coordinates():
        if x < 0 or x >= COLUMNS or y >= ROWS:
            return True
        if y >= 0 and grid[y][x] !=black:
            return True    
    return False

def lock_tetshape(tetshape, grid):
    for x, y in tetshape.get_coordinates():
        if y >= 0:    #ensure its not above the visable screen
            grid[y][x] = tetshape.color

def clear_rows(grid):      #clear full rows and shift above rows down
    cleared = 0
    y = ROWS - 1
    while y >= 0:
        if all(grid[y][x] != black for x in range(COLUMNS)):
            del grid[y]
            grid.insert(0, [black for _ in range(COLUMNS)])
            cleared += 1
        else:
            y -= 1   #only move to the next row if the current row is not cleared
    return cleared

def new_tetshape():           #create a new shape
    shape = random.choice(SHAPES)
    return tetshape(shape)

def draw_text(screen, text, position):
    font = pygame.font.Font(None, 36)
    label = font.render(text, True, font_colors)
    screen.blit(label, position)

def main():
    screen = pygame.display.set_mode((screen_width, screen_height))    #game screen
    pygame.display.set_caption("TETRISISH")
    clock = pygame.time.Clock()

    grid = [[black for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_tetshape = new_tetshape()
    fall_time = 0
    fall_speed = 100   # in miliseconds
    score = 0
    level = 1
    paused = False #pause game

    while True: 
        screen.fill(black)   #fill screen with black
        draw_grid(screen, grid)           #draw grid
        current_tetshape.draw(screen)     #draw falling shape
        draw_text(screen, f"Score: {score}", (10, 10))
        draw_text(screen, f"Level: {level}", (10, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:     #pause game
                    paused = not paused

                if not paused:   #allow other input
                    if event.key == pygame.K_LEFT:
                        current_tetshape.x -= 1
                        if check_collision(current_tetshape, grid):
                            current_tetshape.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_tetshape.x += 1
                        if check_collision(current_tetshape, grid):
                            current_tetshape.x -= 1
                    elif event.key == pygame.K_DOWN:
                        current_tetshape.y += 1
                        if check_collision(current_tetshape, grid):
                            current_tetshape.y -= 1
                    elif event.key == pygame.K_UP:
                        current_tetshape.rotate(grid)
                
        if paused:   #paused screen
            draw_text(screen, "PAUSED", (screen_width // 3, screen_height // 2))
            pygame.display.update()
            clock.tick(10)  #slow down loop to save cpu
            continue    #skip the rest of the game loop when paused

        fall_time += clock.get_rawtime()     #handle time based movement
        clock.tick(30)          #run at 30 frames per second

        if fall_time > fall_speed:
            current_tetshape.y += 1
            if check_collision(current_tetshape, grid):
                current_tetshape.y -= 1
                lock_tetshape(current_tetshape, grid)
                cleared = clear_rows(grid)
                score += cleared * 100 
                level = 1 + score // 1000
                fall_speed = max(10, 100 - (level - 1) * 30)
                current_tetshape = new_tetshape()
                if check_collision(current_tetshape, grid):     # gameover condition
                    draw_text(screen, "GAME OVER", (screen_width // 3, screen_height // 2))
                    draw_text(screen, "Press R to Restart",(screen_width // 3 - 20, screen_height // 2 + 40))
                    pygame.display.update()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                main()    #restart game
                        pygame.time.delay(100)        
            fall_time = 0

                    
        pygame.display.update()                    


main()       
