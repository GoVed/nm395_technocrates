
lat=25.4 # 25 to 26.2
long=90 # 89 to 93

cx=4505/1.2
cy=14844/4

lat-=25
long-=89

x=int(lat*cx)
y=int(long*cy)

pid=1

if y>7168:
    pid+=1
    y-=7168

if y>7168:
    pid+=1
    y-=7168
  
x/=100
y/=100

x=int(x)
y=int(y)
sid=0
if pid==1 or pid==2:
    sid=(x*46)+y
else:
    sid=(x*6)+y
year=2000
month="01"
filepath=str(year)+month+str(pid)+"_"+str(sid)

