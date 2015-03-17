import sys
import os.path


castleWhite = 0 # 1 when white has already done castle
castleBlack = 0 # 1 when black has already done castle
kingWhiteMoved = 0 # using it in castles if white king moved = 1 hasn't moved = 0
kingBlackMoved = 0 # using it in castles if black king moved = 1 hasn't moved = 0
rockKingWhiteMoved = 0  # rocked (KING-SIDE WHITE) has made a move
rockQueenWhiteMoved = 0 # rocked (QUEEN-SIDE WHITE)has made a move
rockKingBlackMoved = 0  # rocked (KING-SIDE BLACK) has made a move
rockQueenBlackMoved = 0  # rocked (QUEEN-SIDE WHITE)has made a move
checkMode = 0 # state of check
mateMode = 0 # state of mate
kingWhiteCoord = [7,4] # initial coordinates of white king
kingBlackCoord = [0,4] # initial coordinates of black king
promotionMode = ''
passingMoveAvailable = ''
coordEmpty = []
noBlackMove = 1

lastPosition1 = [9,9]
lastPosition2 = [9,9]
errorAtMove = []

gameLineCorrected = 0

board = []
startBoard = []
moveNumber = 0

takenWhite = []
takenBlack = []


def convertCoord(line):
    """
    converts coordinates into coordinates of the matrix [column][row]
    """
    newLine = ""
    newLineFinal = ""
    diffCoord = "" #Number of row or column which is different in two pieces
    numberOfAddCoord = 0
    tempLine = ""
    haveCastle = 0
    global promotionMode
    promotionMode = ''
    global checkMode
    global mateMode

    if 'O-O' in line and 'O-O-O' not in line:
        if line[0]=='.':
            newLineFinal += 'w'
        else:
            newLineFinal += 'b'
        newLineFinal +=  line[1:]
        haveCastle = 1
    elif 'O-O-O' in line:
        if line[0]=='.':
            newLineFinal += 'w'
        else:
            newLineFinal += 'b'
        newLineFinal +=  line[1:]
        haveCastle = 1
    elif line[0]=='.':
        newLine += 'w'
    else:
        newLine += 'b'
    if not haveCastle:
        for i in range(1,len(line)):
                if line[i] == 'a':
                    newLine += '0'
                elif line[i] == 'b':
                    newLine += '1'
                elif line[i] == 'c':
                    newLine += '2'
                elif line[i] == 'd':
                    newLine += '3'
                elif line[i] == 'e':
                    newLine += '4'
                elif line[i] == 'f':
                    newLine += '5'
                elif line[i] == 'g':
                    newLine += '6'
                elif line[i] == 'h':
                    newLine += '7'
                elif line[i] == '1':
                    newLine += '7'
                elif line[i] == '2':
                    newLine += '6'
                elif line[i] == '3':
                    newLine += '5'
                elif line[i] == '4':
                    newLine += '4'
                elif line[i] == '5':
                    newLine += '3'
                elif line[i] == '6':
                    newLine += '2'
                elif line[i] == '7':
                    newLine += '1'
                elif line[i] == '8':
                    newLine += '0'
                elif line[i] == '.':
                    pass
                elif line[i] == '+':
                    if i == len(line)-1:
                        checkMode = 1
                    else:
                        return 0
                elif line[i] == '#':
                    if i == len(line)-1:
                        mateMode = 1
                    else:
                        return 0
                elif line[i] == 'x':
                    newLine += 'x'
                elif line[i] == 'R':
                    newLine += 'R'
                elif line[i] == 'N':
                    newLine += 'N'
                elif line[i] == 'B':
                    newLine += 'B'
                elif line[i] == 'Q':
                    newLine += 'Q'
                elif line[i] == 'K':
                    newLine += 'K'
                elif line[i] == '=':
                    if ((line[i+1]=='Q') or (line[i+1]=='R') or (line[i+1]=='B') or (line[i+1]=='N')) and i==len(line)-2:
                        promotionMode = line[i+1]
                        break
                    elif ((line[i+1]=='Q') or (line[i+1]=='R') or (line[i+1]=='B') or (line[i+1]=='N')) and i==len(line)-3 and line[len(line)-1]=='+':
                        promotionMode = line[i+1]
                        checkMode = 1
                        break
                    else:
                        return 0
                else:
                    return 0
                #print newLine

        for i in range(len(newLine)-2):
            newLineFinal += newLine[i]
        newLineFinal += newLine[len(newLine)-1]
        newLineFinal += newLine[len(newLine)-2]

#        if "w" in newLineFinal:
#            print "%3d" % moveNumber,
#        else:
#            print "   ",
#        print "Original: ",
#        if "." not in line:
#            print "%5s" % line,
#        else:
#            print "%5s" % line[1:],
#        print " :: Converted: ", newLineFinal

        if newLineFinal[1] == 'R' or newLineFinal[1] == 'N' or newLineFinal[1] == 'B' or newLineFinal[1] == 'K':
            if len(newLineFinal)>4 and newLineFinal[2]!='x':
                if len(newLineFinal)>5:
                    try:
                        number = int(newLineFinal[3])
                        number = int(newLineFinal[2])
                        numberOfAddCoord = 2
                    except:
                        try:
                            number = int(newLineFinal[2])
                            numberOfAddCoord = 1
                        except:
                            numberOfAddCoord = 0
                else:
                    numberOfAddCoord = 1
                if numberOfAddCoord == 2:
                    tempLine = newLineFinal[0:2]+'r'+newLineFinal[3]+'c'+newLineFinal[2]+newLineFinal[4:len(newLineFinal)]
                    newLineFinal = tempLine

                elif numberOfAddCoord == 1:
                    try:                                #row
                        number = int(line[2])
                        diffCoord = 'r'+newLineFinal[2]
                    except:                             #column
                        diffCoord = 'c'+newLineFinal[2]
                    tempLine = newLineFinal[0:2]+diffCoord+newLineFinal[3:len(newLineFinal)]
                    newLineFinal = tempLine

    return newLineFinal

