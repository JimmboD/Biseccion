#Funcion
def f(x):
    r=1.25
    s=0.1
    return (x**3)-3*r*(x**2)+4*(r**3)*s

#Variables
a=0
b=2.5
n=50
tol=0.0001
i=0
c=a+b/2

#Encabezado
print(f"{'i':>3} | {'a':>8} | {'b':>8} | {'c':>8} | {'f(a)':>8} | {'f(b)':>8} | {'f(c)':>8} | {'Residual':>8}")
print("-" * 80)


# Forma de recurrencia
while (abs(f(c))>tol) and i < n:

    #Punto medio
    c=(a+b)/2

    print(f"{i:>3} | {a:>8.4f} | {b:>8.4f} | {c:>8.4f} | {f(a):>8.4f} | {f(b):>8.4f} | {f(c):>8.4f} | {abs(f(c)):>8.4f}")

    #Cambios de intervalo
    if (f(a)*f(c)<0):
        b=c
    else:
        a=c

    #Contador
    i+=1

print(f"Raiz aproximada: ",c)