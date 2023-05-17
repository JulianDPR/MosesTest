import pandas as pd
import numpy as np
import scipy.stats as ss


def MosesTest(x,y,a,extreme=0):

    def factorial(x):
        y = 1
        for i in range(1,x+1):
            y = y*i
        return y

    def combinatoria(x,y,factorial=factorial):

        z = factorial(x)/(factorial(y)*factorial(x-y))
        return z

    def moses(r,m,h,n, combinatoria=combinatoria):

        y = combinatoria(r+m-2*h-2, r)
        x = combinatoria(n+2*h+1-r, n-r)
        z = combinatoria(m+n, m)
        return y*x/z

    def cdf(r, m, h, n, moses=moses):

        r = list(range(r+1))
        return np.sum(list(map(lambda x: moses(x, m, h, n), r)))

    def t(r,m,h,n,a, moses=moses):

        r = list(range(r+1))
        s = np.cumsum(list(map(lambda x: moses(x, m, h, n), r)))
        r = np.array(r)
        return r[s<=a][-1]

    m = len(x)
    n = len(y)

    f = pd.DataFrame(x+y, columns=["value"])
    f["is"]=np.select([f.index<len(x), f.index>=len(x)], ["x", "y"])
    f = f.sort_values("value")
    f.index = list(range(1, len(f)+1))

    indexer = np.cumsum(f["is"]=="x")<=extreme
    f.loc[indexer, "is"]="h"
    indexer = np.cumsum((f["is"]=="x")[::-1])<=extreme
    f.loc[indexer,"is"]="h"

    inf = f.index[f["is"]=="x"][0]
    sup = f.index[f["is"]=="x"][-1]
    s_ = sup-inf+1

    m_h = len(x)-2*extreme

    r = s_ - m_h
    valor_p = cdf(r, m, extreme, n)

    R = t(r,m,extreme,n,a)

    dic = {"S*":s_,"P(Wh<=S*)":valor_p, "R(S*<=Wa)":f"{s_}<={m+R-2*h}"}

    print(dic)

    return list(dic.values())

x = [21,21.4,22.5,23.6,25.8,25.9,27,27.8,30.1,30.5,33.7,34.8,35.1,35.3,38.9,45]
y = [17.4,18.6,19.1,22.3,24.7,25.2,26.1,27.1,28,29.5,30.3,30.4]

print(MosesTest(x,y,0.5))


