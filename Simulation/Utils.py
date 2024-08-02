import numpy as np

def circumcenter(A, B, C):
    # Convert points to NumPy arrays
    A, B, C = np.array(A), np.array(B), np.array(C)

    # Calculate midpoints of AB and BC
    mid_AB = (A + B) / 2
    mid_BC = (B + C) / 2

    # Calculate slopes of AB and BC
    slope_AB = (B[1] - A[1]) / (B[0] - A[0]) if B[0] != A[0] else np.inf
    slope_BC = (C[1] - B[1]) / (C[0] - B[0]) if C[0] != B[0] else np.inf

    # Calculate slopes of the perpendicular bisectors
    if slope_AB != 0:
        perp_slope_AB = -1 / slope_AB
    else:
        perp_slope_AB = np.inf

    if slope_BC != 0:
        perp_slope_BC = -1 / slope_BC
    else:
        perp_slope_BC = np.inf

    # Line equations (y = mx + b) for the perpendicular bisectors
    if perp_slope_AB != np.inf:
        b_AB = mid_AB[1] - perp_slope_AB * mid_AB[0]
    if perp_slope_BC != np.inf:
        b_BC = mid_BC[1] - perp_slope_BC * mid_BC[0]

    # Find the intersection of the two lines
    if perp_slope_AB == np.inf:
        circumcenter_x = mid_AB[0]
        circumcenter_y = perp_slope_BC * circumcenter_x + b_BC
    elif perp_slope_BC == np.inf:
        circumcenter_x = mid_BC[0]
        circumcenter_y = perp_slope_AB * circumcenter_x + b_AB
    else:
        circumcenter_x = (b_BC - b_AB) / (perp_slope_AB - perp_slope_BC)
        circumcenter_y = perp_slope_AB * circumcenter_x + b_AB

    return circumcenter_x, circumcenter_y
