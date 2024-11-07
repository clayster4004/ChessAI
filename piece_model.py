# Final Project - Chess - CIS 163
# Prof. Ira Woodring
# Created by Clay Beal
# - in association with Zachary Bauer
from enum import Enum
import abc
import pygame


class Color(Enum):
    """
    Enumeration for the colors of the chess pieces
    """
    WHITE = 0
    BLACK = 1


class Piece(abc.ABC):
    """
    Abstract Method
    Blueprint to make the chess pieces and give them valid moves and images
    """
    # Static variable to hold images
    image_path = 'images/pieces.png'
    SPRITESHEET = pygame.image.load(image_path)
    # So pieces can keep track of the current game
    _game = None

    def set_game(game):
        """
        Sets the current instance of game for the pieces; unused
        """
        #if not isinstance(game, Game):
            #raise ValueError('You must provide a valid Game instance.')
        Piece._game = game

    def __init__(self, color: Color) -> None:
        """
        Instance of a piece with a color assigned to it
        Parameters:
            color (Color): Color associated with the piece
        """
        self._color = color
        # CHANGED THIS TO PYGAME.SRCALPHA
        self._image = pygame.Surface((105, 105), pygame.SRCALPHA) # ???

    @property
    def color(self) -> Color:
        """
        Getter for the color of a piece
        Returns:
            (enum): Color of the piece
        """
        return self._color

    def set_image(self, x: int, y: int) -> None:
        """
        Sets the image of a piece at an x, y coordinate
        x (int): x coordinate
        y (int): y coordinate
        """
        self._image.blit(Piece.SPRITESHEET, (0,0),
                         pygame.rect.Rect(x, y, 105, 105))

    def _diagonal_moves(self, y: int, x: int, y_d: int, x_d: int,
                        distance: int) -> list[tuple[int, int]]:
        """
        Gets the possible moves for a piece that can move diagonally
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
            y_d (int): direction you want to go with the y coordinate
            x_d (int): direction you want to go with the x coordinate
            distance (int): how many spaces the pieces can move
        Returns:
            possible_moves (list): possible moves for a piece
        """
        # Current location is (y, x)
        possible_moves = []
        piece = self._game._board[y][x]
        color = piece.color
        try:
            # This will be used to check number of spaces from the current
            # piece we can use
            for i in range(1, distance + 1):
                # Need to check the board at this index and see if it's None
                # current index + (direction * number of spaces)
                # If the space is None add it to the possible moves
                if (y + y_d * i) >= 0 and (x + x_d * i) >= 0:
                    if self._game._board[y + y_d * i][x + x_d * i] is None:
                        possible_moves.append((y + (y_d * i), x + (x_d * i)))
                    elif self._game._board[y + y_d * i][x + x_d * i].color is not color:
                        possible_moves.append((y + (y_d * i), x + (x_d * i)))
                        return possible_moves
                    else:
                        return possible_moves
        except IndexError:
            pass
        return possible_moves

    def _horizontal_moves(self, y: int, x: int, y_d: int, x_d: int,
                        distance: int) -> list[tuple[int, int]]:
        """
        Gets the possible moves for a piece that can move horizontally
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
            y_d (int): direction you want to go with the y coordinate
            x_d (int): direction you want to go with the x coordinate
            distance (int): how many spaces the pieces can move
        Returns:
            possible_moves (list): possible moves for a piece
        """
        # Current location is (y,x)
        possible_moves = []
        piece = self._game._board[y][x]
        color = piece.color
        try:
            # This will be used to check number of spaces from the current
            # piece we can use
            for i in range(1, distance + 1):
                # Need to check the board at this index and see if it's None
                # current index + (direction * number of spaces)
                # If the space is None add it to the possible moves
                if (x + x_d * i) >= 0:
                    if self._game._board[y][x + x_d * i] is None:
                        possible_moves.append((y, x + (x_d * i)))
                    elif self._game._board[y][x + x_d * i].color is not color:
                        possible_moves.append((y, x + (x_d * i)))
                        return possible_moves
                    else:
                        return possible_moves
        except IndexError:
            pass
        return possible_moves

    def _vertical_moves(self, y: int, x: int, y_d: int, x_d: int,
                        distance: int) -> list[tuple[int, int]]:
        """
        Gets the possible moves for a piece that can move vertically
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
            y_d (int): direction you want to go with the y coordinate
            x_d (int): direction you want to go with the x coordinate
            distance (int): how many spaces the pieces can move
        Returns:
            possible_moves (list): possible moves for a piece
        """
        # Current location is (y,x)
        possible_moves = []
        piece = self._game._board[y][x]
        color = piece.color
        try:
            # This will be used to check number of spaces from the current
            # piece we can use
            for i in range(1, distance + 1):
                # Need to check the board at this index and see if it's None
                # current index + (direction * number of spaces)
                # If the space is None add it to the list of possible moves
                if (y + y_d * i) >= 0:
                    if self._game._board[y + y_d * i][x] is None:
                        possible_moves.append((y + (y_d * i), x))
                    elif self._game._board[y + y_d * i][x].color is not color:
                        possible_moves.append((y + (y_d * i), x))
                        return possible_moves
                    else:
                        return possible_moves
        except IndexError:
            pass
        return possible_moves

    def get_diagonal_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """
        Calls diagonal functions to get all the diagonal directions spaces
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
            distance (int): How many spaces a piece can move
        Returns:
            (list): of all the total moves
        """
        moves1 = self._diagonal_moves(y, x, -1, -1, distance)
        moves2 = self._diagonal_moves(y, x, -1, 1, distance)
        moves3 = self._diagonal_moves(y, x, 1, -1, distance)
        moves4 = self._diagonal_moves(y, x, 1, 1, distance)
        return moves1 + moves2 + moves3 + moves4

    def get_horizontal_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """
        Calls horizontal functions to get all the horizontal directions spaces
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
            distance (int): How many spaces a piece can move
        Returns:
            (list): of all the total moves
        """
        moves1 = self._horizontal_moves(y, x, 1, 1, distance)
        moves2 = self._horizontal_moves(y, x, 1, -1, distance)
        return moves1 + moves2

    def get_vertical_moves(self, y: int, x: int, distance: int) -> list[tuple[int, int]]:
        """
        Calls vertical functions to get all the vertical directions spaces
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
            distance (int): How many spaces a piece can move
        Returns:
            (list): of all the total moves
        """
        moves1 = self._vertical_moves(y, x, 1, 1, distance)
        moves2 = self._vertical_moves(y, x, -1, 1, distance)
        return moves1 + moves2

    @abc.abstractmethod
    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        This function is going to be used to get the valid moves for a piece
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
        Returns:
            (list): of all the total valid moves
        """
        pass

    @abc.abstractmethod
    def copy(self):
        """
        Deep copy of a piece
        """
        pass


class King(Piece):
    def __init__(self, color: Color):
        """
        Creates an instance of a King
        Parameters:
            color (Color): The color of the king
        """
        super().__init__(color)
        # Sets the image for black and white king
        if self.color == Color.WHITE:
            self.set_image(0,0)
        else:
            self.set_image(0, 104)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        Gets the valid moves for the king
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
        Returns:
            (list): of valid king moves
        """
        # Gets the diagonal, horizontal and vertical moves
        # Returns them all in one big valid moves list
        diag_moves = self.get_diagonal_moves(y, x, 1)
        horizontal_moves = self.get_horizontal_moves(y, x, 1)
        vertical_moves = self.get_vertical_moves(y, x, 1)
        return diag_moves + horizontal_moves + vertical_moves

    def copy(self):
        """
        Deep copies King
        Returns:
            (King): New instance of King
        """
        k = King(self.color)
        return k


