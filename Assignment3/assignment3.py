from collections import defaultdict

class SymbolTable:
    def __init__(self):
        self.rows = []
        self.auto_id = 0

    def insert(self, name, idtype, datatype, scope, value=None):
        self.auto_id += 1
        entry = {
            "SlNo": self.auto_id,
            "Name": name,
            "Id": idtype,
            "Type": datatype,
            "Scope": scope,
            "Value": value
        }
        self.rows.append(entry)

    def update(self, name, field, new_value, scope=None):
        for row in self.rows:
            if row["Name"] == name and (scope is None or row["Scope"] == scope):
                row[field] = new_value
                return True
        return False

    def display(self, file):
        print("Sl.No  Name   Id     Type     Scope     Value", file=file)
        for r in self.rows:
            print(f"{r['SlNo']:<6} {r['Name']:<6} {r['Id']:<6} {r['Type']:<8} {r['Scope']:<8} {r['Value'] or ''}", file=file)


def read_tokens(filename):
    tokens = []
    with open(filename) as f:
        content = f.read()
    token = ""
    inside_brackets = False
    for ch in content:
        if ch == "[":
            inside_brackets = True
            token = ""
        elif ch == "]":
            inside_brackets = False
            tokens.append(token.strip())
        elif inside_brackets:
            token += ch
    return tokens


def parse_tokens(token_list):
    st = SymbolTable()
    scope_stack = ["global"]
    current_func = None
    declared = defaultdict(set)

    def cur_scope():
        return scope_stack[-1]

    i = 0
    while i < len(token_list):
        tok = token_list[i]

        if tok == "{":
            scope_stack.append(current_func or cur_scope())
            i += 1
            continue
        if tok == "}":
            scope_stack.pop()
            if not scope_stack:
                scope_stack = ["global"]
            if current_func and cur_scope() == "global":
                current_func = None
            i += 1
            continue

        if tok in {"int", "float", "double", "char", "void"}:
            dtype = tok
            if i + 1 < len(token_list) and token_list[i+1].startswith("id "):
                name = token_list[i+1].split()[1]

                if i + 2 < len(token_list) and token_list[i+2] == "(":
                    st.insert(name, "func", dtype, "global")
                    current_func = name
                    i += 2

                    while i + 1 < len(token_list) and token_list[i+1] != ")":
                        i += 1
                    i += 1
                else:
                    value = None
                    if i + 2 < len(token_list) and token_list[i+2] == "=":
                        if i + 3 < len(token_list):
                            value = token_list[i+3]
                    st.insert(name, "var", dtype, cur_scope(), value)
                    i += 2
            else:
                i += 1
            continue

        if tok.startswith("id "):
            name = tok.split()[1]
            if i + 1 < len(token_list) and token_list[i+1] == "=":
                valtok = token_list[i+2] if i + 2 < len(token_list) else None
                if valtok and not valtok.startswith("id"):
                    st.update(name, "Value", valtok, scope=cur_scope())
            i += 1
            continue

        i += 1

    return st


if __name__ == "__main__":
    tokens = read_tokens("input3.txt")
    st = parse_tokens(tokens)
    with open("output3.txt", "w") as fout:
        st.display(fout)
