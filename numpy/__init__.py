import math

pi = math.pi

def linspace(start, stop, num):
    if num <= 1:
        return [stop]
    step = (stop - start) / (num - 1)
    return [start + i * step for i in range(num)]

def meshgrid(x, y):
    X = []
    Y = []
    for yi in y:
        X.append(list(x))
        Y.append([yi] * len(x))
    return X, Y

def zeros(shape):
    rows, cols = shape
    return [[0.0 for _ in range(cols)] for _ in range(rows)]
