#include <bits/stdc++.h>
using namespace std;


//д��ǰ��
//�˴�����ȫ�������ϵ�α����д�����ڲ�����ѧԭ�����ܿ���
long long mt[624];
int idx=0;
const long long l32=(1LL<<32)-1;
const long long l31=(1LL<<31)-1;
const long long nd32=(1LL<<32);
void ini(long long seed)                    //��ʼ��������ʹ��ǰ��Ҫ����
{
    idx=0;
    mt[0]=seed;
    for(int i=1;i<624;i++)
    {
        mt[i]=(1812433253LL*((mt[i-1]^(mt[i-1]>>30))+i))&(l32);
    }
}
void geneNum()                              //�㷨�е�һЩ����ѧ�任
{
    for(int i=0;i<624;i++)
    {
        int y=(mt[i]&nd32)+((mt[(i+1)%624])&l31);
        mt[i]=mt[(i+397)%624]^(y>>1);
        if(y&1)
        {
            mt[i]^=(2567483615LL);
        }
    }
}
long long extNum()                          //��ȡ�õ��������
{
    if(idx==0)
    {
        geneNum();
    }
    long long y=mt[idx];
    y^=(y>>11);
    y^=((y<<7)&(2636928640LL));
    y^=((y<<15)&(4022730752LL));
    y^=(y>>18);
    idx=(idx+1)%624;
    return y;
}
string enc(string p)
{
    string res="";
    for(int i=0;i<p.length();i++)                    //��mt19937�������������ctr�ļ���
    {
        int now=extNum();
        res+=p[i]^(now&255);
    }
    return res;
}
int main()
{
    string pt="AAAAAAAAAAAAAAAA";            //���õ�����
    string ct;                               //����
    int key=0;
    for(int i=0;i<16;i++)
    {
        key+=(rand()%2)*(1<<i);              //����һ��16λ��key
    }
    ini(key);
    ct=enc(pt);
    for(int k=0;k<(1<<16);k++)               //����ö�ٿ��ܵ�key
    {
        ini(k);
        if(enc(pt)==ct)
        {
            printf("the key is %d\n",k);
            break;
        }
    }
    return 0;
}
