from phevaluator import Card
from phevaluator import evaluate_5cards
from phevaluator import evaluate_6cards
from phevaluator import evaluate_7cards
from phevaluator import evaluate_cards
from phevaluator import evaluate_omaha_cards
from phevaluator import evaluate_plo4_cards
from phevaluator import evaluate_plo5_cards
from phevaluator import evaluate_plo6_cards


def example1() -> None:
    print("Example 1: A Texas Holdem example")

    a = 7 * 4 + 0  # 9c
    b = 2 * 4 + 0  # 4c
    c = 2 * 4 + 3  # 4s
    d = 7 * 4 + 1  # 9d
    e = 2 * 4 + 2  # 4h

    # Player 1
    f = 10 * 4 + 0  # Qc
    g = 4 * 4 + 0  # 6c

    # Player 2
    h = 0 * 4 + 0  # 2c
    i = 7 * 4 + 2  # 9h

    rank1 = evaluate_cards(a, b, c, d, e, f, g)  # expected 292
    rank2 = evaluate_cards(a, b, c, d, e, h, i)  # expected 236

    print(f"The rank of the hand in player 1 is {rank1}")
    print(f"The rank of the hand in player 2 is {rank2}")
    print("Player 2 has a stronger hand")


def example2() -> None:
    print("Example 2: Another Texas Holdem example")

    rank1 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")  # expected 292
    rank2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")  # expected 236

    print(f"The rank of the hand in player 1 is {rank1}")
    print(f"The rank of the hand in player 2 is {rank2}")
    print("Player 2 has a stronger hand")


def example3() -> None:
    print("Example 3: An Omaha poker example")
    # fmt: off
    rank1 = evaluate_omaha_cards(
        "4c", "5c", "6c", "7s", "8s", # community cards
        "2c", "9c", "As", "Kd",       # player hole cards
    )

    rank2 = evaluate_omaha_cards(
        "4c", "5c", "6c", "7s", "8s", # community cards
        "6s", "9s", "Ts", "Js",       # player hole cards
    )
    # fmt: on

    print(f"The rank of the hand in player 1 is {rank1}")  # expected 1578
    print(f"The rank of the hand in player 2 is {rank2}")  # expected 1604
    print("Player 1 has a stronger hand")


def example4() -> None:
    print("Example 4: Evaluating 5, 6, and 7 cards with string arguments")

    rank5 = evaluate_5cards("Ac", "Ad", "Ah", "As", "Kc")  # expected 11
    rank6 = evaluate_6cards("Ac", "Ad", "Ah", "As", "Kc", "Kd")  # expected 11
    rank7 = evaluate_7cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")  # expected 292

    print(f"The rank of the 5-card hand is {rank5}")
    print(f"The rank of the 6-card hand is {rank6}")
    print(f"The rank of the 7-card hand is {rank7}")


def example5() -> None:
    print("Example 5: Evaluating Omaha (PLO) hands with string arguments")

    # evaluate_plo4_cards is equivalent to evaluate_omaha_cards.
    # fmt: off
    rank4 = evaluate_plo4_cards(
        "4c", "5c", "6c", "7s", "8s", # community cards
        "2c", "9c", "As", "Kd",       # player hole cards
    )
    # fmt: on
    print(f"The rank of the PLO4 hand is {rank4}")  # expected 1578

    # PLO5 and PLO6 require the package to be built with PLO5/PLO6 support (see
    # PHEVALUATOR_BUILD_PLO in the README). They raise NotImplementedError
    # otherwise.
    try:
        # fmt: off
        rank5 = evaluate_plo5_cards(
            "4c", "5c", "6c", "7s", "8s",  # community cards
            "2c", "9c", "As", "Kd", "Jh",  # player hole cards
        )
        # fmt: on
        print(f"The rank of the PLO5 hand is {rank5}")  # expected 1578
    except NotImplementedError as error:
        print(f"PLO5 is unavailable: {error}")

    try:
        # fmt: off
        rank6 = evaluate_plo6_cards(
            "4c", "5c", "6c", "7s", "8s",        # community cards
            "2c", "9c", "As", "Kd", "Jh", "8d",  # player hole cards
        )
        # fmt: on
        print(f"The rank of the PLO6 hand is {rank6}")  # expected 1578
    except NotImplementedError as error:
        print(f"PLO6 is unavailable: {error}")


def example6() -> None:
    print("Example 6: Passing int, string, and Card arguments to evaluate_cards")

    # The same hand (2d 2h 2s Tc Ac) expressed with different argument types.
    rank_int = evaluate_cards(1, 2, 3, 32, 48)
    rank_str = evaluate_cards("2d", "2h", "2s", "Tc", "Ac")
    rank_card = evaluate_cards(
        Card("2d"), Card("2h"), Card("2s"), Card("Tc"), Card("Ac")
    )
    rank_mixed = evaluate_cards(1, "2h", "2S", Card(32), Card("Ac"))

    print(f"Using ints:    {rank_int}")  # expected 2405
    print(f"Using strings: {rank_str}")
    print(f"Using Cards:   {rank_card}")
    print(f"Using mixed:   {rank_mixed}")
    print("All four calls return the same rank")


if __name__ == "__main__":
    example1()
    example2()
    example3()
    example4()
    example5()
    example6()
