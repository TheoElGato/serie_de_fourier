from math import *

# constante
TWO_PI = pi * 2

class Complex:
  def __init__(self, a, b):
    self.re = a
    self.im = b


  def add(self, c):
    self.re += c.re
    self.im += c.im


  def mult(self, c):
    re = self.re * c.re - self.im * c.im
    im = self.re * c.im + self.im * c.re
    return Complex(re, im)


def dft(x):
  X = []
  N = len(x)
  for k in range(N):
    sum = Complex(0, 0)
    for n in range(N):
      phi = (TWO_PI * k * n) / N
      c = Complex(cos(phi), -sin(phi))
      sum.add(x[n].mult(c))

    sum.re = sum.re / N
    sum.im = sum.im / N

    freq = k
    amp = sqrt(sum.re * sum.re + sum.im * sum.im)
    phase = atan2(sum.im, sum.re)
    X.append([sum.re, sum.im, freq, amp, phase])
  return X

