def soma(v1, v2):
    try:
        print(f"{float(v1):.2f}+{float(v2):.2f} = {float(v1+v2):.2f} ")
    except:
        print("Ocorreu um erro.")
def sub(v1, v2):
    try:
        print(f"{float(v1):.2f}-{float(v2):.2f} = {float(v1-v2):.2f} ")
    except:
        print("Ocorreu um erro.")
def mult(v1, v2):
    try:
        print(f"{float(v1):.2f}*{float(v2):.2f} = {float(v1*v2):.2f} ")
    except:
        print("Ocorreu um erro.")
def div(v1, v2):
    try:
        print(f"{float(v1):.2f}/{float(v2):.2f} = {float(v1/v2):.2f} ")
    except ZeroDivisionError:
        print("Não é possível dividir por ZERO.")
    except:
        print("Ocorreu um erro.")