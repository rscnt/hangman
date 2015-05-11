"""
Engines that could be used to write a mediocre hangman game interface.
"""

from hangman.core.errors import InvalidGuessError


class HangmanEngine:
    """ Core of a Hangman game.

    Provides basic functionality of a simple game, a guess string, lives or
    changes to guess it and case sensitivity functionality, if needed.

    Attributes:
        string_to_guess (str):  The Word or Sentence to guess in the game.
        guess_misses (list): Chars not in  string_to_guess attribute.
        guess_asserted (list): Chars in the string_to_guess attribute.
        case_sensitive (boolean, optional): Defaults to False.
        max_attempts (int, optional): The limit size of guess_misses attribute.

    """

    def __init__(self, string_to_guess, case_sensitive=False, max_attempts=5):
        """
        Args:
            string_to_guess (str): The sentences to guess in the game.
            case_sensitive (boolean, optional): Defaults to False.
            max_attempts (int, int): Limit of chars missed.

        """

        self.string_to_guess = string_to_guess
        self.case_sensitive = case_sensitive
        self.max_attempts = max_attempts
        self.guess_misses = []
        self.guess_asserted = []
        self.found_indexes = []
        self.list_string_found = list('*'*len(string_to_guess))

    def count(self, char):
        """ Returns the number of times a character appears in the guess_string
        attribute.

        If the engine is configured to be case sensitive, this method returns
        the total occurrences in both cases (upper and down).

        Args:
            char (str): A string, but its length has to be equal to 1.

        """

        self.__class__.check_character(char)
        result = 0
        if self.case_sensitive:
            result = self.string_to_guess.count(char)
        else:
            result = self.count_uppercase(char) + self.count_downcase(char)

        return result

    def count_downcase(self, char):
        """ Returns the number of times the char downcased appears in the
        string_to_guess attribute.

        Args:
            char (str): A string, but its length has to be equal to 1.

        """
        self.__class__.check_character(char)
        return self.string_to_guess.count(char.lower())

    def count_uppercase(self, char):
        """ Returns the number of times the char uppercased appears in the
        string_to_guess attribute.

        Args:
            char (str): A string, but its length has to be equal to 1.

        """
        self.__class__.check_character(char)
        return self.string_to_guess.count(char.upper())

    def already_asserted(self, char):
        """ Checks if the char is already asserted.

        Returns:
            bool: True if the char is already asserted. False otherwise.

        """
        return self.__class__.__already_collected(self.guess_asserted,
                                                  self.case_sensitive, char)

    def already_missed(self, char):
        """ Checks if the char is already missed.

        Returns:
            bool: True if the char is already missed. False otherwise.

        """
        return self.__class__.__already_collected(self.guess_misses,
                                                  self.case_sensitive, char)

    def already_tried(self, char):
        """ Checks if the char was already tried, missed or asserted.

        Returns:
            bool: True if the char was already tried. False otherwise

        """
        return self.already_asserted(char) or self.already_missed(char)

    def occurrences(self, char):
        """ All occurrences of the char passed in the guess_string attribute.

        If the engine is configured with case sensitivity then only returns the
        character occurrences but if not it chains both downcased and
        upppercased occurrences.

        Yields:
            int: The next index of the found char in the guess_string attribute.

        """
        self.__class__.check_character(char)
        result = None
        asserted_guess = self.already_asserted(char) or self.count(char)
        if asserted_guess:
            result = self.__occurrences(char)
        else:
            self.guess_misses.append(char)

        return result

    def get_text_found(self):
        """ Returns the string for the founded characters.
        """
        return ''.join(self.list_string_found)

    def __occurrences_downcase(self, char=''):
        """ Search for all the occurrences of a  char lowercased in the
        string_to_guess attribute.

        Yields:
            int: The next index of the found char in string_to_guess list.

        """

        return self.__occurrences(char.lower())

    def __occurrences_uppercase(self, char=''):
        """ Search for all the occurrences of a  char uppercased in the
        string_to_guess attribute.

        Yields:
            int: The next index of the found char in string_to_guess list.

        """

        return self.__occurrences(char.upper())

    def __occurrences(self, char=''):
        """ Search for all the occurrences of a char in the string_to_guess
        attribute.

        Yields:
            int: The next index of the found char in string_to_guess list.

        """

        self.__class__.check_character(char)
        times_should_appear = self.count(char)
        if times_should_appear:
            self.guess_asserted.append(char)
            last_i = found = 0
            while(found < times_should_appear):
                found_at = self.find_first_occurrence(char, last_i)
                if found_at is not -1:
                    occurrence_at = found_at + last_i if last_i else found_at
                    last_i = found_at + 1
                    found += 1
                    self.found_indexes.append(occurrence_at)
                    self.list_string_found[occurrence_at] = (
                        self.string_to_guess[occurrence_at]
                    )
                    yield occurrence_at

    def find_first_occurrence(self, char, start_index):
        """ Search the char in string_to_guess starting at an index.

        If the property case_sensitive is `False` then it will swapcase the
        char if found and the index is less that the first that last index
        will be returned.

        Args:
            char (str): The string to search.
            start_index (str, optional): The index to begin in.

        Returns:
            int: The index of the first occurrence.

        """
        str_part = self.string_to_guess[start_index:]
        result = first_result = str_part.find(char)
        second_result = -1
        if not self.case_sensitive:
            result = second_result = str_part.find(char.swapcase())
            # smelly... sometimes... you... just let it go...
            if first_result != -1:
                if second_result != -1:
                    if second_result < first_result:
                        result = second_result
                    else:
                        result = first_result

                else:
                    result = first_result

        return result

    @classmethod
    def __already_collected(class_, char_list, case_sensitive, char):
        """ Returns the number of times the char uppercased appears in the
        string_to_guess attribute.

        Args:
            char_list (list): A list of char.
            case_sensitive (boolean): Whatever or not search for the other case.
            char (str): Its length has to be equal to 1.

        Returns:
            bool: True if successful. False  otherwise.

        """
        class_.check_character(char)
        found = char in char_list
        if not case_sensitive and not found:
            found = char.swapcase() in char_list

        return found

    @classmethod
    def check_character(self, char):
        """ Check if the char is length of 1 and is alpha.

        Yes probably ord function could be used. But no mother-fucker it's not
        used deal with it.

        Returns:
            bool: True. When it fails then raise there's not falsehood.

        Raise:
            InvalidGuessError: If the char is not length of 1 and not alpha.

        """
        if len(char) != 1 and char is not char.isalpha():
            raise InvalidGuessError(char)
        return True

    def get_status_text(self):
        return "Found {0}/{1} | Lost Attempts {2}/{3}".format(
            len(self.found_indexes), len(self.string_to_guess),
            len(self.guess_misses), self.max_attempts
        )

    def __repr__(self):
        return "Case sensitive: {0}, Max Attempts: {1}, Length: {2}".format(
            self.case_sensitive, self.max_attempts, len(self.string_to_guess)
        )
