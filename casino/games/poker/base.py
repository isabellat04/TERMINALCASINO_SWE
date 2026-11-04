from collections import Counter
from itertools import combinations
from casino.utils import cinput

from .variants.poker import Poker
from .views.view import *
# from .constants import *
from ...cards import StandardCard


# ---------------------------------------------------------------------------
# Public entry point (preserves original interface)
# ---------------------------------------------------------------------------

def play_poker(ctx: GameContext) -> None:
    """Play a poker game."""
    Poker(ctx).play()