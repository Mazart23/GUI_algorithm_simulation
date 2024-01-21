'''
GUI Algorithm Simulation
MIT License
Copyright (c) 2024 Artur Mazurkiewicz
'''



import numpy as np
from scipy import signal


class ObiektNieliniowy:

    def __init__(self, typ, *args):
        self.typ = typ
        match self.typ:
            case 'sinus':
                self.amp, self.T, self.przes, self.skl_st = args
            case 'sinus_2':
                self.amp1, self.T1, self.przes1, self.amp2, self.T2, self.przes2, self.skl_st = args
            case 'exp':
                self.amp, self.st_czas, self.skl_st = args

    def ret(self):
        match self.typ:
            case 'sinus':
                return "Nieliniowy", self.typ, self.amp, self.T, self.przes, self.skl_st
            case 'sinus_2':
                return "Nieliniowy", self.typ, self.amp1, self.T1, self.przes1, self.amp2, self.T2, self.przes2, self.skl_st
            case 'exp':
                return "Nieliniowy", self.typ, self.amp, self.st_czas, self.skl_st


class ObiektLiniowy:

    def __init__(self, typ, stopien, b):
        self.typ = typ
        self.stopien = stopien
        self.b = b

    def ret(self):
        return self.typ, self.stopien, self.b


class ObiektDynamiczny:

    def __init__(self, typ, *args):
        self.typ = typ
        self.wsp = args
        match self.typ:
            case 'iner1':
                self.wzm, self.st_czas = args
                self.G = ([self.wzm], [self.st_czas, 1])
            case 'iner2':
                self.wzm, self.st_czas_1, self.st_czas_2 = args
                self.G = ([self.wzm], [self.st_czas_1 * self.st_czas_2, self.st_czas_1 + self.st_czas_2, 1])
            case 'osc':
                self.wzm, self.tlum, self.okr_dr = args
                self.G = ([self.wzm], [self.okr_dr ** 2, 2 * self.tlum * self.okr_dr, 1])

    def ret(self):
        match self.typ:
            case 'iner1':
                return "Dynamiczny", self.typ, self.G, self.wzm, self.st_czas
            case 'iner2':
                return "Dynamiczny", self.typ, self.G, self.wzm, self.st_czas_1, self.st_czas_2
            case 'osc':
                return "Dynamiczny", self.typ, self.G, self.wzm, self.tlum, self.okr_dr


class Parametry(ObiektLiniowy):

    def __init__(self, obkt, stopien_m = 1, N = 100, range_min = 0.0, range_max = 10.0, od_std = 1.0):
        super().__init__(obkt.typ, obkt.stopien, obkt.b)
        self.stopien_m = stopien_m
        self.N = N                     # ilość próbek
        self.range_min = range_min
        self.range_max = range_max
        self.od_std = od_std
        self.sigma = od_std ** 2

        self.krok = abs(self.range_max - self.range_min) / self.N

    def calc(self):
        self.zaklocenie = self.od_std * np.random.randn(self.N)

        self.u = np.linspace(self.range_min, self.range_max, self.N)    # wektor wejść
        self.U = np.zeros((self.stopien+1,self.N))                # macierz wejść - inicjalizacja
        self.U_m = np.zeros((self.stopien_m+1, self.N))

        for st in range(self.stopien+1):
            self.U[-st-1] = self.u ** st      # macierz wejść - konstrukcja

        for st in range(self.stopien_m+1):
            self.U_m[-st-1] = self.u ** st      # macierz wejść - konstrukcja

        self.y_wzorzec = self.b @ self.U
        self.y = self.y_wzorzec + self.zaklocenie

        self.u_aprox = np.linspace(self.range_min, self.range_max, 1000)
        self.U_aprox = np.zeros((self.stopien_m+1, 1000))

        for st in range(self.stopien_m+1):
            self.U_aprox[-st-1] = self.u_aprox ** st      # macierz wejść - konstrukcja

    def ret(self):
        return self.stopien_m, self.N, self.range_min, self.range_max, self.od_std


