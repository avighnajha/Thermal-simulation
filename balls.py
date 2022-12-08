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
            raise Exception("Invalid time to collision.")
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
    
    

