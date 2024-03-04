from reader import *
from infix_converter import *
from Tree_ import *
from Draw_diagrams import *
from AFN import *
from AFD import *
from Minimized import *
from typing import *
from Simulator import Simulator
from Colors import *

def display_expression_options(contents: Dict[str, str]):
    print(f"\n{BOLD}{REVERSE}{GREEN}BIENVENIDOS AL PROYECTO 1 DE LENGUAJES DE PROGRAMACIÓN{RESET}")
    print(f"\n{BOLD}{YELLOW}Expresiones disponibles:{RESET}")
    for i, expression in contents.items():
        print(f"{i}. {expression}")

if __name__ == '__main__':
    '''Read the file and return its contents'''
    contents: List[str] = reader('datos.txt')
    accepted: List[str] = validate(contents=contents)
    alphabets: List[str] = extract_alphabet(accepted)
    formatted: List[str] = format_regex(accepted)
    postfix: List[str] = translate_to_postfix(formatted)
    
    options: Dict[str, str] = { str(i+1): accepted[i] for i in range(len(accepted))}
    
    inside = True
    
    while inside:
        display_expression_options(options)
        expression_number = input("Ingrese el número de opción de la expresión que desea evaluar: ").replace(" ", "")
        if expression_number in options:
            selected_expression = contents[int(expression_number) - 1]

            tree = make_tree(postfix[int(expression_number) - 1])
            direct_tree, nodes = make_direct_tree(postfix[int(expression_number) - 1])

            direct_states, direct_initS, total_d = make_direct_AFD(direct_tree, nodes, alphabets[int(expression_number) - 1])
            afnInit, _, finalS = make_AFN(tree)
            finalS.isFinalState = True
            afdN_Init = makeAFD_from_AFN(afnInit, alphabets[int(expression_number) - 1])

            afd_min_afN, initMAFD = minimizeAFD(afdN_Init, alphabets[int(expression_number) - 1])
            afd_min_direct, initM_direct = minimizeAFD(total_d, alphabets[int(expression_number) - 1])

            afDict = {
                'FNA': afnInit,
                'FDA': afdN_Init['q0'],
                'Minimized FDA': initMAFD,
                'Direct FDA': direct_initS,
                'Minimized & Direct FDA': initM_direct
            }
            
            inside2 = True
            
            while inside2:
                print(f"\n{BOLD}{YELLOW}Selected Expression: {selected_expression}{RESET}")
                #Opciones para la expresión
                print("Opciones:")
                print("1. Ejecutar diagramas correspondientes de la expresión")
                print("2. Ejecutar el evaluador regex para la expresión")
                print("3. Ejecutar árbol de la expresión")
                print("4. Regresar a seleccionar expresión")

                option = input("Ingrese el número de la opción que desea ejecutar (o 'exit' para salir): ").replace(" ", "")

                if option == 'exit':
                    inside = False
                    inside2 =  False
                elif option == '1':
                    draw_AF(afnInit, legend='FNA', expression='default', direct=False)
                    draw_AF(afdN_Init['q0'], legend='FDA', expression='default', direct=False, name='AFD')
                    draw_AF(initMAFD, legend='Minimized FDA', expression='default', direct=False, name='AFD_min')
                    draw_AF(direct_initS, legend='Direct FDA', expression='default', direct=True, name='AFD_direct')
                    draw_AF(initM_direct, legend='Minimized & Direct FDA', expression='default', direct=True, name='AFD_min_direct')
                    print(f"{BOLD}{GREEN}Diagrams Succeed!{RESET}")
                elif option == '2':
                    while True:
                        print(YELLOW + "Bienvenido al evaluador de regex para", selected_expression, RESET)
                        string = input(CYAN + "Ingrese la cadena a evaluar: " + RESET).strip().replace("ε", "")
                        print(WHITE, "Ingrese 'exit' para salir del programa", RESET)

                        if string.lower() == 'exit':
                            break

                        simulationResult, _paths = Simulator(afDict, string)
                elif option == '3':
                    draw_tree(tree)
                    print(f"{BOLD}{GREEN}Tree Succeed!{RESET}")
                elif option == '4':
                    inside2 = False
                else:
                    print("Opción no válida. Por favor, ingrese una opción válida.")
        else:
            print("Seleccione una opción válida.")