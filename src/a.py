def max_array(arr):
    maxi = -1
    for i in range(len(arr)):
        maxi = max(maxi, arr[i])

    return maxi
