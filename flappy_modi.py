
            


#                                           KAAM SHURU YHA SE 

import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

#                                        YHA JYADA CHED-CHAD NHI

# --- WINDOW SETTINGS ---
# Optimized for 9:16 Phone Aspect Ratio
#Level of game can also  be edited( sochna bhi mtt )
WIDTH = 450
HEIGHT = 800
GRAVITY = 0.30 #0.60<hard
BIRD_JUMP = -7 #-3>hard
PIPE_SPEED = 4 #6<hard
FPS = 60 #keep at 60, can be changed but results in change of game speed weirdly.



#                            Setup Screen (Windowed Mode, isi mein jyada mza aata hai)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLAPPY Bird: MODI Edition")
clock = pygame.time.Clock()

#                                        ASSETS LOAD HONGE YHA

try:
    # Background
    back_img = pygame.image.load("background.png").convert()
    back_img = pygame.transform.smoothscale(back_img, (WIDTH, HEIGHT))
    
    # Bird - Large and High Quality (meri shakal jaisi nhi)

    bird_original = pygame.image.load("modi1.png").convert_alpha()
    bird_base = pygame.transform.smoothscale(bird_original, (150, 145))
    
    # Pipe
    pipe_original = pygame.image.load("p.png").convert_alpha()
    pipe_img = pygame.transform.smoothscale(pipe_original, (100, 600))
    pipe_mask = pygame.mask.from_surface(pipe_img)
    
    # Audio
    pygame.mixer.music.load("Modi_s.mp3")
    game_over_sound = pygame.mixer.Sound("Maza Nahi Aa Raha Hai Meme Download Mp3.mp3")
    
except Exception as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    sys.exit()


#                                TAGDI BAAT-CHEET (VENOM BHAI KA ASAR) 


class Bird:
    def __init__(self):
        self.rect = bird_base.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.image = bird_base
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0
        self.rotation = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        

    #         [  TILT EFFECT FOR BETTER VISUALS (ISKE BINA SBB MERI SHAKAL JAISA LGG RHA THA)  ]



        self.rotation = -self.velocity * 2 
        self.image = pygame.transform.rotate(bird_base, self.rotation)
        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        self.velocity = BIRD_JUMP

    def draw(self):

        # KEEPS MODI JI CENTERED EVEN WHEN ROTATING (in short modi ji ko girne se bachane ke liye)

        new_rect = self.image.get_rect(center=self.rect.center)
        screen.blit(self.image, new_rect)

class Pipe:
    def __init__(self):
        self.gap = 210
        self.x = WIDTH + 100
        self.top_height = random.randint(150, 450)
        self.passed = False
        
        self.bottom_rect = pipe_img.get_rect(topleft=(self.x, self.top_height + self.gap))
        self.bottom_mask = pipe_mask
        
        self.top_pipe_img = pygame.transform.flip(pipe_img, False, True)
        self.top_rect = self.top_pipe_img.get_rect(bottomleft=(self.x, self.top_height))
        self.top_mask = pygame.mask.from_surface(self.top_pipe_img)

    def update(self):
        self.bottom_rect.x -= PIPE_SPEED
        self.top_rect.x -= PIPE_SPEED

    def draw(self):
        screen.blit(pipe_img, self.bottom_rect)
        screen.blit(self.top_pipe_img, self.top_rect)

def check_collision(bird, pipes):
        for pipe in pipes:
            bird_final_rect = bird.image.get_rect(center=bird.rect.center)
            b_offset = (pipe.bottom_rect.x - bird_final_rect.x, pipe.bottom_rect.y - bird_final_rect.y)
            t_offset = (pipe.top_rect.x - bird_final_rect.x, pipe.top_rect.y - bird_final_rect.y)
            
            if bird.mask.overlap(pipe.bottom_mask, b_offset) or bird.mask.overlap(pipe.top_mask, t_offset):
                return True
                
        if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT - 10:
            return True
        return False

def draw_score(score, is_game_over=False):
    font_size = 70 if is_game_over else 90
    font = pygame.font.SysFont("Impact", font_size)
    color = (255, 255, 255) if not is_game_over else (255, 50, 50)
    
    score_surf = font.render(str(score), True, color)
    y_pos = 80 if not is_game_over else HEIGHT // 2 - 50
    score_rect = score_surf.get_rect(center=(WIDTH // 2, y_pos))
    screen.blit(score_surf, score_rect)

def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_active = True
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.jump()
                    else:
                        main() # Reset

        # Draw Background (iske bina game nhi)
        screen.blit(back_img, (0, 0))

        if game_active:
            bird.update()
            bird.draw()

#                                [        PIPE LOGIC (MAIN MASALA)    ]


            if pipes[-1].bottom_rect.x < WIDTH - 250:
                pipes.append(Pipe())

            for pipe in pipes:
                pipe.update()
                pipe.draw()

#                                [   SCORE LOGIC( TUMSE NA HO PAYGA ) ]

                if not pipe.passed and bird.rect.left > pipe.bottom_rect.right:
                    score += 1
                    pipe.passed = True

            if check_collision(bird, pipes):
               pygame.mixer.music.stop()
               game_over_sound.play()
               game_active = False

            pipes = [p for p in pipes if p.bottom_rect.right > 0]
            draw_score(score)
        else:


#                                       KHEL KHATM BETA: UserInterface


            draw_score(score, True)
            font = pygame.font.SysFont("Impact", 30)
            msg = font.render("TU ANTINATIONAL HAI KYA?", True, (255, 255, 255))
            screen.blit(msg, (WIDTH//2 - 115 , HEIGHT//2 + 50))
            font=pygame.font.SysFont("Impact",10)
            font=font.render("Press Space To Restart",True,(200,100,200))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main() 