def cellUnderAttack(row,column,color,canMoveCheckOnly = 0):

    # you send color of piece which can attack cell. if canmovecheckonly==1, then not only possibility of attack on the
    # cell will be checked, but ability of moving there too (without king)

    global board
    underAttack = 0
    cellsAttack = []
    #horisontal
    #right
    for i in range(column+1,8):
        if board[row][i]==color+'Q' or board[row][i]==color+'R':
            underAttack = 1
            cellsAttack += [[row*10+i]]
        elif board[row][i]!='em':
            break
    #left
    for i in range(column-1,-1,-1):
        if board[row][i]==color+'Q' or board[row][i]==color+'R':
            underAttack = 1
            cellsAttack += [[row,i]]
        elif board[row][i]!='em':
            break
    #vertical
    #up
    for i in range(row+1,8):
        if board[i][column]==color+'Q' or board[i][column]==color+'R':
            underAttack = 1
            cellsAttack += [[i,column]]
        elif board[i][column] != 'em':
            break
    #down
    for i in range(row-1,-1,-1):
        if board[i][column]==color+'Q' or board[i][column]==color+'R':
            underAttack = 1
            cellsAttack += [[i,column]]
        elif board[i][column]!='em':
            break
    #diagonal
    #upright
    checkContinue = 1
    r = row
    c = column
    while checkContinue:
        r += 1
        c += 1
        if r<0 or r>7 or c<0 or c>7:
            checkContinue = 0
        else:
            if board[r][c]==color+'B' or board[r][c]==color+'Q':
                underAttack = 1
                cellsAttack += [[r,c]]
            elif board[r][c] != 'em':
                checkContinue = 0

    #upleft
    checkContinue = 1
    r = row
    c = column
    while checkContinue:
        r += 1
        c -= 1
        if r<0 or r>7 or c<0 or c>7:
            checkContinue = 0
        else:
            if board[r][c]==color+'B' or board[r][c]==color+'Q':
                underAttack = 1
                cellsAttack += [[r,c]]
            elif board[r][c] != 'em':
                checkContinue = 0
    #downright
    checkContinue = 1
    r = row
    c = column
    while checkContinue:
        r -= 1
        c += 1
        if r<0 or r>7 or c<0 or c>7:
            checkContinue = 0
        else:
            if board[r][c]==color+'B' or board[r][c]==color+'Q':
                underAttack = 1
                cellsAttack += [[r,c]]
            elif board[r][c] != 'em':
                checkContinue = 0
    #downleft
    checkContinue = 1
    r = row
    c = column
    while checkContinue:
        r -= 1
        c -= 1
        if r<0 or r>7 or c<0 or c>7:
            checkContinue = 0
        else:
            if board[r][c]==color+'B' or board[r][c]==color+'Q':
                underAttack = 1
                cellsAttack += [[r,c]]
            elif board[r][c] != 'em':
                checkContinue = 0
    #pawn
    if not canMoveCheckOnly:
        if color =='w':
            if row<7:
                if (column>0 and board[row+1][column-1]=='wP'):
                    underAttack = 1
                    cellsAttack += [[(row+1),(column-1)]]
                if (column<7 and board[row+1][column+1]=='wP'):
                    underAttack = 1
                    cellsAttack += [[(row+1),(column+1)]]
        elif color == 'b':
            if row>0:
                if (column>0 and board[row-1][column-1]=='bP'):
                    underAttack = 1
                    cellsAttack += [[(row-1),(column-1)]]
                if  (column<7 and board[row-1][column+1]=='bP'):
                    underAttack = 1
                    cellsAttack += [[(row-1),(column+1)]]
    else:
        if color =='w':
            if row<7:
                if (column>0 and board[row+1][column-1]=='wP') and board[row][column]=='bP':
                    underAttack = 1
                    cellsAttack += [[(row+1),(column-1)]]
                if (column<7 and board[row+1][column+1]=='wP') and board[row][column]=='bP':
                    underAttack = 1
                    cellsAttack += [[(row+1),(column+1)]]
                if row<7 and board[row+1][column]=='wP':
                    underAttack = 1
                    cellsAttack += [[(row+1),(column)]]
        elif color=='b':
            if row>0:
                if (column>0 and board[row-1][column-1]=='bP') and board[row][column]=='wP':
                    underAttack = 1
                    cellsAttack += [[(row-1),(column-1)]]
                if  (column<7 and board[row-1][column+1]=='bP') and board[row][column]=='wP':
                    underAttack = 1
                    cellsAttack += [[(row-1),(column+1)]]
                if row>0 and board[row-1][column]=='bP':
                    underAttack = 1
                    cellsAttack += [[(row-1),(column)]]

    #king
    if not canMoveCheckOnly:
        stopCycle = 0
        for i in range(row-1,row+2):
                for j in range(column-1, column+2):
                    if i<8 and i>-1 and j<8 and j>-1 and board[i][j]==color+'K' and str(i)+str(j) != str(row)+str(column):
                        underAttack = 1
                        stopCycle = 1
                        cellsAttack += [[i,j]]
                        break
                if stopCycle:
                    break
    #knight
    for i in range(8):
        for j in range(8):
            if board[i][j]==color+'N':
                if abs(i-row)+abs(j-column)==3 and (abs(i-row)==2 or abs(j-column)==2):
                    underAttack = 1
                    cellsAttack += [[i,j]]

    if not underAttack:
        return 0
    else:
        return cellsAttack

