def leaders(nums):
    ans = []
    stack = []
    for i in range(len(nums)-1, -1, -1):
        while len(stack)>0 and stack[-1] < nums[i]:
            stack.pop()
        if len(stack) == 0:
            ans.append(nums[i])
        stack.append(nums[i])
    print(ans[::-1])
    return ans[::-1]

leaders([1,2,5,3,1,2])