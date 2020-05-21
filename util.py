def lines(file):
    for char in file: yield char
    yield '\n'


def blocks(file):
    block = []
    for char in lines(file):
        if char.strip():
            block.append(char)
        elif block:
            yield ''.join(block).strip()
            block = []
