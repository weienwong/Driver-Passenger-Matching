import scipy.optimize
from utils import geo
from models import model

def populate_matrix(passengers, drivers):
    matrix=[]
    for p in passengers:
        row = []
        for d in drivers:
            row.append(geo.haversine_dist(p, d))
        matrix.append(row)
    return matrix    

def match(passengers, drivers):
    if len(passengers) == 0:
        raise TypeError("number of passengers cannot be zero")
    if len(drivers) == 0:
        raise TypeError("number of drivers cannot be zero")
    for p in passengers:
        if p.type != model.PersonType.PASSENGER:
            raise TypeError("passengers list contains a driver")
    for d in drivers:
        if d.type !=model.PersonType.DRIVER:
            raise TypeError("drivers list contains a passenger")

    m = populate_matrix(passengers, drivers)

    return zip_results(m, passengers, drivers)

def zip_results(m, passengers, drivers):
    row_ind, col_ind = scipy.optimize.linear_sum_assignment(m)
    results = []
    for i, j in zip(row_ind, col_ind):
        result = (passengers[i], drivers[j])
        results.append(result)
    return results
