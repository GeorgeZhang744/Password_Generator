import random
from tkinter import *
from tkinter import messagebox

import password_setting as PS

NUMBERS = tuple([str(x) for x in range(10)]) # Create a tuple of integers from 0 to 9
LOWERCASES = tuple([chr(x) for x in range(97, 123)]) # Create a tuple of lowercase letters of alphabet
UPPERCASES = tuple([chr(x) for x in range(65, 91)]) # Create a tuple of uppercase letters of alphabet
SYMBOLS = ('`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', 
                 '{', '}', '\\', '|', ';', ':', '\'', '\"', ',', '<', '.', '>', '/', '?')
SIMILAR_CHARACTERS = ('i', 'l', '1', 'I', '!', '|', 'o', '0', 'O', ';', ':')
AMBIGUOUS_CHARACTERS = ('[', ']', '{', '}', '(', ')', '<', '>', ';', ':', '\'', '\"')

PASSWORD_MAX_LENGTH = 20
PASSWORD_MIN_LENGTH = 6

class PasswordGenerator:
    # Initialize the password generator given the expected length of the password
    def __init__(self, password_length, include_numbers=True, include_lowercases=True, 
                 include_uppercases=True, include_symbols=True,
                 exclude_similar_chars=False, exclude_ambiguous_chars=False):
        self.__password_length = password_length
        self.__settings = {
            'numbers': PS.PasswordSetting(include_numbers, NUMBERS),
            'lowercases': PS.PasswordSetting(include_lowercases, LOWERCASES),
            'uppercases': PS.PasswordSetting(include_uppercases, UPPERCASES),
            'symbols': PS.PasswordSetting(include_symbols, SYMBOLS)
        }
        self.__excluding_characters = {
            "similar_characters": PS.PasswordSetting(exclude_similar_chars, SIMILAR_CHARACTERS),
            "ambiguous_characters": PS.PasswordSetting(exclude_ambiguous_chars, AMBIGUOUS_CHARACTERS)
        }

    # Update the password length
    def set_password_length(self, new_length):
        if new_length < PASSWORD_MIN_LENGTH:
            raise Exception(f"Password's length must be longer than {PASSWORD_MIN_LENGTH}")
        if new_length > PASSWORD_MAX_LENGTH:
            raise Exception(f"Password's length must be short than {PASSWORD_MAX_LENGTH}")
        
        self.__password_length = new_length

    # Set the given password generator setting to on/off
    def change_setting(self, setting_to_change, on_off):
        if setting_to_change not in self.__settings.keys():
            raise Exception(f"Setting {setting_to_change} does not exist")
        
        self.__settings[setting_to_change].change_setting(on_off)

    # Set the given password generator filter (setting that filters out a certain characters in the generated password) to on/off
    def change_filter_setting(self, setting_to_change, on_off):
        if setting_to_change not in self.__excluding_characters.keys():
            raise Exception(f"Setting {setting_to_change} does not exist")
        
        self.__excluding_characters[setting_to_change].change_setting(on_off)

    # Generate the password with given password length based on the password settings that are on
    def generate_password(self):
        new_password = ''

        included_characters = [set(setting.get_components()) for setting in self.__settings.values() if setting.is_setting_on()]

        if len(included_characters) == 0:
            messagebox.showerror("Error", "The password must include something!")

        excluded_characters = [set(excluded_chars.get_components()) for excluded_chars in self.__excluding_characters.values() if excluded_chars.is_setting_on()]

        filtered_result = []
        for chars in included_characters:
            filtered_chars = chars
            for excluded_chars in excluded_characters:
                filtered_chars = filtered_chars.difference(excluded_chars)

            if len(filtered_chars) != 0:
                filtered_result.append(list(filtered_chars))

        for _ in range(self.__password_length):
            new_password += (random.choice(random.choice(filtered_result)))

        return new_password