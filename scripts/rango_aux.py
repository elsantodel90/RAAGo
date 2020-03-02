#!/usr/bin/python3

from math import exp
from scipy.stats import norm

sigma_px = 1.0569463399999999 # Numero magico del modelo: en definitiva estima que el desvio en la performance de un jugador es 0.747 

def new_ratings(mu1, mu2, sigma1, sigma2):
    # Function de verosimilitud bayesiana (con constantes ya ignoradas): buscamos el mu que maximiza esto,
    # y ese es el nuevo ranking del 1.
    def f(nmu1, nmu2):
        return norm.cdf((nmu1 - nmu2)/sigma_px) * exp(-0.5 * ((nmu1-mu1)/sigma1)**2.0) * exp(-0.5 * ((nmu2-mu2)/sigma2)**2.0)
    best = -1.0
    bestx = None
    besty = None
    x = -30.0
    while x < 10.0:
        a = -30.0
        b = 10.0
        while (b-a > 0.005):
            c1 = a + (b-a)/3.0
            c2 = a + 2.0*(b-a)/3.0
            if (f(x,c1) > f(x,c2)):
                b = c2
            else:
                a = c1
        y = 0.5 * (a+b)
        v = f(x, y)
        if v > best:
            best = v
            bestx = x
            besty = y
        x += 0.01
    return bestx, besty

def show_data(mu1, mu2, sigma1, sigma2):
    print("Estimated prior probability for player 1 win: {}".format(norm.cdf((mu1 - mu2)/sigma_px)))
    nmu1, nmu2 = new_ratings(mu1, mu2, sigma1 , sigma2)
    print("Estimated new rating for player 1: {:.3f} (+ {:.3f})".format(nmu1, nmu1 - mu1))
    print("Estimated new rating for player 2: {:.3f} (- {:.3f})".format(nmu2, mu2 - nmu2))
    print("Estimated new probability for player 1 win: {}".format(norm.cdf((nmu1 - nmu2)/sigma_px)))


show_data(-3.748, -1.136, 0.219 , 0.465)
