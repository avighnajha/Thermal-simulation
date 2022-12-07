import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
#%%

class Ball:
    """
    A class to represent a ball.

    ...

    Attributes
    ----------
        velocity : np.array
            Velocity of the ball
        position : np.array
            Position of the ball
        mass : int
            Mass of the ball
        radius : int
            Radius of the ball
        patch : patch object for the ball
        KE : int
            Kinetic energy of the ball

    Methods
    -------
        pos():
            returns the position of the ball
        vel():
            returns the velocity of the ball
        get_patch():
            returns the patch belonging to the ball
        time_to_collision(other):
            returns the amount of time it will take to collide with "other" another ball object.
        move(dt):
            changes the position of the ball in the direction of its velocity to a time "dt" later. Returns the ball moved.
        collide(other, t_min):
            changes the velocities of the ball itself and another ball object "other" after an ellastic collision. Returns the ball object it has been used on.    
    """
    
    def __init__(self, mass, radius, position = [0,0], velocity = [0,0]):
        
        '''
        Constructs necessary attributes for a ball object.
        
        Parameters
        -----------
            velocity : np.array
                Velocity of the ball
            position : np.array
                Position of the ball
            mass : int
                Mass of the ball
            radius : int
                Radius of the ball. In the case of a container the radius is negative.
            patch : patch object for the ball
        '''
        
        velocity = np.array(velocity, dtype = float)
        position = np.array(position, dtype = float)
        self._mass = mass
        self._radius = radius
        self._position = position
        self._velocity = velocity
        if self._mass == np.inf:
            self._KE = 0
        else:
            self._KE = self._mass*np.dot(self._velocity, self._velocity)/2
        if self._mass == np.inf:
            self._patch = pl.Circle(self._position, self._radius, ec = "b" ,fill = False)
        else:
            self._patch = pl.Circle(self._position, self._radius, fc = "r")

    def __repr__(self):
        return f"Ball at {self._position}, with speed {self._velocity}"
    def pos(self):
        '''
        Returns the position of the ball.
        '''
        return self._position
    def vel(self):
        '''
        Returns velocity of the ball.
        '''
        return self._velocity
    def get_patch(self):
        '''
        Returns the patch on the axis belonging to the ball.
        '''
        return self._patch
    def time_to_collision(self, other):
        '''
        Parameters
        ----------
            other : The other ball object we're checking the time to collisiion with.
        Returns
        --------
            The time it takes for the ball to collide with another ball.
        '''
        rel_vel = self.vel() - other.vel()
        rel_pos = self.pos() - other.pos()
        R = self._radius + other._radius 
        #a b and c correspond to coefficients in at^2+bt+c = 0
        a = np.dot(rel_vel, rel_vel)
        b = 2*np.dot(rel_vel, rel_pos)
        c = np.dot(rel_pos, rel_pos) - R**2
        
        disc = b**2 - 4*a*c
        if abs(a)<1e-7: # 0 relative velocity 
            return None
        if (disc)<0: #Balls never collided and will never collide
            return None
        elif b>0 and self._mass!=np.inf and other._mass != np.inf:
            return None
        t_minus = (-b - np.sqrt(disc))/(2*a)
        t_plus = (-b + np.sqrt(disc))/(2*a)
        if t_minus <0 and t_plus<0:
            return None
        else:
            t = min(t_minus, t_plus)
            if t<1e-7: #t<1e-7 chosen to avoid rounding errors where t is supposed to be 0 but due to rounding error returns a vary small positive value
                t = max(t_minus, t_plus)
        return t
    
    
    def move(self, dt):
        '''
        Moves the ball and its patch in the direction of its velocities by a time dt.
        Parameters
        ----------
        dt : The amount of time we want to move the ball ahead by.

        Returns
        -------
        The ball itself.

        '''
        if dt == None:
            raise TypeError("Time to collision provided is NoneType")
        if dt <0:
            raise Exception("Balls cannot move by a -ve time")
        new_position = self.pos() +(dt*self._velocity) 
        
        self._position = new_position
        self.get_patch().center = new_position

        return self
        
    def collide(self, other, t_min):
        '''
        Carrys out the collision between the ball and another ball object "other" and changes their velocities for an elastic collision. Make sure the balls are moved to the point of collision before this method is called.
        Parameters
        ----------
        other : The other ball object we are carrying out the collision with.
        t_min : The time to collision for this ball and the "other" ball object

        Returns
        -------
        The ball itself.

        '''
        if t_min == None:
            raise Exception("Time to collision cannot be negative")
        if other._mass == np.inf: #Here we're assuming and later will make sure that the container is always "other"
            new_pos = self.pos()
            new_pos_norm = new_pos/np.sqrt(np.dot(new_pos, new_pos))

            v_norm = np.dot(self.vel(), new_pos_norm)
            v_norm_arr = v_norm*new_pos_norm
            v_par_arr = self.vel() - v_norm_arr

            final_v = v_par_arr - v_norm_arr

            self._velocity = final_v
            
        else:    
            rel_vel = self.vel() - other.vel()
            rel_r = self.pos() - other.pos()
            
            m1 = self._mass
            m2 = other._mass
            v1 = self.vel()-(2*(m2/(m1+m2))*(np.dot(rel_vel, rel_r)/(np.dot(rel_r, rel_r)))*rel_r)
            v2 = other.vel()+(2*(m1/(m1+m2))*(np.dot(rel_vel, rel_r)/(np.dot(rel_r, rel_r)))*rel_r)
            self._velocity = v1
            other._velocity = v2
        return self
    

