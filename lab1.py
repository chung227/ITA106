# =========================
# LAB 1 - DO PHUC TAP BIG-O
# =========================

# -------------------------
# BAI 1
# -------------------------

# Snippet 1
def snippet_1(n):
    total = 0

    for i in range(n):
        total = total + 1

    return total

# Snippet 2
def snippet_2(n):
    count = 0

    for i in range(n):
        for j in range(n):
            count += 1

    return count

# Snippet 3
def snippet_3(n):
    steps = 0

    while n > 0:
        n = n // 2
        steps += 1

    return steps


# Snippet 4
def constant_work():
    x = 1
    y = 2
    z = x + y

    return z


def snippet_4(n):
    for i in range(n):
        constant_work()

# -------------------------
# BAI 2
# -------------------------

# Snippet 5
def snippet_5(n):
    total = 0

    for i in range(n):
        for j in range(i):
            total += 1

    return total




# Snippet 6
def snippet_6(n):
    k = 1
    total = 0

    while k < n:
        for i in range(n):
            total += 1

        k = k * 2

    return total



# Snippet 7
def snippet_7(arr):
    count = 0

    for x in arr:
        if x in arr:
            count += 1

    return count



# Snippet 8
def snippet_8(arr):
    s = set(arr)

    count = 0

    for x in arr:
        if x in s:
            count += 1

    return count




# -------------------------
# BAI 3
# -------------------------


def two_sum_quadratic(arr, target):
    n = len(arr)

    for i in range(n):
        for j in range(i + 1, n):

            if arr[i] + arr[j] == target:
                return (i, j)

    return None





# PHIEN BAN O(n)
def two_sum_linear(arr, target):
    seen = {}

    for i in range(len(arr)):

        complement = target - arr[i]

        # Kiểm tra complement đã xuất hiện chưa
        if complement in seen:
            return (seen[complement], i)

        # Lưu giá trị hiện tại
        seen[arr[i]] = i

    return None


# Độ phức tạp: O(n)
# Giải thích: chỉ duyệt mảng 1 lần.


# -------------------------
# TEST CHUONG TRINH
# -------------------------

import time
import random

arr = list(range(100000))
random.shuffle(arr)

target = arr[123] + arr[9876]

# Test O(n)
start = time.time()

result = two_sum_linear(arr, target)

end = time.time()

print("Ket qua O(n):", result)
print("Thoi gian O(n):", end - start)

# Test O(n^2) voi mang nho
small_arr = arr[:5000]

small_target = small_arr[10] + small_arr[100]

start = time.time()

result = two_sum_quadratic(small_arr, small_target)

end = time.time()

print("Ket qua O(n^2):", result)
print("Thoi gian O(n^2):", end - start)