from cmath import phase
from math import log2
from time import time
import matplotlib.pyplot as plt
import pennylane as qml
from numpy import NaN, complex128
from pennylane.ops.qubit import PauliX, PauliZ
from qiskit import *
from pennylane import numpy as np


class Finance:

    global dev

    dev = qml.device('lightning.qubit', wires=['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', '0'])

    def __init__(self, time_step, N, m):
        self.time_step = time_step
        self.N = N #discrete price values
        self.n = log2(self.N)

        self.m = m #representing time step m = log2(M) : M is the no. of time step
        self.total_qubit = self.n + self. m + 3
        self.cost_history = []


    def single_qubit_layer(self, phase):
        for i in range(self.n+ self.m):
            qml.RX(phase, i)
            qml.RZ(phase, i)

    def entangling_layer(self):
        total_wires = self.m+self.n
        for i in range(total_wires-1):
            for j in range(total_wires -1):                
                qml.IsingXX(wires=(i, j+1))
                # qml.IsingXX(wires=(i, i+2))
                # qml.IsingXX(wires=(i, i+3))

    def quantum_circuit_born_machine(self, phase):
        self.single_qubit_layer(phase)
        self.entangling_layer()

    # @qml.qnode(dev, diff_method="autograd")
    def crca_Rv(self, w_x, w_y, w_z):

        total_wires = self.m + self.n + 1
        qml.RY(w_y[0], wires=total_wires-1)
        qml.RZ(w_z[0], wires=total_wires-1)
        qml.RY(w_y[0], wires=total_wires-1)
        for i in range(total_wires-1):
            qml.CRX(w_x[i], wires=(i, total_wires-1))
            qml.CRY(w_y[i+1], wires=(i, total_wires-1))
            qml.CRZ(w_z[i+1], wires=(i, total_wires-1))

            # qml.Ry(params[1], wires='0')
            # qml.Rz(params[2], wires='0')
            # qml.Ry(params[3], wires='0')
        
            # qml.Rx(params[4], wires=['0','i1'])
            # qml.Ry(params[5], wires=['0','i1'])
            # qml.Rz(params[6], wires=['0','i1'])
            # qml.Rx(params[7], wires=['0','i2'])

        # return qml.expval(qml.PauliZ(1))
    def crca_Rq(self, w_x, w_y, w_z):

        total_wires = self.n+self.m+2

        qml.RY(w_y[0], wires=total_wires-1)
        qml.RZ(w_z[0], wires=total_wires-1)
        qml.RY(w_y[0], wires=total_wires-1)

        for i in range(self.n):
            qml.CRX(w_x[i], wires=(i, total_wires-1))
            qml.CRY(w_y[i+1], wires=(i, total_wires-1))
            qml.CRZ(w_z[i+1], wires=(i, total_wires-1))

    def crca_Rp(self, w_x, w_y, w_z):
        
        total_wires = self.n + self.m + 3

        qml.RY(w_y[0], wires=total_wires-1)
        qml.RZ(w_z[0], wires=total_wires-1)
        qml.RY(w_y[0], wires=total_wires-1)

        for i in range(self.n):
            qml.CRX(w_x[i], wires=(i, total_wires-1))
            qml.CRY(w_y[i+1], wires=(i, total_wires-1))
            qml.CRZ(w_z[i+1], wires=(i, total_wires-1))
        


    @qml.qnode(dev, diff_method="autograd")
    def full_circuit(self):

        q_delta = 0.1
        rng_seed = 0
        phase = NaN #to be updated
        # steps = 100

        # opt = qml.AdamOptimizer(stepsize=0.01, beta1=0.9, beta2=0.99, eps=tol)
        np.random.seed(rng_seed)

        w_x = q_delta*np.random.randn(self.m+self.n, requires_grad=True)
        w_y = q_delta*np.random.randn(self.m+self.n + 1, requires_grad=True)
        w_z = q_delta*np.random.randn(self.m+self.n + 1, requires_grad=True)

        self.quantum_circuit_born_machine(phase)
        self.crca_Rv(w_x, w_y, w_z)
        self.crca_Rq(w_x, w_y, w_z)
        self.crca_Rp(w_x, w_y, w_z)

        

        return qml.expval(qml.PauliZ(1)) #to be changed
        # https://pennylane.readthedocs.io/en/stable/introduction/measurements.html


###############################################################################################################################      



# @qml.qnode(dev)
# def circuit(params):
#     qml.Ry(params[1], wires='0')
#     qml.Rz(params[2], wires='0')
#     qml.Ry(params[3], wires='0')
   
#     qml.Rx(params[4], wires=['0','i1'])
#     qml.Ry(params[5], wires=['0','i1'])
#     qml.Rz(params[6], wires=['0','i1'])
#     qml.Rx(params[7], wires=['0','i2'])

#     return qml.expval(qml.PauliZ(1))



# drawer = qml.draw(circuit, show_all_wires=True, wire_order=['i1','i2','i3','i4','i5','i6','i7',0])
# print(drawer(params))

   

