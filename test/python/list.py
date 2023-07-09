newlist = [1, 2, 3, 4, 5]
newlist.append(6)
newlist.append(7)
newlist.append(8)

for item in newlist:
    print(item)

print(newlist[0])
print(newlist[1])

newlist.sort()
newlist.reverse()