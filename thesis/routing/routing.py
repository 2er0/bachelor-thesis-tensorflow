#!/usr/bin/env python
"""
Saving-Algorithmus
Routing in Pyhton

Step 1:
    - Init costmatrix
    - Init base routes
    - Init savings-list + check time windows
    - Order savings-list desc
Step 2:
    - Select top saving
    - Merge Routes
    - Check time windows
    - Clear no more available savings
    - Replace route a with new route a in savings
    - Calc savings-list + order desc
"""
import copy
from route import *
from util import *

node_de = node(0, 'DE', time_window(7, 19)) # -> Depot
node_a = node(1, 'A', time_window(10, 13)) # -> A
node_b = node(2, 'B', time_window(7, 19)) # -> B; Depot time window
node_c = node(3, 'C', time_window(8, 12)) # -> C
node_d = node(4, 'D', time_window(7, 19)) # -> D; Depot time window
node_e = node(5, 'E', time_window(8, 11)) # -> E


"""      DE,     A,       B,       C,       D,       E"""
d_mx = [[0,     24.14,  14.14,  10,     20,     10      ], # DE
        [24.14, 0,      10,     20,     24.14,  14.14   ], # A
        [14.14, 10,     0,      10,     20,     10      ], # B
        [10,    20,     10,     0,      22.36,  14.14   ], # C
        [20,    24.14,  20,     22.36,  0,      10      ], # D
        [10,    14.14,  10,     14.14,  10,     0       ]] # E

"""      DE,     A,       B,       C,       D,       E"""
t_mx = [[0,     869,    509,    360,    760,    360     ], # DE
        [869,   0,      450,    850,    909,    509     ], # A
        [509,   450,    0,      400,    727,    327     ], # B
        [350,   850,    400,    0,      619,    727     ], # C
        [760,   909,    727,    619,    0,      400     ], # D
        [360,   509,    327,    727,    400,    0       ]] # E

matrix = cost_matrix(d_mx, t_mx, 6)

print(matrix)

routes = []
routes.append(route([node_a], 0, node_de, t_mx))
routes.append(route([node_b], 1, node_de, t_mx))
routes.append(route([node_c], 2, node_de, t_mx))
routes.append(route([node_d], 3, node_de, t_mx))
routes.append(route([node_e], 4, node_de, t_mx))

savings = []
for item_a in routes:
    for item_b in routes:
        if item_a is not item_b:
            s = saving(
                    copy.deepcopy(item_a),
                    copy.deepcopy(item_b),
                    matrix)
            if s is not -1:
                savings.append(s)

savings = util.sort_savings(savings)
util.print_savings(savings)

while len(savings) > 0:
    saving = savings.pop(0)
    print('\nSelected Saving')
    util.print_savings([saving])

    route_b_id = saving.r_b.r_id
    route = saving.r_a
    route.add_stops(saving.r_b)

    print('\nMerged Routes')
    print(route)

    savings = [x for x in savings if x.r_b.r_id != route_b_id]
    savings = [x for x in savings if x.r_a.r_id != route_b_id]

    routes = [r for r in routes if r.r_id != route_b_id]

    for i in range(len(routes)):
        if routes[i].r_id == route.r_id:
            routes[i] = route

    for saving in savings:
        if saving.r_a.r_id == route.r_id:
            saving.r_a = route
        elif saving.r_b.r_id == route.r_id:
            saving.r_b = route

    savings = [x for x in savings if x.calc(matrix) is not -1]

    savings = util.sort_savings(savings)

    print('\nCurrentSaving & CurrentRoutes')
    util.print_savings(savings)

print('\n\t ---- Result ---- ')
print(routes)