class Simulation:
    '''
    A class to represent a simulation of the several ball objects with their unique positions and velocities
    ...
    Class variables
    ---------------
    Class variables must be reset before every new initialisation of a simulation to make sure impulse and time are tracked accurately.
        impulse_tot :
            Tracks the total impulse on the container object throughout the simulation.
        t_container :
            Tracks the total time the simulation has been running for.
    
    Attributes
    ----------
        container : a ball object
        con_radius : int
            radius of above container but with positive radius as container's are given negative radius when inialised as ball objects.
        balls : list
            list of ball objects that exist inside the container.
        press_evol:
        
        ke_evol: list
            list of total kinetic energy of all balls at every collision
        
        ang_mom_evol : list 
            list of the total modulus of angular momentum of the balls in the container about the center of the container at every collision.
        
        col_times : list
            list of the times at which every collision takes place.     
            
        temp_evol : list
            list of the tempreture of the container at each collision.
        
        mom_evol : list
            list of the total modulus of momentum of the balls in the container at every collision.
        
    Methods
    --------
        calc_impulse(balli_vel, ballf):
            calculates the impulse due to the change in velocity of a ball object. Returns the total impulse on the container object.
        
        calc_pressure(rad_con):
            calculates the pressure on the container using the total impulse and the total time the simulation has been running for. Returns the pressure.
        
        plot_position():
            plots a histogram of the distribution of the distance of each ball object from the center of the container object. Returns the distance data.
        
        plot_pair_distance():
            plots a histogram of the distribution of the distance between all pairs of ball objects. Returns the distance data.
        
        calc_ang_mom() :
            calculates the sum of the moduli of the angular momentum of each ball with respect to the center of the container.
        
        calc_mom():
            calculates the sum of the moduli of the momentum of each ball.
            
        plot_ang_mom():
            plots the evolution of the sum of the moduli of the angular momentum of each ball with respect to the center of the container for every collision.
            
        plot_mom_evol():
            plots the evolution of the sum of the moduli of the momentum of each ball for every collision.
        
        plot_press_evol():
            plots the evolution of the pressure on the walls of the containerover time.
        
        plot_ke_evol():
            plots the evolution of the total kinetic energy inside the container over time.
        
        plot_v_dist():
            plots a histogram of the distribution of the speeds of all of the balls inside the container. Returns an array of all ball velocities and the heights and positions of the bins in the histogram.
        
        next_collision(plots):
            finds the 2 balls in the system that are going to collide first, carries out the collision and moves all balls forward in time to the collision time. Returns the simulation itself.
        
        calc_temp():
            calculates the total temperature inside the container object using the total kinetic energy of the balls. Returns the temperature.
        
        run(num_frames, animate = False, plots = True):
            runs the simulation for a certain number of collisions and animates the movement of the balls.
    
    '''
    impulse_tot = 0 
    t_container = 0
    def __init__(self,container, no_balls=100, v_max = 10, ball_rad = 0.5):
        '''
        
        Parameters
        ----------
        container : a ball object with a -ve radius and infinite mass to signify a container.

        no_balls : int
            The number of balls to be initialised inside the container. The default is 100.
        v_max : int
            The maximum speed in x or y a ball is allowed to have. The default is 10.
        ball_rad : int
            The radius of the balls generated inside the container. The default is 0.5.

        Returns
        -------
        None

        '''
        #Checking for errors with parameters to allow someone else using my code to realise when values are invalid.
        if ball_rad<0:
            raise Exception("Ball's cannot have a radius smaller than 0")
        if container._radius > 0:
            raise Exception("Container's must have a negative radius to differentiate them from ordinary balls.")
        if container._mass!=np.inf:
            raise Exception("Container must have infinite mass, please import and use numpy.inf as mass for the container.")
        if no_balls<0:
            raise Exception("Cannot have less than 0 balls in container.")
            
        self._container = container
        self._con_radius = -container._radius
        '''
        For the generation of balls, I take a range of radii from slightly more than 2*ball radius to a point that is 1 ball radius from the edge of the container with steps of slightly more than 2*ball radius. This range of radii form concentric circles from the center to the edge of the container and generate balls in each of these concentric circles with 0.5*ball radius distance between each ball. The balls stop generating either if the number of balls generated is equal to the no_balls, or if no more balls fit inside the container.
        '''
        balls = []
        
        vel_overall = [0,0]
        cur_no_balls = 1
        for r in np.arange(2.1*ball_rad, -container._radius - ball_rad, 2.1*ball_rad):
            if cur_no_balls == no_balls:
                break
            splits = (2*np.pi*r)//(2.5*ball_rad)
            split_angle = 2*np.pi/splits
            for j in range(int(splits)):
                if cur_no_balls == no_balls:
                    break
                ball_rad
                mass = 1
                theta = split_angle*j
                velocityx = np.random.uniform(-v_max,v_max)
                velocityy = np.random.uniform(-v_max,v_max)
                vel = np.array([velocityx, velocityy])
                vel_overall+=vel
                posx = r*np.cos(theta)
                posy = r*np.sin(theta)
                pos = np.array([posx, posy])
                ball = Ball(mass, ball_rad, pos, vel)
                balls.append(ball)
                cur_no_balls+=1
        print(f"Balls generated = {cur_no_balls}")
        vel_remaining = -1*vel_overall
        ball_center = Ball(1, ball_rad, [0,0], vel_remaining)
        balls.append(ball_center)
        balls.append(self._container) #Container always appended as the last ball to make sure it is "other" when considering collisions.
        self._balls = balls
        self._press_evol = []
        self._ke_evol = []
        self._ang_mom_evol = []
        self._col_times = []
        self._temp_evol = []
        self._mom_evol = []
        
        
    
    def calc_impulse(self, balli_vel, ballf):
        '''

        Parameters
        ----------
        balli_vel : int
            The initial velocity of the ball.
        ballf : ball object
            The final state of the ball.

        Returns
        -------
        Total impulse on the container in the simulation.

        '''
        vi = balli_vel
        vf = ballf.vel()
        mass = ballf._mass
        impulse = mass*(vf-vi)
        impulse_mag = np.sqrt(np.dot(impulse, impulse))
        Simulation.impulse_tot += impulse_mag
        # print("Collision impulse: ", impulse_mag)
        # print("Total Impulse: ", Simulation.impulse_tot)
        return Simulation.impulse_tot
    
    def calc_pressure(self, rad_con):
        '''

        Parameters
        ----------
        rad_con : int
            The radius of the container for which the pressure is being calculated for.

        Returns
        -------
        pressure : int
            The total pressure on the container at this instant in the simulation.

        '''
        perimeter = 2*np.pi*rad_con
        force = Simulation.impulse_tot/Simulation.t_container
        pressure = force/perimeter
        return pressure
    
    def plot_position(self):
        '''
        Plots a histogram of the distribution of the positions of the balls in the container.
        Returns
        -------
        positions : list
            An array of positions of the ball with respect to the center of the container.
        '''
        positions = []
        for ball in self._balls:
            positions.append(np.sqrt(np.dot(ball.pos(), ball.pos())))                             
        plt.hist(positions)
        plt.title("Distance from center")
        plt.xlabel("Distance from center")
        plt.ylabel("Number of balls")
        plt.grid()
        plt.show()
        return positions
        
    def plot_pair_distance(self):
        '''
        Iterated through every ball and find distance to every other ball in the simulation unless the ball pair have already been checked in which case the iteration is skipped. If not, the pair is added to the dictionary done to prevent double checking of pairs.
        
        Returns
        -------
        distances : list
            A list of the distribution of the distance between any pair of balls in the simulation.

        '''
        balls = self._balls
        distances = []
        done = {}
        for i in range(len(balls)):
            for j in range(len(balls)):
                if i == j:
                    continue
                if f"[{j},{i}]" in done:
                    continue
                else:
                    done[f"[{i},{j}]"] = True
                    
                distance = balls[i].pos() - balls[j].pos()
                distance_mag = np.sqrt(np.dot(distance, distance))
                distances.append(distance_mag)
        height, edges, patches = plt.hist(distances)
        bincenters = 0.5*(edges[1:]+edges[:-1])
        errors = np.sqrt(height)
        plt.errorbar(bincenters, height, yerr = errors,fmt = "none", capsize =2)
        plt.legend(["Bins", "Errors"])
        plt.title("Pair distances")
        plt.xlabel("Distance between pair of balls ")
        plt.ylabel("Number of balls")
        plt.grid()
        plt.show()
        return distances
        
    def calc_ang_mom(self):
        '''


        Returns
        -------
        mod_tot_ang : int
            The total of the modulus of angular momentums of balls about the center of the container in the simulation.

        '''
        total_ang = np.array([0,0])
        for ball in self._balls[:-1]:
            ang_mom = np.cross(ball.pos(), ball._mass*ball.vel())
            total_ang = total_ang + ang_mom
        mod_tot_ang = np.sqrt(np.dot(total_ang, total_ang))
        return mod_tot_ang
    def calc_mom(self):
        '''
        

        Returns
        -------
        mod_tot_mom : int
            The total of the modulus of momentums of balls in the simulation.

        '''
        total_mom = np.array([0,0])
        for ball in self._balls[:-1]:
            mom = ball._mass*ball.vel()
            total_mom = total_mom + mom
        mod_tot_mom = np.sqrt(np.dot(total_mom, total_mom))
        return mod_tot_mom
        
    def plot_ang_mom(self):
        '''
        Plots the evolution of the sum of the moduli of the angular momentum of each ball with respect to the center of the container for every collision.
        Returns
        -------
        None.

        '''
        plt.plot(self._col_times, self._ang_mom_evol)
        plt.ylim(0, 1000)
        plt.xlabel("Time (s)")
        plt.ylabel("Angular momentum")
        plt.title("Evolution of total angular momentum inside container over time")
        plt.grid()
        plt.show()
    def plot_mom_evol(self):
        '''
        Plots the evolution of the sum of the moduli of the momentum of each ball for every collision.

        Returns
        -------
        None.

        '''
        plt.plot(self._col_times, self._mom_evol)
        plt.xlabel("Time")
        plt.ylabel("Momentum")
        plt.title("Evolution of momentum inside container over time")
        plt.grid()
        plt.show()
                
            
    def plot_pressure_evol(self):
        '''
        Plots the evolution of the pressure on the container over time.

        Returns
        -------
        None.

        '''
        plt.plot(self._col_times, self._press_evol)
        plt.xlabel("Time (s)")
        plt.ylabel("Pressure")
        plt.title("Evolution of the pressure on the container over time")
        plt.grid()
        plt.show()
    def plot_ke_evol(self):
        '''
        Plots the evolution of the total kinetic energy of the balls in the container over time.

        Returns
        -------
        None.

        '''
        plt.plot(self._col_times, self._ke_evol)
        plt.xlabel("Time (s)")
        plt.ylabel("KE")
        plt.title("Evolution of KE in the system over time")
        plt.grid()
        plt.show()
    
    def plot_v_dist(self):
        '''
        Plots a historgam showing the distribution of the speeds of the balls in the container at an instant.

        Returns
        -------
        list
            returns a list of the velocity distributions, heights of the bins and the position of the edges of the bins in the histogram plotted.

        '''
        all_v = []
        for j in self._balls:
            speed = np.sqrt(np.dot(j.vel(), j.vel()))
            all_v.append(speed)
        height, edges, patches = plt.hist(all_v)
        bincenters = 0.5*(edges[1:]+edges[:-1])
        errors = np.sqrt(height)
        plt.errorbar(bincenters, height, yerr = errors,fmt = "none", capsize =2)
        plt.legend(["Bins", "Errors"])
        plt.title("Speed distribution")
        plt.xlabel("Speed of ball")
        plt.ylabel("Number of balls")
        plt.grid()

        return [all_v, height, edges]
    
    def calc_temp(self):
        '''
        Calculates the temperature inside the container of the simulation using the equipartition theorem. 

        Returns
        -------
        temp : int
            The temperature calculated.

        '''
        
        #Using fNkT/2 = KE as only 2 degrees of freedom in this system, f = 2, therefore NkT = KE.
        totalKE = 0
        k = 1.38e-23
        N = len(self._balls)
        for ball in self._balls:
            totalKE += ball._KE
        temp = totalKE/(N*k)
        return temp
        
    def next_collision(self, plots = True):
        '''
        Goes through all balls and finds the balls that are going to collide first, moves all balls to the point at which these 2 balls collide and carries out collision and changes the velocities of the 2 balls colliding.

        Parameters
        ----------
        plots : bool, optional
            If true the plots for pair distances, speed distribution and distance from center are plotted. The default is True.

        Returns
        -------
        The simulation itself.

        '''
        t_col_info = [] # Stores the 2 balls that are going to be colliding in this collision.
        t_min_col = np.inf # Keeps track of the minimum time to collision
    
        
        for i in range(len(self._balls)):
            for j in range(i, len(self._balls)): # j starts at i to prevent double counting of balls
                if i ==j:
                    continue
                t_col = self._balls[i].time_to_collision(self._balls[j])
                if t_col == None:
                    continue

                if t_col<t_min_col:
                    t_min_col = t_col
                    t_col_info = [self._balls[i], self._balls[j], t_col]
        
        for k in range(len(self._balls)):
            self._balls[k].move(t_min_col)
        
        '''
        Here regarding the intial stages of the balls only the velocity is stored but the whole ball objects stored for post collision. This is because velocities change post collision so can't store full objects. Therefore whenever properties such as mass and radius needed we use the post collision versions
        '''
        ball1i = t_col_info[0]
        ball2i = t_col_info[1]
        ball1i_vel = ball1i.vel()
        ball2i_vel = ball2i.vel()

        t_col_info[0].collide(t_col_info[1], t_min_col)
        
       
        ball1f = t_col_info[0]
        ball2f = t_col_info[1]

        if ball1i._mass == np.inf:
            #If ball 1 is a container impulse for collision calculated and added to total impulse
            Simulation.t_container+=t_min_col
            self.calc_impulse(ball2i_vel, ball2f)
            
        elif ball2i._mass == np.inf:
            #if ball 2 is a container impulse for collision calculated and added to total impulse

            Simulation.t_container+=t_min_col
            self.calc_impulse(ball1i_vel, ball1f)
        else:
            Simulation.t_container+=t_min_col
        
        if plots:
            self.plot_position()
            self.plot_pair_distance()
            self.plot_v_dist()


        '''
        Below appends are to keep track of times at which collissions happen and the pressure, KE, angular momentum, temperature, momentum at those instances.
        '''
        self._press_evol.append(self.calc_pressure(self._con_radius))
        self._col_times.append(Simulation.t_container)
        total_ke = 0
        for ball in self._balls:
            total_ke += ball._KE
        self._ke_evol.append(total_ke)
        self._ang_mom_evol.append(self.calc_ang_mom())
        self._temp_evol.append(self.calc_temp())
        self._mom_evol.append(self.calc_mom())
            
        return self
    
            
    def run(self, num_frames, animate = False, plots = True):
        '''

        Parameters
        ----------
        num_frames : int
            The number of collisions to be carried out in the simulation.
        animate : bool, optional
            If True, the animation is showed. The default is False.
        plots : bool, optional
            If true the plots for pair distances, speed distribution and distance from center are plotted for all frames. Do not have both plots and animate set as true at once as they both prefer different matplotlib backends. The default is True.

        Returns
        -------
        None.

        '''
        if animate:
            f = pl.figure()
            ax = pl.axes(xlim=(-self._con_radius, self._con_radius), ylim=(-self._con_radius, self._con_radius))
            for i in range(len(self._balls)):
                ax.add_patch(self._balls[i].get_patch())
            
        for frame in range(num_frames):
            self.next_collision(plots)
            
            if animate:
                pl.pause(0.00001)

            if animate == True:
                pl.show()
    