class Queen(Piece):
    """
    Creates an instance of a Queen
        Parameters:
            color (Color): The color of the queen
    """
    def __init__(self, color: Color):
        super().__init__(color)
        # Sets image for black and white queen
        if self.color == color.WHITE:
            self.set_image(104, 0)
        else:
            self.set_image(104, 104)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        Gets the valid moves for the queen
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
        Returns:
            (list): of valid queen moves
        """
        # Gets the diagonal, horizontal and vertical moves
        # Returns them all in one big valid moves list
        diag_moves = self.get_diagonal_moves(y, x, 8)
        horizontal_moves = self.get_horizontal_moves(y, x, 8)
        vertical_moves = self.get_vertical_moves(y, x, 8)
        return diag_moves + horizontal_moves + vertical_moves

    def copy(self):
        """
        Deep copies the queen
        Returns:
            (Queen): New instance of a queen
        """
        q = Queen(self.color)
        return q


class Bishop(Piece):
    """
    Creates an instance of a Bishop
        Parameters:
            color (Color): The color of the bishop
    """
    def __init__(self, color: Color):
        super().__init__(color)
        # Sets the image for a black and white bishop
        if self.color == color.WHITE:
            self.set_image(210, 0)
        else:
            self.set_image(210, 104)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        Gets the valid moves for the queen
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
        Returns:
            (list): of valid queen moves
        """
        # Gets the diagonal moves & returns them in a list
        diag_moves = self.get_diagonal_moves(y, x, 8)
        return diag_moves

    def copy(self):
        """
        Deep copies the bishop
        Returns:
            (Bishop): New instance of a bishop
        """
        b = Bishop(self.color)
        return b


