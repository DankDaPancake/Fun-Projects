import sys
import math
import queue
import os

cut = slice(0, -1)
words_bylen = {}
data = []
final = [set() for _ in range(16)]
graph = [[] for i in range(1, 26)]
board = [[' ' for j in range(1, 6)] for i in range(1, 6)]

def FileIO():
    sys.stdin  = open('input.txt', 'r')  
    sys.stdout = open('output.txt', 'w') 

def addEdge(r1, c1, r2, c2):
    u = (r1-1) * n + c1
    v = (r2-1) * n + c2
    graph[u].append(v)
    graph[v].append(u)

def addWord(array_v):
    ansWord = ""
    L = len(array_v)
    for i in array_v: 
        ansWord += inString[i]
    #print(ansWord, L) 
    if ansWord in words_bylen[L]: final[L].add(ansWord)

#Basic BFS to connect adjacenced letters -> words
#Acceptable performance if the lengths of words are at most 10
def bfs(s):
    myQueue = queue.Queue()
    myQueue.put([s])
    while myQueue.qsize() > 0:
        array_u = myQueue.get()
        u = array_u[-1]
        #print(array_u)
        for v in graph[u]:
            if v in array_u: continue
            array_v = array_u.copy()
            array_v.append(v)
            #print(array_v)
            if 3 < len(array_v) and len(array_v) < 15: 
                addWord(array_v)
            if len(array_v) < 10: 
                myQueue.put(array_v)
                #print(myQueue.qsize())
    
def main():
    for i in range(16): words_bylen[i]={}
    for i in range(len(data)): 
        word = data[i][cut]
        ws = len(word)
        words_bylen[ws][word] = i
        
    """for i in range(16):
        for item in words_bylen[i]: print(item)"""
    
    global inString
    inString = '#' + input()
    inString = inString.replace('-', '')
    global n
    n = math.floor(math.sqrt(len(inString)))
    #print(n)
    k = 1
    for i in range(1, n+1): 
        for j in range(1, n+1):
            board[i][j] = inString[k]
            if inString[k] == '.': continue
            if i>1 and board[i-1][j] != '.': addEdge(i-1, j, i, j)
            if j>1 and board[i][j-1] != '.': addEdge(i, j-1, i, j)
            if i>1 and j>1 and board[i-1][j-1] != '.': addEdge(i-1, j-1, i, j)
            if i>1 and j<n and board[i-1][j+1] != '.': addEdge(i-1, j+1, i, j)
            k+=1
        
    """for i in range(1, n*n+1):
        print(i, end = " - ")
        for v in graph[i]: print(v, end = " ")
        print()"""
        
    for i in range(1, n*n+1): bfs(i)
    for wordsize in range(4, 16):
        if (len(final[wordsize]) > 0): 
            print('Words of size', wordsize,':')
            counter = 0
            for item in final[wordsize]:
                if counter>0 and counter % (10-wordsize) == 0: print()
                print(item, end = " ")
                counter+=1
            print() 
            print()
     
#https://github.com/minoli-g/squaredle-solver/blob/master/words3.js
#Thanks to minoli-g for the modified dictionary
with open(os.path.join(os.path.dirname(__file__), 'dictionary.txt'), 'r') as f:
    data = f.readlines()
    
FileIO() 
main()

