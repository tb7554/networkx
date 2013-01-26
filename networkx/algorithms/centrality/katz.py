"""
Katz centrality.
"""
#    Copyright (C) 2004-2013 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
import networkx as nx
from networkx.utils import *
__author__ = "\n".join(['Aric Hagberg (hagberg@lanl.gov)',
                        'Pieter Swart (swart@lanl.gov)',
                        'Sasha Gutfraind (ag362@cornell.edu)',
                        'Vincent Gauthier (vgauthier@luxbulb.org)'])

__all__ = ['katz_centrality',
           'katz_centrality_numpy']

@not_implemented_for('multigraph')
def katz_centrality(G, alpha=0.1, beta=1.0,
                    max_iter=1000, tol=1.0e-6, nstart=None, normalized=True):
    r"""Compute the Katz centrality for the nodes of the graph G.

    This algorithm it uses the power method to find the eigenvector
    corresponding to the largest eigenvalue of the adjacency matrix of G.
    The constant alpha should be strictly less than the inverse of largest
    eigenvalue of the adjacency matrix for the algorithm to converge.

    Parameters
    ----------
    G : graph
      A networkx graph

    alpha : float
      Attenuation factor

    beta : scalar or dictionary, optional (default=1.0)
      Weight attributed to the immediate neighborhood. If not a scalar the
      dictionary must have an value for every node.

    max_iter : interger, optional (default=1000)
      Maximum number of iterations in power method.

    tol : float, optional (default=1.0e-6)
      Error tolerance used to check convergence in power method iteration.

    nstart : dictionary, optional
      Starting value of Katz iteration for each node.

    normalized : bool, optional (default=True)
      If True normalize the resulting values.

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with Katz centrality as the value.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> centrality=nx.katz_centrality(G)

    print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
    ['0 0.37', '1 0.60', '2 0.60', '3 0.37']

    Notes
    -----
    The Katz calculation is done by the power iteration method
    and has no guarantee of convergence.  The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    Notes
    ------
    Katz centrality overcome some limitations of the eigenvalue centrality and
    it is defined as follows:

    .. math::

        x_i = \alpha \sum_{i} A_{ij} x_j + \beta

    with

    .. math::

        \alpha < \frac{1}{\lambda_{max}}

    Katz centrality computes the relative influence of a node within a
    network by measuring the number of the immediate neighbors (first
    degree nodes) and also all other nodes in the network that connect
    to the node under consideration through these immediate neighbors,
    extra weight could be provided to immediate neighbor through the
    parameter :math:`\beta`.  Connections made with distant neighbors
    are, however, penalized by an attenuation factor `\alpha` which
    should be strictly less than the inverse largest eigenvalue of the
    adjacency matrix in order for the Katz centrality to be computed
    correctly. More information is  provided in [1]_ .


    References
    ----------
    .. [1] M. Newman, Networks: An Introduction. Oxford University Press,
       USA, 2010, p. 720.

    See Also
    --------
    katz_centrality_numpy
    eigenvector_centrality
    eigenvector_centrality_numpy
    pagerank
    hits
    """
    from math import sqrt

    if len(G)==0:
        return {}

    nnodes=G.number_of_nodes()

    if nstart is None:
        # choose starting vector with entries of 0
        x=dict([(n,0) for n in G])
    else:
        x=nstart

    # Cast beta from list to dict
    if type(beta) is list:
        beta = dict((nodeid,beta[nodeid]) for nodeid in G.nodes())

    # Cast beta from scalar to dict
    if type(beta) is not dict:
        beta = dict.fromkeys(G,beta)

    # make up to max_iter iterations
    for i in range(max_iter):
        xlast=x
        x=dict.fromkeys(xlast, 0)
        # do the multiplication y = Alpha * Ax - Beta
        for n in x:
            for nbr in G[n]:
                x[n] += xlast[nbr] * G[n][nbr].get('weight',1)
            x[n] = alpha*x[n] + beta[n]

        # check convergence
        err=sum([abs(x[n]-xlast[n]) for n in x])
        if err < nnodes*tol:
            if normalized:
                # normalize vector
                try:
                    s=1.0/sqrt(sum(v**2 for v in x.values()))
                # this should never be zero?
                except ZeroDivisionError:
                    s=1.0
            else:
                s = 1
            for n in x:
                x[n]*=s
            return x

    raise nx.NetworkXError('Power iteration failed to converge in ',
                           '%d iterations."%(i+1))')

@not_implemented_for('multigraph')
def katz_centrality_numpy(G, alpha=0.1, beta=1.0, normalized=True):
    r"""Compute the Katz centrality for the graph G.

    The constant alpha should be strictly inferior to the inverse of largest
    eigenvalue of the adjacency matrix for the algorithm to converge.

    Parameters
    ----------
    G : graph
      A networkx graph

    alpha : float
      Attenuation factor

    beta : scalar or array, optional (default=1.0)
        Weight attributed to the immediate neighborhood. If not a scalar the
        array must have len(G) entries.

    normalized : bool
      If True normalize the resulting values.

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with Katz centrality as the value.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> centrality=nx.katz_centrality_numpy(G)

    print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
    ['0 0.37', '1 0.60', '2 0.60', '3 0.37']

    Notes
    ------
    Katz centrality overcome some limitations of the eigenvalue centrality and
    it is defined as follows:

    .. math::

        x_i = \alpha \sum_{i} A_{ij} x_j + \beta,

    with

    .. math::

        \alpha < \frac{1}{\lambda_{max}}.

    Katz centrality computes the relative influence of a node within a network
    by measuring the number of the immediate neighbors (first degree nodes) and
    also all other nodes in the network that connect to the node under
    consideration through these immediate neighbors, extra weight could be
    provided to immediate neighbor through the parameter :math:`\beta`.
    Connections made with distant neighbors are, however, penalized by an
    attenuation factor `\alpha` which should be strictly less than
    the inverse largest eigenvalue of the adjacency matrix in order for the Katz
    centrality to be computed correctly. More information is provided in [1]_ .

    References
    ----------
    .. [1] M. Newman, Networks: An Introduction. Oxford University Press,
       USA, 2010, p. 720.

    See Also
    --------
    katz_centrality
    eigenvector_centrality_numpy
    eigenvector_centrality
    pagerank
    hits
    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError('Requires NumPy: http://scipy.org/')

    if len(G)==0:
        return {}

    A=nx.adj_matrix(G,nodelist=G.nodes())
    n = np.array(A).shape[0]
    beta = np.ones((n,1))*beta
    centrality = np.linalg.solve( np.eye(n,n) - (alpha * A) , beta)
    if normalized:
        norm = np.sign(sum(centrality)) * np.linalg.norm(centrality)
    else:
        norm = 1.0
    centrality=dict(zip(G,map(float,centrality/norm)))
    return centrality


# fixture for nose tests
def setup_module(module):
    from nose import SkipTest
    try:
        import numpy
        import numpy.linalg
    except:
        raise SkipTest("numpy not available")
