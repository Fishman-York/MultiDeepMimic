import os
import json
import numpy as np
import torch

#doesn't work, use rotate_deepmimic to rotate deepmimic mocap data around
#variables

input_file_path = 'Hug 3.json'
output_file_path = '/home/julian/Documents/Dissertation/DeepMimic/MultiDeepMimic/data/motions/hug_3_convert.txt'
fps = 50
char = 0
loop = "wrap"

def data_load(content):
    transl= np.array(content.get("transl"))
    global_orient = np.array(content.get("global_orient"))
    body_pose = np.array(content.get("body_pose"))
    return transl, global_orient, body_pose

def root_conversion(root_coordinates):
    t_root = np.empty([len(root_coordinates),3])
    t_root[:,0] = root_coordinates[:,0] #0
    t_root[:,1] = root_coordinates[:,2] #2
    t_root[:,2] = root_coordinates[:,1] #1
    root = torch.from_numpy(t_root)
    return root

def global_orientation_conversion(root_orientation):
    frames = len(root_orientation)
    t_root_rotation = np.empty([frames,3,3])
    for i in range(0, frames):
        #t_root_rotation[i] = rotate_y(root_orientation[i,0], -90)
        t_root_rotation[i] = convert_coordinate_system(root_orientation[i,0], "xzy", "xyz")
        t_root_rotation[i] = rotate_x(t_root_rotation[i],180)
    root_rotation = torch.from_numpy(t_root_rotation)
    #t_root_rotation[:] = root_rotation[:,0]
    print(root_rotation.shape)
    root_quat = torch.matrix_to_quaternion(root_rotation)
    
    return root_quat

def pose_conversion(body_rotations):
    frames = len(body_rotations)
    left_shoulder_rotation = np.empty([frames, 3, 3])
    right_shoulder_rotation = np.empty([frames, 3, 3])
    z_to_y = np.empty([frames,21,3,3])

    #left shoulder rotation
    for i in range(0, frames):
        #left_shoulder_rotation[i] = rotate_x(body_rotations[i,15], 90)
        #right_shoulder_rotation[i] = rotate_x(body_rotations[i,16], -90)

        for j in range(0, 21):
            z_to_y[i,j] = convert_coordinate_system(body_rotations[i,j],"xyz","xyz")
        z_to_y[i,15] = rotate_y(rotate_x(z_to_y[i,15], 0),90) #left
        z_to_y[i,16] = rotate_x(z_to_y[i,16],-90) #right
        
        

    pose = torch.from_numpy(z_to_y)
    
    
    pose_axis = torch.matrix_to_axis_angle(pose)
    revolute_joint_id = [4, 18, 3, 17]
    revolute_rotation = revolute_axis_calculations(pose_axis, revolute_joint_id)
    
    quat = torch.matrix_to_quaternion(pose)
    return quat, revolute_rotation

#check which rotation we want for 1d (5,19,4,18)
def revolute_axis_check(joint_rotation):
    diff = torch.abs(joint_rotation[1:]-joint_rotation[:-1]).sum(dim=0)
    revolute_axis = diff.argmax()
    return revolute_axis

def revolute_axis_calculations(joint_rotations, revolute_joint_id): #list of revolute joints
    specific_joint = torch.empty([len(joint_rotations), 3])
    revolute_pose_rotation = np.empty([len(joint_rotations),4])
    for i in range(0,len(revolute_joint_id)):
        specific_joint[:] = joint_rotations[:,revolute_joint_id[i]]
        axis = revolute_axis_check(specific_joint)
        print(i, axis)
        revolute_pose_rotation[:,i] = -specific_joint[:,axis]
    return revolute_pose_rotation

def convert_coordinate_system(matrix, from_system, to_system):
    # Create conversion matrix
    conv = np.eye(3)
    for i, (f, t) in enumerate(zip(from_system, to_system)):
        conv[i, "xyz".index(f.lower())] = 1 if f == t else -1
    
    # Apply conversion
    return np.dot(conv, np.dot(matrix, conv.T))

# Example usage:
# smpl_matrix = ... # Your 3x3 SMPL rotation matrix
# converted_matrix = convert_coordinate_system(smpl_matrix, "xyz", "yxz")

def rotate_x(joint, angle):
    radian = angle_to_radians(angle)
    c = np.cos(radian)
    s = np.sin(radian)
    alignment_rotation = np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
        ])
    return np.dot(joint, alignment_rotation)

def rotate_y(joint, angle):
    radian = angle_to_radians(angle)
    c = np.cos(radian)
    s = np.sin(radian)
    alignment_rotation = np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
        ])
    return np.dot(joint, alignment_rotation)

def rotate_z(joint, angle):
    radian = angle_to_radians(angle)
    c = np.cos(radian)
    s = np.sin(radian)
    alignment_rotation = np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
        ])
    return np.dot(joint, alignment_rotation)

def angle_to_radians(angle):
    return angle * (np.pi/180)
    
    

#list of bones we want
#chest, neck, right hip, right knee, right ankle, right shoulder
#right elbow, left hip, left knee, left ankle, left shoulder
#left elbow

def deepmimic_conver(frame_time, root, root_rotation, joint_rotations, revolute_joints, loop_variable):
    deepmimic_dict = {}
    deepmimic_dict['Loop'] = loop_variable
    deepmimic = np.empty((len(joint_rotations),44))
    
    for frames in range(0,len(joint_rotations)):
        deepmimic_frame = np.empty(44)
        deepmimic_frame[0] = frame_time
        deepmimic_frame[1:4] = root[frames].numpy() #root pos
        deepmimic_frame[4:8] = root_rotation[frames].numpy() #root rotation
        deepmimic_frame[8:12] = joint_rotations[frames][8].numpy() #chest rotation
        deepmimic_frame[12:16] = joint_rotations[frames][11].numpy() #neck rotation
        deepmimic_frame[16:20] = joint_rotations[frames][1].numpy() #right hip rotation
        deepmimic_frame[20] = revolute_joints[frames][0] #right knee
        deepmimic_frame[21:25] = joint_rotations[frames][7].numpy() #right ankle
        deepmimic_frame[25:29] = joint_rotations[frames][16].numpy() #right shoulder
        deepmimic_frame[29] = revolute_joints[frames][1] #right elbow
        deepmimic_frame[30:34] = joint_rotations[frames][0].numpy() #left hip
        deepmimic_frame[34] = revolute_joints[frames][2] #left knee
        deepmimic_frame[35:39] = joint_rotations[frames][6].numpy() #left ankle
        deepmimic_frame[39:43] = joint_rotations[frames][15].numpy() #left shoulder
        deepmimic_frame[43] = revolute_joints[frames][3] #left elbow
        deepmimic[frames] = deepmimic_frame

    deepmimic_dict["Frames"] = deepmimic.tolist()
    return deepmimic_dict



def main(input, output, char_variable, fps_variable, loop_variable):
    with open(input, 'r') as f:
        content = json.load(f)
    transl,global_orient,body_pose = data_load(content)

    frame_time = 1/fps_variable
    root = root_conversion(transl[char_variable])
    root_rotation = global_orientation_conversion(global_orient[char_variable])
    joint_rotations, revolute_rotation = pose_conversion(body_pose[char_variable])
    deepmimic_obj = deepmimic_conver(frame_time, root, root_rotation, joint_rotations, revolute_rotation, loop_variable)
    with open(output, 'w') as file:
        json.dump(deepmimic_obj, file)

main(input_file_path, output_file_path, char, fps, loop)