def changePosition(moveLine):
    """
    makes move 'moveLine'
    """

    global kingWhiteMoved # using it in castles if white king moved = 1 hasn't moved = 0
    global kingBlackMoved # using it in castles if black king moved = 1 hasn't moved = 0
    global rockKingWhiteMoved  # rocked (KING-SIDE WHITE) has made a move
    global rockQueenWhiteMoved # rocked (QUEEN-SIDE WHITE)has made a move
    global rockKingBlackMoved  # rocked (KING-SIDE BLACK) has made a move
    global rockQueenBlackMoved  # rocked (QUEEN-SIDE WHITE)has made a move
    global checkMode
    global mateMode
    global castleWhite
    global castleBlack
    global kingWhiteCoord
    global kingBlackCoord
    global passingMoveAvailable

    global lastPosition1
    global lastPosition2

    global takenWhite
    global takenBlack

    piecesOnWay = 0 # var for finding pieces on the way
    pawnIsMoving = 0 #if is pawn's move
    checkFurther = 1 #checking after validation coordinates of initial position
    piecesFound = 0 # indicates how many pieces which can move to the deestination are found
    global coordEmpty # coordinates of a cell which is made to be empty
    coordEmpty = []
    piecesError = 0 # error that indicates that there are pieces on the way
    pieceAdditional = 0 # number of pieces that match additional coords found
    makeCastle = 1 # posibility to make a castle
    castleMode = 0 #indicates that castle has been made
    kingUnderAttack = 0

    moveLine = convertCoord(moveLine)
    if moveLine:
        ### BISHOP ###
        if moveLine[1] == "B":
            dif = int(moveLine[-1])-int(moveLine[-2])
            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-2])+1,8):
                    if 0 <= i+dif <= 7:
                        if  board[i][i+dif][0:2] == moveLine[0:2]:
                            if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and i+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                            elif 'c' in moveLine and i+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                            elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                            if piecesOnWay:
                                if piecesFound == 0:
                                    piecesError = 1
                            else:
                                piecesFound += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                piecesError = 0
                            break
                        elif  board[i][i+dif][0:2] != "em":
                            piecesOnWay = 1
                    else:
                        break

            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-2])-1,-1,-1):
                    if 0 <= i+dif <= 7:
                        if  board[i][i+dif][0:2] == moveLine[0:2]:
                            if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and i+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                            elif 'c' in moveLine and i+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                            elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                            if piecesOnWay:
                                if piecesFound == 0:
                                    piecesError = 1
                            else:
                                piecesFound += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                piecesError = 0
                            break
                        elif  board[i][i+dif][0:2] != "em":
                            piecesOnWay = 1
                    else:
                        break

            if checkFurther:
                piecesOnWay = 0
                j = int(moveLine[-2])
                for i in range(int(moveLine[-2])+1, 8):
                    j-=1
                    if 0 <= j+dif <= 7 and 0 <= i <= 7:
                        if  board[i][j+dif][0:2] == moveLine[0:2]:
                            if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and j+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                            elif 'c' in moveLine and j+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                            elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                            if piecesOnWay:
                                if piecesFound == 0:
                                    piecesError = 1
                            else:
                                piecesFound += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                piecesError = 0
                            break
                        elif  board[i][j+dif][0:2] != "em":
                            piecesOnWay = 1
                    else:
                        break

            if checkFurther:
                piecesOnWay = 0
                j = int(moveLine[-2])
                for i in range(int(moveLine[-2])-1, -1, -1):
                    j+=1
                    if 0 <= j+dif <= 7 and 0 <= i <= 7:
                        if  board[i][j+dif][0:2] == moveLine[0:2]:
                            if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and j+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                            elif 'c' in moveLine and j+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                            elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                            if piecesOnWay:
                                if piecesFound == 0:
                                    piecesError = 1
                            else:
                                piecesFound += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                piecesError = 0
                            break
                        elif  board[i][j+dif][0:2] != "em":
                            piecesOnWay = 1
                    else:
                        break

        ### KNIGHT ###
        elif moveLine[1]=='N':
            #FindAllHorses
            horseList = ''
            numberOfHorses = 0
            deleteHorse = 0
            cutLine = 0
            temp = ""
            cIndex = 0
            checkComplete = 0 #viewed all string with horses
            for i in range(8):
                for j in range(8):
                    if board[i][j][0:2]==moveLine[0:2]:
                        if abs(i-int(moveLine[-2]))+abs(j-int(moveLine[-1]))==3 and (abs(i-int(moveLine[-2]))==2 or abs(j-int(moveLine[-1]))==2):
                            numberOfHorses += 1
                            horseList += str(i)+str(j)
            if 'r' in moveLine:
                if numberOfHorses>0:
                    checkComplete = 0
                    while not checkComplete:
                        for i in range(0,numberOfHorses*2,2):
                            if not int(moveLine[3])==int(horseList[i]):
                                cutLine = 1
                                temp = horseList[0:i]+horseList[i+2:len(horseList)]
                                horseList = temp
                                numberOfHorses -= 1
                                break
                            else:
                                cutLine = 0
                            if (cutLine==0 and i==len(horseList)-2) or (cutLine==1 and i==len(horseList)):
                                checkComplete = 1
                                break
            if 'c' in moveLine:
                if numberOfHorses>0:
                    cIndex = moveLine.find('c')+1
                    checkComplete = 0
                    while not checkComplete:
                        for i in range(1,numberOfHorses*2,2):
                            if not int(moveLine[cIndex])==int(horseList[i]):
                                cutLine = 1
                                temp = horseList[0:i-1]+horseList[i+1:len(horseList)]
                                horseList = temp
                                numberOfHorses -= 1
                                break
                            else:
                                cutLine = 0
                            if (cutLine==0 and i==len(horseList)-1) or (cutLine==1 and i==len(horseList)+1):
                                checkComplete = 1
                                break
            piecesFound = numberOfHorses
            pieceAdditional = numberOfHorses
            if numberOfHorses>0:
                coordEmpty += [int(horseList[0])]
                coordEmpty += [int(horseList[1])]


        ### ROCK ###
        elif moveLine[1]=='R':
            #Checking Vertical line for presence of ROCK
            if checkFurther:
                for i in range(int(moveLine[-2])-1,-1,-1):
                    if board[i][int(moveLine[-1])][0:2]== moveLine[0:2]:
                        if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and int(moveLine[-1]) == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        elif 'c' in moveLine and int(moveLine[-1]) == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        if piecesOnWay:
                            if piecesFound == 0:
                                piecesError = 1
                        else:
                            piecesFound += 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            piecesError = 0
                        break
                    elif  board[i][int(moveLine[-1])][0:2] != "em":
                        piecesOnWay = 1

            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-2])+1,8):
                    if board[i][int(moveLine[-1])][0:2]== moveLine[0:2]:
                        if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and int(moveLine[-1]) == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        elif 'c' in moveLine and int(moveLine[-1]) == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        if piecesOnWay:
                            if piecesFound == 0:
                                piecesError = 1
                        else:
                            piecesFound += 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            piecesError = 0
                        break
                    elif  board[i][int(moveLine[-1])][0:2] != "em":
                        piecesOnWay = 1


            #Checking Horisontal line for presence of ROCK
            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-1])-1,-1,-1):
                    if board[int(moveLine[-2])][i][0:2]== moveLine[0:2]:
                        if 'c' in moveLine and 'r' in moveLine and int(moveLine[-2]) == int(moveLine[moveLine.find("r")+1]) and i == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        elif 'c' in moveLine and i == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        elif 'r' in moveLine and int(moveLine[-2]) == int(moveLine[moveLine.find("r")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break

                        if piecesOnWay:
                            if piecesFound == 0:
                                piecesError = 1
                        else:
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            piecesFound += 1
                            piecesError = 0
                        break
                    elif  board[int(moveLine[-2])][i][0:2] != "em":
                        piecesOnWay = 1

            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-1])+1,8):
                    if board[int(moveLine[-2])][i][0:2]== moveLine[0:2]:
                        if 'c' in moveLine and 'r' in moveLine and int(moveLine[-2]) == int(moveLine[moveLine.find("r")+1]) and i == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        elif 'c' in moveLine and i == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        elif 'r' in moveLine and int(moveLine[-2]) == int(moveLine[moveLine.find("r")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        if piecesOnWay:
                            if piecesFound == 0:
                                piecesError = 1
                        else:
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            piecesFound += 1
                            piecesError = 0
                        break
                    elif  board[int(moveLine[-2])][i][0:2] != "em":
                        piecesOnWay = 1

        ### QUEEN ROCKS###
        elif moveLine[1]=='Q':
            #rock part
            #Checking Vertical line for presence of QUEEN
            if checkFurther:
                for i in range(int(moveLine[-2])-1,-1,-1):
                    if board[i][int(moveLine[-1])][0:2]== moveLine[0:2]:
                        if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and int(moveLine[-1]) == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        elif 'c' in moveLine and int(moveLine[-1]) == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        if piecesOnWay:
                            if piecesFound == 0:
                                piecesError = 1
                        else:
                            piecesFound += 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            piecesError = 0
                        break
                    elif  board[i][int(moveLine[-1])][0:2] != "em":
                        piecesOnWay = 1

            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-2])+1,8):
                    if board[i][int(moveLine[-1])][0:2]== moveLine[0:2]:

                        if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and int(moveLine[-1]) == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        elif 'c' in moveLine and int(moveLine[-1]) == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            break
                        if piecesOnWay:
                            if piecesFound == 0:
                                piecesError = 1
                        else:
                            piecesFound += 1
                            coordEmpty += [i]
                            coordEmpty += [int(moveLine[-1])]
                            piecesError = 0
                        break
                    elif  board[i][int(moveLine[-1])][0:2] != "em":
                        piecesOnWay = 1


            #Checking Horisontal line for presence of ROCK
            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-1])-1,-1,-1):
                    if board[int(moveLine[-2])][i][0:2]== moveLine[0:2]:
                        if 'c' in moveLine and 'r' in moveLine and int(moveLine[-2]) == int(moveLine[moveLine.find("r")+1]) and i == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        elif 'c' in moveLine and i == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        elif 'r' in moveLine and int(moveLine[-2]) == int(moveLine[moveLine.find("r")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        if piecesOnWay:
                            if piecesFound == 0:
                                piecesError = 1
                        else:
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            piecesFound += 1
                            piecesError = 0
                        break
                    elif  board[int(moveLine[-2])][i][0:2] != "em":
                        piecesOnWay = 1

            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-1])+1,8):
                    if board[int(moveLine[-2])][i][0:2]== moveLine[0:2]:
                        if 'c' in moveLine and 'r' in moveLine and int(moveLine[-2]) == int(moveLine[moveLine.find("r")+1]) and i == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        elif 'c' in moveLine and i == int(moveLine[moveLine.find("c")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        elif 'r' in moveLine and int(moveLine[-2]) == int(moveLine[moveLine.find("r")+1]):
                            checkFurther = 0
                            piecesFound = 1
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            break
                        if piecesOnWay:
                            if piecesFound == 0:
                                piecesError = 1
                        else:
                            coordEmpty += [int(moveLine[-2])]
                            coordEmpty += [i]
                            piecesFound += 1
                            piecesError = 0
                        break
                    elif  board[int(moveLine[-2])][i][0:2] != "em":
                        piecesOnWay = 1

            #bishop part
            dif = int(moveLine[-1])-int(moveLine[-2])
            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-2])+1,8):
                    if 0 <= i+dif <= 7:
                        if  board[i][i+dif][0:2] == moveLine[0:2]:
                            if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and i+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                break
                            elif 'c' in moveLine and i+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                break
                            elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                break
                            if piecesOnWay:
                                if piecesFound == 0:
                                    piecesError = 1
                            else:
                                piecesFound += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                piecesError = 0
                            break
                        elif  board[i][i+dif][0:2] != "em":
                            piecesOnWay = 1
                    else:
                        break

            if checkFurther:
                piecesOnWay = 0
                for i in range(int(moveLine[-2])-1,-1,-1):
                    if 0 <= i+dif <= 7:
                        if  board[i][i+dif][0:2] == moveLine[0:2]:
                            if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and i+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                break
                            elif 'c' in moveLine and i+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                break
                            elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                break
                            if piecesOnWay:
                                if piecesFound == 0:
                                    piecesError = 1
                            else:
                                piecesFound += 1
                                coordEmpty += [i]
                                coordEmpty += [i+dif]
                                piecesError = 0
                            break
                        elif  board[i][i+dif][0:2] != "em":
                            piecesOnWay = 1
                    else:
                        break

            if checkFurther:
                piecesOnWay = 0
                j = int(moveLine[-2])
                for i in range(int(moveLine[-2])+1, 8):
                    j-=1
                    if 0 <= j+dif <= 7 and 0 <= i <= 7:
                        if  board[i][j+dif][0:2] == moveLine[0:2]:
                            if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and j+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                break
                            elif 'c' in moveLine and j+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                break
                            elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                break
                            if piecesOnWay:
                                if piecesFound == 0:
                                    piecesError = 1
                            else:
                                piecesFound += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                piecesError = 0
                            break
                        elif  board[i][j+dif][0:2] != "em":
                            piecesOnWay = 1
                    else:
                        break

            if checkFurther:
                piecesOnWay = 0
                j = int(moveLine[-2])
                for i in range(int(moveLine[-2])-1, -1, -1):
                    j+=1
                    if 0 <= j+dif <= 7 and 0 <= i <= 7:
                        if  board[i][j+dif][0:2] == moveLine[0:2]:
                            if 'c' in moveLine and 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]) and j+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                break
                            elif 'c' in moveLine and j+dif == int(moveLine[moveLine.find("c")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                break
                            elif 'r' in moveLine and i == int(moveLine[moveLine.find("r")+1]):
                                checkFurther = 0
                                piecesFound = 1
                                pieceAdditional += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                break
                            if piecesOnWay:
                                if piecesFound == 0:
                                    piecesError = 1
                            else:
                                piecesFound += 1
                                coordEmpty += [i]
                                coordEmpty += [j+dif]
                                piecesError = 0
                            break
                        elif  board[i][j+dif][0:2] != "em":
                            piecesOnWay = 1
                    else:
                        break


        ### KING ###
        elif moveLine[1]=='K':  #check field 3x3 and find there king; replice that piece with king with input coords
            if checkFurther:
                for i in range(int(moveLine[-2])-1,int(moveLine[-2])+2):
                    for j in range(int(moveLine[-1])-1,int(moveLine[-1])+2):
                        if i<8 and i>-1 and j<8 and j>-1 and board[i][j][:2]==moveLine[:2] and str(i)+str(j) != int(moveLine[-2:]):
                            piecesFound = 1
                            kingMoved = 1
                            coordEmpty += [i]
                            coordEmpty += [j]
                            break
                    if piecesFound == 1:
                        break
                if moveLine[0]=='w':
                    if cellUnderAttack(int(moveLine[-2]),int(moveLine[-1]),'b'):
                        kingUnderAttack = 1
                elif moveLine[0]=='b':
                    if cellUnderAttack(int(moveLine[-2]),int(moveLine[-1]),'w'):
                        kingUnderAttack = 1

        ### CASTLES ###
        ## QUEEN-SIDE ##
        elif 'O-O-O' in moveLine:
            if moveLine == 'wO-O-O':
                if board[-1][0] == "wR" and board[-1][1] == "em" and board[-1][2] == "em" and board[-1][3] == "em" and board[-1][4] == "wK" and not rockQueenWhiteMoved and not kingWhiteMoved and not cellUnderAttack(7,1,'b') and not cellUnderAttack(7,2,'b') and not cellUnderAttack(7,3,'b') and not kingUnderAttack:
                    board[-1][0] = board[-1][1] = board[-1][4] = "em"
                    board[-1][2] = "wK"
                    kingWhiteCoord[0] = 7
                    kingWhiteCoord[1] = 2
                    board[-1][3] = "wR"
                   # castleMode = 1
                    castleWhite = 1
                    return 1
                else:
                    makeCastle = 0
            elif moveLine == 'bO-O-O':
                if board[0][0] == "bR" and board[0][1] == "em" and board[0][2] == "em" and board[0][3] == "em" and board[0][4] == "bK" and not rockQueenBlackMoved and not kingBlackMoved and not cellUnderAttack(0,1,'w') and not cellUnderAttack(0,2,'w') and not cellUnderAttack(0,3,'w') and not kingUnderAttack:
                    board[0][0] = board[0][1] = board[-1][4] = "em"
                    board[0][2] = "bK"
                    kingBlackCoord[0] = 0
                    kingBlackCoord[1] = 2
                    board[0][3] = "bR"
                    #castleMode = 1
                    castleBlack = 1
                    return 1
                else:
                    makeCastle = 0

        ## KING-SIDE ##
        elif 'O-O' in moveLine:
            if moveLine == 'wO-O':
                if board[-1][-1] == "wR" and board[-1][-2] == "em" and board[-1][-3] == "em" and board[-1][-4] == "wK" and not rockKingWhiteMoved and not kingWhiteMoved and not cellUnderAttack(7,6,'b') and not cellUnderAttack(7,5,'b') and not kingUnderAttack:
                    board[-1][-1] = board[-1][-4] = "em"
                    board[-1][-2] = "wK"
                    kingWhiteCoord[0] = 7
                    kingWhiteCoord[1] = 6
                    board[-1][-3] = "wR"
                   # castleMode = 1
                    castleWhite = 1
                    return 1
                else:
                    makeCastle = 0
            elif moveLine == 'bO-O':
                if board[0][-1] == "bR" and board[0][-2] == "em" and board[0][-3] == "em" and board[0][-4] == "bK" and not rockKingBlackMoved and not kingBlackMoved and not cellUnderAttack(0,6,'w') and not cellUnderAttack(0,5,'w') and not kingUnderAttack:
                    board[0][-1] = board[0][-4] = "em"
                    board[0][-2] = "bK"
                    kingBlackCoord[0] = 0
                    kingBlackCoord[1] = 6
                    board[0][-3] = "bR"
                    #castleMode = 1
                    castleBlack = 1
                    return 1
                else:
                    makeCastle = 0

 ## PAWN ###
        elif moveLine[1] in ['1','2','3','4','5','6','7','8','9','0'] :
            if checkFurther:
                piecesFound = 0
                #ordinary move white/black, short/long
                if len(moveLine)==3:
                    if moveLine[0]=='w' and int(moveLine[1])<7 and board[int(moveLine[1])+1][int(moveLine[2])]=="wP":   #white pawn
                        coordEmpty += [int(moveLine[1])+1]
                        coordEmpty += [int(moveLine[2])]
                        piecesFound = 1
                        pawnIsMoving = 1
                    elif moveLine[0]=='w' and board[6][int(moveLine[2])]=="wP" and moveLine[1]=='4':
                        if board[5][int(moveLine[2])]=='em':
                            coordEmpty += [6]
                            coordEmpty += [int(moveLine[2])]
                            piecesFound = 1
                            pawnIsMoving = 1
                            passingMoveAvailable = 'b'+moveLine[-1]
                        else:
                            piecesError = 1
                    elif moveLine[0]=='b' and int(moveLine[1])>0 and board[int(moveLine[1])-1][int(moveLine[2])]=="bP":   #black pawn
                        coordEmpty += [int(moveLine[1])-1]
                        coordEmpty += [int(moveLine[2])]
                        piecesFound = 1
                        pawnIsMoving = 1
                        passingMoveAvailable = 'w'+moveLine[-1]
                    elif moveLine[0]=='b' and board[1][int(moveLine[2])]=="bP" and moveLine[1]=='3':
                        if board[2][int(moveLine[2])]=='em':
                            coordEmpty += [int(moveLine[1])-2]
                            coordEmpty += [int(moveLine[2])]
                            piecesFound = 1
                            pawnIsMoving = 1
                        else:
                            piecesError = 1
                    else:
                        piecesError = 1
                                        #ATTACK#
                if len(moveLine)==5 and moveLine[2]=='x': #'shot'
                    if moveLine[0]=='w' and board[int(moveLine[3])+1][int(moveLine[1])]=='wP':
                        coordEmpty += [int(moveLine[3])+1]
                        coordEmpty += [int(moveLine[1])]
                        piecesFound = 1
                        pawnIsMoving = 1
                    if moveLine[0]=='b' and board[int(moveLine[3])-1][int(moveLine[1])]=='bP':
                        coordEmpty += [int(moveLine[3])-1]
                        coordEmpty += [int(moveLine[1])]
                        piecesFound = 1
                        pawnIsMoving = 1
                    elif passingMoveAvailable!='':
                        if moveLine[0]==passingMoveAvailable[0]:
                            #check, if pawn is moving on correct row and passing move can be made on right column
                            #and if there are pawns in coord of move and in cell of attack
                            if moveLine=='w' and moveLine[-1]=='5' and moveLine[-2]==passingMoveAvailable[-1] and board[int(moveLine[3])-1][int(moveLine[1])]=='wP' and board[int(moveLine[-2])-1][int(moveLine[-1])]=='bP':
                                coordEmpty += [int(moveLine[3])-1]
                                coordEmpty += [int(moveLine[1])]
                                piecesFound = 1
                                pawnIsMoving = 1
                        passingMoveAvailable = ''

                pieceAdditional = piecesFound
    else:
        return 12

    if piecesFound != 0:
        if board[int(moveLine[-2])][int(moveLine[-1])][0]  == moveLine[0]:
            # check if there are 2 pieces of same color on 2 coords
            return 2
        elif 'x' not in moveLine and board[int(moveLine[-2])][int(moveLine[-1])][0]  != moveLine[0] and board[int(moveLine[-2])][int(moveLine[-1])][0:2]  != "em":
            #check if a move needs 'x'
            return 3
        elif 'x' in moveLine and board[int(moveLine[-2])][int(moveLine[-1])][0]  == moveLine[0]:
            #trying to take own piece
            return 4
        elif 'x' in moveLine and board[int(moveLine[-2])][int(moveLine[-1])][0:2]  == "em":
            #trying to take an empty cell
            return 5

    #different checks for checking if a move is valid
    if not castleMode:
        if piecesError == 0 and piecesFound == 1 and kingUnderAttack==1:
            return 11
        elif piecesError == 0 and piecesFound == 1:
            
            # adding taken pieces to a list of taken pieces
            if board[int(moveLine[-2])][int(moveLine[-1])][0] == "w":
               if board[int(moveLine[-2])][int(moveLine[-1])][1] == "R":
                   takenBlack.append("R")
               elif board[int(moveLine[-2])][int(moveLine[-1])][1] == "N":
                   takenBlack.append("N")
               elif board[int(moveLine[-2])][int(moveLine[-1])][1] == "B":
                   takenBlack.append("B")
               elif board[int(moveLine[-2])][int(moveLine[-1])][1] == "Q":
                   takenBlack.append("Q")
               elif board[int(moveLine[-2])][int(moveLine[-1])][1] == "P":
                   takenBlack.append("P")

            elif board[int(moveLine[-2])][int(moveLine[-1])][0] == "b":
               if board[int(moveLine[-2])][int(moveLine[-1])][1] == "R":
                   takenWhite.append("R")
               elif board[int(moveLine[-2])][int(moveLine[-1])][1] == "N":
                   takenWhite.append("N")
               elif board[int(moveLine[-2])][int(moveLine[-1])][1] == "B":
                   takenWhite.append("B")
               elif board[int(moveLine[-2])][int(moveLine[-1])][1] == "Q":
                   takenWhite.append("Q")
               elif board[int(moveLine[-2])][int(moveLine[-1])][1] == "P":
                   takenWhite.append("P")

            board[coordEmpty[-2]][coordEmpty[-1]] = "em"
            lastPosition1[0] = coordEmpty[-2]
            lastPosition1[1] = coordEmpty[-1]
            if not pawnIsMoving:
                board[int(moveLine[-2])][int(moveLine[-1])]=moveLine[0:2]
                lastPosition2[0] = int(moveLine[-2])
                lastPosition2[1] = int(moveLine[-1])
                #check if Rock has made moves for making castles
                if moveLine[0:2] == "wR" and coordEmpty[-2] == 7 and coordEmpty[-1] == 7 and not rockKingWhiteMoved:
                    #White King Rock
                    rockKingWhiteMoved = 1
                elif moveLine[0:2] == "wR" and coordEmpty[-2] == 7 and coordEmpty[-1] == 0 and not rockQueenWhiteMoved:
                    #White Queen Rock
                    rockQueenWhiteMoved = 1
                elif moveLine[0:2] == "bR" and coordEmpty[-2] == 0 and coordEmpty[-1] == 0 and not rockQueenBlackMoved:
                    #Black Queen Rock
                    rockQueenBlackMoved = 1
                elif moveLine[0:2] == "bR" and coordEmpty[-2] == 0 and coordEmpty[-1] == 7 and not rockKingBlackMoved:
                    #Black King Rock
                    rockKingBlackMoved = 1
                elif moveLine[0:2] == "wK":
                    #White King
                    if not kingWhiteMoved:
                        kingWhiteMoved = 1
                    kingWhiteCoord[0] = int(moveLine[-2])
                    kingWhiteCoord[1] = int(moveLine[-1])
                elif moveLine[0:2] == "bK":
                    #Black King
                    if not kingBlackMoved:
                        kingBlackMoved = 1
                    kingBlackCoord[0] = int(moveLine[-2])
                    kingBlackCoord[1] = int(moveLine[-1])
            else:
                if promotionMode=='':
                    board[int(moveLine[-2])][int(moveLine[-1])]=moveLine[0]+'P'
                    lastPosition2[0] = int(moveLine[-2])
                    lastPosition2[1] = int(moveLine[-1])
                else:
                    board[int(moveLine[-2])][int(moveLine[-1])]=moveLine[0]+promotionMode
                    lastPosition2[0] = int(moveLine[-2])
                    lastPosition2[1] = int(moveLine[-1])


        elif   moveLine == "wO-O" and castleWhite:
            return 10
        elif   moveLine == "wO-O-O" and castleWhite:
            return 10
        elif   moveLine == "bO-O" and castleBlack:
            return 10
        elif   moveLine == "bO-O-O" and castleBlack:
            return 10
        elif  not makeCastle:
            return 9
        elif pieceAdditional == 0  and 'c' in moveLine and 'r' in moveLine:
            return 8
        elif pieceAdditional == 0  and 'c' in moveLine:
            return 8
        elif pieceAdditional == 0  and 'r' in moveLine:
            return 8
        elif piecesFound > 1 and not piecesError:
            return 6
        elif piecesFound == 0:
            return 7
        elif piecesError == 1:
            return 13

    ### CHECK ###
    if checkMode == 1 and piecesFound != 0 :
        if moveLine[0] == "w":
            if not cellUnderAttack(kingBlackCoord[0], kingBlackCoord[1], "w"):
                board[int(moveLine[-2])][int(moveLine[-1])]= "em"
                if not pawnIsMoving:
                    board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0:2]
                else:
                    if promotionMode=='':
                        board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0]+'P'
                    else:
                        board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0]+promotionMode
                return 17

        else:
            if not cellUnderAttack(kingWhiteCoord[0], kingWhiteCoord[1], "b"):
                board[int(moveLine[-2])][int(moveLine[-1])]= "em"
                if not pawnIsMoving:
                    board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0:2]
                else:
                    if promotionMode=='':
                        board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0]+'P'
                    else:
                        board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0]+promotionMode
                return 17
        checkMode = 2

    # checks if a move after check is valid
    elif checkMode == 2 and piecesFound != 0:
        if moveLine[0] == "w":
            if cellUnderAttack(kingWhiteCoord[0], kingWhiteCoord[1], "b"):
                board[int(moveLine[-2])][int(moveLine[-1])]= "em"
                if not pawnIsMoving:
                    board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0:2]
                else:
                    if promotionMode=='':
                        board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0]+'P'
                    else:
                        board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0]+promotionMode
                return 18
        else:
            if cellUnderAttack(kingBlackCoord[0], kingBlackCoord[1], "w"):
                board[int(moveLine[-2])][int(moveLine[-1])]= "em"
                if not pawnIsMoving:
                    board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0:2]
                else:
                    if promotionMode=='':
                        board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0]+'P'
                    else:
                        board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0]+promotionMode
                return 18
        checkMode = 0

    ### CHECKMATE ###
    ##replace cellUnderAttack with new function
    elif mateMode and piecesFound != 0:
        checkFurther = 1
        if moveLine[0] == "w":
            attackPieces = cellUnderAttack(kingBlackCoord[0], kingBlackCoord[1], "w")
        else:
            attackPieces = cellUnderAttack(kingWhiteCoord[0], kingWhiteCoord[1], "b")
        if moveLine[0] == "w":
            kingAttacked = kingBlackCoord
            sideAttacks = "w"
            sideDefends = "b"
        else:
            kingAttacked = kingWhiteCoord
            sideAttacks = "b"
            sideDefends = "w"

        if not cellUnderAttack(kingAttacked[0], kingAttacked[1], sideAttacks):
            return 19
        #main part checks if avoiding mate is possible
        for piece in attackPieces:
            if board[piece[0]][piece[1]][1] == "R":
                #HORIZONTAL
                if kingAttacked[0] == piece[0]:
                    if kingAttacked[1] > piece[1]:
                        for i in range(piece[1], kingAttacked[1]):
                            if cellUnderAttack(piece[0], i, sideDefends,1):
                                return 20
                    elif kingAttacked[1] < piece[1]:
                        for i in range(piece[1], kingAttacked[1], -1):
                            if cellUnderAttack(piece[0], i, sideDefends,1):
                                return 20
                #VERTICAL
                elif kingAttacked[1] == piece[1]:
                    if kingAttacked[0] > piece[0]:
                        for i in range(piece[0], kingAttacked[0]):
                            if cellUnderAttack(i, piece[1], sideDefends,1):
                                return 20
                    elif kingAttacked[0] < piece[0]:
                        for i in range(piece[0], kingAttacked[0],-1):
                            if cellUnderAttack(i, piece[1], sideDefends,1):
                                return 20

            elif board[piece[0]][piece[1]][1] == "N":
                pass
            elif board[piece[0]][piece[1]][1] == "B":
                dif = kingAttacked[1]- kingAttacked[0]

                if checkFurther:
                    coordToCheck = []
                    for i in range(kingAttacked[0]+1, 8):
                        if 0 <= i+dif <= 7:
                            if board[i][i+dif][0] == sideDefends:
                                break
                            elif board[i][i+dif][0] == sideAttacks:
                                checkFurther = 0
                                break
                            else:
                                coordToCheck.append([i,i+dif])

                if checkFurther:
                    coordToCheck = []
                    for i in range(kingAttacked[0]-1,-1,-1):
                        if 0 <= i+dif <= 7:
                            if board[i][i+dif][0] == sideDefends:
                                break
                            elif board[i][i+dif][0] == sideAttacks:
                                checkFurther = 0
                                break
                            else:
                                coordToCheck.append([i,i+dif])

                if checkFurther:
                    coordToCheck = []
                    j = kingAttacked[0]
                    for i in range(kingAttacked[0]+1, 8):
                        j-=1
                        if 0 <= j+dif <= 7 and 0 <= i <= 7:
                            if board[i][j+dif][0] == sideDefends:
                                break
                            elif board[i][j+dif][0] == sideAttacks:
                                checkFurther = 0
                                break
                            else:
                                coordToCheck.append([i,j+dif])

                if checkFurther:
                    j = kingAttacked[0]
                    coordToCheck = []
                    for i in range(kingMoved[0], -1, -1):
                        j+=1
                        if 0 <= j+dif <= 7 and 0 <= i <= 7:
                            if board[i][j+dif][0] == sideDefends:
                                break
                            elif board[i][j+dif][0] == sideAttacks:
                                checkFurther = 0
                                break
                            else:
                                coordToCheck.append([i,j+dif])
                if coordToCheck:
                    for i in coordToCheck:
                        if cellUnderAttack(i[0], i[1], sideDefends,1):
                            return 20
                else:
                    return 0


            elif board[piece[0]][piece[1]][1] == "Q":
                #Rock part
                #HORIZONTAL
                if kingAttacked[0] == piece[0]:
                    if kingAttacked[1] > piece[1]:
                        for i in range(piece[1], kingAttacked[1]):
                            if cellUnderAttack(piece[0], i, sideDefends,1):
                                return 20
                    elif kingAttacked[1] < piece[1]:
                        for i in range(piece[1], kingAttacked[1], -1):
                            if cellUnderAttack(piece[0], i, sideDefends,1):
                                return 20
                #VERTICAL
                elif kingAttacked[1] == piece[1]:
                    if kingAttacked[0] > piece[0]:
                        for i in range(piece[0], kingAttacked[0]):
                            if cellUnderAttack(i, piece[1], sideDefends,1):
                                return 20
                    elif kingAttacked[0] < piece[0]:
                        for i in range(piece[0], kingAttacked[0],-1):
                            if cellUnderAttack(i, piece[1], sideDefends,1):
                                return 20

                #Bishop part
                dif = kingAttacked[1]- kingAttacked[0]

                if checkFurther:
                    coordToCheck = []
                    for i in range(kingAttacked[0]+1, 8):
                        if 0 <= i+dif <= 7:
                            if board[i][i+dif][0] == sideDefends:
                                break
                            elif board[i][i+dif][0] == sideAttacks:
                                checkFurther = 0
                                break
                            else:
                                coordToCheck.append([i,i+dif])

                if checkFurther:
                    coordToCheck = []
                    for i in range(kingAttacked[0]-1,-1,-1):
                        if 0 <= i+dif <= 7:
                            if board[i][i+dif][0] == sideDefends:
                                break
                            elif board[i][i+dif][0] == sideAttacks:
                                checkFurther = 0
                                break
                            else:
                                coordToCheck.append([i,i+dif])

                if checkFurther:
                    coordToCheck = []
                    j = kingAttacked[0]
                    for i in range(kingAttacked[0]+1, 8):
                        j-=1
                        if 0 <= j+dif <= 7 and 0 <= i <= 7:
                            if board[i][j+dif][0] == sideDefends:
                                break
                            elif board[i][j+dif][0] == sideAttacks:
                                checkFurther = 0
                                break
                            else:
                                coordToCheck.append([i,j+dif])

                if checkFurther:
                    j = kingAttacked[0]
                    coordToCheck = []
                    for i in range(kingMoved[0], -1, -1):
                        j+=1
                        if 0 <= j+dif <= 7 and 0 <= i <= 7:
                            if board[i][j+dif][0] == sideDefends:
                                break
                            elif board[i][j+dif][0] == sideAttacks:
                                checkFurther = 0
                                break
                            else:
                                coordToCheck.append([i,j+dif])
                if coordToCheck:
                    for i in coordToCheck:
                        if cellUnderAttack(i[0], i[1], sideDefends,1):
                            return 20
                else:
                    return 0


            else:
                #pawn does not work this way
                pass

        #checks if king can escape
        try:
            if board[kingAttacked[0]][kingAttacked[1]-1] == "em" and not cellUnderAttack(kingAttacked[0], kingAttacked[1]-1, sideAttacks):
                return 21
        except:
            pass
        try:
            if board[kingAttacked[0]][kingAttacked[1]+1] == "em" and not cellUnderAttack(kingAttacked[0], kingAttacked[1]+1, sideAttacks):
                return 21
        except:
            pass
        try:
            if board[kingAttacked[0]-1][kingAttacked[1]] == "em" and not cellUnderAttack(kingAttacked[0]-1, kingAttacked[1], sideAttacks):
                return 21
        except:
            pass
        try:
            if board[kingAttacked[0]+1][kingAttacked[1]] == "em" and not cellUnderAttack(kingAttacked[0]+1, kingAttacked[1], sideAttacks):
                return 21
        except:
            pass
        try:
            if board[kingAttacked[0]-1][kingAttacked[1]-1] == "em" and not cellUnderAttack(kingAttacked[0]-1, kingAttacked[1]-1, sideAttacks):
                return 21
        except:
            pass
        try:
            if board[kingAttacked[0]+1][kingAttacked[1]+1] == "em" and not cellUnderAttack(kingAttacked[0]+1, kingAttacked[1]+1, sideAttacks):
                return 21
        except:
            pass
        try:
            if board[kingAttacked[0]+1][kingAttacked[1]-1] == "em" and not cellUnderAttack(kingAttacked[0]+1, kingAttacked[1]-1, sideAttacks):
                return 21
        except:
            pass
        try:
            if board[kingAttacked[0]-1][kingAttacked[1]+1] == "em" and not cellUnderAttack(kingAttacked[0], kingAttacked[1]-1, sideAttacks):
                return 21
        except:
            pass

        mateMode = 0
        return 'mate'

    if moveLine[0:2] == "wK":
        if cellUnderAttack(kingWhiteCoord[0], kingWhiteCoord[1], "b"):
            board[int(moveLine[-2])][int(moveLine[-1])]= "em"
            board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0:2]
            return 22
    elif moveLine[0:2] == "bK":
        if cellUnderAttack(kingBlackCoord[0], kingBlackCoord[1], "w"):
            board[int(moveLine[-2])][int(moveLine[-1])]= "em"
            board[coordEmpty[-2]][coordEmpty[-1]]=moveLine[0:2]
            return 22
    return 1

