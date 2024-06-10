from Graph import Graph
import numpy as np

def graph_example(N=7,row=5,col=3):

    L=np.random.randint(1,1e3,N)
    x = {}
    y = {}

    for i in range(N):
        x[i] = (np.arange(L[i])) 
        y[i] = (np.random.randn(L[i],1)) 

    joinVec= {0:[1],
            1:[2],
            2:[3,9],
            3:[4],
            4:[5],
            5:[12,15],
            6:[7,14]} 

    graph_type= {   5:'scatter',
                    6:'plot'}

    xlim = {        0:[0,3],
                    1:[0,3]
                    }

    xlabel = {      0:'xlim1',
                    1:'xlim2',
                    2:'xlim3',
                    3:'xlim4',
                    4:'xlim5'}


    ylim = {    }

    ylabel = {      0:'',
                    1:'ylim2',
                    2:'ylim3',
                    3:'ylim4',
                    4:'ylim5',
                    5:'ylim6',
                    6:'ylim7'}


    obj_in = {'x': x,'y': y, 'row':row, 'col':col, 
            'joinVec':joinVec,'typeGraf':graph_type,
            'ylabel':ylabel, 'xlim':xlim,'ylim':ylim,
            'xlabel':xlabel, 'show': True }

    graph = Graph(**obj_in)
    graph.create_figure()