class ParametryNiestacjo(ObiektLiniowy):

    def __init__(self, obkt, N, range_min, range_max, wymuszenie_typ, od_std):
        super().__init__(obkt.typ, obkt.stopien, obkt.b)
        self.N = N                     # ilość próbek
        self.range_min = range_min
        self.range_max = range_max
        self.wymuszenie_typ = wymuszenie_typ
        self.od_std = od_std
        self.sigma = od_std ** 2

    def calc_niestacjo(self):
        self.zaklocenie = self.od_std * np.random.randn(self.N)
        self.u_wz = np.linspace(self.range_min, self.range_max, self.N)  # wektor wejść
        match self.wymuszenie_typ:
            case 'sekwencyjne':
                self.u = self.u_wz
            case 'losowo-sekwencyjne':
                self.u = np.random.choice(self.u_wz, size=self.N, replace=True)
            case 'losowe':
                self.u =  np.random.rand(self.N) * (self.range_max - self.range_min) + self.range_min
        self.U = np.zeros((self.stopien + 1, self.N))  # macierz wejść - inicjalizacja

        for st in range(self.stopien + 1):
            self.U[-st - 1] = self.u ** st  # macierz wejść - konstrukcja

        self.b_wzorzec = np.zeros((self.N, self.stopien + 1))

        for i, sublst in enumerate(self.b):
            match sublst[0]:
                case 'staly':
                    self.b_wzorzec[:, i] = sublst[1] * np.ones((self.N,))
                case 'liniowy':
                    self.b_wzorzec[:, i] = sublst[1] * self.u_wz + sublst[2] * np.ones((self.N,))
                case 'sinus':
                    self.b_wzorzec[:, i] = sublst[2] * np.sin(2 * np.pi / sublst[3] * self.u_wz + np.pi * sublst[4]) + sublst[1]

        self.y_wzorzec = np.diag(np.matmul(self.b_wzorzec, self.U))
        self.y_last = np.matmul(self.b_wzorzec, self.U)
        self.y = self.y_wzorzec + self.zaklocenie

        self.u_aprox = np.linspace(min(self.u), max(self.u), 1000)
        self.U_aprox = np.zeros((self.stopien + 1, 1000))

        for st in range(self.stopien + 1):
            self.U_aprox[-st - 1] = self.u_aprox ** st  # macierz wejść - konstrukcja

    def ret(self):
        return self.N, self.range_min, self.range_max, self.wymuszenie_typ, self.od_std


class ParametryNieliniowy(ObiektNieliniowy):

    def __init__(self, obkt, N, range_min, range_max, od_std):
        match obkt.typ:
            case 'sinus':
                super().__init__(obkt.typ, obkt.amp, obkt.T, obkt.przes, obkt.skl_st)
            case 'sinus_2':
                super().__init__(obkt.typ, obkt.amp1, obkt.T1, obkt.przes1, obkt.amp2, obkt.T2, obkt.przes2, obkt.skl_st)
            case 'exp':
                super().__init__(obkt.typ, obkt.amp, obkt.st_czas, obkt.skl_st)

        self.N = N
        self.range_min = range_min
        self.range_max = range_max
        self.od_std = od_std
        self.sigma = od_std ** 2

    def calc(self):
        self.zaklocenie = self.od_std *  np.random.randn(self.N)

        self.u = np.linspace(self.range_min, self.range_max, self.N)  # wektor wejść

        match self.typ:
            case 'sinus':
                self.y_wzorzec = self.amp * np.sin(2 * np.pi / self.T * self.u + np.pi * self.przes) + self.skl_st
            case 'sinus_2':
                self.y_wzorzec = self.amp1 * np.sin(2 * np.pi / self.T1 * self.u + np.pi * self.przes1) + \
                                 self.amp2 * np.sin(2 * np.pi / self.T2 * self.u + np.pi * self.przes2) + self.skl_st
            case 'exp':
                self.y_wzorzec = self.amp * np.exp(-1 * self.u / self.st_czas) + self.skl_st

        self.y = self.y_wzorzec + self.zaklocenie

        self.u_aprox = np.linspace(self.range_min, self.range_max, 1000)

    def calc_ret(self):
        return self.u, self.y

    def ret(self):
        return self.N, self.range_min, self.range_max, self.od_std


class ParametryDynamiczny(ObiektDynamiczny):

    def __init__(self, obkt, N, range_max, od_std_w, od_std):
        match obkt.typ:
            case 'iner1':
                super().__init__(obkt.typ, obkt.wzm, obkt.st_czas)
            case 'iner2':
                super().__init__(obkt.typ, obkt.wzm, obkt.st_czas_1, obkt.st_czas_2)
            case 'osc':
                super().__init__(obkt.typ, obkt.wzm, obkt.tlum, obkt.okr_dr)

        self.N = N
        self.range_max = range_max
        self.od_std_w = od_std_w
        self.od_std = od_std
        self.dt = range_max / N

    def calc(self):
        self.u = self.od_std_w * np.random.randn(self.N)
        self.t = np.linspace(0, self.range_max, self.N)  # wektor wejść

        _, self.y, _1 = signal.lsim(self.G, self.u, self.t, interp=True)
        self.y = self.y + self.od_std * np.random.randn(self.N)

    def ret(self):
        return self.N, self.range_max, self.od_std_w, self.od_std


