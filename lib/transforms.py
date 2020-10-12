#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - transform functions module

from multiprocessing.dummy import Pool as ThreadPool

from lib.config import Config


################################################################################
def case_transforms(word):
    new_wordlist = []

    # Make each one upper (hello => Hello, hEllo, heLlo, helLo, hellO)
    i=0
    for char in word:
        new_word = word[:i] + char.upper() + word[i+1:]
        i += 1
        if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make pairs upper (hello => HeLlO)
    i=0
    new_word = ''
    for char in word:
        if i % 2 == 0: new_word += char.upper()
        else: new_word += char
        i += 1
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make odds upper (hello => hElLo)
    i=0
    new_word = ''
    for char in word:
        if i % 2 != 0: new_word += char.upper()
        else: new_word += char
        i += 1
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make consonants upper (hello => HeLLo)
    vowels = 'aeiou'
    new_word = ''
    for char in word:
        if char.lower() not in vowels: new_word += char.upper()
        else: new_word += char
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # Make vowels upper (hello => hEllO)
    new_word = ''
    for char in word:
        if char.lower() in vowels: new_word += char.upper()
        else: new_word += char
    if new_word not in new_wordlist: new_wordlist.append(new_word)

    # recursive call function (not working, maybe this option won't be even useful)
    # for new_word in new_wordlist:
    #     original_size = len(new_wordlist)
    #     new_wordlist.extend(case_transforms(new_word))
    #     if len(new_wordlist) == original_size:
    #         break  # breaking recursive call

    return new_wordlist


################################################################################
def leet_transforms(word):
    new_wordlist = []
    i=0
    leet_charset = Config.LEET_CHARSET
    for char in word:
        for lchar in leet_charset:
            leeted_char = ''
            if lchar.startswith(char.lower()):
                leeted_char = lchar[-1:]
                new_word = word[:i] + leeted_char + word[i + 1:]
                if new_word not in new_wordlist: new_wordlist.append(new_word)
                # dont break to allow multiple transforms to a single char (e.g. a into 4 and @)
        i += 1

    # recursive call function
    #recursive_leet = read_config('TRANSFORMS', 'recursive_leet')
    if Config.RECURSIVE_LEET:
        for new_word in new_wordlist:
            original_size = len(new_wordlist)
            new_wordlist.extend(leet_transforms(new_word))
            if len(new_wordlist) == original_size:
                break  # breaking recursive call

    return new_wordlist


################################################################################
def multithread_transforms(transform_type, wordlist):
    pool = ThreadPool(16)
    # process each word in their own thread and return the results
    new_wordlist = pool.map(transform_type, wordlist)
    pool.close()
    pool.join()
    for lists in new_wordlist:
        wordlist += lists
    return new_wordlist


################################################################################
def space_transforms(word):
    new_wordlist = [word,]
    if ' ' in word:  # Avoiding non-space words to be included many times
        new_wordlist.append(word.replace(' ', ''))
        if Config.SPACE_REPLACEMENT_CHARSET:
            for character in Config.SPACE_REPLACEMENT_CHARSET:
                new_wordlist.append(word.replace(' ', character))

    return new_wordlist


################################################################################
def take_initials(word):
    splitted = word.split(' ')
    initials = ''
    for char in splitted:
        try: initials += char[0]
        except IndexError: continue
    return initials
