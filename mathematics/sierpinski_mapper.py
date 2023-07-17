# Creates a Sierpinski Triangle using PyPlot.

import matplotlib.pyplot as plt
import numpy as np

def sierpinski_gasket(n):
    # three vertices of the initial triangle
    vertices = np.array([[0, 0], [0.5, np.sqrt(3)/2], [1, 0]])

    # empty list to store the points of the gasket
    points = []

    # choose random starting point within  triangle
    point = np.array([0.5, 0.5])

    # perform chaos game to generate gasket
    for i in range(n):
        vertex = vertices[np.random.randint(3)]
        point = (point + vertex) / 2
        points.append(point)

    # plot
    points = np.array(points)
    plt.scatter(points[:,0], points[:,1], s=1, c='k')
    plt.axis('equal')
    plt.axis('off')
    plt.show()

# n=100000 points
sierpinski_gasket(100000)
