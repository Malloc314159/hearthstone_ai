import random as rd
import pygame as pg  # pygame library
import time
from pygame.locals import *
import threading
import copy
import sys
input=sys.stdin.readline

class Card:
    def __init__(self):
        self.name = 0
        self.number=0
        self.attack = 0
        self.health = 0
        self.fightHealth = 0
        self.fightAttack = 0
        self.alive=True
        self.golden=False
        self.tribe = 0
        self.ability = 0
        self.abilused=False
        self.star = 0 #하수인 별
        self.goldenHealth = 0
        self.goldenAttack = 0
        self.goldenAbility = 0

pg.init()
screen = pg.display.set_mode((1500, 720))
pg.display.set_caption('HearthStone_Beta')
stop = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
sec = 1
Round = 0
playerCard = []  # 플레이어가 들고 있는 카드
cardImg = []
goldencardImg = []
cardList = []
playerGround = []  # 플레이어 전장
opponentGround = []  # 상대 전장
playerHealth = 20 #플레이어 체력
op1Health = 20
op2Health = 20
op3Health = 20
p2tGround=[]
p3tGround=[]
p4tGround=[]
p2Ground = []
p3Ground = []
p4Ground = []
buyList = []  # 선술집 목록
shopCard_number = [3, 4, 4, 5, 5, 6]  # 선술집에서 나오는 카드 수
shopLevel_cost = [5, 7, 8, 9, 11]
shopLevel = 1
freezed = False  # check if freezed
upgraded = False  # check if upgraded this turn
upgrade_cost = 5
gold = 0
max_gold = 0
cardLimit = [18, 15, 13, 11, 9, 7]  # 등급별 총 복사본 개수(근데 이거 4명이서 하면 바꿔야함)
cardCount = []
cardBound = [0, 6, 14, 26, 40, 51, 62]
font30 = pg.font.Font('NanumGothic.ttf', 30)
font20 = pg.font.Font('NanumGothic.ttf', 20)
rrButton=pg.image.load('reroll.png')
upButton=pg.image.load('upgrade.png')
freezeButton=pg.image.load('freeze.png')
rrButton=pg.transform.scale(rrButton, (50,50))
upButton=pg.transform.scale(upButton, (50,50))
freezeButton=pg.transform.scale(freezeButton, (50,50))
op=1
opAlive=[True]*3
'''
cardStats -> <Level> <Attack> <Health> <Ability> <Tribe>
goldencardStats -> <Attack> <Health> <Ability>

Effect numbers:
Battlecry - 1           전투의 함성
Deathrattle - 2         죽음의 메아리
Divine Shield - 3       천상의 보호막
Taunt - 4               도발

Tribe numbers:
Dragon - 1              용족
Mech - 2                기계
Murloc - 3              멀록
'''

def printText():
    global freezed
    screen.fill(BLACK)

    for i in range(len(buyList)):
        tmp = buyList[i].number
        screen.blit(cardImg[tmp], (i * 210, 40))
    if freezed == True:
        text1 = 'Freezed'
        freezedimg = font30.render(text1, True, WHITE)
        screen.blit(freezedimg, (20, 500))
    for i in range(len(playerGround)):
        tmp = playerGround[i].number
        if playerGround[i].golden:
            screen.blit(goldencardImg[tmp], (i*200+270, 250))
        else:
            screen.blit(cardImg[tmp], (i * 200 + 270, 250))

    text1 = 'Buy List'
    buylistimg = font30.render(text1, True, WHITE)
    screen.blit(buylistimg, (20, 0))
    text1 = 'Gold: ' + str(gold)
    goldimg = font30.render(text1, True, WHITE)
    screen.blit(goldimg, (20, 340))
    text2 = 'Level: ' + str(shopLevel)
    levelimg = font30.render(text2, True, WHITE)
    screen.blit(levelimg, (20, 370))
    text1 = 'Upgrade Cost: ' + str(upgrade_cost)
    upgrade_costimg = font30.render(text1, True, WHITE)
    screen.blit(upgrade_costimg, (20, 400))
    text1='Player Health: '+str(playerHealth)
    healthimg=font30.render(text1, True, WHITE)
    screen.blit(healthimg, (20,430))
    screen.blit(rrButton, (150, 0))
    screen.blit(upButton, (210, 0))
    screen.blit(freezeButton, (270, 0))
    pg.display.flip()


