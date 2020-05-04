# 归并：拆分合并

# 归并排序： 先把序列两两拆分，拆到最后只有一个元素的时候，停止拆分，开始合并，两两合并，到最后完成排序。
#           合并的时候，上一次拆分出来的两个子序列，左面的第一个元素下标为left，右面的第一个元素下标为high，
#           left和high做比较，小的为合并和序列的第一个，放入新序列后，left小则left加1，right小则right加一，
#           继续比较，left或right到达末尾后停止，将排好的序列返回。


#   额外开销了一个新的列表
def merge_sort(l):
    n = len(l)
    if n == 1:
        return l                                      # 返回的是合并后的序列
    mid = n // 2
    left_list = merge_sort(l[:mid])                    # l[:mid]代表的是拆分 left_list是合并后的小序列
    right_list = merge_sort(l[mid:])

    result = []
    left,right = 0,0
    while left < len(left_list) and right < len(right_list):
        if left_list[left] <= right_list[right]:      # 如果有了等于号就是稳定的
            result.append(left_list[left])
            left += 1
        else:
            result.append(right_list[right])
            right += 1
    result += left_list[left:]
    result += right_list[right:]
    return result                                   # 返回的是合并后的序列

l = [1,4,6,2,7,2,9]

print(merge_sort(l))


def merge(l):
    n = len(l)
    mid = n // 2
    if n == 1:
        return l
    left_list = merge(l[:mid])
    right_list = merge(l[mid:])
    left,right = 0,0
    result = []
    while left < len(left_list) and right < len(right_list):
        if left_list[left] < right_list[right]:
            result.append(left_list[left])
            left += 1
        else:
            result.append(right_list[right])
            right += 1
    result += left_list[left:]
    result += right_list[right:]
    return result

l = [1,4,6,2,7,2,9]

print(merge(l))











