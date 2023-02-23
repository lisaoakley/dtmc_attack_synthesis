Experiment Code for Attack Synthesis in DTMCs (https://arxiv.org/pdf/2110.02125.pdf)

# Starting the PRISM gateway server
Skip this step if using **optimization with symbolic solution function** ([Oakley et al. Section 4.2.2](https://arxiv.org/pdf/2110.02125.pdf)). If, however, you are using **optimization with direct computation** ([Oakley et al. Section 4.2.1](https://arxiv.org/pdf/2110.02125.pdf)) with [PRISM](https://www.prismmodelchecker.org/) for the probabilistic model checker, you must first open the Prism gateway
```
% cd prism-gateway
% make
% make start
% cd ..
```

# Running the program
Basic usage for the tool can be found by running 
```
./run --help
```
from the base directory. Examples of experiments can be found in the `./scripts` directory.

## Symbolic Solution Function Formatting
When using **optimization with symbolic solution function** ([Oakley et al. Section 4.2.2](https://arxiv.org/pdf/2110.02125.pdf)), the parametric model checking tool ([PARAM](https://depend.cs.uni-saarland.de/tools/param/) or [PRISM](https://www.prismmodelchecker.org/)) outputs a string representation of the symbolic solution function. To parse this string into sympy, we would have to use the [SymPy built-in parser](https://docs.sympy.org/latest/modules/core.html#sympy.core.sympify.sympify), which uses `eval` on unsanitized input and should therefore be avoided.

As a result, the user must:
1. Run each experiment once to generate the solution function. The solution function will be saved to a file along with the duration it took to generate this function. A list of paths to these files will be saved to `failed_function_parsing.out`. Then, the program will error out with the following message:
```
Original simpleeval Error: [SOME PARSING ERROR]

Explanation: Cannot parse function [FUNCTION STRING]

Go to the function file: results/[case study name]/[case study id]/symbolic/[epsilon * 100, padded with zeros]/[property id]/[threat model id]/symb_F.txt and manually edit the function so that
(1) all implicit multiplications are replaced with explicit ones (e.g. '( -1 ) p' becomes '( -1 )*p'),
(2) all parameters are wrapped in a Sy function (e.g. 'p' becomes 'Sy('p')')
(3) all vertical pipes are replaced by parens and division (e.g. 'p + 1 | q' becomes '(p + 1) / (q)'), and
(4) ** is used for exponents (e.g. 'p^2' becomes 'p**2').

This is a workaround to avoid using SymPy's built-in parser, which uses eval and should be avoided.
After this file is modified, you can re-run the experiment and the correct solution function will be used.


Experiment not completed, Continuing to next experiment...
```
2. Modify the appropriate line of each `symb_F.txt` file, replacing the original function string with the correctly formatted string as described in the error message. Then re-run all experiments exactly as before. The program will execute, skipping the function generation step and instead pulling the function and duration from the modified file, continuing on to complete the experiment as expected. 

Feedback on how to eliminate this manual step without using `eval` is welcome and can be emailed to `oakley.l [at] northeastern [dot] edu` or submitted as a pull request/issue.

# Troubleshooting
For error 
```
py4j.protocol.Py4JNetworkError: An error occurred while trying to connect to the Java server
```
make sure you have [started the PRISM JVM](#starting-the-prism-gateway-server). Note that if the PRISM JVM exits with an error, the server terminates and must be re-started using `make start`.

For error
```
Original simpleeval Error: [SOME PARSING ERROR]

Explanation: Cannot parse function [FUNCTION STRING]

...
```
see [Symbolic Solution Function Formatting](#symbolic-solution-function-formatting).

Other issues/questions please email `oakley.l [at] northeastern [dot] edu` or open a GitHub issue.

# Reproducing experiments
Experiments from [Oakley et al.](https://arxiv.org/pdf/2110.02125.pdf) can be run from the base directory as follows:

## Figure 1 (4-state DTMC):
Experiments:
```
% ./scripts/fig1.sh
```
Perturbed transition probability matrix CSVs can be found in:
```
results/fig1/fig1/concrete/010/until10_fig1/SPSS_1/PplusX.csv
results/fig1/fig1/concrete/010/until10_fig1/SPST_9/PplusX.csv
results/fig1/fig1/concrete/010/until10_fig1/SS_1/PplusX.csv
results/fig1/fig1/concrete/010/until10_fig1/ST_9/PplusX.csv
```

## Figure 5a (simple communication protocol):
Experiment:
```
% ./scripts/protocol_Pr_vs_eps_by_tm.sh
```
Plotting:
```
% ./plotting/Pr_vs_epsilon_protocol  
```

## Figure 5b (IPv4 ZeroConf protocol):
Experiment:
```
% ./scripts/zeroconf_n10_Pr_vs_eps_by_tm.sh
```
Plotting:
```
% ./plotting/Pr_vs_epsilon_zeroconf_n10 
```

## Figure 5c and 5d (5x5 Gridworld):
Experiment:
```
% ./scripts/Pr_vs_eps_by_tm.sh
```
Plotting:
5c
```
% ./plotting/Pr_vs_epsilon_SS
```
5d
```
% ./plotting/Pr_vs_epsilon_ST
```

## Figure 6 (perturbation heatmaps for 3x3 Gridworld):
Experiment:
```
% ./scripts/3x3heatmaps.sh
```
Plotting:
```
% ./plotting/heatmaps
```

## Figure 7 (component analysis heatmaps for 3x3 Gridworld):
Experiment:
```
% ./scripts/3x3states.sh
```
Plotting:
```
% ./plotting/selected_states_heatmap
```

## Table 1 (comparing optimization approaches):
Experiments:
```
% ./scripts/3params_concrete.sh
% ./scripts/3params_symbolic.sh
% ./scripts/5params_concrete.sh
% ./scripts/5params_symbolic.sh
% ./scripts/10params_concrete.sh
% ./scripts/10params_symbolic.sh
% ./scripts/15params_concrete.sh
% ./scripts/15params_symbolic.sh
```
Plotting:
```
% ./plotting/scale_table
```

# How to Cite
Oakley, Lisa, Alina Oprea, and Stavros Tripakis. "Adversarial Robustness Verification and Attack Synthesis in Stochastic Systems," 2022 IEEE 35th Computer Security Foundations Symposium (CSF), 2022, doi: 10.1109/CSF54842.2022.9919660.

```
@inproceedings{oakley2022adversarial,
  author={Oakley, Lisa and Oprea, Alina and Tripakis, Stavros},
  booktitle={2022 IEEE 35th Computer Security Foundations Symposium (CSF)}, 
  title={Adversarial Robustness Verification and Attack Synthesis in Stochastic Systems}, 
  year={2022},
  pages={380-395},
  doi={10.1109/CSF54842.2022.9919660}}

```
