# GitHub username: Garbledorf
# Start Date: 03/02/2024
# Finish Date: 03/15/2024
# Description: Program runs a game of chess, full functionality with added
# fairy piece support.

class ChessVar:
    """
    Object for game of chess.
    """
    def __init__(self):
        """
        Initializes the game of chess
        - Generates Chess Board with 8x8 2D array
        - Sets turn count to be incremented
        - Sets player turn to 'white' to begin game
        - Algebraic notation set to allow movement between
          positions on game board. See get_move() for details
        - Runs game_start_generator()  
        """
        rows, cols = (8,8)
        self.__board = [[None for _ in range(cols)]for _ in range(rows)]
        self.__turn_count = 1
        self.__current_turn = "white"
        self.__algebraic_notation = {"A" : 0, "B" : 1, "C" : 2, "D" : 3, 
                                    "E" : 4, "F" : 5, "G" : 6, "H" : 7}
        self.__winner = "UNFINISHED"
        self.__fairy_pieces_used = []
        self.__captured_pieces = {'R' : 0, 'N' : 0, 'B' : 0, 'Q' : 0,
                                  'r' : 0, 'n' : 0, 'b' : 0, 'q' : 0}
        self.__white_req = 1
        self.__black_req = 1
        self.game_start_generator()

    def get_turn(self):
        """
        Sets turn for each player
        - Begins game on turn 1
        - odd numbered turns are white's turn
        - even numbered turns are black's turn
        """
        if self.__turn_count != 1:
            if self.__turn_count % 2 != 0:
                self.__current_turn = "white"
            else:
                self.__current_turn = "black"
        return self.__current_turn

    def get_notation(self):
        """
        Returns Notation Dict
        """    
        return self.__algebraic_notation
    
    def get_board(self):
        """
        Returns board
        """
        return self.__board

    def get_game_state(self):
        """
        Returns state of game
        - If Game is ongoing, return 'UNFINISHED'
        - If White has won, return 'WHITE_WON'
        - If Black has won, return 'BLACK_WON'
        """
        return self.__winner
        
    def make_move(self, move_from, move_to):
        """
        Takes in two strings, position to move from & position to move into
        Example: game.make_move('B2', 'B3')

        - Takes in position strings, then separates them into indexes
        - Letters are translated into algebraic notation, numbers are used
        as they are.
        - Method scans if move is legal. If not, returns False. Otherwise, moves
        piece.
        - Updates turn count, calls get_turn(), calls print_board()
        """
        if self.__winner != "UNFINISHED":
            return False

        turn = self.__current_turn
        move_from_notation = self.__algebraic_notation[move_from[0].upper()]
        move_to_notation = self.__algebraic_notation[move_to[0].upper()]

        if move_from_notation is None or move_to_notation is None:
            return False


        move_from_number, move_to_number = int(move_from[1]), int(move_to[1])

        if move_from_number < 1 or move_from_number > 8 or \
            move_to_number < 1 or move_to_number > 8:
            return False


        previous_move = self.__board[8 - move_from_number][move_from_notation]
        next_move = self.__board[8 - move_to_number][move_to_notation]
        
        # If ownership is incorrect
        if previous_move == None or turn != previous_move.color:
            return False
        
        # If friendly fire
        elif next_move != None and turn == next_move.color:
            return False

        # Check if there is a piece in the way
        if previous_move.color == 'white':
            direction = 1
        else:
            direction = -1

        # For diagonal movement
        delta_x = abs(move_to_number - move_from_number)
        delta_y = abs(move_to_notation - move_from_notation)

        if previous_move is not None and previous_move.name.upper() != 'N':
            if delta_x == delta_y:
                row_direction = 1 if move_to_number > move_from_number else -1
                col_direction = 1 if move_to_notation > move_from_notation else -1
                for i in range(1, abs(move_to_notation - move_from_notation)):
                    row = 8 - (move_from_number + row_direction * i)
                    col = move_from_notation + col_direction * i
                    if self.__board[row][col] is not None:
                        return False
            else:
                # For non-diagonal movement
                for i in range(1, delta_x):
                    row = 8 - (move_from_number + direction * i)
                    if self.__board[row][move_to_notation] is not None:
                        return False
        else:
            pass
        # Check if the move is legal using the move() method of the piece
        if not previous_move.move(previous_move, next_move, move_from_notation, 
                                  move_from_number, move_to_notation, move_to_number):
            return False
        
        else:
            # Move from position to new position
            if hasattr(previous_move, 'moved'):
                if previous_move.moved == False:
                    previous_move.moved = True

            if next_move is not None:
                if next_move.name == 'K':
                    self.__winner = 'BLACK_WON'

                if next_move.name == 'k':
                    self.__winner = 'WHITE_WON'
                
                if next_move.name in ['R', 'N', 'B', 'Q', 'r', 'n', 'b', 'q']:
                    self.__captured_pieces[next_move.name] += 1


            self.__board[8 - move_to_number][move_to_notation] = previous_move
            self.__board[8 - move_from_number][move_from_notation] = None
            

            self.__turn_count += 1
            self.get_turn()
        self.print_board()
        return True

    def enter_fairy_piece(self, fairy_piece, move_to):
        """
        Enters either Falcon or Hunter piece to specified 
        player's side. Can enter within that player's initial two rows.
        First fairy piece of player's choice may only be added
        after losing one rook, bishop, knight or queen.
        Second fairy piece of player's choice added after
        loss of second rook, bishop, knight or queen.
        Player isn't forced to add after losing a piece, can add 
        once anytime after.
        Method will take as parameters the piece to be added 
        and position to add to.
        """
        move_to_notation = self.__algebraic_notation[move_to[0].upper()]
        move_to_number = int(move_to[1])
        next_move = self.__board[8 - move_to_number][move_to_notation]

        if fairy_piece in self.__fairy_pieces_used:
            return False
        if next_move == None:
            if move_to_number == 1 or move_to_number == 2:
                for piece in self.__captured_pieces:
                    if self.__captured_pieces[piece] >= self.__white_req:
                        if fairy_piece == 'F':
                            obj_name = 'F'
                            obj = Falcon(obj_name, "white")
                            self.__board[8 - move_to_number][move_to_notation] = obj
                            self.__fairy_pieces_used.append(fairy_piece)
                            self.__white_req += 1

                        if fairy_piece == 'H':
                            obj_name = 'H'
                            obj = Hunter(obj_name, "white")
                            self.__board[8 - move_to_number][move_to_notation] = obj
                            self.__fairy_pieces_used.append(fairy_piece)
                            self.__white_req += 1
                        self.__turn_count += 1
                        self.get_turn()
                        self.print_board()
                        return True

            if move_to_number == 8 or move_to_number == 7:
                for piece in self.__captured_pieces:
                    if self.__captured_pieces[piece] >= self.__black_req:  
                        if fairy_piece == 'f':
                            obj_name = 'f'
                            obj = Falcon(obj_name, "black")
                            self.__board[8 - move_to_number][move_to_notation] = obj
                            self.__fairy_pieces_used.append(fairy_piece)
                            self.__black_req += 1

                        if fairy_piece == 'h':
                            obj_name = 'h'
                            obj = Hunter(obj_name, "black")
                            self.__board[8 - move_to_number][move_to_notation] = obj
                            self.__fairy_pieces_used.append(fairy_piece)
                            self.__black_req += 1
                        self.__turn_count += 1
                        self.get_turn()
                        self.print_board()
                        return True
        return False

    def print_board(self):
        """
        Prints board for player usage.
        - Updates positions on board if there are any changes
        - If a cell is occupied, update cell with object, else print '| |'
        """
        print("\n       TURN COMPLETE\n")
        print("           BLACK")
        numbers = [8,7,6,5,4,3,2,1]
        count = 0
        for row in self.__board:
            print(numbers[count], end=" ")
            # Prints position of 
            print("".join([f"|{cell.name}|" if cell is not None else "| |" for cell in row]))
            count += 1
        print("   A  B  C  D  E  F  G  H")
        print("           WHITE")
        print(f"\n           TURN {self.__turn_count}") 
        print(f"        {self.__current_turn.upper()}'S TURN")
                
    def game_start_generator(self, side = "white"):
        """
        Generates the board at the start of the game
        - Parameter Side defaulted to white to generate white side first
        - Generates each piece in for loops, sets position on board
          depending on which side is currently generated
        - Recursively calls itself once to switch the side to 'black',
          then starting the generation again for black's pieces.
        - After generation, prints board for user.
        """
        # Generation
        # Pawn Generation
        for i in range(8):
            if side == "white":
                obj_name = "P"
                obj = Pawn(obj_name, side)
                self.__board[6][i - 1] = obj
            else:
                obj_name = "p"
                obj = Pawn(obj_name, side)
                self.__board[1][i - 1] = obj

        # Rook Generation
        for i in range(2):
            if side == "white":
                obj_name = "R"
                obj = Rook(obj_name, side)
                if i > 0:
                    self.__board[7][7] = obj
                else:
                    self.__board[7][0] = obj
            else:
                obj_name = "r"
                obj = Rook(obj_name, side)
                if i > 0:
                    self.__board[0][0] = obj
                else:
                    self.__board[0][7] = obj
        
        # Knight Generation
        for i in range(2):
            if side == "white":
                obj_name = "N"
                obj = Knight(obj_name, side)
                if i > 0:
                    self.__board[7][1] = obj
                else:
                    self.__board[7][6] = obj
            else:
                obj_name = "n"
                obj = Knight(obj_name, side)
                if i > 0:
                    self.__board[0][1] = obj
                else:
                    self.__board[0][6] = obj

        # Bishop Generation
        for i in range(2):
            if side == "white":
                obj_name = "B"
                obj = Bishop(obj_name, side)
                if i > 0:
                    self.__board[7][2] = obj
                else:
                    self.__board[7][5] = obj
            else:
                obj_name = "b"
                obj = Bishop(obj_name, side)
                if i > 0:
                    self.__board[0][2] = obj
                else:
                    self.__board[0][5] = obj

        # King & Queen Generation
            if side == "white":
                obj_name = "K"
                obj = King(obj_name, side)
                self.__board[7][4] = obj

                obj_name = "Q"
                obj = Queen(obj_name, side)
                self.__board[7][3] = obj

            else:
                obj_name = "k"
                obj = King(obj_name, side)
                self.__board[0][4] = obj

                obj_name = "q"
                obj = Queen(obj_name, side)
                self.__board[0][3] = obj
            
        # Switch sides after white
        if side == "white":
            return ChessVar.game_start_generator(self, side = "black")
        else:
            self.print_board()       

