from ..boids import Boids
from nose.tools import assert_almost_equal, assert_equal
import os
import yaml
import numpy as np
import random

def test_bad_boids_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixtures','fixture.yml')))
    boid_data=regression_data["before"]
    positions=np.array([boid_data[0], boid_data[1]])
    velocities=np.array([boid_data[2], boid_data[3]])
    #feed data into boid
    boids=Boids({})
    boids.positions=positions
    boids.velocities=velocities
    #do update check if same values obtained
    boids.update_boids()
    for after,before in zip(regression_data["after"],positions.tolist()+velocities.tolist()):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.02)
	
def test_gen_random():
    low=np.array([-1,1])
    up=np.array([0,1])
    count=10
    boids=Boids({})
    x, y = boids.gen_random(count, low, up)
    #check if length is correct and if within given bounds
    assert_equal(len(x), count)
    assert max(x) <= up[0]
    assert min(x) >= low[0]
    assert_equal(len(y), count)
    assert max(y) <= up[1]
    assert min(y) >= low[1]

def test_fly_towards_middle():
    #randomized test
    # generate random range data
    length=random.randint(10,50)
    boids=Boids({},length)
    boids.positions=np.array([random.random()*np.arange(length), random.random()*np.arange(length)])
    fly_middle=boids._fly_towards_middle(random.random())

    # check length
    assert_equal(fly_middle.size, 2*length)
    # for range variables it should sum to zero due to symmetry
    assert_almost_equal(np.sum(fly_middle), 0, delta = 1e-10)

    #regression test
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixtures','flyToMiddle.yml')))
    boid_data=regression_data["before"]
    positions=np.array([boid_data[0], boid_data[1]])
    velocities=np.array([boid_data[2], boid_data[3]])
    #feed data into boid
    boids=Boids({})
    boids.positions=positions
    boids.velocities=velocities
    #do update check if same values obtained
    boids.velocities += boids._fly_towards_middle(0.01)
    boids.positions += boids.velocities
    for after,before in zip(regression_data["after"],positions.tolist()+velocities.tolist()):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.02)
	

def test_avoid_collisions():
    # generate random range data
    length=random.randint(10,50)
    boids=Boids({},length)
    boids.positions=np.array([100*random.random()*np.arange(length), 100*random.random()*np.arange(length)])
    collisions=boids._avoid_collisions(1000)

    # check length
    assert_equal(collisions.size, 2*length)
    # for range variables it should sum to zero due to symmetry
    assert_almost_equal(np.sum(collisions), 0, delta = 1e-10)

    #regression test
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixtures','avoidCollisions.yml')))
    boid_data=regression_data["before"]
    positions=np.array([boid_data[0], boid_data[1]])
    velocities=np.array([boid_data[2], boid_data[3]])
    #feed data into boid
    boids=Boids({})
    boids.positions=positions
    boids.velocities=velocities
    #do update check if same values obtained
    boids.velocities += boids._avoid_collisions(100)
    boids.positions += boids.velocities
    for after,before in zip(regression_data["after"],positions.tolist()+velocities.tolist()):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.02)
	

def test_match_Speed():
    # generate random range data
    length=random.randint(10,50)
    boids=Boids({}, length)
    speed=boids._match_speed_nearby(100,100)

    # check length
    assert_equal(speed.size, 2*length)
    # for range variables it should sum to zero due to symmetry
    assert_almost_equal(np.sum(speed), 0, delta = 1e-10)
    
    #regression test
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixtures','matchSpeed.yml')))
    boid_data=regression_data["before"]
    positions=np.array([boid_data[0], boid_data[1]])
    velocities=np.array([boid_data[2], boid_data[3]])
    #feed data into boid
    boids=Boids({})
    boids.positions=positions
    boids.velocities=velocities
    #do update check if same values obtained
    boids.velocities += boids._match_speed_nearby(10000,0.125)
    boids.positions += boids.velocities
    for after,before in zip(regression_data["after"],positions.tolist()+velocities.tolist()):
        for after_value,before_value in zip(after,before): 
            assert_almost_equal(after_value,before_value,delta=0.02)
	

