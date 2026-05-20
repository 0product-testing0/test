import pytest

from tic_tac_toe import (
    EMPTY,
    InvalidMove,
    available_moves,
    current_player,
    is_draw,
    make_move,
    new_board,
    render_board,
    winner,
)


def test_new_board_starts_empty():
    assert new_board() == (EMPTY,) * 9


def test_render_board_shows_numbers_for_empty_squares():
    board = make_move(new_board(), 5, "X")

    assert render_board(board) == "1 | 2 | 3\n---------\n4 | X | 6\n---------\n7 | 8 | 9"


def test_make_move_adds_player_without_mutating_original_board():
    board = new_board()

    updated_board = make_move(board, 1, "X")

    assert board == (EMPTY,) * 9
    assert updated_board == ("X", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY)


def test_make_move_uses_current_player_when_player_is_not_provided():
    board = new_board()

    board = make_move(board, 1)
    board = make_move(board, 2)

    assert board[:2] == ("X", "O")


def test_make_move_rejects_occupied_square():
    board = make_move(new_board(), 1, "X")

    with pytest.raises(InvalidMove, match="already occupied"):
        make_move(board, 1, "O")


def test_make_move_rejects_out_of_range_square():
    with pytest.raises(InvalidMove, match="between 1 and 9"):
        make_move(new_board(), 10, "X")


def test_make_move_rejects_invalid_player():
    with pytest.raises(InvalidMove, match="player must be X or O"):
        make_move(new_board(), 1, "A")


def test_make_move_rejects_finished_game():
    board = ("X", "X", "X", "O", "O", EMPTY, EMPTY, EMPTY, EMPTY)

    with pytest.raises(InvalidMove, match="already over"):
        make_move(board, 6, "O")


def test_available_moves_returns_open_square_numbers():
    board = ("X", EMPTY, "O", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY)

    assert available_moves(board) == [2, 4, 5, 6, 7, 8, 9]


@pytest.mark.parametrize(
    "board",
    [
        ("X", "X", "X", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY),
        ("O", EMPTY, EMPTY, "O", EMPTY, EMPTY, "O", EMPTY, EMPTY),
        ("X", EMPTY, EMPTY, EMPTY, "X", EMPTY, EMPTY, EMPTY, "X"),
    ],
)
def test_winner_detects_winning_lines(board):
    assert winner(board) == board[0]


def test_winner_returns_none_without_winner():
    assert winner(new_board()) is None


def test_is_draw_identifies_full_board_without_winner():
    board = ("X", "O", "X", "X", "O", "O", "O", "X", "X")

    assert is_draw(board) is True


def test_is_draw_is_false_when_there_is_a_winner():
    board = ("X", "X", "X", "O", "O", EMPTY, EMPTY, EMPTY, EMPTY)

    assert is_draw(board) is False


def test_current_player_alternates_between_players():
    assert current_player(new_board()) == "X"

    board = make_move(new_board(), 1, "X")

    assert current_player(board) == "O"


def test_current_player_rejects_finished_game():
    board = ("X", "X", "X", "O", "O", EMPTY, EMPTY, EMPTY, EMPTY)

    with pytest.raises(ValueError, match="already over"):
        current_player(board)
