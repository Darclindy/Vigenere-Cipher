import string

"""
Script that runs through a Vigenere cipher text and tries to get an appropriate key based on the frequency

Index of coincidence is SUM(Z-A) Fi(Fi - 1)/N(N - 1)
Where Fi is the sum of occurrences of the letter, N is total number of letters in cipher text

Vigenere Cipher:
Say cipher text is ABCDEF
You check ACE and BDF and average
Then you check AD, BE, and CF and average
Former is 2 length key, latter 3
"""

# Arbitrary constant to reduce runtime
MAX_KEY_LENGTH = 50
# Arbitrary IOC threshold to determine when the distribution is likely english (Website said 0.06)
MIN_IOC_THRESHOLD = 0.07

cipher_text = "alp gwcsepul gtavaf, nlv prgpbpsu mb h jcpbyvdlq, ipltga rv glniypfa we ekl 16xs nsjhlcb. px td o " \
              "lccjdstslpahzn fptspf xstlxzi te iosj ezv sc xcns ttsoic lzlvrmhaw ez sjqijsa xsp rwhr. tq vxspf " \
              "sciov, alp wsphvcv pr ess rwxpqlvp nwlvvc dyi dswbhvo ef htqtafvyw hqzfbpg, ezutewwm zcep xzmyr o " \
              "scio ry tscoos rd woi pyqnmgelvr vpm . qbctnl xsp akbflowllmspwt nlwlpcg, lccjdstslpahzn fptspfo " \
              "oip qvx dfgysgelipp ec bfvbxlrnj ojocjvpw, ld akfv ekhr zys hskehy my eva dclluxpih yoe mh " \
              "yiacsoseehk fj l gebxwh sieesn we ekl iynfudktru. xsp yam zd woi qwoc."

def sanitize_string(input_string):
    """Sanitizes a given string and returns a string with only alphabetical characters"""
    input_string = input_string.lower()
    return ''.join(filter(str.isalpha, input_string))


def calculate_ioc(input_string):
    """Calculates Index of Coincidence"""

    frequency_sum = 0

    for char in string.ascii_lowercase:
        frequency_sum += input_string.count(char) * (input_string.count(char) - 1)

    return frequency_sum/(len(input_string)*(len(input_string) - 1))


def calculate_best_ioc(input_string):
    """Finds the first key length by finding length that passes IOC threshold"""

    input_sanitized = sanitize_string(input_string)
    running_ioc = 0
    running_key = 0

    for i in range(2, MAX_KEY_LENGTH):
        # Grabs the key length being tested
        strings = []
        for j in range(0, i):
            # Grabs the strings for said key length
            intervals = ""
            index = j
            while index < len(input_sanitized):
                # Grabs appropriate characters on the sanitized string and adds them to interval string
                intervals += input_sanitized[index]
                index += i

            strings.append(intervals)

        total_ioc = 0
        for s in strings:
            total_ioc += calculate_ioc(s)

        average_ioc = total_ioc/len(strings)

        if average_ioc > running_ioc:
            running_ioc = average_ioc
            running_key = i

        # THIS STEP IS 100% BASED ON AN ARBITRARY VALUE
        if running_ioc > MIN_IOC_THRESHOLD:
            return running_key


def calculate_chi_squared(input_string):
    """Computes Chi Squared statistic on given string based on letter frequency"""

    letter_frequency = {"a": 0.08167, "b": 0.01492, "c": 0.02782, "d": 0.04253, "e": 0.12702, "f": 0.02228,
                        "g": 0.02015, "h": 0.06094, "i": 0.06966, "j": 0.00153, "k": 0.00772, "l": 0.04025,
                        "m": 0.02406, "n": 0.06749, "o": 0.07507, "p": 0.01929, "q": 0.00095, "r": 0.05987,
                        "s": 0.06327, "t": 0.09056, "u": 0.02758, "v": 0.00978, "w": 0.02360, "x": 0.00150,
                        "y": 0.01974, "z": 0.00074}

    chi_squared = 0

    for char in string.ascii_lowercase:
        expected_freq = len(input_string) * letter_frequency[char]
        chi_squared += ((input_string.count(char) - expected_freq)**2)/expected_freq

    return chi_squared


def format_into_ceasar(input_string, key_len):
    """Gets given a Vigenere Cipher string and formats it into a list of Ceasar Cipher strings based on Key Len"""

    current_string = list(input_string)
    return_strings = [[] for i in range(0, key_len)]

    for i in range(0, len(current_string)):
        return_strings[i % (key_len)].append(current_string[i])

    return return_strings


def find_key(input_string):
    """Attempts to find the key to a Vigenere Cipher based on Key Len and Chi-Squared algorithm"""

    input_string = sanitize_string(input_string)
    key_len = calculate_best_ioc(input_string)
    ceasared_strings = format_into_ceasar(input_string, key_len)
    key = list("a" * key_len)

    for i in range(0, key_len):
        running_chi_squared = 9999  # Large arbitrary value
        running_char = ""
        for char in string.ascii_lowercase:
            deciphered_string = ""
            for letter in ceasared_strings[i]:
                deciphered_string += string.ascii_lowercase[ord(letter) - ord(char)]
            current_chi_squared = calculate_chi_squared(deciphered_string)
            if current_chi_squared < running_chi_squared:
                running_chi_squared = current_chi_squared
                running_char = char

        key[i] = running_char

    return "".join(key)


print(find_key(cipher_text))
