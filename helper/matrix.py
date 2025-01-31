def transpose_matrix(matrix):
    # Use zip to transpose the rows to columns and convert them to lists
    columns = [list(column) for column in zip(*matrix)]
    return columns