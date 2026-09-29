import zlib, struct, random, math, sys
W,H=1770,461
def png(path, rows):
    raw=b''.join(b'\x00'+r for r in rows)
    def ch(t,d): c=struct.pack('>I',len(d))+t+d; return c+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    open(path,'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',W,H,8,6,0,0,0))+ch(b'IDAT',zlib.compress(raw,9))+ch(b'IEND',b''))
def hx(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def make(path, core, edge, flip=True, transparent=True, seed=7):
    random.seed(seed); c1=hx(core); c2=hx(edge)
    cx=W/2; cy=H if flip else 0; rx=900; ry=330
    rows=[]
    for y in range(H):
        row=bytearray()
        for x in range(W):
            dx=(x-cx)/rx; dy=(y-cy)/ry; d=math.sqrt(dx*dx+dy*dy)
            a=max(0.0,1-d); a=(a**1.3)*1.25
            if a>0.9: a=0.9
            u=random.random()
            ae=a+(u-0.5)*(1.25*math.sqrt(max(a*(1-a),0))+0.10)
            ae=min(1.0,max(0.0,ae))
            t=min(1,d*1.1)
            col=[c1[i]*(1-t)+c2[i]*t for i in range(3)]
            if transparent:
                row+=bytes([int(col[0]),int(col[1]),int(col[2]),int(ae*255)])
            else:
                row+=bytes([int(255*(1-ae)+col[i]*ae) for i in range(3)])+b'\xff'
        rows.append(bytes(row))
    png(path,rows)
make('glow-accent.png','#A02538','#D46A7C')
make('glow-dark.png','#6E0D1F','#A8475A')
make('glow-accent-white.png','#A02538','#D46A7C',transparent=False)
make('glow-dark-white.png','#6E0D1F','#A8475A',transparent=False)
