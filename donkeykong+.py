# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:58:58 2019

@author: MSI
"""
import pygame
import math
import random
# Beginning
pygame.init()

screen = pygame.display.set_mode((800, 800))

sprites = [
    "mario.png",
    "marion.png",
    "marioj.png",
    "mariorev.png",
    "marionrev.png",
    "mariojrev.png",
    "mariob.png",
    "mariost.png",
    "mariostrev.png",
    "mariostend.png",
    "mariostendrev.png",
    "dk.png",
    "dkb.png",
    "phelp.png",
    "plove.png",
    "marioll.png",
    "marioh.png",
    "logo.png",
    "lotsofbarrels.png"
]

platforms = [
    ((800, 740), (800, 770), (0, 800), (0, 770)),
    ((26, 619), (720, 653), (720, 683), (26, 649)),
    ((774, 504), (774, 534), (80, 562), (80, 532)),
    ((26, 382), (720, 416), (720, 446), (26, 412)),
    ((774, 266), (774, 296), (80, 325), (80, 295)),
    ((320, 159), (720, 178), (720, 208), (320, 189)),
    ((320, 69), (480, 69), (480, 99), (320, 99)),
    ((26, 159), (320, 159), (320, 189), (26, 189)),
    ((240, 99), (320, 99), (320, 129), (240, 129))
]
# Menu Constants
barrels = []
R = 12
G = 6
VM = 5
TIME_B = 5000
VB = 5
lives = 3
remix_v = [[G, 1, 10], [R, 1, 30], [TIME_B, 1000, 10000], [VB, 1, 30], [VM, 1, 30], [lives, 1, 9]]
stairs_remix = "Normal"
font_g = pygame.font.SysFont("comicsans", 30, True)
font_menu = pygame.font.SysFont("comicsans", 50, True)
box_size = (180, 30)
xbox = 400 - int(box_size[0] / 2)
POS_CL = (xbox, 400)
POS_RE = (xbox, 500)
POS_CO = (xbox, 600)
POS_QU = (xbox, 700)
positions = [POS_CL, POS_RE, POS_CO, POS_QU]
boxes = [pygame.Rect(post, box_size) for post in positions]

# Base Functions
def draw_menu(alist):
    font_menu = pygame.font.SysFont("comicsans", 50, True)
    cl_text = font_menu.render("Classic", 1, pygame.Color(alist[0]))
    re_text = font_menu.render("Remix", 1, pygame.Color(alist[1]))
    co_text = font_menu.render("Controls", 1, pygame.Color(alist[2]))
    qu_text = font_menu.render("Quit", 1, pygame.Color(alist[3]))
    texts = [cl_text, re_text, co_text, qu_text]
    text_string = ["Classic", "Remix", "Controls", "Quit"]
    text_size = [font_menu.size(txt) for txt in text_string]
    screen.fill((0, 0, 0))
    for box in boxes:
        ind = boxes.index(box)
        pygame.draw.rect(screen, pygame.Color("white"), box, 1)
        screen.blit(texts[ind], (int(xbox + int(box_size[0] / 2)) - int(text_size[ind][0] / 2), positions[ind][1]))
    screen.blit(pygame.transform.scale(pygame.image.load(sprites[17]), (444, 300)), (178, 50))
    pygame.display.update()
    pygame.display.flip()


def plat_lim(plat):
    xmin = 800
    xmax = 0
    for atuple in platforms[plat]:
        if atuple[0] < xmin:
            xmin = atuple[0]
        if atuple[0] > xmax:
            xmax = atuple[0]
    return list(range(xmin, xmax + 1))


def inplat(x, plat, c):
    lrange = plat_lim(plat)
    return int(x) in range(lrange[0] - c, lrange[-1])


def y_min(x, plat):
    p = list(platforms[plat])
    y1 = 800
    y2 = 800
    x1 = p[0][0]
    for a in range(len(p)):
        if p[a][0] != x1:
            x2 = p[a][0]
    for i in p:
        if i[0] == x1:
            if i[1] < y1:
                y1 = i[1]
        if i[0] == x2:
            if i[1] < y2:
                y2 = i[1]
    n = (y2 - y1) / (x2 - x1)
    b = y1 - (n * x1)
    return (n * x + b)


def st(x, plat):
    return ((x, y_min(x, plat + 1)), (x + 40, y_min(x + 40, plat + 1)), (x + 40, y_min(x + 40, plat)), (x, y_min(x, plat)))


def findx(plat, xx0, xx1):
    if plat >= 5:
        pl = [350, plat_lim(plat)[-1] - 40]
    elif plat == 0:
        pl = [200, plat_lim(plat + 1)[-1] - 40]
    else:
        lcplat = [plat_lim(plat)[0], plat_lim(plat)[-1] - 40]
        lnplat = [plat_lim(plat + 1)[0], plat_lim(plat + 1)[-1] - 40]
        pl = [max(lcplat[0], lnplat[0]), min(lcplat[1], lnplat[1])]
    if xx0 == -1 and xx1 == -1:
        return random.randrange(pl[0], pl[1])
    elif xx0 != -1 and xx1 == -1:
        if xx0 - 50 <= pl[0]:
            return random.randrange(xx0 + 50, pl[1])
        elif xx0 + 50 >= pl[1]:
            return random.randrange(pl[0], xx0 - 50)
        else:
            d = random.randrange(0, 2)
            if d == 0:
                return random.randrange(pl[0], xx0 - 50)
            else:
                return random.randrange(xx0 + 50, pl[1])
    else:
        if xx1 < xx0:
            xx2 = xx0
            xx0 = xx1
            xx1 = xx2
        if xx0 - 50 <= pl[0]:
            if xx1 + 50 >= pl[1]:
                return random.randrange(xx0 + 50, xx1 - 50)
            else:
                d = random.randrange(0, 2)
                if d == 0 and xx1 - 50 > xx0 + 50:
                    return random.randrange(xx0 + 50, xx1 - 50)
                else:
                    return random.randrange(xx1 + 50, pl[1])
        else:
            if xx1 + 50 >= pl[1]:
                d = random.randrange(0, 2)
                if d == 0 and xx1 - 50 > xx0 + 50:
                    return random.randrange(xx0 + 50, xx1 - 50)
                else:
                    return random.randrange(pl[0], xx0 - 50)
            else:
                d = random.randrange(0, 3)
                if d == 0:
                    return random.randrange(pl[0], xx0 - 50)
                elif d == 1 and xx1 - 50 > xx0 + 50:
                    return random.randrange(xx0 + 50, xx1 - 50)
                else:
                    return random.randrange(xx1 + 50, pl[1])

# Modes
intro = True
classic = False
menu = True
play = False
remix = False
running = True
clock = pygame.time.Clock()
# Game Cicle / Events
while running is True:
    dt = clock.tick(30) / 50
    if dt > 3:
        dt = 1
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
# Mouse Function
    def mouse_over(box_size, pos):
        return mpos[0] in range(pos[0], pos[0] + box_size[0]) and mpos[1] in range(pos[1], pos[1] + box_size[1])
# Initial Menu
    if menu is True:
        win = False
        intro = True
        mpos = pygame.mouse.get_pos()
        colors = ["yellow", "yellow", "yellow", "yellow"]
        for p in positions:
            ind = positions.index(p)
            if mouse_over(box_size, p) is True:
                colors[ind] = "blue"
            else:
                colors[ind] = "yellow"
        draw_menu(colors)
        if mouse_over(box_size, POS_CL) and click:
            classic = True
            play = True
            menu = False
        if mouse_over(box_size, POS_RE) and click:
            remix = True
            menu = False
        if mouse_over(box_size, POS_QU) and click:
            menu = False
            running = False
# Remix Menu
    if remix is True:
        mpos = pygame.mouse.get_pos()
        remix_text_string = ["-", "+", "Gravity", "Barrel Size", "Barrel Time", "Barrel Velocity", "Mario Velocity", "Lives", "Stairs", "Play", "Back"]
        y_remix = [125, 200, 275, 350, 425, 500, 575, 700]
        remix_text_size = [font_menu.size(rtxt) for rtxt in remix_text_string]
        remix_size_x = [sizetxt[0] for sizetxt in remix_text_size]
        remix_size_y = remix_text_size[0][1]
        r_text = [font_menu.render(remixtxt, 1, pygame.Color("yellow")) for remixtxt in remix_text_string[2:-1]]
        r_box_size = (max(remix_size_x), remix_size_y)
        r_box_x = 400 - int(r_box_size[0] / 2)
        r_boxes = [pygame.Rect((r_box_x - 100, r_box_y), r_box_size) for r_box_y in y_remix[:-1]]
        if mouse_over((160, 35), (460, 575)) and click:
            if stairs_remix == "Random":
                stairs_remix = "Normal"
            else:
                stairs_remix = "Random"
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((400 - int(r_box_size[0] / 2), y_remix[-1]), r_box_size), 1)
        if mouse_over(r_box_size, (400 - int(r_box_size[0] / 2), y_remix[-1])):
            screen.blit(font_menu.render(remix_text_string[-2], 1, pygame.Color("blue")), (360, y_remix[-1]))
        else:
            screen.blit(font_menu.render(remix_text_string[-2], 1, pygame.Color("yellow")), (360, y_remix[-1]))
        for nv in range(len(remix_v)):
                if mouse_over((35, 35), (105, y_remix[nv])) and click and remix_v[nv][0] > remix_v[nv][1]:
                    remix_v[nv][0] -= remix_v[nv][1]
                if mouse_over((35, 35), (572, y_remix[nv])) and click and remix_v[nv][0] < remix_v[nv][2]:
                    remix_v[nv][0] += remix_v[nv][1]
        for r_box in r_boxes:
            ind = r_boxes.index(r_box)
            pygame.draw.rect(screen, pygame.Color("white"), r_box, 1)
            screen.blit(r_text[ind], (300 - int(remix_size_x[ind + 2] / 2), y_remix[ind]))
        for y_r in y_remix[:-2]:
            yind = y_remix.index(y_r)
            if yind == 2:
                v = int(remix_v[yind][0] / 1000)
            else:
                v = remix_v[yind][0]
            pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((105 , y_r), (35, 35)), 1)
            if mouse_over((35, 35), (105, y_r)):
                screen.blit(font_menu.render("-", 1, pygame.Color("blue")), (116, y_r))
            else:
                screen.blit(font_menu.render("-", 1, pygame.Color("yellow")), (116, y_r))
            pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((572 , y_r), (35, 35)), 1)
            if mouse_over((35, 35), (572, y_r)):
                screen.blit(font_menu.render("+", 1, pygame.Color("blue")), (579, y_r - 2))
            else:
                screen.blit(font_menu.render("+", 1, pygame.Color("yellow")), (579, y_r - 2))
            pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((460 , y_r), (100, 35)), 1)
            screen.blit(font_menu.render(str(v), 1, pygame.Color("yellow")), (470, y_r))
        pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((460 , 575), (160, 35)), 1)
        if mouse_over((160, 35), (460, 575)):
            screen.blit(font_menu.render(stairs_remix, 1, pygame.Color("blue")), (462, 575))
        else:
            screen.blit(font_menu.render(stairs_remix, 1, pygame.Color("yellow")), (462, 575))
        pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((39 , 650), (112, 35)), 1)
        if mouse_over((112, 35), (39, 650)):
            screen.blit(font_menu.render("Reset", 1, pygame.Color("blue")), (39, 650))
            if click:
                stairs_remix = "Normal"
                R = 12
                G = 6
                VM = 5
                TIME_B = 5000
                VB = 5
                lives = 3
                remix_v = [[G, 1, 10], [R, 1, 30], [TIME_B, 1000, 10000], [VB, 1, 10], [VM, 1, 10], [lives, 1, 9]]
        else:
            screen.blit(font_menu.render("Reset", 1, pygame.Color("yellow")), (39, 650))
        pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect((39 , 700), (112, 35)), 1)
        if mouse_over((112, 35), (39, 700)):
            screen.blit(font_menu.render("Back", 1, pygame.Color("blue")), (47, 700))
            if click:
                remix = False
                menu = True
        else:
            screen.blit(font_menu.render("Back", 1, pygame.Color("yellow")), (47, 700))
        pygame.display.update()
        pygame.display.flip()
        if mouse_over(r_box_size, (400 - int(r_box_size[0] / 2), y_remix[-1])) and click:
            G = remix_v[0][0] 
            R = remix_v[1][0]
            TIME_B = remix_v[2][0]
            VB = remix_v[3][0]
            VM = remix_v[4][0]
            lives = remix_v[5][0]
            intro = True
            remix = False
            play = True
# Intro/Revive
    if play is True:
        if intro is True:
            if classic is True:
                stairs_remix = "Normal"
                G = 6
                R = 12
                TIME_B = 5000
                VB = 5
                VM = 5
                lives = 3
                classic = False
            sprt = sprites[1]
            dk_sprt = sprites[11]
            p_sprt = sprites[13]
            last_sprt = sprites[0]
            cplat = 0
            plat_max = 0
            jumptime = 0
            climbing = False
            lost_life = False
            win = False
            win_menu = False
            gameover = False
            time_last_barrel = pygame.time.get_ticks()
            anim_time = pygame.time.get_ticks()
            score = 0
            rscore = 0
            x = 180
            y = 763
            xb = 240
            yb = 159
            barrels = []
            LB = math.sqrt(2 * (R ** 2))
            SIZE = (30, 45)
            DK_SIZE = (150, 110)
            A_BARREL = (math.pi) * (R ** 2)
            DK_POS = [240 - DK_SIZE[0], 159 - DK_SIZE[1]]
            P_SIZE = (80, 60)
            P_POS = (320, 69 - P_SIZE[1])
            SCORE_POS = (600, 10)
            LIVES_POS = (600, 40)
            barrels.append([xb, yb, 7])
            if stairs_remix == "Normal":
                x00 = 640
                x01 = 280
                x10 = 120
                x11 = 340
                x20 = 400
                x21 = 640
                x22 = 240
                x30 = 120
                x31 = 220
                x32 = 580
                x40 = 640
                x41 = 320
            else:
                x00 = findx(0, -1, -1)
                x01 = findx(0, x00, -1)
                x10 = findx(1, -1, -1)
                x11 = findx(1, x10, -1)
                x20 = findx(2, -1, -1)
                x21 = findx(2, x20, -1)
                x22 = findx(2, x20, x21)
                x30 = findx(3, -1, -1)
                x31 = findx(3, x30, -1)
                x32 = findx(3, x30, x31)
                x40 = findx(4, -1, -1)
                x41 = findx(4, x40, -1)
            stairs = [
                    (0, st(x00, 0)),
                    (1, st(x10, 1)),
                    (1, st(x11, 1)),
                    (2, st(x20, 2)),
                    (2, st(x21, 2)),
                    (3, st(x30, 3)),
                    (3, st(x31, 3)),
                    (4, st(x40, 4)),
                    (5, ((440, 69), (480, 69), (480, 167), (440, 167)))
                    ]
            stairs_broken = [
                            (0, st(x01, 0)),
                            (2, st(x22, 2)),
                            (3, st(x32, 3)),
                            (4, st(x41, 4)),
                            (5, ((240, 99), (280, 99), (280, 159), (240, 159))),
                            (5, ((280, 99), (320, 99), (320, 159), (280, 159)))
                        ]
            intro = False
# Characters / Texts
        Mario = pygame.transform.scale(pygame.image.load(sprt), SIZE)
        Mario_lostlife = pygame.transform.scale(pygame.image.load(sprites[15]), SIZE)
        Dk = pygame.transform.scale(pygame.image.load(dk_sprt), DK_SIZE)
        Princess = pygame.transform.scale(pygame.image.load(p_sprt), P_SIZE)
        last_sprt = sprt
        text_score = font_g.render("Score: " + str(score), 1, pygame.Color('white'))
        text_lives = font_g.render("Lives: " + str(lives), 1, pygame.Color('white'))
        text_gameover = font_menu.render("Game Over", 1, pygame.Color('white'))
        pos = (x, y)
# Draw Functions 
        def draw_screen(stairs, stairs_broken, platforms):
            for s in stairs:
                pygame.draw.polygon(screen, pygame.Color('blue'), s[1])
            for sb in stairs_broken:
                pygame.draw.polygon(screen, pygame.Color('brown'), sb[1])
            for p in platforms:
                pygame.draw.polygon(screen, pygame.Color('red'), p)
            screen.blit(pygame.transform.scale(pygame.image.load(sprites[18]), (75, 100)), (25, 60))

        def draw_screen_charct(stairs, stairs_broken, platforms, Dk, Princess, text_score):
            draw_screen(stairs, stairs_broken, platforms)
            screen.blit(Princess, P_POS)
            screen.blit(Dk, DK_POS)
            screen.blit(text_score, SCORE_POS)
# Stairs Detection Functions
        def inst(x, y, plat, size):
            stairs_plat = []
            for s in stairs:
                if s[0] == plat:
                    stairs_plat.append(s[1])
            for ss in stairs_plat:
                if int(x) + (size[0] / 2) in range(ss[0][0], ss[1][0]) and y <= y_min(x, cplat) - size[1]:
                    return True
            return False

        def inbst(x, y, plat, size):
            bstairs_plat = []
            for sb in stairs_broken:
                if sb[0] == plat:
                    bstairs_plat.append(sb[1])
            for ssb in bstairs_plat:
                if int(x) + (size[0] / 2) in range(ssb[0][0], ssb[1][0]) and y <= y_min(x, cplat) - size[1]:
                    return True
            return False
# Lost Life Case
        if lost_life:
            lives -= 1
            if lives == 0:
                gameover = True
            text_lives = font_g.render("Lives: " + str(lives), 1, pygame.Color('white'))
            barrels = []
            y = y_min(x, cplat) - SIZE[1]
            screen.fill((0, 0, 0))
            draw_screen_charct(stairs, stairs_broken, platforms, Dk, Princess, text_score)
            screen.blit(pygame.transform.scale(pygame.image.load(sprites[16]), SIZE), (x, y))
            pygame.display.update()
            pygame.display.flip()
            pygame.time.wait(1000)
            while y < 799:
                screen.fill((0, 0, 0))
                draw_screen_charct(stairs, stairs_broken, platforms, Dk, Princess, text_score)
                screen.blit(Mario_lostlife, (x, y))
                screen.blit(text_score, SCORE_POS)
                pygame.display.update()
                pygame.display.flip()
                y += 2 * dt
            x = 180
            y = 763
            jumptime = 0
            climbing = False
            cplat = 0
            plat_max = 0
            sprt = sprites[1]
            screen.fill((0, 0, 0))
            if gameover is True:
                screen.blit(text_gameover, (400 - int(font_menu.size("Game Over")[0] / 2), 400 - int(font_menu.size("Game Over")[1] / 2)))
            else:
                screen.blit(text_lives, (400 - int(font_g.size("Lives: " + str(lives))[0] / 2), 400 - int(font_g.size("Lives: " + str(lives))[1] / 2)))
            pygame.display.update()
            pygame.display.flip()
            if gameover is True:
                pygame.time.wait(3500)
            else:
                pygame.time.wait(2000)
            if gameover is True:
                menu = True
                play = False
                gameover = False
            lost_life = False
# Win Case
        if win is True:
            barrels = []
            screen.fill((0, 0, 0))
            y = 69 - SIZE[1]
            draw_screen(stairs, stairs_broken, platforms)
            p_sprt = sprites[14]
            screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(sprites[11]), DK_SIZE), 180), (DK_POS[0], 680))
            sprt = sprites[4]
            screen.blit(pygame.transform.scale(pygame.image.load(p_sprt), P_SIZE), P_POS)
            screen.blit(pygame.transform.scale(pygame.image.load(sprt), SIZE), (x, y))
            pygame.display.update()
            pygame.display.flip()
            pygame.time.wait(3000)
            screen.fill((0, 0, 0))
            screen.blit(font_menu.render("Congratulations!!!", 1, pygame.Color("white")), (218, 370))
            screen.blit(text_score, (353, 410))
            pygame.display.update()
            pygame.display.flip()
            pygame.time.wait(3000)
            play = False
            menu = True
# Platform              
        if inplat(x, cplat, SIZE[0]) is False and y == y_min(x, cplat) - SIZE[1]:
            cplat -= 1
# Keys
        if not lost_life and not win:
            keys = pygame.key.get_pressed()

        if inst(x, y, cplat - 1, SIZE) is True and keys[pygame.K_DOWN]:
            cplat -= 1
            climbing = True

        if keys[pygame.K_q]:
            running = False

        if keys[pygame.K_m]:
            play = False
            menu = True

        if keys[pygame.K_SPACE]:
            if y == y_min(x, cplat) - SIZE[1]:
                jumptime = 10

        if keys[pygame.K_RIGHT]:
            if int(x) < 760 and climbing is False and win is False:
                x += VM * dt

        if keys[pygame.K_LEFT]:
            if cplat < 5:
                if int(x) > 0 and climbing is False and win is False:
                    x -= VM * dt
            else:
                if int(x) > 320 and climbing is False and win is False:
                    x -= VM * dt
# Jump 
        if jumptime != 0:
            y -= G
            jumptime -= 1
        else:
            y = min(y, y_min(x, cplat) - SIZE[1])

        if jumptime == 0 and climbing is False:
            y += G
            if y > y_min(x, cplat) - SIZE[1]:
                y = y_min(x, cplat) - SIZE[1]

        if y < y_min(x, cplat) - SIZE[1] and climbing is False:
            if keys[pygame.K_LEFT]:
                sprt = sprites[5]
            elif keys[pygame.K_RIGHT]:
                sprt = sprites[2]
            else:
                if last_sprt == sprites[0] or last_sprt == sprites[1]:
                    sprt = sprites[2]
                if last_sprt == sprites[3] or last_sprt == sprites[4]:
                    sprt = sprites[5]
# Sprites
        if y == y_min(x, cplat) - SIZE[1] and climbing is False:
            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                if last_sprt != sprites[0] and last_sprt != sprites[1]:
                    sprt = sprites[1]
                if last_sprt == sprites[1]:
                    if pygame.time.get_ticks() - anim_time > 100:
                        sprt = sprites[0]
                if last_sprt == sprites[0]:
                    if pygame.time.get_ticks() - anim_time > 100:
                        sprt = sprites[1]
            elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                if last_sprt != sprites[3] and last_sprt != sprites[4]:
                    sprt = sprites[4]
                if last_sprt == sprites[4]:
                    if pygame.time.get_ticks() - anim_time > 100:
                        sprt = sprites[3]
                if last_sprt == sprites[3]:
                    if pygame.time.get_ticks() - anim_time > 100:
                        sprt = sprites[4]
            else:
                if last_sprt == sprites[5]:
                    sprt = sprites[4]
                if last_sprt == sprites[2]:
                    sprt = sprites[1]
# Climbing and Sprites
        if climbing is True:
            if y == y_min(x, cplat) - SIZE[1]:
                sprt = sprites[6]
            elif y - y_min(x, cplat + 1) > 10:
                if (keys[pygame.K_UP] and not keys[pygame.K_DOWN]) or (keys[pygame.K_DOWN] and not keys[pygame.K_UP]):
                    if last_sprt != sprites[7] and last_sprt != sprites[8]:
                        sprt = sprites[7]
                    if last_sprt == sprites[7]:
                        if pygame.time.get_ticks() - anim_time > 200:
                            sprt = sprites[8]
                    if last_sprt == sprites[8]:
                        if pygame.time.get_ticks() - anim_time > 200:
                            sprt = sprites[7]
            else:
                if (keys[pygame.K_UP] and not keys[pygame.K_DOWN]) or (keys[pygame.K_DOWN] and not keys[pygame.K_UP]):
                    if last_sprt != sprites[9] and last_sprt != sprites[10]:
                        sprt = sprites[9]
                    if last_sprt == sprites[9]:
                        if pygame.time.get_ticks() - anim_time > 200:
                            sprt = sprites[10]
                    if last_sprt == sprites[10]:
                        if pygame.time.get_ticks() - anim_time > 200:
                            sprt = sprites[9]
# Animation Time
        if last_sprt != sprt:
            anim_time = pygame.time.get_ticks()

        if cplat > plat_max:
            plat_max = cplat
        if inst(x, y, cplat, SIZE) is True:
            if y == y_min(x, cplat) - SIZE[1] and keys[pygame.K_UP]:
                climbing = True
            if climbing is True:
                if keys[pygame.K_DOWN]:
                    y += VM
                if keys[pygame.K_UP]:
                    y -= VM
            if y < y_min(x, cplat + 1) - SIZE[1]:
                if cplat == plat_max:
                    score += 200
                    rscore += 200
                cplat += 1
                climbing = False
                sprt = sprites[6]
# Climbing State and Sprites
        if y == y_min(x, cplat) - SIZE[1] or inst(x, y, cplat, SIZE) is False:
            climbing = False

        if inst(x, y, cplat, SIZE) is True and climbing is False:
            if last_sprt == sprites[7] or last_sprt == sprites[8]:
                sprt = sprites[6]

        for barrel in barrels:
            if barrel[2] == 7 and int(barrel[0]) in range (319, 326):
                barrel[2] -= 2
# Barrels
        for barrel in barrels:
            if inplat(int(barrel[0]), barrel[2], R) is True:
                if barrel[1] + R < y_min(int(barrel[0]), barrel[2]):
                    barrel[1] += (VB + 2) * dt
                else:
                    if barrel[2] % 2 == 0:
                        barrel[0] -= VB * dt
                    else:
                        barrel[0] += VB * dt
            else:
                barrel[2] -= 1
            if barrel[2] == 0 and barrel[0] <= R:
                barrels.remove(barrel)
            if barrel[2] == cplat and climbing is False:
                if lost_life is False and x + int(SIZE[0] / 2) in range(int(barrel[0]) - int(VM / 2), int(barrel[0]) + int(VM / 2)) and y + (SIZE[1] / 2) < barrel[1]:
                    score += 100
                    rscore += 100

        if pygame.time.get_ticks() - time_last_barrel > TIME_B and win is False:
            barrels.append([xb, yb, 7])
            time_last_barrel = pygame.time.get_ticks()
        if pygame.time.get_ticks() - time_last_barrel > TIME_B - 200 or pygame.time.get_ticks() - time_last_barrel < 200:
            dk_sprt = sprites[12]
        else:
            dk_sprt = sprites[11]

        for barrel in barrels[1:]:
            if barrel[2] > cplat:
                if inst(int(barrel[0]), barrel[1], barrel[2] - 1, (0, SIZE[1])) or inbst(int(barrel[0]), barrel[1], barrel[2] - 1, (0, SIZE[1])):
                    barrel_x = [bb[0] for bb in barrels if bb[2] == barrel[2] - 1]
                    for bx in barrel_x:
                        if abs(int(barrel[0]) - bx) > 250:
                            if abs(int(barrel[0]) - x) <= 3:
                                barrel[2] -= 1
                            if barrel[0] > x and keys[pygame.K_RIGHT]:
                                barrel[2] -= 1
                            if barrel[0] < x and keys[pygame.K_LEFT]:
                                barrel[2] -= 1
# Barrel Draw
        screen.fill((0, 0, 0))
        draw_screen(stairs, stairs_broken, platforms)
        for barrel in barrels:
            if lost_life is False:
                pygame.draw.circle(screen, pygame.Color('sandybrown'), (int(barrel[0]), int(barrel[1])), R)

        Mariobox = pygame.Rect(pos, SIZE)
        for barrel in barrels:
            box = pygame.Rect(int(barrel[0]) - (LB / 2), barrel[1] - (LB / 2), LB, LB)
            if Mariobox.colliderect(box):
                lost_life = True
# Win and Lost Life Conditions
        if cplat == 6:
            win = True

        if lost_life is False:
            screen.blit(Mario, pos)

        if win is False:
            p_sprt = sprites[13]
            screen.blit(Dk, DK_POS)
# Real Score
        if rscore >= 3000:
            lives += 1
            rscore = 0
# Screen Update
        screen.blit(Princess, P_POS)
        screen.blit(text_score, SCORE_POS)
        screen.blit(text_lives, LIVES_POS)
        pygame.display.update()
        pygame.display.flip()
# End
del font_g
del font_menu
pygame.display.quit()
pygame.quit()

"""
# Equações retas superiores das plataformas:
# Plat 0 == (-30/800) * x + 770 ((800, 740), (800, 770), (0, 800), (0, 770))
# Plat 1 == (17/347) * x + 618 ((26, 619), (720, 653), (720, 683), (26, 649))
# Plat 2 == (-14/347) * x + 535 ((774, 504), (774, 534), (80, 562), (80, 532))
# Plat 3 == (17/347) * x + 381 ((26, 382), (720, 416), (720, 446), (26, 412))
# Plat 4 == (-14/347) * x + 297 ((774, 266), (774, 296), (80, 325), (80, 295))
# Plat 5 inclinada == (19/400) * x + 144 ((320, 159), (720, 178), (720, 208), (320, 189))
# Plat 6 Princesa == 69 ((320, 69), (480, 69), (480, 99), (320, 99))
# Plat 7 plana == 159 ((26, 159), (320, 159), (320, 189), (26, 189))
# Plat 8 Barris == 99 ((240, 99), (320, 99), (320, 129), (240, 129))
"""
