import time
import logging
import numpy as np
import sympy as sy
import pandas as pd
from py4j.java_gateway import JavaGateway

from .model_parsing import is_stored,generate_model,generate_function_string,generate_symbolic_function,read_function_string

class Objective(object):
    def __init__(self,n,prop,attack_transitions,attack_idxs):
        self.n,self.prop = n,prop
        self.attack_idxs,self.attack_transitions = attack_idxs, attack_transitions
        self.instantiated = False

    def reset_F(self):
        """Resets F to before it was instantiated with P"""
        raise NotImplementedError

    def instantiate_F(self,P):
        """Instantiate the function F with P values in whatever format is appropriate
        
        For ClosedForm, this is a symbolic expression
        For ModelChecker, this is just setting P matrix
        """
        if self.instantiated:
            raise ValueError('F was previously instantiated, must call reset_F before instantiating again.')
        self.instantiated = True
        self.P = P

    def evaluate_F(self, X):
        """Objective is probability that P+X satisfies some given property.
        
        Input can be a matrix or 'unrolled' vector representing the perturbation matrix.
        [[x0,x1],[x2,x3]] <-> [x0,x1,x2,x3] 

        Output is the objected evaluated at X.
        """
        raise NotImplementedError

    def get_PplusX(self, x):
        if not self.instantiated:
            raise ValueError('Cannot get P + X for non-instantiated objective')
        X = self.fill(x).reshape(self.n,self.n)
        return self.P + X
    
    def fill(self,X):
        X = X.tolist()
        return np.array([0 if i not in self.attack_idxs else X.pop(0) for i in range(self.n**2)])

class ModelChecker(Objective):
    """A class for objective functions defined in PRISM."""
    def __init__(self,n,prop,attack_transitions,attack_idxs):
        super().__init__(n,prop,attack_transitions,attack_idxs)
        self.__set_prism_gateway()

    def instantiate_F(self,P):
        super().instantiate_F(P)
        return 0

    def evaluate_F(self, X):
        # logging.info(f'Evaluating F with X = {X}')
        X = self.fill(X)
        PplusX = self.gateway.jvm.java.util.ArrayList()
        for i,v in enumerate(self.P.flatten()):
            PplusX.add(v + X[i])
        F_evaluated = self.prism_gateway.runPrism(self.prop, PplusX, self.n, 0)
        # logging.info(f'Successfully evaluated F: {F_evaluated}')
        return F_evaluated

    def __set_prism_gateway(self):
        self.gateway = JavaGateway()
        self.prism_gateway = self.gateway.entry_point

class SymbolicFunction(Objective):
    """A class for objective functions which are closed form rational functions generated from a pDTMC model checker. 
    Note that this objective should only be used when the input is not a pDTMC file.
    """
    def __init__(self,n,prop,results_base,prism_bin,modelchecker,param_bin,attack_transitions,attack_idxs):
        super().__init__(n,prop,attack_transitions,attack_idxs)
        self.results_base = results_base
        self.modelchecker = modelchecker
        self.param_bin = param_bin
        self.prism_bin = prism_bin

    def instantiate_F(self,P):
        super().instantiate_F(P)
        self.P_symb = self.__generate_P_symb(P)
        function_file = f"{self.results_base}/symb_F.txt"
        func_str = ""
        stored = is_stored(function_file)
        if not stored:
            logging.info(f"{function_file} does not exist. Generating symbolic function.")
            self.pm = generate_model(self.P_symb,self.n,self.modelchecker)
            duration, func_str = generate_function_string(self.pm,self.prop,function_file,self.P_symb,self.prism_bin,self.param_bin,self.modelchecker)
        else:
            logging.info(f"{function_file} exists. Reading symbolic function and duration from file.")
            duration, func_str = read_function_string(function_file) 

        logging.info("Attempting to parse function string.")
        self.F_symb = generate_symbolic_function(func_str,function_file)

        logging.info(f"Successfully parsed function string. Function is: {str(self.F_symb)}")

        self.instantiated = True
        return duration

    def evaluate_F(self,X):
        # logging.info(f'Evaluating F with X = {X}')
        param_list = np.array([s.name for s in self.P_symb if isinstance(s,sy.Symbol)])
        filled_X = self.fill(X)
        flat_P = self.P.flatten()
        instantiation = np.array([filled_X[i] + flat_P[i] for i in range(self.n**2) if isinstance(self.P_symb[i], sy.Symbol)])
        F_evaluated = self.F_symb.subs(zip(param_list,instantiation))
        # logging.info(f'Successfully evaluated F: {F_evaluated}')
        return F_evaluated

    def __generate_P_symb(self,P):
        P_symb = sy.Matrix(np.array([[sy.Symbol(f'Pr{i}to{j}E') if [i,j] in self.attack_transitions else P[i,j] for j in range(self.n)] for i in range(self.n)]))
        return P_symb