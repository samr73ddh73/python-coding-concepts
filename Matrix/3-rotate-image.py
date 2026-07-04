

# Two lines of real logic. Say it out loud as you type: "transpose upper triangle, then reverse rows" — that sentence is your entire plan, no need to think further.
def rotate(matrix, n):
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    for row in matrix:
        row.reverse()
    return matrix