import numpy as np
from numpy import pi, r_
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.stats import power_divergence

def fit_power_law(xdata, ydata, log=False):
    powerlaw = lambda x, amp, index: amp * (x**index)
    fitfunc = lambda p, x: p[0] + p[1] * x
    errfunc = lambda p, x, y: (y - fitfunc(p, x))
    logx = np.log10([x + 1 for x in xdata])
    logy = np.log10([y + 1 for y in ydata])
    pinit = [1.0, -1.0]
    out = optimize.leastsq(errfunc, pinit,
                       args=(logx, logy), full_output=1)
    pfinal = out[0]
    covar = out[1]
    print("pfinal:", pfinal)
    print("covar:", covar)
    index = pfinal[1]
    amp = 10.0**pfinal[0]
    indexErr = np.sqrt( covar[0][0] )
    ampErr = np.sqrt( covar[1][1] ) * amp
    if log:
        plt.semilogy(xdata, powerlaw(xdata, amp, index))
    else:
        plt.plot(xdata, powerlaw(xdata, amp, index))
    
    print('Ampli = %5.2f +/- %5.2f' % (amp, ampErr))
    print('Index = %5.2f +/- %5.2f' % (index, indexErr))
    

def plot_xy_line(x, y, doFit = False, log=False):
    if doFit:
        fit_power_law(x,y, log)
    if log:
        plt.semilogy(x, y)
    else:
        plt.plot(x, y)
    plt.show()

def plot_xy_dot(x, y, doFit = False, log=False):
    if doFit:
        fit_power_law(x,y, log)
    if log:
        plt.semilogy(x, y, '.', markersize=2)
    else:
        plt.plot(x, y, '.', markersize=2)
    plt.show()

def plot_xy_point(x, y, doFit = False, log=False):
    if doFit:
        fit_power_law(x,y, log)
    plt.plot(x, y, 'o', markersize=3, alpha=0.5)
    plt.show()


def plot_pairs(pairs, plot_foo, log = False, doFit = False):
    val = [x[1] for x in pairs]
    plot_foo([x[0] for x in pairs], val, doFit=doFit, log=log )
    if doFit:
        print(power_divergence(val))


def plot_rank(y, plot_foo, log = False, doFit = False):
    val = list(range(0,len(y)))
    plot_foo(val, y, doFit=doFit, log=log )
    if doFit:
        print(power_divergence(y))

def plot_labels(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)



def plot_with_gaussion_fit(stat):
    data = [x[1] for x in stat]
    xdata = [x[0] for x in stat]

    plt.plot(xdata, data, '-', label="Experiment")

    X = np.arange(len(data))
    x = np.sum(X*data)/np.sum(data)
    width = np.sqrt(np.abs(np.sum((X-x)**2*data)/np.sum(data)))

    max_data = max(data)

    fit = lambda t : max_data*np.exp(-(t-x)**2/(2*width**2))

    plt.plot(xdata, fit(X), '-', label="Gaussian fit")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()

