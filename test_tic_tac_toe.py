import unittest

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


class TicTacToeTest(unittest.TestCase):
    def test_new_board_starts_empty(self):
        self.assertEqual(new_board(), (EMPTY,) * 9)

    def test_render_board_shows_numbers_for_empty_squares(self):
        board = make_move(new_board(), 5, "X")

        self.assertEqual(
            render_board(board),
            "1 | 2 | 3\n---------\n4 | X | 6\n---------\n7 | 8 | 9",
        )

    def test_make_move_adds_player_without_mutating_original_board(self):
        board = new_board()

        updated_board = make_move(board, 1, "X")

        self.assertEqual(board, (EMPTY,) * 9)
        self.assertEqual(
            updated_board,
            ("X", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY),
        )

    def test_make_move_uses_current_player_when_player_is_not_provided(self):
        board = new_board()

        board = make_move(board, 1)
        board = make_move(board, 2)

        self.assertEqual(board[:2], ("X", "O"))

    def test_make_move_rejects_occupied_square(self):
        board = make_move(new_board(), 1, "X")

        with self.assertRaisesRegex(InvalidMove, "already occupied"):
            make_move(board, 1, "O")

    def test_make_move_rejects_out_of_range_square(self):
        with self.assertRaisesRegex(InvalidMove, "between 1 and 9"):
            make_move(new_board(), 10, "X")

    def test_make_move_rejects_invalid_player(self):
        with self.assertRaisesRegex(InvalidMove, "player must be X or O"):
            make_move(new_board(), 1, "A")

    def test_make_move_rejects_finished_game(self):
        board = ("X", "X", "X", "O", "O", EMPTY, EMPTY, EMPTY, EMPTY)

        with self.assertRaisesRegex(InvalidMove, "already over"):
            make_move(board, 6, "O")

    def test_available_moves_returns_open_square_numbers(self):
        board = ("X", EMPTY, "O", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY)

        self.assertEqual(available_moves(board), [2, 4, 5, 6, 7, 8, 9])

    def test_winner_detects_winning_lines(self):
        winning_boards = (
            ("X", "X", "X", EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY),
            ("O", EMPTY, EMPTY, "O", EMPTY, EMPTY, "O", EMPTY, EMPTY),
            ("X", EMPTY, EMPTY, EMPTY, "X", EMPTY, EMPTY, EMPTY, "X"),
        )

        for board in winning_boards:
            with self.subTest(board=board):
                self.assertEqual(winner(board), board[0])

    def test_winner_returns_none_without_winner(self):
        self.assertIsNone(winner(new_board()))

    def test_is_draw_identifies_full_board_without_winner(self):
        board = ("X", "O", "X", "X", "O", "O", "O", "X", "X")

        self.assertTrue(is_draw(board))

    def test_is_draw_is_false_when_there_is_a_winner(self):
        board = ("X", "X", "X", "O", "O", EMPTY, EMPTY, EMPTY, EMPTY)

        self.assertFalse(is_draw(board))

    def test_current_player_alternates_between_players(self):
        self.assertEqual(current_player(new_board()), "X")

        board = make_move(new_board(), 1, "X")

        self.assertEqual(current_player(board), "O")

    def test_current_player_rejects_finished_game(self):
        board = ("X", "X", "X", "O", "O", EMPTY, EMPTY, EMPTY, EMPTY)

        with self.assertRaisesRegex(ValueError, "already over"):
            current_player(board)


if __name__ == "__main__":
    unittest.main()
