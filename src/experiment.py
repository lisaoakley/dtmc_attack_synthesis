from .model_parsing import matfile2mat
from .constraints import OptConstraints
from .objective import ModelChecker,SymbolicFunction

import pandas as pd
import numpy as np
from scipy import optimize
import time
import os
import logging

class Experiment(object):
    def __init__(self, matrix_file, prop, tm, tm_args, epsilon, results_base, method, prism_bin, param_bin, pdtmc_modelchecker):
        self.P = matfile2mat(matrix_file)
        self.n = len(self.P)
        self.__set_common_params(prop, tm, tm_args, epsilon, results_base, method, prism_bin, param_bin, pdtmc_modelchecker)
        
    # For model file, create new constructor that takes in model file and convert model to matrix

    def __set_common_params(self, prop, tm, tm_args, epsilon, results_base, method, prism_bin, param_bin, pdtmc_modelchecker):
        self.prop = prop
        self.method = method
        self.tm = tm
        self.tm_args = tm_args
        self.results_base = results_base
        self.prism_bin = prism_bin
        self.param_bin = param_bin
        self.modelchecker = pdtmc_modelchecker
        self.epsilon = epsilon
        self.attack_transitions, self.attack_states, self.attack_idxs = self.__get_attack_vals(self.tm,self.tm_args,self.n,self.P)
        self.constr = OptConstraints(n=self.n,attack_states=self.attack_states,attack_idxs=self.attack_idxs)

    def run(self):
        # Initialize objective function (connection to PRISM or parametric solution)
        logging.info('Initializing Objective Function')
        if self.method == "concrete":
            objective = ModelChecker(n=self.n,prop=self.prop,attack_transitions=self.attack_transitions,attack_idxs=self.attack_idxs)
        elif self.method == "symbolic":
            objective = SymbolicFunction(n=self.n,prop=self.prop,results_base=self.results_base,prism_bin=self.prism_bin,modelchecker=self.modelchecker,param_bin=self.param_bin,attack_transitions=self.attack_transitions,attack_idxs=self.attack_idxs)
        else:
            raise NotImplementedError

        logging.info('Instantiating Objective with Original Model')
        preprocess_duration = objective.instantiate_F(self.P.to_numpy())
        
        # Instantiate constraints
        logging.info('Generating optimization constraints')
        bnds, lin_constr = self.constr.get_scipy_constraints(self.P,self.epsilon)
        # Set initial X
        X_init = np.zeros(len(self.attack_transitions))

        # Compute probability property is satisfied on the original model
        unperturbed_prob = objective.evaluate_F(np.array(X_init))
        logging.info(f"Unperturbed F = {unperturbed_prob}")

        # Run optimization
        logging.info('Starting optimization')
        opt_start = time.time()
        sol = optimize.minimize(objective.evaluate_F,X_init,bounds=bnds,constraints=lin_constr)
        opt_duration = time.time() - opt_start
        logging.info(f"optimization output: {sol.message}")
        if not sol.success:
            raise ValueError('Optimization unsuccessful')
        logging.info(f"Successfully minimized F in {opt_duration} seconds. F = {sol.fun}")


        # Store results
        pd.DataFrame(objective.get_PplusX(sol.x)).to_csv("{}/PplusX.csv".format(self.results_base),index=False,header=False)
        pd.DataFrame([str(preprocess_duration)+str(opt_duration),preprocess_duration,opt_duration,sol.nfev,sol.nit,unperturbed_prob,sol.fun,unperturbed_prob-sol.fun,sol.success,len(X_init),self.prop,self.modelchecker,self.n],index=["run_duration","preprocessing_duration","optimization_duration","num_F_evals","num_opt_iterations","unperturbed_probability","minimized_probability","max_delta","status","num_params","property","pdtmc_modelchecker","num_states"]).to_csv("{}/res.csv".format(self.results_base))

        logging.info(f"Experiment complete. results can be found in {self.results_base}")

    def __get_attack_vals(self,tm,tm_args,n,P):
        if tm == 'SS':
            attack_transitions = [[int(out_state),in_state] for in_state in range(n) for out_state in tm_args]
        elif tm == 'SPSS':
            attack_transitions = [[int(out_state),in_state] for in_state in range(n) for out_state in tm_args if P.iloc[int(out_state),in_state] > 0]
        elif tm == 'ST':
            attack_transitions = [[int(a[0]),int(a[1])] for a in tm_args]
        elif tm == 'SPST':
            attack_transitions = [[int(a[0]),int(a[1])] for a in tm_args if P.iloc[int(a[0]),int(a[1])] > 0]
        else:
            raise NotImplementedError
        
        out_states = np.unique(np.array([transition[0] for transition in attack_transitions]))
        attack_idxs = np.unique((np.array([i*n+j for [i,j] in attack_transitions])))
        logging.info(f"\nattackable states: {out_states}\n attackable transitions: {attack_transitions}\n unrolled attackable transition idxs: {attack_idxs}")
        return attack_transitions, out_states, attack_idxs