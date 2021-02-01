import pygame

mario_coin = './audio/smb_coin.wav'
mario_level_complete = './audio/smb_stage_clear.wav'

class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()
        
    def play(self, file):
        print('playing {}'.format(file))
        sound = pygame.mixer.Sound(file)
        pygame.mixer.Sound.play(sound)
        return pygame.mixer.Sound.get_length(sound)

if __name__ == "__main__":
    import time
    time.sleep(1)
    sp = SoundPlayer()
    duration = sp.play(mario_coin)
    time.sleep(.5)
    sp.play(mario_level_complete)
