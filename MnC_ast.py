from itertools import count

def drawState(state):
    print(state[0] * "M", state[1] * "C", (6-state[0]-state[1]) * " ", "|", "B    " if state[2] else "    B", "|", (3-state[0]) * "M", (3-state[1]) * "C")
    print()

def genChild(state):
    children = []
    candidates = []

    def changeState(index, plus):
        child = list(state)[:]
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

# heuristic
def h(state):
    return state[0] + state[1]


def ast(startState, goalState):

    global expanded
    reached = [startState, ]
    parents = {startState : None}
    gn = {startState : 0}
    global fn
    fn = {startState : 0}

    while len(reached) != 0:
        if goalState in reached:
            path = []
            current = goalState
            while current != startState:
                path.append(current)
                current = parents[current]
            return [startState] + path[::-1]
        
        reached.sort(key=lambda x: fn[x])
        node = reached.pop(0)
        expanded.add(node)
        
        for child in genChild(node):
            child = tuple(child)
            if child in expanded: continue
            if child not in reached:
                parents[child] = node
                gn[child] = gn[node] + 1
                fn[child] = gn[node] + 1 + h(child)
                reached.append(child)

    return None


# deal with input
startState = [3, 3, 1]
goalState = [0, 0, 0]

expanded = set()
print("\nSolving Missionaries and Cannibals Problem with A* Search. ")
print("Initial State: ")
print(startState)
result = ast(tuple(startState), tuple(goalState))
if result: 
    print("Successful path found with A* Search!")
    print("Nodes expanded:", len(expanded), "\n\nPath: \n")
    for i, j in enumerate(result): 
        print("Move:", i, " " if i<10 else "", list(j))
    print()
    for i in result:
        drawState(i)
else: 
    print("No successful path found. ")