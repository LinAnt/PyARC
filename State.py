class State:
    def run(self):
        assert 0, "run not implemented"


class HeatUpState(State):
    def run(self, controller):
        pass
        # Both heaters on, valve shut
        # Check if boiler temp is equal to HeatUpTemp, if so enter stabilisation


class StabState(State):
    def run(self, controller):
        pass
        # One heater on, valve shut
        # Check reflux column temperature, if constant for stabTime set stableTemp and move to OutState


class OutState(State):
    def run(self, controller):
        pass
        # One heater on, valve open
        # Check boiler temp, if equal to maxTemp, shut down the system.
        # Check column temperature, if the difference between column temp and stableTemp is
        # greater than 0.1 -> ReStabState


class ReStabState(State):
    def run(self, controller):
        pass
        # One heater on, valve closed
        # Check boiler temp, if equal to maxTemp, shut down the system.
        # Check column temperature, if equal to stableTemp -> OutState

