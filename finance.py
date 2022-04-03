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