class ChessPiece():
    """
    Parent class for all pieces
    - self.name sets name of chess piece
    - self.color sets side of each piece
    """
    def __init__(self, name, color):
        self.name = name
        self.color = color
        
class Pawn(ChessPiece):
    """
    Class for Pawns, inherits ChessPiece
    """
    def __init__(self, name, color):
        """
        - self.moved checks if specific pawn has already moved. 
          If it hasn't, pawn can move 2 tiles. Else, 1 tile.
        - self.movement initialized to 1 movement.
        """
        super().__init__(name, color)
        self.moved = False
        self.movement = 1
        
    def move(self, previous_move, next_move, move_from_notation,
             move_from_number, move_to_notation, move_to_number):
        """
        Defines legal moves for this piece
        - Moves forward one square. If it hasn't moved yet, may move two squares forward instead.
        Captures diagonally in either direction in front of it.
        """
        if next_move is None:
            if move_to_notation != move_from_notation:
                return False

        if self.color == 'white':
            if move_to_number - move_from_number > 1:
                if self.moved:
                    return False
                elif move_to_number - move_from_number > 2:
                    return False
            if move_to_number < move_from_number:
                return False
        elif self.color == 'black':
            if move_from_number - move_to_number > 1:
                if self.moved:
                    return False
                elif move_from_number - move_to_number > 2:
                    return False
            if move_to_number > move_from_number:
                return False
            
        delta_x = abs(move_to_number - move_from_number)
        delta_y = abs(move_to_notation - move_from_notation)

        if next_move is not None:
            if next_move.color != self.color:
                if delta_x != delta_y:
                    return False
        if next_move is None:
            if delta_x == delta_y:
                return False
        return True

