import numpy as np
from scipy.integrate import odeint
from math import sin, cos, tan, atan, pi, sqrt, ceil

class dubins_car_v2:
    def __init__(self) -> None:
        #############################
        # Tracking controller gains #
        #############################
        self.k0 = 10000 #might need to change different k values higher usually converges
        self.k1 = 1000
        self.k2 = 1000
        self.k3 = 1000

        self.length = 5

        #######################################################
        # Reference state-input trajectories (For simulation) #
        #######################################################
        self.state_ref = None
        self.input_ref = None

        self.state_ref_traj = None
        self.input_ref_traj = None

        # ##########################
        # # Initializing car state #
        # ##########################
        # self.initial_state = initial_state 
        # # self.initial_mode = initial_mode
        # self.curr_state = initial_state # For simulation

        self.dt = 0.01

    def dubinsDynamics(self, state, t, input):
        x,y,theta = state
        v, w = input

        xdot = v*cos(theta)
        ydot = v*sin(theta)
        thetadot = w
        
        return [xdot, ydot, thetadot]

    def dubinsControlledDynamics(self, state, t):
        ref_idx = ceil(t/self.dt)
        if ref_idx >= len(self.ref_traj):
            ref_idx = len(self.ref_traj)-1

        ref_state = self.ref_traj[ref_idx]
        ref_input = self.ref_input[ref_idx]
        # v,w = self.trackingControl(state, ref_state, ref_input)
        v,phi = self.trackingControl(state, ref_state, ref_input)
        
        x,y,theta = state
        # v, w = input

        xdot = v*cos(theta)
        ydot = v*sin(theta)
        # thetadot = w
        thetadot = (v/self.length)*tan(phi)

        return [xdot, ydot, thetadot]

    def trackingControl(self, curr_state, ref_state, ref_input):
        x,y,theta = curr_state
        xref,yref,thetaref = ref_state
        vref,wref = ref_input

        xerr = (xref - x)*cos(theta) + (yref - y)*sin(theta)
        yerr = (xref - x)*(-sin(theta)) + (yref - y)*cos(theta) 
        
        xerr = -xerr
        yerr = -yerr
        thetaerr = thetaref - theta
        #thetaerr bar is thetaerr - alpha dot
        v = vref*cos(thetaerr) + self.k1/100*xerr
        w = wref + vref*(self.k2/100*yerr + self.k3/100*sin(thetaerr)) 

        # f1 = sin(thetaerr) / thetaerr
        # v = -self.k1*xerr + vref*cos(thetaerr)
        # w = -self.k2*thetaerr + wref - self.k0*vref*yerr*f1 #thetaerr change to theta bar, need to *last by f1 and add a.
        
        #can set ρ to 0 or 1     for this one set to 0

        phi = np.clip(atan(w*self.length/v),-pi, pi)

        # input = [v, w]
        input = [v,phi]

        return input
    # def errBound(self, init_poly, i):
    #     err_0 = init_poly.chebR*sqrt(2)
    #     err = sqrt(err_0**2 + (4*i)/(self.k2))
    #     # err = 0.1
    #     return err
    def errBound(self, init_poly, i):
        err_0 = init_poly.chebR*sqrt(2)
        # err = sqrt(err_0**2 + (2*i*np.pi**2)/(self.k2))
        err = sqrt(err_0**2 + (4*i)/(self.k2))
        # print("err: ", err)
        return err
        
    def set_ref(self, xref, vref):
        self.ref_traj = []
        self.ref_input = []

        curr_time = 0
        prev_t = 0
        for i in range(len(xref)-1):
            p1 = xref[i]
            p2 = xref[i+1]

            mx = p2[0] - p1[0]
            bx = p1[0]
            
            my = p2[1] - p1[1]
            by = p1[1]
            
            theta_ref = np.arctan2((np.array(p2) - np.array(p1))[1], (np.array(p2) - np.array(p1))[0])

            t = np.linalg.norm(np.array(p2)-np.array(p1))/vref

            while curr_time <= t + prev_t:
                px = mx*((curr_time - prev_t)/t) + bx
                py = my*((curr_time - prev_t)/t) + by
                self.ref_traj.append((px,py,theta_ref))
                self.ref_input.append((vref,0))
                curr_time += self.dt

            prev_t += t

        return None

    def set_timed_ref(self, xref):
        self.ref_traj = []
        self.ref_input = []

        curr_time = 0
        prev_t = 0
        for i in range(len(xref)-1):
            p1 = xref[i]
            p2 = xref[i+1]

            mx = p2[0] - p1[0]
            bx = p1[0]
            
            my = p2[1] - p1[1]
            by = p1[1]
            
            theta_ref = np.arctan2((np.array(p2) - np.array(p1))[1], (np.array(p2) - np.array(p1))[0])

            t = p2[2] - p1[2]
            vref = np.linalg.norm(np.array(p2) - np.array(p1))/t

            while curr_time <= t + prev_t:
                px = mx*((curr_time - prev_t)/t) + bx
                py = my*((curr_time - prev_t)/t) + by
                self.ref_traj.append((px,py,theta_ref))
                self.ref_input.append((vref,0))
                curr_time += self.dt

            prev_t += t
            
        return None

    def run_simulation(self, xref, initial_state, T, vref = 1, sim_type = "base"): #TODO: MAY WANT TO COME UP WITH A BETTER WAY TO DO THIS
        if sim_type == "base":
            self.set_ref(xref, vref)
        else:
            self.set_timed_ref(xref)

        time_array = np.arange(0,T,self.dt)
        state_trace = odeint(self.dubinsControlledDynamics, initial_state, time_array, full_output = 1)
        return state_trace

    def run_omega_simulation(self, hybrid_aut, curr_state, vref = 1, num_cycles = 3):
        if len(hybrid_aut.buchi_inits) > 1:
            raise Exception('Runs not implemented for automata with multiple possible initial states!')


        curr_buchi_state = hybrid_aut.buchi_inits[0]

        prefix_run = hybrid_aut.buchi_run['prefix']
        cycle_run = hybrid_aut.buchi_run['cycle']

        all_states = [] #TODO: MAY WANT TO SEPERATE CYCLES

        for transition in prefix_run:
            print('curr buchi state is ', curr_buchi_state)
            print('prefix transition is ', transition)
            possible_transitions = hybrid_aut.buchi_transitions[curr_buchi_state]

            possible_flows = hybrid_aut.flows[curr_buchi_state][str(transition)]
            found_flow = False
            for potential_flow in possible_flows:
                init_part = potential_flow['init']
                if init_part.contains(np.array([[curr_state[0]],[curr_state[1]]]))[0] and not found_flow:
                    waypoints = potential_flow['xref']
                    found_flow = True

            print('running simulation from ', curr_state)
            length = 0
            for i in range(1,len(waypoints)):
                length += np.linalg.norm(np.array(waypoints[i] - np.array(waypoints[i-1])))
            
            T = length/vref
            
            if length > 0:
                states = self.run_simulation(waypoints, curr_state, T, vref=vref)
                curr_state = states[-1]
                all_states.extend(states)

            for potential_transition in possible_transitions:
                if potential_transition[0] == transition:
                    #TODO: NEED TO USE THE JUMP FUNCTIONS HERE TO RUN A CHECK
                    print('updating buchi state to ', potential_transition[1])
                    curr_buchi_state = potential_transition[1]

        curr_cycle = 1
        while curr_cycle <= num_cycles:
            for transition in cycle_run:
                print('curr buchi state is ', curr_buchi_state)
                print('cycle ', curr_cycle,' transition is ', transition)
                possible_transitions = hybrid_aut.buchi_transitions[curr_buchi_state]

                possible_flows = hybrid_aut.flows[curr_buchi_state][str(transition)]
                found_flow = False
                for potential_flow in possible_flows:
                    init_part = potential_flow['init']
                    if init_part.contains(np.array([[curr_state[0]],[curr_state[1]]]))[0] and not found_flow:
                        waypoints = potential_flow['xref']
                        found_flow = True

                print('running simulation from ', curr_state)
                length = 0
                for i in range(1,len(waypoints)):
                    length += np.linalg.norm(np.array(waypoints[i] - np.array(waypoints[i-1])))
                
                T = length/vref
                
                if length > 0: #TODO: NEED TO FIGURE OUT WHAT TO DO WHEN THE LENGTH IS 0
                    states = self.run_simulation(waypoints, curr_state, T, vref=vref)

                    keep_running = True
                    for state in states:
                        if keep_running:
                            all_states.append(state)
                            goal_poly = hybrid_aut.transition_reqs[str(transition)]['goal'][0]
                            if goal_poly.contains(np.array([[state[0]],[state[1]]]))[0] :
                                keep_running = False


                    curr_state = all_states[-1]
                    # all_states.extend(states)

                for potential_transition in possible_transitions:
                    if potential_transition[0] == transition:
                        #TODO: NEED TO USE THE JUMP FUNCTIONS HERE TO RUN A CHECK
                        print('updating buchi state to ', potential_transition[1])
                        curr_buchi_state = potential_transition[1]
            curr_cycle += 1
        
        return all_states

    def simulate_run(self, initial_state, sample_run, flow_cache, init_sets, vref = 1):
        initial_set = init_sets[sample_run[0]]
        if not initial_set.__contains__(np.array(initial_state[:2]).T):
            raise Exception("Initial state is not contained within initial set!")

        all_states = []
        for i in range(len(sample_run)-1):
            flow_dict = flow_cache[sample_run[i]+','+sample_run[i+1]]
            for flow_id in flow_dict.keys():
                if flow_dict[flow_id]['poly'].__contains__(np.array(initial_state[:2]).T):
                    break
            
            xref = flow_dict[flow_id]['xref']
            T = 0
            for point_idx in range(len(xref)-1):
                T += np.linalg.norm(np.array(xref[point_idx+1]) - np.array(xref[point_idx]))

            states = self.run_simulation(xref, initial_state, T, vref = vref)
            initial_state = states[-1]
            
            all_states.extend(states)

        return all_states

    #################################################################################################
    # Following code is in case we want to run reachability analysis on the synthesized controllers #
    #################################################################################################
    # def simulate(self, mode, initial_state, time_horizon, time_step):
    #     time_array = np.arange(0, time_horizon+time_step, time_step)
    #     if self.state_ref == None and self.input_ref == None:
    #         # No controller used here!
    #         input = [0, 0]
    #     elif (self.state_ref == None and self.input_ref != None) or (self.state_ref != None and self.input_ref == None):
    #         # Either the state or reference trajectory is not defined
    #         raise Exception('Both state and input trajectories must be defined!')
    #     else:
    #         # This is where both state and reference trajectories are defined
    #         input = self.trackingControl(initial_state, self.state_ref, self.input_ref)
    #     state_trace = odeint(self.dubinsDynamics, initial_state, time_array, args=(input,))
    #     trace = []
    #     for i in range(len(time_array)):
    #         trace.append([time_array[i]]+list(state_trace[i]))
    #     return trace

    # def TC_simulate(self, mode, initialSet, time_horizon, time_step, map=None):
    #     #TODO: Implement TC simulate for reachability
    #     return None
