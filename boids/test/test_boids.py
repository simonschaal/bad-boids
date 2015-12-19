from ..boids import Boids
from nose.tools import assert_almost_equal, assert_equal
import os
import yaml
import numpy as np

def test_bad_boids_regression():
    boids=Boids(0)
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixtures','fixture.yml')))
    boid_data=regression_data["before"]
    positions=np.array([boid_data[0], boid_data[1]])
    velocities=np.array([boid_data[2], boid_data[3]])
    boids.update_boids(positions, velocities)
    for after,before in zip(regression_data["after"],positions.tolist()+velocities.tolist()):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.02)
	
def test_gen_random():
    low=np.array([-1,1])
    up=np.array([0,1])
    count=10
    boids=Boids(0)
    x, y = boids.gen_random(count, low, up)
    assert_equal(len(x), count)
    assert max(x) <= up[0]
    assert min(x) >= low[0]
    assert_equal(len(y), count)
    assert max(y) <= up[1]
    assert min(y) >= low[1]

