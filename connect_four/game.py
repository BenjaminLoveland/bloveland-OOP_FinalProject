"""
Game module to handle gameplay logic for Connect Four.

@startuml
class Game {
    - _ROWS: int
    - _COLUMNS: int
    - _board: List[List[int]]
    - _current_player: int
    + __init__(): None
    + rows(): int
    + columns(): int
    + board(): List[List[int]]
    + board(new_board: List[List[int]]): None
    + current_player(): int
    + current_player(player: int): None
    + reset_board(): None
    + check_winner(): int
    + make_move(column: int): Tuple[int, int]
    + is_column_full(column: int): bool
    + to_string(): str
}

@enduml
"""


from typing import List, Tuple


class Game:
    """
    A class representing the gameplay logic for connect 4.
    """

    def __init__(self) -> None:
        """
        Initialize the Connect Four game board and set the current player.
        """
        self._ROWS: int = 6
        self._COLUMNS: int = 7
        self._board: List[List[int]] = [
            [0 for _ in range(self._COLUMNS)] for _ in range(self._ROWS)]
        self._current_player: int = 1

    @property
    def rows(self) -> int:
        """
        Gets the number of rows in the board.
        """
        return self._ROWS

    @property
    def columns(self) -> int:
        """
        Gets the number of columns in the board.
        """
        return self._COLUMNS

    @property
    def board(self) -> List[List[int]]:
        """
        Gets the game board.
        """
        return self._board

    @board.setter
    def board(self, new_board: List[List[int]]) -> None:
        """
        Sets the game board.
        """
        if len(new_board) != self._ROWS or any(
                len(row) != self._COLUMNS for row in new_board):
            raise ValueError("Invalid board dimensions.")
        self._board = new_board

    @property
    def current_player(self) -> int:
        """
        Gets the current player.
        """
        return self._current_player

    @current_player.setter
    def current_player(self, player: int) -> None:
        """
        Sets the current player.
        """
        if player not in (1, 2):
            raise ValueError("Invalid player number. Must be 1 or 2.")
        self._current_player = player

    def reset_board(self) -> None:
        """
        Reset the game board to initital state.
        """
        self._board = [
            [0 for _ in range(self._COLUMNS)] for _ in range(self._ROWS)]
        self._current_player = 1

    def check_winner(self) -> int:
        """
        Checks if there is a winner, returns 1 or 2 if a player wins, 0 if not.
        """
        for row in range(self._ROWS):
            for column in range(self._COLUMNS):
                if self._board[row][column] != 0:
                    # Horizontal Check (-)
                    if column + 3 < self._COLUMNS and all(
                        self._board[row][
                            column + i] == self._board[row][column]
                        for i in range(4)
                    ):
                        print(f"Horizontal at {row}, {column} to {column + 3}")
                        return self._board[row][column]
                    # Vertical Check (|)
                    if row + 3 < self._ROWS and all(
                        self._board[row + i][
                            column] == self._board[row][column]
                        for i in range(4)
                    ):
                        print(f"Vertical at {column}, rows {row} to {row + 3}")
                        return self._board[row][column]
                    # Diagonal Check (/)
                    if (
                        row + 3 < self._ROWS
                        and column + 3 < self._COLUMNS
                        and all(
                            self._board[row + i][
                                column + i] == self._board[row][column]
                            for i in range(4)
                        )
                    ):
                        print(f"Diagonal {row}, {column}")  # pragma: no cover
                        return self._board[row][column]  # pragma: no cover
                    # Diagonal Check (\)
                    if row - 3 >= 0 and column + 3 < self._COLUMNS and all(
                        self._board[row - i][
                            column + i] == self._board[row][column]
                        for i in range(4)
                    ):
                        print(f"Diagonal starting at {row}, column {column}")
                        return self._board[row][column]
        return 0

    def make_move(self, column: int) -> Tuple[int, int]:
        """
        Make a move for the current player.
        """
        if column < 0 or column >= self._COLUMNS:
            raise ValueError("Column out of bounds.")
        for row in range(self._ROWS - 1, -1, -1):
            if self._board[row][column] == 0:
                self._board[row][column] = self._current_player
                self._current_player = 3 - self._current_player
                return row, column
        raise ValueError("Column is full.")

    def is_column_full(self, column: int) -> bool:
        """
        Check if the specified column is full.
        """
        return all(row[column] != 0 for row in self._board)

    def to_string(self) -> str:
        """
        Gets a string representation of the game board.
        """
        return "\n".join([" ".join(map(str, row)) for row in self._board])
