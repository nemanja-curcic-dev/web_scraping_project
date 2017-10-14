def find_number(s):
    """Finds the number in string and returns it"""
    split = s.split()
    digit = 0
    for s in split:
        if s.isdigit():
            digit = s
    return digit


def find_floor(s):
    floor = ""

    for c in s:
        if c.isdigit():
            floor += c

    return floor

if __name__ == '__main__':
    print(find_floor("Etage: 20. Stock"))