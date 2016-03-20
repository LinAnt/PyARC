from State import *


class Controller:
    def __init__(self):
        self.state = HeatUpState

    def run_state(self):
        self.state = self.state.run()  # Runs the state which returns the next state.

    def set_new_state(self, new_state):
        self.state = new_state
