# Fig. 7, section 7: rounding of the angle w*t + phi as the page computes it in doubles (sumAt, L817),
# against the exact value of the same double inputs. Run: python3 -I notes/fig07/angle_rounding.py
from fractions import Fraction
import random, math
random.seed(7)
worst = 0.0
for _ in range(200000):
    t = random.uniform(0, 1000.0)
    w = random.choice([32.0, -32.0, 31.99, 17.0, 4.0])
    phi = random.uniform(0, 6.28)
    ang = w * t + phi                      # what JavaScript computes
    exact = Fraction(w) * Fraction(t) + Fraction(phi)
    worst = max(worst, abs(float(Fraction(ang) - exact)))
print('largest rounding of the angle, t <= 1000 s, |w| <= 32 rad/s:', worst)
print('one ulp at 32000 rad:', math.ulp(32000.0))
