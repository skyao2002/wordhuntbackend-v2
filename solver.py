import os

class TrieNode(object):
    def __init__(self):
        self.children = {}
        # Is it the last character of the word.`
        self.word_finished = False

def loadDict():
    print("loading needed values...")
    dictionaryTrie = TrieNode()

    print("loading dictionary")
    dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colins-scrabble-dictionary.txt')
    with open(dict_path, "r") as infile:
        for line in infile:
            word = line.rstrip()
            curr = dictionaryTrie
            for i, char in enumerate(word):
                char = char.upper()
                if not char in curr.children:
                    curr.children[char] = TrieNode()
                curr = curr.children[char]
                if i == len(word) - 1:
                    curr.word_finished = True

    return dictionaryTrie

directions = [
    (1,0),
    (0,1),
    (-1,0),
    (0,-1),
    (1,-1),
    (-1,-1),
    (-1,1),
    (1,1)
]

class solveWordHunt():
    def __init__(self, letters, size, trie):
        self.board = []
        self.size = size
        self.trie = trie
        temp = []
        
        for i, v in enumerate(letters.upper()):
            temp.append(v)
            if((i+1)%size == 0):
                self.board.append(temp)
                temp = []

        self.visited = [
            [False for i in range(size)] for j in range(size)
        ]

        self.ans = []

        for i in range(size):
            for j in range(size):
                self.recurse(i, j, "", "", self.visited, self.trie)
        
        def sortAns(e):
            return len(e[0])
        
        self.ans.sort(key=sortAns, reverse=True)

        temp = []

        self.ansNoDuplicates = []

        for row in self.ans:
            row[1] = [int(i) for i in row[1].split()]
            if row[0] not in temp:
                temp.append(row[0])
                self.ansNoDuplicates.append(row)


    def recurse(self, row, col, word, path, visited, currNode):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return
        if visited[row][col]:
            return
        
        letter = self.board[row][col]
        
        if not letter in currNode.children:
            return
        word += letter
        visited[row][col] = True

        if len(word) > 3 and currNode.children[letter].word_finished:
            self.ans.append([word, path+" "+str(row*self.size+col)])
        
        for dir in directions:
            x = dir[0]
            y = dir[1]
            if row+x >=0 and row+x < self.size and col+y >= 0 and col+y < self.size:
                if not visited[row+x][col+y]:
                    self.recurse(row+x, col+y, word, path+" "+str(row*self.size+col), visited, currNode.children[letter])

        visited[row][col] = False


if __name__=="__main__":
    trie = loadDict()

    solved = solveWordHunt("qwertyuiopasdfgh", 4, trie)

    print(solved.ans)
    print(solved.ansNoDuplicates)