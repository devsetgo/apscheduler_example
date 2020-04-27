# -*- coding: utf-8 -*-
import statistics
from random import randint


async def run_stats():

    data = []
    for _ in range(100):
        data.append(randint(1, 100))

    the_mean = statistics.mean(data)
    the_median = statistics.median(data)
    the_mode = statistics.mode(data)
    the_quantiles = statistics.quantiles(data)
    the_stdev = statistics.stdev(data)
    the_variance = statistics.variance(data, the_mean)
    result = {
        "mean": the_mean,
        "median": the_median,
        "mode": the_mode,
        "quantiles": the_quantiles,
        "stdev": the_stdev,
        "variance": the_variance,
        "values": data,
    }

    print(result)
    return result


async def run_addition():

    result: list = []
    for _ in range(5):

        v1 = randint(1, 1000)
        v2 = randint(1, 1000)
        add = v1 + v2
        result.append({"value1": v1, "value2": v2, "value": add})
    print(result)
    return result


async def happy_fourth():
    print("Happy Fourth of July!")