class Bishop(ChessPiece):
    """
    Class for Bishops, inherits ChessPiece
    """
    def __init__(self, name, color):
        super().__init__(name, color)
    
    def move(self, previous_move, next_move, move_from_notation,
             move_from_number, move_to_notation, move_to_number):
        """
        Defines legal moves for this piece
        - Moves any number of squares diagonally
        """
        
        delta_x = abs(move_to_number - move_from_number)
        delta_y = abs(move_to_notation - move_from_notation)
        
        if delta_x != delta_y:
            return False
        return True

class Knight(ChessPiece):
    """
    Class for Knights, inherits ChessPiece
    """
    def __init__(self, name, color):
        super().__init__(name, color)
    
    def move(self, previous_move, next_move, move_from_notation,
             move_from_number, move_to_notation, move_to_number):
        """
        Defines legal moves for this piece
        - Moves two squares straight, then one square perpendicular 
        in an L-Shape
        """

        delta_x = abs(move_from_notation - move_to_notation)
        delta_y = abs(move_from_number - move_to_number)
        
        if (delta_x == 1 and delta_y == 2) or (delta_x == 2 and delta_y == 1):
            return True
        else:
            return False

class Rook(ChessPiece):
    """
    Class for Rooks, inherits ChessPiece
    """
    def __init__(self, name, color):
        super().__init__(name, color)
    
    def move(self, previous_move, next_move, move_from_notation,
             move_from_number, move_to_notation, move_to_number):
        """
        Defines legal moves for this piece
        - Moves any number of squares horizontally or vertically
        """
        delta_x = abs(move_to_number - move_from_number)
        delta_y = abs(move_to_notation - move_from_notation)
        
        if delta_x == delta_y:
            return False
        return True

