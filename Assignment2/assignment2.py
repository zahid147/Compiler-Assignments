import re

def lexer(text):
    tokens = [
        ('kw',     r'\b(?:char|int|float|if|else)\b'),
        ('id',     r'[a-zA-Z_]\w*'),
        ('num',    r'\b\d+\.\d+|\b\d+\b'),
        ('op',     r'<=|>=|==|!=|[+\-*/=<>]'),
        ('par',    r'[(){}]'),
        ('sep',    r'[;,\'"]'),
        ('ws',     r'\s+'),
        ('unkn',   r'.')
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
    get_token = re.compile(tok_regex).finditer

    res = []
    for ch in get_token(text):
        key = ch.lastgroup
        value = ch.group()
        if key == 'ws':
            continue
        elif key == 'num' and '.' in value:
            if not re.fullmatch(r'\d+\.\d+', value):
                res.append(f"[unkn {value}]")
                continue
        res.append(f"[{key} {value}]")
    return res


with open("input2.txt", "r") as file, open("output2.txt", "w") as out:
    tokens = lexer(file.read())
    out.write(" ".join(tokens))