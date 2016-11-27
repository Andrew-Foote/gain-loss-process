import random
from matplotlib import pyplot as plot

class DiscreteGainLossProcess:
    def __init__(self, n, A, X_0, t):
        self.n = n
        self.A = A
        self.X_0 = X_0
        self.t = t

    def run(self, remember=False, verbose=False):
        X = list(self.X_0)
        if remember:
            Y = [[x] for x in X]
        for i in range(self.t):
            if verbose:
                print("---")
                print("The current time is", repr(i) + ".")
                print("The current state is", "".join(str(1 if x else 0) for x in X) + ".")
            for j in range(self.n):
                if verbose:
                    print("Will trait", j, "change? The probability that it will is", str(self.A[j][tuple(X)]) + ".")
                if random.random() < self.A[j][tuple(X)]:
                    X[j] = not X[j]
                    if verbose:
                        print("Yes, trait", j, "has been", ("gained" if X[j] else "lost") + ".")
                else:
                    if verbose:
                        print("No, trait", j, "remains", ("present" if X[j] else "absent") + ".")
                if remember:
                    Y[j].append(X[j])
        if remember:
            return tuple(tuple(y) for y in Y)
        else:
            return tuple(X)

    def plot(self, m):
        data = tuple(self.run(remember=True) for i in range(m))
        for i in range(self.n):
            p = [sum(datum[i][j] for datum in data)/m for j in range(self.t)]
            plot.plot(p)

    def expected_plot(self):
        assert(self.n == 1)
        p = self.A[0][(False,)]
        q = self.A[0][(True,)]
        if self.X_0[0]:
            plot.plot(tuple((p + q * (1 - p - q)**i) / (p + q) for i in range(self.t)))
        else:
            plot.plot(tuple(p * (1 - (1 - p - q)**i) / (p + q) for i in range(self.t)))

def test_n_1():
    p = DiscreteGainLossProcess(1,
        ({(False,): 0.01, (True,): 0.02},),
        (False,),
        500)
    p.plot(1000)
    p.expected_plot()

def test_n_2():
    p = DiscreteGainLossProcess(2,
        ({(False, False): 0.01, (False, True): 0.03, (True, False): 0.02, (True, True): 0.04},
         {(False, False): 0.03, (False, True): 0.01, (True, False): 0.04, (True, True): 0.02}),
        (False, False),
        500)
    p.plot(1000)