def reset():  # 전장 새로고침
    screen.fill(BLACK)
    buyList.clear()
    for i in range(shopCard_number[shopLevel - 1]):
        tmp = rd.randrange(0, cardBound[shopLevel])
        buyList.append(copy.deepcopy(cardList[tmp]))
    printText()


def freeze():  # 전장 빙결
    global freezed
    freezed = not freezed
    printText()

def upgrade():  # 선술집 강화
    global gold, upgrade_cost, shopLevel, upgraded
    if gold - upgrade_cost >= 0:
        if shopLevel < 6:
            gold -= upgrade_cost
            shopLevel += 1
            if shopLevel==6:
                upgrade_cost=10000
            else:
                upgrade_cost = shopLevel_cost[shopLevel - 1]
            upgraded = True
    printText()

def discover():
    screen.fill(BLACK)
    if shopLevel<6:
        tmp_1 = rd.randint(cardBound[shopLevel], cardBound[shopLevel + 1])
        tmp_2 = rd.randint(cardBound[shopLevel], cardBound[shopLevel + 1])
        tmp_3 = rd.randint(cardBound[shopLevel], cardBound[shopLevel + 1])
    else:
        tmp_1=rd.randint(cardBound[5], cardBound[6])
        tmp_2 = rd.randint(cardBound[5], cardBound[6])
        tmp_3 = rd.randint(cardBound[5], cardBound[6])
    screen.blit(cardImg[tmp_1], (300, 480))
    screen.blit(cardImg[tmp_2], (510, 480))
    screen.blit(cardImg[tmp_3], (720, 480))
    pg.display.flip()
    time.sleep(1)
    d=True
    while d:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == pg.K_1:
                    playerGround.append(copy.deepcopy(cardList[tmp_1]))
                    d=False

                elif event.key == pg.K_2:
                    playerGround.append(copy.deepcopy(cardList[tmp_2]))
                    d=False

                elif event.key == pg.K_3:
                    playerGround.append(copy.deepcopy(cardList[tmp_3]))
                    d=False
    printText()

def buy(boughtNumber):  # 하수인 고용
    global gold
    buyCard = buyList[boughtNumber]
    if 3 <= gold:
        if len(playerGround)<7:
            gold -= 3
            playerGround.append(copy.deepcopy(buyCard))
            count=[]
            for i in range(len(playerGround)-1):
                if playerGround[i].number==buyCard.number:
                    count.append(i)
            if len(count) == 2:
                for i in range(2):
                    del playerGround[count[i]]
                playerGround[-1].golden=True
                discover()
            del buyList[boughtNumber]
            printText()
    else:
         print('error')

def checkBattleCry(cardNum):        #안쓰는거
    # 전투의 함성
    if cardList[cardNum].ability==1:
        print('battlecry')

def checkDeath():
    # 플레이어 전장이 비었으면 1, 상대 전장이 비었으면 2, 다 살아있으면 0 리턴, 둘 다 ㅂㅇ며
    global playerGround, opponentGround, op1Health, op2Health, op3Health, playerHealth
    dead = 1
    for i in range(len(playerGround)):
        if playerGround[i].alive == True:
            dead = 0
            break
    opponentdead = 1
    for i in range(len(opponentGround)):
        if opponentGround[i].alive == True:
            opponentdead = 0
            break
    if dead and opponentdead:
        return 1
    elif dead:
        for i in range(len(opponentGround)):
            if opponentGround[i].alive:
                playerHealth -= opponentGround[i].star
        if playerHealth<=0:
            print('Game End')
            exit(0)
        return 1
    elif opponentdead:
        for i in range(len(playerGround)):
            if playerGround[i].alive:
                if op==1:
                    op1Health -= playerGround[i].star
                    if op1Health<=0:
                        print('Op 1 Dead')
                        opAlive[0]=False
                elif op==2:
                    op2Health -= playerGround[i].star
                    if op2Health<=0:
                        print('Op 2 Dead')
                        opAlive[1]=False
                else:
                    op3Health -= playerGround[i].star
                    if op3Health<=0:
                        print('Op 3 Dead')
                        opAlive[2]=False
        return 1
    else:
        return 0

