import numpy as np
from collections import defaultdict
import time
import random as rd
import sys
import os

card_amount = [7, 8, 12, 14, 11, 11]
shopLevel_cost = [5, 7, 8, 9, 11]
n=1
tree_num=1
sys.setrecursionlimit(10**6)

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Failed to create the directory.")

class MonteCarloTreeSearchNode():
    def __init__(self, state, num, act, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = []
        self.number = num
        self.action=act
        return

    def untried_actions(self):  # 안한 행동
        if self.state[0] >= 3 and self.state[5][0] + self.state[6][0] < 7:
            for i in range(len(self.state[4])):
                self._untried_actions.append("1 "+str(self.state[4][i]))

        if self.state[0] >= self.state[3] and self.state[1]<6:
            self._untried_actions.append("2")

        if self.state[0] >= 1:
            self._untried_actions.append("3")

        self._untried_actions.append("5")
        rd.shuffle(self._untried_actions)

    def expand(self):  # generate next node by action
        global n, tree_num
        self.untried_actions()
        action = self._untried_actions.pop()
        print(self._untried_actions, action)
        next_state = self.move(action)
        print(next_state)

        n+=1
        print(n)
        child_node = MonteCarloTreeSearchNode(state=next_state, num=n, act=action, parent=self)
        deltahp=0
        self.children.append(child_node)
        file=open('tree'+str(tree_num)+'/node_'+str(n)+'.txt', 'w')
        '''
        1/ state(children)
        2/ parent number
        3/ number of visits
        4/ result : plushp minushp
        '''
        for i in range(7):
            file.write(str(child_node.state[i])+' ')
        file.write("\n")
        file.write(str(child_node.parent.number))
        file.write("\n")
        file.write(str(child_node._number_of_visits))
        file.write("\n")
        file.write(str(child_node._results[1])+' '+str(child_node._results[-1])+"\n")
        file.write(str(child_node.action))
        file.write("\n")
        file.close()
        if action=="5":
            while True:
                try:
                    f2 = open('deltahp.txt', 'r')
                    deltahp = int(f2.readline().strip())
                    f2.close()
                    if deltahp>0:
                        self.backpropagate(result=1, deltahp=deltahp)
                    else:
                        self.backpropagate(result=-1, deltahp=-deltahp)
                    print('deltahp:', deltahp)
                    break
                except:
                    time.sleep(0.01)
            f2 = open('deltahp.txt', 'w')
            f2.close()
            if next_state[0] == -1:
                print('next tree')
                tree_num += 1
                main()
                return
        child_node.expand()

    def backpropagate(self, result, deltahp):       # result는 -1 아니면 1
        self._number_of_visits += 1
        self._results[result] += deltahp
        file = open('tree'+str(tree_num)+'/node_' + str(self.number) + '.txt', 'w')

        for i in range(7):
            file.write(str(self.state[i]) + ' ')
        file.write("\n")
        if self.number==1:
            file.write(str(0)+'\n')
        else:
            file.write(str(self.parent.number))
            file.write("\n")
        file.write(str(self._number_of_visits))
        file.write("\n")
        file.write(str(self._results[1])+ ' ' +str(self._results[-1]) + "\n")
        file.write(str(self.action))
        file.write("\n")
        file.close()
        if self.parent!=0:  # 부모 노드(최종노드)에 도달할때까지
            self.parent.backpropagate(result, deltahp)

    def move(self, action):
        f=open('gameaction.txt', 'w')
        f.write(action)
        f.close()
        state_m=[]
        time.sleep(0.01)
        while True:
            try:
                f1 = open('gamedata.txt', 'r')
                state_m.append(int(f1.readline().strip()))  # gold
                state_m.append(int(f1.readline().strip()))  # level
                state_m.append(int(f1.readline().strip()))  # player health
                state_m.append(int(f1.readline().strip()))  # levelup gold
                a = list(map(int, f1.readline().strip().split()))
                state_m.append(a)  # 상점 카드
                a = list(map(int, f1.readline().strip().split()))
                t = [0] * 63
                t[0] = len(a)
                for i in range(0, len(a)):
                    t[a[i]+1] += 1
                state_m.append(t)  # 전장 일반 카드(원핫인코딩)
                a = list(map(int, f1.readline().strip().split()))
                t = [0] * 63
                t[0] = len(a)
                for i in range(0, len(a)):
                    t[a[i]+1] += 1
                state_m.append(t)  # 전장 골드 카드(원핫인코딩)
                f1.close()
                break
            except:
                time.sleep(0.01)
        f1 = open('gamedata.txt', 'w')
        f1.close()
        return state_m

def main():
    global tree_num, n
    createDirectory('tree'+str(tree_num))
    f1 = open('gamedata.txt', 'r')
    state_t = []
    while True:
        try:
            state_t.append(int(f1.readline().strip()))  # gold
            state_t.append(int(f1.readline().strip()))  # level
            state_t.append(int(f1.readline().strip()))  # player health
            state_t.append(int(f1.readline().strip()))  # levelup gold
            a = list(map(int, f1.readline().strip().split()))
            state_t.append(a)  # 상점 카드
            a = list(map(int, f1.readline().strip().split()))
            t = [0] * 63
            t[0] = len(a)
            for i in range(0, len(a)):
                t[a[i] + 1] += 1
            state_t.append(t)  # 전장 일반 카드(원핫인코딩)
            a = list(map(int, f1.readline().strip().split()))
            t = [0] * 63
            t[0] = len(a)
            for i in range(0, len(a)):
                t[a[i] + 1] += 1
            state_t.append(t)  # 전장 골드 카드(원핫인코딩)
            f1.close()
            break
        except:
            time.sleep(0.01)
    f1 = open('gamedata.txt', 'w')
    f1.close()
    root = MonteCarloTreeSearchNode(state=state_t, num=1, act=0, parent=0)
    n=1
    file = open('tree' + str(tree_num) + '/node_' + str(root.number) + '.txt', 'w')

    for i in range(7):
        file.write(str(root.state[i]) + ' ')
    file.write("\n")
    file.write(str(0))
    file.write("\n")
    file.write(str(root._number_of_visits))
    file.write("\n")
    file.write(str(root._results[1]) + ' ' + str(root._results[-1]) + "\n")
    file.write(str(root.action))
    file.close()
    root.expand()

if __name__ == '__main__':
    main()