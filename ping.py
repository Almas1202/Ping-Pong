import pygame, random

from pygame.draw import circle
from in_game_utils import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ping_Pong")

speedx = random.randint(-7, 7)

if speedx == 0:
    speedx = -5
    speedy = 2
else:
    speedy = 7 - abs(speedx)

#MUSIC
sound1 = pygame.mixer.Sound('sounds/Hit_Hurt2.wav')
sound2 = pygame.mixer.Sound('sounds/Hit_Hurt.wav')
sound1.set_volume(0.5)
sound2.set_volume(0.2)
#Objects
player_rect = pygame.Rect(x, y, pw, ph)
player2_rect = pygame.Rect(x2, y, pw, ph)
bot_rect = pygame.Rect(x2, y, pw, ph+10)
space1 = pygame.Rect(665, 0, 35, 10)
space2 = pygame.Rect(665, 390, 35, 10)

space3 = pygame.Rect(x + 15, y, 2, ph)
space4 = pygame.Rect(x, y, pw, 1)
space5 = pygame.Rect(x, y + ph - 1, pw, 1)

space6 = pygame.Rect(x2, y, 5, ph + 10)
space7 = pygame.Rect(x2, y, pw, 3)
space8 = pygame.Rect(x2, y + ph + 10, pw, 3)

space9 = pygame.Rect(x2, y, 5, ph)
space10 = pygame.Rect(x2, y, pw, 3)
space11 = pygame.Rect(x2, y + ph, pw, 3)

#Кнопки в меню
u_vs_bot = pygame.Rect(450, 100, 200, 75)
u_vs_pl = pygame.Rect(450, 200, 200, 75)
inf_lvl = pygame.Rect(450, 300, 200, 75)

pl_bot = pygame.image.load("imgs/pl_bot.png")
pl_pl = pygame.image.load("imgs/pl_pl.png")
sets = pygame.image.load("imgs/sets.png")

#Тексты
font = pygame.font.Font('utils/GraduateRegular.ttf', 120)
win_text = font.render('Yo won', 1, white)
lose_text = font.render('Yo lose', 1, white)

title1 = font.render('Ping', 1, yellow)
title2 = font.render('and', 1, white)
title3 = font.render('Pong', 1, yellow)

font1 = pygame.font.Font('GraduateRegular.ttf', 30)
but1 = font1.render('1 player', 1, black)
but2 = font1.render('2 players', 1, black)
but3 = font1.render('Infinitive', 1, black)

#Функции
def bot_moving():
    global moving
    if bot_rect.colliderect(space2):
        moving = 'up'
    if bot_rect.colliderect(space1):
        moving = 'down'

    if moving == 'down':
        bot_rect.bottom += 3
        space6.bottom += 3
        space7.bottom += 3
        space8.bottom += 3
    if moving == 'up':
        bot_rect.top -= 3
        space6.top -= 3
        space7.top -= 3
        space8.top -= 3
def menu():
    score_player = font.render(str(score1), 1, grey)
    score_bot = font.render(str(score2), 1, grey)
    player_text_rect = score_player.get_rect(center=(180, H/2))
    bot_text_rect = score_bot.get_rect(center=(500, H/2))
    screen.blit(score_player, player_text_rect)
    screen.blit(score_bot, bot_text_rect)

    pygame.draw.line(screen, grey, (W/2 - 5, 0), (W/2 - 5, H), 10)
    pygame.draw.rect(screen, white, player_rect)

    if gamemode == 3:
        pygame.draw.rect(screen, white, player2_rect)
    else:
        pygame.draw.rect(screen, white, bot_rect)
def ball():
    global posx, posy, speedx, speedy, score1, score2, pl2_hit, circl
    global can_hit, bot_hit, win, lose, player_moving, gamemode

    posx += speedx
    posy -= speedy

    circl = pygame.draw.circle(screen, yellow, (posx, posy), 20)

    if circl.left <= 0 or circl.right >= W:
        speedx = -speedx
        sound2.play()
        if circl.left <= 0:
            score2 += 1
            bot_hit = True
            pl2_hit = True
            circl.left = 0
        
        if circl.right >= W:
            score1 += 1
            can_hit = True
            circl.right = W


    if circl.topleft[1] <= 0 or circl.bottomright[1] >= H:
        speedy = -speedy
        sound2.play()

    if score1 >= 10 and score2 < 10:
        win = True
    elif score2 >= 10 and score1 <10:
        lose = True

    #Мяч с игроком
    if circl.colliderect(space3):
        speedx = -speedx
        circl.left = x + pw
        sound1.play()
        if player_moving == 'up':
            if speedx >= 3:
                speedy += 1
                speedx += 1
        if player_moving == 'down':
            if speedx >= 3:
                speedy -= 1
                speedx += 1
        can_hit = False
        bot_hit = True
        pl2_hit = True

    if circl.colliderect(space4):
        if can_hit:
            sound1.play()
            speedy = -speedy
            can_hit = False
            bot_hit = True
            pl2_hit = True

    if circl.colliderect(space5):
        if can_hit:
            sound1.play()
            speedy = -speedy
            can_hit = False
            bot_hit = True
            pl2_hit = True

    if gamemode != 3:
        if circl.colliderect(space6):
            if bot_hit:
                speedx = -speedx
                sound1.play()
                if moving == 'up':
                    if speedx>=3:
                        speedy += 1
                        speedx -= 1
                elif moving == 'down':
                    if speedx>=3:
                        speedy -= 1
                        speedx -= 1
                can_hit = True
                bot_hit = False
        
        if circl.colliderect(space7):
            if bot_hit:
                sound1.play()
                speedy = -speedy
                can_hit = True
                bot_hit = False
        
        if circl.colliderect(space8):
            if bot_hit:
                sound1.play()
                speedy = -speedy
                can_hit = True
                bot_hit = False
    #PL VS PL
    if gamemode == 3:
        if circl.colliderect(space9):
            if pl2_hit:
                sound1.play()
                speedx = -speedx
                if player2_moving == 'up':
                    if speedx >= 3:
                        speedy += 1
                        speedx -= 1
                elif player2_moving == 'down':
                    if speedx >= 3:
                        speedy -= 1
                        speedx -= 1
                can_hit = True
                pl2_hit = False

        if circl.colliderect(space10):
            if pl2_hit:
                sound1.play()
                speedy = -speedy
                can_hit = True
                pl2_hit = False
        
        if circl.colliderect(space11):
            if pl2_hit:
                sound1.play()
                speedy = -speedy
                can_hit = True
                pl2_hit = False
