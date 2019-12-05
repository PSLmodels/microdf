def fpl(people):
    """Calculates the federal poverty guideline for a household of a certain
       size.

    Args:
        XTOT: The number of people in the household.

    Returns:
        The federal poverty guideline for the contiguous 48 states.
    """
    return 7820 + 4320 * people
