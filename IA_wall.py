from tkinter import *
import numpy as np
from math import *
from random import *
import time
import random
import keyboard
import numpy as np

tk = Tk()
cnv=Canvas(tk, width=800, height=800, bg="white")
cnv.pack(padx=0, pady=0)

#-------------------------------------------------------------------------------------------------------------------------------------------
#classe joueurs

class point:
    def __init__(self, name):
        self.name = name
        self.x = 400
        self.y = 750
        self.alive = True
        self.memory = []
        self.draw = 0
        self.alpha = -np.pi/2
        self.alphapre = self.alpha
        self.fit = 0

#-------------------------------------------------------------------------------------------------------------------------------------------
#variables initiales

player = []
memorymin = []

cnv.create_oval(390, 740, 410, 760, fill = "pink")
cnv.create_rectangle(375, 25, 425, 75, fill = "pink")
cnv.create_rectangle(200, 375, 800, 425, fill = "blue")
cnv.create_rectangle(0, 175, 600, 225, fill = "blue")

tempo = 0

for i in range(0, 250):
    player.append(point(i))

nb_vie = 250
gen = 0
begin = time.time()
timer = 0
generation = 0
fitmin = 0
fini = False
deathx = [0]
deathy = [0]

#-------------------------------------------------------------------------------------------------------------------------------------------
#distance

def distance(x, y, xp, yp):
    return sqrt((x-xp)**2 +(y-yp)**2)

#-------------------------------------------------------------------------------------------------------------------------------------------
#mouvements et logique

def move():
    global tempo, timer, memorymin, gen, fini, nb_vie
    for i in range(0, len(player)):
        if ((player[i].x+2 >= 200 and player[i].y+2 >= 375 and player[i].y-2 <= 425) or player[i].x+2 >= 800 or player[i].x-2 <= 0 or player[i].y+2 >= 800 or player[i].y-2 <= 0):
            deathx.append(player[i].x)
            deathy.append(player[i].y)
            cnv.create_oval(player[i].x-20, player[i].y-20, player[i].x+20, player[i].y+20, fill = "lime")
            player[i].alive = False
            player[i].x = 400
            player[i].y = 750
            nb_vie -= 1
        
        elif(player[i].x <= 600 and player[i].y <= 225 and player[i].y >= 175):
            deathx.append(player[i].x)
            deathy.append(player[i].y)
            cnv.create_oval(player[i].x-20, player[i].y-20, player[i].x+20, player[i].y+20, fill = "lime")
            player[i].alive = False
            player[i].x = 400
            player[i].y = 750
            nb_vie -= 1

        if(player[i].alive):
            if(fini):
                if(gen >= 1) and (timer <= len(memorymin)):
                    player[i].alpha = memorymin[timer-1]+gauss(0, np.pi/16)
                else:
                    player[i].alpha = random.random()*np.pi/2-np.pi/4+player[i].alphapre
            else:
                if(gen >= 1) and (timer <= len(memorymin)-15):
                    player[i].alpha = memorymin[timer-1]+gauss(0, np.pi/8)
                else:
                    for j in range(len(deathx)):
                        if(distance(player[i].x, player[i].y, deathx[j], deathy[j]) <= 20):
                            print("turn")
                            player[i].alphapre = -player[i].alphapre
                            # player[i].x = 400
                            # player[i].y = 750
                        else:
                            player[i].alpha = random.random()*np.pi/2-np.pi/4+player[i].alphapre

            player[i].x += 5*np.cos(player[i].alpha)
            player[i].y += 5*np.sin(player[i].alpha)
            player[i].alphapre = player[i].alpha
            player[i].memory.append(player[i].alpha)
        else:
            pass

#-------------------------------------------------------------------------------------------------------------------------------------------
#apparition

def draw():
    global generation
    for i in range(0, len(player)):
        cnv.delete(player[i].draw)
        player[i].draw = cnv.create_oval(player[i].x-2, player[i].y-2, player[i].x+2, player[i].y+2, fill = "red")
    cnv.delete(generation)
    generation = cnv.create_text(400, 25, font=('Arial', 30, 'bold italic'), text = "gen : "+str(gen), fill = "black")

#-------------------------------------------------------------------------------------------------------------------------------------------
#mémoire et logique

def brain():
    global gen, timer, memorymin, fitmin, fini

    move()

    for i in range(0, len(player)):
        if(player[i].x+2>=375 and player[i].x-2<=425 and player[i].y+2>=25 and player[i].y-2<=75):
            if(len(player[i].memory) <= len(memorymin)):
                memorymin = player[i].memory
                fini = True
                print("fini")
                print(len(memorymin))
            new_gen()
        player[i].fit = 1/((player[i].x-400)*(player[i].x-400)+(player[i].y-50)*(player[i].y-50))
        if(player[i].fit >= fitmin):
            fitmin = player[i].fit
            memorymin = player[i].memory

    timer+=1

#-------------------------------------------------------------------------------------------------------------------------------------------
#nouvelle génération

def new_gen():
    global gen, begin, timer, nb_vie
    gen+=1
    timer = 0
    nb_vie = 250
    begin = time.time()
    for i in range(0, len(player)):
        player[i].x = 400
        player[i].y = 750
        player[i].alpha = -np.pi/2
        player[i].alphapre = -np.pi/2
        player[i].memory = []
        player[i].alive = True
        player[i].fit = 0

#-------------------------------------------------------------------------------------------------------------------------------------------
#main

def main():
    global gen, begin, timer, nb_vie
    brain()
    draw()
    if(nb_vie == 0):
        new_gen()
    tk.after(25, main)

#-------------------------------------------------------------------------------------------------------------------------------------------

main()

tk.mainloop()