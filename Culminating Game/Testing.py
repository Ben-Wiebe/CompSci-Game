file = open("listTest.txt", "r")
contents = file.readlines()
file.close()

maps = []
currentMap = []
for i in contents:
    if "@" in i:    maps.append(currentMap); currentMap = []
    i = i.translate({ord("\n"): None})
    i = i.translate({ord("@") : None})
    currentMap.append(list(i))
    
    
#contents = [list(i) for i in contents]
#contents = [[int(y) if y != "\n" else 1 for x in contents[y]] for y in range(0,32)]
print(maps)
print("\n\n".join("\n".join("".join(str(y) for y in x) for x in z) for z in maps))
