"""
Example of hooking the keyboard on Linux using pyxhook

Generates JSON for keystroke timings. Refer paper for format.
"""

import ast
import math
import time

import pynput
from pynput import keyboard
import numpy as np

keyWord = "pythonlab7"
frequency_keyWord_entry = 10
key_timings = dict()

user_keystroke_timings_list = list()
user_keystroke_timings_json = dict()

dict_intervals = dict()

for char in list(keyWord):
    key_timings[char] = dict()
    key_timings[char]['keyDown'] = None
    key_timings[char]['keyUp'] = None

key_timings["Return"] = {"keyUp": None, "keyDown": None}

a_key_down = dict()
a_key_up = dict()


# This function is called every time a key is pressed down
def kb_down_event(key):
    try:
        # Sprint(key)
        if key != keyboard.Key.enter and key != keyboard.Key.backspace and key != keyboard.Key.down and key != keyboard.Key.up and key != keyboard.Key.left and key != keyboard.Key.right:
            # key_timings[key]["keyUp"] = time.time()
            a_key_down[key.char] = time.time()
        # print(key_timings[key]["keyUp"] )
    except KeyError or AttributeError:
        # print("This key is not to be recorded : ", event.Key)
        pass


# This function is called every time a keypress is released
def kb_up_event(key):
    try:
        if key != keyboard.Key.enter and key != keyboard.Key.backspace and key != keyboard.Key.down and key != keyboard.Key.up and key != keyboard.Key.left and key != keyboard.Key.right:
            # print(key.char)
            # key_timings[key]["keyDown"] = time.time()
            a_key_up[key.char] = time.time()

    except KeyError or AttributeError:
        pass

def check_user(user_name, attempt, math_expect, despersion):
    with open('output/{}_studying_math_expect.txt'.format(user_name), 'r') as outfile:
        contents = outfile.read()
        dict_math_expect = ast.literal_eval(contents)
    with open('output/{}_studying_despersion.txt'.format(user_name), 'r') as outfile:
        contents = outfile.read()
        dict_despersion = ast.literal_eval(contents)
    # checking
    k = 1
    s2 = dict()
    while k <= len(dict_despersion):
        s1 = (math.pow(dict_despersion[k], 4) + math.pow(despersion, 4)) * (len(attempt) - 1)
        #print(dict_despersion[k],' ',despersion,' ', s1)
        s2[k] = (np.sqrt(s1 / ((2 * len(attempt)) - 1)))
        k += 1
    k = 1
    tp = dict()
    while k <= len(dict_math_expect):
        tp_abs = np.abs(dict_math_expect[k] - math_expect)
        tp[k] = tp_abs / (s2[k] * np.sqrt(2 / len(attempt)))
        k += 1
    print(tp)
    return (tp)


