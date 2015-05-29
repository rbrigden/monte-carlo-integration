import random as rand
import math
from decimal import *
import time
from numpy import *
import sys

# basic monte carlo integration 
def monte_carlo(function, darts, start, end):
    runs = darts
    points = []
    
    # base of A' from a -> b
    a = start
    b = end
    
    # top of the 'dartboard'
    top = get_max_value(function, a, b)
    # bottom of the 'dartboard'
    bottom = get_min_value(function, a, b)
    
    
    # generate random x and y; check if y value is bounded by f(x) or not
    # counting array: x-position, y-position, bounded by curve (bool)
    for i in range(runs):
        x = a  + rand.random() * (b-a)
        y = rand.random() * abs(top-bottom) + bottom
        if y >= 0:
            if y <= function(x):
                points.append([x,y,True])
            else:
                points.append([x,y,False])
        if y < 0:
            if y >= function(x):
                points.append([x,y,True])
            else:
                points.append([x,y,False])

    area = 0
    area_prime = abs(b-a) * abs(top-bottom)
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

# monte carlo integration for function that is both negative and positive between the interval
def monte_carlo_neg(function, darts, start, end):
    # create arrays for return
    x_points_in, y_points_in, x_points_out, y_points_out = ([] for i in range(4))
    # total bounded area
    bounded_area = 0
    # find the zeroes to break into multiple functions
    zeroes = find_zeroes(function, start, end)
    zeroes.append(start)
    zeroes.append(end)
    zeroes = sorted(zeroes)
    for i in range(len(zeroes)-1):
        a = zeroes[i] 
        b = zeroes[i+1]
        mid = (a + b)/2
        result = monte_carlo(function, darts/len(zeroes), a, b)
        
        if (function(mid) >= 0):
            bounded_area += result['integration']
        else:
            bounded_area -= result['integration']
            
        x_points_in +=  result['x_points_in']
        y_points_in +=  result['y_points_in']
        x_points_out +=  result['x_points_out']
        y_points_out +=  result['y_points_out']
        
    return dict(x_points_in=x_points_in, 
                y_points_in=y_points_in, 
                x_points_out=x_points_out, 
                y_points_out=y_points_out,
                integration=bounded_area,
                darts=darts)

# using average value theorem and monte-carlo method to evaluate integral
def monte_carlo_avg_val(function, runs, start, end):
    # value lists
    x_values = []
    y_values = []
    
    # total for calc of average value
    total = 0
    
    # bounds of integration
    a = start
    b = end
    
    # generate random x values and calculate function values
    # Append data to value lists
    for i in range(runs):
        x = a  + rand.random() * (b-a)
        x_values.append(x)
        y_values.append(function(x))
        
    for val in y_values:
        total += val
        
    # average function value
    average = total / len(y_values)
    
    return average * abs(b-a)

# riemann sum (type = [righthand, lefthand, midpoint)
def riemann_sum(function, divisions, start, end, method):
    x = start
    area = 0
    division = 1.0 * divisions
    dx = Decimal(abs(start-end)) / Decimal(divisions)
    if method == 'lefthand':
        for i in range(divisions):
            area += dx * Decimal(function(x))
            x += dx
    elif method == 'righthand':
        for i in range(divisions):
            x += dx
            area += dx * Decimal(function(x))
    elif method == 'midpoint':
        for i in range(divisions):
            area += dx * Decimal(function(x + dx/2))
            x += dx
    else:
        return "error, method fault [lefthand, righthand or midpoint]"
    return area

    
         
def average_error(function, darts, start, end, runs, true_value):
    sum = 0
    for i in range(runs):
        result = monte_carlo(function, darts, start, end)
        sum += abs(1 - Decimal(result['integration'])/Decimal(true_value))
    return (sum / Decimal(runs)) * 100

def average_time(function, darts, start, end, runs):
    sum = 0
    for i in range(runs):
        start = time.clock()
        monte_carlo(function, darts, start, end)
        end = time.clock()
        sum += abs(end - start)
    return (sum / runs)

def get_max_value(func, start, end):
    numlist = arange(start, end, 0.001)
    max_value = -sys.maxint - 1
    numlist = map(func, numlist)
    for num in numlist:
        if num >= max_value:
            max_value = num
    return max_value

def get_min_value(func, start, end):
    numlist = arange(start, end, 0.001)
    min_value = sys.maxint
    numlist = map(func, numlist)
    for num in numlist:
        if num <= min_value:
            min_value = num
    return min_value
    
def find_zeroes(function, start, end):
    num_range = arange(start, end, 0.0001)
    zeroes = []
    for num in num_range:
        if function(num) * function(num-0.0001) < 0:
            zeroes.append((num + num-0.0001)/2)
    return zeroes




            

        

