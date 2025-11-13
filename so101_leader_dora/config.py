from dataclasses import dataclass, field
from typing import Dict

from lerobot.teleoperators.config import TeleoperatorConfig
from lerobot.cameras import CameraConfig
from lerobot.cameras.configs import ColorMode
from lerobot.cameras.opencv import OpenCVCameraConfig


class ArmConfig():
    def __init__(self):
        self.port = None
        self.motors = None


@TeleoperatorConfig.register_subclass("so101_leader_dora")
@dataclass
class SO101LeaderDoraTeleoperatorConfig(TeleoperatorConfig):
    leader_arms: Dict[str, Dict] = field(
        default_factory=lambda: {
            "main": ArmConfig(
                port="/dev/ttyACM0",
                motors={
                    "joint_shoulder_pan": [1, "sts3215"],
                    "joint_shoulder_lift": [2, "sts3215"],
                    "joint_elbow_flex": [3, "sts3215"],
                    "joint_wrist_flex": [4, "sts3215"],
                    "joint_wrist_roll": [5, "sts3215"],
                    "joint_gripper": [6, "sts3215"],
                },
            ),
        }
    )
