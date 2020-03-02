#!/usr/bin/python3

from math import exp
from scipy.stats import norm

sigma_px = 1.05694634 # Numero magico del modelo: en definitiva estima que el desvio estandar en la performance de un jugador es 0.747

def new_ratings(mu1, mu2, sigma1, sigma2):
    # Function de verosimilitud bayesiana (con constantes ya ignoradas): buscamos el mu que maximiza esto,
    # y ese es el nuevo ranking del 1.
    def f(nmu1, nmu2):
        return norm.cdf((nmu1 - nmu2)/sigma_px) * exp(-0.5 * ((nmu1-mu1)/sigma1)**2.0) * exp(-0.5 * ((nmu2-mu2)/sigma2)**2.0)
    def besty(x):
        a = -30.0
        b = 10.0
        while (b-a > 0.0005):
            c1 = a + (b-a)/3.0
            c2 = a + 2.0*(b-a)/3.0
            if (f(x,c1) > f(x,c2)):
                b = c2
            else:
                a = c1
        return 0.5 * (a+b)
    xa = -30.0
    xb = 10.0
    while xb-xa > 0.0005:
        c1 = xa + (xb-xa)/3.0
        c2 = xa + 2.0*(xb-xa)/3.0
        if (f(c1,besty(c1)) > f(c2,besty(c2))):
            xb = c2
        else:
            xa = c1
    bestx = 0.5 * (xa+xb)
    return bestx, besty(bestx)

def closegap(x):
    if x > 0.0:
        return x - 1.0
    else:
        return x + 1.0

def creategap(x):
    if x > 0.0:
        return x + 1.0
    else:
        return x - 1.0


def show_data(mu1, mu2, sigma1, sigma2):
    print("Previous rating for player 1 : {:.3f} ± {:.3f}".format(mu1, sigma1))
    print("Previous rating for player 2 : {:.3f} ± {:.3f}".format(mu2, sigma2))
    mu1 = closegap(mu1)
    mu2 = closegap(mu2)
    print("Estimated prior probability for player 1 win: {}".format(norm.cdf((mu1 - mu2)/sigma_px)))
    nmu1, nmu2 = new_ratings(mu1, mu2, sigma1 , sigma2)
    print("Estimated new rating for player 1: {:.3f} (+ {:.3f})".format(creategap(nmu1), nmu1 - mu1))
    print("Estimated new rating for player 2: {:.3f} (- {:.3f})".format(creategap(nmu2), mu2 - nmu2))
    print("Estimated new probability for player 1 win: {}".format(norm.cdf((nmu1 - nmu2)/sigma_px)))


show_data(-3.748, -1.136, 0.219 , 0.465)
