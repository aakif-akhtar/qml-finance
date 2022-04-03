from cmath import phase
from time import time
import matplotlib.pyplot as plt
import pennylane as qml
from numpy import complex128
from pennylane.ops.qubit import PauliX, PauliZ
from qiskit import *
from pennylane import numpy as np


class Finance:
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

###############################################################################################################################      
dev = qml.device('default.qubit', wires=['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', '0'])


@qml.qnode(dev)
def circuit(params):
    qml.Ry(params[1], wires='0')
    qml.Rz(params[2], wires='0')
    qml.Ry(params[3], wires='0')
   
    qml.Rx(params[4], wires=['0','i1'])
    qml.Ry(params[5], wires=['0','i1'])
    qml.Rz(params[6], wires=['0','i1'])
    qml.Rx(params[7], wires=['0','i2'])

    return qml.expval(qml.PauliZ(1))

params = [0.1, 0.3, 0.2, 0.3, 0.1, 0.2, 0.3 ]
drawer = qml.draw(circuit, show_all_wires=True, wire_order=[2,1,0,3])
print(drawer(params))

   

