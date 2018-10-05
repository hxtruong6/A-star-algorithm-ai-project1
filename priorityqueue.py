#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 15:57:27 2018

@author: hxtruong
"""


import heapq

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
    
    
    
if (__name__ =='__main__'):
    qtest = PriorityQueue();
    qtest.push(3,(3,4));
    qtest.push(32,5);
    qtest.push(1, 40);
    qtest.push(6,3);
    qtest.push(1,2);
    
    a, b = qtest.pop()
    
    #ele = qtest.pop()
    
