from casino.cards import StandardCard
from casino.types import GameContext
from ..constants import *
from casino.utils import display_topbar, cprint

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------
class PokerView:
    @staticmethod
    def display_poker_topbar(ctx: GameContext) -> None:
        display_topbar(ctx.account, **HEADER_OPTIONS)

    @staticmethod
    def print_cards(hand: list[StandardCard]) -> None:
        """Print cards side by side (face-up)."""
        if not hand:
            return
        card_lines = [card.front.strip("\n").splitlines() for card in hand]
        max_lines = max(len(lines) for lines in card_lines)
        for lines in card_lines:
            while len(lines) < max_lines:
                lines.append(" " * len(lines[0]))
        hand_string = "\n".join(
            "  ".join(card_lines[j][i] for j in range(len(hand)))
            for i in range(max_lines)
        )
        cprint(hand_string)

    @staticmethod
    def print_opponent_cards(opponent_hand: list[StandardCard]) -> None:
        """Print opponent's cards face-down."""
        if not opponent_hand:
            cprint("")
            return
        hidden_cards = [card.back for card in opponent_hand]
        hand_string = "\n".join(
            "  ".join(lines)
            for lines in zip(*[card.strip("\n").splitlines() for card in hidden_cards])
        )
        cprint(hand_string)

    @staticmethod
    def print_hand(hand: list[StandardCard], hidden: bool = False) -> None:
        if hidden:
            PokerView.print_opponent_cards(hand)
        else:
            PokerView.print_cards(hand)

