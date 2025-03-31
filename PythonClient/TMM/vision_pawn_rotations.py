import airsim
import airsim.utils as utils
from airsim.types import Vector3r
from airsim.types import Pose
from math import radians, degrees
import random

import test_to_euler

client = airsim.VehicleClient()
client.confirmConnection()


for randomizer in [
    test_to_euler.get_random_euler_at_sigularity,
    test_to_euler.get_random_euler_near_singularity,
    test_to_euler.get_random_euler,
]:
    for _ in range(10):
        test_euler = randomizer()
        print(f"pitch :{degrees(test_euler[0])}")
        quat = utils.to_quaternion(*randomizer())
        position = Vector3r(5, 0, -10)
        client.simSetVehiclePose(Pose(position, quat), True)
        airsim.wait_key("press key to check conversion")
        pose = client.simGetVehiclePose()
        eulers = utils.to_eularian_angles(pose.orientation)
        quat = utils.to_quaternion(*eulers)
        client.simSetVehiclePose(Pose(position, quat), True)
        airsim.wait_key("press key to try next orientation")
