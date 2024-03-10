from reader import *
from infix_converter import *
from Tree_ import *
from AFD import *
from Minimized import *
import string
import os
import importlib.util
import pickle
from Draw_diagrams import draw_AF, draw_tree


def prepareAFN(expressions: Dict[str, List[str]], showTree = False) -> State:
    initState: State or None = None
    cont = 0
    treeN = []
    for token, regex in expressions.items():
        parsed: List[List[str or int]] = transformsChar(regex)
        accepted: List[List[str or int]] = validate(parsed)
        alphabets: List[Set[int]] = extract_alphabet(accepted)
        formatted: List[List[str or int]] = format_regex(accepted)
        postfix: List[str or int] = translate_to_postfix(formatted)
        for i in range(len(postfix)):
            tree = make_direct_tree(postfix[i])
            treeN.append(tree[0])
            direct = make_direct_AFD(tree[0], tree[1], alphabets[i], token)
            minimize = minimizeAFD(direct[2], alphabets[i], id_=string.ascii_lowercase[cont])
            if initState is None:
                initState = minimize[1]
            else:
                initState.combine_States(minimize[1])

            cont += 1
            
    init = Node("Root")
    
    for i in treeN:
        if init.left == None:
            init.left = i
        else:
            init.right = i
            new_init = Node("Root")
            new_init.left = init
            init = new_init

    return initState


def translateToCode(initState: State, isOut: bool = False) -> str:
    code = ''
    setStates: Dict[str, State] = {initState.value: initState}

    def addState(state: State):
        for tran, states in state.transitions.items():
            for st in states:
                if st.value not in setStates:
                    setStates[st.value] = st
                    addState(st)

    addState(initState)

    for i, state in setStates.items():
        code = f"{i} = State('{i}')\n" + code
        if state.isFinalState:
            code += f"{i}.isFinalState = True\n"
        if len(state.token) > 0:
            code += f"""\n\ndef tk_{i}(): \n"""
            for j in state.token:
                code += f"\t{j}\n"

            code += f"\n\n{i}.token = tk_{i}\n"
        for tran, states in state.transitions.items():
            for st in states:
                code += f"{i}.add_transition({tran}, {st.value})\n"
        code += '\n'

    return code


def statesTotla(initState: State) -> str:
    code = ''
    setStates: Dict[str, State] = {initState.value: initState}

    def addState(state: State):
        for tran, states in state.transitions.items():
            for st in states:
                if st.value not in setStates:
                    setStates[st.value] = st
                    addState(st)

    addState(initState)

    for i, state in setStates.items():
        code = f"{i} = State('{i}')\n" + code
        if state.isFinalState:
            code += f"{i}.isFinalState = True\n"
        if len(state.token) > 0:
            code += f"{i}.addToken( '{state.getToken()}')\n"
        for tran, states in state.transitions.items():
            for st in states:
                code += f"{i}.add_transition({tran}, {st.value})\n"
        code += '\n'
    else:

        code = f"from typing import *\nfrom Classes_ import State\n\n" + code

    return code

def import_module(file, regex, showTree=False):
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            module = pickle.load(f)
        a0 = getattr(module, 'a0', None)
    else:
        a0 = prepareAFN(regex, showTree=showTree)
        code = translateToCode(a0)
        with open(file, 'wb') as fileW:
            pickle.dump(a0, fileW)

    return a0