import sys
import math
import queue
import os

class Node:
    def __init__(self):
        self.leaf = None
        self.next = [None] * 26
data = []
Trie = [Node()]
final = [set() for _ in range(16)]
graph = [[] for i in range(1, 26)]
verticeHash = [1, 2, 3, 5, 7, 11, 
               13, 17, 19, 23, 29, 
               31, 37, 41, 43, 47, 
               53, 59, 61, 67, 71, 
               73, 79, 83, 89, 97]
board = [[' ' for j in range(1, 6)] for i in range(1, 6)]

def FileIO():
    sys.stdin  = open('input.txt', 'r')  
    sys.stdout = open('output.txt', 'w') 

def addEdge(r1, c1, r2, c2):
    u = (r1-1) * n + c1
    v = (r2-1) * n + c2
    graph[u].append(v)
    graph[v].append(u)
    
def addWord(id):
    word = data[id]
    final[len(word)].add(word)
    
def addString(st, id):
    v = 0
    for ch in st:
        c = ord(ch) - 97
        #print(v, end = ' ')
        if (Trie[v].next[c] == None):
            Trie[v].next[c] = len(Trie)
            Trie.append(Node())
        v = Trie[v].next[c]
    Trie[v].leaf = id
    
#Basic BFS to connect adjacenced letters -> words
#Alongside traversing on the dictionary's Trie to check if:
    #There is any child of the node u 
        #(could contain valid words with the prefix constructed from the vertices traversing until node u)
    #Or if there isn't then skip the turn 
        #(no valid words can be created with the prefix constructed from the vertices traversing until node u)
#Acceptable performance no longer limited at 10-letter words
def TrieSearch(s):
    myQueue = queue.Queue()
    c = ord(inString[s]) - 97
    myQueue.put((s, verticeHash[s], 1, Trie[0].next[c]))
    while myQueue.qsize() > 0:
        item_u = myQueue.get()
        #print(item_u)
        u, hash_til_u, len_til_u, vert_u = item_u
        for v in graph[u]:
            if hash_til_u % verticeHash[v] == 0: continue
            c = ord(inString[v]) - 97
            if Trie[vert_u].next[c] == None: 
                continue
            else: 
                vert_v = Trie[vert_u].next[c]
            if Trie[vert_v].leaf != None: 
                addWord(Trie[vert_v].leaf)
            if len_til_u + 1 < 15: 
                myQueue.put((v, hash_til_u * verticeHash[v], len_til_u + 1, vert_v))
                #print(myQueue.qsize())
    
def main():
    for i in range(len(data)):
        data[i] = data[i][:-1]
        addString(data[i], i)
        
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
            
    for i in range(1, n*n + 1): TrieSearch(i)
    for wordsize in range(4, 16):
        if (len(final[wordsize]) > 0): 
            final[wordsize] = sorted(final[wordsize])
            print(str(wordsize) + '-letter words:')
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

