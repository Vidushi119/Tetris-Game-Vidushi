from settings import *
from sys import exit
from os.path import join
import os
# components
from game import Game
from score import Score
from preview import Preview
from random import choice

class Main:
    def __init__(self,game_over):

        # general 
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Vidushi\'s Tetris')

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # components
        self.game = Game(self, self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

        # audio 
        self.music = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'sound', 'music.wav'))
        self.music.set_volume(0.05)
        self.music.play(-1)

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def reset_game(self):
        self.__init__(game_over=False)  # Reinitialize the main instance to reset the game

    def run(self,game_over):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.game.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            exit()

            # display 
            self.display_surface.fill(GRAY)
            
            # components
            self.game.run()
            self.score.run()
            self.preview.run(self.game.game_over,self.next_shapes)

            # game over handling
            if self.game.game_over:
                font = pygame.font.Font(None, 50)
                text_surface = font.render("Game Over! \nPress R to Restart or Q to Quit", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display_surface.blit(text_surface, text_rect)

            # updating the game
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game_over=False
    main = Main(game_over)
    
    main.run(game_over)


