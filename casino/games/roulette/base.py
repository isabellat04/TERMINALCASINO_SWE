from .variants.european_roulette import *
from .variants.roulette import *
# from variants import european_roulette, roulette

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