from .cat_number_letter import num_let
from collections import Counter
import re
from urllib.parse import urlparse #used to check if a string is an url
import csv

lett2spell = {
    "a": "a",
    "b": "be",
    "c": "ce",
    "ç": "ce trencada",
    "d": "de",
    "e": "e",
    "f": "efa",
    "g": "ge",
    "h": "hac",
    "i": "i",
    "j": "jota",
    "k": "ka",
    "l": "ela",
    "m": "ema",
    "n": "ena",
    "o": "o",
    "p": "pe",
    "q": "cu",
    "r": "erra",
    "s": "essa",
    "t": "te",
    "u": "u",
    "v": "ve baixa",
    "w": "ve doble",
    "x": "ics",
    "y": "i grega",
    "z": "zeta"
}

num2months = {
    "01": "gener",
    "02": "febrer",
    "03": "març",
    "04": "abril",
    "05": "maig",
    "06": "juny",
    "07": "juliol",
    "08": "agost",
    "09": "setembre",
    "10": "octubre",
    "11": "novebre",
    "12": "desembre"
}
sym2spell = {
    "!": "exclamació",
    "%": "percentatge",
    ".": "punt",
    ":": "dos punts",
    "&": "et",
    "'": "apòstrof",
    "(": "obre parèntesi",
    ")": "tanca parèntesi",
    ",": "coma",
    "-": "guió",
    "/": "barra diagonal",
    "=": "igual",
    "<": "menor que",
    ">": "major que",
    "?": "interrogant",
    "@": "arrova",
    "[": "obre claudàtor",
    "]": "tanca claudàtor",
    "^": "circumflex",
    "_": "guió baix",
    "{": "obre clau",
    "}": "tanca clau",
    "|": "barra vertical",
    "€": "euro",
    "$": "dòlar",
    "¥": "ien",
    "~": "vírgula"
}

dict_abbreviatures = {}
abbrev_csv = '/home/alvaro/TTS-API/csv_files/dict_abbrv.csv'

with open(abbrev_csv, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if len(row) == 2:  
            key, value = row[0], row[1]
            dict_abbreviatures[key] = value

def canBeNumber(n):
    try:
        int(n)
        return True
    except ValueError:
        # Not a number
        return False

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

# STUB: Function to write out letter (b->be, w->ve doble)
#     #Source: https://www.cursdecatala.com/es/pronunciar-el-alfabeto-catalan/

def pronounce_letter(letter):
    letter = letter.lower()
    for key, val in lett2spell.items():
        if (letter == key):
            return val

def pronounce_symbol(letter):
    for key, val in sym2spell.items():
        if letter == key:
            return val

def abbreviature_word(word):
    for key, val in dict_abbreviatures.items():
        if word.lower() == key.lower():
            return val, True
    return None, False

def read_hours(text):
    if not text.endswith(":"):
        hour_part, minute_part = text.split(':')
        hour_processed = num_let(int(remove_nonnumber(hour_part)))
        minute_processed = num_let(int(remove_nonnumber(minute_part)))
        text = hour_processed + " i " + minute_processed
        return text
    else:
        text.rstrip(":")

def read_dates(text):
    if "/" in text:
        day, month, year = text.split('/')
    elif "-" in text:
        day, month, year = text.split('-')
    day_processed = num_let(int(remove_nonnumber(day)))
    year_processed = num_let(int(remove_nonnumber(year)))
    for key, value in num2months.items():
        if str(month) == key:
            month_processed = num2months[key]
    text = day_processed + " de " + month_processed + " de " + year_processed
    return text

def is_url(text):
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc]) 
    except:
        return False

def webpage(text):
    try:
        print('debug1')
        result = urlparse(text)
        res_args = [result.scheme, result.netloc, result.path, result.params, result.query, result.fragment]
        res = [var for var in res_args if var]
        res = ' '.join(res)

        for symbol, spelling in sym2spell.items():
            if symbol in res:
                res = res.replace(symbol, f' {spelling} ')
        
        find_numbers = res.split()
        for i, word in enumerate(find_numbers):
            if has_numbers(word):
                word = num_let(int(remove_nonnumber(word)))
                find_numbers[i] = word
            
            print('debug2', word)
            res_word, output = abbreviature_word(word)
            print(res_word, output)
            if output:
                print('word is ' + res_word)
                find_numbers[i] = res_word

        return ' '.join(find_numbers)

    except Exception as e:
        return e

def remove_nonnumber(text):
    return re.sub('[^0-9]','', text)

def text_preprocess(text):
    text = text.strip()
    text = text.replace('&', 'i')
    text = re.sub('[Ö|ö]', 'o', text)
    text = re.sub('[ş|Ş]', 's', text)
    text = re.sub('[ü|Ü]', 'u', text)
    #text = re.sub('[ç|Ç]', 'c', text)
    text = re.sub('[İ|ı]', 'i', text)

    #return ' '.join([num_let(int(remove_nonnumber(t))) if has_numbers(t) else t for t in text.split()])
    #return ' '.join([pronounce_letter(t) if (len(t) == 1 and type(t) is not int) else (num_let(int(remove_nonnumber(t))) if has_numbers(t) else t) for t in text.split()])

    processed_words = []

    for t in text.split():
        #if len(t) >= 3 and t[0] == "w" and t[1] == "w" and t[2] == "w" and t.count('.') >= 2:
            #processed_words.append(webpage(t))
            #check all functions so that system does not break if text doesnt fulfill

        if len(t) == 1 and t.isalpha():
            processed_words.append(pronounce_letter(t))
        
        elif len(t) == 1 and not t.isalpha() and not t.isdigit():
            processed_words.append(pronounce_symbol(t))
       
        elif is_url(t):
            processed_words.append(webpage(t))
        else:
            if has_numbers(t):
                if ':' in t:
                    processed_words.append(read_hours(t))

                elif t.count('/') == 2 or t.count('-') == 2 or t.count('.') == 2:
                    #condition that follows DD/MM/YYYY
                    print('debug' + str(read_dates(t)))
                    processed_words.append(read_dates(t))

                else:    
                    processed_words.append(num_let(int(remove_nonnumber(t))))
            else:
                processed_words.append(t)

    print(processed_words)
    return ' '.join(processed_words)