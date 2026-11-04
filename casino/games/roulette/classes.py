from __future__ import annotations

from typing import Type

from casino.accounts import Account
from casino.types import GameContext

from .variants.european_roulette import EuropeanRoulette
from .variants.roulette import AmericanRoulette
from .views import european_view, standard_view


class Roulette:
    """Base game facade, configured for American or European roulette.

    Game rules, wheel configuration, betting, and payouts remain implemented
    by the existing variant classes. This facade selects the requested variant
    without duplicating or changing that behavior.
    """

    def __init__(self, accounts: list[Account], *, european: bool = False) -> None:
        variant: Type[AmericanRoulette] = EuropeanRoulette if european else AmericanRoulette
        self.game = variant(accounts)

    def __getattr__(self, name: str):
        # Preserve the variant game's existing API (reset_round, submit_bets,
        # spin_wheel, payout, and state) for callers of the facade.
        return getattr(self.game, name)


class RouletteView:
    """Roulette terminal rendering operations for either wheel variant."""

    def __init__(self, *, european: bool = False) -> None:
        self._view = european_view if european else standard_view

    def display_topbar(self, context: GameContext) -> None:
        self._view.display_roulette_topbar(context)

    def refresh_topbar(self, context: GameContext) -> None:
        self._view.refresh_roulette_topbar(context)

    def render_header(self, context: GameContext) -> None:
        if self._view is european_view:
            self._view.render_header(context)
        else:
            self._view.clear_screen()
            self._view.display_roulette_topbar(context)

    def print_wheel(self, game: Roulette, highlighted_num: str | None = None) -> None:
        game.print_wheel(highlighted_num=highlighted_num)


__all__ = ["Roulette", "RouletteView", "play_roulette", "play_european_roulette"]


def play_roulette(context: GameContext) -> None:
    """Compatibility entry point for the American roulette game."""
    from .base import play_roulette as play

    play(context)


def play_european_roulette(context: GameContext) -> None:
    """Compatibility entry point for the European roulette game."""
    from .base import play_european_roulette as play

    play(context)
