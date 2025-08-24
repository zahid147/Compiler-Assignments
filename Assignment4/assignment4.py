braces = {')': '(', '}': '{', ']': '['}
bracket_messages = []
variable_messages = []

li = []
variables = set()

with open("input4.txt", 'r') as file:
    for n, line in enumerate(file, start=1):
        for ch in line:
            if ch in "({[":
                li.append((ch, n))
            elif ch in braces:
                if li and braces[ch] != li[-1][0]:
                    bracket_messages.append(f"Unmatched '{ch}' on line {n}")
                else:
                    if not li:
                        bracket_messages.append(f"Unmatched '{ch}' on line {n}")
                    else:
                        li.pop()

        tokens = line.strip().split()
        for i, word in enumerate(tokens):
            if word in {"int", "float", "char", "double"}:
                if i + 1 < len(tokens):
                    var = tokens[i + 1].rstrip(';')
                    value = (word, var)
                    if value in variables:
                        variable_messages.append(f"Duplicate variable {value} on line {n}")
                    else:
                        variables.add(value)

for ch, line_num in li:
    bracket_messages.append(f"Unmatched '{ch}' on line {line_num}")

with open("output4.txt", "w") as file:
    if not bracket_messages:
        file.write("Brackets are balanced")
    else:
        file.write("\n".join(bracket_messages))

    file.write("\n")

    if not variable_messages:
        file.write("No duplicate variable declared!")
    else:
        file.write("\n".join(variable_messages))