class LS(Parametry):

    def __init__(self, obkt, param):
        super().__init__(obkt, param.stopien_m, param.N, param.range_min, param.range_max, param.od_std)

    def calc(self):
        super().calc()

        self.b_m = np.transpose(np.matmul(np.matmul(np.linalg.inv(np.matmul(self.U_m, np.transpose(self.U_m))), self.U_m), self.y))
        self.y_m = np.matmul(self.b_m, self.U_m)
        self.y_m_aprox = np.matmul(self.b_m, self.U_aprox)

        self.cov = self.sigma * np.linalg.inv(np.matmul(self.U_m, np.transpose(self.U_m)))

        if self.stopien < self.stopien_m:
            self.b = np.hstack((np.zeros((abs(self.stopien - self.stopien_m),)), self.b))
        else:
            self.b_m = np.hstack((np.zeros((abs(self.stopien - self.stopien_m),)), self.b_m))

        return 'LS', self.u, self.y, self.y_m_aprox, self.b_m, self.b, None, self.cov


class RLS(Parametry):

    def __init__(self, obkt, param, alfa, b_0, N_pocz):
        super().__init__(obkt, param.stopien_m, param.N, param.range_min, param.range_max, param.od_std)
        self.alfa = alfa
        self.b_0 = b_0
        self.N_pocz = N_pocz if N_pocz is not None else 0

    def calc(self):
        super().calc()
        if not self.N_pocz:
            self.P = self.alfa * np.eye(self.stopien_m+1)
            self.b_ = np.hstack((np.transpose(self.b_0), np.zeros((self.stopien_m+1, self.N - 1))))
        else:
            self.P = np.linalg.inv(self.U_m[:, :self.N_pocz] @ self.U_m[:, :self.N_pocz].T)
            self.b_LS_pocz = (self.P @ self.U_m[:, :self.N_pocz] @ self.y[:self.N_pocz]).reshape(self.stopien_m+1, 1)
            self.b_ = np.hstack((self.b_LS_pocz * np.ones((self.stopien_m+1, self.N_pocz)), np.zeros((self.stopien_m+1, self.N - self.N_pocz))))

        for i in range(self.N_pocz if self.N_pocz else 1, self.N):
            self.c = np.linalg.inv((self.U_m[:, i].T @ self.P @ self.U_m[:, i] + 1).reshape(1,1))
            self.K = self.P @ self.U_m[:, i] * self.c
            self.b_[:, i] = self.b_[:, i-1] + self.K * (self.y[i] - self.U_m[:, i].T @ self.b_[:, i-1])
            self.P = self.P - (self.K.reshape(self.stopien_m + 1, 1) @ self.U_m[:, i].reshape(1, self.stopien_m + 1) @ self.P)

        self.b_m = self.b_[:,self.N - 1]
        self.y_m = np.matmul(self.b_m, self.U_m)

        self.y_m_aprox = np.matmul(self.b_m, self.U_aprox)

        if self.stopien < self.stopien_m:
            self.b = np.hstack((np.zeros((abs(self.stopien - self.stopien_m),)), self.b))
        else:
            self.b_m = np.hstack((np.zeros((abs(self.stopien - self.stopien_m),)), self.b_m))

        return 'RLS', self.u, self.y, self.y_m_aprox, self.b_m, self.b, None, self.sigma * self.P


