from Classes_ import State, Node
from typing import *


def makeAFD_from_AFN(initState: State, alpha: str):
    actualSt: Set[State] = initState.getEpsilonClean()
    stDict: Dict[str, Set[State]] = {'q0': actualSt}
    states: Dict[str, State] = {'q0': State('q0')}
    evaluate = 0
    alphabet = set(list(alpha))
    toEvaluate: List[str] = ['q0']
    while len(toEvaluate) > 0:
        actualSt = stDict[toEvaluate[0]]
        actualState: State = states[toEvaluate[0]]
        if len(toEvaluate) > 1:
            toEvaluate = toEvaluate[1:]
        else:
            toEvaluate.clear()

        preEpsilonStates: Dict[str, Set[State]] = dict()
        epsilonStates: Dict[str, Set[State]] = dict()
        for state in actualSt:
            for letter in alphabet:
                if letter in state.transitions:
                    if letter in preEpsilonStates:
                        preEpsilonStates[letter] = preEpsilonStates[letter].union(state.getStates(letter))
                    else:
                        preEpsilonStates[letter] = state.getStates(letter)

        for letter in preEpsilonStates:
            epsilonStates[letter] = set()
            for state in preEpsilonStates[letter]:
                epsilonStates[letter] = epsilonStates[letter].union(state.getEpsilonClean())

        for letter in epsilonStates:
            if epsilonStates[letter] not in stDict.values():
                evaluate += 1
                index = 'q' + str(evaluate)
                states[index] = State(index)
                stDict[index] = epsilonStates[letter]
                toEvaluate.append(index)
                actualState.add_transition(letter, states[index])
            else:
                for i in stDict:
                    if epsilonStates[letter] == stDict[i]:
                        index = i
                        actualState.add_transition(letter, states[index])

    for index in stDict:
        for statesSt in stDict[index]:
            if statesSt.isFinalState:
                states[index].isFinalState = True

    return states


def make_direct_AFD(tree: Node, nodes: Dict[str, Node], alpha: str):
    states: Dict[Tuple[str, ...], State] = {tuple(tree.first_pos): State('q0')}
    toEvaluate: List[Tuple[str, ...]] = [tuple(tree.first_pos)]
    total_states: Dict[str, State] = dict()
    total_states['q0'] = states[tuple(tree.first_pos)]
    finalState: str = ''
    for state in nodes:
        if nodes[state].value == '#':
            finalState = state
            break
    gen = 1

    while len(toEvaluate) > 0:
        actualState: Tuple[str, ...] = toEvaluate[0]
        if len(toEvaluate) > 1:
            toEvaluate = toEvaluate[1:]
        else:
            toEvaluate.clear()

        for letter in alpha:
            nextState_st: Set[str] = set()
            for state in actualState:
                if nodes[state].value == letter:
                    nextState_st = nextState_st.union(nodes[state].follow_pos)
            if len(nextState_st) <= 0:
                continue
            nextState: Tuple[str, ...] = tuple(nextState_st)
            if nextState not in states:
                states[nextState] = State('q' + str(gen))
                total_states['q' + str(gen)] = states[nextState]
                if finalState in nextState_st:
                    states[nextState].isFinalState = True
                toEvaluate.append(nextState)
                gen += 1
            states[actualState].add_transition(letter, states[nextState])

    for state in states:
        if finalState in state:
            states[state].isFinalState = True

    return states, states[tuple(tree.first_pos)], total_states
