#include <bits/stdc++.h>
using namespace std;


//д��ǰ��
//�˴�����ȫ�������ϵ�α����д�����ڲ�����ѧԭ�����ܿ���
long long mt[624];
long long out[624];
int idx=0;
const long long l32=(1LL<<32)-1;
const long long l31=(1LL<<31)-1;
const long long nd32=(1LL<<32);
int err=0;
void ini(long long seed)                    //��ʼ��������ʹ��ǰ��Ҫ����
{
    idx=0;
    mt[0]=seed;
    for(int i=1; i<624; i++)
    {
        mt[i]=(1812433253LL*((mt[i-1]^(mt[i-1]>>30))+i))&(l32);
    }
}
void geneNum()                              //�㷨�е�һЩ����ѧ�任
{
    for(int i=0; i<624; i++)
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
void rev()
{
    long long x=out[idx],cv;                             //����Ϊ�ָ�����
    x^=(x>>18);
    x^=((x<<15) & 4022730752LL);
    cv=x;
    x^=((x<<7) & 2636928640LL);
    for(long long i=0; i<64; i++)                        //����ö�ٶ�ʧ��6λ
    {
        long long tv = x ^ (((i & 32)<<26) + ((i & 16)<<24) + ((i & 8) <<23) + ((i & 4)<<19) + ((i & 2)<<18) + ((i & 1)<<14));
        //long long tv = x ^ (((i & 32)<<20) + ((i & 16)<<19) + ((i & 8) <<19) + ((i & 4)<<16) + ((i & 2)<<16) + ((i & 1)<<13));
        if ((tv ^ ((tv << 7) & 2636928640LL)) == cv)
        {
            x = tv;
            break;
        }
    }
    cv=x;
    x^=(x>>11);
    for(long long i=0; i<1024; i++)                      //����ö�ٶ�ʧ��10λ
    {
        long long tv=x^i;
        if((tv^(tv>>11))==cv)
        {
            x=tv;
            break;
        }
    }
    if(x!=mt[idx])                              //���ڼ������Ƿ��д�����ָ�����x�����ڶ�Ӧ��mt[idx]�򱨴�
    {
        puts("Error");
        err++;
    }
    idx=(idx+1)%624;
}
int main()
{
    ini(52);
    for(int i=0; i<624; i++)                    //���624�����
    {
        out[i]=extNum();
    }
    for(int i=0; i<624; i++)                    //�ָ�624��״̬
    {
        rev();
    }
    cout<<err<<endl;
    return 0;
}
