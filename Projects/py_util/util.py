import matplotlib.pyplot as plt
import numpy as np


def print_version(pkg_dict):
    for k, v in pkg_dict.items():
        print(k + ': ' + v.__version__)