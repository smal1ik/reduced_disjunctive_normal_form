import math
import os
from itertools import combinations

import numpy as np



def outputMatrix(matrix):
    for elem in matrix:
        print(elem)


def buildMatrix(matrix):
    l = len(matrix[0]) - 1
    pointer = len(matrix[0]) - 2
    n = 1
    while l != 0:

        b = True
        k = 0

        for elem in matrix:
            if b:
                elem[pointer] = 0
                k += 1
                if k == n:
                    b = False
                    k = 0
            else:
                elem[pointer] = 1
                k += 1
                if k == n:
                    b = True
                    k = 0

        pointer -= 1
        l -= 1
        n = n * 2


def countOne(line):
    c = 0

    if type(line) == str:
        n = len(line)
    else:
        n = len(line) - 1

    for elem in line[0:n]:
        if elem != '-':
            if int(elem) == 1:
                c += 1
        elif elem == '-':
            c += 1
    return c

def count(line):
    c = 0

    for elem in line:
        if elem != '-':
            if int(elem) == 1:
                c += 1
    return c


def countMinus(line):
    c = 0
    for elem in line:
        if elem == '-':
            c += 1
    return c


def firstStep(matrix, nx):
    matrix1 = [{} for i in range(nx + 1)]
    counter = countOne(f)

    while counter != 0:

        for elem in matrix:
            if elem[-1] == 1:
                inpt = "".join(str(v) for v in elem[0:len(elem) - 1])
                matrix1[countOne(elem)].update({inpt: 0})

        counter -= 1

    return matrix1


def count_nonzero(m):
    count = 0
    for elem in m:
        if elem:
            count += 1
    return count

def ok(a, b):
    for i in range(len(a)):
        if(b[i] == '-'):
            continue
        elif (a[i] == b[i]):
            continue
        else:
            return False
    return True

def getL(m):
    c = 0
    for elem in m:
        for sym in elem:
            if sym != '-':
                c += 1
    return c


# ================================================================================================================

# f = "00101011011001101010111011101000"
# f = "01111001111000010101100011100011"
# f = "10010101111010001001011110101100"
# f = "1101101011011100"
# f = "10010101111010001001011110101100"
f = "11011100010111100101111001111010"

nx = int(math.log2(len(f)))
matrix = [[0 for i in range(nx)] + [int(f[i])] for i in range(2 ** nx)]

buildMatrix(matrix)
d = firstStep(matrix, nx)
outputMatrix(d)
sett = firstStep(matrix, nx)

result = [{} for i in range(nx + 1)]
while count_nonzero(d) != 0:

    checker = True
    for elem in d[::-1]:
        if elem:
            k = countOne(list(elem.keys())[0]) - countMinus(list(elem.keys())[0])
            break

    matrix1 = [{} for i in range(k)]

    for i, elem in enumerate(d):

        # Если словарь пустой, пропускаем
        if not elem:
            continue

        # берем все элементы (00010)
        for kit in elem:
            # Ищем индексы где стоит 1 и -
            arrayIndex = []
            arrayMinus = []
            b = True
            for index, number in enumerate(kit):
                if number == '1':
                    arrayIndex.append(index)
                if number == '-':
                    arrayMinus.append(index)
            if len(d)-1 == i:
                break
            # берем все элементы где на еденицу больше 1 (00011)
            for kit1 in d[i + 1]:
                # Ищем индексы где стоит 1 и -
                arrayIndex1 = []
                arrayMinus1 = []
                for index, number in enumerate(kit1):
                    if number == '1':
                        arrayIndex1.append(index)
                    if number == '-':
                        arrayMinus1.append(index)

                # Находим разницу между массивами с индексами и масивами с минусами, должны получить индекс - ;[0,1] - [0] = [1]
                index = list(set(arrayIndex1) - set(arrayIndex))
                minus = list(set(arrayMinus1) - set(arrayMinus))
                if len(index) == 1 and len(minus) == 0:
                    # Если индекс найден, то добавляем в новый словарь новую последовательность с - на месте индекса
                    b = False
                    k = countOne(kit1) - countMinus(kit1)
                    matrix1[k - 1].update({kit1[0:index[0]] + "-" + kit1[index[0] + 1:]: 0})
                    d[i].update({kit: 1})
                    d[i+1].update({kit1: 1})
                    # print(kit + " -> " + kit1 + " -> " +kit1[0:index[0]] + "-" + kit1[index[0]+1:] +  " index:" + str(index) + " " + str(minus))
                    # if kit == '01001':
                    #     print(d[i].get(kit))
    for e in d:
        if e:
            for (k, v) in (e.items()):
                if v == 0:
                    result[countOne(k)].update({k: 0})

    # print(print("==========================iteration================================="))
    # outputMatrix(result)



    d = matrix1.copy()

