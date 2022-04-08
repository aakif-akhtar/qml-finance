from cmath import phase
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

    def __init__(self, time_step, total_qubit):
        self.time_step = time_step
        self.total_qubit = total_qubit

        self.cost_history = []


    def single_qubit_layer(self, phase):
        for i in range(self.total_qubit):
            qml.RX(phase, i)
            qml.RZ(phase, i)

    def entangling_layer(self):
        for i in range(self.total_qubit):
            if i!=self.total_qubit-1:

                qml.IsingXX(wires=(i, i+1))
                qml.IsingXX(wires=(i, i+2))
                qml.IsingXX(wires=(i, i+3))

    def quantum_circuit_born_machine(self, phase):
        self.single_qubit_layer(phase)
        self.entangling_layer()

    # @qml.qnode(dev, diff_method="autograd")
    def controlled_rotation_circuit_ansatz(self, params):
        qml.Ry(params[1], wires='0')
        qml.Rz(params[2], wires='0')
        qml.Ry(params[3], wires='0')
    
        qml.Rx(params[4], wires=['0','i1'])
        qml.Ry(params[5], wires=['0','i1'])
        qml.Rz(params[6], wires=['0','i1'])
        qml.Rx(params[7], wires=['0','i2'])

        # return qml.expval(qml.PauliZ(1))

    @qml.qnode(dev, diff_method="autograd")
    def full_circuit(self):

        q_delta = 0.1
        rng_seed = 0
        phase = NaN #to be updated
        # steps = 100

        # opt = qml.AdamOptimizer(stepsize=0.01, beta1=0.9, beta2=0.99, eps=tol)
        np.random.seed(rng_seed)

        w = q_delta*np.random.randn(self.total_qubit - 1, requires_grad=True)
        self.quantum_circuit_born_machine(phase)
        self.controlled_rotation_circuit_ansatz(w)

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

   

