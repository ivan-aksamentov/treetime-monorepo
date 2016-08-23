from __future__ import division, print_function
import numpy as np
from scipy.interpolate import interp1d
from config import WIDTH_DELTA, BIG_NUMBER, MIN_LOG, MIN_INTEGRATION_PEAK, TINY_NUMBER
from collections import Iterable
from copy import deepcopy as make_copy
from scipy.ndimage import binary_dilation

class Distribution(object):
    """docstring for Distribution"""

    @staticmethod
    def calc_fwhm(distribution, is_log=True):
        """
        Assess the width of the probability distribution. This returns full-width-half-max
        """

        if isinstance(distribution, interp1d):

            if is_log:
                ymin = distribution.y.min()
                real_prob = np.exp(-(distribution.y-ymin))
            else:
                real_prob = distribution.y

            xvals = distribution.x

        elif isinstance(distribution, Distribution):
            # Distribution always stores log-prob
            xvals = distribution._func.x
            real_prob = distribution.prob_relative(xvals)
        else:
            raise TypeError("Error in computing the FWHM for the distribution. "
                " The input should be either Distribution or interpolation object");

        x_idxs = binary_dilation(real_prob > 0.5*(real_prob.max() - real_prob.min()), iterations=1)
        xs = xvals[x_idxs]
        if xs.shape[0] < 2:
            #import ipdb; ipdb.set_trace()
            print ("Not enough points to compute FWHM: returning zero")
            return distribution.xmax - distribution.xmin
        else:
            return xs.max() - xs.min()


    @classmethod
    def delta_function(cls, x_pos, weight=1.):
        """
        Create delta function distribution.
        """

        distribution = cls(x_pos,0.,is_log=True)
        distribution.weight  = weight
        return distribution

    @classmethod
    def shifted_x(cls, dist, delta_x):
        return Distribution(dist.x+delta_x, dist.y, kind=dist.kind)

    @staticmethod
    def multiply(dists):
        '''
        multiplies a list of Distribution objects
        '''
        if  not all([isinstance(k, Distribution) for k in dists]):
            raise NotImplementedError("Can only multiply Distribution objects")

        n_delta = np.sum([k.is_delta for k in dists])
        if n_delta>1:
            raise ArithmeticError("Cannot multiply two delta functions!")
        elif n_delta==1:
            delta_dist_ii = np.where([k.is_delta for k in dists])[0][0]
            delta_dist = dists[delta_dist_ii]
            new_xpos = delta_dist.peak_pos
            new_weight  = np.prod([k.prob(new_xpos) for k in dists if k!=delta_dist] * delta_dist.weight)
            res = Distribution.delta_function(new_xpos, weight = new_weight)
        else:
            new_xmin = np.max([k.xmin for k in dists])
            new_xmax = np.min([k.xmax for k in dists])
            x_vals = np.unique(np.concatenate([k.x for k in dists]))
            x_vals = x_vals[(x_vals>new_xmin-TINY_NUMBER)&(x_vals<new_xmax+TINY_NUMBER)]
            if x_vals.shape[0] == 0:
                print ("ERROR in distribution multiplication: Distributions do not overlap")
                x_vals = [0,1]
                y_vals = [BIG_NUMBER,BIG_NUMBER]
                res = Distribution(x_vals, y_vals, is_log=True, kind='linear')
            elif x_vals.shape[0] == 1:
                res = Distribution.delta_function(x_vals[0])
            else:
                y_vals = np.sum([k.__call__(x_vals) for k in dists], axis=0)
                res = Distribution(x_vals, y_vals, is_log=True, kind='linear')

        return res


    def __init__(self, x, y, is_log=True, kind='linear'):

        """
        Create Distribution instance
        """

        if isinstance(x, Iterable) and isinstance (y, Iterable):

            self._delta = False # NOTE in classmethod this value is set explicitly to True.
            xvals, yvals = np.array(sorted(zip(x,y))).T
            # first, prepare x, y values
            if not is_log:
                yvals = -np.log(yvals)
            # just for safety
            yvals [np.isnan(yvals)] = BIG_NUMBER
            # set the properties
            self._kind=kind
            # remember range
            self._xmin, self._xmax = xvals[0], xvals[-1]
            self._support = self._xmax - self._xmin
            # extract peak
            self._peak_idx = yvals.argmin()
            self._peak_val = yvals.min()
            self._peak_pos = xvals[self._peak_idx]
            yvals -= self._peak_val
            self._ymax = yvals.max()
            # store the interpolation object
            self._func= interp1d(xvals, yvals, kind=kind, fill_value=BIG_NUMBER, bounds_error=False)
            self._fwhm = Distribution.calc_fwhm(self)

        elif np.isscalar(x):
            assert (np.isscalar(y) or y is None)
            self._delta = True
            self._peak_pos = x
            self._fwhm = 0
            if y is None:
                self._peak_val = np.inf
            else:
                self._peak_val = y

            self._xmin, self._xmax = x, x
            self._support = 0.
            self._func = lambda x : (x==self.peak_pos)*self.peak_val
        else:
            raise TypeError("Cannot create Distribution: "
                "Input arguments should be scalars or iterables!")


    @property
    def is_delta(self):
        return self._delta

    @property
    def kind(self):
        return self._kind

    @property
    def peak_val(self):
        return self._peak_val

    @property
    def peak_pos(self):
        return self._peak_pos

    @property
    def peak_idx(self):
        return self._peak_idx

    @property
    def support(self):
        return self._support

    @property
    def fwhm(self):
        return self._fwhm

    @property
    def x(self):
        if self.is_delta:
            return [self._peak_pos]
        else:
            return self._func.x

    @property
    def y(self):
        if self.is_delta:
            print("THIS SHOULDN'T BE CALLED ON A DELTA FUNCTION")
            return [self.weight]
        else:
            return self._peak_val + self._func.y

    @property
    def xmin(self):
        return self._xmin

    @property
    def xmax(self):
        return self._xmax


    def __call__(self, x):

        if isinstance(x, Iterable):
            valid_idxs = (x > self._xmin-TINY_NUMBER) & (x < self._xmax+TINY_NUMBER)
            res = np.ones_like (x, dtype=float) * (BIG_NUMBER+self.peak_val)
            tmp_x = np.copy(x[valid_idxs])
            tmp_x[tmp_x<self._xmin+TINY_NUMBER] = self._xmin+TINY_NUMBER
            tmp_x[tmp_x>self._xmax-TINY_NUMBER] = self._xmax-TINY_NUMBER
            res[valid_idxs] = self._peak_val + self._func(tmp_x)
            return res

        elif np.isreal(x):
            if x < self._xmin or x > self._xmax:
                return BIG_NUMBER+self.peak_val
            # x is within interpolation range
            elif self._delta == True:
                return self._peak_val
            else:
                return self._peak_val + self._func(x)
        else:
            raise TypeError("Wrong type: should be float or array")


    def __mul__(self, other):
        return Distribution.multiply((self, other))


    def _adjust_grid(self):
        pass


    def prob(self,x):
        return np.exp(-1 * self.__call__(x))

    def prob_relative(self,x):
        return np.exp(-1 * (self.__call__(x)-self.peak_val))

    def x_rescale(self, factor):
        self._func.x*=factor
        if factor>=0:
            self._xmin*=factor
            self._xmax*=factor
        else:
            tmp = self.xmin
            self._xmin = factor*self.xmax
            self._xmax = factor*tmp


    def integrate(self, return_log=False ,**kwargs):
        if self.is_delta:
            return self.weight
        else:
            integral_result = self.integrate_simpson(**kwargs)
            if return_log:
                if integral_result==0:
                    return -self.peak_val - BIG_NUMBER
                else:
                    return -self.peak_val + max(-BIG_NUMBER, np.log(integral_result))
            else:
                return np.exp(-self.peak_val)*integral_result

    def integrate_trapez(self, a, b,n):
        mult = 0.5
        if a>b:
            b,a = a,b
            mult=-0.5

        x = np.linspace(a,b,n)
        dx = np.diff(x)
        y = self.prob_relative(x)
        return mult*np.sum(dx*(y[:-1] + y[1:]))


    def integrate_simpson(self, a,b,n):
        if n % 2 == 0:
            n += 1
        mult = 1.0/6
        dpeak = max(5*self.fwhm, MIN_INTEGRATION_PEAK)
        threshold = np.array([a,self.peak_pos-dpeak, self.peak_pos+dpeak,b])
        threshold = threshold[(threshold>=a)&(threshold<=b)]
        threshold.sort()
        res = []
        for lw, up in zip(threshold[:-1], threshold[1:]):
            x = np.linspace(lw,up,n)
            dx = np.diff(x[::2])
            y = self.prob_relative(x)
            res.append(mult*(dx[0]*y[0]+ np.sum(4*dx*y[1:-1:2])
                    + np.sum((dx[:-1]+dx[1:])*y[2:-1:2]) + dx[-1]*y[-1]))

        return np.sum(res)


