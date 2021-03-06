import argparse
import os
from collections import Counter

from pacmanProblem import PacmanProblem
from report import report
from search import astar_search, random, hill_climbing, depth_first_tree_search, breadth_first_tree_search, \
    greedy_best_first_graph_search, greedy_best_first_search, breadth_first_graph_search, depth_first_graph_search


def default(str):
    return str + ' [Default: %default]'

usageStr = """
USAGE:      python pacman.py <options>
EXAMPLES:   (1) python pacman.py
                - starts an interactive game
            (2) python pacman.py --layout smallClassic --zoom 2
            OR  python pacman.py -l smallClassic -z 2
                - starts an interactive game on a smaller board, zoomed in
"""

parser = argparse.ArgumentParser(description=usageStr)
parser.add_argument('-l', '--layout', dest='layout',
                    help=default('the LAYOUT_FILE from which to load the map layout'),
                    metavar='LAYOUT_FILE', default='mediumClassic')


def main():
    args = parser.parse_args()

    bounds, ghosts, pacman, goal = mapPositions(args.layout)

    print('Barreiras:', bounds)
    print('Fantasmas:', ghosts)
    print('Pacman:', pacman)
    print('Gol:', goal)
    print()

    #Problema e algoritmos
    problem = PacmanProblem(obstacles=bounds | ghosts, initial=pacman, goal=goal)
    gfsProblem = greedy_best_first_search(problem)
    astarProblem = astar_search(problem)
    bfsProblem = breadth_first_graph_search(problem)
    dfsProblem = depth_first_graph_search(problem)
    print('Greedy Best First Search:')
    print('Caminho:', gfsProblem.path())
    print('Gol:', gfsProblem)
    print('A* Search:')
    print('Caminho:', astarProblem.path())
    print('Gol:', astarProblem)
    print('Breadth-First Search:')
    print('Caminho:', bfsProblem.path())
    print('Gol:', dfsProblem)
    print('Depth-First Search:')
    print('Caminho:', dfsProblem.path())
    print('Gol:', dfsProblem)
    print()
    print('Gerando saídas...')
    generateOutput(gfsProblem.path(), args.layout, 'gfs')
    generateOutput(astarProblem.path(), args.layout, 'astar')
    generateOutput(dfsProblem.path(), args.layout, 'bfs')
    generateOutput(dfsProblem.path(), args.layout, 'dfs')

    print()
    print('Desempenho:')
    report([greedy_best_first_search, astar_search, breadth_first_graph_search, depth_first_graph_search], [problem])

def mapPositions(layoutFile):
    with open('layouts/'+ layoutFile +'.lay', 'r') as layout:
        x = 1
        bounds = set()
        ghosts = set()
        pacman = (1,1)
        goal = (2,2)
        for line in layout.readlines():
            y = 1
            for ch in line:
                if (ch == '%'):
                    bounds |= {(x, y)}
                elif (ch == 'G'):
                    ghosts |= {(x, y)}
                elif (ch == 'P'):
                    pacman = (x, y)
                elif (ch == 'o'):
                    goal = (x, y)

                y += 1

            x += 1
        return bounds, ghosts, pacman, goal

def generateOutput(nodes, layoutFile, searchFile):
    if not os.path.exists('solutions'):
        os.makedirs('solutions')

    with open('layouts/'+ layoutFile +'.lay', 'r') as layout:
        lines = layout.readlines()
        numnodes = 1
        for node in nodes:
            x = 1
            if (numnodes == 1) or (numnodes == len(nodes)):
                numnodes += 1
                continue

            for line in lines:
                if (x == node.state[0]):
                    aux = list(line)
                    aux[node.state[1] - 1] = '*'
                    lines[node.state[0] - 1] = "".join(aux)
                x += 1
            numnodes += 1


        with open('solutions/' + layoutFile + '_' + searchFile + '.lay', 'w') as solution:
            solution.write("".join(lines))


if __name__ == '__main__':
    main()