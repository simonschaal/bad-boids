import yaml
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from boids import Boids

boids=Boids({})
before=boids.positions.tolist() + boids.velocities.tolist()
#boids.update_boids()
boids.velocities += boids._match_speed_nearby(10000,0.125)
boids.positions += boids.velocities
after=boids.positions.tolist() + boids.velocities.tolist()
fixture={"before":before,"after":after}
fixture_file=open("fixtures/matchSpeed.yml",'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
