# -*- coding: utf-8 -*-
from pygraph.classes.digraph import digraph
import random


class PRIterator:
    def __init__(self, graph):
        self.alpha = 0.7  # α in the formula
        self.max_iterations = 1000000  # using a max_iteration to terminal the iteration since I have no idea how to implement the converged part currently
        self.graph = graph

    def page_rank(self):
        # for all selfish nodes, make the edges connected to each other node.
        for node_a in self.graph.nodes():
            if len(self.graph.neighbors(node_a)) == 0:
                for node_b in self.graph.nodes():
                    digraph.add_edge(self.graph, (node_a, node_b))

        nodes_list = self.graph.nodes()
        PR_graph_size = len(nodes_list)

        if PR_graph_size == 0:
            return {}
        page_rank = dict.fromkeys(nodes_list, 1.0 / PR_graph_size)  # initial value of each page, 1/N, where N is the number of pages in the graph
        damping_value = (1.0 - self.alpha) / PR_graph_size  # (1−α)/N in the formula

        converged = 0.000000000000000001
        for i in range(self.max_iterations):
            change = 0
            for node in nodes_list:
                rank = 0
                for incident_page in self.graph.incidents(node):  # get all inbounds-links
                    rank += self.alpha * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                rank += damping_value
                change += abs(page_rank[node] - rank)
                page_rank[node] = rank

            print(i+1)
            print(page_rank)
            if change < converged:
                break


        print("Done!")
        return page_rank

if __name__ == '__main__':
    PR_graph = digraph()

    '''PR_graph.add_nodes(["A", "B", "C", "D", "E", "F"])'''
    node_num = random.randint(1,1000)
    node_order = 0
    for i in range(node_num):
        PR_graph.add_nodes([str(node_order)])
        node_order += 1
    
    for j in range(random.randint(1, node_num)):
        out_node = str(random.randint(0, node_num-1))
        in_node = str(random.randint(0,node_num-1))
        PR_graph.add_edge((out_node, in_node))

    '''
    PR_graph.add_edge(("A", "B"))   
    PR_graph.add_edge(("A", "D"))
    PR_graph.add_edge(("B", "D"))
    PR_graph.add_edge(("C", "E"))
    PR_graph.add_edge(("C", "F"))
    PR_graph.add_edge(("A", "C"))
    PR_graph.add_edge(("D", "E"))
    PR_graph.add_edge(("D", "F"))
    PR_graph.add_edge(("B", "E"))
    PR_graph.add_edge(("E", "A"))
    PR_graph.add_edge(("F", "A"))
    PR_graph.add_edge(("F", "B"))
    '''

    pr = PRIterator(PR_graph)
    page_ranks = pr.page_rank()
    max_node = '0'
    for node in range(node_num):
        if page_ranks[str(node)] > page_ranks[max_node]:
            max_node = str(node)

    print("The page rank value is\n", page_ranks)
    print("The most important page with highest page rank value is %s", max_node)