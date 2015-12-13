import yaml
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import boids
from copy import deepcopy
before=deepcopy(boids.boids)
boids.update_boids(boids.boids)
after=boids.boids
fixture={"before":before,"after":after}
fixture_file=open("fixtures/fixture.yml",'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
