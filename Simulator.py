from Classes_ import State
from typing import *
from Colors import *
import time


def Simulator(states: Dict[str, State], string: str, expression=""):
    print(f"{BOLD}{YELLOW}Simulating the string [{string}] in the automaton{RESET}")
    print(f"{BOLD}{YELLOW}Automaton: {expression}{RESET}")

    pathDict: Dict[str, List[State]] = dict()

    def simulation(initState: State ):
        paths: List[List[State]] = [[initState]]

        for char in string:
            newPaths: List[List[State]] = []

            for path in paths:
                evalState: State = path[-1]

                for st in evalState.getStates(char):
                    newPath = path.copy()
                    newPath.append(st)
                    newPaths.append(newPath)

                for st_e in evalState.getEpsilonClean() - {evalState}:
                    for st in st_e.getStates(char):
                        newPath = path.copy()
                        newPath.append(st)
                        newPaths.append(newPath)

            paths = newPaths

        for path in paths:
            evalState: State = path[-1]

            if evalState.isFinalState:
                return True, path

            for st_e in evalState.getEpsilonClean():
                if st_e.isFinalState:
                    finalPath = path.copy()
                    finalPath.append(st_e)
                    return True, finalPath

        return False, []

    simulationResult = True

    start = time.time()
    for key in states:
        result, simulationPaths = simulation(states[key])
        simulationResult = simulationResult and result
        pathDict[key] = simulationPaths
        print(f"{BOLD}Simulation for {key}: {GREEN+'Excellent!' if result else RED+'Bad result'}{RESET}")
        if not result:
            break
    end = time.time()

    if simulationResult:
        print(f"{BOLD}{GREEN}The string was accepted{RESET}")
    else:
        print(f"{BOLD}{RED}The string was not accepted{RESET}")

    print(f"{BOLD}{YELLOW}Time elapsed: {end - start} seconds{RESET}")

    return simulationResult, pathDict
