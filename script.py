import numpy as np
import _chi2 as _chi2
x, y, yerr = np.loadtxt('./data/datalist.txt').T

for i in range(500000):
    _chi2.chi2(1.234, -43.21, x, y, yerr) / (len(x) - 2)