#pqsva is applicable when the map P, which maps
#all infeasible solutions to feasible soultions
#exists, here consider COPs with independent 
#constraints
from typing import List, bool

#check independence of constraints
def check_cst(constraints: List[set])->bool:
    check = set.intersection(*constraints)
    return bool(check)

#check existance of feasible solutions

#need: get all solutions-->divide into feasible
#and infeasible, for infeasible ones use mapping,
#and also need hamiltonian Q to be defined to 
#calculate energy of each solution