class RLSZapominanie(ParametryNiestacjo):
    def __init__(self, obkt, param, alfa, b_0, wsp_zap):
        super().__init__(obkt, param.N, param.range_min, param.range_max, param.wymuszenie_typ, param.od_std)
        self.alfa = alfa
        self.b_0 = b_0
        self.wsp_zap = wsp_zap

    def calc(self):
        super().calc_niestacjo()
        self.P = self.alfa * np.eye(self.stopien+1)
        self.b_ = np.hstack((np.transpose(self.b_0), np.zeros((self.stopien+1, self.N - 1))))

        for i in range(1, self.N):
            self.c = np.linalg.inv((self.U[:, i].T @ self.P @ self.U[:, i] + self.wsp_zap).reshape(1, 1))
            self.K = self.P @ self.U[:, i] * self.c
            self.b_[:, i] = self.b_[:, i-1] + self.K * (self.y[i] - self.U[:, i].T @ self.b_[:, i-1])
            self.P = (self.P - (self.K.reshape(self.stopien + 1, 1) @ self.U[:, i].reshape(1, self.stopien + 1) @ self.P)) / self.wsp_zap

        self.b_m = self.b_[:, self.N - 1]
        self.y_m = np.matmul(self.b_m, self.U)

        self.y_m_aprox = np.matmul(self.b_m, self.U_aprox)

        return 'WRLS', self.u, self.y, self.y_m_aprox, self.b_, self.b, self.b_wzorzec, None


class GLS(Parametry):
    def __init__(self, obkt, param, przek_wart, algorytm):
        super().__init__(obkt, param.stopien_m, param.N, param.range_min, param.range_max, param.od_std)
        self.algorytm = algorytm
        self.przek_wart = przek_wart

        if przek_wart:
            self.korel = 'skorelowane'
        else:
            self.korel = 'nieskorelowane'

        self.macierz = np.diag(np.ones(self.N))
        for sublst in przek_wart:
            self.macierz += sublst[1] * np.diag(np.ones(self.N - sublst[0]), k=sublst[0])
            self.macierz += sublst[1] * np.diag(np.ones(self.N - sublst[0]), k=-sublst[0])

    def calc(self):
        self.zaklocenie = np.random.default_rng().multivariate_normal(np.zeros(len(self.macierz), ), self.sigma * self.macierz, method='cholesky').flatten()

        self.u = np.linspace(self.range_min, self.range_max, self.N)  # wektor wejść
        self.U = np.zeros((self.stopien + 1, self.N))  # macierz wejść - inicjalizacja
        self.U_m = np.zeros((self.stopien_m + 1, self.N))

        for st in range(self.stopien + 1):
            self.U[-st - 1] = self.u ** st  # macierz wejść - konstrukcja

        for st in range(self.stopien_m + 1):
            self.U_m[-st - 1] = self.u ** st  # macierz wejść - konstrukcja

        self.y_wzorzec = np.matmul(self.b, self.U)
        self.y = self.y_wzorzec + self.zaklocenie

        self.u_aprox = np.linspace(self.range_min, self.range_max, 1000)
        self.U_aprox = np.zeros((self.stopien_m + 1, 1000))

        for st in range(self.stopien_m + 1):
            self.U_aprox[-st - 1] = self.u_aprox ** st  # macierz wejść - konstrukcja

        if self.algorytm == 'GLS':
            self.b_m = np.linalg.inv(self.U_m @ np.linalg.inv(self.macierz) @ self.U_m.T) @ self.U_m @ np.linalg.inv(
                self.macierz) @ self.y

            self.y_m = self.b_m @ self.U_m

            self.y_m_aprox = self.b_m @ self.U_aprox

            self.cov = self.sigma * np.linalg.inv(self.U_m @ np.linalg.inv(self.macierz) @ self.U_m.T)

            if self.stopien < self.stopien_m:
                self.b = np.hstack((np.zeros((abs(self.stopien - self.stopien_m),)), self.b))
            else:
                self.b_m = np.hstack((np.zeros((abs(self.stopien - self.stopien_m),)), self.b_m))

            return 'GLS', self.u, self.y, self.y_m_aprox, self.b_m, self.b, None, self.cov

        elif self.algorytm == 'LS':
            self.b_m = np.linalg.inv(self.U_m @ self.U_m.T) @ self.U_m @ self.y
            self.y_m = self.b_m @ self.U_m

            self.y_m_aprox = self.b_m @ self.U_aprox

            self.cov = self.sigma * np.linalg.inv(self.U_m @ self.U_m.T) @ self.U_m @ self.macierz @ self.U_m.T @ np.linalg.inv(self.U_m @ self.U_m.T)

            if self.stopien < self.stopien_m:
                self.b = np.hstack((np.zeros((abs(self.stopien - self.stopien_m),)), self.b))
            else:
                self.b_m = np.hstack((np.zeros((abs(self.stopien - self.stopien_m),)), self.b_m))

            return 'GLS', self.u, self.y, self.y_m_aprox, self.b_m, self.b, None, self.cov

    def check(self):
        try:
            np.linalg.cholesky(self.macierz)
            return True
        except:
            return False

    def positive_matrix(self):
        while self.check() == False:
            for i, sublst in enumerate(self.przek_wart):
                if abs(sublst[1]) > 1:
                    diff = self.przek_wart[i][1] - np.sign(sublst[1]) * 0.4
                    self.przek_wart[i][1] = np.sign(sublst[1]) * 0.4
                else:
                    diff = self.przek_wart[i][1] / 2
                    self.przek_wart[i][1] -= diff

                self.macierz -= diff * np.diag(np.ones(self.N - sublst[0]), k=sublst[0])
                self.macierz -= diff * np.diag(np.ones(self.N - sublst[0]), k=-sublst[0])
        return self.przek_wart[:]


