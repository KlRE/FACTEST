import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 4'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.4830773429113347, -0.8755776840267943], [0.8797065135761271, -0.475517034365474], [-0.9966696040549201, 0.08154569487722083], [0.04489849680945924, 0.9989915540104686]])
b1 = np.array([-6.566832630200958, 0.014265511030964628, 0.6115927115791564, 18.52175239632218])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.8502651466878615, -0.5263546146162961], [-0.4236851089014133, 0.9058095431685391], [0.3060091804131214, -0.9520285612852641], [-0.04756514941545007, -0.9988681377244375]])
b2 = np.array([1.4737929209256126, 10.977827269949039, -11.747352425859232, -15.606125523208952])
O2 = pc.Polytope(A2, b2)
A3 = np.array([[-0.9557790087219502, 0.2940858488375231], [0.8320502943378443, 0.5547001962252283], [-0.7071067811865476, -0.7071067811865476], [0.9990958406831207, -0.04251471662481349]])
b3 = np.array([-9.506325063672936, 21.328222544860054, -14.707821048680191, 15.052335421015275])
O3 = pc.Polytope(A3, b3)
O = [O1, O2, O3]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
