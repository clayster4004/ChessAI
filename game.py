# Final Project - Chess - CIS 163
# Prof. Ira Woodring
# Created by Clay Beal
# - in association with Zachary Bauer
from typing import Optional
import random

from piece_model import Color, Rook, King, Knight, Queen, Bishop, Pawn, Piece


class Game:
    """
    The game class is a blueprint for creating the chess game. It does things
    like set up pieces, keeps track of the current player and keeps track of
    prior states of the board
    Attributes:
        _board (list): Holds the current 2-d list of pieces on the board
        current_player (Enum): Holds the color enum for the current player
        _prior_states (list): Holds the prior states of the board via stack
    """
    def __init__(self) -> None:
        """
        Creates the board, sets up the pieces, sets the color to white, and
        creates the prior stack
        """
        self._board = self._setup_pieces()
        self.current_player = Color.WHITE
        self._prior_states = []

    def reset(self) -> None:
        """
        Resets the game to the state it was initialized as
        """
        self._board = self._setup_pieces()
        self.current_player = Color.WHITE
        self._prior_states = []

    def _setup_pieces(self):
        """
        Creates the pieces, gives them the same game instance and puts
        them on the board in the correct locations
        Returns:
            (list): 2-d that is the board for the chess game
        :return:
        """
        r1 = Rook(Color.BLACK)
        r1._game = self

        k1 = Knight(Color.BLACK)
        k1._game = self

        b1 = Bishop(Color.BLACK)
        b1._game = self

        q1 = Queen(Color.BLACK)
        q1._game = self

        king1 = King(Color.BLACK)
        king1._game = self

        b2 = Bishop(Color.BLACK)
        b2._game = self

        k2 = Knight(Color.BLACK)
        k2._game = self

        r2 = Rook(Color.BLACK)
        r2._game = self

        p1 = Pawn(Color.BLACK)
        p2 = Pawn(Color.BLACK)
        p3 = Pawn(Color.BLACK)
        p4 = Pawn(Color.BLACK)
        p5 = Pawn(Color.BLACK)
        p6 = Pawn(Color.BLACK)
        p7 = Pawn(Color.BLACK)
        p8 = Pawn(Color.BLACK)
        p1._game = self
        p2._game = self
        p3._game = self
        p4._game = self
        p5._game = self
        p6._game = self
        p7._game = self
        p8._game = self

        P1 = Pawn(Color.WHITE)
        P2 = Pawn(Color.WHITE)
        P3 = Pawn(Color.WHITE)
        P4 = Pawn(Color.WHITE)
        P5 = Pawn(Color.WHITE)
        P6 = Pawn(Color.WHITE)
        P7 = Pawn(Color.WHITE)
        P8 = Pawn(Color.WHITE)
        P1._game = self
        P2._game = self
        P3._game = self
        P4._game = self
        P5._game = self
        P6._game = self
        P7._game = self
        P8._game = self

        R1 = Rook(Color.WHITE)
        R1._game = self

        K1 = Knight(Color.WHITE)
        K1._game = self

        B1 = Bishop(Color.WHITE)
        B1._game = self

        Q1 = Queen(Color.WHITE)
        Q1._game = self

        king2 = King(Color.WHITE)
        king2._game = self

        B2 = Bishop(Color.WHITE)
        B2._game = self

        K2 = Knight(Color.WHITE)
        K2._game = self

        R2 = Rook(Color.WHITE)
        R2._game = self

        return [
            [r1, k1, b1, q1, king1, b2, k2, r2],
            [p1, p2, p3, p4, p5, p6, p7, p8],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [P1, P2, P3, P4, P5, P6, P7, P8],
            [R1, K1, B1, Q1, king2, B2, K2, R2]
        ]

    def get(self, y: int, x: int) -> Optional[Piece]:
        """
        Will return the piece object when given a coordinate
        Parameters:
            y (int): y coordinate of the location
            x (int): x coordinate of the location
        Returns:
            (Piece): returns the piece object if it exists at (y,x)
        """
        try:
            if isinstance(self._board[y][x], Piece):
                return self._board[y][x]
        except IndexError:
            return None

    def switch_player(self) -> None:
        """
        Switches the current player
        """
        if self.current_player == Color.WHITE:
            self.current_player = Color.BLACK
        else:
            self.current_player = Color.WHITE

    def undo(self) -> bool:
        """
        Undoes the board twice (1 move from both pieces)
        Returns:
            (bool): True upon completion
        """
        for _ in range(2):
            previous_board = self._prior_states.pop()
            self._board = previous_board
        return True

    def copy_board(self):
        """
        Preforms a deepcopy of the board to put on the stack after moves
        have been made
        _copy (list): a deepcopy of the board after a move has been made
        """
        self._copy = [[None for _ in range(8)] for _ in range(8)]
        # Loops over the entire current board and copies each piece onto a
        # new board
        for i in range(8):
            for j in range(8):
                if self._board[i][j] is not None:
                    new_piece = self._board[i][j].copy()
                    new_piece._game = self
                    self._copy[i][j] = new_piece

        return self._copy

    def move(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        """
        This function will move a designated piece to a new specific location
        on the board and return True if it did not put them in check to do so,
        otherwise returns False.
        Parameters:
            piece (Piece): piece object being moved
            y (int): current piece y coordinate
            x (int): current piece x coordinate
            y2 (int): desired piece y coordinate
            x2 (int): desired piece x coordinate
        Returns:
            (bool) - True if the move did not put the user in check, otherwise
                     False
        """
        self._prior_states.append(self.copy_board())

        self._board[y2][x2] = self._board[y][x]
        self._board[y][x] = None
        # Have to keep track if a pawn has moved at least once
        if isinstance(piece, Pawn):
            piece.moved = True
        # If the move put you in check, undo it and return False
        if self.check(piece.color):
            previous_board = self._prior_states.pop()
            self._board = previous_board
            return False

        # Promote to Queen if pawn reaches opposite side of board
        if isinstance(piece, Pawn) and piece.color == Color.WHITE:
            for i in range(8):
                if self._board[0][i] == piece:
                    self._board[0][i] = Queen(Color.WHITE)
                    self._board[0][i]._game = self
        if isinstance(piece, Pawn) and piece.color == Color.BLACK:
            for i in range(8):
                if self._board[7][i] == piece:
                    self._board[7][i] = Queen(Color.BLACK)
                    self._board[7][i]._game = self

        self.switch_player()
        return True

    def get_piece_locations(self, color: Color) -> list[tuple[int, int]]:
        """
        Gets all the specific piece locations based on the color of the piece
        Parameter:
            color (Color): passed in color enum to get piece locations from
        Returns:
            piece_locations (list): list of tuples holding the piece locations
                                    from the passed in color
        """
        piece_locations = []
        for i in range(len(self._board)):
            for j in range(len(self._board)):
                if self._board[i][j] is not None:
                    if self._board[i][j].color == color:
                        piece_locations.append((i, j))
        return piece_locations

    def find_king(self, color: Color) -> tuple[int, int]:
        """
        Gives the coordinate of the king of passed in color
        Parameter:
            color (Color): passed in color enum to get king location from
        Returns:
            (tuple): king coordinated in form of tuple
        """
        for i in range(len(self._board)):
            for j in range(len(self._board)):
                if isinstance(self._board[i][j], King):
                    if self._board[i][j].color == color:
                        return (i, j)

    def check(self, color: Color) -> bool:
        """
        Checks to see if the passed in color is in check
        Parameters:
            color (Color): passed in color enum to see if king in check
        Returns:
            (bool): True if king in check, otherwise False
        """
        # Gets piece locations from passed in color
        valid_moves = []
        # Locations are a list of tuples
        if color == Color.WHITE:
            piece_locations = self.get_piece_locations(Color.BLACK)
        else:
            piece_locations = self.get_piece_locations(Color.WHITE)

        # Gets the valid moves for the passed in colors pieces
        for i in piece_locations:
            # "i" is the first tuple
            valid_moves += self._board[i[0]][i[1]].valid_moves(i[0], i[1])

        # If the king of one color is in the valid moves of the other color
        # then they are in check
        if color == Color.WHITE:
            if self.find_king(Color.WHITE) in valid_moves:
                return True
        if color == Color.BLACK:
            if self.find_king(Color.BLACK) in valid_moves:
                return True
        return False

    def mate(self, color) -> bool:
        """
        Checks to see if the passed in color is in checkmate
        Parameters:
            color (Color): passed in color enum to see if king in checkmate
        Returns:
            (bool): True if king in checkmate, otherwise False
        """
        if color == Color.BLACK:
            attacker_color = Color.WHITE
        else:
            attacker_color = Color.BLACK

        # if the king is not in check then it is not in checkmate
        if not self.check(color):
            return False

        # Gets the kings space tuple
        king_space = self.find_king(color)
        # Gets king object
        king = self._board[king_space[0]][king_space[1]]
        # Gets valid moves for the king
        king_moves = king.valid_moves(king_space[0], king_space[1])

        # Gets a list of the attackers valid moves
        attacker_moves = []
        attacker_pieces = self.get_piece_locations(attacker_color)
        for i in attacker_pieces:
            attacker_moves += self.get(i[0], i[1]).valid_moves(i[0], i[1])

        # Checks to see if there is a defending queen move that isn't in the
        # list of attacker moves
        for j in king_moves:
            if j not in attacker_moves:
                # If the king has a valid move, try it to ensure that it will
                # not put you in check
                if self.move(king, king_space[0], king_space[1], j[0], j[1]):
                    # Code gets here it the move worked, it undoes the move
                    # and returns false beacause the king is not in checkmate
                    previous_board = self._prior_states.pop()
                    self._board = previous_board
                    self.current_player = Color.WHITE
                    return False

        # My checkmate function gets here if there are no valid king moves
        # Gets a list of defender moves
        defender_moves = []
        defender_pieces = self.get_piece_locations(color)
        for r in defender_pieces:
            defender_moves += self.get(r[0], r[1]).valid_moves(r[0], r[1])

        # Goes through all the defender pieces
        for k in defender_pieces:
            # Gets a specific piece object
            piece = self.get(k[0], k[1])
            piece_moves = piece.valid_moves(k[0], k[1])
            # Loops through that pieces valid moves
            for m in piece_moves:
                # Checks to see if the move is valid via move function
                if self.move(piece, k[0], k[1], m[0], m[1]):
                    # This means the move is valid so it undoes the move; False
                    previous_board = self._prior_states.pop()
                    self._board = previous_board
                    self.current_player = Color.WHITE
                    return False
        return True

    def _computer_move(self) -> None:
        """
        AI that plays chess as the black pieces, it plays moves based on
        priority of the piece in this order: checkmate, check, queen, bishop,
        knight, rook, pawn, random
        """
        # Gets a list of moves for the AI
        black_moves = []
        b_piece_locations = self.get_piece_locations(Color.BLACK)
        for sp in b_piece_locations:
            black_moves += self._board[sp[0]][sp[1]].valid_moves(sp[0], sp[1])
        # Gets a list of pieces for its opponent
        w_piece_locations = self.get_piece_locations(Color.WHITE)

        # Going to go through all the black piece locations, tuple by tuple
        for black_tuple in b_piece_locations:
            # Gets an object of a piece
            current_piece = self._board[black_tuple[0]][black_tuple[1]]
            # Gets a tuple that holds that pieces moves
            its_moves = current_piece.valid_moves(black_tuple[0], black_tuple[1])
            # Going to go through each of the current pieces moves
            for j in its_moves:
                # If the move returns True it worked; and the move has been made
                if self.move(current_piece, black_tuple[0], black_tuple[1], j[0], j[1]):
                    # If this move results in white being put in check then return
                    if self.mate(Color.WHITE):
                        return
                    # If this move results in white not being put in check; undo the move
                    # and continue from the previous state of the board
                    else:
                        previous_board = self._prior_states.pop()
                        self._board = previous_board
                        self.current_player = Color.BLACK

        # Going to go through all the black piece locations, tuple by tuple
        for black_tuple in b_piece_locations:
            # Gets an object of a piece
            current_piece = self._board[black_tuple[0]][black_tuple[1]]
            # Gets a tuple that holds that pieces moves
            its_moves = current_piece.valid_moves(black_tuple[0], black_tuple[1])
            # Going to go through each of the current pieces moves
            for j in its_moves:
                # If the move returns True it worked; and the move has been made
                if self.move(current_piece, black_tuple[0], black_tuple[1], j[0], j[1]):
                    # If this move results in white being put in check then return
                    if self.check(Color.WHITE):
                        return
                    # If this move results in white not being put in check; undo the move
                    # and continue from the previous state of the board
                    else:
                        previous_board = self._prior_states.pop()
                        self._board = previous_board
                        self.current_player = Color.BLACK

        # Checks to see if the AI can take a queen
        queen_exists = False
        # Checks if any of the user pieces are a queen object
        for piece_tuple in w_piece_locations:
            if isinstance(self.get(piece_tuple[0], piece_tuple[1]), Queen):
                queen_location = (piece_tuple[0], piece_tuple[1])
                queen_exists = True
        # If the user has a queen object then it checks to see if its
        # coordinates are in the list of black moves
        if queen_exists:
            if queen_location in black_moves:
                # Looks for the piece who has the queens space as a valid move
                for black_tuple in b_piece_locations:
                    piece = self._board[black_tuple[0]][black_tuple[1]]
                    # Get a list of tuples of available moves for a certain piece
                    available_moves = piece.valid_moves(black_tuple[0], black_tuple[1])
                    # Loops through each move of the current piece checking if
                    # a queen is located there
                    for i in available_moves:
                        if isinstance(self.get(i[0], i[1]), Queen):
                            # If the move is the space as the queen, make that move
                            if self.move(piece, black_tuple[0], black_tuple[1], i[0], i[1]):
                                return
                            else:
                                self.current_player = Color.BLACK

        # Checks to see if AI can take a bishop
        bishop_exists = False
        # Checks if any of the user pieces are a bishop object
        for piece_tuple in w_piece_locations:
            if isinstance(self.get(piece_tuple[0], piece_tuple[1]), Bishop):
                bishop_location = (piece_tuple[0], piece_tuple[1])
                if bishop_location in black_moves:
                    bishop_exists = True
                    break
        # If the user has a bishop object then it checks to see if its
        # coordinates are in the list of black moves
        if bishop_exists:
            if bishop_location in black_moves:
                # Looks for the piece who has the bishops space as a valid move
                for black_tuple in b_piece_locations:
                    piece = self._board[black_tuple[0]][black_tuple[1]]
                    # Get a list of tuples of available moves for a certain piece
                    available_moves = piece.valid_moves(black_tuple[0], black_tuple[1])
                    # Loops through each move of the current piece checking if
                    # a bishop is located there
                    for i in available_moves:
                        if isinstance(self.get(i[0], i[1]), Bishop):
                            # If the move is the space as the bishop, make that move
                            if self.move(piece, black_tuple[0], black_tuple[1], i[0], i[1]):
                                return
                            else:
                                self.current_player = Color.BLACK

        # Checks to see if AI can take a knight
        knight_exists = False
        # Checks if any of the user pieces are a knight object
        for piece_tuple in w_piece_locations:
            if isinstance(self.get(piece_tuple[0], piece_tuple[1]), Knight):
                knight_location = (piece_tuple[0], piece_tuple[1])
                if knight_location in black_moves:
                    knight_exists = True
                    break
        # If the user has a knight object then it checks to see if its
        # coordinates are in the list of black moves
        if knight_exists:
            if knight_location in black_moves:
                # Looks for the piece who has the knights space as a valid move
                for black_tuple in b_piece_locations:
                    piece = self._board[black_tuple[0]][black_tuple[1]]
                    # Get a list of tuples of available moves for a certain piece
                    available_moves = piece.valid_moves(black_tuple[0], black_tuple[1])
                    # Loops through each move of the current piece checking if
                    # a knight is located there
                    for i in available_moves:
                        if isinstance(self.get(i[0], i[1]), Knight):
                            # If the move is the space as the knight, make that move
                            if self.move(piece, black_tuple[0], black_tuple[1], i[0], i[1]):
                                return
                            else:
                                self.current_player = Color.BLACK

        # Checks to see if AI can take a rook
        rook_exists = False
        # Checks if any of the user pieces are a rook object
        for piece_tuple in w_piece_locations:
            if isinstance(self.get(piece_tuple[0], piece_tuple[1]), Rook):
                rook_location = (piece_tuple[0], piece_tuple[1])
                if rook_location in black_moves:
                    rook_exists = True
                    break
        # If the user has a rook object then it checks to see if its
        # coordinates are in the list of black moves
        if rook_exists:
            if rook_location in black_moves:
                # Looks for the piece who has the rooks space as a valid move
                for black_tuple in b_piece_locations:
                    piece = self._board[black_tuple[0]][black_tuple[1]]
                    # Get a list of tuples of available moves for a certain piece
                    available_moves = piece.valid_moves(black_tuple[0], black_tuple[1])
                    # Loops through each move of the current piece checking if
                    # a rook is located there
                    for i in available_moves:
                        if isinstance(self.get(i[0], i[1]), Rook):
                            # If the move is the space as the rook, make that move
                            if self.move(piece, black_tuple[0], black_tuple[1], i[0], i[1]):
                                return
                            else:
                                self.current_player = Color.BLACK

        # Checks to see if AI can take a pawn
        pawn_exists = False
        # Checks if any of the user pieces are a pawn object
        for piece_tuple in w_piece_locations:
            if isinstance(self.get(piece_tuple[0], piece_tuple[1]), Pawn):
                pawn_location = (piece_tuple[0], piece_tuple[1])
                if pawn_location in black_moves:
                    pawn_exists = True
                    break
        # If the user has a pawn object then it checks to see if its
        # coordinates are in the list of black moves
        if pawn_exists:
            if pawn_location in black_moves:
                # Looks for the piece who has the pawns space as a valid move
                for black_tuple in b_piece_locations:
                    piece = self._board[black_tuple[0]][black_tuple[1]]
                    # Get a list of tuples of available moves for a certain piece
                    available_moves = piece.valid_moves(black_tuple[0], black_tuple[1])
                    # Loops through each move of the current piece checking if
                    # a pawn is located there
                    for i in available_moves:
                        if isinstance(self.get(i[0], i[1]), Pawn):
                            # If the move is the space as the pawn, make that move
                            if self.move(piece, black_tuple[0], black_tuple[1], i[0], i[1]):
                                return
                            else:
                                self.current_player = Color.BLACK

        # This generates a random move for the AI
        # Gets a list of tuples of all the black pieces
        pieces = self.get_piece_locations(Color.BLACK)
        # While there are still piece tuples in the list
        while pieces:
            # Gets a tuple for a specific piece
            piece_tuple = random.choice(pieces)
            # Gets the piece object
            piece = self.get(piece_tuple[0], piece_tuple[1])
            # Get the pieces move
            piece_moves = piece.valid_moves(piece_tuple[0], piece_tuple[1])
            if piece_moves:
                for m in piece_moves:
                    # If the move worked then that is the chosen move
                    if self.move(piece, piece_tuple[0], piece_tuple[1], m[0], m[1]):
                        return
            pieces.remove(piece_tuple)
