import numpy as np

def pagerank(G, d=0.15):
    """ Ranks the nodes in G """
    n = len(G)
    A = adj_matrix(G) * (1 - d)
    E = np.ones((n, n)) / n * d
    w, v = np.linalg.eig(A.T + E)
    pi = v[:, w.argmax()]
    return pi / sum(pi)

def adj_matrix(G):
    """ Returns the probability adjacency matrix of G """ 
    n = len(G)
    P = np.zeros((n, n))
    for i in range(len(G)):
        for neighbor in G[i]:
            P[i][neighbor] = 1 / len(G[i])
    return P

if __name__ == '__main__':
    A = [1, 3]
    B = [2]
    C = [0]
    D = [0, 1, 4]
    E = [1, 2]

    G = [A, B, C, D, E]
    print(pagerank(G))
