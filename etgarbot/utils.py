from functools import lru_cache


@lru_cache(2 ** 10)
def string_distance(a: str, b: str) -> int:
    """ Calculates the distance between the two given strings. """

    lengths = len(a), len(b)
    if min(lengths) == 0:
        return max(lengths)

    a_char, a_reminder = a[-1], a[:-1]
    b_char, b_reminder = b[-1], b[:-1]
    cost = 1 if a_char != b_char else 0

    return min((
        string_distance(a, b_reminder) + 1,
        string_distance(a_reminder, b) + 1,
        string_distance(a_reminder, b_reminder) + cost,
    ))
