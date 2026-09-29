import zlib, struct, random, math, sys
def read_png(p):
    d=open(p,'rb').read(); assert d[:8]==b'\x89PNG\r\n\x1a\n'; i=8; idat=b''
    while i<len(d):
        l=struct.unpack('>I',d[i:i+4])[0]; t=d[i+4:i+8]; c=d[i+8:i+8+l]; i+=12+l
        if t==b'IHDR': W,H,bd,ct,_,_,il=struct.unpack('>IIBBBBB',c)
        elif t==b'IDAT': idat+=c
    assert bd==8 and il==0 and ct in (2,6); bpp=3 if ct==2 else 4
    raw=zlib.decompress(idat); stride=W*bpp; rows=[]; prev=bytearray(stride); p=0
    for y in range(H):
        f=raw[p]; line=bytearray(raw[p+1:p+1+stride]); p+=1+stride
        if f==1:
            for x in range(bpp,stride): line[x]=(line[x]+line[x-bpp])&255
        elif f==2:
            for x in range(stride): line[x]=(line[x]+prev[x])&255
        elif f==3:
            for x in range(stride): line[x]=(line[x]+((line[x-bpp] if x>=bpp else 0)+prev[x])//2)&255
        elif f==4:
            for x in range(stride):
                a=line[x-bpp] if x>=bpp else 0; b=prev[x]; c=prev[x-bpp] if x>=bpp else 0
                pa=abs(b-c); pb=abs(a-c); pc=abs(a+b-2*c)
                pr=a if (pa<=pb and pa<=pc) else (b if pb<=pc else c)
                line[x]=(line[x]+pr)&255
        rows.append(line); prev=line
    return W,H,bpp,rows
def write_png(p,W,H,rows):
    raw=b''.join(b'\x00'+bytes(r) for r in rows)
    def ch(t,d): c=struct.pack('>I',len(d))+t+d; return c+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    open(p,'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',W,H,8,6,0,0,0))+ch(b'IDAT',zlib.compress(raw,9))+ch(b'IEND',b''))
src,dst,core=sys.argv[1],sys.argv[2],sys.argv[3]
cr,cg,cb=(int(core[i:i+2],16) for i in (1,3,5))
W,H,bpp,rows=read_png(src); random.seed(11); out=[]
for y in range(H):
    r=rows[y]; o=bytearray(W*4)
    for x in range(W):
        R,G,B=r[x*bpp],r[x*bpp+1],r[x*bpp+2]
        a=(255-G)/(255-cg); a=(a-0.09)/0.91   # насколько пиксель «бордовый»; почти белое считаем белым
        a=0.0 if a<0 else (1.0 if a>1 else a)
        if a>0.004:
            # чистый цвет этого места (без примеси белого)
            pr=255-(255-R)/a; pg=255-(255-G)/a; pb=255-(255-B)/a
            pr=min(255,max(0,pr)); pg=min(255,max(0,pg)); pb=min(255,max(0,pb))
            w=min(1.0,a*1.6)   # на краях берём фирменный цвет, а не вычисленный (иначе серые/бирюзовые точки)
            pr=cr*(1-w)+pr*w; pg=cg*(1-w)+pg*w; pb=cb*(1-w)+pb*w
        else: pr,pg,pb=cr,cg,cb
        u=random.random()
        ae=a+(u-0.5)*(1.3*math.sqrt(a*(1-a))+0.16)
        ae=0.0 if ae<0 else (1.0 if ae>1 else ae)
        o[x*4]=int(pr); o[x*4+1]=int(pg); o[x*4+2]=int(pb); o[x*4+3]=int(min(1.0,a*5.0)*255) if a>0.02 else 0
        if a>0.02: o[x*4]=int(255*(1-ae)+pr*ae); o[x*4+1]=int(255*(1-ae)+pg*ae); o[x*4+2]=int(255*(1-ae)+pb*ae)
    out.append(o)
write_png(dst,W,H,out)
print('ok',W,H)
