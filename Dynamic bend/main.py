import numpy as np
import matplotlib.pyplot as plt
def transform(l, E, J):
    B = [[12, 6 * l, -12, 6 * l],
         [6 * l, 4 * l ** 2, -6 * l, 2 * l ** 2],
         [-12, -6 * l, 12, -6 * l],
         [6 * l, 2 * l ** 2, -6 * l, 4 * l ** 2]]
    ke_loc = E * J / (l ** 3) * np.array(B)
    return ke_loc


def global_matrix(ster, ke_loc, n_uz, n_el):
    K = np.zeros((2 * n_uz, 2 * n_uz))
    for el in ster:
        for i in range(2):
            for j in range(2):
                K[2 * el[i] - 2, 2 * el[j] - 2] += ke_loc[2 * i, 2 * j]
                K[2 * el[i] - 2, 2 * el[j] - 1] += ke_loc[2 * i, 2 * j + 1]
                K[2 * el[i] - 1, 2 * el[j] - 2] += ke_loc[2 * i + 1, 2 * j]
                K[2 * el[i] - 1, 2 * el[j] - 1] += ke_loc[2 * i + 1, 2 * j + 1]
    return K


def form(l):
    B = [[156, 12 * l, 54, -13 * l],
         [22 * l, 4 * l ** 2, 13 * l, -3 * l ** 2],
         [54, 13 * l, 156, -22 * l],
         [-13 * l, -3 * l ** 2, -22 * l, 4 * l ** 2]]
    return B


def m_loc(B, ro, S, L):
    M_loc = ro * S * L * np.array(B) / 420
    return M_loc


if __name__ == "__main__":
    n_uz = 11
    n_el = 10
    Dt = 10
    dt = 1 / Dt
    time = np.linspace(0, 1, 11)
    Uz = np.linspace(0, 1, 11)

    ster = [[1, 2],
            [2, 3],
            [3, 4],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 8],
            [8, 9],
            [9, 10],
            [10, 11]]

    BC = [1]
    Force_uz = [11]
    F = np.zeros(2 * n_uz)
    E = 2 * 10 ** 11
    ro = 7800
    b = 0.055
    h = 0.1
    t1 = 0.0057
    t2 = 0.0041
    J = (b * h ** 3) / 12 - 2 * (0.5 * (b - t2) * (h - 2 * t1) ** 3) / 12
    S = (b * h) - 2 * (0.5 * (b - t2) * (h - 2 * t1))

    L = 1
    l = L / n_el

    ke_loc = transform(l, E, J)
    K = global_matrix(ster, ke_loc, n_uz, n_el)
    B = form(l)
    me_loc = m_loc(B, ro, S, l)
    M = global_matrix(ster, me_loc, n_uz, n_el)

    # Граничные условия
    K[:, 2 * BC[0] - 2] = 0
    K[:, 2 * BC[0] + 1] = 0
    K[2 * BC[0] - 2, :] = 0
    K[2 * BC[0] + 1, :] = 0

    K[2 * BC[0] - 2, 2 * BC[0] - 2] = 1
    K[2 * BC[0] + 1, 2 * BC[0] + 1] = 1

    M[:, 2 * BC[0] - 2] = 0
    M[:, 2 * BC[0] + 1] = 0
    M[2 * BC[0] - 2, :] = 0
    M[2 * BC[0] + 1, :] = 0

    M[2 * BC[0] - 2, 2 * BC[0] - 2] = 1
    M[2 * BC[0] + 1, 2 * BC[0] + 1] = 1

    u = []
    v = []
    a = []
    # Начальные условия
    u.append(np.zeros((2 * n_uz, 1)))
    v.append(np.zeros((2 * n_uz, 1)))
    a.append(np.zeros((2 * n_uz, 1)))

    uv = np.zeros((2 * n_uz, 1))
    vv = np.zeros((2 * n_uz, 1))

    ff = -100000
    f = ff / (0.5 * Dt)

    betta = 0.25
    gamma = 2 * betta
    for i in range(0, len(time)-1):
        F = np.zeros((2 * n_uz, 1))

        if i <= (len(time) - 1) / 2 -1:
            F[21,0] = f * (i+1)

        uv = u[i][0:22] + dt * v[i] + (0.5 - betta) * dt ** 2 * a[i][0:22]
        vv = v[i][0:22] + (1 - gamma) * dt * a[i][0:22]

        A = np.array(M + betta * (dt ** 2) * np.array(K))
        B = np.array(F - K.dot(uv))

        a.append(np.linalg.solve(A, B))
        v.append(vv + dt * gamma * a[i + 1][0:22])
        u.append(uv + dt ** 2 * betta * a[i + 1][0:22])

    U = np.zeros((11, n_uz))
    V = np.zeros((11, n_uz))
    A = np.zeros((11, n_uz))

    k = 0
    for j in range(0, 11):
        for i in range(0, 11):
            U[k, i] = u[j][i * 2, 0]
            V[k, i] = v[j][i * 2, 0]
            A[k, i] = a[j][i * 2, 0]
        k += 1

    phi = np.linspace(0, 2. * np.pi, 100)
    plt.plot(phi, np.sin(phi))
    plt.plot(phi, np.cos(phi))

    plt.show()
