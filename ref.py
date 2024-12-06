a = str(input("First text: "))
list = []
b = str(input("Second text: "))
list2 = []
for i in range(len(a)):
    list.append(a[i])
for i in range(len(b)):
    list2.append(b[i])
print(list)
print(list)

for i in range(len(list)):
    for j in range (len(list2)):
        if list[i] == list2[j]:
            print("good")
        else:
            print("not anagram")
        
