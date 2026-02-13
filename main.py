import re

#Kyle Bertrand
#Robert Huntington
search_list : list[str] = ["22.11","23","66.7f","123abc",
                           "Case44","Happy","78","66.7","yes123","Book111"]

patterns = [
    ("a: integer", re.compile(r"^\d+$")),
    ("b: float", re.compile(r"^\d+\.\d+$")),
    ("c: float with\\d[2] after decimal", re.compile(r"^\d+\.\d{2}$")),
    ("d: float with f", re.compile(r"^\d+\.\d+f$")),
    ("e: Capital + lowercase + digits", re.compile(r"^[A-Z][a-z]+\d+$")),
    ("f: Exactly 3 digits + 2 or more letters", re.compile(r"^\d{3}[A-Za-z]{2,}$"))
]


def print_matches(search_list : list[str], patterns : list[str] ):
    for s in search_list:
        matches = []

        for desc, rx in patterns:
                if rx.match(s):
                    matches.append(desc)
        if matches:
            print(f'{s:10} -> matches:{", ".join(matches)}')
        else:
            print(f'{s:10} -> no matches')

def remove_leading_integer(text : str) -> None:
    match = re.match(r"^(\d+)\s*", text)

    if match:
        number = match.group(1)
        start_index = match.start(1)
        end_index = match.end(1) -1
        rest_of_str = text[match.end():]

        print(
            f'Found integer {number} at the beginning of this string, '
            f'starting at index {start_index}, ending at index {end_index}. '
            f'The rest of the string is: {rest_of_str}. '
        )
    else:
        print("Found no integer at the beginning of this string")

print("\n------------Task 1 ---------------\n")
print_matches(search_list, patterns)
print("\n------------Task 2 ---------------\n")
remove_leading_integer("22 street")
remove_leading_integer("90years")