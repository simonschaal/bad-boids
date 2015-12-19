
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np


class Boids(object):
    def __init__(self, boid_count, xlimits=(-450, 50), ylimits=(300, 600), vxlimits=(0, 10), vylimits=(-20, 20)):
        self.boid_count=boid_count
        self._xy_low_lim=np.array([xlimits[0], ylimits[0]])
        self._xy_up_lim=np.array([xlimits[1], ylimits[1]])
        self._vxy_low_lim=np.array([vxlimits[0], vylimits[0]])
        self._vxy_up_lim=np.array([vxlimits[1], vylimits[1]])
        # generate random boid positions and velocities within given limits
        self.pos = self.gen_random(self.boid_count, self._xy_low_lim, self._xy_up_lim)
        self.vel = self.gen_random(self.boid_count, self._vxy_low_lim, self._vxy_up_lim)

    def gen_random(self, count, lower_limits, upper_limits):
        width=upper_limits-lower_limits
        return (lower_limits[:,np.newaxis] + 
            np.random.rand(2, count)*width[:,np.newaxis])

    def _fly_towards_middle(self, positions, strength):
        # Fly towards the middle
        middle=np.mean(positions, 1)
        direction_to_middle = positions - middle[:, np.newaxis]
        return (-1) * direction_to_middle * strength

    def _avoid_collisions(self, positions, alert_distance):
        # Fly away from nearby boids
        separations = positions[:,np.newaxis,:] - positions[:,:,np.newaxis]
        squared_displacements = separations * separations
        square_distances = np.sum(squared_displacements, 0)
        far_away = square_distances > alert_distance
        separations_if_close = np.copy(separations)
        separations_if_close[0,:,:][far_away] =0
        separations_if_close[1,:,:][far_away] =0
        return np.sum(separations_if_close,1) 

    def _match_speed_nearby(self, positions, velocities, formation_flying_distance, formation_flying_strength):
   	    # Try to match speed with nearby boids
        separations = positions[:,np.newaxis,:] - positions[:,:,np.newaxis]
        squared_displacements = separations * separations
        square_distances = np.sum(squared_displacements, 0)
        velocity_differences = velocities[:,np.newaxis,:] - velocities[:,:,np.newaxis]
        very_far=square_distances > formation_flying_distance
        velocity_differences_if_close = np.copy(velocity_differences)
        velocity_differences_if_close[0,:,:][very_far] =0
        velocity_differences_if_close[1,:,:][very_far] =0
        return (-1) * np.mean(velocity_differences_if_close, 1) * formation_flying_strength
       

    def update_boids(self, positions, velocities):
        velocities += self._fly_towards_middle(positions, 0.01)  
        velocities += self._avoid_collisions(positions, 100) 
        velocities += self._match_speed_nearby(positions, velocities, 10000, 0.125)
        #update positions acc to models
        positions += velocities

    def animate(self,frame, scatter):
        self.update_boids(self.pos, self.vel)
        scatter.set_offsets(zip(self.pos[0], self.pos[1]))


boids=Boids(50)
figure=plt.figure()
axes=plt.axes(xlim=(-500,1500), ylim=(-500,1500))
scatter=axes.scatter(boids.pos[0],boids.pos[1])


anim = animation.FuncAnimation(figure, boids.animate, fargs=[scatter], 
                               frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
