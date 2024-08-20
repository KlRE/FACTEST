import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 7'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.16439898730535737, 0.9863939238321437], [0.6923288217962462, -0.7215821522946793], [-0.9899494936611667, 0.1414213562373094], [-0.9938837346736189, -0.11043152607484648]])
b1 = np.array([11.425729617722332, 0.823968809039195, -1.9091883092036803, -4.163268533021714])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.5051792015689375, 0.8630144693469346], [0.5900165893423103, 0.8073911222578979], [-0.9386697595167285, -0.3448174626796145], [0.871152209203766, -0.49101306336939543]])
b2 = np.array([18.04963188939016, 18.694209830740565, -15.537857998857518, 10.770609131973835])
O2 = pc.Polytope(A2, b2)
A3 = np.array([[0.1737853339090472, 0.9847835588179369], [-0.8840349603087043, -0.4674207836114989], [0.658504607868518, 0.752576694706878], [0.7917822555634717, -0.6108034542918214]])
b3 = np.array([16.25472156495959, -16.371921012061893, 18.993154332664833, 8.58970635535572])
O3 = pc.Polytope(A3, b3)
A4 = np.array([[0.6515919145275291, 0.7585696915395113], [0.2095290887308733, 0.9778024140774095], [-0.498471124258083, -0.866906303057535], [-0.511805175094578, -0.859101543908756]])
b4 = np.array([21.11449560642863, 20.219557062529287, -19.477217363945172, -19.56740856924092])
O4 = pc.Polytope(A4, b4)
A5 = np.array([[-0.1046847845180428, -0.994505452921406], [-0.25912856608734963, -0.9658428372346685], [0.27881019486395553, 0.9603462267536241], [-0.9246780984747164, -0.38074980525429397]])
b5 = np.array([-16.885655742760296, -18.16255676848608, 19.64682506474673, -12.999886207968055])
O5 = pc.Polytope(A5, b5)
A6 = np.array([[-0.9976303284229833, -0.06880209161537806], [0.7665204811801636, -0.6422198626104074], [-0.3713906763541052, 0.9284766908852587], [0.7071067811865476, 0.7071067811865475]])
b6 = np.array([-9.047475047422227, -1.8065023232137933, 14.18712383672674, 19.516147160748712])
O6 = pc.Polytope(A6, b6)
O = [O1, O2, O3, O4, O5, O6]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
