import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 8'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.2544932992796438, 0.9670745372626466], [-0.9690145353270456, 0.24700370508336475], [-0.199604482144226, 0.9798765487080173], [0.6145754526161543, -0.7888580436565563]])
b1 = np.array([14.699532966392228, -4.833672505631377, 15.558262090041737, -4.900092638620145])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.6273295378726444, -0.7787539090832831], [0.9774761341556752, -0.21104598351088427], [-0.8398448353890342, -0.5428265399465708], [0.20829198036780217, 0.9780666904227234]])
b2 = np.array([-11.244341165041401, 17.37797058961993, -13.554276282363995, 12.80814555800794])
O2 = pc.Polytope(A2, b2)
A3 = np.array([[0.6207029443655611, 0.7840458244617615], [0.4534572437205525, -0.8912780307610862], [-0.22903933372554644, 0.9734171683335762], [-0.9315776194850603, -0.3635424856527066]])
b3 = np.array([20.953624658740576, -2.261031635930758, 14.618435475033067, -15.325587910796909])
O3 = pc.Polytope(A3, b3)
A4 = np.array([[0.9979253089684582, -0.06438227799796482], [0.7440487115290025, 0.6681253736178796], [-0.5792071321891946, -0.815180408266274], [-0.9971641204866132, -0.07525766947068752]])
b4 = np.array([19.131193907095312, 20.136387680787962, -15.451959159847291, -16.24248651351119])
O4 = pc.Polytope(A4, b4)
A5 = np.array([[0.9221201798103953, -0.3869035719484176], [-0.0, -1.0], [-0.36039927920216247, 0.9327981344055969], [-0.9939944406408661, -0.10943058062101271]])
b5 = np.array([12.57049705260409, -0.40000000000000036, 6.576226847559456, -12.170504408066972])
O5 = pc.Polytope(A5, b5)
A6 = np.array([[0.9533422253507436, 0.3018917046944019], [-0.06237828615518045, -0.9980525784828888], [-0.8944271909999152, 0.4472135954999593], [-0.990830168044299, 0.13511320473331306]])
b6 = np.array([19.019177395747338, -4.179345172397095, -11.269782606598918, -15.222754399953322])
O6 = pc.Polytope(A6, b6)
A7 = np.array([[0.0, 1.0], [-1.0, 0.0], [0.9928768384869222, 0.11914522061842953], [0.18208926018230753, -0.9832820049844603]])
b7 = np.array([18.5, -15.2, 19.678818938810778, -12.473114322488062])
O7 = pc.Polytope(A7, b7)
O = [O1, O2, O3, O4, O5, O6, O7]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
