from ..views.european_view import *

class EuropeanRoulette(Roulette):
    """Plays roulette using European rules."""

    def __init__(self, accounts: List[Account]):
        super().__init__(accounts)
        self.wheel = STANDARD_EUROPEAN_ROULETTE_WHEEL
        self.valid_numbers = [number for (number, _, _, _) in self.wheel]


def play_european_roulette(context: GameContext) -> None:
    # Temporary fix
    # TODO: fix argument in play_roulette to only except `List[GameContext]`
    # and not `GameContext`

    # Access account data
    accounts = [context.account]

    roulette = EuropeanRoulette(accounts)
    while True:
        roulette.reset_round()
        render_header(context)

        # Input to stop loop from running constantly
        choice = cinput("Press [Enter] to start a new round and [q] to quit: ").strip().lower()

        if choice in {"q", "quit"}:
            return

        status = roulette.submit_bets(context)
        if status == "BANKRUPT":
            return

        roulette.spin_wheel(context)
        roulette.payout()
        refresh_roulette_topbar(context)

        # play again?
        play_again = cinput("🤵: Would you like to play another round (Y/n): ").strip().lower()
        if play_again in {"", "y", "yes"}:
            pass  # next round
        elif play_again in {"n", "no"}:
            return
        else:
            play_again = prompt_with_error(
                ctx=context,
                prompt="🤵: Would you like to play another round (Y/n): ",
                validator=lambda a: a in {"", "y", "yes", "n", "no"},
                error_text="Please enter 'Yes' or 'No'.",
                render_table=False,
                transform=lambda s: s.strip().lower(),
            )
            if play_again in {"n", "no"}:
                return
