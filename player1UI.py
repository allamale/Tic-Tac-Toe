import socket
from gameboardUI import BoardClass
from tkinter import * 
from tkinter.ttk import Button

#Player 1 = client (connects to the host server)

#class for player1
class Player1:

    def __init__(self, username1: str = '', username2: str= '', HOST: str = '', PORT = ''):
        """Attributes for player1 class (connection, sockets, exchange usernames)"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root = Tk()
        self.game = BoardClass()
        self.canvas()
        self.HOST= HOST
        self.PORT= PORT
        self.username1 = username1
        self.username2 = username2
        self.RECV_SIZE = 1024
        self.player1symbol = "X"
        self.player2symbol = "O"
        self.waiting = False

    def setusername1(self, username1: str):
        """set username for player1"""

        self.username1 = username1

    def setusername2(self, username2: str):
        """set username for player2"""

        self.username2 = username2

    def getusername1(self):
        """get username for player1"""

        return self.username1

    def getusername2(self):
        """get username for player2"""

        return self.username2

    def canvas(self):
        """Creates the window
        
        """
        self.root.geometry('500x300')
        self.root.title("Player1")

        self.userinputframe= Frame(self.root, bg = 'pink')
        self.userinputframe.pack(side= TOP)

    def getHOST(self):
        """Gets the Host and creates the host entry widget
        
        """

        h = Label(self.userinputframe, text = "Enter in a Host Name: ")
        h.pack(side=TOP)

        self.HOSTvar = StringVar()
        self.HOST = Entry(self.userinputframe, textvariable = self.HOSTvar, width=20)
        self.HOST.pack()
        # self.HOST.insert(0, '')


    def getPORT(self):
        """Gets the Port and creates the Port entry widget
        
        """
        p = Label(self.userinputframe, text = "Enter in a Port #: ")
        p.pack(side=BOTTOM)

        self.PORTvar = StringVar()
        self.PORT = Entry(self.userinputframe, textvariable = self.PORTvar, width=20)
        self.PORT.pack()
        # self.PORT.insert(0, '')

    def connectbutton(self):
        """Creates the connect button and quit button
        
        """
        self.connButt = Button(self.userinputframe, text = "Connect", command=self.connecttoserver)
        self.connButt.pack()

        self.leaveBUTT = Button(self.userinputframe, text = "Quit", command= lambda: self.leave())
        self.leaveBUTT.pack()

    def leave(self):
        """Destroys the window if player clicks the quit button
        
        """
        self.root.destroy()

    def connecttoserver(self): 
        """Attemps to connect to server
        
        """
        
        try:
            self.socket.connect( (self.HOSTvar.get(), int(self.PORTvar.get()) ))

            self.connButt.destroy()
            self.leaveBUTT.destroy()
            self.getusername()

        except Exception as e:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.noconnection = Label(self.userinputframe, text ="Connection failed, click connect again when you have valid inputs")
            self.noconnection.pack(side= RIGHT)




    def getusername(self):
        """Creates the username entry widget and submit button
        
        """
        self.usernameframe = Frame(self.root, bg = 'pink')
        self.usernameframe.pack(side=BOTTOM)

        self.askforuser = Label(self.usernameframe, text = "Successful Connection!\n" + "Enter in a username: ")
        self.askforuser.pack(side=LEFT)
        self.askforuserenter = Entry(self.usernameframe, width=20)
        self.askforuserenter.pack()

        self.submitusernameBUTT = Button(self.usernameframe, text = "Submit username", command = lambda: self.submitusername())
        self.submitusernameBUTT.pack(side=RIGHT)



    def submitusername(self):
        """Tests for a valid username and then recieves server username
        
        """
        try:
            if not self.askforuserenter.get().strip().isalnum():
                raise ValueError
        except ValueError:
            self.badname = Label(self.usernameframe, text = "invalid username").pack(side= BOTTOM)
            return

        self.goodname = Label(self.usernameframe, text = "Nice name!").pack(side=BOTTOM)
        self.setusername1(str(self.askforuserenter.get()))
        self.submitusernameBUTT.destroy()
        self.socket.sendall(str(self.askforuserenter.get()).encode())
        self.recieveplayer2name()


    def recieveplayer2name(self):
        """recieves server username and prints the board, then prints the names of the players
        
        """
        self.usernameofserver = self.socket.recv(self.RECV_SIZE).decode()
        self.setusername2(str(self.usernameofserver))

        self.printgameboard()
        self.printnames()
        self.game.updateGamesPlayed()

    def printnames(self):
        """Prints the names of the users onto the gui
        
        """
        self.printusernamesframe = Frame(self.root, bg = 'pink')
        self.printusernamesframe.pack(side= RIGHT)

        self.printusernames = Label(self.printusernamesframe, text = " Welcome to tictactoe!\n" + str(self.getusername1()) + "  and  " + str(self.getusername2()) + "Player 1's turn")
        self.printusernames.pack()

    def printgameboard(self):
        """Prints the gameboard onto the GUI
        
        """
        gameboardframe= Frame(self.root, bg='pink')

        self.b1 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(1))
        self.b2 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(2))
        self.b3 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(3))       
        self.b4 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(4))
        self.b5 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(5))
        self.b6 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(6))
        self.b7 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(7))
        self.b8 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(8))
        self.b9 = Button(gameboardframe, text=' ', command=lambda: self.sendmoves(9))

        self.b1.grid(row= 0, column= 0)
        self.b2.grid(row= 0, column= 1)
        self.b3.grid(row= 0, column= 2)
        self.b4.grid(row= 1, column= 0)
        self.b5.grid(row= 1, column= 1)
        self.b6.grid(row= 1, column= 2)
        self.b7.grid(row= 2, column= 0)
        self.b8.grid(row= 2, column= 1)
        self.b9.grid(row= 2, column= 2)
        gameboardframe.pack(side=LEFT)


    #If Button on board is clicked
    def sendmoves(self, i):
        """sends moves to server, updates the gameboard, and checks for winners and ties
        
        """
        self.game.updateGameBoard(i, self.player1symbol)
        self.updateGUI(i, self.player1symbol)
        self.socket.sendall(str(i).encode())

        if self.game.isWinner("X") == True:
            self.printusernames.config(text = "Player X wins! \n Do you want to play again?")
            self.game.incrementWin()
            self.yesbutton = Button(self.askforuser, text = "YES", command= lambda: self.playagain())
            self.yesbutton.pack()
            self.nobutton = Button(self.askforuser, text = "NO", command= lambda: self.printstats())
            self.nobutton.pack()
        elif self.game.boardIsFull("X") or self.game.boardIsFull("O"):
            self.printusernames.config(text = "There's a Tie!\n Do you want to play again?")
            self.game.incrementTie()
            self.yesbutton = Button(self.askforuser, text = "YES", command= lambda: self.playagain())
            self.yesbutton.pack()
            self.nobutton = Button(self.askforuser, text = "NO", command= lambda: self.printstats())
            self.nobutton.pack()
        else:
            self.printusernames.config(text = "Player 2's turn")
            self.game.setLastplayer(str(self.getusername2()))

            self.waiting= False

            self.root.after(50, self.recievemoves)
            self.root.wait_variable(self.waiting)


    def recievemoves(self):
        """Recieves moves from the server and checks for winners and ties
        
        """
        self.player2move = self.socket.recv(self.RECV_SIZE).decode()
        self.updateGUI(self.player2move, self.player2symbol)
        self.game.updateGameBoard(self.player2move, self.player2symbol)

        if self.game.isWinner("O") == True:
            self.printusernames.config(text = "Player O wins!\n Do you want to play again?")
            self.game.incrementLoss()
            self.yesbutton = Button(self.askforuser, text = "YES", command= lambda: self.playagain())
            self.yesbutton.pack()
            self.nobutton = Button(self.askforuser, text = "NO", command= lambda: self.printstats())
            self.nobutton.pack()
        elif self.game.boardIsFull("X") or self.game.boardIsFull("O"):
            self.printusernames.config(text = "There's a Tie! \nDo you want to play again?")
            self.game.incrementTie()
            self.yesbutton = Button(self.askforuser, text = "YES", command= lambda: self.playagain())
            self.yesbutton.pack()
            self.nobutton = Button(self.askforuser, text = "NO", command= lambda: self.printstats())
            self.nobutton.pack()
        else:
            self.printusernames.config(text = "Player 1's turn")
            self.game.setLastplayer(str(self.getusername1()))

        
            self.waiting= True


    def updateGUI(self, playermove, playersymbol):
        """Updates the GUI game board
        
        """

        if int(playermove) == 1:
            self.b1.config(text = playersymbol)
            self.b1['state']= DISABLED
        elif int(playermove) == 2:
            self.b2.config(text = playersymbol)
            self.b2['state']= DISABLED
        elif int(playermove) == 3:
            self.b3.config(text = playersymbol)
            self.b3['state']= DISABLED
        elif int(playermove) == 4:
            self.b4.config(text = playersymbol)
            self.b4['state']= DISABLED
        elif int(playermove) == 5:
            self.b5.config(text = playersymbol)
            self.b5['state']= DISABLED
        elif int(playermove) == 6:
            self.b6.config(text = playersymbol)
            self.b6['state']= DISABLED
        elif int(playermove) == 7:
            self.b7.config(text = playersymbol)
            self.b7['state']= DISABLED
        elif int(playermove) == 8:
            self.b8.config(text = playersymbol)
            self.b8['state']= DISABLED
        elif int(playermove) == 9:
            self.b9.config(text = playersymbol)
            self.b9['state']= DISABLED
        else:
            pass

    def playagain(self):
        """Resets the GUI gameboard 
        
        """
        self.yesbutton.destroy()
        self.nobutton.destroy()
        self.game.incrementGamesplayed()
        self.game.resetGameBoard()
        self.b1['state'] = NORMAL
        self.b2['state'] = NORMAL
        self.b3['state'] = NORMAL
        self.b4['state'] = NORMAL
        self.b5['state'] = NORMAL
        self.b6['state'] = NORMAL
        self.b7['state'] = NORMAL
        self.b8['state'] = NORMAL
        self.b9['state'] = NORMAL
        self.b1.config(text=' ')
        self.b2.config(text=' ')
        self.b3.config(text=' ')
        self.b4.config(text=' ')
        self.b5.config(text=' ')
        self.b6.config(text=' ')
        self.b7.config(text=' ')
        self.b8.config(text=' ')
        self.b9.config(text=' ')

        self.socket.sendall(b'Play Again')
        self.askforuser.config(text= "Make a move \n then wait")

    def printstats(self):
        """Prints the stats 
        
        """

        self.nobutton.destroy()
        self.yesbutton.destroy()
        self.printusernames.config(text = f'\nYour Username: {self.getusername1()}\nLast person to make a move: {self.game.getLastplayer()}\nNumber of games played: {self.game.getGamesplayed()}\nNumber of Wins: {self.game.getWin()}\nNumber of Losses: {self.game.getLoss()}\nNumber of Ties: {self.game.getTie()}\n')
        self.socket.sendall(b'Fun times')
        self.askforuser.config(text= "Games Complete")
        self.__del__()
        


    def __del__(self):
        """Closes socket connection
        
        """
        self.socket.close()

def run_client():
    """Run the client
    
    """
    connection = Player1()

    connection.getHOST()
    connection.getPORT()
    connection.connectbutton()

    connection.root.mainloop()


if __name__ == "__main__":
    run_client()