def attack(attackerNum, whoTurn):  # 공격(공격하는 유닛, 플레이어)
    global playerGround, opponentGround
    tauntArr = []  # taunted enemy list
    time.sleep(0.5)
    if whoTurn == "player":
        for i in range(len(opponentGround)):
            if opponentGround[i].ability == 4 and opponentGround[i].alive:
                tauntArr.append(i)
        if len(tauntArr) != 0:
            tmp = rd.randint(0, len(tauntArr) - 1)
            while not opponentGround[tauntArr[tmp]].alive:
                tmp = rd.randint(0, len(tauntArr)-1)
            if opponentGround[tauntArr[tmp]].ability==3 and opponentGround[tauntArr[tmp]].abilused==False:
                opponentGround[tauntArr[tmp]].abilused=True
            else:
                opponentGround[tauntArr[tmp]].fightHealth -= playerGround[attackerNum].fightAttack
                playerGround[attackerNum].fightHealth -= opponentGround[tauntArr[tmp]].fightAttack
                if opponentGround[tauntArr[tmp]].fightHealth<=0:
                    opponentGround[tauntArr[tmp]].alive=False
                if playerGround[attackerNum].fightHealth<=0:
                    playerGround[attackerNum].alive=False
        else:
            tmp = rd.randint(0, len(opponentGround) - 1)
            while not opponentGround[tmp].alive:
                tmp = rd.randint(0, len(opponentGround)-1)
            opponentGround[tmp].fightHealth -= playerGround[attackerNum].attack
            playerGround[attackerNum].fightHealth -= opponentGround[tmp].attack
            if opponentGround[tmp].fightHealth<=0:
                opponentGround[tmp].alive=False
            if playerGround[attackerNum].fightHealth<=0:
                playerGround[attackerNum].alive=False

    elif whoTurn == "opponent":
        for i in range(len(playerGround)):
            if playerGround[i].ability == 4 and playerGround[i].alive:
                tauntArr.append(i)
        if len(tauntArr) != 0:
            tmp = rd.randint(0, len(tauntArr) - 1)
            while not playerGround[tauntArr[tmp]].alive:
                tmp = rd.randint(0, len(tauntArr)-1)
            playerGround[tauntArr[tmp]].fightHealth -= opponentGround[attackerNum].attack
            opponentGround[attackerNum].fightHealth -= playerGround[tauntArr[tmp]].attack
            if playerGround[tauntArr[tmp]].fightHealth<=0:
                playerGround[tauntArr[tmp]].alive=False
            if opponentGround[attackerNum].fightHealth<=0:
                opponentGround[attackerNum].alive=False
        else:
            tmp = rd.randint(0, len(playerGround)-1)
            playerGround[tmp].fightHealth -= opponentGround[attackerNum].attack
            opponentGround[attackerNum].fightHealth -= playerGround[tmp].attack
            if playerGround[tmp].fightHealth<=0:
                playerGround[tmp].alive=False
            if opponentGround[attackerNum].fightHealth<=0:
                opponentGround[attackerNum].alive=False
    printGround()

def heroAbility(heroNumber): # 우두머리 능력
    global gold
    if gold > 1:
        discover()

def printGround():
    screen.fill(BLACK)
    text1='Player Health: '+str(playerHealth)
    timg=font30.render(text1, True, WHITE)
    screen.blit(timg,(0,550))
    if op==1:
        text1 = 'Opponent Health: ' + str(op1Health)
    elif op==2:
        text1 = 'Opponent Health: ' + str(op2Health)
    else:
        text1 = 'Opponent Health: ' + str(op3Health)
    timg = font30.render(text1, True, WHITE)
    screen.blit(timg, (300, 550))
    for i in range(len(playerGround)):
        if playerGround[i].alive:
            if playerGround[i].golden:
                screen.blit(goldencardImg[playerGround[i].number], (i*130,300))
            else:
                screen.blit(cardImg[playerGround[i].number],(i*130, 300))
            text1 = 'Health: '+str(playerGround[i].fightHealth)
            healthimg = font30.render(text1, True, WHITE)
            screen.blit(healthimg, (i*130, 430))
            text1 = 'Attack: ' + str(playerGround[i].fightAttack)
            attackimg = font30.render(text1, True, WHITE)
            screen.blit(attackimg, (i*130, 460))
    for i in range(len(opponentGround)):
        if opponentGround[i].alive:
            tmp=opponentGround[i].number
            if opponentGround[i].golden:
                screen.blit(goldencardImg[tmp], (i*130,0))
            else:
                screen.blit(cardImg[tmp], (i*130,0))
            text1 = 'Health: ' + str(opponentGround[i].fightHealth)
            healthimg = font30.render(text1, True, WHITE)
            screen.blit(healthimg, (i * 130, 130))
            text1 = 'Attack: ' + str(opponentGround[i].fightAttack)
            attackimg = font30.render(text1, True, WHITE)
            screen.blit(attackimg, (i * 130, 160))
    pg.display.flip()


