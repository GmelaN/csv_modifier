with open("./a", 'r', encoding="UTF8") as f:
    a = list(f.readlines())

with open("./b", 'r', encoding = "UTF8") as f:
    b = list(f.readlines())


for i in range(len(a)):
    if a[i] != b[i]: print(i)
