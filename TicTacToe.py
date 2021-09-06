class TicTacToe():
    def __init__(self, play_mode):
        self.play_mode = play_mode
        self.player_marker = " "
        self.number_board = [ ["1","2","3"] , ["4","5","6"] ,["7","8","9"] ]
        self.play_board = [ ["_","_","_"] , ["_","_","_"] ,["_","_","_"] ]
        self.last_player = "Player 1"
        self.flag_end_game = False

    def check_win_conditions(self, current_board):
        if (current_board[0][0] == current_board[0][1] and current_board[0][0] == current_board[0][2] or 
            current_board[1][0] == current_board[1][1] and current_board[1][0] == current_board[1][2] or 
            current_board[2][0] == current_board[2][1] and current_board[2][0] == current_board[2][2] or
            current_board[0][0] == current_board[1][0] and current_board[0][0] == current_board[2][0] or
            current_board[0][1] == current_board[1][1] and current_board[0][1] == current_board[2][1] or 
            current_board[0][2] == current_board[1][2] and current_board[0][2] == current_board[2][2] or
            current_board[0][0] == current_board[1][1] and current_board[0][0] == current_board[2][2] or
            current_board[0][2] == current_board[1][1] and current_board[0][2] == current_board[2][0]):

            print(f"Congratulations! {self.last_player} won!")

            self.flag_end_game = True

    def intro_messages(self):
        print("Welcome to tic-tac-toe python v0.01!")

        if self.play_mode == "2P":
            print("You selected two-player mode.")
        
        print("In order to play, you need to input letters according to the following board: ")

        print(["1","2","3"])
        print(["4","5","6"]) 
        print(["7","8","9"])

    def game(self):
        self.intro_messages()

        for i in range(9):
            if i % 2 == 0: #odd turns
                self.last_player = "Player 1"
                self.player_marker = "x"
            if i % 2 == 1: #even turns
                self.last_player = "Player 2"
                self.player_marker = "o"

            selection_player_1 = input(f"{self.last_player} , choose a number between 1-9 to play according to the board: ")

            #update choice upon board
            if selection_player_1 == "1":
                self.play_board[0][0] = self.player_marker
                self.number_board[0][0] = self.player_marker
            elif selection_player_1 == "2":
                self.play_board[0][1] = self.player_marker
                self.number_board[0][1] = self.player_marker
            elif selection_player_1 == "3":
                self.play_board[0][2] = self.player_marker
                self.number_board[0][2] = self.player_marker
            elif selection_player_1 == "4":
                self.play_board[1][0] = self.player_marker
                self.number_board[1][0] = self.player_marker
            elif selection_player_1 == "5":
                self.play_board[1][1] = self.player_marker
                self.number_board[1][1] = self.player_marker
            elif selection_player_1 == "6":
                self.play_board[1][2] = self.player_marker
                self.number_board[1][2] = self.player_marker
            elif selection_player_1 == "7":
                self.play_board[2][0] = self.player_marker
                self.number_board[2][0] = self.player_marker
            elif selection_player_1 == "8":
                self.play_board[2][1] = self.player_marker
                self.number_board[2][1] = self.player_marker
            elif selection_player_1 == "9":
                self.play_board[2][2] = self.player_marker
                self.number_board[2][2] = self.player_marker
            
            #display updated board
            print(self.play_board[0])
            print(self.play_board[1])
            print(self.play_board[2])

            #check if win condition was met
            self.check_win_conditions(self.number_board)
            if self.flag_end_game:
                break

if __name__ == '__main__':
    play_2p = TicTacToe("2P")
    play_2p.game()
            