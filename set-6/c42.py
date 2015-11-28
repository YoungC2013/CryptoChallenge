#!/usr/bin/env python
#! --coding:utf-8-- !# 


from rsa import RSA # RSA�㷨
import math
import hashlib
from decimal import *

def i2s(i):
  x = hex(i).replace("0x","").replace("L","")
  if len(x) % 2 == 1:
    x = "0" + x
  return x.decode('hex')

def s2i(s):
  return int(s.encode('hex'),16)

class PKCS15:


  def pad(self,msg,k):
    fflen = k - 20 - 13  #  k����Կ�ĳ��ȣ�fflen��ʾ��������ַ����ĳ��ȣ�������\xff��ʾ����ַ���
    return "\x00\x01%s\x00%s" % ("\xff" * fflen, msg)

  def unpad(self,msg):
    if msg[0:2] == '\x00\x01':
      i = msg.find('\x00', 2)
      return msg[i+1:i+1+20] #�������İ���ȡ�������ǵ�msg
    return None

class RSAsign:

  def make(self,msg,key):
    pkcs15 = PKCS15()
    rsa = RSA()
    dgst = hashlib.sha1(message).digest() #����msg��sha1
    paddgst = pkcs15.pad(dgst,len(i2s(key[1]))) #��sha1������䣬��亯����ǰ���н���
    return rsa.encrypt(paddgst,key) #����rsa���ܵķ������м��ܣ�c39����rsa���㷨

  def verify(self,msg,sign,key):
    pkcs15 = PKCS15()
    rsa = RSA()
    dgst = hashlib.sha1(message).digest()
    return pkcs15.unpad("\x00"+rsa.decrypt(sign,key)) == dgst #������sign��keyͨ�����ܺ������ܳ�����Ȼ�������֮��İ����msg�ָ������Ա�һ��

def forging(mesg,key):

  e = key[0]
  n = key[1]

  if e != 3:    #���e�ǲ���3
    raise Exception("e not equal 3")
  pkcs15 = PKCS15()
  dgst = hashlib.sha1(mesg).digest() #������Ϣ��sha1
  keylen = len(i2s(n)) #��Կ����

  getcontext().prec = keylen * 8 #���������þ���


  forge = "\x00\x01%s\x00%s" % ("\xff" * 8, dgst) # ������
  garbage = "\x00" * (keylen - 8 - len(dgst) - 13)
  whole = s2i(forge+garbage)
  cr = int(pow(whole,Decimal(1)/Decimal(3)))+1 #�����ǵõ���whole��3�η����õ���Ӧ��������α��ļ���sign

  return i2s(cr) #ת��Ϊ�ַ���

if __name__ == "__main__":

  message = "hi mom"
  print 'msg is :'+message+'\n'
  re = RSA()
  pub1,priv1 = re.keygen(l=512,s=False) #ͨ��c39��ĺ��������Կ

  rs = RSAsign()
  sign = rs.make(message,priv1) #���ú������sign��rsa����֮��Ľ��
  print 'rsa sign is :'+''.join(sign)+'\n'
  if rs.verify(message,sign,pub1): #����ط�����֤����ɹ������ok
    print "sign is correct \n"
  else:
    print 'sign is incorrect \n'

  signf = [ forging(message,pub1) ] #������ù�Կ����Ϣ���ǿ���α���һ��signf
  print 'signf is :'+''.join(signf)+'\n'
  if rs.verify(message,signf,pub1): #����ط�����֤
    print "sign is correct \n"
  else:
    print 'sign is incorrect \n'
