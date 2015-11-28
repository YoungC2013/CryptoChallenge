#!/usr/bin/env python
# -*- coding: gbk -*-

import Crypto.Util.number
import gmpy2

class RSA:
  #RSA��Ӧ����
  def keygen(self, l=2048, s=True):
    while True:
      p = gmpy2.mpz(Crypto.Util.number.getPrime(l))
      q = gmpy2.mpz(Crypto.Util.number.getPrime(l))
      n = gmpy2.mpz(p * q)
      et = (p - 1) * (q - 1)
      if s == True:
        e = 2**16+1 # << - this is better
      else:
        e = 3  # << - this is bad
      d = gmpy2.invert(e, et)
      if d != None:
        break

    return (e, n), (d, n)

  def encrypt(self, m, (e,n)):
    #���м��ܵ�m������string
    m=s2i(m)
    len_n = (gmpy2.bit_length(n))-1
    len_m = gmpy2.bit_length(m)-1
    if len_n < len_m:
      pass#return [i2s(pow(s2i(m), e, n))]
    else:
      cs=gmpy2.powmod(m,e,n)
      return cs

  def decrypt(self, cs, (d,n)):
    #���н����������string
    m=gmpy2.powmod(cs,d,n)
    m=i2s(m)
    return m


def i2s(i):
  #����ת�ַ��� 
  x = hex(i).replace("0x","").replace("L","")
  if len(x) % 2 == 1:
    x = "0" + x
  return x.decode('hex')

def s2i(s):
  #�ַ���ת����
  return int(s.encode('hex'),16)


if __name__ == "__main__":

  msg = "I'm YoungC in OneA"
  print "���Ժ򡭡�"
  rsa = RSA()
  pub,priv = rsa.keygen()
  C = rsa.encrypt(msg,pub)
  #��������
  assert rsa.decrypt(C,priv) == msg, "bug in my RSA, decryption didn't provide the same clear text"

  S = 3
  print "����:"+msg
  print "���ģ�C ��:"+str(C)
  #��С���ܹ�����������s����Ϊ2��Phi(N)�����أ���������
  C1=gmpy2.f_mod(gmpy2.mul(C,gmpy2.powmod(S,pub[0],pub[1])),pub[1])
  if C1 != C: # C1��������C��ͬŶ��
    P1 = rsa.decrypt(C1,priv)
    print "���ģ�C'����"+str(C1)
    print "�ָ�C'��P'/3��="+i2s(gmpy2.divm(s2i(P1),S,pub[1]))
  else:
    print "something wrong C1 and C should be different"




