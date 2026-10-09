# Ele AND gate
# open top toggle
# power flows through base on bottom resistor

# https://everycircuit.com/circuit/6192963629744128/and-gate


# 5 volts
v = 5

# resistance of each resistor
r1 = 1000  
 

# OHMS law
# V = I x R
#
# so I = V / R


v_transistor_base = 0.782  # forward bias, read from chart


print(f"volts through transistor base {v_transistor_base} volts\n")
 

i = v_transistor_base / r1

print(f"current at r1 {i} amps\n")
 

# voltage drop at r1
# if old voltage - drop in voltage due to 
# resistance = new voltage aka potential voltage

v_r1 = v - v_transistor_base

# current at r1
i_r1 = v_r1 / r1

print(f"current at i_r1  ={i_r1 * 1000} miliamps\n")

# where did voltage at transistor base come from: diode calculation

 # pico amps.  transistor is not a perfect switch.  it leaks
