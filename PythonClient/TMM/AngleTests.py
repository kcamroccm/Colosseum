from math import degrees, radians
from airsim.types import Quaternionr
import airsim.utils as utils

#pitch roll yaws
inputs = [
    (0, 22.5, 45),
    (-90, 0, 45),
    (-90, 45, 0),
    (90, 0, 45),
    (90, 45, 0),
    (88.00, 0, 45)
    ]

for i in inputs:
    quat = utils.to_quaternion(*tuple(map(radians, i)))
    print(quat)
    rot = utils.to_eularian_angles(quat)
    in_pitch, in_roll, in_yaw = i
    pitch, roll, yaw = tuple(map(degrees, rot))
    print(f"input:  pitch = {in_pitch}, roll = {in_roll}, yaw = {in_yaw}")
    print(f"result: pitch = {pitch}, roll = {roll}, yaw = {yaw}")

