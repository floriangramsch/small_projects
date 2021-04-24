from globals import *
import math

def IX(x, y):
    if 0 <= x < N and 0 <= y < N:
        return x + y * N
    return 0

def lin_solve(b, x, x0, a, c):
    cRecip = 1.0 / c
    for k in range(iter):
        for j in range(N):
            for i in range(N):
                x[IX(i, j)] = (x0[IX(i, j)] + a *(x[IX(i + 1, j)] + x[IX(i - 1, j)] + x[IX(i, j + 1)] + x[IX(i, j - 1)])) * cRecip
    set_bnd(b, x)

def diffuse(b, x, x0, diff, dt):
    a = dt * diff * (N-2) * (N-2)
    lin_solve(b, x, x0, a, 1 + 6 * a) 

def project(velocX, velocY, p, div):
    for j in range(N):
        for i in range(N):
            div[IX(i, j)] = (-0.5 *
                (velocX[IX(i + 1, j)] -
                    velocX[IX(i - 1, j)] +
                    velocY[IX(i, j + 1)] -
                    velocY[IX(i, j - 1)])) / N
            p[IX(i, j)] = 0

    set_bnd(0, div)
    set_bnd(0, p)
    lin_solve(0, p, div, 1, 6)

    for j in range(N):
        for i in range(N):
            velocX[IX(i, j)] -= 0.5 * (p[IX(i + 1, j)] - p[IX(i - 1, j)]) * N
            velocY[IX(i, j)] -= 0.5 * (p[IX(i, j + 1)] - p[IX(i, j - 1)]) * N

    set_bnd(1, velocX)
    set_bnd(2, velocY)

def advect(b, d, d0, velocX, velocY, dt):
    dtx = dt * (N - 2)
    dty = dt * (N - 2)

    Nfloat = N - 2

    for j, jfloat in zip(range(N), range(N)): 
        for i, ifloat in zip(range(N), range(N)):
            tmp1 = dtx * velocX[IX(i, j)]
            tmp2 = dty * velocY[IX(i, j)]
            x = ifloat - tmp1
            y = jfloat - tmp2

            if x < 0.5: x = 0.5
            if (x > Nfloat + 0.5): x = Nfloat + 0.5
            i0 = math.floor(x)
            i1 = i0 + 1.0
            if (y < 0.5): y = 0.5
            if (y > Nfloat + 0.5): y = Nfloat + 0.5
            j0 = math.floor(y)
            j1 = j0 + 1.0

            s1 = x - i0 
            s0 = 1.0 - s1
            t1 = y - j0
            t0 = 1.0 - t1

            i0i = int(i0)
            i1i = int(i1)
            j0i = int(j0)
            j1i = int(j1)

            d[IX(i, j)] = s0 * (t0 * d0[IX(i0i, j0i)] + t1 * d0[IX(i0i, j1i)]) + s1 * (t0 * d0[IX(i1i, j0i)] + t1 * d0[IX(i1i, j1i)])

    set_bnd(b, d)

def set_bnd(b, x):
    for i in range(N):
        x[IX(i, 0)] = b == 2 if -x[IX(i, 1)] else x[IX(i, 1)]
        x[IX(i, N - 1)] = b == 2 if -x[IX(i, N - 2)] else x[IX(i, N - 2)]

    for j in range(N):
        x[IX(0, j)] = b == 1 if -x[IX(1, j)] else x[IX(1, j)]
        x[IX(N - 1, j)] = b == 1 if -x[IX(N - 2, j)] else x[IX(N - 2, j)]


    x[IX(0, 0)] = 0.5 * (x[IX(1, 0)] + x[IX(0, 1)])
    x[IX(0, N - 1)] = 0.5 * (x[IX(1, N - 1)] + x[IX(0, N - 2)])
    x[IX(N - 1, 0)] = 0.5 * (x[IX(N - 2, 0)] + x[IX(N - 1, 1)])
    x[IX(N - 1, N - 1)] = 0.5 * (x[IX(N - 2, N - 1)] + x[IX(N - 1, N - 2)])

