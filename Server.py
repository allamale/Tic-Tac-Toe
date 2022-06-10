import socket
from gameboardUI import BoardClass
from tkinter import *
from tkinter.ttk import Button
from time import *

#Player 2 = server (provides host information to player 1)

#class for player1
class Player2: 

    def __init__(self, username1: str = '', username2: str= '', HOST: str = '', PORT = ''):
        """Attributes for player1 class (connection, sockets, exchange usernames)"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root = Tk()
        self.game = BoardClass()
        self.con = None
        self.addr = None
        self.canvas()
        self.HOST= HOST
        self.PORT= PORT
        self.username1 = username1
        self.username2 = username2
        self.RECV_SIZE = 1024
        self.player2symbol = "O"
        self.player1symbol = "X"
        self.waiting = False

        self.isconnected = False


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
        """Creates the window for tkinter.
        
        """
        self.root.geometry('500x300')
        self.root.title("Player2")


        self.userinputframe= Frame(self.root, bg = 'pink')
        self.userinputframe.pack(side= TOP)

    def getHOST(self):
        """Gets the host and creates the host entry widget 
        
        Returns: None 
        """

        h = Label(self.userinputframe, text = "Enter in a Host Name: ")
        h.pack(side=TOP)

        self.HOST = Entry(self.userinputframe, width=20)
        self.HOST.pack()
        self.HOST.insert(0, '')


    def getPORT(self):
        """Gets the Port and creates the Port entry widget 
        
        """
        p = Label(self.userinputframe, text = "Enter in a Port #: ")
        p.pack(side=BOTTOM)

        self.PORT = Entry(self.userinputframe, width=20)
        self.PORT.pack()
        self.PORT.insert(0, '')

    def connectbutton(self):
        """Creates the connection button and quit button
        
        """
        self.connButt = Button(self.userinputframe, text = "Connect", command=self.connecttoclient)
        self.connButt.pack()
        
        self.leaveBUTT = Button(self.userinputframe, text = "Quit", command= lambda: self.leave())
        self.leaveBUTT.pack()

    def leave(self):
        """If user clicks on the quit button then it will destroy the window
        
        """
        self.root.destroy

    def connecttoclient(self):
        """Connects to the client and recieved client username 
        
        """
        self.socket.bind( (self.HOST.get(), int(self.PORT.get()) ))

        self.socket.listen()

        self.con, self.addr = self.socket.accept()

        self.leaveBUTT.destroy()
        self.connButt.destroy()
        self.isconnected = True

        self.usernameplayer1 = self.con.recv(self.RECV_SIZE).decode()
        self.setusername1(str(self.usernameplayer1))

        self.getusername()

    def getusername(self):
        """Gets username from the server and creates entry widget for username
        
        """
        self.usernameframe = Frame(self.root, bg = 'pink')
        self.usernameframe.pack(side=BOTTOM)


        self.askforuser = Label(self.usernameframe, text = "Successful Connection!\n" + "Enter in a username: ")
        self.askforuser.pack(side=LEFT)
        self.askforuserenter = Entry(self.usernameframe, width=20)
        self.askforuserenter.pack()
        
        self.submitusernameBUTT = Button(self.usernameframe, text = "Submit username", command = self.submitusername)
        self.submitusernameBUTT.pack(side=RIGHT)

    def submitusername(self):
        """Tests for valid username input and then prints the board 
        
        """
        try:
            if not self.askforuserenter.get().strip().isalnum():
                raise ValueError

        except ValueError:
            self.badname = Label(self.usernameframe, text = "invalid username").pack(side=BOTTOM)
            return

        self.setusername2(str(self.askforuserenter.get()))
        self.goodname = Label(self.usernameframe, text = "Nice name!").pack(side=BOTTOM)
        self.con.sendall(self.askforuserenter.get().encode())
        self.submitusernameBUTT.destroy()
        self.printgameboard()
        self.printnames()
        self.game.updateGamesPlayed()

    def printnames(self):
        """Gets a valid username and then prints the names of the players 
        
        """
        self.printusernamesframe = Frame(self.root, bg = 'pink')
        self.printusernamesframe.pack(side= RIGHT)

        self.printusernames = Label(self.printusernamesframe, text = " Welcome to tictactoe!\n" + str(self.getusername2()) + "  and  " + str(self.getusername1()) + " Player 2's turn")
        self.printusernames.pack()

    def printgameboard(self):
        """Prints the gameboard 
        
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
        self.b6.grid(row=1, column = 2)
        self.b7.grid(row= 2, column= 0)
        self.b8.grid(row=2, column = 1)
        self.b9.grid(row= 2, column= 2)
        
        gameboardframe.pack(side=LEFT)

        self.recievemoves()

    #If Button on board is clicked
    def sendmoves(self, i):
        """ sends moves to player 1 and also checks for winner and ties and prints stats
        
        """
        self.game.updateGameBoard(i, self.player2symbol)
        self.updateGUIboard(i, self.player2symbol)
        self.con.sendall(str(i).encode())

        if self.game.isWinner("O") == True:
            self.askforuser.config(text = "Player O wins!")
            self.game.incrementWin()
            playagain= self.con.recv(self.RECV_SIZE).decode()
            if str(playagain) == "Play Again":
                self.printusernames.config(text = "Play Again")
                self.playagain()
            if str(playagain) == "Fun times":
                self.askforuser.config(text = "Fun times")
                self.printusernames.config(text = f'\nYour Username: {self.getusername2()}\nLast person to make a move: {self.game.getLastplayer()}\nNumber of games played: {self.game.getGamesplayed()}\nNumber of Wins: {self.game.getWin()}\nNumber of Losses: {self.game.getLoss()}\nNumber of Ties: {self.game.getTie()}\n')
                self.__del__()
        elif self.game.boardIsFull("X") or self.game.boardIsFull("O"):
            self.askforuser.config(text = "There's a Tie!")
            self.game.incrementTie()
            playagain= self.con.recv(self.RECV_SIZE).decode()
            if str(playagain) == "Play Again":
                self.printusernames.config(text = "Play Again")
                self.playagain()
            if str(playagain) == "Fun times":
                self.askforuser.config(text = "Fun times")
                self.printusernames.config(text = f'\nYour Username: {self.getusername2()}\nLast person to make a move: {self.game.getLastplayer()}\nNumber of games played: {self.game.getGamesplayed()}\nNumber of Wins: {self.game.getWin()}\nNumber of Losses: {self.game.getLoss()}\nNumber of Ties: {self.game.getTie()}\n')
                self.__del__()
        else:
            self.askforuser.config(text = "Player 1's turn")
            self.game.setLastplayer(str(self.getusername1()))

        
            self.waiting= False

            self.root.after(50, self.recievemoves)
            self.root.wait_variable(self.waiting)


    def recievemoves(self):
        """Recieves moves here and checks for winners and ties and prints stats 
        
        """
        self.player1move = self.con.recv(self.RECV_SIZE).decode()
        self.updateGUIboard(self.player1move, self.player1symbol)
        self.game.updateGameBoard(self.player1move, self.player1symbol)
        
        if self.game.isWinner("X") == True:
            self.askforuser.config(text = "Player X wins!")
            self.game.incrementLoss()
            playagain= self.con.recv(self.RECV_SIZE).decode()
            if str(playagain) == "Play Again":
                self.printusernames.config(text = "Play Again")
                self.playagain()
            if str(playagain) == "Fun times":
                self.askforuser.config(text = "Fun times")
                self.printusernames.config(text = f'\nYour Username: {self.getusername2()}\nLast person to make a move: {self.game.getLastplayer()}\nNumber of games played: {self.game.getGamesplayed()}\nNumber of Wins: {self.game.getWin()}\nNumber of Losses: {self.game.getLoss()}\nNumber of Ties: {self.game.getTie()}\n')
                self.__del__()
        elif self.game.boardIsFull("X") or self.game.boardIsFull("O"):
            self.askforuser.config(text = "There's a Tie!")
            self.game.incrementTie()
            playagain= self.con.recv(self.RECV_SIZE).decode()
            if str(playagain) == "Play Again":
                self.printusernames.config(text = "Play Again")
                self.playagain()
            if str(playagain) == "Fun times":
                self.askforuser.config(text = "Fun times")
                self.printusernames.config(text = f'\nYour Username: {self.getusername2()}\nLast person to make a move: {self.game.getLastplayer()}\nNumber of games played: {self.game.getGamesplayed()}\nNumber of Wins: {self.game.getWin()}\nNumber of Losses: {self.game.getLoss()}\nNumber of Ties: {self.game.getTie()}\n')
                self.__del__()
        else:
            self.askforuser.config(text = "Player 2's turn")
            self.game.setLastplayer(str(self.getusername2()))


        
            self.waiting= True


    def updateGUIboard(self, playermove, playersymbol):
        """Updates the GUI board
        
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
        """Resets the GUI Board
        
        """
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

        self.recievemoves()

    def __del__(self):
        """Closes the connection
        
        """
        self.con.close()


def run_server():
    """Runs the server
    
    """
    connection = Player2()

    connection.getHOST()
    connection.getPORT()
    connection.connectbutton()

    connection.root.mainloop()


if __name__ == "__main__":
    run_server()