class NLS(ParametryNieliniowy):
    def __init__(self, obkt, param, iter, *args):
        super().__init__(obkt, param.N, param.range_min, param.range_max, param.od_std)
        self.iter = iter
        self.ob_param = param
        match obkt.typ:
            case 'sinus':
                self.amp_0, self.T_0, self.przes_0, self.skl_st_0 = args
            case 'sinus_2':
                self.amp1_0, self.T1_0, self.przes1_0, self.amp2_0, self.T2_0, self.przes2_0, self.skl_st_0 = args
            case 'exp':
                self.amp_0, self.st_czas_0, self.skl_st_0 = args

    def calc(self):
        self.u = self.ob_param.u
        self.y = self.ob_param.y

        match self.typ:
            case 'sinus':
                self.b_ = np.hstack((np.array([self.amp_0, self.T_0, self.przes_0, self.skl_st_0]).reshape(4, 1), np.zeros((4, self.iter))))

                self.F = np.zeros((self.N, 4))

                for i in range(self.iter):
                    self.F = np.hstack(((np.sin(2 * np.pi / self.b_[1, i] * self.u + np.pi * self.b_[2, i]).reshape(self.N, 1)),
                                        (-2 * np.pi * self.b_[0, i] * self.u * np.cos(self.b_[2, i] + 2 * np.pi * self.u / self.b_[1, i]) / self.b_[1, i] ** 2).reshape(self.N,1),
                                        (self.b_[0, i] * np.cos(self.b_[2, i] + 2 * np.pi * self.u / self.b_[1, i])).reshape(self.N,1),
                                        np.ones((self.N, 1))))
                    self.b_[:, i + 1] = self.b_[:, i] + (np.linalg.inv(self.F.T @ self.F) @ self.F.T @ (self.y - (self.b_[0, i] * np.sin(2 * np.pi / self.b_[1, i] * (self.u + self.b_[2, i])) + self.b_[3, i])))

                self.y_aprox = self.b_[0, self.iter] * np.sin(2 * np.pi / self.b_[1, self.iter] * (np.linspace(self.range_min, self.range_max, 1000) + self.b_[2, self.iter])) + self.b_[3, self.iter]

                return 'NLS', self.u, self.y, self.y_aprox, self.b_[:, -1], \
                    np.array([self.amp, self.T, self.przes, self.skl_st]), None, None

            case 'sinus_2':
                self.b_ = np.hstack((np.array([self.amp1_0, self.T1_0, self.przes1_0, self.amp2_0, self.T2_0, self.przes2_0, self.skl_st_0]).reshape(7, 1), np.zeros((7, self.iter))))

                self.F = np.zeros((self.N, 7))

                for i in range(self.iter):
                    self.F = np.hstack(((np.sin(2 * np.pi / self.b_[1, i] * self.u + np.pi * self.b_[2, i]).reshape(self.N, 1)),
                                        (-2 * np.pi * self.b_[0, i] * self.u * np.cos(self.b_[2, i] + 2 * np.pi * self.u / self.b_[1, i]) / self.b_[1, i] ** 2).reshape(self.N,1),
                                        (self.b_[0, i] * np.cos(self.b_[2, i] + 2 * np.pi * self.u / self.b_[1, i])).reshape(self.N,1),
                                        (np.sin(2 * np.pi / self.b_[4, i] * self.u + np.pi * self.b_[5, i]).reshape(self.N, 1)),
                                        (-2 * np.pi * self.b_[3, i] * self.u * np.cos(self.b_[5, i] + 2 * np.pi * self.u / self.b_[4, i]) / self.b_[4, i] ** 2).reshape(self.N, 1),
                                        (self.b_[3, i] * np.cos(self.b_[5, i] + 2 * np.pi * self.u / self.b_[4, i])).reshape(self.N, 1),
                                        np.ones((self.N, 1))))
                    self.b_[:, i + 1] = self.b_[:, i] + (np.linalg.inv(self.F.T @ self.F) @ self.F.T @ (self.y - (self.b_[0, i] * np.sin(2 * np.pi / self.b_[1, i] * (self.u + self.b_[2, i])) + self.b_[3, i] * np.sin(2 * np.pi / self.b_[4, i] * (self.u + self.b_[5, i])) + self.b_[6, i])))

                self.y_aprox = self.b_[0, self.iter] * np.sin(2 * np.pi / self.b_[1, self.iter] * (np.linspace(self.range_min, self.range_max, 1000) + self.b_[2, self.iter])) + self.b_[3, self.iter] * np.sin(2 * np.pi / self.b_[4, self.iter] * (np.linspace(self.range_min, self.range_max, 1000) + self.b_[5, self.iter])) + self.b_[6, self.iter]

                return 'NLS', self.u, self.y, self.y_aprox, self.b_[:, -1], \
                    np.array([self.amp1, self.T1, self.przes1, self.amp2, self.T2, self.przes2, self.skl_st]), None, None

            case 'exp':
                self.b_ = np.hstack((np.array([self.amp_0, self.st_czas_0, self.skl_st_0]).reshape(3, 1), np.zeros((3, self.iter))))

                self.F = np.zeros((self.N, 7))

                for i in range(self.iter):
                    self.F = np.hstack(((np.exp(-1 * self.u / self.b_[1, i])).reshape(self.N, 1),
                                        (self.b_[0, i] * self.u * np.exp(-1 * self.u / self.b_[1, i]) / self.b_[1, i] ** 2).reshape(self.N, 1),
                                        np.ones((self.N, 1))))
                    self.b_[:, i + 1] = self.b_[:, i] + (np.linalg.inv(self.F.T @ self.F) @ self.F.T @ (self.y - (self.b_[0, i] * np.exp((-1) * self.u / self.b_[1, i]) + self.b_[2, i])))

                self.y_aprox = self.b_[0, self.iter] * np.exp((-1) * np.linspace(self.range_min, self.range_max, 1000) / self.b_[1, self.iter]) + self.b_[2, self.iter]
                return 'NLS', self.u, self.y, self.y_aprox, self.b_[:, -1], \
                    np.array([self.amp, self.st_czas, self.skl_st]), None, None


