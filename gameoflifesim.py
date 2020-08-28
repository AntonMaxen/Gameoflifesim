import sys
import pygame
import random
import time
import math
import json
pygame.init()

size = width, height = 600, 600
rows = 30
cols = 30
cellWidth = width / cols
cellHeight = height / rows
screen = pygame.display.set_mode(size)

pink = (254, 169, 129)
purple = (92, 17, 47)

def setup(cols, rows):
    newCells = []
    for y in range(rows):
        for x in range(cols):
            if random.randint(0, 10) > 7:
                newCells.append(1)
            else:
                newCells.append(0)
    return newCells

def printCells(cells, cols, rows):
    for y in range(rows):
        row = ""
        for x in range(cols):
            cell = cells[x + (y * cols)]
            symbol = "\u25A0" if cell == 1 else " "
            row += " " + symbol + " "
        print(row)

def createSquares(cells, cols, rows, cellWidth, cellHeight):
    #print("creating squares")
    newSquares = []
    for y in range(rows):
        for x in range(cols):
            currCell = cells[x + (y * cols)]
            if currCell == 1:
                relativeX = x * cellWidth
                relativeY = y * cellHeight
                newSquares.append(pygame.Rect(relativeX, relativeY, cellWidth, cellHeight))

    return newSquares

def drawSquares(squares, screen, color = (19, 62, 89)):
    #Draw them squares.
    for square in squares:
        pygame.draw.circle(screen, color, square.center, math.floor(square.width / 4))
        #print(square)

def updateCells(cells, cols, rows):
    #print("update")
    newCells = []
    for yCoord in range(rows):
        for xCoord in range(cols):
            counter = 0
            for yCheck in range(-1, 2):
                for xCheck in range(-1, 2):
                    leftBound = xCoord + xCheck < 0
                    rightBound = xCoord + xCheck >= cols
                    topBound = yCoord + yCheck < 0
                    bottomBound = yCoord + yCheck >= rows

                    if (leftBound or rightBound) or (topBound or bottomBound) or (yCheck == 0 and xCheck == 0):
                        pass
                    elif cells[(xCoord + xCheck) + ((yCoord + yCheck) * cols)] == 1:
                        counter += 1

            isAlive = cells[xCoord + (yCoord * cols)] == 1
            if isAlive:
                if counter < 2:
                    newCells.append(0)
                elif (counter >= 2) and (counter <= 3):
                    newCells.append(1)
                elif counter > 3:
                    newCells.append(0)
            else:
                if counter == 3:
                    newCells.append(1)
                else:
                    newCells.append(0)
    #print(newCells)
    return newCells

def checkEquals(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False

    return True


def saveJson(fileName, data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

cells = setup(cols, rows)
screen.fill(pink)
squares = createSquares(cells, cols, rows, cellWidth, cellHeight)
drawSquares(squares, screen, purple)
pygame.display.update()
time.sleep(1)

rotations = 0
longestEvolution = 0
data = {'generation': []}

evenCells = []
oddCells = []
startCells = cells.copy()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(startCells)
            saveJson("data.json", data)

            sys.exit()

    rotations += 1
    cells = updateCells(cells, cols, rows)
    newCells = cells.copy()

    if rotations % 2 == 0:
        if checkEquals(evenCells, newCells):
            if rotations > longestEvolution:
                longestEvolution = rotations
                data['generation'].append({
                    'startarray': startCells.copy(),
                    'generations': longestEvolution
                })
                saveJson("data.json", data)
                print(longestEvolution)
                print(len(data['generation']))

            rotations = 0
            cells = setup(cols, rows)
            startCells = cells.copy()

        evenCells = cells.copy()
    elif rotations % 3 == 0:
        if checkEquals(oddCells, newCells):
            if rotations > longestEvolution:
                longestEvolution = rotations
                data['generation'].append({
                    'startarray': startCells.copy(),
                    'generations': longestEvolution
                })
                saveJson("data.json", data)
                print(longestEvolution)
                print(len(data['generation']))

            rotations = 0
            cells = setup(cols, rows)
            startCells = cells.copy()
        oddCells = cells.copy()

    screen.fill(pink)
    squares = createSquares(cells, cols, rows, cellWidth, cellHeight)
    drawSquares(squares, screen, purple)

    pygame.display.update()
    time.sleep(0.5)