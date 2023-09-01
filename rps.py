import setup
import random
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

"""The Player class is the parent class for all of the Players
in this game"""


class Player:
    moves = ['rock', 'paper', 'scissors']

    def __init__(self):
        # initialization of the list for the move function
        self.my_move = self.moves
        # random choise for first round
        self.their_move = random.choice(self.moves)

    def learn(self, my_move, their_move):
        # moves of the players stored
        self.my_move = my_move
        self.their_move = their_move


class RandomComputerPlayer(Player):
    def learn(self, my_move, their_move):
        pass

    def move(self):
        # random move
        return random.choice(self.moves)


class ReflectComputerPlayer(Player):
    def move(self):
        # reflects the choice of the previous round
        return self.their_move


class RockLovingComputerPlayer(Player):
    def learn(self, my_move, their_move):
        pass

    def move(self):
        # reflects the choice of the previous round
        return "rock"


class PredictiveComputerPlayer(Player):
    def __init__(self):
        super().__init__()
        self.their_moves = [self.their_move]

    def learn(self, my_move, their_move):
        super().learn(my_move, their_move)
        self.their_moves.append(their_move)

    def most_frequent_move(self):
        moves = self.their_moves
        counter = 0
        most_frequent = moves[0]
        for move in moves:
            frequency = moves.count(move)
            if frequency > counter:
                counter = frequency
                most_frequent = move
                self.predicted_frequency = frequency
        return most_frequent

    def move(self):
        # Tries to predict player's next move based on frequent past moves
        predicted_move = self.most_frequent_move()
        if self.predicted_frequency > 6 and predicted_move != self.their_move:
            return random.choice(self.moves)
        elif predicted_move == "rock":
            return "paper"
        elif predicted_move == "paper":
            return "scissors"
        elif predicted_move == "scissors":
            return "rock"


class CycleComputerPlayer(Player):
    def move(self):
        # choses a different move of the last round
        if self.my_move == self.moves[0]:
            return self.moves[1]
        elif self.my_move == self.moves[1]:
            return self.moves[2]
        else:
            return self.moves[0]


class HumanPlayer(Player):
    def learn(self, my_move, their_move):
        pass

    def move(self):
        while True:
            move_human = input("Rock, Paper, or Scissors? ")
            if move_human.lower() in self.moves:
                return move_human.lower()
            elif move_human.lower() == 'exit':
                exit()


class Game:
    def __init__(self, p1, p2, rounds):
        self.p1 = p1
        self.p2 = p2
        self.score_p1 = 0
        self.score_p2 = 0
        self.number_rounds = rounds

    def beats(self, one, two):
        return ((one == 'rock' and two == 'scissors') or
                (one == 'scissors' and two == 'paper') or
                (one == 'paper' and two == 'rock'))

    def play_round(self):
        # move
        move1 = self.p1.move()
        move2 = self.p2.move()
        # result of the match
        if self.beats(move1, move2):
            self.score_p1 += 1
            winner = f'{Fore.GREEN}*** YOU WIN ***{Style.RESET_ALL}'
        elif move1 == move2:
            self.score_p1 = self.score_p1
            self.score_p2 = self.score_p2
            winner = f'{Fore.YELLOW}*** TIE ***{Style.RESET_ALL}'
        else:
            self.score_p2 += 1
            winner = f'{Fore.RED}*** COMPUTER WINS ***{Style.RESET_ALL}'
        # output the match information
        print(
            f"> You played : {move1}"
            f"\n> Computer played : {move2}"
            f"\n{winner}"
            f"\nScore: You ( {self.score_p1} ),"
            f"Computer ( {self.score_p2} )"
        )
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self):
        print(
            "Playing Rock,  Paper, Scissors!"
            "\n(If do you want exit game, enter 'exit'.)"
        )
        for round in range(int(self.number_rounds)):
            print(f"\nRound {round + 1} --")
            self.play_round()
        if self.score_p1 == self.score_p2:
            print(
                f"\n{Fore.YELLOW}--- The game ended in a tie!" +
                f"---{Style.RESET_ALL}"
                f"\nScore: You ( {self.score_p1} ),"
                f"Computer ( {self.score_p2} )"
            )
        elif self.score_p1 > self.score_p2:
            print(
                f"\n{Fore.GREEN}--- You Have Won! ---{Style.RESET_ALL}"
                f"\nScore: You ( {self.score_p1} ), "
                f"Computer ( {self.score_p2} )"
            )
        else:
            print(
                f"\n{Fore.RED}--- Computer Has Won! ---{Style.RESET_ALL}"
                f"\nScore: You ( {self.score_p1} ), "
                f"Computer ( {self.score_p2} )"
            )


def setup_game():
    while True:
        number_rounds = input(
            "Playing Paper, Rock, Scissors!"
            "\n(If do you want exit game, enter 'exit'.)"
            "\nHow many rounds do you want want play? ")
        if number_rounds.isdigit():
            computer_players = [
                RandomComputerPlayer(),
                ReflectComputerPlayer(),
                CycleComputerPlayer(),
                RockLovingComputerPlayer()
            ]
            if int(number_rounds) > 5:
                computer_players.append(PredictiveComputerPlayer())
            game = Game(
                HumanPlayer(),
                random.choice(
                    computer_players
                ),
                number_rounds
            )
            game.play_game()
        elif number_rounds.lower() == 'exit':
            exit()


if __name__ == '__main__':
    setup_game()
