import polytope as pc
import numpy as np

title = '2D Curve Environment (Rotated 90 Degrees)'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])


# Function to rotate the b vector by 90 degrees
def rotate_b_vector(b):
    return np.array([b[2], b[3], b[0], b[1]])


# Original b vectors
b0 = np.array([-6, 7, 4, -3])
b1 = np.array([-6, 7, -5, 6])
b2 = np.array([-1, 3, 4, -2])
b3 = np.array([1, 1, 2, 0])
b4 = np.array([3, -1, 0, 2])
b5 = np.array([1, 1, -2, 4])
b6 = np.array([-1, 3, -4, 6])

# Apply the shift before rotation
shift = 6
b2_shifted = np.array([b2[0] - shift, b2[1] + shift, b2[2], b2[3]])
b3_shifted = np.array([b3[0] - shift, b3[1] + shift, b3[2], b3[3]])
b4_shifted = np.array([b4[0] - shift, b4[1] + shift, b4[2], b4[3]])
b5_shifted = np.array([b5[0] - shift, b5[1] + shift, b5[2], b5[3]])
b6_shifted = np.array([b6[0] - shift, b6[1] + shift, b6[2], b6[3]])

# Apply the rotation to all b vectors (original and shifted)
b0_rotated = rotate_b_vector(b0)
b1_rotated = rotate_b_vector(b1)
b2_rotated = rotate_b_vector(b2)
b3_rotated = rotate_b_vector(b3)
b4_rotated = rotate_b_vector(b4)
b5_rotated = rotate_b_vector(b5)
b6_rotated = rotate_b_vector(b6)

b8_rotated = rotate_b_vector(b2_shifted)
b9_rotated = rotate_b_vector(b3_shifted)
b10_rotated = rotate_b_vector(b4_shifted)
b11_rotated = rotate_b_vector(b5_shifted)
b12_rotated = rotate_b_vector(b6_shifted)

Theta = pc.Polytope(A, b0_rotated)
G = pc.Polytope(A, b1_rotated)

# Original obstacles (rotated)
O1_rotated = pc.Polytope(A, b2_rotated)
O2_rotated = pc.Polytope(A, b3_rotated)
O3_rotated = pc.Polytope(A, b4_rotated)
O4_rotated = pc.Polytope(A, b5_rotated)
O5_rotated = pc.Polytope(A, b6_rotated)

# Shifted obstacles (rotated)
O6_rotated = pc.Polytope(A, b8_rotated)
O7_rotated = pc.Polytope(A, b9_rotated)
O8_rotated = pc.Polytope(A, b10_rotated)
O9_rotated = pc.Polytope(A, b11_rotated)
O10_rotated = pc.Polytope(A, b12_rotated)

# Combine original and shifted obstacles into one list
O = [O1_rotated, O2_rotated, O3_rotated, O4_rotated, O5_rotated,
     O6_rotated, O7_rotated, O8_rotated, O9_rotated, O10_rotated]

# Workspace rotated (assuming workspace needs to be rotated similarly)
workspace = pc.Polytope(A, rotate_b_vector(np.array([3, 9, 5, 7])))

if __name__ == "__main__":
    from plot_env import plot_env

    plot_env(title, Theta, G, O, workspace)
