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
        # if self._radius <0:
        #     self._patch = pl.Circle(position, radius, ec = "b" ,fill = False)
        # else:
        #     self._patch = pl.Circle(position, radius, fc = "r")
        
        #axes.add_patch(self.ball_patch)
    def __repr__(self):
        return f"Ball at {self._position}, with speed {self._velocity}"
    def pos(self):
        return self._position
    def vel(self):
        return self._velocity
    def get_patch(self):
        if self._radius <0:
            patch = pl.Circle(self.pos(), self._radius, ec = "b" ,fill = False)
        else:
            patch = pl.Circle(self.pos(), self._radius, fc = "r")
        return patch
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
        
        if (b**2 - (4*a*c))<0 :
            return None
        elif b>0 and other._mass != np.inf:
            return None
        t = min((-b + np.sqrt(b**2 - 4*a*c))/(2*a),(-b - np.sqrt(b**2 - 4*a*c))/(2*a))
        if t<=0:
            t = max((-b + np.sqrt(b**2 - 4*a*c))/(2*a),(-b - np.sqrt(b**2 - 4*a*c))/(2*a))       
        
        return t
    
    
    def move(self, dt):
        new_position = self.pos() +(dt*self._velocity) 
        
        self._position = new_position
        #self._patch.center = new_position
        self.get_patch().center = new_position

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
            # print(self.vel(), self.pos(),other.vel())
            # print(time, "time")
            # print(new_pos, "new pos")
            # print(new_pos_norm, "pos new")
            # print(v_norm_arr, "v_norm")
            # print(v_par_arr, "v parallel")
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
    def __init__(self,container, balls):
        self._container = container
        self._balls = balls
        self._balls.append(self._container)
    
    def next_collision(self):
        t_col_info = []
        t_min_col = np.inf
        print("All Balls", self._balls)
        for i in range(len(self._balls)):
            for j in range(len(self._balls)):
                if i ==j:
                    continue
                t_col = self._balls[i].time_to_collision(self._balls[j])
                if t_col == None:
                    
                    continue
                #print(t_col, t_min_col)

                if t_col<t_min_col:
                    t_min_col = t_col
                    t_col_info = [self._balls[i], self._balls[j], t_col]
                    #print(t_col_info)
                    
        for k in range(len(self._balls)):
            self._balls[k].move(t_min_col)
        
        print("Balls pre col", t_col_info)
        # ball1 = t_col_info[0]
        # ball2 = t_col_info[1]
        # KEi1 = np.dot(ball1.vel(), ball1.vel())* ball1._mass/2
        # KEi2 = np.dot(ball2.vel(), ball2.vel())* ball2._mass/2
        
        t_col_info[0].collide(t_col_info[1])
        
        # KEf1 = = np.dot(ball1.vel(), ball1.vel())* ball1._mass/2
        # KEf2 = np.dot(ball2.vel(), ball2.vel())* ball2._mass/2
        
        # if KEi1 == KEf1 and KEi2 == KEf2:
        #     print("ALL KE CONSERVED")
        
        #t_col = self._balls.time_to_collision(self._container)
        #print("v before col", self._balls.vel(), ", collision time", t_col, )
        # self._balls.move(t_col)
        # self._balls.collide(self._container)
        #print(", v post col", self._balls.vel())
        print("Balls post col", t_col_info)
        print("Min time", t_min_col)
        print("Final all balls", self._balls)
        print("---------------------------------")
        return self
    
    def run(self, num_frames, animate = False):
        if animate:
            f = pl.figure()
            ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
            ax.add_artist(self._container.get_patch())
            ax.add_patch(self._balls.get_patch())
            
        for frame in range(num_frames):
            
            # v_init = self._balls.vel()
            # mass = self._balls._mass
            # KEi = (mass*np.dot(v_init,v_init))/2
            # t_col_impulse = self._balls.time_to_collision(self._container)
            # container_per = -2*np.pi*self._container._radius # -ve sign as we define container with -ve radius
            self.next_collision()
            #v_fin = self._balls.vel()
            #KEf = (mass*np.dot(v_fin, v_fin))/2
            
            # if abs(KEi - KEf)<0.001:
            #     print("KE conserved")
            # else:
            #     print("KE not conserved")
            #     raise "KE not conserved"
            # # print("ball pos", self._ball.pos())
            # # print(self._ball.get_patch())
            # '''
            # Calculating pressure on container
            # '''
            # impulse = mass*(v_fin-v_init)
            # impulse_mag = np.sqrt(np.dot(impulse, impulse))
            # force = impulse_mag/t_col_impulse
            # pressure = force/container_per
            # print(f"Pressure from that collision: {pressure}")
            if animate:
                pl.pause(0.01)

        if animate == True:
            pl.show()
    

