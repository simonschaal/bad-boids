from ..boids import update_boids, gen_random
from nose.tools import assert_almost_equal, assert_equal
import os
import yaml

def test_bad_boids_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixtures','fixture.yml')))
    boid_data=regression_data["before"]
    update_boids(boid_data)
    for after,before in zip(regression_data["after"],boid_data):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.01)
	
def test_gen_random():
    xlim=(-1,1)
    ylim=(0,1)
    count=10
    x, y = gen_random(xlim, ylim, count)
    assert_equal(len(x), count)
    assert max(x) <= max(xlim)
    assert min(x) >= min(xlim)
    assert_equal(len(y), count)
    assert max(y) <= max(ylim)
    assert min(y) >= min(ylim)

