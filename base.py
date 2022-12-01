import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
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
        if self._mass == np.inf:
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
        
        disc = b**2 - 4*a*c
        if abs(a)<1e-7: # 0 relative velocity 
            return None
        if (disc)<0:
            return None
        elif b>0 and self._mass!=np.inf and other._mass != np.inf:
            return None
        #print(f"value of b: {b}, Both possible ts = {(-b + np.sqrt(b**2 - 4*a*c))/(2*a),(-b - np.sqrt(b**2 - 4*a*c))/(2*a)}")
        t_minus = (-b - np.sqrt(disc))/(2*a)
        t_plus = (-b + np.sqrt(disc))/(2*a)
        
        
        if t_minus <0 and t_plus<0:
            return None
        else:
            t = min(t_minus, t_plus)
            #if t<0 and abs(t)<1e-7:
                #t = abs(t)
            if t<1e-7:
                t = max(t_minus, t_plus)
            
        # if t_minus>=0 and t_plus>=0:
        #     t = min(t_minus, t_plus)
        # elif t_minus<0 and t_plus>=0:
        #     if abs(t_minus)<1e-7:
        #         t = abs(t_minus)
        #     else:
        #         t = t_plus
        # elif t_minus>=0 and t_plus<0:
        #     if abs(t_plus)<1e-7:
        #         t = abs(t_plus)
        # else:
        #     return None
            
        # t = min((-b + np.sqrt(disc))/(2*a),(-b - np.sqrt(disc))/(2*a))
        # if t<=0:
        #     t = max((-b + np.sqrt(b**2 - 4*a*c))/(2*a),(-b - np.sqrt(b**2 - 4*a*c))/(2*a))
        return t
    
    
    def move(self, dt):
        new_position = self.pos() +(dt*self._velocity) 
        
        self._position = new_position
        #self._patch.center = new_position
        self.get_patch().center = new_position

        return self
        
    def collide(self, other, t_min):
        '''
        All parameters labelled with a 1 are self and 2 are the other ball
        '''
        if other._mass == np.inf: #Assuming its alwasy the ball colliding with teh container so "other" is alwasy container
            print("Self", self)
            print("Other", other)
            #time = self.time_to_collision(other)
            #time = t_min Dont need this as ball already moved.
            #print("time:", time)
            new_pos = self.pos() #+(self.vel()*time)
            print("New pos: ", new_pos)
            new_pos_norm = new_pos/np.sqrt(np.dot(new_pos, new_pos))
            print("new pos norm: ", new_pos_norm)
            v_norm = np.dot(self.vel(), new_pos_norm)
            v_norm_arr = v_norm*new_pos_norm
            v_par_arr = self.vel() - v_norm_arr
            print("v norm, v par: ", v_norm_arr, v_par_arr)
            final_v = v_par_arr - v_norm_arr

            self._velocity = final_v
            print("final v:", self._velocity, self.vel())
            
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
    impulse_tot = 0 # Seems to be a problem here cuz class variable carries over to all isntances of class. so my pressure calcs have all been adding up
    t_container = 0
    def __init__(self,container, velfactor):
        
        self._container = container
        
        #balls = generate_balls()
          
        balls = []
        rs = [3, 6, 9]
        
        vel_overall = [0,0]
        for r in rs:
            splits = 2*np.pi/r
            
            for j in range(r):
                radius = 0.5
                mass = 1
                theta = splits*j
                velocityx = np.random.uniform(-10,10)
                velocityy = np.random.uniform(-10,10)
                vel = velfactor*np.array([velocityx, velocityy])
                vel_overall+=vel
                if r == 9:
                    r = 8.5
                posx = r*np.cos(theta)
                posy = r*np.sin(theta)
                pos = np.array([posx, posy])
                ball = Ball(radius, mass, pos, vel)
                balls.append(ball)
        vel_remaining = -vel_overall
        ball_center = Ball(1, 1, [0,0], vel_remaining)
        balls.append(ball_center)
        # balls = [Ball(1, 1, [1, 5], [np.random.uniform(-10, 10), np.random.uniform(-10, 10)]), Ball(1, 1, [-3, 5], [np.random.uniform(-10, 10), np.random.uniform(-10, 10)]), Ball(1, 1, [-1, -7], [np.random.uniform(-10, 10), np.random.uniform(-10, 10)])] # 3 test balls
        balls.append(self._container)
        self._balls = balls
        '''
        Added below to arrays to allow me to track the pressures at each container collisiona nd what times they happen so I can plot the vairation of pressure over time.
        '''
        self._press_evol = []
        self._col_times = []
        
    
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
        
    def plot_position(self, balls):
        positions = []
        for ball in balls:
            positions.append(np.sqrt(np.dot(ball.pos(), ball.pos())))                             
        #print(positions)
        plt.hist(positions)
        plt.title("Distance from center")
        plt.xlabel("Distance from center")
        plt.ylabel("Number of balls")
        plt.grid()
        plt.show()
    def plot_pair_distance(self, balls):
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
        plt.hist(distances)
        plt.title("Pair distances")
        plt.xlabel("Distance between pair of balls ")
        plt.ylabel("Number of balls")
        plt.grid()
        plt.show()
    def plot_pressure_evol(self):
        plt.plot(self._col_times, self._press_evol)
        plt.xlabel("Time (s)")
        plt.ylabel("Pressure")
        plt.grid()
        plt.show()
        
    def next_collision(self, plots = True):
        t_col_info = []
        t_min_col = np.inf
        #print("All Balls", self._balls)
        '''
        Here balls r double counted so need to optimise
        ''' 
        
        for i in range(len(self._balls)):
            for j in range(len(self._balls)):
                if self._balls[j]._mass == np.inf:
                # elif self._balls[j]._mass == np.inf and self._balls[i]._mass == np.inf:
                #     print("!!!!!!!!!!CONTAINER TO CONTAINER COLLISION!!!!!!!!!")
                #print('''Balls in cons:''', self._balls[i], self._balls[j])
                if i ==j:
                    continue
                t_col = self._balls[i].time_to_collision(self._balls[j])
                if t_col == None:
                    continue
                #print("Time for this col:", t_col)
                #print("Min time: ", t_min_col)
                if t_col == 0:
                    print("Balls colliding:", self._balls[i], self._balls[j])

                if t_col<t_min_col:
                    t_min_col = t_col
                    t_col_info = [self._balls[i], self._balls[j], t_col]
                    #print(t_col_info)
        print("MOVING TIME", t_min_col)
        for k in range(len(self._balls)):
            self._balls[k].move(t_min_col)
        
        #print("Balls pre col", t_col_info)
        #print(t_col_info[1]._KE)
        '''
        Here regarding the intial stages of the balls only the velocity is stored but the whole ball objects stored for post collision. bEcasue velcoities change post collision so cant store full objects. Therefore whenever properties such as mass and radius needed we use the post collision versions
        '''
        ball1i = t_col_info[0]
        ball2i = t_col_info[1]
        ball1i_vel = ball1i.vel()
        ball2i_vel = ball2i.vel()
        
        KEi1 = ball1i._KE
        KEi2 = ball2i._KE #Change it to self._KE
        
        t_col_info[0].collide(t_col_info[1], t_min_col)
        
       
        ball1f = t_col_info[0]
        ball2f = t_col_info[1]
        
        KEf1 = ball1f._KE
        KEf2 = ball2f._KE #Change it to self._KE
        #print(ball1i_vel, ball1f)
    
        if ball1i._mass == np.inf:
            #if t_min_col == 0:
            #    Simulation.t_container = t_prev_min
            Simulation.t_container+=t_min_col
            #print(ball2i_vel, ball2f)
            self.calc_impulse(ball2i_vel, ball2f)
        elif ball2i._mass == np.inf:
            # if t_min_col == 0:
            #     Simulation.t_container = t_prev_min
            Simulation.t_container+=t_min_col
            self.calc_impulse(ball1i_vel, ball1f)
        else:
            Simulation.t_container+=t_min_col
        
        #print("Balls post col", t_col_info)
        if (KEi1 - KEf1)<0.001 and (KEi2 - KEf2)<0.001:
            print("ALL KE CONSERVED")
        else:
            print("KEs not conserved")
        if plots:
            self.plot_position(self._balls)
            self.plot_pair_distance(self._balls)
        print(f'''
              Collided balls
              Initially: {ball1i, ball2i}
              Finally: {ball1f, ball2f}
              ''')
        if t_min_col <0:
            
            print(f'''
                  ###########
                  NEGATIVE TIME FOR COLLISION
                  Balls initiAally = {ball1i, ball2i}
                  Balls post = {ball1f, ball2f}
                  ###########
                  ''')
            
        print("Min time:", t_min_col)
        print("Total time:", Simulation.t_container)
        #print("Final all balls", self._balls)
        '''
        Below appends are to keep track of times at which collissions happen and the pressure at those instances.
        '''
        self._press_evol.append(self.calc_pressure(2*np.pi*10))
        self._col_times.append(Simulation.t_container)
        print("Total pressure till here: ", self.calc_pressure(2*np.pi*10))
        print("---------------------------------")
        return self
    def calc_temp(self):
        totalKE = 0
        k = 1.38e-23
        for ball in self._balls:
            totalKE += ball._KE
        temp = 2*totalKE/(3*k)
        return temp
            
    def run(self, num_frames, animate = False, plots = True):
        if animate:
            f = pl.figure()
            ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
            for i in range(len(self._balls)):
                ax.add_patch(self._balls[i].get_patch())
            
        for frame in range(num_frames):
            self.next_collision(plots)
            
            if animate:
                pl.pause(0.00001)

            if animate == True:
                pl.show()
    