def playGame(gameList, playToNumber=-1, whiteLast=0):
    moveWhite = 0
    moveBlack = 0
    global moveNumber, board,noBlackMove
    numberCounter = 1
    moveNumber = 0
    global errorAtMove
    errorAtMove = []
    currentNumberInLine = ''
    spaceNumber = 0
    endMoveNumber = 0
    lastMove = 0
    noBlackMove=0

    global takenWhite
    global takenBlack
    takenWhite = []
    takenBlack = []

    if playToNumber<-1:
        return 14
    else:
        for i in range(0,len(gameList)):
            try:
                temp = int(gameList[i])
                if gameList[i+1]=='.':
                    #check if numeration is correct
                    if len(str(numberCounter))==2:
                        try:
                            currentNumberInLine = gameList[i-1:i+1]
                        except:
                            return 15
                    elif len(str(numberCounter))==3:
                        try:
                            currentNumberInLine = gameList[i-2:i+1]
                        except:
                            return 15
                    elif len(str(numberCounter))==1:
                        try:
                            currentNumberInLine = gameList[i:i+1]
                        except:
                            return 15
                    else:
                        return 16
                    if int(currentNumberInLine)==numberCounter and (i-len(currentNumberInLine)==-1 or gameList[i-len(currentNumberInLine)]==' '):
                        numberCounter+=1
                    else:
                        return 15
                    #check if maximum number reached
                    if playToNumber!=-1:
                        if numberCounter==playToNumber+2:
                            return board
                    for j in range(i+1,len(gameList)):
                        if gameList[j]==' ':
                            spaceNumber = j
                            break
                        elif j==len(gameList)-1:
                            spaceNumber = j+1
                            noBlackMove = 1
                    if ((playToNumber==-1 and not str(numberCounter-1) in gameList[i:]) or (playToNumber!=-1 and numberCounter==playToNumber+1)) and whiteLast:
                        noBlackMove = 1
                    if not noBlackMove:
                        lastMove = 1
                        for j in range(spaceNumber+1,len(gameList)):
                            if gameList[j]==' ':
                                lastMove = 0
                                endMoveNumber = j-1
                                break
                        if lastMove:
                            endMoveNumber = len(gameList)-1
    #                print '*'+gameList[i+1:spaceNumber]+'*', '*'+gameList[spaceNumber:endMoveNumber+1]+'*'
                    moveNumber += 1

                    moveWhite = changePosition(gameList[i+1:spaceNumber])
                    if moveWhite != 1:
                        print 'ERROR AT MOVE:', moveNumber
                        #print gameList[:i-2]
                        errorAtMove = [moveNumber,"w"]
                        print errorAtMove
                        return moveWhite
                        break

                    if not noBlackMove:
                        moveBlack = changePosition(gameList[spaceNumber:endMoveNumber+1])
                        if moveBlack != 1:
                            errorAtMove = [moveNumber,"b"]
                            print errorAtMove
                            return moveBlack
                            break

                    else:
                        return board
                    spaceNumber = 0
                    endMoveNumber = 0

            except:
                pass
        if moveWhite !=1 or moveBlack != 1:
            print 'ERROR AT MOVE:', gameList[i-1:]
            return 0
        return board

