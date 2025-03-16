#for building basic functions 
from typing import List, Any, Callable
import numpy as np
from qutip import *
import scipy

sx = sigmax()
sy = sigmay()
sz = sigmaz()

ket0 = basis(2,0)
ket1 = basis(2,1)

'''
#to be moved to example.py: problem-specific
def h_cst(
        num_cst: int, 
        bmin_list: list[int], 
        bmax_list: list[int], 
        a_list: list[list[int]]
        )->list[int]:
    
    #how to express x_i? x_i is binary variable representing any possible config
    ...
    #return constraint hamiltonian
    #i think this depends on individual problem setup, maybe move this to example.py?
'''

def h_ising(j_array: np.ndarray[tuple[int], np.dtype[np.float64]], 
            h_array: np.ndarray[tuple[tuple], np.dtype[np.float64]], 
            h0: float,
            n_sites: int)->Qobj:
    #expect hamiltonian using binary variable
    #this function does variable transformation to get the ising form
    #from eq1, get sum_i,j J_ij sz_i*sz_j + sum_i h_i sz_i + h0 (const)
    h_int = 0
    h_self = 0
    for i in np.arange(n_sites): 
        operatorlist = [qeye(2)]*n_sites
        operatorlist[i] = sz
        h_self += h_array[i] * tensor(*operatorlist)
        operatorlist[i+1] = sz
        h_int += j_array[i, i+1] * tensor(*operatorlist)
    return h_int + h_self + h0



def cost(config_ket: Qobj, obj_function: Qobj)->np.float64:
    #define cost function C, evaluated on eigenbasis of pauli z
    return obj_function.matrix_element(config_ket.conj(), config_ket)

def linear_schedule(t, s1, s2, evol_time): 
    #build schedule function
    #given a list of time, 0 to T, return a list of s values
    #dependent on the form of s chosen
    #can use the linear form given in eq12
    return s1 + t*(s2 - s1)/evol_time

def evolve_schrodinger(h_ising: Qobj, 
                       h_cst: Qobj, 
                       init_state: Qobj, 
                       evol_time:  int, 
                       schedule: Callable,
                       time_step: int = 10,
                       operator_list: Any | None = None)->Qobj:
    #for time evolution of state psi, from time 0 to T
    #need changes: hamiltonian should be time-dependent->should be a list of Qobj 
    #with s at each time steps?
    hamiltonian = [[h_ising, schedule], [h_cst, (1-schedule)]]
    tlist = np.arange(0, evol_time, step = time_step)
    result = sesolve(H=hamiltonian, psi0= init_state, tlist=tlist, e_ops=operator_list)
    return result.states


def prob(): 
    #probability p of a spin configuration
    ...


def renormalised_prob():
    #renormalised prob
    ...

def energy_expectation():
    #expectation of energy E
    ...