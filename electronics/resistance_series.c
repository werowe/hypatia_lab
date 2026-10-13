# circuit https://everycircuit.com/circuit/5486623643009024


r1 = 6
 

r2 = 1000

r_tot = r1 + r2


v = 120

'''
ohms law
calculate relationship between voltage and resistance
v = i * r

so i = v / r1

so i current is:

'''

f"initial voltage %.2f{v}"

i = v / r_tot

print("current in amps", i)

v_r1 = i * r1
v_r2 = i * r2

print(f"voltage drop at  % {v_r1:.5f}")

print(f"voltage drop at % {v_r2:.5f}")

'''
Kirchhoffs voltage law says the voltage drops across
 two resistors in series add up to the supply voltage:

so 120 = v_r1 + v_r2


'''
 

print(f"check {v - v_r1 - v_r2:.4f}")
