import math

# --------------- Accumulation --------------- 
def compound_acc(i, n, principal=1):
    return principal*(1 + i)**n


def simple_acc(i, n, principal=1):
    return  principal*(1 + i*n)


# --------------- Convertion of interst rates --------------- 
# ----- Accumultion -----
# To simple interest
def compound_int_to_simple_int(i, n=1):
    return (compound_acc(i, n) - 1)/n

# To compound interest
def simple_int_to_compound_int(i, n=1):
    return n*math.log(simple_acc(i, n))-1



# ----- Discounting -----
# To Discounting factor
def compound_int_to_discount_fac(i, n= 1):
    return ((1+i)**-1)**n
    
def discount_rat_to_discount_fac(d):
    return 1-d

# To discounting rates
def discount_fac_to_discount_rat(v, n=1):
    return  1 - v**n

def compound_int_to_discount_rat(i, n=1):
    return (i * compound_int_to_discount_fac(i))**n



# --------------- discounting --------------- 

def compound_dis(d, n, principal=1):
    return principal*(1-d)**n

def simple_dis(d, n, principal=1):
    return  principal*(1 - d*n)

def present_val(i, n=1, principal=1):
    return principal*(compound_int_to_discount_fac(i, n=n))