def fightTurn():  # 전투 단계
    screen.fill(BLACK)
    global playerGround, opponentGround, p2Ground, p3Ground, p4Ground, op1Health, op2Health, op3Health, playerHealth,op
    first = 0  # first=1이면 내가 선공, 0이면 상대가 선공
    tmp = rd.randint(0,2)  # 어떤 상대와 싸우는지 정함
    if opAlive[0]==False and opAlive[1]==False and opAlive[2]==False:
        print('Player win')
    while not opAlive[tmp]:
        tmp=rd.randint(0,2)
    op=tmp
    if tmp == 0:
        opponentGround = copy.deepcopy(p2Ground)
    elif tmp == 1:
        opponentGround = copy.deepcopy(p3Ground)
    elif tmp == 2:
        opponentGround = copy.deepcopy(p4Ground)
    for i in range(len(playerGround)):
        playerGround[i].abilused=False
        playerGround[i].alive=True
        if playerGround[i].golden:
            playerGround[i].fightHealth = playerGround[i].goldenHealth
            playerGround[i].fightAttack = playerGround[i].goldenAttack
        else:
            playerGround[i].fightHealth = playerGround[i].health
            playerGround[i].fightAttack = playerGround[i].attack

    for i in range(len(opponentGround)):
        opponentGround[i].abilused=False
        opponentGround[i].alive = True
        if opponentGround[i].golden:
            opponentGround[i].fightHealth = opponentGround[i].goldenHealth
            opponentGround[i].fightAttack = opponentGround[i].goldenAttack
        else:
            opponentGround[i].fightHealth = opponentGround[i].health
            opponentGround[i].fightAttack = opponentGround[i].attack
    if checkDeath(): return
    if len(opponentGround) > len(playerGround):
        first = "player"
    elif len(opponentGround) == len(playerGround):
        tmp = rd.randint(0, 2)
        if tmp == 0:
            first = "player"
        elif tmp == 1:
            first = "opponent"
    else:
        first = "opponent"
    printGround()
    x=0
    y=0
    # 여기까지 선공 정하기 구현
    if first == "player":
        while 1:
            if len(playerGround)>x:
                while playerGround[x].alive!=True:
                    x += 1
                    if x > len(playerGround) - 1:
                        x=0
                attack(x,"player")
            if checkDeath(): break
            if len(opponentGround)>y:
                while opponentGround[y].alive!=True:
                    y+=1
                    if y > len(opponentGround) - 1:
                        y=0
                attack(y,"opponent")
            if checkDeath(): break
    else:
        while 1:
            if len(opponentGround)>y:
                while opponentGround[y].alive == False:
                    y+=1
                    if y > len(opponentGround)-1:
                        y=0
                attack(y, "opponent")
            if checkDeath(): break
            if len(playerGround)>x:
                while playerGround[x].alive == False:
                    x+=1
                    if x > len(playerGround) - 1:
                        x=0
                attack(x, "player")
            if checkDeath(): break
    printGround()
    time.sleep(1)

