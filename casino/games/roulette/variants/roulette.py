from casino.stats import GameStats, display_stats
from ..views.standard_view import *



class AmericanRoulette(Roulette):
    """Plays roulette using American rules."""

    def __init__(self, accounts: List[Account]):
        super().__init__(accounts)
        self.wheel = STANDARD_AMERICAN_ROULETTE_WHEEL
        self.valid_numbers = [number for (number, _, _, _) in self.wheel]


def play_roulette(context: GameContext) -> None:
    continue_game = True

    # Temporary fix
    # TODO: fix argument in play_roulette to only except `List[GameContext]`
    # and not `GameContext`
    contexts = [context]

    # Access account data
    accounts = [account.account for account in contexts]

    if not isinstance(accounts, list):
        raise ValueError("accounts is not a list. "
                         f"accounts is a {type(accounts)}")

    cprint("roulette object created")
    roulette = AmericanRoulette(accounts)
    stats = GameStats("Roulette", context.account.balance)
    stats.rounds_played = 0
    while continue_game:
        roulette.reset_round()
        clear_screen()
        display_roulette_topbar(context)
        stats.rounds_played += 1
        cprint("within loop, round incremented")

        # Input to stop loop from running constantly
        choice = cinput("Press [Enter] to start a new round and [q] to quit: ")

        if choice.lower() in {"q", "quit"}:
            continue_game = False
            stats.ending_balance = context.account.balance
            display_stats(stats)
            break

        status = roulette.submit_bets(context)
        if status == "BANKRUPT":
            stats.ending_balance = context.account.balance
            display_stats(stats)
            break

        roulette.spin_wheel(context)
        roulette.payout(stats)
        refresh_roulette_topbar(context)

        play_again = None

        while True:
            valid_choices = ["N", "NO", "Y", "YES", ""]
            play_again = cinput("🤵: Would you like to play another round (Y/n): ")

            if play_again.upper() not in valid_choices:
                cprint("Please enter 'Yes' or 'No'.")
                continue
            if play_again.lower() in {"n", "no"}:
                stats.ending_balance = context.account.balance
                print("before display stats")
                display_stats(stats)
                continue_game = False
                break
            elif play_again == "" or play_again.lower() in {"y", "yes"}:
                continue_game = True
                break

    #cprint("Exiting roulette...")
    #sleep(0.5)
