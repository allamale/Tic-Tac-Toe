from tkinter import *

class BoardClass:

    def __init__(self, username: str = "", lastplayer: str = "", win: int = 0, tie: int = 0, loss: int = 0, gamesplayed: int = 0, board: list = []):
        """Makes a BoardClass.

        Attributes:
            username (str): Players user name
            lastplayer (str): User name of the last player to have a turn
            win (int): Number of wins
            tie (int): Number of ties
            loss (int): Number of losses
            gamesplayed (int): Number of gamesplayed in total
            board (list): nested list 
        """
        
        self.setUsername(username) 
        self.setLastplayer(lastplayer)
        self.win = win
        self.tie = tie
        self.loss = loss
        self.gamesplayed = gamesplayed
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    #Setting, Getting, and Incrementing Variables/Attributes
        
    def setUsername(self, username: str):
        """set the name of the User.

        Args:
            username: Players user name
        """
        self.username = username

    def setLastplayer(self, lastplayer: str):
        """set the username of the player who's turn was last.

        Args:
            lastplayer: User name of the last player to have a turn
        """
        self.lastplayer = lastplayer

    def getUsername(self):
        """Get the username of the player.

        Returns: players username
        """
        return self.username

    def getLastplayer(self):
        """Get the user name of the last player to have a turn.

        Returns: last player's username
        """
        return self.lastplayer

    def incrementWin(self):
        """Increment the times of Wins a player has by 1 if a player wins a game.

        """
        self.win += 1

    def getWin(self):
        """Get the total number of wins a player has.

        """
        return self.win

    def incrementTie(self):
        """Increment the times of Ties a player has by 1 if a player ties a game.

        """
        self.tie += 1

    def getTie(self):
        """Get the total number of ties a player has.

        """
        return self.tie

    def incrementLoss(self):
        """Increment the times of Losses a player has by 1 if a player losses a game.

        """
        self.loss += 1

    def getLoss(self):
        """Get the total number of losses a player has.

        """
        return self.loss
    
    def getGamesplayed(self):
        """Get the total number of games that have been played.

        """
        return self.gamesplayed

    def incrementGamesplayed(self):
        """Increment the number of times a game has started.

        """
        self.gamesplayed += 1


    #Required Functions for the Game

    def updateGamesPlayed(self):
        """Keeps track how many games have started.

            Returns: None
        """
        self.incrementGamesplayed()
        
    def resetGameBoard(self):
        """Clear all the moves from game board.

            Returns: None
        """
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    
    def updateGameBoard(self, playermove, playersymbol):
        """Updates the game board with the player's move.

            Args:
            playermove: coordinate of the point on the board where the player wants their symbol
            playersymbol: symbol representing the player (x/X or o/O)
            
            Returns: None
        """

        if int(playermove) == 1:
            self.board[0][0] = playersymbol
        elif int(playermove) == 2:
            self.board[0][1] = playersymbol
        elif int(playermove) == 3:
            self.board[0][2] = playersymbol
        elif int(playermove) == 4:
            self.board[1][0] = playersymbol
        elif int(playermove) == 5:
            self.board[1][1] = playersymbol
        elif int(playermove) == 6:
            self.board[1][2] = playersymbol
        elif int(playermove) == 7:
            self.board[2][0] = playersymbol
        elif int(playermove) == 8:
            self.board[2][1] = playersymbol
        elif int(playermove) == 9:
            self.board[2][2] = playersymbol
        else:
            pass

    def isWinner(self, playersymbol):
        """Checks if the latest move resulted in a win
            Updates the wins and losses count.

            Args:
            playersymbol: symbol representing the player (x/X or o/O)

            Returns: Boolean Value
            
        """

        #check horizontally 
        winner = False
        for r in range(len(self.board)):
            if self.board[r] == [playersymbol, playersymbol, playersymbol]:
                winner = True

        #check vertically
        for r in range(len(self.board)):
            cnt = 0
            for c in range(len(self.board[0])):
                if self.board[c][r] == playersymbol:
                    cnt += 1
            if cnt == 3:
                winner = True
                break
        
        #check diagonally from the left side
        cnt = 0
        for r in range(len(self.board)):
            if self.board[r][r] == playersymbol:
                cnt += 1
        if cnt == 3:
            winner = True

        #check diagonally from the right side (reversed)
        cnt = 0
        for r in range(len(self.board)):
            if self.board[len(self.board) - r - 1][r] == playersymbol:
                cnt += 1

        if cnt == 3:
            winner = True

        if winner:
            # print("Player", playersymbol, "wins!")
            return winner
        
        return winner

                
    def boardIsFull(self, playersymbol):
        """Checks if the board is full (I.e. no more moves to make - tie)
            Updates the ties count.

            Args:
            playersymbol: symbol representing the player (x/X or o/O)
            
            Returns: Boolean Value
        """
        
        cnt = 0
        tie = False
        if self.isWinner(playersymbol) == False: 
            for r in range(len(self.board)):
                for x in range(len(self.board)):
                    if self.board[r][x] == " " or self.board[r][x] == "":
                        cnt += 1
        
                if cnt == 0:
                    tie = True
                else:
                    tie = False
        else:
            pass
        
        # if tie:
            # print("Game Over, there's a tie!")
        # else:
        #     pass
        
        return tie


    def printStats(self):
        """Prints the following each on a new line:

                Prints the players user name
                Prints the user name of the last person to make a move
                Prints the number of games
                Prints the number of wins
                Prints the number of losses
                Prints the number of ties

            Returns: String
        """

        return f'\nYour Username: {self.getUsername()}\nLast person to make a move: {self.getLastplayer()}\nNumber of games played: {self.getGamesplayed()}\nNumber of Wins: {self.getWin()}\nNumber of Losses: {self.getLoss()}\nNumber of Ties: {self.getTie()}\n'




            
            