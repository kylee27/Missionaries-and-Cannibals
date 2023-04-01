from itertools import count

expanded = []

def drawState(state):
    print(state[0] * "M", state[1] * "C", (6-state[0]-state[1]) * " ", "|", "B    " if state[2] else "    B", "|", (3-state[0]) * "M", (3-state[1]) * "C")
    print()

def genChild(state):
    children = []
    candidates = []

    def changeState(index, plus):
        child = state[:]
        for i in index: child[i] += plus
        child[2] = int(plus > 0)
        for i in child:
            if i < 0 or i > 3: return None
        if (child[0] > 0 and child[0] < child[1]) or ((3-child[0]) > 0 and (3-child[0] < 3-child[1])): return None
        return child

    # boat is on the initial side
    if state[2]:
        # move MM to other side
        candidates.append(changeState([0], -2))
        # move CC to other side
        candidates.append(changeState([1], -2))
        # move MC to other side
        candidates.append(changeState([0, 1], -1))
        # move M to other side
        candidates.append(changeState([0], -1))
        # move C to other side
        candidates.append(changeState([1], -1))
    else:
        # move MM to initial side
        candidates.append(changeState([0], 2))
        # move CC to initial side
        candidates.append(changeState([1], 2))
        # move MC to initial side
        candidates.append(changeState([0, 1], 1))
        # move M to initial side
        candidates.append(changeState([0], 1))
        # move C to initial side
        candidates.append(changeState([1], 1))

    for i in candidates:
        if i: children.append(i)
    
    return children


# returns the path from startState to goalState if any
def dfs(path, goalState, depth):
    global expanded

    if depth == 0: return
    if path[-1] == goalState: return path

    expanded.append(path[-1])
    # generate at most four children
    for child in genChild(path[-1]):
        newPath = dfs(path+[child], goalState, depth-1)
        if newPath and newPath!=0: return newPath
    

def ids(startState, goalState):
    for depth in count():
        print("Depth:", depth, end="")
        path = dfs([startState], goalState, depth)
        # return path if goalState is reached at depth
        if path: return path
        print("\tNodes expanded:", len(expanded))
        

# deal with input
startState = [3, 3, 1]
goalState = [0, 0, 0]
print("\nSolving Missionaries and Cannibals Problem with Iterative Deepening Search. ")
print("Initial State: ")
print(startState)
result = ids(startState, goalState)
if result: 
    print("\tFound \nSuccessful path found! \nNodes expanded:", len(expanded), "\n\nPath: ")
    for i, j in enumerate(result): 
        print("Move:", i, " " if i<10 else "", j)
    print()
    for i in result:
        drawState(i)