class Rook(Piece):
    """
    Creates an instance of a Rook
        Parameters:
            color (Color): The color of the rook
    """
    def __init__(self, color: Color):
        super().__init__(color)
        # Sets the image for a black and white rook
        if self.color == color.WHITE:
            self.set_image(420, 0)
        else:
            self.set_image(420, 104)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        Gets the valid moves for the queen
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
        Returns:
            (list): of valid queen moves
        """
        # Gets the horizontal moves & returns them in a list
        vertical_moves = self.get_vertical_moves(y, x, 8)
        horizontal_moves = self.get_horizontal_moves(y, x, 8)
        return horizontal_moves + vertical_moves

    def copy(self):
        """
        Deep copies the rook
        Returns:
            (Rook): New instance of the rook
        """
        r = Rook(self.color)
        return r


class Knight(Piece):
    """
    Creates an instance of a Rook
        Parameters:
            color (Color): The color of the rook
    """
    def __init__(self, color: Color):
        super().__init__(color)
        # Sets the image for a black and white knight
        if self.color == color.WHITE:
            self.set_image(312, 0)
        else:
            self.set_image(312, 104)

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        Gets the valid moves for the knight
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
        Returns:
            (list): of valid knight moves
        """
        valid_moves = []
        piece = self._game._board[y][x]
        color = piece.color
        # This is checking the spaces that are either two up/down
        # or two left/right from the current space
        for i in range(-2, 3, 4):
            # This is checking the spaces that are either one up/down
            # or one left/right from the current space
            for j in range(-1, 2, 2):
                # If this space on the board is not occupied it is a valid move
                # It is also a valid move if it is a piece of the opposite color
                if (0 <= (y + i) < 8) and (0 <= (x + j) < 8) and\
                        self._game._board[y + i][x + j] is None:
                    valid_moves.append((y + i, x + j))
                elif (0 <= (y + i) < 8) and (0 <= (x + j) < 8) and\
                    self._game._board[y + i][x + j].color is not color:
                    valid_moves.append((y + i, x + j))

                if (0 <= (x + i) < 8) and (0 <= (y + j) < 8) and\
                        self._game._board[y + j][x + i] is None:
                    valid_moves.append((y + j, x + i))
                elif (0 <= (x + i) < 8) and (0 <= (y + j) < 8) and\
                    self._game._board[y + j][x + i].color is not color:
                    valid_moves.append((y + j, x + i))
        return valid_moves

    def copy(self):
        """
        Deep copies a knight
        Returns:
            (Knight): New instance of a knight
        """
        k = Knight(self.color)
        return k


