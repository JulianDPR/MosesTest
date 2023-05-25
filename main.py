
def MosesTest(x,y,a,extreme=0, rand = False):

    import pandas as pd
    import numpy as np
    import scipy.stats as ss
    import seaborn as sns
    import matplotlib.pyplot as plt
    
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
        try:
          return r[s<=a][-1]
        except:
          return r[0]

    m = len(x)
    n = len(y)


    if rand == True:

      def random(m,h,n, t=t):

        k = [15, 30, 60, 120, 240, 480]
        fig, ax = plt.subplots(2,3)
        ax = ax.ravel()
        for i,j in zip(k,ax):

          v = []
          np.random.seed(2)
          u = np.random.uniform(0,1, i)
          for l in u:
        
            v.append(t(n,m,h,n,l))

          sns.kdeplot(v, ax=j, linestyle="--", label=f"n={i}")
          sns.kdeplot(np.random.normal(np.mean(v),(np.var(v))**(1/2),1000), ax=j, linestyle="dotted", label=f"Norm")
          j.legend(bbox_to_anchor=(1,-0.1),ncol=len(k))
          j.grid()
        
        
        fig.tight_layout()
      
      random(m,extreme,n)

    f = pd.DataFrame(x+y, columns=["value"])
    f["is"]=np.select([f.index<len(x), f.index>=len(x)], ["x", "y"])
    f = f.sort_values("value")
    f.index = list(range(1, len(f)+1))

    indexer = np.cumsum(f["is"]=="x")<=extreme
    f.loc[indexer, "is"]="h"
    indexer = np.cumsum((f["is"]=="x")[::-1])<=extreme
    f.loc[indexer,"is"]="h"

    print("Variables ordenadas \n \n",f.transpose())

    inf = f.index[f["is"]=="x"][0]
    sup = f.index[f["is"]=="x"][-1]
    s_ = sup-inf+1

    m_h = len(x)-2*extreme

    r = s_ - m_h
    valor_p = cdf(r, m, extreme, n)

    R = t(r,m,extreme,n,a)
  
    dic = {"S*":s_,"Robs":r,"P(R<=Robs*)":valor_p, "Rc=(Robs<=R)":f"{r}<={R}", "Rc=(S*<=SR)":f"{s_}<={R+m_h}",
           "a*":cdf(R,m,extreme,n)}

    return pd.DataFrame(dic.values(), index=dic.keys(), columns=["Results"]).transpose()

#x = [21,21.4,22.5,23.6,25.8,25.9,27,27.8,30.1,30.5,33.7,34.8,35.1,35.3,38.9,45]
#y = [17.4,18.6,19.1,22.3,24.7,25.2,26.1,27.1,28,29.5,30.3,30.4]

#print(MosesTest(x=x,y=y,a=0.05,extreme=4,rand=True))#.to_latex())

#x = [1.7,2.7,1.8,2.8,1.9,3.1,2.2,3.6,3.7]
#y = [1.3,3.5,1.5,3.8,1.6,4.5,3.4,6.7]

#print(MosesTest(x=x,y=y,a=0.05,extreme=2, rand=False))#.to_latex())

#x = [5.86,5.46,5.69,6.49,7.81,9.03,7.49,8.98]
#y = [8.18,5.64,7.36,5.33,8.82,5.26,7.1]

#print(MosesTest(x=x,y=y,a=0.05,extreme=1,rand=False))

#import pandas as pd

#print(pd.DataFrame([x,y], index = ["x","y"]).transpose().to_latex())
