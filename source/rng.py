# python 3.7.1
from random import *

''' method 1
lowercases = [chr(_) for _ in range (ord('a'), ord('z') + 1)]

uppercases = [chr(_) for _ in range (ord('A'), ord('Z') + 1)]

numbers = [chr(_) for _ in range (ord('0'),ord('9') + 1)]
'''

# method 2
import string


class StringGenerator:

    def __init__(self):

        self.specials = '_-*@/'
        self.full_specials = '''"!#$%&'()*+-./:;<=>?@[]\\^_`{|}~'''

        self.char_list = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
            self.specials,
            self.full_specials
        ]

        self.length = 0
        self.MIN_LENGTH = 8
        self.max_length = 100 - len(self.full_specials)
        self.is_full_special = False
        self.l_len = None
        self.is_repeatable = None

    def get_idx(self):
        if self.is_full_special:
            idx = randint(0, 4)
            while idx == 3:
                idx = randint(0, 4)
        else:
            idx = randint(0, 3)
        return idx

    def get_input(self):
        if self.is_repeatable is None:
            self.is_repeatable = input("Allows repeated characters? (y/n)\t").lower() == 'y'

        if self.is_full_special is None:
            self.is_full_special = input("Contains full special characters? (y/n)\t").lower() == 'y'
        if self.is_full_special:
            self.max_length = 100 - len(self.specials)

        try:
            while self.length is None or self.length < self.MIN_LENGTH or \
                    (not self.is_repeatable and self.length > self.max_length):
                if self.length is not None:
                    print("Invalid input")
                s = f"How many characters? (min = {self.MIN_LENGTH}"
                if not self.is_repeatable:
                    s += f", max = {self.max_length}"

                self.length = int(
                    input(f"{s})\t")
                )
        except ValueError:
            self.length = self.MIN_LENGTH  # default

    def get_len(self):
        temp = int(self.length / 4)
        self.l_len = [temp] * 5

        if self.is_full_special and not self.is_repeatable:
            self.l_len[3] = len(self.specials)

        if temp * 4 < self.length:
            for i in range(0, self.length - temp * 4):
                idx = self.get_idx()
                while not self.is_repeatable and self.l_len[idx] >= len(self.char_list[idx]):
                    idx = self.get_idx()
                self.l_len[idx] += 1
                # print(self.l_len)

        if self.is_repeatable:
            return

        for i in range(0, len(self.l_len)):
            while self.l_len[i] > len(self.char_list[i]):
                idx = self.get_idx()

                while self.l_len[idx] == len(self.char_list[idx]):
                    idx = self.get_idx()
                self.l_len[idx] += 1
                self.l_len[i] -= 1

    def get(self, length=None, fs=None, rp=None):
        self.is_full_special = fs
        self.is_repeatable = rp
        self.length = length
        self.get_input()
        self.get_len()

        password_characters = []

        if not self.is_repeatable:
            # faster than + (concat)
            password_characters = [
                *sample(self.char_list[0], self.l_len[0]),
                *sample(self.char_list[1], self.l_len[1]),
                *sample(self.char_list[2], self.l_len[2])
            ]

            if self.is_full_special:
                password_characters.extend(
                    sample(self.char_list[4], self.l_len[4])
                )
            else:
                password_characters.extend(
                    sample(self.char_list[3], self.l_len[3])
                )

        else:
            for i in range(0, 5):
                if i == 3 and self.is_full_special:
                    i = 4

                if self.l_len[i] > len(self.char_list[i]):
                    while self.l_len[i] > len(self.char_list[i]):
                        password_characters.extend(
                            sample(self.char_list[i], 1)
                        )
                        self.l_len[i] -= 1

                password_characters.extend(
                    sample(self.char_list[i], self.l_len[i]
                           )
                )

                if (i == 4 and self.is_full_special) or \
                        (i == 3 and not self.is_full_special):
                    break

        # print(self.l_len)
        shuffle(password_characters)

        return ''.join(password_characters)


# BEST EFFORT NON_REPEATED CHARACTERS 
# GET(LENGTH, USE_FULL_SPECIAL_CHARS, IS_REPEATABLE)     
# buffer = PasswordGenerator()
#
# while input("Continue? (y/n) \t").lower() != 'n':
#     # new_pass = buffer.get(8)
#
#     # new_pass = buffer.get(67, 0)
#     # new_pass = buffer.get(67, 1)
#     # new_pass = buffer.get(67, 0, 1)
#     # new_pass = buffer.get(67, 1, 1)
#
#     # new_pass = buffer.get(20)
#     # new_pass = buffer.get(20, 0)
#     # new_pass = buffer.get(20, 1)
#
#     # new_pass = buffer.get(95)
#     # new_pass = buffer.get(95, 0, 1)
#     # new_pass = buffer.get(95, 1, 0)
#     # new_pass = buffer.get(95, 1, 1)
#
#     # new_pass = buffer.get(200, 0, 1)
#     # new_pass = buffer.get(200, 1, 1)
#
#     # new_pass = buffer.get(1000,0,1)
#
#     new_pass = buffer.get()
#
#     print(f"Pass = {new_pass}")
#     print(f"Len = {len(new_pass)}", end='\n\n')