def main_menu():
    global title_pos_y, title_up
    screen.fill(black)
    #Buttons
    screen.blit(pl_bot, u_vs_bot)
    screen.blit(pl_pl, u_vs_pl)
    screen.blit(sets, inf_lvl)

    if title_up:
        title_pos_y += 0.5
        if title_pos_y >= 15:
            title_up = False
    else:
        title_pos_y -= 0.5
        if title_pos_y <= -20:
            title_up = True

    screen.blit(title1, (65, title_pos_y + 30))
    screen.blit(title2, (80, title_pos_y + 140))
    screen.blit(title3, (40, title_pos_y + 250))

    screen.blit(but1, (475, 120))
    screen.blit(but2, (470, 220))
    screen.blit(but3, (465, 320)) 
def player_moving_system():
    global player_moving
    key = pygame.key.get_pressed()
                
    if key[pygame.K_DOWN] and player_rect.bottom <= 390:
        player_rect.bottom += 2
        space3.bottom += 2
        space4.bottom += 2
        space5.bottom += 2
        player_moving = 'down'
        
    if key[pygame.K_UP] and player_rect.top >= 10:
        player_rect.top -= 2
        space3.top -= 2
        space4.top -= 2
        space5.top -= 2
        player_moving = 'up'
    else:
        player_moving = 'stop'

running = True
while running:
    for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False

    if gamemode == 0:
        main_menu()

        #CHOOSE GAMEMODE
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] > 450 and pos[0] < 650 and pos[1] > 100 and pos[1] < 175 :
                    gamemode = 1

                    speedx = random.uniform(-7, 7)
                    if speedx == 0:
                        speedx = -5
                        speedy = 2
                    else:
                        speedy = 7 - abs(speedx)

                if pos[0] > 450 and pos[0] < 650 and pos[1] > 300 and pos[1] < 375 :
                    gamemode = 2
                    speedx = random.uniform(-3, 3)
                    if speedx == 0:
                        speedx = 2
                        speedy = 1
                    else:
                        speedy = 3 - abs(speedx)

                if pos[0] > 450 and pos[0] < 650 and pos[1] > 200 and pos[1] < 275 :
                    gamemode = 3

                    speedx = random.uniform(-7, 7)
                    if speedx == 0:
                        speedx = -5
                        speedy = 2
                    else:
                        speedy = 7 - abs(speedx)

        
    #PLAYER VS BOT
    elif gamemode == 1:
        pygame.draw.rect(screen, yellow, space4)
        if win == False and lose == False:  
            screen.fill(black)
            menu()
            bot_moving()
            ball()
            player_moving_system()
            pygame.draw.rect(screen, yellow, space4)



            if speedx <= 0:
                speedx -= 0.01
            else:
                speedx += 0.01
            
        elif win == True and lose == False:
            screen.blit(win_text, (120, 200))
            pygame.display.update()
            clock.tick(FPS)

        elif win == False and lose == True:
            screen.blit(lose_text, (120, 200))
    #PLAYER VS PLAYER2
    elif gamemode == 3:
        if win == False and lose == False:  
            screen.fill(black)
            menu()
            ball()
            key = pygame.key.get_pressed()
            if key[pygame.K_s] and player_rect.bottom <= 390:
                player_rect.bottom += 2
                space3.bottom += 2
                space4.bottom += 2
                space5.bottom += 2
                player_moving = 'down'
            
            if key[pygame.K_w] and player_rect.top >= 10:
                player_rect.top -= 2
                space3.top -= 2
                space4.top -= 2
                space5.top -= 2
                player_moving = 'up'
            else:
                player_moving = 'stop'
            
            if key[pygame.K_DOWN] and player2_rect.bottom <= 390:
                player2_rect.bottom += 2
                space9.bottom += 2
                space10.bottom += 2
                space11.bottom += 2
                player2_moving = 'down'
            
            if key[pygame.K_UP] and player2_rect.top >= 10:
                player2_rect.top -= 2
                space9.top -= 2
                space10.top -= 2
                space11.top -= 2
                player2_moving = 'up'
            else:
                player2_moving = 'stop'

            if speedx <= 0:
                speedx -= 0.005
            else:
                speedx += 0.005
        elif win == True and lose == False:
            screen.blit(font.render('P1 won', 1, white), (120, 200))

            pygame.display.update()
            clock.tick(FPS)

        elif win == False and lose == True:
            screen.blit(font.render('P2 won', 1, white), (120, 200))

    #INFINITY
    elif gamemode == 2:
        screen.fill(black)
        menu()
        bot_moving()
        ball()
        player_moving_system()
        key = pygame.key.get_pressed()
        
        if add_speed:
            if speedx <=3:
                if speedx <= 0:
                    speedx -= 0.01
                else:
                    speedx += 0.01
            else:
                if speedx <= 0:
                    speedx -= 0.005
                else:
                    speedx += 0.005
        if abs(speedx) >= 7:
            add_speed = False
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()