def study():
    user_name = input("Please enter your name: ")
    dict_intervals["user_name"] = user_name
    password_entry_count = 1
    listener = keyboard.Listener(on_press=kb_down_event, on_release=kb_up_event)
    listener.start()
    while password_entry_count <= frequency_keyWord_entry:
        dict_intervals[password_entry_count] = list()
        print("{} times left!".format(1 + frequency_keyWord_entry - password_entry_count))
        input_pwd = input("Enter '{}' : ".format(keyWord))
        is_pwd_correct = False
        if input_pwd == keyWord:
            print("pwd correct!")
            is_pwd_correct = True

        if is_pwd_correct:
            password_entry_count += 1
            # Calculate hold time of keys!

            for key1, key2 in zip(keyWord, keyWord[1:]):
                # Calculate ud_k1_k2    
                v = a_key_down[key2] - a_key_up[key1]
                dict_intervals[password_entry_count - 1].append(v)

        else:
            print("Password entered was not correct! Please type '{}' again !".format(keyWord))

    with open('output/{}_studying_intervals.txt'.format(user_name), 'w') as outfile:
        outfile.write(str(dict_intervals))
    listener.stop()

    dict_math_expect = dict()
    # mathematical expectation studying
    k = 1
    while k <= frequency_keyWord_entry:
        math_expect = 0
        i = 0
        while i < len(dict_intervals[k]):
            math_expect += dict_intervals[k][i]
            i += 1
        dict_math_expect[k] = (math_expect / len(dict_intervals[k]))
        k += 1

    # print (dict_math_expect)

    with open('output/{}_studying_math_expect.txt'.format(user_name), 'w') as outfile:
        outfile.write(str(dict_math_expect))

    # despersion studying
    dict_despersion = dict()
    k = 1
    while k <= frequency_keyWord_entry:
        i = 0
        despersion = 0
        while i < len(dict_intervals[k]):
            xk = dict_intervals[k][i]
            Mxk = dict_math_expect[k]
            despersion += (xk - Mxk) * (xk - Mxk)
            i += 1
        dict_despersion[k] = (math.sqrt(despersion / (len(dict_intervals[k]) - 1)))
        k += 1

    with open('output/{}_studying_despersion.txt'.format(user_name), 'w') as   outfile:
        outfile.write(str(dict_despersion))


def authentication():
    attempt = list()
    user_name = input("Enter your name: ")
    listener = keyboard.Listener(on_press=kb_down_event, on_release=kb_up_event)
    listener.start()
    input_pwd = input("Enter '{}' : ".format(keyWord))
    while (input_pwd != keyWord):
        print("Password entered was not correct! Please type '{}' again !".format(keyWord))
        input_pwd = input("Enter '{}' : ".format(keyWord))

    print("pwd correct!")

    for key1, key2 in zip(keyWord, keyWord[1:]):
        # Calculate ud_k1_k2
        v = a_key_down[key2] - a_key_up[key1]
        attempt.append(v)

    # print(attempt)

    with open('output/{}_authentication_intervals.txt'.format(user_name), 'w') as outfile:
        outfile.write(str(attempt))
    listener.stop()

    math_expect = 0
    # mathematical expectation authentication
    i = 0
    while i < len(attempt):
        ts = attempt[i]
        math_expect += ts
        i += 1
    math_expect = math_expect / len(attempt)

    # print (dict_math_expect)

    with open('output/{}_authentication_math_expect.txt'.format(user_name), 'w') as outfile:
        outfile.write(str(math_expect))

    # despersion authentication
    despersion = 0
    i = 0
    while i < len(attempt):
        yi = attempt[i]
        despersion += (yi - math_expect) * (yi - math_expect)
        i += 1
    despersion = (math.sqrt(despersion / (len(attempt) - 1)))

    with open('output/{}_authentication_despersion.txt'.format(user_name), 'w') as outfile:
        outfile.write(str(despersion))

    tp = check_user(user_name, attempt, math_expect, despersion)
    # print(tp)

    # from table student 9-1 intervals
    t_theory = 2.31

    k = 1
    r = 0
    while k <= (frequency_keyWord_entry):
        if t_theory > tp[k]:
            print(tp[k], ' ', t_theory)
            r += 1
        k += 1
    print("successful: {} out of: {}".format(r, frequency_keyWord_entry))

    probability = (r / frequency_keyWord_entry)
    print('The probability of the validity of the user: {}'.format('%.2f' % probability))
    if probability >= 0.6:
        print("authentication is approved")
    else:
        print("authentication fails")


def selection(argument):
    switcher = {
        "0": study,
        "1": authentication
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "Invalid input")
    # Execute the function
    (func())

argument=-1
while(argument!="2"):
    print()
    print("Please, choose (0) for studying, (1) for authentication or (2) for exit")
    print(
        "PAY ATTENTION! When you run the program please don't press extra buttons on your keyboard. In such case results can be incorrect!")
    argument = input("Select studying (0) or authentication (1) or exit (2): ")
    # print(argument)
    if(argument!="2"):
        selection(argument)

