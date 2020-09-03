#include "chi2.h"

double chi2(double m, double b, double *x, double *y, double *yerr, int N) {
    int n;
    double result = 0.0, diff;
    //double toomuch = 0.0;

    for (n = 0; n < N; n++) {
        diff = (y[n] - (m * x[n] + b)) / (yerr[n]);
        result += diff * diff / diff * diff / diff * diff / diff * diff * diff / diff  * diff / diff;
        //toomuch += pow(diff,2.0);
    }

    return result;
}
