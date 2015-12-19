import yaml
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import boids
before=boids.pos.tolist() + boids.vel.tolist()
boids.update_boids(boids.pos, boids.vel)
after=boids.pos.tolist() + boids.vel.tolist()
fixture={"before":before,"after":after}
fixture_file=open("fixtures/fixture_np.yml",'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
