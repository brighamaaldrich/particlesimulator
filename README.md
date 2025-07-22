# particlesimulator

AUTHORS:        Brigham Aldrich
DESCRIPTION:    2D and 3D particle simulation using Python and visualized with PyGame.
DEPENDENCIES:   Python 3.XX, PyGame 2.6.1

INFO:           This program contains two executable python files called particles.py and particles3D.py which run the 2 dimensional and 3 dimensional simulations respectively.
                Both programs use the kinematic equations for conservation of momentum and conservation of kinetic energy to determine collision behavior.
                The friction variable is a constant between 0 and 1 which indicates what percentage of a particles momentum is conserved in a collision.
                The color spectrum of the particles goes from blue (low energy) to red (high energy) with the hue varying continuously between the two.

DIRECTIONS:     For particles.py, you can simply click and hold anywhere on the particle simulation section of the program to "heat" (add energy to) that section of the simulation field.
                A circular indicator will follow the cursor when clicking.
                For particles3D.py, clicking and dragging rotates the 3D simulation field so you can view it from different angles. 
                If you wish to return to the default view, simply press the space key and the field will smoothly rotate back to the initial state.
                Finally, pressing and holding the up arrow key will uniformly "heat" (add energy to) the entire field.

GRAPHS:         In both programs there is a kinetic energy graph which tracks the realtime total kinetic energy of the system (also seen in the caption on the top bar).
                Both programs also show a Maxwell-Boltzmann distribution which is effectively a histogram showing the number of particles at various energy levels.
                As desired, the histogram closely resembles the shape of the theoretical Maxwell-Boltsmann distribution which can be derived from thermodynamics equations.
