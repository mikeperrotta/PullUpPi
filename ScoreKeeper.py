import pygame
import pygame_gui
import time


class ScoreKeeper:
    def __init__(self, goal=40, resolution=(800, 480), caption='Score Keeper'):
        self.goal = goal
        self.resolution = resolution
        pygame.init()
        pygame.display.set_caption(caption)
        self.window_surface = pygame.display.set_mode(resolution)
        self.load_resources()
        self.draw_statics()

    def load_resources(self):
        self.midline = pygame.image.load('./assets/midline.bmp')
        self.score_line = pygame.image.load('./assets/score_line.bmp')
        self.title_font = pygame.font.Font('./assets/HelveticaNeue Light.ttf', 32)
        self.number_font = pygame.font.Font('./assets/HelveticaNeue Light.ttf', 60)

    def draw_statics(self):
        background = pygame.Surface(self.resolution)
        background.fill(pygame.Color('#ffffff'))
        self.window_surface.blit(background, (0, 0))
        self.window_surface.blit(self.score_line, (self.resolution[0] // 4 - self.score_line.get_size()[0] // 2, 234))
        self.window_surface.blit(self.midline, (self.resolution[0] // 2, (self.resolution[1] - self.midline.get_size()[1]) // 2))
        daily_goal_text = "Today's goal"
        daily_goal_text_surface = self.title_font.render(daily_goal_text, True, (112, 112, 112))
        self.window_surface.blit(daily_goal_text_surface, (self.resolution[0] // 4 - daily_goal_text_surface.get_size()[0] // 2, 150))
        lifetime_score_text = "Lifetime score"
        lifetime_score_text_surface = self.title_font.render(lifetime_score_text, True, (112, 112, 112))
        self.window_surface.blit(lifetime_score_text_surface, (self.resolution[0] * 3 // 4 - lifetime_score_text_surface.get_size()[0] // 2, 150))
        daily_goal_surface = self.number_font.render(str(self.goal), True, (112, 112, 112))
        self.window_surface.blit(daily_goal_surface, (self.resolution[0] // 4 - daily_goal_surface.get_size()[0] // 2 + 50, 240 + 30))

    def update_scores(self, daily_completed, lifetime_score):
        self.draw_statics()
        daily_completed_surface = self.number_font.render(str(daily_completed), True, (112, 112, 112))
        self.window_surface.blit(daily_completed_surface, (self.resolution[0] // 4 - daily_completed_surface.get_size()[0] // 2 - 50, 240 - 30))
        lifetime_score_surface = self.number_font.render(str(lifetime_score), True, (112, 112, 112))
        self.window_surface.blit(lifetime_score_surface, (self.resolution[0] * 3 // 4 - lifetime_score_surface.get_size()[0] // 2, 240))
        pygame.display.update()


if __name__ == "__main__":
    goal = 40
    daily = 0
    total = 0

    sk = ScoreKeeper(goal)
    for i in range(10):
        sk.update_scores(daily, total)
        time.sleep(1)
        daily += 1
        total += 1
