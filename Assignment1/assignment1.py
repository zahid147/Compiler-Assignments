with open("input1.c", 'r') as infile, open("output1.txt", 'w') as outfile:
    tmp = True
    for line in infile:
        if len(line) > 1 and line[0] == line[1] == '/': continue
        if len(line) > 1 and line[0] == '/' and line[1] == '*': tmp = False
        if tmp:
            outfile.write(line[:-1])
        if len(line) > 1 and line[0] == '*' and line[1] == '/': tmp = True