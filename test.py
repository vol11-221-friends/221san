import csv
import pprint
import numpy as np

with open('ProLanguages.csv',encoding = "utf-8-sig") as f:
    reader = csv.reader(f)
    l = [row for row in reader]

words = ['C', 'みかん', 'python', 'トマト', 'java', 'レタス', 'りんご']

result = []
for i in range(len(l)):
    for j in range(len(words)):
        if words[j].lower() == l[i][0].lower():
            result.append(l[i])

final = []
for i in range(len(result)):
    temp = result[i]
    temp.pop(0)
    final.append(temp)


print(result)
print(final)