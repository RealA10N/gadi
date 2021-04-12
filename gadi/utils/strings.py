""" A collection of utility functions that are used with strings. """


def levenshtein_distance(string1: str, string2: str) -> int:
    """ Returns the edit distance between the two given strings.
    https://en.wikipedia.org/wiki/Levenshtein_distance """

    if min(len(string1), len(string2)) == 0:
        return max(len(string1), len(string2))

    previous_row = range(len(string2) + 1)  # The 'zero' row

    for i, c1 in enumerate(string1):
        current_row = [i + 1]

        for j, c2 in enumerate(string2):

            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return current_row[-1]


def levenshtein_score(string1: str, string2: str) -> float:
    """ Returns a floating number between 0 and 1. If the number is 0,
    The two given strings are totally different. However, if the returned
    number is 1, the two given strings the the same. """

    max_distance = max(len(string1), len(string2))
    if max_distance == 0:
        # Special case: if both strings are empty (length zero).
        return 0

    distance = levenshtein_distance(string1, string2)
    return (max_distance - distance) / max_distance
