def increasingOrder(n):
    final = []
    helper(0, n, '', final)
    return final
def helper(start, n, numStr, final):
    if len(numStr) >= n:
        final.append(int(numStr))
        return
    choices = [ str(i) for i in range(start+1, 10) ]
    for c in choices:
        numStr = numStr + c
        helper(int(c), n, numStr, final)
        numStr = numStr[:len(numStr)-1]

print(increasingOrder(3))