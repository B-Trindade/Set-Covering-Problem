NEIGHBORS1 = [
    [1], # I want to start index from 1 instead of 0
    [0, 2, 3],
    [1, 4, 3],
    [1, 2, 4],
    [2, 3],
]
NEIGHBORS = [
    [],
    [1,3,4,5],
    [0,3,4,5],
    [4],
    [0,1],
    [0,1,2,5],
    [0,1,4],
]
NODES = set(range(1, len(NEIGHBORS)))