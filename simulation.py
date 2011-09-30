import numpy

# {{{ Global constants

# No. of Simulations
TIMES = 100

# Lambda
LAMBDA = 2

# Stop-time
STOP_TIME = 100

# weather period
WEATHER_PERIOD = 3

# Good weather period
GOOD_WEATHER_PERIOD = 2

# infinity
INFINITY = 10000

# }}}

# First arrival of the message after time T0
def poisson_arrival(T0):
    random = numpy.random.uniform(0,1)
    return T0 - (1.0/LAMBDA)*numpy.log(random)

# Returns 1 for 'Good' weather or 0 for 'Rough' weather
def weather(time):
    if int(time)%WEATHER_PERIOD == GOOD_WEATHER_PERIOD:
        return 0
    return 1

# Simulates 'size' times
def simulation(size):
    results=[]
    for x in xrange(size):
        departureTime = [INFINITY, INFINITY, INFINITY]
        availability = [1,1,1]
        arrivalTime = poisson_arrival(0)
        time = arrivalTime
        lost = 0

        while time < STOP_TIME:
            # {{{ Simulate the arrival of the new message
            if arrivalTime < min(departureTime):
                time = arrivalTime
                if sum(availability) > 0:
                    currWeather = weather(time)
                    Y = numpy.random.uniform(0,1)
                    if currWeather is 0:
                        Y = Y**(0.33)
                    for y in xrange(len(availability)):
                        if availability[y] is 1:
                            departureTime[y] = time+Y
                            availability[y] = 0
                            break
                else:
                    lost += 1
                arrivalTime = poisson_arrival(time)
            # }}}
            # {{{ Simulate the departure of one of the pending messages
            else:
                time = min(departureTime)
                for var in xrange(len(availability)):
                    if departureTime[var] <= min(departureTime):
                        departureTime[var] = INFINITY
                        availability[var] = 1
                        break
            # }}}

        results.append(lost)
        print "Sample #"+str(x+1),lost
    print "# Samples:",str(len(results)) + ", Result:",sum(results)*1.0/len(results)

if __name__ == '__main__':
    simulation(TIMES)
