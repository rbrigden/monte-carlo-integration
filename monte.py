import random as rand
import math
from decimal import *
def monte_carlo(function, darts, start, end):
    runs = darts
    points = []
    
    # base of A' from a -> b
    a = start
    b = end
    # height of enclosed box base -> height
    height = function(b)
    
    # generate random x and y; check if y value is bounded by f(x) or not
    for i in range(runs):
        x = a  + rand.random() * (b-a)
        y = rand.random() * height
        if y < function(x):
            points.append([x,y,True])
        else:
            points.append([x,y,False])

    area = 0
    area_prime = b * height
    points_within = 0
    points_outside = 0
    
    # count the points bounded and unbounded by the curve
    for i in points:
        if i[2]:
            points_within += 1
        elif not i[2]:
            points_outside += 1
    
    # calculate the best estimate of the integral using our previous formula: A = N/N' * A'
    area = (Decimal(points_within) / Decimal(points_outside + points_within)) * Decimal(area_prime)

    x_points_in, y_points_in, x_points_out, y_points_out = ([] for i in range(4))
    
    # add points for plotting
    for i in points:
        if i[2]:
            x_points_in.append(i[0])
            y_points_in.append(i[1])
        elif not i[2]:
            x_points_out.append(i[0])
            y_points_out.append(i[1])
        
    
    
    return dict(x_points_in=x_points_in, 
                y_points_in=y_points_in, 
                x_points_out=x_points_out, 
                y_points_out=y_points_out,
                integration=area,
                darts=runs)
        

