import numpy as np
import sympy as sy
import scipy as sp
import cvxopt as cvx
from scipy import optimize
import logging

class OptConstraints(object):
    """Stores and converts constraints on x for different optimization types.
    
    Stores the values G,h,A,b of constraints on x such that
    Gx >= h and Ax = b
    and converts to constraints formatted for each optimization type.
    """

    def __init__(self,n,attack_states,attack_idxs):
        self.n=n
        self.attack_states = attack_states
        self.attack_idxs = attack_idxs
        self.P_symb = sy.Matrix([[sy.Symbol('p{}'.format(i*n+j)) for j in range(n)] for i in range(n)])

    def get_scipy_constraints(self,P,epsilon):
        """Return bounds as scipy constraint/bound objects.

        Bounds: lb <= x <= ub
        Constraints: lb <= A.dot(x) <= ub
        """
        logging.info('Setting up subs_vals')
        p = P.values.flatten()

        logging.info(f'set bounds')
        bnds_lb =  np.array([max(-epsilon,-p[i]) for i in self.attack_idxs])
        bnds_ub = np.array([min(epsilon,1-p[i]) for i in self.attack_idxs])
        # bnds_lb <= x <= bnds_ub
        bnds = sp.optimize.Bounds(bnds_lb,bnds_ub)
        logging.info(f'bounds generation complete.')

        logging.info('setting linear constraints')
        # lb <= A.dot(x) <= ub ... set lb=ub=b for equality constraint
        A_pruned = self.__prune_A(self.__compute_A(self.n))
        b = np.zeros(len(A_pruned))
        lin_constr = sp.optimize.LinearConstraint(A=A_pruned,lb=b,ub=b)
        logging.info('constraints generation complete.')

        return bnds, lin_constr

    def __compute_A(self,n):
        """Compute A s.t. Ax=b"""
        return np.array(cvx.matrix(cvx.spmatrix(1,sorted([i % n for i in range(n**2)]),range(n**2))))

    def __prune_A(self, A):
        # remove columns which correspond to transitions that cannot be attacked
        rm_cols = np.delete([i for i in range(self.n*self.n)], self.attack_idxs)
        A = np.delete(A, rm_cols, axis=1)

        # remove rows that correspond to states that cannot be attacked
        rm_rows = np.delete([i for i in range(self.n)], self.attack_states)
        A = np.delete(A, rm_rows, axis=0)
        return A
            


