def load(file_path):
    try:
        with open(file_path) as file:
            lines = file.readlines()
    except FileNotFoundError:
        return None
    return lines


def save(file_path, lines):
    with open(file_path, 'w') as file:
        file.write("\n".join(lines))
