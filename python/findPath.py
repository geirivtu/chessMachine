import copy
import sys
#brd = [[0 for x in xrange(8)] for x in xrange(8)]


def showWeight(weight):
    for y in range(8):
        for x in range(8):
            sys.stdout.write(str(weight[y][x]) + "\t")
        sys.stdout.write("\n")

def getPath(brd, start, end):
    

    weight = [[(0,10) for x in xrange(8)] for x in xrange(8)]
    for x in range(8):
        for y in range(8):
            weight[x][y] = (0, 10)
    solution = "false"
    path = []
    steps = []
    nextSteps = []
    steps.append((start[0], start[1], 0))
    weight[7-start[1]][start[0]] = (1,0);
    count = 2;
    while solution == "false":
        if len(steps) == 0:
            solution = "true"
        for step in steps:
            if step[1]<7:
                if brd[7-step[1]-1][step[0]] == 1:
                    if weight[7-step[1]-1][step[0]][1] > 1 + step[2]:
                        nextSteps.append((step[0], step[1]+1, step[2]+1))
                        weight[7-step[1]-1][step[0]] = (count, step[2]+1)
                else:
                     if weight[7-step[1]-1][step[0]][1] > step[2]:
                        nextSteps.append((step[0], step[1]+1, step[2]))
                        weight[7-step[1]-1][step[0]] = (count, step[2])

            if step[1]>0:
                if brd[7-step[1]+1][step[0]] == 1:
                    if weight[7-step[1]+1][step[0]][1] > 1 + step[2]:
                        nextSteps.append((step[0], step[1]-1, step[2]+1))
                        weight[7-step[1]+1][step[0]] = (count, step[2]+1)
                else:
                     if weight[7-step[1]+1][step[0]][1] > step[2]:
                        nextSteps.append((step[0], step[1]-1, step[2]))
                        weight[7-step[1]+1][step[0]] = (count, step[2])

            if step[0]<7:
                if brd[7-step[1]][step[0]+1] == 1:
                    if weight[7-step[1]][step[0]+1][1] > 1 + step[2]:
                        nextSteps.append((step[0]+1, step[1], step[2]+1))
                        weight[7-step[1]][step[0]+1] = (count, step[2]+1)
                else:
                     if weight[7-step[1]][step[0]+1][1] > step[2]:
                        nextSteps.append((step[0]+1, step[1], step[2]))
                        weight[7-step[1]][step[0]+1] = (count, step[2])
        
            if step[0]>0:
                if brd[7-step[1]][step[0]-1] == 1:
                    if weight[7-step[1]][step[0]-1][1] > 1 + step[2]:
                        nextSteps.append((step[0]-1, step[1], step[2]+1))
                        weight[7-step[1]][step[0]-1] = (count, step[2]+1)
                else:
                     if weight[7-step[1]][step[0]-1][1] > step[2]:
                        nextSteps.append((step[0]-1, step[1], step[2]))
                        weight[7-step[1]][step[0]-1] = (count, step[2])
        steps = copy.deepcopy(nextSteps)
        nextSteps = []
        count += 1

    step = (end[1], end[0])
    count = weight[7-end[0]][end[1]][0]
    #showWeight(weight)
    path.append(step)
    if solution == "true":
        while step[0] != start[0] or step[1] != start[1]:
            w = weight[7-step[1]][step[0]][1]
            if step[1]<7 and weight[7-step[1]-1][step[0]][0] == count-1 and weight[7-step[1]-1][step[0]][1] < w:
                path.append((step[0], step[1]+1))
                step = (step[0], step[1]+1)
            elif step[1]>0 and weight[7-step[1]+1][step[0]][0] == count-1 and weight[7-step[1]+1][step[0]][1] < w:
                path.append((step[0], step[1]-1))
                step = (step[0], step[1]-1)
            elif step[0]<7 and weight[7-step[1]][step[0]+1][0] == count-1 and weight[7-step[1]][step[0]+1][1] < w:
                path.append((step[0]+1, step[1]))
                step = (step[0]+1, step[1])
            elif step[0]>0 and weight[7-step[1]][step[0]-1][0] == count-1 and weight[7-step[1]][step[0]-1][1] < w:
                path.append((step[0]-1, step[1]))
                step = (step[0]-1, step[1])

            elif step[1]<7 and weight[7-step[1]-1][step[0]][0] == count-1 and weight[7-step[1]-1][step[0]][1] <= w:
                path.append((step[0], step[1]+1))
                step = (step[0], step[1]+1)
            elif step[1]>0 and weight[7-step[1]+1][step[0]][0] == count-1 and weight[7-step[1]+1][step[0]][1] <= w:
                path.append((step[0], step[1]-1))
                step = (step[0], step[1]-1)
            elif step[0]<7 and weight[7-step[1]][step[0]+1][0] == count-1 and weight[7-step[1]][step[0]+1][1] <= w:
                path.append((step[0]+1, step[1]))
                step = (step[0]+1, step[1])
            elif step[0]>0 and weight[7-step[1]][step[0]-1][0] == count-1 and weight[7-step[1]][step[0]-1][1] <= w:
                path.append((step[0]-1, step[1]))
                step = (step[0]-1, step[1])
            else:
                print "fail"
                break
            count -= 1
    return path[::-1]

