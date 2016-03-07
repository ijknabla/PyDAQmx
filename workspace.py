allchar = set()

with open("NIDAQmx.h") as file:
    for line in file:
        for char in line:
            allchar.add(char)
