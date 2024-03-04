from typing import *


def reader(filename: str) -> List[str]:
    contents = []
    """Reads a file and returns its contents"""
    with open(filename, 'r', encoding='utf-8') as archivo:
        line = archivo.readlines()
        for i in line:
            if len(i.strip().replace(' ', '')) != 0:
                contents.append(i.strip().replace(' ', ''))
    return contents


def validate(contents: List[str]) -> List[str]:
    """Validates the contents of the file are correct expressions"""
    counterparty = {
        '(': ')',
        '[': ']',
        '{': '}',
        ')': '(',
        ']': '[',
        '}': '{',
    }

    accepted = []

    '''Validate the expressions are balanced'''
    for line in contents:
        pila_regex = []
        test = True
        for character in line:
            if character in '([{':
                pila_regex.append(character)
            elif character in ')]}':
                if pila_regex:
                    if counterparty[pila_regex[-1]] == character:
                        pila_regex.pop()
                    else:
                        test = False
                        break
                else:
                    test = False
                    break

        if len(pila_regex) == 0 and test:
            accepted.append(line)

    return accepted