##def clearPathRecursive(brd, path, moves)
##    result = validSquare(brd, (pos[0]+1, pos[1]), path)
##    if pos[0] < 7 and result != []:
##        return ((pos[0]+1, pos[1]),  result)
##
##    result = validSquare(brd, (pos[0]-1, pos[1]), path)
##    elif pos[0] > 0 and result != []:
##        return ((pos[0]-1, pos[1]), result)
##    
##    result = validSquare(brd, (pos[0], pos[1]+1), path)
##    elif pos[1] < 7 and result != []:
##        return ((pos[0], pos[1]+1), result)
##
##    result = validSquare(brd, (pos[0], pos[1]-1), path)
##    elif pos[1] > 0 and result != []:
##        return ((pos[0], pos[1]-1), result)
##    else:
        
def clearSquare(brd, pos, path):
    solution = "false"
    squares = []
    squares.append([pos]);
    while solution == "false":
        nextSquares = []
        for sqr in squares:
            if sqr[-1][0] < 7:
                result = validSquare(brd, (sqr[-1][0]+1, sqr[-1][1]), path)
                if result != []:
                    sqr.append(result)
                    return sqr
                elif (sqr[-1][0]+1, sqr[-1][1]) not in path:
                    temp = copy.deepcopy(sqr)
                    temp.append((sqr[-1][0]+1, sqr[-1][1]))
                    nextSquares.append(temp)
            
            if sqr[-1][0] > 0:
                result = validSquare(brd, (sqr[-1][0]-1, sqr[-1][1]), path)
                if result != []:
                    sqr.append(result)
                    return sqr
                elif (sqr[-1][0]-1, sqr[-1][1]) not in path:
                    temp = copy.deepcopy(sqr)
                    temp.append((sqr[-1][0]-1, sqr[-1][1]))
                    nextSquares.append(temp)
            
            if sqr[-1][1] < 7:
                result = validSquare(brd, (sqr[-1][0], sqr[-1][1]+1), path)
                if result != []:
                    sqr.append(result)
                    return sqr
                elif (sqr[-1][0], sqr[-1][1]+1) not in path:
                    temp = copy.deepcopy(sqr)
                    temp.append((sqr[-1][0], sqr[-1][1]+1))
                    nextSquares.append(temp)
            
            if sqr[-1][1] > 0:
                result = validSquare(brd, (sqr[-1][0], sqr[-1][1]-1), path)
                if result != []:
                    sqr.append(result)
                    return sqr
                elif (sqr[-1][0], sqr[-1][1]-1) not in path:
                    temp = copy.deepcopy(sqr)
                    temp.append((sqr[-1][0], sqr[-1][1]-1))
                    nextSquares.append(temp)
        squares = copy.deepcopy(nextSquares)
        nextSquares = []

    return []

def validSquare(brd, pos, path):
    if brd[7-pos[1]][pos[0]] == 0 and ((pos[0] , pos[1]) not in path):
        return pos
    return []
                
def clearPath(brd, path):
    obsMoves = []
    for pos in path[1:len(path)]:
        if brd[7-pos[1]][pos[0]] == 1:
            obsMoves.append(clearSquare(brd, pos, path)) # after this, the board must be updated. Only the last spot
            t = obsMoves[-1][-1]
            brd[7-t[1]][t[0]] = 1
    temp = []
    for p in obsMoves:
        for i in range(len(p)-1):
            a = [p[-i-2], p[-i-1]]
            temp.append(a)
    return temp
def findPath(boardMatrix, moves):
    
    boardMatrixCp = copy.deepcopy(boardMatrix);
    start = moves[0][0]
    end = moves[0][1][::-1]
    #print end
    #print end[::-1]
    path = getPath(boardMatrixCp, start, end)
    #print "Path:"
    #print path
    cP = clearPath(boardMatrixCp, path)
    
    revCP = cP[::-1]

    for a in range(len(revCP)):
        revCP[a] = revCP[a][::-1]
    
    allMoves = copy.deepcopy(cP)
    allMoves.append(path)
    allMoves.extend(revCP)
    return allMoves

##brd = [[1, 1, 1, 1, 1, 1, 0, 1],
##        [1, 1, 1, 1, 1, 1, 1, 1],
##        [0, 0, 0, 0, 0, 0, 0, 0],
##        [0, 0, 0, 0, 0, 0, 0, 0],
##        [0, 0, 0, 0, 0, 0, 0, 0],
##        [0, 0, 0, 0, 0, 0, 0, 0],
##        [1, 1, 1, 1, 1, 1, 1, 1],
##        [1, 1, 0, 1, 1, 1, 1, 1]]
##
##moves = [[(2, 0), (7, 6)]];
##findPath(brd, moves)

