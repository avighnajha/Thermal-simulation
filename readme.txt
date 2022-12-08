The models for the ball and simulation objects are contained in the balls.py and simulation.py files.

balls.py : Contains the ball object along with all of its methods

simulation.py : Contains the simulation object along with all of its methods.

text.py : Contains the tests carried out to chheck for indivisual and integration tests for different methods and to check teh functionality of the 2 classes together. Some tests are now invalid as they were used in the earlier stages of the project. Initially balls were a parameter for the simulation class and hence had to be provided, however now the balls are generated within Simulation and hence soem of these tests are no more functional.

analysis.py : Used to carry out inital investigations of the distribution of pair distances, distance from thecentre of container, the distribution of speeds and to check various properties such as the rms speed, average speed and the variance of the speed dsitribution.

no_balls.py : Carries out investigations where the parameter being changed is the number of balls in the container and produces required plots to investigate P-T relationships with the number of balls.

con_r.py : Carries out investigations where the parameeter being changed in the radius of the contianer and produces required plots to investigate how the P-T relationship varies with changing container radius.

van_der_vaals.py : Carries out simulations to investigate the equation of state for a simulation and also investigates the van der Waals equation by checking equation of state for balls of different radii. Calculates values for the coefficient b and its error in the van der waals equation.