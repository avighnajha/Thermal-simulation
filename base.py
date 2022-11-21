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
        if self._mass == np.inf:
            self._KE = 0
        else:
            self._KE = self._mass*np.dot(self._velocity, self._velocity)/2
        if self._radius<0:
            self._patch = pl.Circle(self._position, self._radius, ec = "b" ,fill = False)
        else:
            self._patch = pl.Circle(self._position, self._radius, fc = "r")

    def __repr__(self):
        return f"Ball at {self._position}, with speed {self._velocity}"
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
    impulse_tot = 0
    t_container = 0
    def __init__(self,container, balls):
        
        self._container = container
        balls.append(self._container)
        
        self._balls = balls
        
    
    def calc_impulse(self, balli_vel, ballf):
        vi = balli_vel
        vf = ballf.vel()
        mass = ballf._mass
        impulse = mass*(vf-vi)
        impulse_mag = np.sqrt(np.dot(impulse, impulse))
        Simulation.impulse_tot += impulse_mag
        print("Collision impulse: ", impulse_mag)
        print("Total Impulse: ", Simulation.impulse_tot)
        return Simulation.impulse_tot
    
    def calc_pressure(self, perimeter):
        force = Simulation.impulse_tot/Simulation.t_container
        pressure = force/perimeter
        return pressure
        
    
    def next_collision(self):
        t_col_info = []
        t_min_col = np.inf
        #print("All Balls", self._balls)
        '''
        Here balls r double counted so need to optimise
        '''
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
        #print(t_col_info[1]._KE)
        '''
        Here regarding the intial stages of the balls only the velocity is stored but the whole ball objects stored for post collision. bEcasue velcoities change post collision so cant store full objects. Therefore whenever properties such as mass and radius needed we use the post collision versions
        '''
        ball1i = t_col_info[0]
        ball2i = t_col_info[1]
        ball1i_vel = ball1i.vel()
        ball2i_vel = ball2i.vel()
        
        KEi1 = ball1i._KE
        KEi2 = 0 #Change it to self._KE
        t_col_info[0].collide(t_col_info[1])
        
       
        ball1f = t_col_info[0]
        ball2f = t_col_info[1]
        
        KEf1 = ball1f._KE
        KEf2 = 0 #Change it to self._KE
        #print(ball1i_vel, ball1f)
        
        '''
        For pressure calc need to add functionality for if 2 balls collide at the same time
        '''
        if ball1i._mass == np.inf:
            #if t_min_col == 0:
            #    Simulation.t_container = t_prev_min
            Simulation.t_container+=t_min_col
            print(ball2i_vel, ball2f)
            self.calc_impulse(ball2i_vel, ball2f)
        elif ball2i._mass == np.inf:
            # if t_min_col == 0:
            #     Simulation.t_container = t_prev_min
            Simulation.t_container+=t_min_col
            self.calc_impulse(ball1i_vel, ball1f)
        else:
            Simulation.t_container+=t_min_col
        
        print("Balls post col", t_col_info)
        if (KEi1 - KEf1)<0.001 and (KEi2 - KEf2)<0.001:
            print("ALL KE CONSERVED")
        else:
            print("KEs not conserved")
        
        #print("Min time", t_min_col)
        #print("Final all balls", self._balls)
        print("Total pressure till here: ", self.calc_pressure(2*np.pi*10))
        print("---------------------------------")
        return self
    def generate_balls(self):
        balls = []
        vel_overall = [0,0]
        for r in range(3, 10, 3):
            splits = 2*np.pi/r
            print("r = ", r)
            for j in range(r):
                radius = 0.1
                mass = 1
                theta = splits*j
                velocityx = np.random.uniform(-10,10)
                velocityy = np.random.uniform(-10,10)
                vel = np.array([velocityx, velocityy])
                vel_overall+=vel
                posx = r*np.cos(theta)
                posy = r*np.sin(theta)
                pos = np.array([posx, posy])
                ball = Ball(radius, mass, pos, vel)
                balls.append(ball)
        vel_remaining = -vel_overall
        ball_center = Ball(1, 1, [0,0], vel_remaining)
        balls.append(ball_center)
        #balls.append(self._container)
        return balls
        
    def run(self, num_frames, animate = False):
        if animate:
            f = pl.figure()
            ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
            for i in range(len(self._balls)):
                ax.add_patch(self._balls[i].get_patch())
            
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
                pl.pause(0.001)

            if animate == True:
                pl.show()
    

