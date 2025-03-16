#for building basic functions 
from typing import List, Any, Callable
import numpy as np
import qutip
import scipy

def h_cst(
        num_cst: int, 
        bmin_list: list[int], 
        bmax_list: list[int], 
        a_list: list[list[int]]
        )->list[int]:
    
    #how to express x_i? x_i is binary variable representing any possible config
    ...
    #return constraint hamiltonian

def h_ising():
    ...
    #expect hamiltonian using binary variable
    #this function does variable transformation to get the ising form

def cost():
    #define cost function C, evaluated on eigenbasis of pauli z
    ...

def build_schedule(s1, s2, evol_time): 
    #build schedule function
    #given a list of time, 0 to T, return a list of s values
    #dependent on the form of s chosen
    #can use the linear form given in eq12
    ...

def evolve_schrodinger(h_ising: qutip.Qobj, 
                       h_cst: qutip.Qobj, 
                       init_state: qutip.Qobj, 
                       evol_time:  int, 
                       schedule: Callable,
                       time_step: int = 10,
                       operator_list: Any | None = None)->qutip.Qobj:
    #for time evolution of state psi, from time 0 to T
    #need changes: hamiltonian should be time-dependent->should be a list of Qobj 
    #with s at each time steps?
    hamiltonian = schedule * h_ising + (1 - schedule) * h_cst
    tlist = np.arange(0, evol_time, step = time_step)
    result = qutip.sesolve(H=hamiltonian, psi0= init_state, tlist=tlist, e_ops=operator_list)
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

def greedy_post_processing(sigma_prime, Q_prime):
    """
    Greedy post-processing algorithm for PVSQA.

    Parameters:
    sigma_prime (np.array): Input spin configuration (values ±1).
    Q_prime (np.array): Quadratic matrix representing energy function.

    Returns:
    sigma (np.array): Processed spin configuration (values ±1).
    """

    # Convert spin configuration to binary
    x = (sigma_prime + 1) // 2
    V = len(x)

    f = True
    while f:
        delta_Q = np.zeros(V)
        
        for i in range(V):
            # Calculate energy change if we flip x[i]
            delta_x = 1 - 2 * x[i]
            delta_Q[i] = delta_x * (Q_prime[i, :] @ x + Q_prime[:, i] @ x - Q_prime[i, i] * x[i])

        # Find the best spin flip
        j = np.argmin(delta_Q)

        if delta_Q[j] < 0:
            x[j] = 1 - x[j]  # flip spin
        else:
            f = False

    # Convert binary configuration back to spins
    sigma = 2 * x - 1
    return sigma
