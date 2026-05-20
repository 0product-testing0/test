"""A small two-player tic tac toe game for the command line."""

from __future__ import annotations

from collections.abc import Callable, Iterable


EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"
BOARD_SIZE = 9

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

Board = tuple[str, ...]


class InvalidMove(ValueError):
    """Raised when a move cannot be played on the current board."""


def new_board() -> Board:
    """Return a blank tic tac toe board."""
    return (EMPTY,) * BOARD_SIZE


def validate_board(board: Iterable[str]) -> Board:
    """Return board as a tuple after validating its shape and symbols."""
    normalized = tuple(board)
    if len(normalized) != BOARD_SIZE:
        raise ValueError(f"board must contain {BOARD_SIZE} squares")

    invalid_symbols = set(normalized) - {EMPTY, PLAYER_X, PLAYER_O}
    if invalid_symbols:
        symbols = ", ".join(sorted(repr(symbol) for symbol in invalid_symbols))
        raise ValueError(f"board contains invalid symbols: {symbols}")

    return normalized


def render_board(board: Iterable[str]) -> str:
    """Render a board, showing square numbers for open spaces."""
    normalized = validate_board(board)
    display_squares = [
        value if value != EMPTY else str(index + 1)
        for index, value in enumerate(normalized)
    ]
    rows = [
        " | ".join(display_squares[row_start : row_start + 3])
        for row_start in range(0, BOARD_SIZE, 3)
    ]
    return "\n---------\n".join(rows)


def available_moves(board: Iterable[str]) -> list[int]:
    """Return the playable square numbers on the board."""
    normalized = validate_board(board)
    return [
        index + 1
        for index, value in enumerate(normalized)
        if value == EMPTY
    ]


def winner(board: Iterable[str]) -> str | None:
    """Return the winning player, or None if the game has no winner yet."""
    normalized = validate_board(board)
    for first, second, third in WINNING_LINES:
        symbol = normalized[first]
        if symbol != EMPTY and symbol == normalized[second] == normalized[third]:
            return symbol
    return None


def is_draw(board: Iterable[str]) -> bool:
    """Return True when the board is full and neither player has won."""
    normalized = validate_board(board)
    return winner(normalized) is None and EMPTY not in normalized


def current_player(board: Iterable[str]) -> str:
    """Return whose turn it is on a valid in-progress board."""
    normalized = validate_board(board)
    x_count = normalized.count(PLAYER_X)
    o_count = normalized.count(PLAYER_O)

    if o_count > x_count or x_count - o_count > 1:
        raise ValueError("board has an invalid move count")
    if winner(normalized) is not None or is_draw(normalized):
        raise ValueError("game is already over")

    return PLAYER_X if x_count == o_count else PLAYER_O


def make_move(board: Iterable[str], square: int, player: str | None = None) -> Board:
    """Return a new board with a player's move applied."""
    normalized = validate_board(board)
    if winner(normalized) is not None or is_draw(normalized):
        raise InvalidMove("game is already over")
    if player is None:
        player = current_player(normalized)
    if player not in {PLAYER_X, PLAYER_O}:
        raise InvalidMove("player must be X or O")
    if square < 1 or square > BOARD_SIZE:
        raise InvalidMove("square must be between 1 and 9")

    index = square - 1
    if normalized[index] != EMPTY:
        raise InvalidMove(f"square {square} is already occupied")

    next_board = list(normalized)
    next_board[index] = player
    return tuple(next_board)


def play(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> Board:
    """Run an interactive two-player tic tac toe game."""
    board = new_board()
    output_func("Tic Tac Toe")
    output_func("Enter a square number from 1 to 9. Enter q to quit.")

    while True:
        output_func("")
        output_func(render_board(board))
        player = current_player(board)
        raw_move = input_func(f"Player {player}, choose a square: ").strip().lower()

        if raw_move in {"q", "quit", "exit"}:
            output_func("Game ended.")
            return board

        try:
            square = int(raw_move)
        except ValueError:
            output_func("Invalid move: enter a number from 1 to 9")
            continue

        try:
            board = make_move(board, square, player)
        except InvalidMove as error:
            output_func(f"Invalid move: {error}")
            continue

        game_winner = winner(board)
        if game_winner is not None:
            output_func("")
            output_func(render_board(board))
            output_func(f"Player {game_winner} wins!")
            return board

        if is_draw(board):
            output_func("")
            output_func(render_board(board))
            output_func("It's a draw!")
            return board


if __name__ == "__main__":
    play()
