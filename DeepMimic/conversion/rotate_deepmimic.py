import os
import json
import numpy as np
import math
import torch

input_file_path = 'humanoid3d_punch.txt'
output_file_path = '/home/julian/Documents/Dissertation/DeepMimic/MultiDeepMimic/DeepMimic/data/motions/punch_convert.txt'


def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    
    return np.array([w,x,y,z])

def normalize(v, tolerance=0.00001):
    mag2 = sum(n * n for n in v)
    if abs(mag2 - 1.0) > tolerance:
        mag = np.sqrt(mag2)
        v = tuple(n / mag for n in v)
    return np.array(v)

def rotate_character_y(q1):
    q2 = axisangle_to_q(y_axis_unit, np.pi)
    return q_mult(q1,q2)       


def q_conjugate(q):
    w,x,y,z = q
    return np.array([w,-x,-y,-z])

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))

def axisangle_to_q(v, theta):
    v = normalize(v)
    x, y, z = v
    theta /= 2
    w = np.cos(theta)
    x = x * np.sin(theta)
    y = y * np.sin(theta)
    z = z * np.sin(theta)
    return w, x, y, z

def q_to_axisangle(q):
    w, v = q[0], q[1:]
    theta = np.acos(w) * 2.0
    return np.normalize(v), theta

x_axis_unit = (1, 0, 0)
y_axis_unit = (0, 1, 0)
z_axis_unit = (0, 0, 1)


def rotate_motion_file(motion_file):
    print(motion_file.shape)
    frames = len(motion_file)
    converted = np.empty([frames, 44])
    for i in range(0,frames):
        convert = np.empty([44])
        convert[0] = motion_file[i, 0]
        convert[1] = -motion_file[i,1]
        convert[2] = motion_file[i,2]
        convert[3] = -motion_file[i,3]


        convert[4:8] = rotate_character_y(motion_file[i,4:8])
        convert[8:12] = motion_file[i,8:12]
        convert[12:16] = motion_file[i, 12:16]
        convert[16:20] = motion_file[i, 16:20]
        convert[20] = motion_file[i, 20]
        convert[21:25] = motion_file[i, 21:25]
        convert[25:29] = motion_file[i, 25:29]
        convert[29] = motion_file[i, 29]
        convert[30:34] = motion_file[i, 30:34]
        convert[34] = motion_file[i, 34]
        convert[35:39] = motion_file[i, 35:39]
        convert[39:43] = motion_file[i, 39:43]
        convert[43] = motion_file[i, 43]
        converted[i,:] = convert[:]
    print(converted.shape)
    return converted

def main(input, output):
    with open(input, 'r') as f:
        content = json.load(f)
    motion = np.array(content["Frames"])
    converted = rotate_motion_file(motion)
    content["Frames"] = converted.tolist()
    with open(output, 'w') as file:
        json.dump(content, file)

main(input_file_path, output_file_path)