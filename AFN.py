from Classes_ import State, Node


def make_AFN(tree: Node, initState: State = State(str(0))):
    noInit = int(initState.value)

    if tree.value == '|':
        left, noInit, leftFinal_state = make_AFN(tree.left, State(str(noInit+1)))
        right, noInit, rightFinal_state = make_AFN(tree.right, State(str(noInit+1)))
        initState.add_transition('ε', left)
        initState.add_transition('ε', right)
        finalState = State(str(noInit + 1))
        leftFinal_state.add_transition('ε', finalState)
        rightFinal_state.add_transition('ε', finalState)

    elif tree.value == '.':
        left, noInit, leftFinal_state = make_AFN(tree.left, initState)
        right, noInit, rightFinal_state = make_AFN(tree.right, leftFinal_state)
        finalState = rightFinal_state

    elif tree.value == '*':
        left, noInit, leftFinal_state = make_AFN(tree.left, State(str(noInit+1)))
        initState.add_transition('ε', left)
        finalState = State(str(noInit+1))
        leftFinal_state.add_transition('ε', finalState)
        initState.add_transition('ε', finalState)
        leftFinal_state.add_transition('ε', left)

    else:
        finalState = State(str(noInit + 1))
        initState.add_transition(tree.value, finalState)

    return initState, int(finalState.value), finalState