def createStartPosition():
    """Creating a start position"""
    global board
    global startBoard
    board = []
    for i in range(8):
                board.append([])
                for j in range(8):
                    board[i].append('em')

    board[0][0] = board[0][-1] = "bR"
    board[0][1] = board[0][-2] = "bN"
    board[0][2] = board[0][-3] = "bB"
    board[0][3] =  "bQ"
    board[0][4] =  "bK"
    for i in range(8):
        board[1][i] = "bP"
        board[-2][i] = "wP"

    board[-1][0] = board[-1][-1] = "wR"
    board[-1][1] = board[-1][-2] = "wN"
    board[-1][2] = board[-1][-3] = "wB"
    board[-1][3] =  "wQ"
    board[-1][4] =  "wK"

    startBoard = board
    return board

def showBoard(coord = 0):
    """ prints function in console.
        coord = TRUE : prints coordinates
        coord = FALSE: prints without coordinates
    """
    global board
    print
    if not coord:
        for i in range(8):
            for j in range(8):
                if board[i][j] == "em":
                    print "..",
                else:
                    print board[i][j],
            print
    else:
        coord = ['1','2','3','4','5','6','7','8']
        for i in range(8):
            print coord[7-i], "|",
            for j in range(8):
                if board[i][j] == "em":
                    print "..",
                else:
                    print board[i][j],
            print
        print "    -----------------------"
        print "    a  b  c  d  e  f  g  h"

