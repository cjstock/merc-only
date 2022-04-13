"""
Implements the Finite State Machine Design Pattern found here: https://auth0.com/blog/state-pattern-in-python/
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from detection import Detection

from windowcapture import WindowCapture

# Context with initial state
class GameContext:

    _state = None
    _wincap = None
    _detection = None
    _uilocations_cache = {}


    def __init__(self, state: State) -> None:
        self.setState(state)

    # method to change the state of the object
    def setState(self, state: State):

        self._state = state
        self._state.context = self

    def printState(self):
        print(f"GameContext is in state: {type(self._state).__name__}")

    def performActions(self):
        self._state.performActions()


# STATE INTERFACE
class State(ABC):
    @property
    def context(self) -> GameContext:
        return self._context

    @context.setter
    def context(self, context: GameContext) -> None:
        self._context = context

    @abstractmethod
    def performActions(self) -> None:
        pass

# CONCRETE STATES
class initialize(State):
    
    def performActions(self) -> None:
        self.context._wincap = WindowCapture('League of Legends (TM) Client')
        self.context._detection = Detection()
        self.context._wincap.start()
        self.context.setState()

class wait_for_stage12(State):

    def performActions(self) -> None:
        self.context._detection.action(targets=['stage-12'], action='start')
        location = []
        while location == []:
            location = self.context._detection.detectors['stage-12'].rectangles
        self.context._uilocations_cache['stage'] = location
        self.context.setState(set_ui_locations())


class set_ui_locations(State):

    def performActions(self) -> None:
        self.context._detection.action(targets=['roll'], action='start')
        self.context._detection.action(targets=['roll'], action='update', args=self.context._wincap.screenshot)

class end(State):

    def performActions(self) -> None:
        self.context._wincap.stop()