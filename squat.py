import dynamixel_sdk as dxl
import init_pose

# pose init
init_pose.init_pose()

PORT_NAME = '/dev/ttyUSB0' 
BAUDRATE = 1000000
PROTOCOL_VERSION = 1.0
MOTOR_IDS = list(range(1, 13))


DOF_POSITION = {
        1: 512,
        2: 512,
        3: 480,
        4: 410,
        5: 582,
        6: 512,
        7: 512,
        8: 512,
        9: 544,
        10: 614,
        11: 442,
        12: 512,
    } 
# 초기 위치로 초기화


ADDR_GOAL_POSITION = 30 

portHandler = dxl.PortHandler(PORT_NAME)
packetHandler = dxl.PacketHandler(PROTOCOL_VERSION)