def readFileLine(fileName):
    #TO DO:
    #RESULT LINE CHECK!!!!!!!!
    #WHAT IS THE _MOVE_ OF COMMENT, NO LINE!!!
    comments = []
    gameLine = ''
    countLine = 1
#    print os.path.isfile(fileName)
    if os.path.isfile(fileName):
        fileIn = open(fileName,"r")
        for line in fileIn:
        #    print line
            #Additional information part:
            if line[0]=='[':
                if line[len(line)-2]==']':
                    print line[1:len(line)-2]
                else:
                    print 'ERROR IN LINE',countLine,'WITH ADD. INFORMATION'
                    fileIn.close()
                    return 'ERROR'
            #main part:
            else:
                #line with result:
                if '-' in line and (line[line.find('-')-1]!='O' or line[line.find('-')+1]!='O') and not ('{' in line or '}' in line):
                    print 'RESULT:',line
                    print 'Comments:',comments

                    resultTemp = ''
                    if line.find('1/2-1/2')!=-1:
                        resultTemp = '1/2-1/2'
                    elif line.find('1-0')!=-1:
                        resultTemp = '1-0'
                    else:
                        resultTemp = '0-1'
                    fileIn.close()

                    gameLine += line[:line.find(resultTemp)-1]                    
                    gameLine = clearLine(gameLine)
                    
                    print gameLine
                    return gameLine
                else:
                    #comments in line, cut it:
                    commentCut = 0
                    while not commentCut:
                        if '{' in line:
                            if '}' in line and line.find('{')<line.find('}'):
                                comments += [str(countLine)+':'+line[line.find('{')+1:line.find('}')]]
                                print 'c',comments
                                a = line[line.find('{'):line.find('}')+1]
                                line = line.replace(a,'')
                            else:
                                print 'ERROR IN LINE',countLine,'WITH COMMENTS'
                                fileIn.close()
                                return 'ERROR'
                        else:
                            commentCut = 1
                    gameLine += line[0:len(line)-1]
            countLine += 1
        fileIn.close()
        #print comments
        #print gameLine
        gameLine = clearLine(gameLine)
        return gameLine
    else:
        print "FILE COULD NOT BE OPENED"
        return 'ERROR'


