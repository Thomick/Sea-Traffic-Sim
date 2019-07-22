showAll = False
nbCase = 4
caseIndex = 1

if showAll:
    for i in range(1, nbCase + 1):
        exec(open(f"Cases/Case{i}.py").read())
else:
    exec(open(f"Cases/Case{caseIndex}.py").read())
