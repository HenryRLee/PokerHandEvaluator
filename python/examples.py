from phevaluator import evaluate_cards, evaluate_omaha_cards


def example1():
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

    p1 = evaluate_cards(a, b, c, d, e, f, g)  # expected 292
    p2 = evaluate_cards(a, b, c, d, e, h, i)  # expected 236

    print(f"The rank of the hand in player 1 is {p1}")
    print(f"The rank of the hand in player 2 is {p2}")
    print("Player 2 has a stronger hand")


def example2():
    print("Example 2: Another Texas Holdem example")

    p1 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "Qc", "6c")  # expected 292
    p2 = evaluate_cards("9c", "4c", "4s", "9d", "4h", "2c", "9h")  # expected 236

    print(f"The rank of the hand in player 1 is {p1}")
    print(f"The rank of the hand in player 2 is {p2}")
    print("Player 2 has a stronger hand")


def example3():
    print("Example 3: An Omaha poker example")
    # fmt: off
    p1 = evaluate_omaha_cards(
        "4c", "5c", "6c", "7s", "8s", # community cards
        "2c", "9c", "As", "Kd",       # player hole cards
    )

    p2 = evaluate_omaha_cards(
        "4c", "5c", "6c", "7s", "8s", # community cards
        "6s", "9s", "Ts", "Js",       # player hole cards
    )
    # fmt: on

    print(f"The rank of the hand in player 1 is {p1}")  # expected 1578
    print(f"The rank of the hand in player 2 is {p2}")  # expected 1604
    print("Player 1 has a stronger hand")


if __name__ == "__main__":
    example1()
    example2()
    example3()
