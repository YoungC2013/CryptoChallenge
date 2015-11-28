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
int main()
{
    ini(52);                                //ʹ������һ�����ӽ��г�ʼ��
    for(int i=0;i<5;i++)
    {
        cout<<extNum()<<endl;
    }
    return 0;
}
