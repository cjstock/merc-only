"""
Implements the Finite State Machine Design Pattern found here: https://auth0.com/blog/state-pattern-in-python/
"""
from __future__ import annotations
from abc import ABC, abstractmethod

# Context with initial state
class Tactician:

    _state = None
    _health = 100
    _gold = 0
    _traits = None


    def __init__(self, state: State) -> None:
        self.setState(state)

    # method to change the state of the object
    def setState(self, state: State):

        self._state = state
        self._state.tactician = self

    def printState(self):
        print(f"Tactician is in state: {type(self._state).__name__}")

    def performActions(self):
        self._state.performActions()


# STATE INTERFACE
class State(ABC):
    @property
    def tactician(self) -> Tactician:
        return self._tactician

    @tactician.setter
    def tactician(self, tactician: Tactician) -> None:
        self._tactician = tactician

    @abstractmethod
    def performActions(self) -> None:
        pass

# CONCRETE STATES
class initialize(State):
    
    def performActions(self) -> None:
        self.tactician.setState(find_mercs())

class find_mercs(State):

    def performActions(self) -> None:
        self.tactician.setState(loss_streak())

class loss_streak(State):

    def performActions(self) -> None:
        pass

class try_cashing(State):

    def performActions(self) -> None:
        pass

class acquire_5C(State):

    def performActions(self) -> None:
        pass

class end(State):

    def performActions(self) -> None:
        pass



if __name__ == "__main__":
    # The client code.

    myTactician = Tactician(initialize())
    myTactician.performActions()
    myTactician.performActions()