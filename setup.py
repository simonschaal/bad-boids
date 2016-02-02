from setuptools import setup, find_packages
setup(
    name = "Boids",
    version = "1.0",
    description='Simulate flocking birds (boids)',
    author='Simon Schaal',
    author_email='simon.schaal.15@ucl.ac.uk',
    license='MIT',
    packages = find_packages(exclude=['*test']),
    scripts = ['scripts/boids'],
    install_requires = ['matplotlib', 'numpy', 'pyyaml', 'argparse']
)
