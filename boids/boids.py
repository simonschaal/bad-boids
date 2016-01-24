
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

# Boids
# needs config file. Important simulation parameters can be changed optionally and will be overwrite config file parameters if given.
class Boids(object):
    def __init__(self, config, count=0, fly_to_middle=0, alert_distance=0, formation_flying_distance=0, formation_flying_strength=0): 
        #get config 
        self.config=config

        #default config used if config empty
        if not self.config:
            self.config={
                'Boids': 
                {'count': 50, 'vylim': [-20, 20], 'vxlim': [0, 10], 'xlim': [-450, 50], 'ylim': [300, 600]}, 
                'Dynamics': 
                {'formation_flying_distance': 10000, 'alert_distance': 100, 'fly_to_middle_strength': 0.01, 'formation_flying_strength': 0.125}, 
                'Animation': 
                {'frames': 50, 'interval': 50, 'ylim': [-500, 1500], 'xlim': [-500, 1500]}
            }
        # Overwrite simulation parameters if given separately
        if count:
            self.config['Boids']['count']=count
        if fly_to_middle:
            self.config['Dynamics']['fly_to_middle_strength']=fly_to_middle
        if alert_distance:
            self.config['Dynamics']['alert_distance']=alert_distance
        if formation_flying_distance:
            self.config['Dynamics']['formation_flying_distance']=formation_flying_distance
        if formation_flying_strength:
            self.config['Dynamics']['formation_flying_strength']=formation_flying_strength


        # setup flock
        self.boid_count=self.config['Boids']['count']
        self._xy_low_lim=np.array([self.config['Boids']['xlim'][0], self.config['Boids']['ylim'][0]])
        self._xy_up_lim=np.array([self.config['Boids']['xlim'][1], self.config['Boids']['ylim'][1]])
        self._vxy_low_lim=np.array([self.config['Boids']['vxlim'][0], self.config['Boids']['vylim'][0]])
        self._vxy_up_lim=np.array([self.config['Boids']['vxlim'][1], self.config['Boids']['vylim'][1]])

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
        # apply boids model
        self.velocities += self._fly_towards_middle(self.config['Dynamics']['fly_to_middle_strength'])  
        self.velocities += self._avoid_collisions(self.config['Dynamics']['alert_distance']) 
        self.velocities += self._match_speed_nearby(self.config['Dynamics']['formation_flying_distance'], self.config['Dynamics']['formation_flying_strength'])
        #update positions acc to models
        self.positions += self.velocities

    def _animate(self,frame, scatter):
        # animation runs update_boids() for each frame
        self.update_boids()
        scatter.set_offsets(zip(self.positions[0], self.positions[1]))

    def simulate(self):
        #open plot for simulation and run animation
        figure=plt.figure()
        axes=plt.axes(xlim=self.config['Animation']['xlim'], ylim=self.config['Animation']['ylim'])
        scatter=axes.scatter(self.positions[0],self.positions[1])
        anim = animation.FuncAnimation(figure, self._animate, fargs=[scatter], 
                                       frames=self.config['Animation']['frames'], interval=self.config['Animation']['interval'])
        plt.show()


