from inc.chessengine import *
from Tkinter import *
import Pmw
from tkMessageBox import showinfo
from PIL.ImageTk import PhotoImage
from tkFileDialog import askopenfilename

__author__="Hollgam and Vinchkovsky"
__description__="A reader for PGN files."
__version__="1.0"

###VARS
stopOnWhite = 1
firstMove = 1
maxNumber = -1
tempCounter = 0


### end of VARS

class PGN_GUI(Frame):

    def __init__(self):

        Frame.__init__(self)
        Pmw.initialise()

        self.lightColor = ""
        self.darkColor = ""
        self.lastMoveColor1 = "#FBF4A1"
        self.lastMoveColor2 = "#E9DC42"
        self.colorSelected = "#eff6b2"
        self.takenPiecesBackground = "white"
        self.sideBarWidth = 220
        self.boardFliped  = 0
        self.currentPosition = createStartPosition()
        self.notesFile = 0
        self.notesImported = 0
        self.firstTimeLoaded = 1
        self.font1 = "14"
        self.font2 = "Helvetica 9"
        self.infoRightFont = "Helvetica 9 bold"
        self.infoLeftFont = "Helvetica 9"
        self.boardSize = 'Default'
        self.numberOfSet = '2'
        self.boardColor = 'Brown'
        self.showLastMove = 'Yes'
        self.loadConfig()

        self.prevButton = Button()
        self.keyWidthx=13
        self.takenPiecesWhiteImages = []
        self.takenPiecesBlackImages = []
        self.infoLabelsData = []
        self.doFurther = 1

        self.noBlackLastMove = 0
        self.noBlackMove2 = 0

        self.middleListPos = 7
        self.buttonHC = 1.0

        self.gameLine = "1."
        #self.gameInfo = {'White': '', 'WhiteElo': '', 'Black': '', 'BlackElo': '', 'Event': '', 'Site': '', 'Date': '', 'TimeControl': '', 'Round': '', 'Result': '', 'Termination': ''}
        self.gameInfoKeys = ['White', 'Black', 'WhiteElo', 'BlackElo', 'Event', 'Site', 'Date', 'TimeControl', 'Round', 'Result', 'Termination']
        #self.gameInfoKeys.sort()

        try:
