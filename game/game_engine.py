import pygame
from .paddle import Paddle
from .ball import Ball
import time  

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.target_score = 5  # default winning score

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball first
        self.ball.move()

        # ✅ Immediately check for paddle collisions
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width  # reposition to avoid overlap
            self.ball.velocity_x *= -1

        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width  # reposition to avoid overlap
            self.ball.velocity_x *= -1

        # Then handle wall bounce and scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Finally, move AI
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        winner_text = None
        if self.player_score >= self.target_score:
            winner_text = "Player Wins!"
        elif self.ai_score >= self.target_score:
            winner_text = "AI Wins!"

        if winner_text:
            # Fill screen black and show winner message
            screen.fill((0, 0, 0))
            text_surface = self.font.render(winner_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()

            # Pause so players can see the result
            time.sleep(2)

            # ✅ Show replay options instead of quitting immediately
            self.show_replay_menu(screen)

    def show_replay_menu(self, screen):
        """Display replay options: Best of 3 / 5 / 7 / Exit."""
        menu_running = True

        while menu_running:
            screen.fill((0, 0, 0))
            title = self.font.render("Play Again? Choose Best of:", True, WHITE)
            opt3 = self.font.render("3 - Best of 3", True, WHITE)
            opt5 = self.font.render("5 - Best of 5", True, WHITE)
            opt7 = self.font.render("7 - Best of 7", True, WHITE)
            exit_opt = self.font.render("ESC - Exit", True, WHITE)

            # Draw menu items
            screen.blit(title, (self.width // 2 - 180, self.height // 2 - 100))
            screen.blit(opt3, (self.width // 2 - 100, self.height // 2 - 40))
            screen.blit(opt5, (self.width // 2 - 100, self.height // 2))
            screen.blit(opt7, (self.width // 2 - 100, self.height // 2 + 40))
            screen.blit(exit_opt, (self.width // 2 - 100, self.height // 2 + 100))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.target_score = 2  # Best of 3 → first to 2
                        menu_running = False
                    elif event.key == pygame.K_5:
                        self.target_score = 3  # Best of 5 → first to 3
                        menu_running = False
                    elif event.key == pygame.K_7:
                        self.target_score = 4  # Best of 7 → first to 4
                        menu_running = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            pygame.time.delay(100)

        # ✅ Reset game state for replay
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
