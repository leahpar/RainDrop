from scipy.optimize import fsolve
# apt-get install python-scipy

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#   REFLEX TIMING
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
#    | R0u          R0d       R1u                               R1d          T
#    |   +-----------+         +---------------------------------+           #
#    |   |           |         |                                 |           #
#  --+---+-----------+---/ /---+---------------------------------+-----------#-----> t
#    0    <---dR0--->           <-----------------DR1-----------> <---dr---->#
#                                                                            #
#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#   VALVE TIMING
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#
#    |                        G1u    G1d  G2u    G2d                         T
#    |                         +------+    +------+           TG1    TG2     #
#    |                         |      |    |      |                          #
#  --+-------------------------+------+----+------+------------X------X------#-----> t
#    0                         <--------------dG--------------> <----dt1---->#
#                              <-dVg-->    <-dVg-->                   <-dt2->#
#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Drop vars
t5 = -50          #    t5  |         __                       
t0 = 0            #      \ |        /  \                      
t1 = 50           #       \|t0     / t3 \                     
t2 = 100          #   -----+------/------+----------------> t 
t3 = 150          #        |\ t1 /t2     t4                   
t4 = 200          #        | \__/                             

# Total duration
T = 3000

# Reflex vars
dR = 100          # delay between trigger off and actual flash
DR1 = 1000        # "long" exposuer
DR0 = 1000        # time for miror to stabilise

# Valve vars
dG = 320          # falling time of a drop (dG = sqrt((2 * 0.5m) / g(= 9.81))
dVg = 50          # valve aperture time for a drop
dt1 = t3          # state of drop G1 at shot
dt2 = t5          # state of drop G2 at shot

def reflex_eq(var):
	""" reflex equations """ 
	R0u, R0d, R1u, R1d = var[0], var[1], var[2], var[3]
	eq1 = T - dR - R1d
	eq2 = R1d - DR1 - R1u
	eq3 = R1u - DR0 - R0u
	eq4 = R0u + dR - R0d
	res = [eq1, eq2, eq3, eq4]
	return res
	
def valve_eq(var):
	""" valve equation """
	G1u, G1d, G2u, G2d = var[0], var[1], var[2], var[3]
	eq1 = (T - dt1) - dG - G1u # (T - dt) = TG1
	eq2 = (T - dt2) - dG - G2u # (T - dt) = TG2
	eq3 = G1u + dVg - G1d
	eq4 = G2u + dVg - G2d
	res = [eq1, eq2, eq3, eq4]
	return res

# Solve reflex timing equations
reflex_eq_sol = fsolve(reflex_eq, [0, 0, 0, 0])

# Solve valve timing equations
valve_eq_sol = fsolve(valve_eq, [0, 0, 0, 0])

print "Reflex timing :"
print reflex_eq_sol
print "Valve timing :"
print valve_eq_sol

# make the ordered timetable
timetable = []
state_reflex = True
state_valve = True

i = 0
j = 0

R = 23
V = 24

while True:
	if i == len(reflex_eq_sol) and j == len(valve_eq_sol):
		break
	elif j == len(valve_eq_sol):
		timetable.append((reflex_eq_sol[i], R, state_reflex))
		state_reflex = not state_reflex
		i += 1
	elif i == len(reflex_eq_sol):
		timetable.append((valve_eq_sol[j], V, state_valve))
		state_valve = not state_valve
		j += 1
	elif reflex_eq_sol[i] < valve_eq_sol[j]:
		timetable.append((reflex_eq_sol[i], R, state_reflex))
		state_reflex = not state_reflex
		i += 1
	else:
		timetable.append((valve_eq_sol[j], V, state_valve))
		state_valve = not state_valve
		j += 1

print timetable


import datetime
import time as time
current_milli_time = lambda: int(round(time.time() * 1000))
log_t = current_milli_time()

t = 0
tt = 0
while True:
	if len(timetable) == 0:
		break
	dt, pin, state = timetable[0]
	print (current_milli_time() - log_t), tt, dt, pin, state
	time.sleep((dt-t)/1000.0)
	tt += dt - t
	t = dt
	
	timetable.pop(0)

print 'done'