#            self.imageEmpty = PhotoImage(file = "img/set1/default/empty.gif")
#            self.imageWhiteRock = PhotoImage(file = "img/set1/default/wr.png")
#            self.imageBlackRock = PhotoImage(file = "img/set1/default/br.png")
#            self.imageWhiteBishop = PhotoImage(file = "img/set1/default/wb.png")
#            self.imageBlackBishop = PhotoImage(file = "img/set1/default/bb.png")
#            self.imageWhiteKnight = PhotoImage(file = "img/set1/default/wn.png")
#            self.imageBlackKnight = PhotoImage(file = "img/set1/default/bn.png")
#            self.imageWhiteQueen = PhotoImage(file = "img/set1/default/wq.png")
#            self.imageBlackQueen = PhotoImage(file = "img/set1/default/bq.png")
#            self.imageWhiteKing = PhotoImage(file = "img/set1/default/wk.png")
#            self.imageBlackKing = PhotoImage(file = "img/set1/default/bk.png")
#            self.imageWhitePawn = PhotoImage(file = "img/set1/default/wp.png")
#            self.imageBlackPawn = PhotoImage(file = "img/set1/default/bp.png")

            self.imageTakenWhiteRock = PhotoImage(file = "img/set1/taken/wr.png")
            self.imageTakenBlackRock = PhotoImage(file = "img/set1/taken/br.png")
            self.imageTakenWhiteBishop = PhotoImage(file = "img/set1/taken/wb.png")
            self.imageTakenBlackBishop = PhotoImage(file = "img/set1/taken/bb.png")
            self.imageTakenWhiteKnight = PhotoImage(file = "img/set1/taken/wn.png")
            self.imageTakenBlackKnight = PhotoImage(file = "img/set1/taken/bn.png")
            self.imageTakenWhiteQueen = PhotoImage(file = "img/set1/taken/wq.png")
            self.imageTakenBlackQueen = PhotoImage(file = "img/set1/taken/bq.png")
            self.imageTakenWhitePawn = PhotoImage(file = "img/set1/taken/wp.png")
            self.imageTakenBlackPawn = PhotoImage(file = "img/set1/taken/bp.png")
        except:
            print "Falied to load files from \\img\\set1 folder"

        try:
            self.imageLogo = PhotoImage(file = "img/logo/gcodelogo.png")
        except:
            print "Falied to load images from \\img\\logo folder"


        self.master.bind("<Control-Key-O>", self.loadGame)
        self.master.bind("<Control-Key-o>", self.loadGame)
        self.master.bind("<Control-Key-Q>", self.closeGame)
        self.master.bind("<Control-Key-q>", self.closeGame)

        self.pack(expand=YES, fill=BOTH)
        self.master.resizable(0, 0)
        self.master.title('PyGN')
        self.master.iconbitmap('img/favicon.ico')


        # HEADER
        self.headerFrame = Frame(self)
        self.headerFrame.grid(column=0 , row=0, sticky = W+N)
        self.myBalloon = Pmw.Balloon(self)
        self.choices = Pmw.MenuBar(self.headerFrame, balloon=self.myBalloon)
        self.choices.pack(side=LEFT, fill=X)

        # create File menu and items
        self.choices.addmenu("Game", "Game")
        self.choices.addmenuitem("Game", "command", "Load new File", command=self.loadGame, label="Load")
        self.choices.addmenuitem("Game", "command", "Close current game", command=self.closeGame, label="Close")
        self.choices.addmenuitem("Game", 'separator')
        self.choices.addmenuitem("Game", "command", "Exit this game", command=self.exitGame, label="Exit")

        self.choices.addmenu("View", "Change the way it looks")
        #flip board
        self.choices.addmenuitem("View", "command", "Flip board", command=self.flipBoard, label="Flip board")

        self.choices.addcascademenu("View", "Show Sidebar")
        self.selectedShowSidebar = StringVar()
        self.selectedShowSidebar.set("Yes")
        self.choices.addmenuitem("Show Sidebar", "radiobutton", label="Yes", variable=self.selectedShowSidebar, command=self.changeShowSidebar)
        self.choices.addmenuitem("Show Sidebar", "radiobutton", label="No", variable=self.selectedShowSidebar, command=self.changeShowSidebar)

        # create Options menu and items
        self.choices.addmenu("Options", "Twik this program")


        #color scheme
        self.choices.addcascademenu("Options", "Pieces Style")
        self.selectedColorScheme = StringVar()
        self.selectedColorScheme.set("Set "+self.numberOfSet)
        self.choices.addmenuitem("Pieces Style", "radiobutton", label="Set 1", variable=self.selectedColorScheme, command=self.changeColorScheme)
        self.choices.addmenuitem("Pieces Style", "radiobutton", label="Set 2", variable=self.selectedColorScheme, command=self.changeColorScheme)

        #board color
        self.choices.addcascademenu("Options", "Board colors")
        self.selectedBoardColor = StringVar()
        self.selectedBoardColor.set(self.boardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Brown", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Light", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Green", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Blue", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Grey", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Red", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Orange", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Pink", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Purple", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Tan", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Black & White", variable=self.selectedBoardColor, command=self.changeBoardColor)
        self.choices.addmenuitem("Board colors", "radiobutton", label="Winboard", variable=self.selectedBoardColor, command=self.changeBoardColor)

        #board size
        self.choices.addcascademenu("Options", "Board size")
        self.selectedBoardSize = StringVar()
        self.selectedBoardSize.set(self.boardSize)
        self.choices.addmenuitem("Board size", "radiobutton", label="Small", variable=self.selectedBoardSize, command=self.changeBoardSize)
        self.choices.addmenuitem("Board size", "radiobutton", label="Default", variable=self.selectedBoardSize, command=self.changeBoardSize)
        self.choices.addmenuitem("Board size", "radiobutton", label="Large", variable=self.selectedBoardSize, command=self.changeBoardSize)

        #self.choices.addmenuitem("Options", 'separator')
        # add items to Options/ShowLastMove
        self.choices.addcascademenu("Options", "Show last move")
        self.selectedShowLastMove = StringVar()
        self.selectedShowLastMove.set(self.showLastMove)
        self.choices.addmenuitem("Show last move", "radiobutton", label="Yes", variable=self.selectedShowLastMove, command=self.changeShowLastMove)
        self.choices.addmenuitem("Show last move", "radiobutton", label="No", variable=self.selectedShowLastMove, command=self.changeShowLastMove)

        self.choices.addmenuitem("Options", 'separator')
        self.choices.addmenuitem("Options", "command", "Make everything default", command=self.defaultAll, label="Default all")


#        # add items to Options/ShowNextMove
#        self.choices.addcascademenu("Options", "Show next move")
#        self.selectedShowNextMove = StringVar()
#        self.selectedShowNextMove.set("No")
#        self.choices.addmenuitem("Show next move", "radiobutton", label="Yes", variable=self.selectedShowNextMove, command=self.changeShowNextMove)
#        self.choices.addmenuitem("Show next move", "radiobutton", label="No", variable=self.selectedShowNextMove, command=self.changeShowNextMove)

#        # add items to Options/ShowLegalMoves
#        self.choices.addcascademenu("Options", "Show legal moves")
#        self.selectedShowLegalMoves = StringVar()
#        self.selectedShowLegalMoves.set("No")
#        self.choices.addmenuitem("Show legal moves", "radiobutton", label="Yes", variable=self.selectedShowLegalMoves, command=self.changeShowLegalMoves)
#        self.choices.addmenuitem("Show legal moves", "radiobutton", label="No", variable=self.selectedShowLegalMoves, command=self.changeShowLegalMoves)

        self.choices.addmenu("Help", "Help")
        self.choices.addmenuitem("Help", "command", command=self.showAbout, label="About")
        self.choices.addmenuitem("Help", "command", command=self.showKeys, label="Keyboard shortcuts")

        self.changeColorScheme(1)
        self.changeBoardColor(1)

        self.mainFrame = Frame(self)
        self.mainFrame.grid(column=0, row=1)

        self.frame1 = Frame(self.mainFrame)
        self.frame1.pack()

        self.buttonsFrame = Frame(self.mainFrame)
        self.createBoard()

        self.KeyWidth=12

        self.frame2 = Frame(self.mainFrame)
        self.frame2.pack(side = RIGHT, fill=BOTH, expand = YES)

        self.KeyStart = Button(self.frame2,text='|<',name='start',command = self.showStartPosition, state = DISABLED)
        self.KeyStart.pack(side=LEFT, fill=BOTH, expand=1)

        self.KeyBack5 = Button(self.frame2,text='<<',name='back5',command = self.moveBack5, state = DISABLED)
        self.KeyBack5.pack(side=LEFT, fill=BOTH, expand=1)

        self.KeyBack = Button(self.frame2,text='<',name='back',command = self.moveBack, state = DISABLED)
        self.KeyBack.pack(side=LEFT, fill=BOTH, expand=1)

        self.KeyForward = Button(self.frame2,text='>',name='forward', command = self.moveForward, state = DISABLED)
        self.KeyForward.pack(side=LEFT, fill=BOTH, expand=1)

        self.KeyForward5 = Button(self.frame2,text='>>',name='forward5', command = self.moveForward5, state = DISABLED)
        self.KeyForward5.pack(side=LEFT, fill=BOTH, expand=1)

        self.KeyEnd = Button(self.frame2,text='>|',name='load',command = self.showLastPosition, state = DISABLED)
        self.KeyEnd.pack(side=LEFT, fill=BOTH, expand=1)



        # Create and pack the NoteBook.
#        self.notebook = Pmw.NoteBook(self)
#        self.notebook.grid(column=1 , row=1,sticky=NW, rowspan=2)

        if self.selectedBoardSize.get() == "Small":
            notebookHeight = 344
            sidebarHeight = 310
            listHeight = 195
            infoHeight = 298
        elif self.selectedBoardSize.get() == "Default":
            notebookHeight = 464
            sidebarHeight = 430
            listHeight = 315
            infoHeight = 418
        elif self.selectedBoardSize.get() == "Large":
            notebookHeight = 584
            sidebarHeight = 550
            listHeight = 435
            infoHeight = 538

        self.notebookFrame = Frame(self, width=self.sideBarWidth+11, height=notebookHeight)
        self.notebookFrame.grid(column=1 , row=1,sticky=NW, rowspan=2)
        self.notebookFrame.grid_propagate(False)
        self.notebook = Pmw.NoteBook(self.notebookFrame)
        self.notebook.grid(column=0 , row=0,sticky=NW)

        # Add the "Appearance" page to the notebook.
        self.movePage = self.notebook.add('Moves   ')

        self.sideBar = Frame(self.movePage, width=self.sideBarWidth, height=sidebarHeight)
        self.sideBar.grid(column=1 , row=1,sticky=NW, rowspan=2)
        self.sideBar.grid_propagate(False)

        #LIST OF MOVES
        self.moveListFrame = Frame(self.sideBar)
        self.moveListFrame.grid(row=0,column=0,sticky=NW)
        self.vscrollbar = Scrollbar(self.moveListFrame)
        self.vscrollbar.grid(row=0, column=1, sticky=N+S, pady=4)
        self.listCanvas = Canvas(self.moveListFrame,yscrollcommand=self.vscrollbar.set,height=listHeight ,width=196)
        self.listCanvas.grid(row=0, column=0, sticky=N+S+E+W, pady=4)
        self.vscrollbar.config(command=self.listCanvas.yview)
        self.frameList = Frame(self.listCanvas)
        self.listCanvas.create_window(0, 0, anchor=NW, window=self.frameList)
        self.frameList.update_idletasks()
        self.listCanvas.config(scrollregion=self.listCanvas.bbox("all"))

        #FRAME SHOWING TAKEN PIECES
        self.numberWhiteTaken = 0
        self.numberBlackTaken = 0
        self.takenPiecesContainer =  Frame(self.sideBar, bg = "black", width=self.sideBarWidth-8, height=102)
        self.takenPiecesContainer.grid(row=1,column=0,sticky=W, padx=4)

        self.takenPiecesFrame = Frame(self.takenPiecesContainer, bg = self.takenPiecesBackground, width=self.sideBarWidth-8, height=100)
        self.takenPiecesFrame.grid(row=0,column=0,sticky=W, padx=1, pady=1)
        self.takenPiecesFrame.grid_propagate(False)

#        self.tekenPiecesHeader = Label(self.takenPiecesFrame, text = "           Taken pieces:", font=14, bg=self.takenPiecesBackground)
#        self.tekenPiecesHeader.grid(row=0,column=0, columnspan = 7, sticky=W, padx=1)
        self.showTakenPieces()



        #INFO ABOUT GAME
        self.infoPage = self.notebook.add('Info      ')

        self.infoFrame = Frame(self.infoPage)
        self.infoFrame.grid(row=0,column=0,sticky=NW)
        self.vscrollbarInfo = Scrollbar(self.infoFrame)
        self.vscrollbarInfo.grid(row=0, column=1, sticky=N+S, pady=4)
        self.canvasInfo = Canvas(self.infoFrame,yscrollcommand=self.vscrollbarInfo.set,height=infoHeight ,width=196)
        self.canvasInfo.grid(row=0, column=0, sticky=N+S+E+W, pady=4)
        self.vscrollbarInfo.config(command=self.canvasInfo.yview)
        self.infoList = Frame(self.canvasInfo)
        self.canvasInfo.create_window(0, 0, anchor=NW, window=self.infoList)
        self.infoList.update_idletasks()
        self.canvasInfo.config(scrollregion=self.canvasInfo.bbox("all"))

        self.noInfoLabel = Label(self.infoList, text = "Load game to see info about it.", font=self.infoLeftFont)
        self.noInfoLabel.grid(row=0,column=0, sticky=W, padx=1)

        #LIST OF GAMES
        self.gamesPage = self.notebook.add('Games   ')
        self.gamesList = Pmw.ScrolledListBox(self.gamesPage,dblclickcommand=self.gameListClick)
        self.gamesList.pack(side = TOP, expand = YES, fill = BOTH)

        self.loadItem = Button(self.gamesPage,text='Load game',command=self.gameListClick).pack(side=LEFT, fill=BOTH, expand=1)
        self.deleteItem = Button(self.gamesPage,text='Delete game',command=self.deleteMLItem).pack(side=LEFT, fill=BOTH, expand=1)
        self.clearItem = Button(self.gamesPage,text='Clear all',command = self.clearMoveList).pack(side=LEFT, fill=BOTH, expand=1)

        self.loadGamesList()
#        self.fileDic = {} #dictionary for files, format: info about file:path
        self.fileToLoad = ''
        self.notebook.tab('Games   ').focus_set()
        self.notebook.selectpage('Games   ')

        #NOTES
        self.notesPage = self.notebook.add('Notes   ')

        entryFont = Pmw.logicalfont('Fixed')
        self.textEntry = Pmw.ScrolledText( self.notesPage, text_width = 10, text_height = 12, text_wrap = WORD,hscrollmode = "none", vscrollmode = "static", text_font = entryFont)
        self.textEntry.pack( side = TOP, expand = YES, fill = BOTH)
#        self.buttonLoadNotes = Button(self.infoPage,text='Load',name='loadNotes',command = self.loadNotes, state = ACTIVE)
#        self.buttonLoadNotes.pack(side=LEFT, fill=BOTH, expand=1)
        self.buttonSaveNotes = Button(self.notesPage,text='Save',name='saveNotes',command = self.saveNotes, state = DISABLED)
        self.buttonSaveNotes.pack(side=LEFT, fill=BOTH, expand=1)
        self.buttonClearNotes = Button(self.notesPage,text='Clear',name='clearNotes',command = self.clearNotes, state = DISABLED)
        self.buttonClearNotes.pack(side=LEFT, fill=BOTH, expand=1)

        self.notebook.setnaturalsize()

        #self.changeBoardSize()
        #self.changeShowLastMove()

    def loadConfig(self):
        cfgName = 'pygn.cfg'
        if os.path.isfile(cfgName):
            cfgFile = open(cfgName,'r')
            for line in cfgFile:
                if line[:2]=='bc':
                    self.boardColor = line[3:line.find('*')]
                elif line[:2]=='lm':
                    self.showLastMove = line[3:line.find('*')]
                elif line[:2]=='f1':
                    self.font1 = line[3:line.find('*')]
                elif line[:2]=='f2':
                    self.font2 = line[3:line.find('*')]
                elif line[:2]=='rf':
                    self.infoRightFont = line[3:line.find('*')]
                elif line[:2]=='lf':
                    self.infoLeftFont = line[3:line.find('*')]
                elif line[:2]=='bf':
                    try:
                        self.boardFliped = int(line[3:line.find('*')])
                    except:
                        pass
                elif line[:2]=='sz':
                    self.boardSize = line[3:line.find('*')]
                elif line[:2]=='ps':
                    self.numberOfSet = line[3:line.find('*')]


    def changeConfig(self,par,value):
        cfgName = 'pygn.cfg'
        itemsList = []
        if os.path.isfile(cfgName):
            cfgFile = open(cfgName,'r')
            for line in cfgFile:
                if line[:2]==par:
                    line=line[:3]+value+line[line.find('*'):]
                itemsList += [line]
            cfgFile.close()
            cfgFile = open(cfgName,'w')
            for cline in itemsList:
                cfgFile.write(cline)

    def loadGamesList(self):
        self.fileDic = {}
        self.fileDicRev = {}
        self.fileListName = "files.list"
        self.filesList = []
        if os.path.isfile(self.fileListName):
            #READ
            fileIn = open(self.fileListName,"r")
            for line in fileIn:
                self.filesList += [line]
            #clear list
            allClear = 0
            while not allClear:
                allClear = 1
                for file in self.filesList:
                    if not os.path.isfile(file[0:file.find('#')]):
                        print "remove",file
                        self.filesList.remove(file)
                        allClear = 0
            #add items to file list
            for item in self.filesList:
                item = item.replace('\n','')
                self.gamesList.insert(END,item[item.find("#")+1:])
                self.fileDic[item[item.find("#")+1:]]=item[:item.find("#")]
                self.fileDicRev[item[:item.find("#")]]=item[item.find("#")+1:]
            fileIn.close()
            #WRITE
            fileIn = open(self.fileListName,"w")
            for line in self.filesList:
                line = line.replace('\n','')
                fileIn.write(line+'\n')
            fileIn.close()
        else:
            print "FILE COULD NOT BE OPENED"
            return 'ERROR'

    def gameListClick(self):
        for line in self.gamesList.getcurselection():
            self.loadGame(self.fileDic[line])
            break


    def deleteMLItem(self):
        try:
            current = self.gamesList.getcurselection()[0]
            fileIn = open(self.fileListName,"w")
            #filter
            for line in self.filesList:
                if line.find(current[:-2])>0:
                    self.filesList.remove(line)
            #write
            for line in self.filesList:
                line = line.replace('\n','')
                fileIn.write(line+'\n')
            fileIn.close()

            self.gamesList.clear()
            self.loadGamesList()
        except:
            pass

    def clearMoveList(self):
        fileIn = open(self.fileListName,"w")
        fileIn.write('')
        fileIn.close()
        self.gamesList.clear()
        self.loadGamesList()


    def createBoard(self):
        self.buttons = []
        color =0
        from inc.chessengine import moveNumber

        global lastPosition1
        global lastPosition2
        for i in range(8):
            self.buttons.append([])
            for j in range(8):
                if not color:
                    bgcolor = self.lightColor
                else:
                    bgcolor = self.darkColor
                buttonName = str(i) + "/" + str(j) + "/" + bgcolor
                self.buttons[-1] += [Label(self.buttonsFrame, name=buttonName, bd=1, background = bgcolor)]
                self.buttons[-1][-1].bind("<Button-1>", self.cellClicked)
                self.buttons[-1][-1].grid(column=j, row=i)
                if not color:
                    color = 1
                else:
                    color = 0
            if not color:
                color = 1
            else:
                color = 0

        #Black pieces
        self.buttons[0][-1].config(image = self.imageBlackRock)
        self.buttons[0][0].config(image = self.imageBlackRock)
        self.buttons[0][-2].config(image = self.imageBlackKnight)
        self.buttons[0][1].config(image = self.imageBlackKnight)
        self.buttons[0][-3].config(image = self.imageBlackBishop)
        self.buttons[0][2].config(image = self.imageBlackBishop)
        self.buttons[0][3].config(image = self.imageBlackQueen)
        self.buttons[0][4].config(image = self.imageBlackKing)
        for i in range(8):
            self.buttons[1][i].config(image = self.imageBlackPawn)

        #Empty cells
        for i in range(2,6):
            for j in range(8):
                self.buttons[i][j].config(image = self.imageEmpty)

        #White pieces

        self.buttons[-1][-1].config(image = self.imageWhiteRock)
        self.buttons[-1][0].config(image = self.imageWhiteRock)
        self.buttons[-1][-2].config(image = self.imageWhiteKnight)
        self.buttons[-1][1].config(image = self.imageWhiteKnight)
        self.buttons[-1][-3].config(image = self.imageWhiteBishop)
        self.buttons[-1][2].config(image = self.imageWhiteBishop)
        self.buttons[-1][3].config(image = self.imageWhiteQueen)
        self.buttons[-1][4].config(image = self.imageWhiteKing)
        for i in range(8):
            self.buttons[-2][i].config(image = self.imageWhitePawn)

        if self.selectedShowLastMove.get() == "Yes":
            try:
                if not self.boardFliped:
                    self.buttons[lastPosition1[0]][lastPosition1[1]].config(background = self.lastMoveColor1)
                    self.buttons[lastPosition2[0]][lastPosition2[1]].config(background = self.lastMoveColor2)
                if self.boardFliped:
                    self.buttons[-lastPosition1[0]-1][-lastPosition1[1]-1].config(background = self.lastMoveColor1)
                    self.buttons[-lastPosition2[0]-1][-lastPosition2[1]-1].config(background = self.lastMoveColor2)
            except:
                pass
            if moveNumber == 0:
                if lastPosition1 in [[0,0], [0,2], [0,4], [0,6], [1,1], [1,3], [1,5], [1,7], [2,0], [2,2], [2,4], [2,6], [4,0], [4,2], [4,4], [4,6], [6,0], [6,2], [6,4], [6,6], [3,1], [3,3], [3,5], [3,7], [5,1], [5,3], [5,5], [5,7], [7,1], [7,3], [7,5], [7,7]]:
                    default1 = self.lightColor
                else:
                    default1 = self.darkColor

                if lastPosition2 in [[0,0], [0,2], [0,4], [0,6], [1,1], [1,3], [1,5], [1,7], [2,0], [2,2], [2,4], [2,6], [4,0], [4,2], [4,4], [4,6], [6,0], [6,2], [6,4], [6,6], [3,1], [3,3], [3,5], [3,7], [5,1], [5,3], [5,5], [5,7], [7,1], [7,3], [7,5], [7,7]]:
                    default2 = self.lightColor
                else:
                    default2 = self.darkColor
                try:
                    if not self.boardFliped:
                        self.buttons[lastPosition1[0]][lastPosition1[1]].config(background = default1)
                        self.buttons[lastPosition2[0]][lastPosition2[1]].config(background = default2)
                    if self.boardFliped:
                        self.buttons[-lastPosition1[0]-1][-lastPosition1[1]-1].config(background = default1)
                        self.buttons[-lastPosition2[0]-1][-lastPosition2[1]-1].config(background = default2)

                except:
                    pass
        self.buttonsFrame.pack()




    def cellClicked(self, event ):
        pass

    def showLastPosition(self,firstTime=0, event= None):
        global maxNumber, stopOnWhite
        from inc.chessengine import board, moveNumber
        createStartPosition()

        if self.gameLine != 'ERROR':
            clearAll()
            lastPosition = playGame(self.gameLine)
            from inc.chessengine import errorAtMove
            if firstTime:
                from inc.chessengine import noBlackMove
                self.noBlackMove2=noBlackMove
                print "noBlackMove:",noBlackMove

            if type(lastPosition) != type(1):
                self.changeImages(lastPosition)
                from inc.chessengine import moveNumber
            else:
                self.invalidMove(lastPosition)

            from inc.chessengine import moveNumber
            maxNumber = moveNumber
            stopOnWhite = 1-self.noBlackMove2

            if firstTime and type(lastPosition) != type(1):
                self.loadMoveList()

            if type(lastPosition) == type(1):
                self.listCanvas.yview(MOVETO,((maxNumber-self.middleListPos-1)*2+stopOnWhite)*self.buttonHC)
            else:
                self.listCanvas.yview(MOVETO,1.0)

            if not firstTime:
                self.prevButton.config(background=self.listCanvas["background"])

            self.buttonsDic[(maxNumber,not self.noBlackLastMove)].config(background=self.colorSelected)
            self.prevButton=self.buttonsDic[(maxNumber,not self.noBlackLastMove)]

    def loadMoveList(self):
        global maxNumber, stopOnWhite
        rows = maxNumber
        self.noBlackLastMove = 0
        self.buttonHC = 1/(2.0*maxNumber)
        self.vscrollbar.config(command=self.listCanvas.yview)
        self.frameList = Frame(self.listCanvas)
        self.listCanvas.create_window(0, 0, anchor=NW, window=self.frameList)
        self.frameList.update_idletasks()

        self.listCanvas.config(scrollregion=self.listCanvas.bbox("all"))

        self.buttonsDic = {}
        for i in range(1,rows+1):
            for j in range(1,4):
                if j==1:
                    self.label = Label(self.frameList,text=str(i))
                    self.label.grid(row=i,column=j)
                else:
                    if j==2:
                        posPoint = self.gameLine.find(" "+str(i)+".")+2+len(str(i))
                        posSpace = self.gameLine.find(" ",posPoint)
                        if posSpace == -1:
                            posSpace = len(self.gameLine)
                            self.noBlackLastMove = 1
                        self.button = Button(self.frameList, width=self.keyWidthx, text=self.gameLine[posPoint:posSpace], name=str(i)+"0",relief=GROOVE)
                        self.button.bind("<Button-1>",self.changePositionList)
                        self.button.grid(row=i, column=j, sticky='news')

                        self.buttonsDic[(i, j-2)] = self.button

                    elif j==3:
                        posEnd = self.gameLine.find(" "+str(i+1)+".", posSpace)
                        if i==maxNumber:
                            posEnd = len(self.gameLine)
                        if not self.noBlackLastMove:
                            self.button = Button(self.frameList, width=self.keyWidthx, text=self.gameLine[posSpace+1:posEnd], name=str(i)+"1",relief=GROOVE)
                            self.button.grid(row=i, column=j, sticky='news')
                            self.button.bind("<Button-1>",self.changePositionList)
                            self.buttonsDic[(i, j-2)] = self.button

        self.listCanvas.create_window(0, 0, anchor=NW, window=self.frameList)
        self.frameList.update_idletasks()
        self.listCanvas.config(scrollregion=self.listCanvas.bbox("all"))

        self.buttonsDic[(1, 0)].update()
        self.middleListPos = int(round(int(self.listCanvas["height"])/(2.0*self.buttonsDic[(1, 0)].winfo_height())))

    def changePositionList(self,event):
        global stopOnWhite
        moveN = int(event.widget.winfo_name()[:len(event.widget.winfo_name())-1])
        color = event.widget.winfo_name()[-1]
        self.prevButton.config(background=self.listCanvas["background"])
        event.widget.config(background=self.colorSelected)
        self.prevButton=event.widget
        print moveN,color

        createStartPosition()
        if self.gameLine != 'ERROR':
            clearAll()
            if color=="0":
                stopOnWhite=1
            if color=="1":
                stopOnWhite=0
            changes = playGame(self.gameLine,moveN,stopOnWhite)
            if type(changes) != type(1):
                self.changeImages(changes)
            else:
                self.invalidMove(changes)
            stopOnWhite = not stopOnWhite


    def showStartPosition(self, event= None):
        global stopOnWhite
        from inc.chessengine import board, moveNumber
        self.currentPosition = board
        createStartPosition()
        clearAll()
        changes = playGame(self.gameLine , 0, 0)
        stopOnWhite = 1
        self.changeImages(changes)
        self.listCanvas.yview(MOVETO,0.0)
        self.prevButton.config(background=self.listCanvas["background"])


    def moveBack(self, event= None):
        global stopOnWhite, tempCounter
        from inc.chessengine import board, moveNumber
        self.buttonsDic[(1, 0)].update()
        global maxNumber
        if int(self.listCanvas['height'])/self.buttonsDic[(1,0)].winfo_height()<maxNumber:
            if maxNumber-moveNumber+1>=self.middleListPos-1+stopOnWhite:
                self.listCanvas.yview(MOVETO,((moveNumber-self.middleListPos-1)*2+stopOnWhite)*self.buttonHC)
            else:
                self.listCanvas.yview(MOVETO,1.0)

        if not (stopOnWhite == 1 and moveNumber == 0):
            createStartPosition()
            if stopOnWhite == 0:
                playTo = moveNumber - 1
            else:
                playTo = moveNumber
            if self.gameLine != 'ERROR':
                clearAll()
                if playTo<0:
                    playTo = 0
                changes = playGame(self.gameLine, playTo, stopOnWhite)
                if stopOnWhite == 0:
                    stopOnWhite = 1
                else:
                    stopOnWhite = 0

                if type(changes) != type(1):
                    self.changeImages(changes)
                else:
                    self.invalidMove(changes)
            self.prevButton.config(background=self.listCanvas["background"])
            if not (playTo == 0 and stopOnWhite==1):
                self.buttonsDic[(playTo,stopOnWhite)].config(background=self.colorSelected)
                self.prevButton=self.buttonsDic[(playTo,stopOnWhite)]

    def moveBack5(self, event= None):
        global stopOnWhite
        from inc.chessengine import board, moveNumber
        global maxNumber
        if int(self.listCanvas['height'])/self.buttonsDic[(1,0)].winfo_height()<maxNumber:
            if maxNumber-moveNumber+5 >= self.middleListPos:
                self.listCanvas.yview(MOVETO,((moveNumber-self.middleListPos-5)*2)*self.buttonHC)
            else:
                self.listCanvas.yview(MOVETO,1.0)

        if  moveNumber >= 5 and not (stopOnWhite == 0 and moveNumber == 5):
            createStartPosition()
            if stopOnWhite == 0:
                playTo = moveNumber - 5
            else:
                playTo = moveNumber - 5
            if self.gameLine != 'ERROR':
                clearAll()
                if playTo<0:
                    playTo = 0
                changes = playGame(self.gameLine, playTo, not stopOnWhite)

                if type(changes) != type(1):
                    self.changeImages(changes)
                else:
                    self.invalidMove(changes)

            self.prevButton.config(background=self.listCanvas["background"])
            if not (playTo == 0 and stopOnWhite==1):
                self.buttonsDic[(playTo,stopOnWhite)].config(background=self.colorSelected)
                self.prevButton=self.buttonsDic[(playTo,stopOnWhite)]
        else:
            createStartPosition()
            if self.gameLine != 'ERROR':
                clearAll()
                changes = playGame(self.gameLine, 0, 0)
                stopOnWhite = 1
                if type(changes) != type(1):
                    self.changeImages(changes)
                else:
                    self.invalidMove(changes)
            self.prevButton.config(background=self.listCanvas["background"])

    def moveForward(self, event= None):
        global maxNumber
        global stopOnWhite
        from inc.chessengine import board, moveNumber
        if int(self.listCanvas['height'])/self.buttonsDic[(1,0)].winfo_height()<maxNumber:
            if moveNumber+stopOnWhite >= self.middleListPos:
                self.listCanvas.yview(MOVETO,((moveNumber-self.middleListPos-1)*2+stopOnWhite)*self.buttonHC)
            else:
                self.listCanvas.yview(MOVETO,0.0)

        if not (moveNumber == maxNumber and stopOnWhite == 1-self.noBlackMove2):
            createStartPosition()
            if stopOnWhite == 0:
                playTo = moveNumber
            else:
                if moveNumber == maxNumber:
                    playTo = maxNumber
                else:
                    playTo = moveNumber+ 1
            if self.gameLine != 'ERROR':
                clearAll()
                changes = playGame(self.gameLine, playTo, stopOnWhite)
                if stopOnWhite == 0:
                    stopOnWhite = 1
                else:
                    stopOnWhite = 0
                if type(changes) != type(1):
                    self.changeImages(changes)
                else:
                    self.invalidMove(changes)
            self.prevButton.config(background=self.listCanvas["background"])
            self.buttonsDic[(playTo,stopOnWhite)].config(background=self.colorSelected)
            self.prevButton=self.buttonsDic[(playTo,stopOnWhite)]

    def moveForward5(self, event = None):
        global stopOnWhite
        global maxNumber
        from inc.chessengine import board, moveNumber
        if int(self.listCanvas['height'])/self.buttonsDic[(1,0)].winfo_height()<maxNumber:
            if moveNumber+5 >= self.middleListPos:
                self.listCanvas.yview(MOVETO,((moveNumber-self.middleListPos+5)*2)*self.buttonHC)
            else:
                self.listCanvas.yview(MOVETO,0.0)

        if moveNumber <= maxNumber - 5:
            createStartPosition()
            if stopOnWhite == 0:
                playTo = moveNumber + 5
            else:
                if moveNumber == maxNumber:
                    playTo = maxNumber
                else:
                    playTo = moveNumber + 5
            if self.gameLine != 'ERROR':
                clearAll()
                changes = playGame(self.gameLine, playTo, not stopOnWhite)
                if type(changes) != type(1):
                    self.changeImages(changes)
                else:
                    self.invalidMove(changes)
            self.prevButton.config(background=self.listCanvas["background"])
            self.buttonsDic[(playTo,stopOnWhite)].config(background=self.colorSelected)
            self.prevButton=self.buttonsDic[(playTo,stopOnWhite)]
        else:
            createStartPosition()
            if self.gameLine != 'ERROR':    #CHECK IN POS IF END ON WHITE!!!!!!!!!!!!!!!!!!!!!!!!!!!
                clearAll()                  #MAYBE EXCEPT "0" SMTH OTHER!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                changes = playGame(self.gameLine, maxNumber)

                stopOnWhite = 1-self.noBlackMove2
                if type(changes) != type(1):
                    self.changeImages(changes)
                else:
                    self.invalidMove(changes)
            self.prevButton.config(background=self.listCanvas["background"])
            self.buttonsDic[(maxNumber,1-self.noBlackMove2)].config(background=self.colorSelected)
            self.prevButton=self.buttonsDic[(maxNumber,1-self.noBlackMove2)]

    def changeImages(self, board):
        self.currentPosition = board

        for i in range(8):
            for j in range(8):
                self.buttons[i][j].destroy()

        for i in range(len(self.takenPiecesWhiteImages)):
            self.takenPiecesWhiteImages[i].destroy()

        for i in range(len(self.takenPiecesBlackImages)):
            self.takenPiecesBlackImages[i].destroy()

        self.numberWhiteTaken.destroy()
        self.numberBlackTaken.destroy()


        self.createBoard()

        if self.boardFliped  == 1:
            boardTemp = []
            for i in range(8):
                boardTemp.append([])
                for j in range(8):
                    boardTemp[i].append('em')

            for i in range(8):
                for j in range(8):
                     boardTemp[i][j] = board[-i-1][-j-1]

            board = boardTemp



        for i in range(8):
            for j in range(8):
                if board[i][j] == "em":
                    self.buttons[i][j].config(image = self.imageEmpty)
                elif board[i][j] == "bR":
                    self.buttons[i][j].config(image = self.imageBlackRock)
                elif board[i][j] == "wR":
                    self.buttons[i][j].config(image = self.imageWhiteRock)
                elif board[i][j] == "bN":
                    self.buttons[i][j].config(image = self.imageBlackKnight)
                elif board[i][j] == "wN":
                    self.buttons[i][j].config(image = self.imageWhiteKnight)
                elif board[i][j] == "bB":
                    self.buttons[i][j].config(image = self.imageBlackBishop)
                elif board[i][j] == "wB":
                    self.buttons[i][j].config(image = self.imageWhiteBishop)
                elif board[i][j] == "bQ":
                    self.buttons[i][j].config(image = self.imageBlackQueen)
                elif board[i][j] == "wQ":
                    self.buttons[i][j].config(image = self.imageWhiteQueen)
                elif board[i][j] == "bK":
                    self.buttons[i][j].config(image = self.imageBlackKing)
                elif board[i][j] == "wK":
                    self.buttons[i][j].config(image = self.imageWhiteKing)
                elif board[i][j] == "bP":
                    self.buttons[i][j].config(image = self.imageBlackPawn)
                elif board[i][j] == "wP":
                    self.buttons[i][j].config(image = self.imageWhitePawn)

        self.showTakenPieces()

    def changeShowLastMove(self):
        self.changeConfig('lm',self.selectedShowLastMove.get())
        if self.selectedShowLastMove.get() == "Yes":
            try:
                if not self.boardFliped:
                    self.buttons[lastPosition1[0]][lastPosition1[1]].config(background = self.lastMoveColor1)
                    self.buttons[lastPosition2[0]][lastPosition2[1]].config(background = self.lastMoveColor2)
                else:
                    self.buttons[-lastPosition1[0]-1][-lastPosition1[1]-1].config(background = self.lastMoveColor1)
                    self.buttons[-lastPosition2[0]-1][-lastPosition2[1]-1].config(background = self.lastMoveColor2)
            except:
                pass
        elif self.selectedShowLastMove.get() == "No":

            if lastPosition1 in [[0,0], [0,2], [0,4], [0,6], [1,1], [1,3], [1,5], [1,7], [2,0], [2,2], [2,4], [2,6],\
            [4,0], [4,2], [4,4], [4,6], [6,0], [6,2], [6,4], [6,6], [3,1], [3,3], [3,5], [3,7], [5,1], [5,3], [5,5], [5,7], [7,1], [7,3], [7,5], [7,7]]:
                default1 = self.lightColor
            else:
                default1 = self.darkColor

            if lastPosition2 in [[0,0], [0,2], [0,4], [0,6], [1,1], [1,3], [1,5], [1,7], [2,0], [2,2], [2,4], [2,6],\
            [4,0], [4,2], [4,4], [4,6], [6,0], [6,2], [6,4], [6,6], [3,1], [3,3], [3,5], [3,7], [5,1], [5,3], [5,5], [5,7], [7,1], [7,3], [7,5], [7,7]]:
                default2 = self.lightColor
            else:
                default2 = self.darkColor
            try:
                if not self.boardFliped:
                    self.buttons[lastPosition1[0]][lastPosition1[1]].config(background = default1)
                    self.buttons[lastPosition2[0]][lastPosition2[1]].config(background = default2)
                else:
                    self.buttons[-lastPosition1[0]-1][-lastPosition1[1]-1].config(background = default1)
                    self.buttons[-lastPosition2[0]-1][-lastPosition2[1]-1].config(background = default2)
            except:
                pass

    def changeShowSidebar(self):

        if self.selectedShowSidebar.get() == "Yes":
            self.notebookFrame.grid()
        elif self.selectedShowSidebar.get() == "No":
            self.notebookFrame.grid_remove()

#        if self.selectedShowSidebar.get() == "Yes":
#            self.selectedShowSidebar.set("No")
#        elif self.selectedShowSidebar.get() == "No":
#            self.selectedShowSidebar.set("Yes")

    def changeShowNextMove(self):
        pass

    def changeShowLegalMoves(self):
        pass

    def changeBoardColor(self, firstTime=0):
        self.changeConfig('bc',self.selectedBoardColor.get())
        if self.selectedBoardColor.get() == "Brown":
            self.lightColor = "#F0D9B5"
            self.darkColor = "#B58863"
        elif self.selectedBoardColor.get() == "Light":
            self.lightColor = "white"
            self.darkColor = "grey"
        elif self.selectedBoardColor.get() == "Green":
            self.lightColor = "#EEEED2"
            self.darkColor = "#769656"
        elif self.selectedBoardColor.get() == "Blue":
            self.lightColor = "#ECECD7"
            self.darkColor = "#4D6D92"
        elif self.selectedBoardColor.get() == "Grey":
            self.lightColor = "#EFEFEF"
            self.darkColor = "#ABABAB"
        elif self.selectedBoardColor.get() == "Red":
            self.lightColor = "#F0D8BF"
            self.darkColor = "#BA5546"
        elif self.selectedBoardColor.get() == "Orange":
            self.lightColor = "#FCE4B2"
            self.darkColor = "#D08B18"
        elif self.selectedBoardColor.get() == "Pink":
            self.lightColor = "#FADDE1"
            self.darkColor = "#D097A1"
        elif self.selectedBoardColor.get() == "Purple":
            self.lightColor = "#EFEFEF"
            self.darkColor = "#8877B7"
        elif self.selectedBoardColor.get() == "Tan":
            self.lightColor = "#EDC9A2"
            self.darkColor = "#D3A36A"
        elif self.selectedBoardColor.get() == "Black & White":
            self.lightColor = "#FFFFFF"
            self.darkColor = "#000000"
        elif self.selectedBoardColor.get() == "Winboard":
            self.lightColor = "#C8C365"
            self.darkColor = "#77A26D"
        self.changeConfig('lc',self.lightColor)
        self.changeConfig('dc',self.darkColor)
        if not firstTime:
            color = 0
            for i in range(8):
                for j in range(8):
                    if not color:
                        bgcolor = self.lightColor
                    else:
                        bgcolor = self.darkColor
                    self.buttons[i][j].config(bg=bgcolor)
                    if not color:
                        color = 1
                    else:
                        color = 0
                if not color:
                    color = 1
                else:
                    color = 0

    def changeBoardSize(self):
        if self.selectedBoardSize.get() == "Small":
            self.changeConfig('sz','Small')
            self.middleListPos = 4
            if self.selectedColorScheme.get() == "Set 1":
                try:
                    self.changeConfig('ps','1')
                    self.imageEmpty = PhotoImage(file = "img/set1/small/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set1/small/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set1/small/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set1/small/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set1/small/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set1/small/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set1/small/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set1/small/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set1/small/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set1/small/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set1/small/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set1/small/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set1/small/bp.png")
                except:
                    print "Falied to load files from \\img\\set1\\small folder"
            elif self.selectedColorScheme.get() == "Set 2":
                try:
                    self.changeConfig('ps','2')
                    self.imageEmpty = PhotoImage(file = "img/set2/small/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set2/small/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set2/small/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set2/small/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set2/small/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set2/small/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set2/small/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set2/small/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set2/small/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set2/small/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set2/small/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set2/small/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set2/small/bp.png")
                except:
                    print "Falied to load files from \\img\\set2\\small folder"
            self.notebookFrame["height"] = 344
            self.sideBar["height"] = 310
            self.listCanvas["height"] = 195
            self.canvasInfo["height"] = 298

        elif self.selectedBoardSize.get() == "Default":
            self.changeConfig('sz','Default')
            self.middleListPos = 7
            if self.selectedColorScheme.get() == "Set 1":
                try:
                    self.changeConfig('ps','1')
                    self.imageEmpty = PhotoImage(file = "img/set1/default/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set1/default/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set1/default/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set1/default/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set1/default/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set1/default/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set1/default/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set1/default/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set1/default/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set1/default/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set1/default/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set1/default/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set1/default/bp.png")
                except:
                    print "Falied to load files from \\img\\set1\\default folder"
            elif self.selectedColorScheme.get() == "Set 2":
                try:
                    self.changeConfig('ps','2')
                    self.imageEmpty = PhotoImage(file = "img/set2/default/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set2/default/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set2/default/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set2/default/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set2/default/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set2/default/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set2/default/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set2/default/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set2/default/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set2/default/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set2/default/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set2/default/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set2/default/bp.png")
                except:
                    print "Falied to load files from \\img\\set2\\default folder"
            self.notebookFrame["height"] = 464
            self.sideBar["height"] = 430
            self.listCanvas["height"] = 315
            self.canvasInfo["height"] = 418

        elif self.selectedBoardSize.get() == "Large":
            self.changeConfig('sz','Large')
            self.middleListPos = 10
            if self.selectedColorScheme.get() == "Set 1":
                try:
                    self.changeConfig('ps','1')
                    self.imageEmpty = PhotoImage(file = "img/set1/large/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set1/large/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set1/large/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set1/large/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set1/large/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set1/large/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set1/large/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set1/large/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set1/large/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set1/large/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set1/large/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set1/large/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set1/large/bp.png")
                except:
                    print "Falied to load files from \\img\\set1\\large folder"
            elif self.selectedColorScheme.get() == "Set 2":
                try:
                    self.changeConfig('ps','2')
                    self.imageEmpty = PhotoImage(file = "img/set2/large/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set2/large/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set2/large/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set2/large/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set2/large/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set2/large/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set2/large/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set2/large/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set2/large/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set2/large/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set2/large/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set2/large/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set2/large/bp.png")
                except:
                    print "Falied to load files from \\img\\set2\\large folder"
            self.notebookFrame["height"] = 584
            self.sideBar["height"] = 550
            self.listCanvas["height"] = 435
            self.canvasInfo["height"] = 538

        for i in range(8):
            for j in range(8):
                self.buttons[i][j].destroy()

        self.createBoard()

        global stopOnWhite
        from inc.chessengine import board, moveNumber
        playTo = moveNumber
        createStartPosition()
        if self.gameLine != 'ERROR':
            clearAll()
            changes = playGame(self.gameLine, playTo, not stopOnWhite)
            if type(changes) != type(1):
                self.changeImages(changes)
            else:
                self.invalidMove(changes)

        self.notebook.setnaturalsize()
        if not self.firstTimeLoaded:
            self.buttonsDic[(1, 0)].update()
            self.middleListPos = int(round(int(self.listCanvas["height"])/(2.0*self.buttonsDic[(1, 0)].winfo_height())))

    def changeColorScheme(self, firstTime = 0):
        if self.selectedColorScheme.get() == "Set 1":
            self.changeConfig('ps','1')
            if self.selectedBoardSize.get() == "Small":
                try:
                    self.changeConfig('sz','Small')
                    self.imageEmpty = PhotoImage(file = "img/set1/small/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set1/small/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set1/small/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set1/small/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set1/small/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set1/small/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set1/small/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set1/small/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set1/small/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set1/small/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set1/small/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set1/small/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set1/small/bp.png")
                except:
                    print "Falied to load files from \\img\\set1\\small folder"
            elif self.selectedBoardSize.get() == "Default":
                try:
                    self.changeConfig('sz','Default')
                    self.imageEmpty = PhotoImage(file = "img/set1/default/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set1/default/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set1/default/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set1/default/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set1/default/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set1/default/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set1/default/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set1/default/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set1/default/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set1/default/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set1/default/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set1/default/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set1/default/bp.png")
                except:
                    print "Falied to load files from \\img\\set1\\default folder"
            elif self.selectedBoardSize.get() == "Large":
                try:
                    self.changeConfig('sz','Default')
                    self.imageEmpty = PhotoImage(file = "img/set1/large/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set1/large/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set1/large/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set1/large/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set1/large/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set1/large/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set1/large/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set1/large/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set1/large/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set1/large/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set1/large/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set1/large/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set1/large/bp.png")
                except:
                    print "Falied to load files from \\img\\set1\\large folder"

        elif self.selectedColorScheme.get() == "Set 2":
            self.changeConfig('ps','2')
            if self.selectedBoardSize.get() == "Small":
                try:
                    self.changeConfig('sz','Small')
                    self.imageEmpty = PhotoImage(file = "img/set2/small/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set2/small/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set2/small/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set2/small/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set2/small/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set2/small/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set2/small/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set2/small/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set2/small/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set2/small/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set2/small/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set2/small/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set2/small/bp.png")
                except:
                    print "Falied to load files from \\img\\set2\\small folder"
            elif self.selectedBoardSize.get() == "Default":
                try:
                    self.changeConfig('sz','Default')
                    self.imageEmpty = PhotoImage(file = "img/set2/default/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set2/default/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set2/default/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set2/default/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set2/default/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set2/default/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set2/default/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set2/default/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set2/default/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set2/default/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set2/default/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set2/default/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set2/default/bp.png")
                except:
                    print "Falied to load files from \\img\\set2\\default folder"
            elif self.selectedBoardSize.get() == "Large":
                try:
                    self.changeConfig('sz','Large')
                    self.imageEmpty = PhotoImage(file = "img/set2/large/empty.gif")
                    self.imageWhiteRock = PhotoImage(file = "img/set2/large/wr.png")
                    self.imageBlackRock = PhotoImage(file = "img/set2/large/br.png")
                    self.imageWhiteBishop = PhotoImage(file = "img/set2/large/wb.png")
                    self.imageBlackBishop = PhotoImage(file = "img/set2/large/bb.png")
                    self.imageWhiteKnight = PhotoImage(file = "img/set2/large/wn.png")
                    self.imageBlackKnight = PhotoImage(file = "img/set2/large/bn.png")
                    self.imageWhiteQueen = PhotoImage(file = "img/set2/large/wq.png")
                    self.imageBlackQueen = PhotoImage(file = "img/set2/large/bq.png")
                    self.imageWhiteKing = PhotoImage(file = "img/set2/large/wk.png")
                    self.imageBlackKing = PhotoImage(file = "img/set2/large/bk.png")
                    self.imageWhitePawn = PhotoImage(file = "img/set2/large/wp.png")
                    self.imageBlackPawn = PhotoImage(file = "img/set2/large/bp.png")
                except:
                    print "Falied to load files from \\img\\set2\\large folder"

        if not firstTime:

            for i in range(8):
                for j in range(8):
                    self.buttons[i][j].destroy()

            self.createBoard()

            global stopOnWhite
            from inc.chessengine import board, moveNumber
            playTo = moveNumber
            createStartPosition()
            if self.gameLine != 'ERROR':
                clearAll()
                changes = playGame(self.gameLine, playTo, not stopOnWhite)
                if type(changes) != type(1):
                    self.changeImages(changes)
                else:
                    self.invalidMove(changes)

    def showTakenPieces(self):
        from inc.chessengine import takenWhite, takenBlack

        self.takenPiecesWhiteImages = []
        self.takenPiecesBlackImages = []

        wP = 0
        wB = 0
        wN = 0
        wQ = 0
        bP = 0
        bN = 0
        wR = 0
        bR = 0
        bB = 0
        bQ = 0
        numberWhiteTaken = 0
        numberBlackTaken = 0

        #SORTING LISTS TO Q-R-B-N-P

        for i in takenWhite:
            if i == "P":
                wP += 1
                numberWhiteTaken += 1
            elif i == "R":
                wR += 1
                numberWhiteTaken += 5
            elif i == "N":
                wN += 1
                numberWhiteTaken += 3
            elif i == "B":
                wB += 1
                numberWhiteTaken += 3
            elif i == "Q":
                wQ += 1
                numberWhiteTaken += 9
        takenWhite = []
        for i in range(wQ):
            takenWhite += "Q"
        for i in range(wR):
            takenWhite += "R"
        for i in range(wB):
            takenWhite += "B"
        for i in range(wN):
            takenWhite += "N"
        for i in range(wP):
            takenWhite += "P"

        for i in takenBlack:
            if i == "P":
                bP += 1
                numberBlackTaken += 1
            elif i == "R":
                bR += 1
                numberBlackTaken += 5
            elif i == "N":
                bN += 1
                numberBlackTaken += 3
            elif i == "B":
                bB += 1
                numberBlackTaken += 3
            elif i == "Q":
                bQ += 1
                numberBlackTaken += 9
        takenBlack = []
        for i in range(bQ):
            takenBlack += "Q"
        for i in range(bR):
            takenBlack += "R"
        for i in range(bB):
            takenBlack += "B"
        for i in range(bN):
            takenBlack += "N"
        for i in range(bP):
            takenBlack += "P"

        #END OF SORTING LISTS
        for i in takenWhite:
            if i == "P":
                self.takenPiecesWhiteImages.append(Label(self.takenPiecesFrame, image = self.imageTakenBlackPawn, bg=self.takenPiecesBackground))
            elif i == "R":
                self.takenPiecesWhiteImages.append(Label(self.takenPiecesFrame, image = self.imageTakenBlackRock, bg=self.takenPiecesBackground))
            elif i == "N":
                self.takenPiecesWhiteImages.append(Label(self.takenPiecesFrame, image = self.imageTakenBlackKnight, bg=self.takenPiecesBackground))
            elif i == "B":
                self.takenPiecesWhiteImages.append(Label(self.takenPiecesFrame, image = self.imageTakenBlackBishop, bg=self.takenPiecesBackground))
            elif i == "Q":
                self.takenPiecesWhiteImages.append(Label(self.takenPiecesFrame, image = self.imageTakenBlackQueen,bg=self.takenPiecesBackground))

        for i in takenBlack:
            if i == "P":
                self.takenPiecesBlackImages.append(Label(self.takenPiecesFrame, image = self.imageTakenWhitePawn, bg=self.takenPiecesBackground))
            elif i == "R":
                self.takenPiecesBlackImages.append(Label(self.takenPiecesFrame, image = self.imageTakenWhiteRock, bg=self.takenPiecesBackground))
            elif i == "N":
                self.takenPiecesBlackImages.append(Label(self.takenPiecesFrame, image = self.imageTakenWhiteKnight, bg=self.takenPiecesBackground))
            elif i == "B":
                self.takenPiecesBlackImages.append(Label(self.takenPiecesFrame, image = self.imageTakenWhiteBishop, bg=self.takenPiecesBackground))
            elif i == "Q":
                self.takenPiecesBlackImages.append(Label(self.takenPiecesFrame, image = self.imageTakenWhiteQueen, bg=self.takenPiecesBackground))

        self.numberBlackTaken = Label(self.takenPiecesFrame, text = numberBlackTaken, font= self.font1, bg=self.takenPiecesBackground)
        self.numberBlackTaken.grid(column = 0, row = 0, sticky=W)
        self.numberBlackTakenBlank = Label(self.takenPiecesFrame, text = "", font= self.font1, bg=self.takenPiecesBackground)
        self.numberBlackTakenBlank.grid(column = 0, row = 1, sticky=W)

        lineCounter = 0
        colunmCounter  = 0
        for i in range(len(self.takenPiecesBlackImages)):
            lineCounter +=1
            if lineCounter <=8:
                self.takenPiecesBlackImages[i].grid(column = i+1, row = 0)
            else:
                colunmCounter += 1
                self.takenPiecesBlackImages[i].grid(column = colunmCounter, row = 1)


        self.numberWhiteTaken = Label(self.takenPiecesFrame, text = numberWhiteTaken, font= self.font1, bg=self.takenPiecesBackground)
        self.numberWhiteTaken.grid(column = 0, row = 2, sticky=W)
        self.numberWhiteTakenBlank = Label(self.takenPiecesFrame, text = "", font= self.font1, bg=self.takenPiecesBackground)
        self.numberWhiteTakenBlank.grid(column = 0, row = 3, sticky=W)

        lineCounter = 0
        colunmCounter = 0
        for i in range(len(self.takenPiecesWhiteImages)):
            lineCounter +=1
            if lineCounter <=8:
                self.takenPiecesWhiteImages[i].grid(column = i+1, row = 2)
            else:
                colunmCounter +=1
                self.takenPiecesWhiteImages[i].grid(column = colunmCounter, row = 3)

    def showInfoAboutGame(self):
        self.noInfoLabel.destroy()
        self.infoLabelsData = []
        self.infoLabels = []
        self.gameInfoKeys1 = self.gameInfo.keys()
        rowCounter = 0
        if "Result" in self.gameInfoKeys1:
            if self.gameInfo["Result"] == "*":
                self.gameInfo["Result"] = "In progress"
                print self.gameInfo["Result"]

        for key in self.gameInfoKeys:
            if key in self.gameInfoKeys1:
                    self.infoLabels += [Label(self.infoList, text = key, font=self.infoLeftFont, wraplength=70)]
                    self.infoLabels[-1].grid(row=rowCounter,column=0, sticky=W, padx=1)
                    self.infoLabelsData += [Label(self.infoList, text = self.gameInfo[key], font = self.infoRightFont, wraplength=152)]
                    self.infoLabelsData[-1].grid(row=rowCounter,column=1, sticky=W, padx=1)
                    rowCounter += 1

     
        for i in self.gameInfoKeys1:
            if i not in self.gameInfoKeys:
                self.infoLabelsData += [Label(self.infoList, text = self.gameInfo[i], font = self.infoRightFont, wraplength=152)]
                self.infoLabels += [Label(self.infoList, text = i, font=self.infoLeftFont)]
                self.infoLabels[-1].grid(row=rowCounter,column=0, sticky=W, padx=1)
                self.infoLabelsData[-1].grid(row=rowCounter,column=1, sticky=W, padx=1)
                rowCounter +=1

        self.infoList.update_idletasks()
        self.canvasInfo.config(scrollregion=self.canvasInfo.bbox("all"))
        if self.gameInfo["White"] and self.gameInfo["Black"]:
            newTitle = "PyGN - " + self.gameInfo["White"] + " vs " + self.gameInfo["Black"]
            self.master.title(newTitle)


    def flipBoard(self):
        self.boardFliped  = not self.boardFliped
        self.changeConfig('bf',str(int(self.boardFliped)))
        if self.gameLine != 'ERROR':
            self.changeImages(self.currentPosition)

    def showAbout(self):
        """Help-About"""
        aboutWindow = Toplevel()
        aboutWindow.title('About')
        aboutWindow.resizable(0, 0)
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        sizeStr = "250x150+" + str(ws/2-125) + "+" + str(hs/2-75)
        aboutWindow.geometry(sizeStr)
        aboutWindow.iconbitmap('img/favicon.ico')
        aboutWindow.config(bg=self.takenPiecesBackground)
        aboutWindow.focus()

        logoLabel = Label(aboutWindow, image = self.imageLogo, bd=0)
        logoLabel.pack(side = TOP)

        aboutText = "Created by:\n   Hollgam (hollgam.com)\n   Vinchkovsky \nVersion: %s\nLanguage: Python 2.6.1\nAdditional modules: Tkinter, PMW, PIL" % __version__
        aboutlabel = Label(aboutWindow, text = aboutText, wraplength=250, justify=LEFT, bg=self.takenPiecesBackground, font= self.font2)
        aboutlabel.pack(side = TOP)
        #showinfo("About", "Made by Hollgam and Vinchkovsky \nVersion: %s\nPython 2.6.1\nAdditional modules: Tkinter, tkMessageBox, PMW, PIL" % __version__)

    def showKeys(self):
        """Help-About"""
        showinfo("Keyboard shortcuts", "6 - Move forward\n4 - Move backwards\n9 - Move forward 5 moves\n7 - Move backwards 5 moves\n8 - Last position\n5 - Initial position\nSpace - Move forward\nCtrl+O - Load a game\nCtrl+Q - Close a game")


    def loadGame(self, fileToLoad="none"):
        # window for choosing file to laod

        if fileToLoad=="none":
            fileToLoad = askopenfilename(title='Choose a file to load', filetypes=[('PGN files','*.pgn')])
            #fileToLoad = "1.pgn"
        if fileToLoad != '':
            self.notebook.selectpage('Moves   ')
            currentCH = int(self.listCanvas["height"])
            currentCW = int(self.listCanvas["width"])

            self.moveListFrame.destroy()
            self.moveListFrame = Frame(self.sideBar)
            self.moveListFrame.grid(row=0,column=0,sticky=NW)
            self.vscrollbar = Scrollbar(self.moveListFrame)
            self.vscrollbar.grid(row=0, column=1, sticky=N+S, pady=4)
            self.listCanvas = Canvas(self.moveListFrame,yscrollcommand=self.vscrollbar.set,height=currentCH ,width=currentCW)
            self.listCanvas.grid(row=0, column=0, sticky=N+S+E+W, pady=4)
            self.vscrollbar.config(command=self.listCanvas.yview)
            self.frameList = Frame(self.listCanvas)
            self.listCanvas.create_window(0, 0, anchor=NW, window=self.frameList)
            self.frameList.update_idletasks()
            self.listCanvas.config(scrollregion=self.listCanvas.bbox("all"))

            notesToLoad = fileToLoad + "n"
            self.notesFile = notesToLoad
            self.loadNotes()
            self.gameLine = readFileLine(fileToLoad)
            from inc.chessengine import gameLineCorrected
            if gameLineCorrected:
                showinfo("Warning", "Line with moves in the file was corrected. A wrong sequence of moves might have been created.")
                gameLineCorrected = 0
            self.gameInfo = readInfoFromFile(fileToLoad)
            self.showLastPosition(1)
            self.loadNotes()
            self.makeButtonsActive()

            self.showInfoAboutGame()
            someInfo=''
            try:
                someInfo+=self.gameInfo["White"]+ ' vs '+self.gameInfo["Black"]+', '
            except:
                try:
                    someInfo+=self.gameInfo["white"]+ ' vs '+self.gameInfo["black"]+', '
                except:
                    someInfo+='[No info about players ], '
            try:
                someInfo += '"'+self.gameInfo["Result"]+'", '
            except:
                try:
                    someInfo+=self.gameInfo['result']+', '
                except:
                    someInfo+='[No info about result], '
            try:
                someInfo += self.gameInfo["Event"]+', '
            except:
                pass
            try:
                someInfo += self.gameInfo["Date"]+', '
            except:
                pass
            try:
                someInfo += self.gameInfo["Site"]
            except:
                pass

            try:
                print self.fileDicRev[fileToLoad]
            except:
                try:
                    print fileToLoad
                    someInfo=someInfo+'\n'
                    self.gamesList.insert(END,someInfo)
                    self.fileDicRev[fileToLoad]=someInfo
                    self.fileDic[someInfo]=fileToLoad
                    fileIn = open(self.fileListName,"w")
                    for line in self.filesList:
                        line = line.replace('\n','')
                        fileIn.write(line+'\n')
                    self.filesList+=[fileToLoad+'#'+someInfo]
                    fileIn.write(fileToLoad+'#'+someInfo+'\n')
                    fileIn.close()
                except:
                    pass


    def closeGame(self, event= None):
        self.saveNotes()
        clearAll()
        self.unBindKeys()
        self.__init__()
#        self.createBoard()
#        self.currentPosition = createStartPosition()
#        self.makeButtonsDisabled()
#        self.showStartPosition()
#
#
#        #LIST OF MOVES
#        self.moveListFrame.grid(row=0,column=0,sticky=NW)
#        self.vscrollbar.grid(row=0, column=1, sticky=N+S, pady=4)
#        self.listCanvas.grid(row=0, column=0, sticky=N+S+E+W, pady=4)
#        self.vscrollbar.config(command=self.listCanvas.yview)
#        self.listCanvas.create_window(0, 0, anchor=NW, window=self.frameList)
#        self.frameList.update_idletasks()
#        self.listCanvas.config(scrollregion=self.listCanvas.bbox("all"))
#
#        #FRAME SHOWING TAKEN PIECES
#        self.numberWhiteTaken = 0
#        self.numberBlackTaken = 0
#        self.takenPiecesContainer.grid(row=1,column=0,sticky=W, padx=4)
#
#        self.takenPiecesFrame.grid(row=0,column=0,sticky=W, padx=1, pady=1)
#        self.takenPiecesFrame.grid_propagate(False)
#
#
#        #INFO ABOUT GAME
#
#        self.infoFrame.grid(row=0,column=0,sticky=NW)
#        self.vscrollbarInfo.grid(row=0, column=1, sticky=N+S, pady=4)
#        self.canvasInfo.grid(row=0, column=0, sticky=N+S+E+W, pady=4)
#        self.vscrollbarInfo.config(command=self.canvasInfo.yview)
#        self.canvasInfo.create_window(0, 0, anchor=NW, window=self.infoList)
#        self.infoList.update_idletasks()
#        self.canvasInfo.config(scrollregion=self.canvasInfo.bbox("all"))
#
#        self.noInfoLabel = Label(self.infoList, text = "Load game to see info about it.", font=self.infoLeftFont)
#        self.noInfoLabel.grid(row=0,column=0, sticky=W, padx=1)


    def makeButtonsActive(self):
        self.KeyStart.config(state = ACTIVE)
        self.KeyBack5.config(state = ACTIVE)
        self.KeyBack.config(state = ACTIVE)
        self.KeyForward.config(state = ACTIVE)
        self.KeyForward5.config(state = ACTIVE)
        self.KeyEnd.config(state = ACTIVE)

        def checkFocus6(event):
            if str(self.master.focus_get()).find(str(self.textEntry))==-1 and str(self.textEntry).find(str(self.master.focus_get()))==-1:
                self.moveForward()
        def checkFocus4(event):
            if str(self.master.focus_get()).find(str(self.textEntry))==-1 and str(self.textEntry).find(str(self.master.focus_get()))==-1:
                self.moveBack()
        def checkFocus9(event):
            if str(self.master.focus_get()).find(str(self.textEntry))==-1 and str(self.textEntry).find(str(self.master.focus_get()))==-1:
                self.moveForward5()
        def checkFocus7(event):
            if str(self.master.focus_get()).find(str(self.textEntry))==-1 and str(self.textEntry).find(str(self.master.focus_get()))==-1:
                self.moveBack5()
        def checkFocus8(event):
            if str(self.master.focus_get()).find(str(self.textEntry))==-1 and str(self.textEntry).find(str(self.master.focus_get()))==-1:
                self.showLastPosition()
        def checkFocus5(event):
            if str(self.master.focus_get()).find(str(self.textEntry))==-1 and str(self.textEntry).find(str(self.master.focus_get()))==-1:
                self.showStartPosition()

#        click on the buttons
        self.master.bind("<KeyPress-6>", checkFocus6)
        self.master.bind("<KeyPress-space>", checkFocus6)
        self.master.bind("<KeyPress-4>", checkFocus4)
        self.master.bind("<KeyPress-9>", checkFocus9)
        self.master.bind("<KeyPress-7>", checkFocus7)
        self.master.bind("<KeyPress-8>", checkFocus8)
        self.master.bind("<KeyPress-5>", checkFocus5)

    def makeButtonsDisabled(self):
        self.KeyStart.config(state = DISABLED)
        self.KeyBack5.config(state = DISABLED)
        self.KeyBack.config(state = DISABLED)
        self.KeyForward.config(state = DISABLED)
        self.KeyForward5.config(state = DISABLED)
        self.KeyEnd.config(state = DISABLED)
        self.buttonSaveNotes.config(state=DISABLED)

    def unBindKeys(self):
#        self.master.unbind("<KeyPress-6>")
#        self.master.unbind("<KeyPress-space>")
#        self.master.unbind("<KeyPress-4>")
#        self.master.unbind("<KeyPress-9>")
#        self.master.unbind("<KeyPress-7>")
#        self.master.unbind("<KeyPress-8>")
#        self.master.unbind("<KeyPress-5>")
        pass

    def loadNotes(self):
        self.clearNotes()
        try:
            self.textEntry.importfile(self.notesFile)
            self.notesImported = 1
        except:
            pass
        self.buttonSaveNotes.config(state=ACTIVE)
        self.buttonClearNotes.config(state=ACTIVE)

    def clearNotes(self):
        self.textEntry.clear()


    def saveNotes(self):
        if self.notesFile:
            self.textEntry.exportfile(self.notesFile)

    def exitGame(self, event=None):
        """Game-Exit"""
        self.destroy()
        sys.exit(1)

    def doN(self, event=None):
        pass


    def invalidMove(self,type=0):
        """
        shows different errors in chess logic of moves
        """
        if not type:
            message = "ERROR"
        elif type==13:
            message = "OTHER PIECES ON THE WAY"
        elif type==2:
            message = "YOUR PIECE ON THE DESTINATION POINT"
        elif type==3:
            message = "x WAS NOT MENTIONED"
        elif type==4:
            message = "TRYING TO TAKE YOUR OWN PIECE"
        elif type==5:
            message = "TRYING TO TAKE AN EMPTY CELL"
        elif type==6:
            message = "MORE THAN ONE PIECE CAN MAKE A MOVE"
        elif type==7:
            message = "NO PIECE CAN MAKE A MOVE"
        elif type==8:
            message = "NO PIECE WITH THIS ADDITIONAL COORDINATES CAN MOVE"
        elif type==9:
            message = "CAN NOT MAKE A CASTLE"
        elif type==10:
            message = "CASTLE HAS ALREADY BEEN DONE"
        elif type==11:
            message = "CHECK FOR YOU CANT BE A RESULT OF YOUR MOVE"
        elif type==12:
            message = "BAD CHARS IN THE MOVE"
        elif type==14:
            message = 'WRONG NUMBER OF MOVE ENTERED'
        elif type==15:
            message = 'INCORRECT ORDER OF MOVE NUMBERS'
        elif type==16:
            message = 'INCORRECT QUANTITYOF MOVES'
        elif type==17:
            message = 'NO CHECK'
        elif type==18:
            message = 'CANNOT MOVE THERE BECAUSE OF THE CHECK'
        elif type==19:
            message = 'NO CHECKMATE: ENENY KING IS NOT UNDER ATTACK'
        elif type==20:
            message = 'NO CHECKMATE: ENENY CAN PROTECT HIS/HER KING'
        elif type==21:
            message = 'NO CHECKMATE: ENEMY KING CAN ESCAPE'
        elif type==22:
            message = 'KING IS UNDER ATTACK AFTER THIS MOVE'

        from inc.chessengine import errorAtMove

        clearAll()
        createStartPosition()
        if errorAtMove[1] == "w":
            if errorAtMove[0]==1:
                changes = playGame(self.gameLine , 0, 0)
            else:
                changes = playGame(self.gameLine, errorAtMove[0]-1, 0)
        elif errorAtMove[1] == "b":
            changes = playGame(self.gameLine, errorAtMove[0], 1)
        print changes
        self.changeImages(changes)
        from inc.chessengine import moveNumber
        global maxNumber, stopOnWhite
        maxNumber = moveNumber

        #FIND MAXNUMBER
        posP=-1
        posS=-1
        for i in range(len(self.gameLine)-1,0,-1):
            if self.gameLine[i]=='.':
                posP = i
            elif (self.gameLine[i]==' ' or not (self.gameLine[i] in ['1','2','3','4','5','6','7','8','9','0'])):
                if posP!=-1:
                    posS=i+1
                    break

        maxNumberInv = int(self.gameLine[posS:posP])
        if maxNumberInv<maxNumber:
            maxNumberInv = maxNumber

        #INIT
        self.noBlackLastMove = 0
        self.buttonHC = 1/(2.0*maxNumberInv)
        self.vscrollbar.config(command=self.listCanvas.yview)
        self.frameList = Frame(self.listCanvas)
        self.listCanvas.create_window(0, 0, anchor=NW, window=self.frameList)
        self.frameList.update_idletasks()
        self.listCanvas.config(scrollregion=self.listCanvas.bbox("all"))

        rows = maxNumberInv

        #LOAD GAME LIST
        self.buttonsDic = {}
        for i in range(1,rows+1):
            for j in range(1,4):
                if j==1:
                    self.label = Label(self.frameList,text=str(i))
                    self.label.grid(row=i,column=j)
                else:
                    if j==2:
                        posPoint = self.gameLine.find(" "+str(i)+".")+2+len(str(i))
                        posSpace = self.gameLine.find(" ",posPoint)
                        if posSpace == -1:
                            posSpace = len(self.gameLine)
                            self.noBlackLastMove = 1

                        if i<errorAtMove[0] or (i==errorAtMove[0] and errorAtMove[1]=='b'):
                            self.button = Button(self.frameList, width=self.keyWidthx, text=self.gameLine[posPoint:posSpace], name=str(i)+"0",relief=GROOVE)
                            self.button.bind("<Button-1>",self.changePositionList)

                        elif i==errorAtMove[0] and errorAtMove[1]=='w':
                            self.button = Button(self.frameList, width=self.keyWidthx, text=self.gameLine[posPoint:posSpace], name=str(i)+"0",relief=GROOVE,background='red')
                        else:
                            self.button = Button(self.frameList, width=self.keyWidthx, text=self.gameLine[posPoint:posSpace], name=str(i)+"0",relief=GROOVE,state=DISABLED)

                        self.button.grid(row=i, column=j, sticky='news')
                        self.buttonsDic[(i, j-2)] = self.button

                    elif j==3:
                        posEnd = self.gameLine.find(" "+str(i+1)+".", posSpace)
                        if i==maxNumberInv:
                            posEnd = len(self.gameLine)
#                        if not self.noBlackLastMove:
#                            self.button = Button(self.frameList, padx=22, text=self.gameLine[posSpace+1:posEnd], name=str(i)+"1",relief=GROOVE)

                        if i<errorAtMove[0]:
                            print 'NOOOORM',self.gameLine[posSpace+1:posEnd]
                            self.button = Button(self.frameList, width=self.keyWidthx, text=self.gameLine[posSpace+1:posEnd], name=str(i)+"1",relief=GROOVE)
                            self.button.bind("<Button-1>",self.changePositionList)
                        elif i==errorAtMove[0] and errorAtMove[1]=='b':
                            print 'REEEEEEEEEED',self.gameLine[posSpace+1:posEnd]
                            self.noBlackMove2=1
                            self.noBlackLastMove = 1
                            self.button = Button(self.frameList, width=self.keyWidthx, text=self.gameLine[posSpace+1:posEnd], name=str(i)+"1",relief=GROOVE,background='red')
                        else:
                            self.button = Button(self.frameList, width=self.keyWidthx, text=self.gameLine[posSpace+1:posEnd], name=str(i)+"1",relief=GROOVE,state=DISABLED)

                        self.button.grid(row=i, column=j, sticky='news')
                        self.buttonsDic[(i, j-2)] = self.button

        self.listCanvas.create_window(0, 0, anchor=NW, window=self.frameList)
#        self.frameList.update_idletasks()
        self.listCanvas.config(scrollregion=self.listCanvas.bbox("all"))

        self.buttonsDic[(1, 0)].update()
        self.middleListPos = int(round(int(self.listCanvas["height"])/(2.0*self.buttonsDic[(1, 0)].winfo_height())))
        print message
        #showinfo("Error", message)

        self.doFurther = 0

        #sys.exit(1) #EXITS A PROGRAM HANDY FOR CHECKS
        return 1
    def defaultAll(self):
        self.selectedColorScheme.set("Set 1")
        self.changeColorScheme()
        self.selectedBoardColor.set("Brown")
        self.changeBoardColor()
        self.selectedBoardSize.set("Default")
        self.changeBoardSize()
        self.selectedShowLastMove.set("Yes")
        self.changeShowLastMove()
def main():
    createStartPosition()
#    fileToLoad = "1.pgn"

    PGN_GUI().mainloop()


if __name__ == "__main__":
    main()