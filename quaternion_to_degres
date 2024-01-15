import numpy as np

def quaternion_to_euler(quat):
    quat= quat/ np.linalg.norm(quat) # Normaliser le quaternion
    a=quat[0]
    b=quat[1]
    c=quat[2]
    d=quat[3]
    yaw = np.arctan2(2 * (a*d + b*c), 1 - 2 * (c**2 + d**2)) #mouvement lacet
    yaw_deg = np.degrees(yaw)
    return yaw_deg

angle_drone= quaternion_to_euler(quat)
