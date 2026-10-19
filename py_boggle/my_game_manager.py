import copy
import random
from typing import List, Optional, Set, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary
from py_boggle.boggle_game import BoggleGame

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

SHORT = 3
CUBE_SIDES = 6

class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`
    """

    def __init__(self):
        """Constructs an empty Boggle Game.

        A newly-constructed game is unplayable.
        The `new_game` method will be called to initialize a playable game.
        Do not call `new_game` here.

        This method is provided for you, but feel free to change it.
        """

        self.board: List[List[str]] # current game board
        self.size: int # board size
        self.words: List[str] # player's current words
        self.dictionary: BoggleDictionary # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] # the position of the last added word, or None

    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        """This method is provided for you, but feel free to change it.
        """
        with open(cubefile, 'r') as infile:
            faces = [line.strip() for line in infile]
        cubes = [f.lower() for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size*size:
            raise ValueError('ERROR: Invalid Dimensions (size, cubes)')
        random.shuffle(cubes)
        # Set all of the game parameters
        self.board =[[random.choice(cubes[r*size + c]) 
                    for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        self.dictionary = dictionary
        self.last_added_word = None


    def get_board(self) -> List[List[str]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.board

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Helper method called by add_word()
        Expected behavior:
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word()
        (see documentation in boggle_game.py).
        If `word` is not present on the board, return None.
        """
        word = word.lower()

        if not word:
            return None

        rows = len(self.board)
        cols = len(self.board[0])

        def dfs(row, col, index, visited, path):
            if (row < 0 or row >= rows or
                    col < 0 or col >= cols):
                return None

            if (row, col) in visited:
                return None

            if self.board[row][col] != word[index]:
                return None

            visited.add((row, col))
            path.append((row, col))

            if index == len(word) - 1:
                return path.copy()

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue

                    result = dfs(
                        row + dr,
                        col + dc,
                        index + 1,
                        visited,
                        path
                    )

                    if result is not None:
                        return result

            visited.remove((row, col))
            path.pop()

            return None

        for row in range(rows):
            for col in range(cols):
                result = dfs(
                    row, col, 0, set(), []
                )

                if result is not None:
                    return result

        return None


    def add_word(self, word: str) -> int:
            """This method is provided for you, but feel free to change it.
            """
            word = word.lower()
            if (len(word) > SHORT and word not in self.words and self.dictionary.contains(word)):
                location = self.find_word_in_board(word)
                if location is not None:
                    self.last_added_word = location
                    self.words.append(word)
                    return len(word) - SHORT
            return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """This method is provided for you, but feel free to change it.
        """
        self.board = [[c.lower() for c in row] for row in board]

    def get_score(self) -> int:
        """This method is provided for you, but feel free to change it.
        """
        return sum([len(word) - SHORT for word in self.words])

    def dictionary_driven_search(self) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """
        found_words = set()

        for word in self.dictionary:
            if len(word) <= SHORT:
                continue

            if word in self.words:
                continue

            if self.find_word_in_board(word) is not None:
                found_words.add(word)

        return found_words

    def board_driven_search(self) -> Set[str]:
        found_words = set()

        rows = len(self.board)
        cols = len(self.board[0])

        def dfs(row, col, prefix, visited):
            if (row < 0 or row >= rows or
                    col < 0 or col >= cols):
                return

            if (row, col) in visited:
                return

            new_word = prefix + self.board[row][col]

            if not self.dictionary.is_prefix(new_word):
                return

            visited.add((row, col))

            if (len(new_word) > SHORT and
                    self.dictionary.contains(new_word) and
                    new_word not in self.words):
                found_words.add(new_word)

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue

                    dfs(
                        row + dr,
                        col + dc,
                        new_word,
                        visited
                    )

            visited.remove((row, col))

        for row in range(rows):
            for col in range(cols):
                dfs(row, col, "", set())

        return found_words
