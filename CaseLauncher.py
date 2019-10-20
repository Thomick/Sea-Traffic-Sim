ByName = False
# Possible name : Evenly_Opposite , RandomSpawner
name = "Evenly_Opposite"

showAll = False
nbCase = 4
caseIndex = 4

if ByName:
    exec(open(f"Cases/" + name + ".py").read())
else:
    if showAll:
        for i in range(1, nbCase + 1):
            exec(open(f"Cases/Case{i}.py").read())
    else:
        exec(open(f"Cases/Case{caseIndex}.py").read())
