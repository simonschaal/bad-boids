from argparse import ArgumentParser
#from genGraph import plotGraph
import sys
import yaml
from StringIO import StringIO
from boids import Boids

def process():
    parser = ArgumentParser(description = "Boid simulator: Simulates birds flying in flocks using the boids model.")
    parser.add_argument('--config', '-c', type=str, default="",  help="Boid simulator YAML configuration file. Defaults are shown and used if not specified.")
    parser.add_argument('--count', type=int, default=0, required=False, help="Overwrite bird count given in cfg file.")
    parser.add_argument('--fly_to_middle_strength', type=float, default=0, required=False, help="Overwrite settings given in cfg file.")
    parser.add_argument('--alert_distance', type=float,default=0, required=False, help="Overwrite settings given in cfg file.")
    parser.add_argument('--formation_flying_distance', type=float,default=0, required=False, help="Overwrite settings given in cfg file.")
    parser.add_argument('--formation_flying_strength', type=float,default=0, required=False, help="Overwrite settings given in cfg file.")
    arguments= parser.parse_args()
    
    #dictionary containing the configuration for the boids simulator
    cfg={}

    #default settings YAML 
    default="""Boids:
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
  ylim: [-500, 1500]"""

    #open given cfg file within try block to catch wrong filename etc.
    try:
        with open(arguments.config) as cfg_file:
            cfg=yaml.load(cfg_file)

            #check if config fullfills requirements
            if not all (k in cfg.keys() for k in ('Boids', 'Dynamics', 'Animation')):
                raise Exception 
            if not all (k in cfg['Boids'].keys() for k in ('count', 'vylim', 'vxlim', 'xlim', 'ylim')):
                raise Exception
            if not all (k in cfg['Dynamics'].keys() for k in ('formation_flying_distance','alert_distance','fly_to_middle_strength','formation_flying_strength')):
                raise Exception
            if not all (k in cfg['Animation'].keys() for k in ('frames', 'interval', 'ylim', 'xlim')):
                raise Exception
    except:
        #use default settings if no or wrong config file given!
        print "Something went wrong when reading the configuration file. Check that all needed configuration elements are given and that the filename is correct."
        print "Using the default settings! See below for the corresponding YAML file."
        print default
        cfg=yaml.load(StringIO(default))
    
    
    #run boids simulation with given settings
    boids=Boids(cfg, arguments.count, arguments.fly_to_middle_strength, arguments.alert_distance, arguments.formation_flying_distance, arguments.formation_flying_strength)
    boids.simulate()


if __name__ == "__main__":
    process()

