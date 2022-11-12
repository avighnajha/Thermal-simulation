import numpy as np
import pylab as pl

#%%

class Ball:
    counter = 0
    def __init__(self, mass, radius, position = [0,0], velocity = [0,0]):
        Ball.counter +=1
        velocity = np.array(velocity, dtype = float)
        position = np.array(position, dtype = float)
        self._mass = mass
        self._radius = radius
        self._position = position
        self._velocity = velocity
        if self._radius <0:
            self._patch = pl.Circle(position, radius, ec = "b" ,fill = False)
        else:
            self._patch = pl.Circle(position, radius, fc = "r")
        
        #axes.add_patch(self.ball_patch)
        
    def pos(self):
        return self._position
    def vel(self):
        return self._velocity
    def get_patch(self):
        return self._patch
    def time_to_collision(self, other):
        rel_vel = self.vel() - other.vel()
        rel_pos = self.pos() - other.pos()
        R = self._radius + other._radius 
#        print(rel_vel, rel_pos, R)
#        print("v^2", np.dot(rel_vel, rel_vel))
#        print("r^2", np.dot(rel_pos, rel_pos))
#        print("b ", (np.dot(rel_vel, rel_pos)))
#        print("c ", np.dot(rel_pos, rel_pos) - R**2)
#        print("under sqrt", 4*(np.dot(rel_vel, rel_pos))**2 - 4*np.dot(rel_vel, rel_vel)*(np.dot(rel_pos, rel_pos) - R**2))
        '''
        Where a b and c correspond to coefficients in at^2+bt+c = 0
        '''
        a = np.dot(rel_vel, rel_vel)
        b = 2*np.dot(rel_vel, rel_pos)
        c = np.dot(rel_pos, rel_pos) - R**2
        
        if (b**2 - (4*a*c))<0:
            return None
        elif b>0:
            return None
        t = min((-b + np.sqrt(b**2 - 4*a*c))/(2*a),(-b - np.sqrt(b**2 - 4*a*c))/(2*a))
        if t<0:
            t = max((-b + np.sqrt(b**2 - 4*a*c))/(2*a),(-b - np.sqrt(b**2 - 4*a*c))/(2*a))       
        
        return t
    
    
    def move(self, dt):
        new_position = self.pos() +(dt*self._velocity) 
        self._position = new_position
        self._patch.center = new_position
        return self
        
    def collide(self, other):
        '''
        All parameters labelled with a 1 are self and 2 are the other ball
        '''
        if other._mass == np.inf: #Assuming its alwasy the ball colliding with teh container so "other" is alwasy container
            time = self.time_to_collision(other)
            new_pos = self.pos() +(self.vel()*time)
            new_pos_norm = new_pos/np.sqrt(np.dot(new_pos, new_pos))
            v_norm = np.dot(self.vel(), new_pos_norm)
            v_norm_arr = v_norm*new_pos_norm
            v_par_arr = self.vel() - v_norm_arr
            final_v = v_par_arr - v_norm_arr
            print(self.vel(), self.pos(),other.vel())
            print(time, "time")
            print(new_pos, "new pos")
            print(new_pos_norm, "pos new")
            print(v_norm_arr, "v_norm")
            print(v_par_arr, "v parallel")
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
    def __init__(self,container, ball):
        self._container = container
        self._ball = ball
    
    def next_collision(self):
        t_col = self._ball.time_to_collision(self._container)
        print(t_col, self._ball.vel())
        self._ball.move(t_col)
        self._ball.collide(self._container)
       
        return self
    
    def run(self, num_frames, animate = False):
        if animate:
            f = pl.figure()
            ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
            ax.add_artist(self._container.get_patch())
            ax.add_patch(self._ball.get_patch())
            
        for frame in range(num_frames):
            self.next_collision()
            if animate:
                pl.pause(0.001)
        if animate:
            pl.show()
        
         
             
        
        
    


#%%
