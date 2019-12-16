import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\nX..'),
        mocker.call('Game is finished, X wins')
    ]
    assert bot.game is None


def test_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\n..X'),
        mocker.call('XO.\nXO.\n.OX'),
        mocker.call('Game is finished, O wins')
    ]
    assert bot.game is None


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\n..X'),
        mocker.call('XO.\nXOO\n..X'),
        mocker.call('XOX\nXOO\n..X'),
        mocker.call('XOX\nXOO\nO.X'),
        mocker.call('XOX\nXOO\nOXX'),
        mocker.call('Game is finished, draw')
    ]
    assert bot.game is None


def test_before_start(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('kek')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
    ]


def test_second_start(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 1 2')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\n..X'),
        mocker.call('XO.\nXO.\n.OX'),
        mocker.call('Game is finished, O wins'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\nX..'),
        mocker.call('Game is finished, X wins')
    ]
    assert bot.game is None


def test_invalid_turn_x(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
    ]


def test_invalid_turn_o(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
    ]


def test_invalid_turn_to_visited(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
    ]
