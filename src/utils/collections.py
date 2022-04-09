def flatten(list: list) -> list:
    """
    Flattens a list of lists into a single list
    """
    return [item for sublist in list for item in sublist]
