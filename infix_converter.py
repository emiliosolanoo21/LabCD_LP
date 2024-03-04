from typing import *
from Classes_ import FormatPointer


def is_operator(token):
    operators = "|?.+*^"
    return token in operators


def precedence(operator: str) -> int:
    return {
        '(': 1, ')': 1, '[': 1, ']': 1, '{': 1, '}': 1,
        '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5, '∗': 4,
    }.get(operator, -1)


def counterSymbol(character: str) -> str:
    return {
        '(': ')',
        '[': ']',
        '{': '}',
        ')': '(',
        ']': '[',
        '}': '{',
    }.get(character, ' ')


def is_binary(token):
    operators = "^|"
    return token in operators


def extract_alphabet(content: List[str]) -> List[str]:
    """Extracts the alphabet from the regular expressions"""
    alphabet: List[str] = []

    for expression in content:
        alphabets = {x for x in expression if x not in '()[]{}|?*ε'}
        alphabet.append(''.join(alphabets))

    return alphabet


def format_regex(content: List[str]) -> List[str]:
    """Formats the regular expressions to be used in the program"""
    formatted: List[str] = []

    def format_(expression_: str) -> str:
        pointer: FormatPointer = FormatPointer()
        operators = '*|?+'  # Operators that can be used in the regular expression

        for i in range(len(expression_)):
            c1 = expression_[i]
            c2 = "*"

            if i + 1 < len(expression_):
                c2 = expression_[i + 1]

            if c1 in '([{':
                pointer.inGroup()
            elif c1 in ')]}':
                pointer.outGroup()

            if c1 == '?':
                pointer.interrogation()
            elif c1 == '+':
                pointer.plus()
            else:
                if c1 not in '([{)]}':
                    pointer.push(c1)

            if c1 not in '|' and c2 not in operators and c2 not in ')]}':

                if c1 not in '([{':
                    c = pointer.actual.stack.pop()
                    pointer.push(c+'.')

        result = pointer.__str__()

        return result

    for expression in content:
        exp = expression.replace('[', '(').replace(']', ')')
        exp = exp.replace('{', '(').replace('}', ')')
        formatted.append(format_(exp))

    return formatted


def translate_to_postfix(content: List[str]) -> List[str]:
    """Converts regulars expressions from infix to postfix notation whit shutting yard algorithm"""
    postfix_format: List[str] = []

    def infix_to_postfix(regex):
        postfix = ""
        postfix_stack = []
        escape_char = False
        formatted_regex = regex
        completed = False

        for character in formatted_regex:
            if character == '\\':
                escape_char = True
            elif character == ' ':
                escape_char = True
            elif character == '[':
                if not escape_char:
                    completed = True
                    postfix += character
            elif character in '{([':
                if not escape_char:
                    postfix_stack.append(character)
            elif character in '})]':
                if not escape_char:
                    while postfix_stack and postfix_stack[-1] != counterSymbol(character):
                        postfix += postfix_stack.pop()
                    postfix_stack.pop()  # Eliminar el paréntesis izquierdo '(' de la pila
            else:
                if (not is_operator(character) and not is_binary(character)) or escape_char or completed:
                    escape_char = False
                    postfix += character
                else:
                    while postfix_stack:
                        picked_char = postfix_stack[-1]
                        pd_picked_char = precedence(picked_char)
                        pd_actual_char = precedence(character)
                        if pd_picked_char >= pd_actual_char:
                            postfix += postfix_stack.pop()
                        else:
                            break
                    postfix_stack.append(character)

        while postfix_stack:
            postfix += postfix_stack.pop()

        return postfix

    for expression in content:
        postfix_format.append(infix_to_postfix(expression))

    return postfix_format
