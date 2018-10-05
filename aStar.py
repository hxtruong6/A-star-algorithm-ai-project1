#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 14:15:09 2018

@author: hxtruong
"""

# references: https://en.wikipedia.org/wiki/A*_search_algorithm

# from . import priorityqueue
import math
import heapq
import sys

NEIGHBORS = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

class PriorityEntry:

    def __init__(self, priority, data):
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def isEmpty(self):
        return len(self.elements) == 0
    
    def push(self, priority, data):
        element = PriorityEntry(priority, data)
        heapq.heappush(self.elements, element)
    
    def pop(self):
        element = heapq.heappop(self.elements)
        return (element.priority, element.data)

class AStarGrid:
    def __init__(self, rows, columns, grid):
        self.rows = rows
        self.columns = columns
        self.grid = grid
        
    def heuristic(self, start, end):
        (x1,y1) = start
        (x2,y2) = end
        return math.sqrt(math.pow(abs(x1-x2),2)+ math.pow(abs(y1-y2),2))
    
    def cost_distance(self, start, end):
        # set value is 1
        return 1
    
    def isValid(self, point):
        (x,y) = point
        return x>=0 and y>=0 and x< self.rows and y< self.columns
    
    def isBlocked(self, point):
        (x,y) = point
        return self.grid[x][y] != 0
    
    def getNeighbors(self, point):
        (x,y) = point
        neighbors = []
        for (u,v) in NEIGHBORS:
            if self.isValid((x+u, y+v)) and not self.isBlocked((x+u,y+v)):
                    neighbors.append((x+u,y+v))
        
        return neighbors
    
def reconstructPath(cameFrom, current):
    aStarPath = [current]
    while current in cameFrom:
        prevPoint = cameFrom[current]
        aStarPath.append(prevPoint)
        current = prevPoint
    
    return aStarPath[::-1]

def aStartFunc(start, end, grid):
    '''
         F(x) = G(x) + H(x)
         G(x) = cost between distance of two point
         H(x) = heuristic between distance of two point
    '''    
    G = {}  # set use store the value of G score
    F = {}  # set use store the value of F score.    
    G[start] = 0
    F[start] = grid.heuristic(start, end)
    
    closedSet = set()
    openSet = set([start])
    openQueue = PriorityQueue() # argument: priority, (x,y)
    openQueue.push(F[start], start)
    cameFrom = {}
    
    while not openQueue.isEmpty():
        # get the cell of grid in openSet has the lowest F score
        fScoreCurr, current = openQueue.pop()
        openSet.remove(current)
        closedSet.add(current)
        if current == end:
            return reconstructPath(cameFrom, current)
            
        neighbors = grid.getNeighbors(current)
        for neighbor in neighbors:
            if (neighbor not in closedSet):
                tentativeG = G[current] + grid.cost_distance(current, neighbor)
                # TODO: get neighbor not in openSet????
                if (neighbor in G and tentativeG < G[neighbor]) or (neighbor not in openSet):
                    cameFrom[neighbor] = current
                    G[neighbor] = tentativeG
                    F[neighbor] = G[neighbor] + grid.heuristic(neighbor, end)
                    openSet.add(neighbor)
                    openQueue.push(F[neighbor], neighbor)
    
    #raise RuntimeError(f"A* algorithm can not find any way from {start} to {end}") 
    return [] # no way
    
def main():
    # read arguments from command
    try: 
        sys.argv[1]
        sys.argv[2]
    except:
        inputFileName = "input.txt"
        outputFileName = "output.txt"
    else:
        inputFileName = sys.argv[1]
        outputFileName = sys.argv[2]
    
    #### read from file
    fi = open(inputFileName, "r")
    
    contents = fi.readlines()
    n = int(contents[0])
    x1,y1 = [int(val) for val in contents[1].split()]
    start = (x1, y1)
    x2,y2 = [int(val) for val in contents[2].split()]
    end = (x2, y2)
    
    aGrid = []
    for i in range(n):
        aGrid.append([int(val) for val in contents[3+i].split()])
    
    aStarGrid = AStarGrid(n,n, aGrid)
    
    fi.close()
    
    #### write to file
    fo = open(outputFileName, "w")
    
    aStarPath = aStartFunc(start, end, aStarGrid)
    if len(aStarPath):
        fo.write(f"{len(aStarPath)}\n")
        for (x,y) in aStarPath:
            fo.write(f"({x},{y}) ")
        fo.write('\n')
        
        # traverse all cell of grid to write to file
        for i in range(n):
            for j in range(n):
                point = (i,j)
                if point == start:
                    fo.write("S ")
                elif point == end:
                    fo.write("G ")
                elif point in aStarPath:
                    fo.write("x ")
                elif aGrid[i][j] == 1: #cell in grid is obstacle
                    fo.write("o ")
                else:
                    fo.write("- ")
            fo.write('\n')
    else:
        fo.write("-1")
    
    fo.close()
        
if (__name__== "__main__"):
    main()