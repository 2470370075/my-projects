
#最优时间复杂度  算法完成最少需要多少步骤
#最坏时间复杂度  算法完成最多需要多少步骤           一般所说的时间复杂度是说的这个
#平均时间复杂度  算法完成平均需要多少步骤






# 枚举法       找出 a + b + c == 1000 并且 a方 + b方 == c方的a，b，c:
def t1():
    for a in range(1000):
        for b in range(1000):
            for c in range(1000):
                if a + b + c == 1000 and a**2 + b**2 == c**2:
                    pass

from timeit import Timer

timer1 = Timer('t1()','from __main__ import t1')
print(timer1.timeit(1000))


def t2():
    l = []
    for i in range(10000):
        l.insert(0,i)

timer1 = Timer('t2()','from __main__ import t2')
print(timer1.timeit(1000))

