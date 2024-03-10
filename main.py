from subprocess import run
from Simulator import *
from reader import reader
from Tree_ import make_direct_tree, make_tree
from Draw_diagrams import draw_tree
from typing import Dict
from preAFD import *
from Colors import BOLD, REVERSE, GREEN, YELLOW, RESET

regex = {
    'comments': ['\(\*[^()]+\*\)'],
    'declarations': ['let +[a-z]+ *= *\n*([^ \n\t]|\'[^\']\'|"[^"]+")+'],
    'tokens': ['(\| +)?([^ \n\t]|\'[^\']\'|"[^"]+")+( +\{ *return +[A-Z]+ *\})?'],
    'RL': ['rule +[a-z]+ *=']
}

machine = import_module('machine.plk', regex)

file = reader('lexer1.yal')

print(exclusiveSim(machine, file))