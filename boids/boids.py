
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np

boid_count=50
plow_lim=np.array([-450, 300])
pup_lim=np.array([50, 600])
vlow_lim=np.array([0, -20])
vup_lim=np.array([10, 20])


def gen_random(count, lower_limits, upper_limits):
    width=upper_limits-lower_limits
    return (lower_limits[:,np.newaxis] + 
         np.random.rand(2, count)*width[:,np.newaxis])

pos = gen_random(boid_count, plow_lim, pup_lim)
vel = gen_random(boid_count, vlow_lim, vup_lim)


def update_boids(positions, velocities):
	# Fly towards the middle
    strength=0.01
    middle=np.mean(positions, 1)
    direction_to_middle = positions - middle[:, np.newaxis]
    velocities -= direction_to_middle * strength

	# Fly away from nearby boids
    separations = positions[:,np.newaxis,:] - positions[:,:,np.newaxis]
    squared_displacements = separations * separations
    square_distances = np.sum(squared_displacements, 0)
    alert_distance = 100
    far_away = square_distances > alert_distance
    separations_if_close = np.copy(separations)
    separations_if_close[0,:,:][far_away] =0
    separations_if_close[1,:,:][far_away] =0
    velocities += np.sum(separations_if_close,1) 

	# Try to match speed with nearby boids
    velocity_differences = velocities[:,np.newaxis,:] - velocities[:,:,np.newaxis]
    formation_flying_distance = 10000
    formation_flying_strength = 0.125
    very_far=square_distances > formation_flying_distance
    velocity_differences_if_close = np.copy(velocity_differences)
    velocity_differences_if_close[0,:,:][very_far] =0
    velocity_differences_if_close[1,:,:][very_far] =0
    velocities -= np.mean(velocity_differences_if_close, 1) * formation_flying_strength

    #update positions acc to velocities
    positions += velocities

figure=plt.figure()
axes=plt.axes(xlim=(-500,1500), ylim=(-500,1500))
scatter=axes.scatter(pos[0],pos[1])

def animate(frame):
   update_boids(pos, vel)
   scatter.set_offsets(zip(pos[0], pos[1]))


anim = animation.FuncAnimation(figure, animate,
                               frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