def clearLine(line):
    global gameLineCorrected
    gameLineCorrected = 0

    gameLine = line

    while gameLine[-1]==' ':
        gameLine = gameLine[:-1]

    #clear *
    if gameLine[-1]=='*':
        gameLine = gameLine[:-1]
    while gameLine[-1]==' ':
        gameLine = gameLine[:-1]

    lineCleared = False
    #clear double spaces
    while not lineCleared:
        lenx = len(gameLine)
        lineCleared = True
        for i in range(0,lenx):
            if i!=0 and gameLine[i-1]==' ' and gameLine[i]==' ':
                gameLineCorrected = 1
                gameLine = gameLine[:i-1]+gameLine[i:lenx]
                lineCleared = False
                break
    #clear not allowed symbols
    lineCleared = False
    allowedSymbols = ['a','b','c','d','e','f','g','h','1','2','3','4','5','6','7','8','9','0','=','P','N','B','R','Q','K','+','#',' ','.','x','-','O']

    while not lineCleared:
        lenx = len(gameLine)
        lineCleared = True
        for i in range(0,lenx):
            if gameLine[i] not in allowedSymbols:
                gameLineCorrected = 1
                gameLine = gameLine[:i]+gameLine[i+1:]
                lineCleared = False
                break

    #clear moves after checkmate
    if gameLine.find('#')>0 and gameLine.find('#')!=len(gameLine)-1:
        gameLine = gameLine[:gameLine.find('#')+1]
        gameLineCorrected = 1

    return gameLine


