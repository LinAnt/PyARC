import Config
from time import time


class State:

    def run(self):
        assert 0, "run not implemented"

    def check_boiler_temperature(self):
        return 50
        # TODO implement method to check and return boiler temperature.

    def check_column_temperature(self):
        return 50
        # TODO implement method to check and return boiler temperature.


class HeatUpState(State):
    def run(self):
        global StateTime
        if self.check_boiler_temperature() == Config.HeatUpTemperature:
            StateTime = time()
            return StabState
        else:
            return HeatUpState

        # Both heaters on, valve shut
        # Check if boiler temp is equal to HeatUpTemp, if so enter stabilisation


class StabState(State):
    def run(self):
        global StateTime
        global StableTemperature

        if time()-StateTime < Config.StabilizationTime: # Checks how many seconds have passed since stabilization began
            return StabState
        else:
            StableTemperature = self.check_column_temperature()
            return OutState

        # One heater on, valve shut
        # Check reflux column temperature, if constant for stabTime set stableTemp and move to OutState


class OutState(State):
    def run(self):
        if self.check_boiler_temperature() > Config.MaxTemperature:
            print("Max temperature reached, shutting down")
            SystemExit(0)

        elif self.check_column_temperature() == Config.StableTemperature:
            return OutState

        else:
            return ReStabState

        # One heater on, valve open
        # Check boiler temp, if equal to maxTemp, shut down the system.
        # Check column temperature, if the difference between column temp and stableTemp is
        # greater than 0.1 -> ReStabState


class ReStabState(State):
    def run(self, controller):
        if self.check_boiler_temperature() > Config.MaxTemperature:
            print("Max temperature reached, shutting down")
            SystemExit(0)

        elif self.check_column_temperature() == Config.StableTemperature:
            return OutState

        else:
            return ReStabState

        # One heater on, valve closed
        # Check boiler temp, if equal to maxTemp, shut down the system.
        # Check column temperature, if equal to stableTemp -> OutState