if __name__=="__main__":

    from matplotlib import pyplot as plt
    plt.ion()

    x = [-1e-10,  0.,    1.,  2.,    2.+1e-10]
    y = [  1e-10, 1e-10, 10., 1e-10, 1e-10]
    d1 = Distribution(x, y,is_log=False)

    def f(x):
        #return (x-5)**2+np.abs(x)**3
        return (x**2-5)**2 #(x-5)**2+np.abs(x)**3
    def g(x):
        return (x-4)**2*(x**(1.0/3)-5)**2

    plot=False
    error = {}
    for kind in ['linear', 'quadratic', 'cubic', 'Q']:
        error[kind]=[[],[]]
    npoints = [11,21] #,31,41, 51,75,101]
    for ex, func in [[0,f],[1,g]]:
        for npoint in npoints:
            if ex==0:
                xnew = np.linspace(-5,15,1000)
                x = np.linspace(0,10,npoint)
            elif ex==1:
                xnew = np.linspace(0,150,1000)
                x = np.linspace(0,9.0,npoint)**3

            if plot:
                plt.figure()
                plt.plot(x, np.exp(-func(x)),'-o', label = 'data')
                plt.plot(xnew, np.exp(-func(xnew)),'-',label='true')
            for kind in ['linear', 'quadratic', 'cubic']:
                try:
                    dist = Distribution(x, func(x), kind=kind, is_log=True)
                    if plot: plt.plot(xnew, dist.prob(xnew), label=kind)
                    E = np.mean((np.exp(-func(xnew))-dist.prob(xnew))[(xnew>dist.xmin) & (xnew<dist.xmax)]**2)
                    print(kind,npoint, E)
                except:
                    E=np.nan
                error[kind][ex].append(E)
            try:
                distQ = quadratic_interpolator(x, func(x))
                if plot: plt.plot(xnew[(xnew>dist.xmin) & (xnew<dist.xmax)], np.exp(-distQ(xnew))[(xnew>dist.xmin) & (xnew<dist.xmax)], label='Q')
                E = np.mean((np.exp(-func(xnew))-np.exp(-distQ(xnew)))[(xnew>dist.xmin) & (xnew<dist.xmax)]**2)
                print('Q',npoint, E)
            except:
                E=np.nan
            error['Q'][ex].append(E)
            if plot:
                plt.yscale('log')
                plt.legend()

    for ex in [0,1]:
        plt.figure()
        for k in error:
            plt.plot(npoints, error[k][ex],'-o', label=k)
        plt.yscale('log')
        plt.legend()

    integration_error = {'trapez':[], 'simpson':[], 'piecewise':[]}
    npoints = [11,21,31, 41, 51,75,101, 201, 501, 1001]
    xnew = np.linspace(-5,15,1000)
    x = np.linspace(0,10,3000)
    dist = Distribution(x, g(x), kind='linear', is_log=True)
    for npoint in npoints:
        integration_error['trapez'].append(dist.integrate_trapez(0,10,npoint))
        integration_error['simpson'].append(dist.integrate_simpson(0,10,npoint))
        xtmp = np.linspace(0,10,min(100,npoint))
        disttmp = Distribution(xtmp, g(xtmp), kind='cubic', is_log=True)
        integration_error['piecewise'].append(disttmp.integrate_piecewise_gaussian(0,10))

    plt.figure()
    base_line = integration_error['simpson'][-1]
    plt.plot(npoints, np.abs(integration_error['trapez']-base_line), label='trapez')
    plt.plot(npoints, np.abs(integration_error['simpson']-base_line), label='simpson')
    plt.plot(npoints, np.abs(integration_error['piecewise']-base_line), label='piecewise')
    plt.xlabel('npoints')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
