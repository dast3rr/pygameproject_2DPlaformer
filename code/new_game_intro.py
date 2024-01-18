import pygame
from graphics import screen
from data import FONT

def new_game_intro():
    phrases = ['Чума...', 'Чума поработила нашу деревню.', 'Столько людей погибло в подземелье, пытаясь нас спасти...',
               'Отважный воин, помоги нам!', 'Отыщи источник.']
    c = 0
    cur_phrase = 0
    num_of_showed_letters = 1
    font = pygame.font.Font(FONT, 40)
    while True:
        screen.fill(pygame.Color('black'))
        showed_text = phrases[cur_phrase][:num_of_showed_letters]
        c += 1
        if c % 40 == 0:
            if num_of_showed_letters - 1 <= len(phrases[cur_phrase]):
                num_of_showed_letters += 1
        text = font.render(showed_text, 1, pygame.Color('white'))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                            screen.get_height() // 2 - text.get_height() // 2))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if num_of_showed_letters < len(phrases[cur_phrase]):
                    num_of_showed_letters = len(phrases[cur_phrase])
                elif cur_phrase + 1 < len(phrases):
                    cur_phrase += 1
                    num_of_showed_letters = 1
                    c = 0
                else:
                    return
        pygame.display.flip()