def readInfoFromFile(fileName):
    info = {}
    if os.path.isfile(fileName):
        fileIn = open(fileName,"r")
        for line in fileIn:
        #    print line
            #Additional information part:
            if line[0]=='[':
                info[line[1:line.find(" ")]] = line[line.find(" ")+2:-3]
        return info
    else:
        print "FILE COULD NOT BE OPENED"
        return 'ERROR'

def clearAll():
    global board, castleWhite, castleBlack, kingWhiteMoved, kingBlackMoved, rockKingWhiteMoved, rockQueenWhiteMoved
    global rockKingBlackMoved, rockQueenBlackMoved, moveNumber, checkMode, mateMode, kingWhiteCoord, kingBlackCoord, promotionMode, passingMoveAvailable
    global takenWhite, takenBlack

    castleWhite = 0 # 1 when white has already done castle
    castleBlack = 0 # 1 when black has already done castle
    kingWhiteMoved = 0 # using it in castles if white king moved = 1 hasn't moved = 0
    kingBlackMoved = 0 # using it in castles if black king moved = 1 hasn't moved = 0
    rockKingWhiteMoved = 0  # rocked (KING-SIDE WHITE) has made a move
    rockQueenWhiteMoved = 0 # rocked (QUEEN-SIDE WHITE)has made a move
    rockKingBlackMoved = 0  # rocked (KING-SIDE BLACK) has made a move
    rockQueenBlackMoved = 0  # rocked (QUEEN-SIDE WHITE)has made a move
    moveNumber = 0 # number of current Move
    checkMode = 0 # state of check
    mateMode = 0 # state of mate
    kingWhiteCoord = [7,4] # initial coordinates of white king
    kingBlackCoord = [0,4] # initial coordinates of black king
    promotionMode = ''
    passingMoveAvailable = ''
    takenWhite = []
    takenBlack = []
