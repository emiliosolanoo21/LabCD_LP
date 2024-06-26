from Classes_ import *
import graphviz


def draw_tree(f_node: Node, expression='default', direct=False):
    dot = graphviz.Digraph(comment='Tree')

    def draw_node(node: Node):
        dot.node(node.getId(), label=node.value)
        if node.left is not None:
            dot.edge(node.getId(), node.left.getId())
            draw_node(node.left)
        if node.right is not None:
            dot.edge(node.getId(), node.right.getId())
            draw_node(node.right)

    draw_node(f_node)

    dot.render('Tree.gv', view=True, directory='./Tree/'+expression+'/'+('Direct' if direct else 'Infix'))


def draw_AF(initState: State, legend: str = 'AF', expression='default', direct=False, name='AFN', useNum=False):
    dot: 'graphviz.graphs.Digraph' = graphviz.Digraph(comment='AFN')
    dot.attr(rankdir='LR')
    setStates = set()

    dot.attr(label=legend)

    def draw_state(state: 'State'):
        nonlocal useNum
        setStates.add(state.getId())
        dot.node(state.getId(), label=state.value, shape='doublecircle' if state.isFinalState else 'circle')
        for transition in state.transitions:
            for destiny in state.transitions[transition]:
                if destiny.getId() not in setStates:
                    draw_state(destiny)
                label = str(transition) if isinstance(transition, str) or useNum else chr(transition)
                dot.edge(state.getId(), destiny.getId(), label=label)

    draw_state(initState)

    dot.render(name + '.gv', view=True, directory='./machine/' + expression)
