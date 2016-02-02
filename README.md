Boids
=====

MPHYG001 Research Software Engineering With Python coursework 2

http://development.rc.ucl.ac.uk/training/engineering/

Refactored clone of:
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.


```
usage: boids [-h] [--config CONFIG] [--count COUNT]
             [--fly_to_middle_strength FLY_TO_MIDDLE_STRENGTH]
             [--alert_distance ALERT_DISTANCE]
             [--formation_flying_distance FORMATION_FLYING_DISTANCE]
             [--formation_flying_strength FORMATION_FLYING_STRENGTH]

Boid simulator: Simulates birds flying in flocks using the boids model.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Boid simulator YAML configuration file. Defaults are
                        shown and used if not specified.
  --count COUNT         Overwrite bird count given in cfg file.
  --fly_to_middle_strength FLY_TO_MIDDLE_STRENGTH
                        Overwrite settings given in cfg file.
  --alert_distance ALERT_DISTANCE
                        Overwrite settings given in cfg file.
  --formation_flying_distance FORMATION_FLYING_DISTANCE
                        Overwrite settings given in cfg file.
  --formation_flying_strength FORMATION_FLYING_STRENGTH
                        Overwrite settings given in cfg file.
```


Exemplary YAML configuration file:
```
Boids:
  count: 50
  vxlim: [0, 10]
  vylim: [-20, 20]
  xlim: [-450, 50]
  ylim: [300, 600]
Dynamics:
  alert_distance: 100
  fly_to_middle_strength: 0.01
  formation_flying_strength: 0.125
  formation_flying_distance: 10000
Animation:
  frames: 50
  interval: 50
  xlim: [-500, 1500]
  ylim: [-500, 1500]
```

