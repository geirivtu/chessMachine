from inc.chessengine import *
import copy
import findPath


#Safe non-blocking readline and closing port on exit


import serial
import atexit
import time

ser = serial.Serial("COM4")
ser.baudrate = 115200

def exit_handler():
    ser.close()

atexit.register(exit_handler)

print ser.name
ser.timeout = 1


def receiveData():
    recData = ser.readline()
    if (recData.startswith("SENT")):
        print "Data sent"
    elif (recData.startswith("STARTED")):
        print "Node started"
    elif (recData.startswith("ASSOCIATED")):
        print "associated with other node"
    elif (recData.startswith("FAIL")):
        print "Sending failed"
        return "FAIL"
    elif (recData.startswith("NEXT")):
        print "Move completed"
        return "NEXT"

#Returns true if ready for next move, false if not
def sendData(data):
    ser.write(data+"\n")
    while(1):
        rec = receiveData()
        print rec
        if (rec == "FAIL"):
            return False
        if (rec == "NEXT"):
            return True   


#ser.write("whatever")
#ser.readline()


def getCoordinates(moveNumber, player):
    if player == "black":
        clearAll()
        board = createStartPosition()
        playGame(gameLine, moveNumber, 1)
        prevBoard = board
        showBoard()
        clearAll()
        board = createStartPosition()
        playGame(gameLine, moveNumber, 0)
        nextBoard = board
        showBoard()
    elif player == "white":
        clearAll()
        board = createStartPosition()
        playGame(gameLine, moveNumber-1, 0)
        prevBoard = copy.deepcopy(board)
        showBoard()
        clearAll()
        board = createStartPosition()
        playGame(gameLine, moveNumber, 1)
        nextBoard = copy.deepcopy(board)
        showBoard()
    clearAll();
    count = 0
    movedFrom = []
    movedTo = []
    captured = []
    moves = []
    for x in range(8):
        for y in range(8):
            if prevBoard[7-y][x] != nextBoard[7-y][x]:
                count += 1;
                if nextBoard[7-y][x] == "em":
                    movedFrom = (x, y)
                    #print "movedFrom:  " + str(movedFrom)
                elif prevBoard[7-y][x] == "em":
                    movedTo = (x,y)
                    #print "movedTo:  " + str(movedTo)
                else:
                    captured = (x,y)
                    movedTo = (x,y)
                    #print "movedTo:  " + str(movedTo)
                    #print "captured:  " + str(captured)
    if count == 2: # Move , capture or pawn tansform
        if captured != []:
            print "capture"
            print "Remove x: " + str(captured[0]) +" y: " + str(captured[1])
            print "Move x: " + str(movedFrom[0]) + " y: " + str(movedFrom[1]) + " to x: " + str(movedTo[0]) + " y: " + str(movedTo[1]) 
            #moves.append([[(captured[0], captured[1]), (-1, -1)]])
            moves.append([[(movedFrom[0], movedFrom[1]), (movedTo[0], movedTo[1])]])
            return moves
        if nextBoard[7-movedTo[1]][movedTo[0]] != prevBoard[7-movedFrom[1]][movedFrom[0]]:
            print "Pawn transform to " + nextBoard[7-movedTo[1]][movedTo[0]]
            print "Remove x: " + str(movedTo[0]) + " y: " + str(movedTo[1])
            print "Move x: " + str(movedFrom[0]) + " y: " + str(movedFrom[1]) + " to x: " + str(movedTo[0]) + " y: " + str(movedTo[1]) 
            #moves.append([[(movedFrom[0], movedFrom[1]) ,(-1, -1)]])
            #moves.append([[(-1,-1), (movedTo[0] ,movedTo[1])]])
            moves.append([[(movedFrom[0], movedFrom[1]), (movedTo[0] ,movedTo[1])]])
            return moves
        else:
            print "Move x: " + str(movedFrom[0]) + " y: " + str(movedFrom[1]) + " to x: " + str(movedTo[0]) + " y: " + str(movedTo[1]) 
            moves.append([[(movedFrom[0],movedFrom[1]), (movedTo[0], movedTo[1])]])
            return moves
    elif count == 3: # En passant
        print "En passant"
    elif count == 4: # castle
        if movedTo == (2,0) or movedTo == (3,0):
            print "White, long castle"
            moves.append([[(4,0),(2,0)]])
            moves.append([[(0,0),(3,0)]])
            return moves
        if movedTo == (5,0) or movedTo == (6,0):
            print "White, short castle"
            moves.append([[(4,0),(6,0)]])
            moves.append([[(7,0),(5,0)]])
            return moves
        if movedTo == (2,7) or movedTo == (3,7):
            print "Black, long castle"
            moves.append([[(4,7),(2,7)]])
            moves.append([[(0,7),(3,7)]])
            return moves
        if movedTo == (5,7) or movedTo == (6,7):
            print "Black, short castle"
            moves.append([[(4,7),(6,7)]])
            moves.append([[(7,7),(5,7)]])
            return moves

def createBoardMatrix(moveNumber, player):
    board = []
    if player == "black":
        clearAll()
        board = createStartPosition()
        playGame(gameLine, moveNumber, 1)
    elif player == "white":
        clearAll()
        board = createStartPosition()
        playGame(gameLine, moveNumber-1, 0)
        

    boardMatrix = [[0 for x in xrange(8)] for x in xrange(8)]
    for x in range(8):
        for y in range(8):
            if board[x][y] != "em":
                boardMatrix[x][y] = 1
    return boardMatrix
    
def tupToText(instructions):
    text = []
    for ins in instructions:
        temp = ""
        for pos in ins:
            temp += chr(97+ pos[0])
            temp += str(pos[1]+1)
        text.append(temp)
    return text

def simplifyText(text):
    simple = []
    for t in text:
        simple_t = ""
        prev = ""
        count = 1
        for i in range(len(t)/2):
            if t[i*2] == prev:
                count += 1
            else:
                prev = t[i*2]
                count = 1;
            if count >= 3:
                s = list(t)
                s[i*2-2] = "x"
                s[i*2-1] = "x"
                t = "".join(s)
            
        prev = ""
        count = 1
        for i in range(len(t)/2):
            if t[i*2+1] == prev:
                count += 1
            else:
                prev = t[i*2+1]
                count = 1;
            if count >= 3:
                s = list(t)
                s[i*2-2] = "x"
                s[i*2-1] = "x"
                t = "".join(s)
        simple_t = t.replace("x", "")
        simple.append(simple_t)
    return simple
                
def playLine(moveNumber, player):
    moves =  getCoordinates(moveNumber, player)
    boardMatrix = createBoardMatrix(moveNumber, player)
    instructions = []
    for move in moves:
        instructions.extend(findPath.findPath(boardMatrix, move))
        boardMatrix[7-move[0][0][1]][move[0][0][0]] = 0;
        boardMatrix[7-move[0][1][1]][move[0][1][0]] = 1;
    
    #boardMatrix[move[]]
    text = tupToText(instructions)
    return simplifyText(text)
    

### Start main here:
    
gameLine = readFileLine("Hollgam_vs_vinch_2009_05_06.pgn")
#gameLine = readFileLine("test.txt")

moveNumber = 1
player = "black"

for moveNumber in range(1,10):
    print moveNumber
    for move in playLine(moveNumber, "white"):
        print move
        sendData(move)
    sendData("X")
    for move in playLine(moveNumber, "black"):
        print move #send(move)
        sendData(move)
    sendData("X")


        
        
