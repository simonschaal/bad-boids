
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np


class Boids(object):
    def __init__(self, boid_count, xlimits=(-450, 50), ylimits=(300, 600), vxlimits=(0, 10), vylimits=(-20, 20)):
        self.boid_count=boid_count
        self._xy_low_lim=np.array([xlimits[0], ylimits[0]])
        self._xy_up_lim=np.array([xlimits[1], ylimits[1]])
        self._vxy_low_lim=np.array([vxlimits[0], vylimits[0]])
        self._vxy_up_lim=np.array([vxlimits[1], vylimits[1]])
        # generate random boid positions and velocities within given limits
        self.positions = self.gen_random(self.boid_count, self._xy_low_lim, self._xy_up_lim)
        self.velocities = self.gen_random(self.boid_count, self._vxy_low_lim, self._vxy_up_lim)

    def gen_random(self, count, lower_limits, upper_limits):
        width=upper_limits-lower_limits
        return (lower_limits[:,np.newaxis] + 
            np.random.rand(2, count)*width[:,np.newaxis])

    def _fly_towards_middle(self, strength):
        # Fly towards the middle
        middle=np.mean(self.positions, 1)
        direction_to_middle = self.positions - middle[:, np.newaxis]
        return (-1) * direction_to_middle * strength

    def _avoid_collisions(self, alert_distance):
        # Fly away from nearby boids
        separations = self.positions[:,np.newaxis,:] - self.positions[:,:,np.newaxis]
        squared_displacements = separations * separations
        square_distances = np.sum(squared_displacements, 0)
        print square_distances
        far_away = square_distances > alert_distance
        separations_if_close = np.copy(separations)
        separations_if_close[0,:,:][far_away] =0
        separations_if_close[1,:,:][far_away] =0
        return np.sum(separations_if_close,1) 

    def _match_speed_nearby(self, formation_flying_distance, formation_flying_strength):
   	    # Try to match speed with nearby boids
        separations = self.positions[:,np.newaxis,:] - self.positions[:,:,np.newaxis]
        squared_displacements = separations * separations
        square_distances = np.sum(squared_displacements, 0)
        velocity_differences = self.velocities[:,np.newaxis,:] - self.velocities[:,:,np.newaxis]
        very_far=square_distances > formation_flying_distance
        velocity_differences_if_close = np.copy(velocity_differences)
        velocity_differences_if_close[0,:,:][very_far] =0
        velocity_differences_if_close[1,:,:][very_far] =0
        return (-1) * np.mean(velocity_differences_if_close, 1) * formation_flying_strength
       

    def update_boids(self):
        self.velocities += self._fly_towards_middle(0.01)  
        self.velocities += self._avoid_collisions(100) 
        self.velocities += self._match_speed_nearby(10000, 0.125)
        #update positions acc to models
        self.positions += self.velocities

    def _animate(self,frame, scatter):
        self.update_boids()
        scatter.set_offsets(zip(self.positions[0], self.positions[1]))

    def simulate(self, frames=50, interval=50, xlimits=(-500, 1500), ylimits=(-500, 1500)):
        figure=plt.figure()
        axes=plt.axes(xlim=xlimits, ylim=ylimits)
        scatter=axes.scatter(self.positions[0],self.positions[1])
        anim = animation.FuncAnimation(figure, self._animate, fargs=[scatter], 
                                       frames=frames, interval=interval)
        plt.show()


if __name__ == "__main__":
    boids=Boids(50)
    boids.simulate()