def buyTurn():  # 고용 단계
    global gold, max_gold, upgrade_cost, max_gold, upgraded, freezed, shopCard_number, sec, Round, opponentGround, p2Ground, cardList, p2tGround, p3Ground, p3tGround, p4Ground, p4tGround
    Round += 1
    if max_gold < 10:
        max_gold += 1
    gold = max_gold
    if not freezed:
        reset()
    sec = 1
    if not upgraded:
        if upgrade_cost > 1:
            upgrade_cost -= 1
    upgraded = False
    printText()
    p2Ground = p2tGround[Round - 1]
    for i in range(len(p2Ground)):
        if p2Ground[i] < 100:
            p2Ground[i] = copy.deepcopy(cardList[p2Ground[i]])
        else:
            p2Ground[i] = copy.deepcopy(cardList[p2Ground[i] // 100])
            p2Ground[i].golden = True
    p3Ground = p3tGround[Round - 1]
    for i in range(len(p3Ground)):
        if p3Ground[i] < 100:
            p3Ground[i] = copy.deepcopy(cardList[p3Ground[i]])
        else:
            p3Ground[i] = copy.deepcopy(cardList[p3Ground[i] // 100])
            p3Ground[i].golden = True
    p4Ground = p4tGround[Round - 1]
    for i in range(len(p4Ground)):
        if p4Ground[i] < 100:
            p4Ground[i] = copy.deepcopy(cardList[p4Ground[i]])
        else:
            p4Ground[i] = copy.deepcopy(cardList[p4Ground[i] // 100])
            p4Ground[i].golden = True
    d=False
    while not d:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                col = event.pos[0]
                row = event.pos[1]
                if col >= 150 and col <= 200 and row >= 0 and row <= 50: # reroll
                    if gold>0:
                        gold-=1
                        reset()
                elif col >= 210 and col <= 260 and row >= 0 and row <= 50: # upgrade
                    upgrade()
                elif col >= 270 and col <= 320 and row >= 0 and row <= 50: # freeze
                    freeze()
            elif event.type == KEYDOWN:
                if event.key == pg.K_1:
                    if len(buyList) > 0:
                        buy(0)
                elif event.key == pg.K_2:
                    if len(buyList) > 1:
                        buy(1)
                elif event.key == pg.K_3:
                    if len(buyList) > 2:
                        buy(2)
                elif event.key == pg.K_4:
                    if len(buyList) > 3:
                        buy(3)
                elif event.key == pg.K_5:
                    if len(buyList) > 4:
                        buy(4)
                elif event.key == pg.K_6:
                    if len(buyList) > 5:
                        buy(5)
                elif event.key == pg.K_a:
                    heroAbility(0)
                elif event.key == pg.K_n:
                    d=True

def init():  # init
    global upgrade_cost, shopLevel_cost, freezed, upgraded, gold, max_gold, upgraded
    cardName_file = open('cardName.txt')
    cardStats_file = open('cardStats.txt')
    goldencardStats_file = open('goldencardStats.txt')
    tmpList=[]
    opAlive = [True] * 3
    upgraded=False
    t=rd.randint(1,9)
    while t in tmpList:
        t = rd.randint(1, 9)
    tmpList.append(t)
    p2Ground_file = open('op/op'+str(t)+'.txt', 'r')
    t = rd.randint(1, 9)
    while t in tmpList:
        t = rd.randint(1, 9)
    tmpList.append(t)
    p3Ground_file = open('op/op' + str(t) + '.txt','r')
    t = rd.randint(1, 9)
    while t in tmpList:
        t = rd.randint(1, 9)
    tmpList.append(t)
    p4Ground_file = open('op/op' + str(t) + '.txt','r')
    i = 0
    upgrade_cost = shopLevel_cost[0]
    freezed = False
    upgraded = True
    max_gold = 2
    gold = max_gold

    # 카드 이름 입력
    while True:
        tmp = cardName_file.readline().strip()
        tmp2 = list(map(int, cardStats_file.readline().strip().split()))
        tmp3 =list(map(int, goldencardStats_file.readline().strip().split()))
        o1=list(map(int, p2Ground_file.readline().strip().split()))
        o2=list(map(int, p3Ground_file.readline().strip().split()))
        o3=list(map(int, p4Ground_file.readline().strip().split()))
        if not tmp: break
        p2tGround.append(o1)
        p3tGround.append(o2)
        p4tGround.append(o3)

        cardList.append(Card())
        cardList[i].name = tmp
        cardList[i].number=i
        cardImg.append(pg.image.load('image/' + tmp + '.png'))
        cardImg[i] = pg.transform.scale(cardImg[i], (200, 240))
        goldencardImg.append(pg.image.load('goldenimage/' + tmp + '.png'))
        goldencardImg[i] = pg.transform.scale(goldencardImg[i], (200, 240))
            
        cardList[i].star = tmp2[0]
        cardList[i].attack = tmp2[1]
        cardList[i].fightAttack = tmp2[1]
        cardList[i].health = tmp2[2]
        cardList[i].fightHealth = tmp2[2]
        cardList[i].ability = tmp2[3]
        cardList[i].goldenAttack = tmp3[0]
        cardList[i].goldenHealth = tmp3[1]
        cardList[i].goldenAbility = tmp3[2]
        cardCount.append(0)
        i += 1
    cardName_file.close()
    cardStats_file.close()
    goldencardStats_file.close()
    p2Ground_file.close()
    p3Ground_file.close()
    p4Ground_file.close()

init()
done = False
while not done:
    buyTurn()
    fightTurn()