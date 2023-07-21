def until(arg: str, conditional: tuple, start: int, increment: int) -> int:
    i = start
    while i >= 0 and i < len(arg) and arg[i] in conditional: i += increment
    return i

def conjoin(*args: str) -> str:
    joint = ('/', '\\')
    return '/'.join([arg[until(arg, joint, 0, +1):until(arg, joint, len(arg)-1, -1)+1] for arg in args])