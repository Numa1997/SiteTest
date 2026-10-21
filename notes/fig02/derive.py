# Fig. 2: symbolic check of the note's derivation, eqs. (3)-(9) and (10)-(11). Run: python3 -I notes/fig02/derive.py
import sympy as sp
t=sp.symbols('t'); m1,m2,l1,l2,g=sp.symbols('m1 m2 l1 l2 g',positive=True)
th1=sp.Function('th1')(t); th2=sp.Function('th2')(t)
x1=l1*sp.sin(th1); y1=-l1*sp.cos(th1); x2=x1+l2*sp.sin(th2); y2=y1-l2*sp.cos(th2)
T=sp.Rational(1,2)*m1*(x1.diff(t)**2+y1.diff(t)**2)+sp.Rational(1,2)*m2*(x2.diff(t)**2+y2.diff(t)**2)
V=m1*g*y1+m2*g*y2
w1,w2=th1.diff(t),th2.diff(t); d=th1-th2
T3=sp.Rational(1,2)*m1*l1**2*w1**2+sp.Rational(1,2)*m2*(l1**2*w1**2+l2**2*w2**2+2*l1*l2*w1*w2*sp.cos(d))
print('eq (3) T matches:',sp.simplify(sp.expand_trig(T-T3))==0)
print('eq (4) V matches:',sp.simplify(V-(-(m1+m2)*g*l1*sp.cos(th1)-m2*g*l2*sp.cos(th2)))==0)
L=T-V
EL1=sp.diff(L.diff(w1),t)-L.diff(th1); EL2=sp.diff(L.diff(w2),t)-L.diff(th2)
a1,a2=th1.diff(t,2),th2.diff(t,2)
eq6=(m1+m2)*l1*a1+m2*l2*a2*sp.cos(d)+m2*l2*w2**2*sp.sin(d)+(m1+m2)*g*sp.sin(th1)
eq7=l1*a1*sp.cos(d)+l2*a2-l1*w1**2*sp.sin(d)+g*sp.sin(th2)
print('eq (6) = EL1/l1:',sp.simplify(sp.expand_trig(EL1/l1-eq6))==0)
print('eq (7) = EL2/(m2 l2):',sp.simplify(sp.expand_trig(EL2/(m2*l2)-eq7))==0)
A,B,W1,W2,TH1,TH2=sp.symbols('A B W1 W2 TH1 TH2')
sub={a1:A,a2:B}
sol=sp.solve([eq6.subs(sub),eq7.subs(sub)],[A,B])
sub2={w1:W1,w2:W2}
sol={k:v.subs(sub2).subs({th1:TH1,th2:TH2}) for k,v in sol.items()}
D=TH1-TH2
alpha1=(-g*(2*m1+m2)*sp.sin(TH1)-m2*g*sp.sin(TH1-2*TH2)-2*m2*sp.sin(D)*(W2**2*l2+W1**2*l1*sp.cos(D)))/(l1*(2*m1+m2-m2*sp.cos(2*D)))
alpha2=(2*sp.sin(D)*(W1**2*l1*(m1+m2)+g*(m1+m2)*sp.cos(TH1)+W2**2*l2*m2*sp.cos(D)))/(l2*(2*m1+m2-m2*sp.cos(2*D)))
print('eq (9) alpha1 matches Cramer:',sp.simplify(sp.expand_trig(sol[A]-alpha1))==0)
print('eq (9) alpha2 matches Cramer:',sp.simplify(sp.expand_trig(sol[B]-alpha2))==0)
M=sp.Matrix([[(m1+m2)*l1,m2*l2*sp.cos(D)],[l1*sp.cos(D),l2]])
print('eq (8) det:',sp.simplify(M.det()-l1*l2*(m1+m2*sp.sin(D)**2))==0)
print('identity 2 sin th2 cos d = sin th1 - sin(th1-2 th2):',sp.simplify(sp.expand_trig(2*sp.sin(TH2)*sp.cos(D)-(sp.sin(TH1)-sp.sin(TH1-2*TH2))))==0)
print('identity sin th1 cos d - sin th2 = cos th1 sin d:',sp.simplify(sp.expand_trig(sp.sin(TH1)*sp.cos(D)-sp.sin(TH2)-sp.cos(TH1)*sp.sin(D)))==0)
# Cramer numerator of alpha2 before the identity: (m1+m2)(l1 w1^2 sin d - g sin th2) + cos d (m2 l2 w2^2 sin d + (m1+m2) g sin th1), over l2 (m1 + m2 sin^2 d)
num2=(m1+m2)*(l1*W1**2*sp.sin(D)-g*sp.sin(TH2))+sp.cos(D)*(m2*l2*W2**2*sp.sin(D)+(m1+m2)*g*sp.sin(TH1))
print('alpha2 Cramer form:',sp.simplify(sp.expand_trig(sol[B]-num2/(l2*(m1+m2*sp.sin(D)**2))))==0)
# small swings, equal masses and lengths
w,gl=sp.symbols('omega gl',positive=True)
Am=sp.Matrix([[2,1],[1,1]]); Bm=sp.Matrix([[2,0],[0,1]])
print('eq (11):',sp.solve(sp.Eq((gl*Bm-w**2*Am).det(),0),w**2))
for s in (2-sp.sqrt(2),2+sp.sqrt(2)):
    om=sp.sqrt(s*9.81); print('omega',float(om),'period',float(2*sp.pi/om),'u2/u1',sp.nsimplify(sp.simplify(2*(1-s)/s)))
# simplify() may not close the trigonometric gap; test the difference numerically at random points
import random
random.seed(1)
worst=0
f1=sp.lambdify((TH1,TH2,W1,W2,m1,m2,l1,l2,g),sol[A]-alpha1); f2=sp.lambdify((TH1,TH2,W1,W2,m1,m2,l1,l2,g),sol[B]-alpha2)
for _ in range(2000):
    args=(random.uniform(-3.2,3.2),random.uniform(-3.2,3.2),random.uniform(-5,5),random.uniform(-5,5),1,random.uniform(0.1,10),1,random.uniform(0.2,5),9.81)
    worst=max(worst,abs(f1(*args)),abs(f2(*args)))
print('eq (9) minus Cramer, worst absolute difference at 2000 random points:',worst)
print('alpha1 symbolic zero via trigsimp:',sp.simplify(sp.trigsimp(sp.expand_trig(sp.together(sol[A]-alpha1))))==0)