class Pawn(Piece):
    """
    Creates an instance of a Pawn
        Parameters:
            color (Color): The color of the pawn
    """
    def __init__(self, color: Color):
        super().__init__(color)
        # Sets image for a black and white pawn
        if self.color == color.WHITE:
            self.set_image(530,0)
        else:
            self.set_image(530, 104)
        self.moved = False

    def valid_moves(self, y: int, x: int) -> list[tuple[int, int]]:
        """
        Gets the valid moves for the pawn
        Parameters:
            y (int): current y coordinate of a piece
            x (int): current x coordinate of a piece
        Returns:
            (list): of valid pawn moves
        """
        valid_moves = []
        piece = self._game._board[y][x]
        color = piece.color
        # This works for the first move for the pawns
        # Black pawns can move down the board and twice on their first move
        if not self.moved and self.color == Color.BLACK:
            for i in range(1, 3):
                try:
                    # If the space in front of them is occupied
                    if self._game._board[y+i][x] is not None:
                        break
                    else:
                        valid_moves.append((y + i, x))
                except IndexError:
                    pass

            for j in range(-1, 2, 2):
                try:
                    if self._game._board[y+1][x+j] is not None and (x+j) != -1:
                        # If the space diagonal to them is a piece of the opposite color
                        if self._game._board[y+1][x+j].color is not color:
                            valid_moves.append((y+1, x+j))
                except IndexError:
                    pass

        # White pawns can move up the board and twice on their first move
        elif not self.moved and self.color == Color.WHITE:
            for i in range(1, 3):
                try:
                    # If the space in front of them is occupied
                    if self._game._board[y - i][x] is not None:
                        break
                    else:
                        valid_moves.append((y - i, x))
                except IndexError:
                    pass

            for j in range(-1, 2, 2):
                try:
                    if self._game._board[y-1][x+j] is not None:
                        # If the space diagonal to them is a piece of the opposite color
                        if self._game._board[y-1][x+j].color is not color:
                            valid_moves.append((y-1, x+j))
                except IndexError:
                    pass

        # If the pawn has already moved once then it can only move one space up
        elif self.moved and self.color == Color.BLACK:
            for j in range(-1, 2, 2):
                try:
                    if self._game._board[y+1][x+j] is not None and (x+j) != -1:
                        # If the space diagonal to them is a piece of the opposite color
                        if self._game._board[y+1][x+j].color is not color:
                            valid_moves.append((y+1, x+j))
                except IndexError:
                    pass
            try:
                # If the space in front of them is not occupied
                if self._game._board[y+1][x] is None:
                    valid_moves.append((y+1, x))
            except IndexError:
                pass

        elif self.moved and self.color == Color.WHITE:
            for j in range(-1, 2, 2):
                try:
                    if self._game._board[y-1][x+j] is not None:
                        # If the space diagonal to them is a piece of the opposite color
                        if self._game._board[y-1][x+j].color is not color:
                            valid_moves.append((y-1, x+j))
                except IndexError:
                    pass
            try:
                # If the space in front of them is not occupied
                if self._game._board[y-1][x] is None:
                    valid_moves.append((y-1, x))
            except IndexError:
                pass
        return valid_moves

    def copy(self):
        """
        Deep copies a pawn
        Returns:
            (Pawn): new instance of a pawn
        """
        # If the pawn had previously moved, set the new one to the same moved
        # status
        if self.moved:
            p = Pawn(self.color)
            p.moved = True
        else:
            p = Pawn(self.color)
            p.moved = False
        return p
