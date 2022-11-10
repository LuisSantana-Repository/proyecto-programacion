import os, xlsxwriter
def ubicar():
    direccion=""
    
    while(os.path.isfile(direccion)==False or direccion.endswith(".txt")==False):
        direccion=input("Cual es la direccion del archivo?")
        if(os.path.isfile(direccion)==False):
            print("No es una drieccion de archivo")
        elif(direccion.endswith(".txt")==False):
            print("No es un archivo .txt")
    return(direccion)
            
            
def primerafila(exel):
    exel.write(0,0,"IP de red")
    exel.write(0,1,"IP de dispositivo")
    exel.write(0,2,"Mascara de red")
    exel.write(0,3,"IP de broadcast")
    exel.write(0,4,"N dispositivos")

def dividir(ip,mascara,linea):
    premascara=[""]*4
    if linea.strip():
        linea=linea.strip()
        print(linea)
        #generar mascara de red sin checar pasarse de 255
        if ("/" in linea):
            divicion=linea.split("/")
            print(divicion)
            if(divicion[1].isnumeric() and int(divicion[1])<32 and int(divicion[1])>0):
                print("Making mask")
                for a in range(int(divicion[1])+1):
                    premascara[a//8]+="1" 
                for a in range(int(divicion[1])+1,32):
                    premascara[a//8]+="0"
                print(premascara)
                for bits in range(len(premascara)):
                    premascara[bits]=str(int(premascara[bits],2))
                print(premascara)
            else:
                return True
        elif(" " in linea):
            divicion=linea.split(" ")
            premascara=divicion[1].split(".")
        else:
            return True
        
        #generar ip
        preip=divicion[0].split(".")
        print(preip)
        #checar valores
        if(len(premascara)==4 and len(preip)==4):
            print("correct intervals")
            for a in range(4):
                if(preip[a].isnumeric() and premascara[a].isnumeric() and (int(preip[a])>=0 and int(preip[a])<=255) and (int(premascara[a])>=0 and int(premascara[a])<=255)):  
                    print("correct range",a)
                    ip[a]=int(preip[a])
                    if(premascara[a]!=0 and (a==0 or int(premascara[a-1])==255)):
                        print("correct mask",a)
                        mascara[a]=int(premascara[a])
                    else:
                        print("incorrect mask",a)
                        return True
                else:
                    print("incorrect range",a)
                    return True  
        else:
            print("incorrect intervals")
            return True
    else:
        print("no ip")
        return True
    return False
    


def ipred(ip,mascara,red):
    for interval in range(4):
        red[interval]=ip[interval]&mascara[interval]
    print(red)

def ipbroadcast(red,mascara,broadcast):
    mascaraBrodcast=[0]*4
    for interval in range(4):
        mascaraBrodcast[interval]=((~mascara[interval]) & 0xff )
        broadcast[interval]=red[interval]+mascaraBrodcast[interval]
    print(mascaraBrodcast)
    print(broadcast)

def ndispositivos(mascara):
    dispositivos=1
    for interval in range(4):
        dispositivos*=((~mascara[interval]) & 0xff )+1
    print(dispositivos)
    return dispositivos


def imprimir(red,mascara,ip,broadcast,dispositivos,contador,Exel):
    Exel.write(contador,0,".".join(map(str,red)))
    if(red==ip or broadcast==ip):
        Exel.write(contador,1,"N/A")
    else:
        Exel.write(contador,1,".".join(map(str,ip)))
    Exel.write(contador,2,".".join(map(str,mascara)))
    Exel.write(contador,3,".".join(map(str,broadcast)))
    Exel.write(contador,4,dispositivos)

direccion=ubicar()
documento=open(direccion,'r')
workbook=xlsxwriter.Workbook('IPV4.xlsx')
Exel=workbook.add_worksheet()
primerafila(Exel)
contador=1
for textLine in documento:
    n1=0
    n2=0
    ip=[0]*4
    mascara=[0]*4
    red=[0]*4
    broadcast=[0]*4
    Error=dividir(ip,mascara,textLine)
    print(Error,ip,mascara)
    if(Error==False):
        ipred(ip,mascara,red)
        ipbroadcast(red,mascara,broadcast)
        dispositivos=ndispositivos(mascara)
        imprimir(red,mascara,ip,broadcast,dispositivos,contador,Exel)
    else:
        Error=True
        Exel.write(contador,0,"informacion erronea o insuficiente")
    contador+=1
workbook.close()