import pytest
from math import degrees, radians
import sys
import random
import math

sys.path.append(".")
sys.path.append("..")
import airsim
from airsim.types import Quaternionr
import airsim.utils as utils


def compare_quats(quat1: Quaternionr, quat2: Quaternionr):
    tolerance = 1e-3
    same = (
        abs(quat1.x_val - quat2.x_val) < tolerance
        and abs(quat1.y_val - quat2.y_val) < tolerance
        and abs(quat1.z_val - quat2.z_val) < tolerance
        and abs(quat1.w_val - quat2.w_val) < tolerance
    )
    if same:
        return same

    inverse = (
        abs(quat1.x_val + quat2.x_val) < tolerance
        and abs(quat1.y_val + quat2.y_val) < tolerance
        and abs(quat1.z_val + quat2.z_val) < tolerance
        and abs(quat1.w_val + quat2.w_val) < tolerance
    )
    if not inverse:
        print(f"q1: x:{quat1.x_val}, y:{quat1.y_val}, z:{quat1.z_val}, w:{quat1.w_val} :: \nq2: x:{quat2.x_val}, y:{quat2.y_val}, z:{quat2.z_val}, w:{quat2.w_val}")
    return inverse


def compare_eulers(eulers1, eulers2):
    quat1 = utils.to_quaternion(*eulers1)
    quat2 = utils.to_quaternion(*eulers2)
    return compare_quats(quat1, quat2)

def get_random_euler():
    return (
        random.uniform(-math.pi / 2, math.pi / 2),
        random.uniform(-2 * math.pi, 2 * math.pi),
        random.uniform(-2 * math.pi, 2 * math.pi)
    )

def get_random_euler_at_sigularity():
    pitch = random.choice([-1, 1]) * (math.pi / 2)
    return (
        pitch,
        math.pi * 2 * random.random(),
        math.pi * 2 * random.random(),
    )

def get_random_euler_near_singularity():
    pitch = random.uniform(-0.002, 0.002) + random.choice([-1, 1]) * (math.pi / 2)
    return (
        pitch,
        math.pi * 2 * random.random(),
        math.pi * 2 * random.random(),
    )

def test_range_near_90():
    for i in range(101):
        pitch = -90 + i * 0.01
        print(f"pitch: {pitch}, {radians(pitch)}")
        test_euler  = tuple(map(radians, (pitch, 110,0)))
        quat = utils.to_quaternion(*test_euler)
        euler = utils.to_eularian_angles(quat) 
        assert compare_eulers(test_euler, euler)
        

def test_to_euler():

    for i in range(100):
        test_euler = get_random_euler_at_sigularity()
        quat = utils.to_quaternion(*test_euler)
        euler = utils.to_eularian_angles(quat)
        assert compare_eulers(test_euler, euler)

    for i in range(100):
        test_euler = get_random_euler_near_singularity()
        quat = utils.to_quaternion(*test_euler)
        euler = utils.to_eularian_angles(quat)
        assert compare_eulers(test_euler, euler)

    for i in range(100):
        test_euler = get_random_euler()
        quat = utils.to_quaternion(*test_euler)
        euler = utils.to_eularian_angles(quat)
        assert compare_eulers(test_euler, euler)
