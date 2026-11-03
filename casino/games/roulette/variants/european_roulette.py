from ..views.european_view import *

class EuropeanRoulette(Roulette):
    """Plays roulette using European rules."""

    def __init__(self, accounts: List[Account]):
        super().__init__(accounts)
        self.wheel = STANDARD_EUROPEAN_ROULETTE_WHEEL
        self.valid_numbers = [number for (number, _, _, _) in self.wheel]