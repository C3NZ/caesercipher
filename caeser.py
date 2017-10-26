# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase chars.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return copy(self.valid_words)

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a char.
        The dictionary maps every uppercase and lowercase char to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase chars and all the lowercase
        chars only.        
        
        shift (integer): the amount by which to shift every char of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a char (string) to 
                 another char (string). 
        '''
        
        char_list = string.ascii_lowercase
        shift_dict = {}
         
        for i in range(len(char_list)):
            shift_dict[char_list[i]] = char_list[(i + shift) % 26]

        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        new_message = []
        shift_dict = self.build_shift_dict(shift)

        #Apply shift to each char
        for char in self.message_text:
            if char.lower() in string.ascii_lowercase and char != char.lower():
                new_message.append(shift_dict[char.lower()].upper())
            elif char not in string.ascii_lowercase:
                new_message.append(char)
            else:
                new_message.append(shift_dict[char])

        return "".join(new_message)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)

        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return copy(self.encryption_dict)

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        
        best_shift = 0
        largest_word_freq = 0
        best_result = []

        #decrypt the encrypted message by applying all possible shifts
        #to the message and then seeing which shifted message produces the most
        #valid words to determine the key used
        for i in range(26, -1, -1):
            
            decrypted_text = self.apply_shift(i)
            each_word = decrypted_text.split()
            shift_word_freq = 0

            for word in each_word:
                if is_word(self.valid_words, word):
                    shift_word_freq += 1

            if shift_word_freq > largest_word_freq:
                best_result.clear()
                best_result.append((i, decrypted_text))
                largest_word_freq = shift_word_freq

            elif shift_word_freq == largest_word_freq and shift_word_freq > 0:
                best_result.append((i, decrypted_text))

        if len(best_result) > 1:
            import random
            return random.choice(best_result)
        else:
            return best_result[0]


if __name__ == '__main__':

    #Test cases
    print('---New plaintext message---')
    print("New plaintext message\n")
    plaintext = PlaintextMessage('hello', 2)
    expected_output = 'jgnnq'
    actual_output = plaintext.get_message_text_encrypted()
    print('\nMessage: "{}" | Shift: {}'.format(plaintext.get_message_text(), plaintext.get_shift()))
    print('Expected Output: ' + expected_output)
    print('Actual Output:', actual_output)
    assert actual_output == expected_output, "FAILURE: output doesn't match"
    print('\n')

    print('---New cipher---')
    print('New cipher\n')
    ciphertext = CiphertextMessage('jgnnq')
    expected_output = (24, 'hello')
    actual_output = ciphertext.decrypt_message()
    print('\nMessage to decrypt: {}'.format(ciphertext.get_message_text()))
    print('Expected Output:', expected_output)
    print('Actual Output:', actual_output)
    assert actual_output == expected_output, "FAILURE: output doesn't match"
    print('\n')

    print('---New plaintext message---')
    plaintext = PlaintextMessage('what is up world?', 10)
    expected_output = 'grkd sc ez gybvn?'
    actual_output = plaintext.get_message_text_encrypted()
    print('\nMessage: "{}" | Shift: {}'.format(plaintext.get_message_text(), plaintext.get_shift()))
    print('Expected Output:', expected_output)
    print('Actual Output:', actual_output)
    assert actual_output == expected_output, "FAILURE: output doesn't match"
    print('\n')

    print('---New cipher---')
    ciphertext = CiphertextMessage('znoy oy g xkgrre iuur ykixkz skyygmk zngz somnz tuz hk makyykj')
    expected_output = (20, 'this is a really cool secret message that might not be guessed')
    actual_output = ciphertext.decrypt_message()
    print('\nMessage: {}'.format(ciphertext.get_message_text()))
    print('Expected Output:', expected_output)
    print('Actual Output:', actual_output)
    assert actual_output == expected_output, "FAILURE: output doesn't match"
    print('\n')

    print('Okay, all tests have passed, now let\'s decrypt this story')

    story = get_story_string()
    print('Here is the story:')
    print(story)
    print('\n Decrypting the message...\n')

    story_ciphertext = CiphertextMessage(story)
    print(story_ciphertext.decrypt_message())

