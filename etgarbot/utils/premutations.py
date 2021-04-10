import typing


def add_to_permutations(permutations: typing.Set[tuple],
                        add
                        ) -> typing.Set[tuple]:
    """
    Recives a set of premutations, and adds adds a single value to all of them.
    Keep in mind that the original order of the permutations is saved!

    for example: add_to_permutations(
        {(1, 2, 3), (4, 5, 6)},
        'x'
    )

    will return: {
        ('x', 1, 2, 3), (1, 'x', 2, 3), (1, 2, 'x', 3), (1, 2, 3, 'x'),
        ('x', 4, 5, 6), (4, 'x', 5, 6), (4, 5, 'x', 6), (4, 5, 6, 'x')
    }

    """
    result = set()
    for permutation in permutations:
        permutation = list(permutation)
        for i in range(len(permutation) + 1):
            new = permutation.copy()
            new.insert(i, add)
            result.add(tuple(new))

    return result
