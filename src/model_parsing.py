import os
import subprocess
import time
import tempfile
import logging
import ast
import operator
import pandas as pd
import simpleeval as se
import sympy as sy

def matfile2mat(matrix_file):
    return pd.read_csv(matrix_file,header=None)

def is_stored(function_file):
    return os.path.isfile(function_file)

def generate_model(P_symb,n,modelchecker):
    logging.info('Generating pm file')
    header = 'dtmc\n\n'

    logging.info('Generating params')
    if modelchecker == "prism":
        params = ''.join([';\n'.join([f"const double {p}" for p in P_symb if isinstance(p,sy.Symbol)]),";\n"])
    elif modelchecker == "param":
        params = ''.join([';\n'.join([f"param {p}: [0.0..1.0]" for p in P_symb if isinstance(p,sy.Symbol)]),";\n"])
    else: raise NotImplementedError

    begin_module = f"""
module casestudy
s:[0..{n-1}] init 0;
"""
    logging.info('Generating body')
    body_list = ['' for _ in range(n)]
    for i in range(n):
        body_list[i] = ''.join([f"    [] s={i} -> ",
                            ' + '.join([f"{P_symb[i,j]}:(s'={j})" for j in range(n) if P_symb[i,j] != 0])])
    body = ';\n'.join(body_list)

    endmodule = "\nendmodule"

    pDTMC_model = f"{header}{params}{begin_module}{body};{endmodule}"

    logging.info('Model complete.')
    logging.info(pDTMC_model)

    return pDTMC_model

def generate_function_string(mc,prop,function_file,P_symb,prism_bin,param_bin,modelchecker):
    duration = 0
    func_str = 0
    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        with tempfile.NamedTemporaryFile(mode='w+') as tmp_pctl:
            tmp.write(mc)
            tmp.read()
            tmp_pctl.write(prop)
            tmp_pctl.read()
            tmp_res = os.path.join(tempfile.mkdtemp(), 'res') # param appends .out to the input file, so we just make a name
            try:
                if modelchecker == "prism":
                    logging.info('generating prism function list')
                    param_list = ','.join([f"{p}=0.0:1.0" for p in P_symb if isinstance(p,sy.Symbol)])
                    logging.info("Starting parametric model checker")
                    start = time.time()
                    func_out = subprocess.check_output([prism_bin, tmp.name, '-pctl', prop, '-param', param_list, '-noprobchecks']).decode("utf-8")
                elif modelchecker == "param":
                    logging.info("Starting parametric model checker")
                    start = time.time()
                    func_out = subprocess.check_output([param_bin, tmp.name, tmp_pctl.name, '--result-file', tmp_res])
                else: raise NotImplementedError
            except subprocess.CalledProcessError as err:
                logging.info(f"{modelchecker} failed after {time.time() - start}.")
                raise RuntimeError(err)
            duration = time.time() - start
            logging.info(f"Model checker completed in time {duration}")
            
            logging.info(f"{modelchecker} output:\n {func_out}")
            if modelchecker == "prism":
                func_str = func_out.split('{')[1].split('}')[0].strip()
            elif modelchecker == "param":
                with open(f"{tmp_res}.out","r") as f:
                    lines = f.readlines()
                    func_str = lines[3]
            else: raise NotImplementedError
            logging.info(f"Successfully computed symbolic function representation. Computation duration: {duration}")
    

    with open(function_file, 'w') as f:
        logging.info(f"Saving function and duration to file {function_file}")
        f.write(f"{str(duration)}\n{func_str}\n")
    
    return duration, func_str

def read_function_string(function_file):
    logging.info('Reading function string')
    duration, func_str = None, None
    with open(function_file, 'r') as f:
        duration = f.readline().strip()
        func_str = f.readline().strip()
    logging.info(f"Function string retrieved. Function: {func_str}, Duration: {duration}")
    return duration, func_str

def generate_symbolic_function(func_str,function_file):
    try:
        s = se.SimpleEval()
        s.operators[ast.Pow] = operator.pow # simpleeval uses a safe power tool, which fails on symbolic inputs'
        s.functions['Sy'] = sy.Symbol
        symb_F = s.eval(func_str)
    except (se.NameNotDefined, KeyError, SyntaxError) as err:
        with open('failed_function_parsing.out', 'a') as f:
            f.write(f'{function_file}\n')
        raise ValueError(f"Original simpleeval Error: {err}\n\nExplanation: Cannot parse function {func_str}. \n\nGo to the function file: {function_file} and manually edit the function so that \n(1) all implicit multiplications are replaced with explicit ones (e.g. '( -1 ) p' becomes '( -1 )*p'), \n(2) all parameters are wrapped in a Sy function (e.g. 'p' becomes 'Sy('p')')\n(3) all vertical pipes are replaced by parens and division (e.g. 'p + 1 | q' becomes '(p + 1) / (q)'), and \n(4) ** is used for exponents (e.g. 'p^2' becomes 'p**2').\n\nThis is a workaround to avoid using SymPy's built-in parser, which uses eval and should be avoided.\nAfter this file is modified, you can re-run the experiment and the correct solution function will be used.\n\n\nExperiment not completed, Continuing to next experiment...\n\n\n")

    return symb_F