# print("==========================result=================================")
# outputMatrix(result)

d = []
for elem in result:
    d.append(elem.copy())

for n, elem in enumerate(result):
    for i, kit in enumerate(elem):
        for j, kit1 in enumerate(elem):
            if (i == j or i > j):
                continue

            arrayIndex = []
            arrayIndex1 = []
            arrayMinus = []
            arrayMinus1 = []
            for index, number in enumerate(kit):
                if number == '1':
                    arrayIndex.append(index)
                if number == '-':
                    arrayIndex.append(index)
                    arrayMinus.append(index)
            for index, number in enumerate(kit1):
                if number == '1':
                    arrayIndex1.append(index)
                if number == '-':
                    arrayIndex1.append(index)
                    arrayMinus1.append(index)
            index = list(set(arrayIndex1) - set(arrayIndex))
            minus = list(set(arrayMinus1) - set(arrayMinus))
            # print(kit + " and " + kit1 + " " + str(index))
            if len(index) == 0 and not (countMinus(kit) == countMinus(kit1)) and arrayMinus == arrayMinus1:

                if countMinus(kit) < countMinus(kit1) and not d[n].get(kit) == None:
                    d[n].pop(kit)
                elif countMinus(kit) > countMinus(kit1) and not d[n].get(kit) == None:
                    d[n].pop(kit1)

# print("==========================final=================================")
# outputMatrix(d)





result = []
for elem in d:
    if elem:
        for (k, v) in (elem.items()):
            result.append(k)

# print(k)
# print(result)
# print(sett)
table = {}
dic = {}

table = []
for elem in sett:
    for elem1 in elem.keys():
        table.append(elem1)


minL = 10000
minV = []
for i in range(0,len(result)):
    temp = list(combinations(result, i))

    for elem1 in temp:
        check = True
        for elem in table:
            check1 = False
            for kit in elem1:
                if ok(elem, kit):
                    check1 = True
                    break

            if not check1:
                check = False
                break

        if check:
            if(getL(elem1) < minL):
                minL = getL(elem1)
                minV = elem1

result = []
for elem in minV:
    result.append(elem)

# for elem in result:
#     dic.update({elem: 0})
#
# for elem in sett:
#     for elem1 in elem:
#         table.update({elem1 : dic.copy()})
#
# for k,v in table.items():
#     for key in v.keys():
#         if (ok(k,key)):
#             v[key] = 1
#
# for elem,k in table.items(): print(elem + " " + str(k))
#
# result = []
# coatings = []
# while len(coatings) != len(table):
#     min = 100000
#     for k,v in table.items():
#         c = 0
#         if not k in coatings:
#             for key, values in v.items():
#                 c = np.sum(list(v.values()))
#                 if c == 1:
#                     tmp = k
#                     break
#                 if c < min:
#                     min = c
#                     tmp = k
#                     # print("====================")
#                     # print(tmp)
#
#     maxSum = 0
#     tmp1= ''
#     for key, value in table.get(tmp).items():
#         sum = 0
#         if value == 1:
#             for key1, value1 in table.items():
#                 sum += value1.get(key)
#         if sum > maxSum:
#             maxSum = sum
#             tmp1 = key
#     # print(tmp)
#     # print(tmp1)
#     # if tmp1 == '0--01':
#     #     print("===========================")
#     if not tmp in coatings:
#         result.append(tmp1)
#     for k, v in table.items():
#         if v.get(tmp1) == 1:
#             if not k in coatings:
#                 coatings.append(k)
#             # print(k + " покравыает " + tmp1)
#
# print("--------------------------------------------------------------------------------------")
# print(coatings)
# print("--------------------------------------------------------------------------------------")

print(result)
print("=======================================result==========================================")
lines = []
for elem in result:
    line = ""
    for i,c in enumerate(elem):
        if c == '-':
            continue
        if c ==  '0':
            if line:
                line = "(" + line + "&" + f"(!{i+1})" + ")"
            else:
                line = f"(!{i+1})"
        if c == '1':
            if line:
                line = "(" + line + "&" + f"{i+1}" + ")"
            else:
                line = f"{i+1}"
    print(line)
    lines.append(line)

finish = ""
for line in lines:
    if finish:
        finish = "(" + finish + "|" + line + ")"
    else:
        finish = line


print("")
print(finish)

with open("input.txt", "w",encoding='utf-8') as f:
    f.write(finish)
    f.close()
os.system('"prff_1.exe"')