def permutation(str, i, tempStr, result):
    if i >= len(str):
        result.append(''.join(tempStr))
        return
    # for j in str:
    for j in range(len(str)):
        if j in visited:
            continue
        tempStr.append(str[j])
        visited.add(j)
        permutation(str, i+1, tempStr, result)
        tempStr.pop()
        visited.remove(j)
    return result

visited = set()
print(permutation('abbc', 0, [], []))