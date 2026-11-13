"""Mini-game by CAN YILDIRIM · Hugging Games."""
import random
import math

def reply(state, message):
    return state, message

def finish(state, message):
    state["done"] = True
    return state, message + "\n🏁 Oyun bitti. Yeniden başlat ile tekrar oyna."

def _spawn(b):
    cells=[i for i,x in enumerate(b) if x==0]
    if cells:b[random.choice(cells)]=2 if random.random()<.9 else 4
def _view(b):return '\n'.join(' '.join(f'{v:4d}' if v else '   ·' for v in b[i:i+4]) for i in (0,4,8,12))
def new_game():
    b=[0]*16;_spawn(b);_spawn(b)
    return {'board':b,'score':0,'done':False},"2048: yukarı/aşağı/sol/sağ yaz.\n"+_view(b)
def _merge(vals):
    a=[x for x in vals if x];out=[];gain=0;i=0
    while i<len(a):
        if i+1<len(a) and a[i]==a[i+1]:out.append(2*a[i]);gain+=2*a[i];i+=2
        else:out.append(a[i]);i+=1
    return out+[0]*(4-len(out)),gain
def play(s,action):
    if s['done']:return reply(s,'Yeni oyun başlat.')
    a=action.strip().lower();dirs={'sol':0,'sağ':1,'sag':1,'yukarı':2,'yukari':2,'aşağı':3,'asagi':3}
    if a not in dirs:return reply(s,'sol, sağ, yukarı, aşağı yaz.')
    d=dirs[a];b=s['board'];out=b[:];gain=0
    for j in range(4):
        ids=([4*j+i for i in range(4)] if d<2 else [4*i+j for i in range(4)])
        if d in (1,3):ids=ids[::-1]
        merged,g=_merge([b[i] for i in ids]);gain+=g
        for i,v in zip(ids,merged):out[i]=v
    if out==b:return reply(s,'Bu yönde hamle yok.\n'+_view(b))
    s['board']=out;s['score']+=gain;_spawn(out)
    msg=f"Puan: {s['score']}\n"+_view(out)
    if max(out)>=2048:return finish(s,'🏆 2048!\n'+msg)
    if 0 not in out and all(out[y*4+x]!=out[y*4+x+1] for y in range(4) for x in range(3)) and all(out[y*4+x]!=out[(y+1)*4+x] for y in range(3) for x in range(4)):
        return finish(s,'Oyun bitti!\n'+msg)
    return reply(s,msg)