class Queen(ChessPiece):
    """
    Class for Queens, inherits ChessPiece
    """
    def __init__(self, name, color):
        super().__init__(name, color)
    
    def move(self, previous_move, next_move, move_from_notation,
             move_from_number, move_to_notation, move_to_number):
        """
        Defines legal moves for this piece
        - Moves any number of squares horizontally, vertically or diagonally
        """
        delta_x = abs(move_to_number - move_from_number)
        delta_y = abs(move_to_notation - move_from_notation)
        
        if delta_x != 0 and delta_y != 0 and delta_x != delta_y:
            return False
        return True

class King(ChessPiece):
    """
    Class for Kings, inherits ChessPiece
    """
    def __init__(self, name, color):
        super().__init__(name, color)
    
    def move(self, previous_move, next_move, move_from_notation,
             move_from_number, move_to_notation, move_to_number):
        """
        Defines legal moves for this piece
        - Moves one square in any direction
        """
        delta_x = abs(move_to_number - move_from_number)
        delta_y = abs(move_to_notation - move_from_notation)
        
        if delta_x > 1 or delta_y > 1:
            return False
        return True

class Falcon(ChessPiece):
    """
    Class for Falcons, inherits ChessPiece
    """
    def __init__(self, name, color):
        super().__init__(name, color)
    
    def move(self, previous_move, next_move, move_from_notation,
             move_from_number, move_to_notation, move_to_number):
        """
        Defines legal moves for this piece
        - Moves forward like a Bishop
        - Moves backward like a Rook
        """
        delta_x = abs(move_to_number - move_from_number)
        delta_y = abs(move_to_notation - move_from_notation)
        if self.color == 'white':
            if move_to_number < move_from_number:
                if delta_x == delta_y:
                    return False
                
            if move_to_number > move_from_number:
                if delta_x != delta_y:
                    return False

        if self.color == 'black':
            if move_to_number > move_from_number:
                if delta_x != delta_y:
                    return False
                
            if move_to_number < move_from_number:
                if delta_x == delta_y:
                    return False    
        return True

class Hunter(ChessPiece):
    """
    Class for Hunters, inherits ChessPiece
    """
    def __init__(self, name, color):
        super().__init__(name, color)

    def move(self, previous_move, next_move, move_from_notation,
             move_from_number, move_to_notation, move_to_number):
        """
        Defines legal moves for this piece
        - Moves forward like a Rook
        - Moves backward like a Bishop
        """
        delta_x = abs(move_to_number - move_from_number)
        delta_y = abs(move_to_notation - move_from_notation)
        if self.color == 'white':
            if move_to_number < move_from_number:
                if delta_x != delta_y:
                    return False
                
            if move_to_number > move_from_number:
                if delta_x == delta_y:
                    return False

        if self.color == 'black':
            if move_to_number > move_from_number:
                if delta_x == delta_y:
                    return False
                
            if move_to_number < move_from_number:
                if delta_x != delta_y:
                    return False    
        return True