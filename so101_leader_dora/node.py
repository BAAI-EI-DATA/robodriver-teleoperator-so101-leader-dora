import logging_mp
import threading
import cv2
import json
import pyarrow as pa
from dora import Node
from typing import Any, Dict


logger = logging_mp.get_logger(__name__)
CONNECT_TIMEOUT_FRAME = 10


class TeleoperatorNode:
    pass

class DoraTeleoperatorNode(TeleoperatorNode):
    pass

class SO101LeaderDoraTeleoperatorNode(DoraTeleoperatorNode):
    def __init__(self):
        self.node = Node("so101_leader_dora")
        
        self.recv_joint: Dict[str, Any] = {}
        self.recv_joint_status: Dict[str, int] = {}
        self.lock = threading.Lock()

        self.thread = threading.Thread(target=self.dora_recv, daemon=True, args=(1,))
        self.running = False

    def dora_recv(self, timeout: float):
        while self.running:
            event = self.node.next(timeout)
            if event["type"] == "INPUT":
                event_id = event["id"]
                data = event["value"].to_numpy()
                # meta_data = json.dumps(event["metadata"])

                if 'joint' in event_id:
                    if data is not None:
                        with self.lock:
                            self.recv_joint[event_id] = data
                            self.recv_joint_status[event_id] = CONNECT_TIMEOUT_FRAME

            elif event["type"] == "STOP":
                break
        
        logger.warning("Dora Node is stopped.")

    def dora_send(self, event_id, data):
        logger.debug(f"zmq send event_id:{event_id}, value:{data}")
        self.node.send_output(event_id, pa.array(data, type=pa.float32()))

    def start(self):
        """Start Dora node thread"""
        if self.running:
            logger.warning("Node is already running.")
            return

        self.running = True
        self.thread.start()

        logger.info("Teleoperator Dora node started. Waiting for sensor data...")