class Korel(ParametryDynamiczny):
    def __init__(self, obkt, param):
        super().__init__(obkt, param.N, param.range_max, param.od_std_w, param.od_std)

    def calc(self):
        super().calc()
        self.nmax = int(0.1 * self.N)
        self.tau = np.arange(0, 0.1 * self.range_max, self.dt)

        self.Ruu = np.zeros(self.nmax)
        self.Ryu = np.zeros(self.nmax)
        self.Ruy = np.zeros(self.nmax)

        for m in range(1, self.nmax + 1):
            for ii in range(self.N - m):
                self.Ruu[m - 1] += self.u[ii] * self.u[ii + m - 1]
                self.Ryu[m - 1] += self.y[ii] * self.u[ii + m - 1]
                self.Ruy[m - 1] += self.u[ii] * self.y[ii + m - 1]

            self.Ruu[m - 1] *= self.dt / (self.N - m)
            self.Ryu[m - 1] *= self.dt / (self.N - m)
            self.Ruy[m - 1] *= self.dt / (self.N - m)

        self.Tau = np.concatenate((-self.tau[:0:-1], self.tau))
        self.RUU = np.concatenate((self.Ruu[:0:-1], self.Ruu))
        self.RYU = np.concatenate((self.Ryu[:0:-1], self.Ruy))

        self.Rwl = self.RUU[:self.nmax].reshape((self.nmax, 1))
        for ii in range(1, self.nmax):
            self.Rwl = np.hstack((self.RUU[ii:ii + self.nmax].reshape((self.nmax, 1)), self.Rwl))

        self.k = self.Ruy @ np.linalg.inv(self.Rwl) / self.dt
        _, self.kwzr = signal.impulse(self.G, T=self.tau)
        return 'korelacyjny', self.tau, self.kwzr, self.k, None, self.wsp, None, None
