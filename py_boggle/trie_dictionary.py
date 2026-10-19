import typing
from typing import Dict, Optional
from py_boggle.boggle_dictionary import BoggleDictionary

class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_word = False


class TrieDictionary(BoggleDictionary):

    def __init__(self):
        self.root: TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()

                if not word:
                    continue

                current = self.root

                for char in word:
                    if char not in current.children:
                        current.children[char] = TrieNode()

                    current = current.children[char]

                current.is_word = True

    def traverse(self, prefix: str) -> Optional[TrieNode]:
        current = self.root

        for char in prefix.lower():
            if char not in current.children:
                return None

            current = current.children[char]

        return current

    def is_prefix(self, prefix: str) -> bool:
        return self.traverse(prefix) is not None

    def contains(self, word: str) -> bool:
        node = self.traverse(word)

        if node is None:
            return False

        return node.is_word

    def __iter__(self) -> typing.Iterator[str]:
        def iterate(node: TrieNode, prefix: str):
            if node.is_word:
                yield prefix

            for char in sorted(node.children):
                yield from iterate(
                    node.children[char],
                    prefix + char
                )

        return iterate(self.root, "")
