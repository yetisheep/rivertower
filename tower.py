import pygame
from pygame.locals import *
import sys
import os
import time

pygame.mixer.init()
pygame.init()#Pygame模組初始化

###必要參數設置###
#紀錄開始時間
time_start = time.time()
#偵測塔是否已建立
tower_exist = list()
tower_correct = list()
#預留空間放置關卡訊息
text_bar_size = 30
#畫面大小
size_width = 800
size_height = 600
size = (size_width, size_height + text_bar_size)
#方格大小
grid_size = 100
grid_linewidth = 1
#選擇框位置變數
choosex = choosey = 0
#顏色變數
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHTGRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 255, 255)
soundwav=pygame.mixer.Sound("tower_music.wav")
soundwav.set_volume(0.3)
pygame.mixer.music.load("tower_music.wav")
pygame.mixer.music.set_volume(0.5)

pygame.mixer.music.load("bgm.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)


#字型設定
font = pygame.font.SysFont("times", 30)
font2 = pygame.font.SysFont("times", 60)

###關卡設計###
ROUND1_RIVER = [(0, 0), (grid_size, 0), (grid_size, grid_size), (2*grid_size, 2*grid_size),(2*grid_size, 3*grid_size),
                (2*grid_size, 4*grid_size),(4*grid_size, 0) ,(5*grid_size, 1*grid_size) ,
                (4*grid_size, 1*grid_size), (5*grid_size, 2*grid_size) , (6*grid_size, 2*grid_size) ,(7*grid_size, 2*grid_size) ,
                (5*grid_size, 3*grid_size) ,(5*grid_size, 4*grid_size) ,(3*grid_size, 3*grid_size) ,
                (3*grid_size, 4*grid_size), (4*grid_size, 4*grid_size) , ]
ROUND1_COUNT = 10

###創建畫面###
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("The Tower of River")
GAME = pygame.Surface(screen.get_size())
GAME = GAME.convert()


#創建方框方法
def GridCreate():
    for x in range(size_width//grid_size):
        for y in range(size_height//grid_size):
            pygame.draw.rect(screen, BLACK, ((x*grid_size, y*grid_size), (grid_size, grid_size)), grid_linewidth)

#畫出塔方法，塔是否位於河流上
def TowerExist():
    for x in range(size_width//grid_size):
        for y in range(size_height//grid_size):
            if (x*grid_size, y*grid_size) in tower_exist:
                if TowerTogether(x*grid_size, y*grid_size):
                    pygame.draw.circle(screen, RED, (x*grid_size + grid_size//2, y*grid_size + grid_size//2), (grid_size//3), 0)
                else:
                    if (x*grid_size, y*grid_size) in ROUND1_RIVER:
                        pygame.draw.circle(screen, GREEN, (x*grid_size + grid_size//2, y*grid_size + grid_size//2), (grid_size//3), 0)
                       
                    else:
                        pygame.draw.circle(screen, GRAY, (x*grid_size + grid_size//2, y*grid_size + grid_size//2), (grid_size//3), 0)
                        
#判斷塔與塔是否相鄰
def TowerTogether(x, y):
    if (x-grid_size, y) in tower_exist or (x+grid_size, y) in tower_exist or (x, y-grid_size) in tower_exist or (x, y+grid_size) in tower_exist:
        return True
    else:
        return False

#判斷塔是否位於正確位置
def TowerCorrect():
    for x in range(size_width//grid_size):
        for y in range(size_height//grid_size):
            if (x*grid_size, y*grid_size) in tower_exist:
                if TowerTogether(x*grid_size, y*grid_size) == False and (x*grid_size, y*grid_size) in ROUND1_RIVER:
                    if (x*grid_size, y*grid_size) not in tower_correct:
                        tower_correct.append((x*grid_size, y*grid_size))
                if TowerTogether(x*grid_size, y*grid_size):
                    if (x*grid_size, y*grid_size)  in tower_correct:
                        del tower_correct[tower_correct.index((x*grid_size, y*grid_size))]
    
#關卡河流產生
def RiverCreate():
    for x in range(size_width//grid_size):
        for y in range(size_height//grid_size):
            if (x*grid_size, y*grid_size) in ROUND1_RIVER:
                pygame.draw.rect(screen, SKYBLUE, ((x*grid_size+grid_linewidth, y*grid_size+grid_linewidth), (grid_size-grid_linewidth*2, grid_size-grid_linewidth*2)), 0)
            else:
                pygame.draw.rect(screen, WHITE, ((x*grid_size+grid_linewidth, y*grid_size+grid_linewidth), (grid_size-grid_linewidth*2, grid_size-grid_linewidth*2)), 0)

#過關判斷
def Pass():
    if len(tower_correct) == ROUND1_COUNT:
        PASS_TEXT = font2.render('Pass!!!', True, RED)
        screen.blit(PASS_TEXT, ((100, size_height//2), (size_width, text_bar_size)))


###主遊戲運作###
while True:
    text10 = 'Tower:', len(tower_correct), 'Tower require:', ROUND1_COUNT, 'Built Tower:', len(tower_exist)
    text1 = str(text10)
    #print(text1)
    ROUND1_TEXT = font.render(text1, True, BLACK)
    RiverCreate()#背景設置
    GridCreate()#建立方格及塔建立與否偵測器
    TowerExist()#建立塔方法呼叫
    pygame.draw.rect(screen, LIGHTGRAY, ((0, size_height), (size_width, text_bar_size)), 0)
    screen.blit(ROUND1_TEXT, ((0, size_height), (size_width, text_bar_size)))
    pygame.draw.rect(screen, PURPLE, ((choosex, choosey), (grid_size, grid_size)), 8)#畫出選擇框
    Pass()

    #事件處理
    for event in pygame.event.get():
        if event.type == QUIT:#離開遊戲
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if choosex > 0:
                    choosex -= grid_size
            if event.key == K_RIGHT:
                if choosex < size_width-grid_size:
                    choosex += grid_size
            if event.key == K_UP:
                if choosey >0:
                    choosey -= grid_size
            if event.key == K_DOWN:
                if choosey < size_height-grid_size:
                    choosey += grid_size
            if event.key == K_SPACE:#空白鍵按下建造或刪去塔
                
                if (choosex, choosey) in tower_exist:
                    del tower_exist[tower_exist.index((choosex, choosey))]
                    if (choosex, choosey) in tower_correct:
                        del tower_correct[tower_correct.index((choosex, choosey))]
                else:
                    tower_exist.append((choosex, choosey))
                    soundwav.play()
                   
                TowerCorrect()#每次按下空白鍵檢查塔是否位於正確位置

    pygame.display.update()#畫面更新方法呼叫
