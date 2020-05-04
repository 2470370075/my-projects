# 二分查找： 也叫折半查找，
#           对于顺序表
#           想要找出一个值在不在一个顺序表中，
#           首先判断这个值是不是中间位置那个，如果是，返回True，
#           如果不是，比它小的话，继续用这种方法查找前面部分，比它大的话，继续用这种方法查找后面部分，
#           直到找到对应数字

#    时间复杂度 log（n）

def binary_serach(l,item):                     # 利用递归，每次查找的都是新建的列表
    n = len(l)
    mid = n // 2
    if n <= 0:
        return False
    if l[mid] == item:
        return True
    elif item > l[mid]:
        return binary_serach(l[mid+1:],item)           # 这里要有renturn，不然找不到的时候返回None，把最后返回的False传递给第一个函数
    elif item < l[mid]:
        return binary_serach(l[:mid],item)


l = [1,3,5,7,8,9]
print(binary_serach(l,3))
print(binary_serach(l,6))



def binary_serach(l,item):
    # 利用循环，不用新建列表，一直在原有列表上操作,通过first和last确定中间值，
    n = len(l)
    first = 0
    last = n                               # last代表长度
    while first <= last:
        print(l[first:last])
        mid = (first + last) // 2          # mid代表第几个为中间值
        if l[mid-1] == item:               # 所以mid-1才是下标，所以l[mid-1]为中间值
            return True
        elif item > l[mid-1]:
            first = mid + 1   #上一次的last正好是这次的last 6
        elif item < l[mid-1]:
            last = mid - 1     #上一次的first正好是这次的first
    return False

l = [1,3,5,7,8,9,12,23,44,]
print(binary_serach(l,3))
print(binary_serach(l,22))
