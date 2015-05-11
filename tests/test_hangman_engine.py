import pytest
from hangman.core.engines import HangmanEngine
from hangman.core.errors import InvalidGuessError


class TestHangmanEngine:

    def setup_method(self, method):
        """ setup any state specific to the execution of the given
        module.setup_module """
        self.string_to_guess_in_test = "Silenus"
        self.hangman = HangmanEngine(self.string_to_guess_in_test)

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_module
        method. """
        pass

    def test_count_uppercase(self):
        """ Checks if the char counter behaves correctly """
        assert self.hangman.count_uppercase('S') is 1
        assert self.hangman.count_uppercase('s') is 1
        assert self.hangman.count_uppercase('i') is 0

    def test_count_downcase(self):
        """ Checks if the char counter behaves correctly """
        assert self.hangman.count_downcase('i') is 1
        assert self.hangman.count_downcase('S') is 1
        assert self.hangman.count_downcase('s') is 1

    def test_count(self):
        """ Checks if the char counter behaves correctly """
        assert self.hangman.count('s') is 2
        assert self.hangman.count('i') is 1

    def test_check_character(self):
        """ Checks if the character validator works fine """
        with pytest.raises(InvalidGuessError):
            self.hangman.check_character('aaaaa')
            self.hangman.check_character(1)
            self.hangman.check_character('1')

    def test_find_first_ocurrence(self):
        """ Checks if the finder for chars works as it was planned """
        assert self.hangman.find_first_occurrence("s", 0) is 0
        assert self.hangman.find_first_occurrence("S", 1) is 5
        assert self.hangman.find_first_occurrence("i", 1) is 0
        assert self.hangman.find_first_occurrence("i", 0) is 1

    def test_occurrences(self):
        """ Checks if the hangman engine can find correctly the chars """
        collected = []
        for char_i in self.hangman.occurrences('s'):
            assert type(char_i) is int
            collected.append(char_i)

        assert len(collected) is not 0
        assert collected[0] is 0
        assert collected[1] is len(self.string_to_guess_in_test) - 1
        assert len(self.hangman.guess_misses) is 0
        assert len(self.hangman.guess_asserted) is 1
        assert self.hangman.already_tried('S') is True
        assert self.hangman.already_tried('s') is True
        assert self.hangman.already_missed('s') is False
        assert self.hangman.already_missed('S') is False
        assert self.hangman.already_asserted('S') is True
        assert self.hangman.already_asserted('S') is True
