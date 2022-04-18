# This code was created as a part of the MITx 6.0002 course

import numpy as np
import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a numpy 1-d array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]


def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).
    Args:
        x: a list with length N, representing the x-coords of N sample points
        y: a list with length N, representing the y-coords of N sample points
        degs: a list of degrees of the fitting polynomial
    Returns:
        a list of numpy arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    ellisto = []
    for i in degs:
        if len(degs) == 1:
            fit = np.polyfit(x, y, degs[0])
            ellisto.append(fit)
            return ellisto
        fit = np.polyfit(x, y, degs[i-1])
        ellisto.append(fit)
    return ellisto

#print(generate_models([1961, 1962, 1963],[4.4,5.5,6.6],[1, 2]))
#print(generate_models([1900, 1901, 1902, 1904, 2000], [32.0, 42.0, 31.3, 22.0, 33.0], [2]))

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    Args:
        y: list with length N, representing the y-coords of N sample points
        estimated: a list of values estimated by the regression model
    Returns:
        a float for the R-squared error term
    """
    y = np.array(y)
    est = np.array(estimated)

    sumSquared = ((est-y)**2).sum()
    avg = (y.sum())/(len(y))
    avgSquared = ((avg-y)**2).sum()
    rSquared = (1 - (sumSquared/avgSquared))

    return rSquared

def evaluate_models_on_training(x, y, models):
    """
    Args:
        x: a list of length N, representing thvirusPopulation = [0 for _ in range(300)]
        y: a list of length N, representing the y-coords of N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.
    Returns:
        None
    """
    xVals = pylab.array(x)
    yVals = pylab.array(y)
    for i in models:
        pylab.plot(xVals, yVals, 'bo')
        pylab.title('San Francisco Average Annual Temp')
        pylab.xlabel('Year')
        pylab.ylabel('Temp / Celsius')
        a,b = models[0][0], models[0][1]
        estYVals = a*xVals + b
        pylab.plot(xVals, estYVals, label = 'R^2 =' + str(round(r_squared(yVals, estYVals),5)))
        pylab.legend(loc = 'best')
        pylab.show()

# ------------------------------------------------- #

raw_data = Climate('data.csv')
INTERVAL_1 = list(range(1961, 2006))
INTERVAL_2 = list(range(2006, 2016))
FULL_INTERVAL = list(range(1961, 2016))

#  Plots the results of a linear regression of average daily temps in a given area
"""
x0 = FULL_INTERVAL
x1 = INTERVAL_1
x2 = INTERVAL_2
y = []
for year in x0:
    y.append(raw_data.get_daily_temp('SAN FRANCISCO', 4, 19, year))
models = generate_models(x0, y, [1])
evaluate_models_on_training(x0, y, models)
"""

# Plots the results of a linear regression of average annual temps in a given area

x0 = FULL_INTERVAL
x1 = INTERVAL_1
x2 = INTERVAL_2
y = []
for year in x0:
    y.append(np.mean(raw_data.get_yearly_temp('SAN FRANCISCO', year)))
models = generate_models(x0, y, [1])
evaluate_models_on_training(x0, y, models)
