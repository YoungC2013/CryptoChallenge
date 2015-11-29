#! --coding:utf-8-- !# 
import hashlib
import random

f_length = 2 # bytes
g_length = 3#ע���������������ĳ����ǲ�һ����
fg_blocksz = 16
f_initial = 'lo'
g_initial = 'lol'
#�����single �Ļ����Ͼ��Ƕ����һ��������ԭ����һ��c�����c_f,c_g
def C_f(m, H):
    r = hashlib.md5(H + m).digest()[:f_length]
    return r

def C_g(m, H):
    # just truncated md5
    r = hashlib.md5(H + m).digest()[:g_length]
    return r

def pad(m):#����������ǰ�m�ֳɿ�
    for i in range(0, len(m), fg_blocksz):
        yield m[i:i+fg_blocksz]
    yield 'length:%d' % (len(m))

def generic_h(m, initial, C): #����Ƿ��ض�ÿ��������Ľ����c���㷨������c_f,����c_g
    H = initial

    for block in pad(m):
        H = C(block, H)
    return H

def f(m):
    return generic_h(m, f_initial, C_f)
def g(m):
    return generic_h(m, g_initial, C_g)
def h(m):
    return f(m) + g(m)

def random_block(): #�������ֵ
    return ''.join(chr(random.getrandbits(8)) for i in range(fg_blocksz))

def internal_collide(H, C): #�õ���ײ����single�л���һ��
    x = random_block()

    xH = C(x, H)
    while True:
        y = random_block()
        yH = C(y, H)
        if xH == yH and x != y:
            return x, y, xH, yH

def crosscheck(found, H):
    # ��single�в��ĺ�����
    left = ''.join(x[0] for x in found)
    right = ''.join(x[1] for x in found)
    assert H(left) == H(right)

def generate_messages(found):
    if len(found) == 0:
        yield ''
    else:
        x, y = found[0]
        for suffixes in generate_messages(found[1:]):
            yield x + suffixes
            yield y + suffixes

def find_dual_collision(): #�ҵ���ײ���ұ���
    H_f = f_initial
    found = []
    for i in range(g_length * 8):
        # ����һ�������ײ����
        x, y, xh, yh = internal_collide(H_f, C_f)
        found.append((x, y))
        H_f = xh

    crosscheck(found, f)

    #����ҵ���ײ����ʾ
    check = {}
    for msg in generate_messages(found):
        gh = g(msg)

        collision = check.setdefault(gh, msg)
        if collision != msg: #�������ʾ�Ƿ��ҵ���ײ
            assert h(collision) == h(msg)
            print 'found collision after', len(check), 'g tests'
            break
    
if __name__ == '__main__':
    find_dual_collision()