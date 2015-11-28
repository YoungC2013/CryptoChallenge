#!/usr/bin/env python
#! --coding:utf-8-- !# 

import sys
import struct


def rol32(word,count):
  return (word << count | word >> (32 - count)) & 0xFFFFFFFF  #��word������countλ������word����32-countλ��Ȼ������ȫ1������

def padding(msglen):

  chunks = int((msglen+9)/64)
  missing_chunks = 64 - abs((chunks*64)-(msglen+9))
  #��64��ȥ���һ��block�еĴ��ڵ���Ϣ����ĩβ�ı�ʾλ���õ��ľ�����Ҫ����\x00�ĸ���
  pad = "\x80"
  for i in xrange(0,missing_chunks):
    pad += "\x00"
  pad += struct.pack('>Q',msglen*8)#����Ϣ��λ���ӵ�ĩβ������Ϣ����*8

  return pad

class sha1:


  blocksize = 64

  def __init__(self,imsg=""):

    self.__setinit()
    self.mesg = imsg
    self.lmsg = len(imsg)

  def __setinit(self):

    self.h0 = 0x67452301
    self.h1 = 0xEFCDAB89
    self.h2 = 0x98BADCFE
    self.h3 = 0x10325476
    self.h4 = 0xC3D2E1F0

  def __transform(self,w):

    for j in range(16,80):
      w.append(rol32(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16],1))

    a = self.h0
    b = self.h1
    c = self.h2
    d = self.h3
    e = self.h4

    for j in range(0,80):#��80��ѭ����ÿһ��ѭ���ò�ͬ�ķ�ʽ���㣬0-20��һ�֣�20-40һ��,40-60һ�֣�60-80һ��
      if j < 20:
        f = (b & c) | ((~ b) & d)
        k = 0x5A827999
      elif j < 40:
        f = b ^ c ^ d
        k = 0x6ED9EBA1
      elif j < 60:
        f = (b & c) | (b & d) | (c & d)
        k = 0x8F1BBCDC
      else:
        f = b ^ c ^ d
        k = 0xCA62C1D6

      temp = (rol32(a,5) + f + e + k + w[j]) & 0xFFFFFFFF #rol32���㷨�ʼ�н���
      e = d
      d = c
      c = rol32(b,30)
      b = a
      a = temp #������ǰ����㷨��Ҫ���abcde���б任

    self.h0 = (self.h0 + a) & 0xFFFFFFFF
    self.h1 = (self.h1 + b) & 0xFFFFFFFF
    self.h2 = (self.h2 + c) & 0xFFFFFFFF
    self.h3 = (self.h3 + d) & 0xFFFFFFFF
    self.h4 = (self.h4 + e) & 0xFFFFFFFF  #���ﰴ��sha1��ԭ����h1h2h3h4h0���б任���õ��µ�h������һ�ּ�����

  def digest(self,imsg=""):

    msg = self.mesg
    lmsg = self.lmsg
    if imsg != "":
      msg = imsg
      lmsg = len(imsg)

    msg += padding(lmsg)  #�������Ϣ��pading�����������������������Ϣ��

    for i in range(0,len(msg)/64):
      self.__transform(list(struct.unpack('>IIIIIIIIIIIIIIII',msg[i*64:(i+1)*64]))) #���������һ��blockΪ��λ��64λ����ÿ��block����__transform�У���������h0h1h2h3h4,���㵽���һ��block��ôh0h1h2h3h4�������ǵ�sha1��

    out = struct.pack('>IIIII',self.h0,self.h1,self.h2,self.h3,self.h4)
    self.__setinit()
    return out

  def hexdigest(self,imsg=""):
    return self.digest(imsg).encode('hex') #����Ϣת��Ϊ16����

  

if __name__ == "__main__":
  try:
    msg = sys.argv[1]
  except:
    msg = " hey girl you look so beautiful"

  print 'msg is :'+msg+'\n'
  key = "fe49e3fe5d7"
  print 'key is :'+key+'\n'
  print 'sha1 is :'+sha1(key+msg).hexdigest() #��һ����sha1����֮��ת��Ϊ16����
