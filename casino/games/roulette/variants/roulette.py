from casino.stats import GameStats, display_stats
from ..views.standard_view import *



class AmericanRoulette(Roulette):
    """Plays roulette using American rules."""

    def __init__(self, accounts: List[Account]):
        super().__init__(accounts)
        self.wheel = STANDARD_AMERICAN_ROULETTE_WHEEL
        self.valid_numbers = [number for (number, _, _, _) in self.wheel]