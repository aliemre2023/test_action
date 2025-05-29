def max_array(arr):
    maxi = -1
    for i in range(len(arr)):
        maxi = max(maxi, arr[i])

    return maxi

def min_array(arr):
    mini = 100
    for i in range(len(arr)):
        mini = min(maxi, arr[i])

    return mini
