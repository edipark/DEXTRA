import dynamixel_sdk as dxl
import init_pose
import time

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


ADDR_TORQUE_ENABLE = 24
ADDR_GOAL_POSITION = 30 
ADDR_MOVING_SPEED = 32
ADDR_PRESENT_POSITION = 36  


LEN_1BYTE = 1
LEN_2BYTE = 2

portHandler = dxl.PortHandler(PORT_NAME)
packetHandler = dxl.PacketHandler(PROTOCOL_VERSION)

portHandler.openPort()
portHandler.setBaudRate(BAUDRATE)



def get_present_position(motor_id):
    pos, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
        portHandler, motor_id, ADDR_PRESENT_POSITION
    )
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print(f"모터 {motor_id} 현재 위치 읽기 오류: {packetHandler.getTxRxResult(dxl_comm_result)}")
        return 512  # 오류 시 기본값
    elif dxl_error != 0:
        print(f"모터 {motor_id} 에러: {packetHandler.getRxPacketError(dxl_error)}")
        return 512
    return pos


def close_port():
    try:
        portHandler.closePort()
    except Exception:
        pass


def enable_torque_for(motor_ids):
    ok = True
    for motor_id in motor_ids:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
            portHandler, motor_id, ADDR_TORQUE_ENABLE, 1
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            print(f"모터 {motor_id} 통신 오류: {packetHandler.getTxRxResult(dxl_comm_result)}")
            ok = False
        elif dxl_error != 0:
            print(f"모터 {motor_id} 오류: {packetHandler.getRxPacketError(dxl_error)}")
            ok = False
    return ok


def move_motors_slow(motor_ids, goal_positions, moving_speed):
    """
    선택된 모터들을 같은 타이밍에 천천히 이동.
    - motor_ids: 리스트[int]
    - goal_positions: {id: pos(0~1023)}
    - moving_speed: 1~1023 (작을수록 느림, 0은 최대속도)
    """
    # 속도 동시 설정
    group_speed = dxl.GroupSyncWrite(portHandler, packetHandler, ADDR_MOVING_SPEED, LEN_2BYTE)
    for i, motor_id in enumerate(motor_ids):
        speed = max(1, min(1023, int(moving_speed[i])))
        param_speed = [speed & 0xFF, (speed >> 8) & 0xFF]
        if not group_speed.addParam(motor_id, param_speed):
            print(f"속도 파라미터 추가 실패: ID {motor_id}")
    dxl_comm_result = group_speed.txPacket()
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print(f"속도 전송 오류: {packetHandler.getTxRxResult(dxl_comm_result)}")
    group_speed.clearParam()

    # 목표 위치 동시 설정 (전송 시 즉시 동작 시작)
    group_pos = dxl.GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_2BYTE)
    for motor_id in motor_ids:
        pos = int(goal_positions.get(motor_id, DOF_POSITION.get(motor_id, 512)))
        pos = max(0, min(1023, pos))
        param_pos = [pos & 0xFF, (pos >> 8) & 0xFF]
        if not group_pos.addParam(motor_id, param_pos):
            print(f"포지션 파라미터 추가 실패: ID {motor_id}")
    dxl_comm_result = group_pos.txPacket()
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print(f"포지션 전송 오류: {packetHandler.getTxRxResult(dxl_comm_result)}")
    group_pos.clearParam()


if __name__ == "__main__":
    target_ids = [3, 4, 5, 9, 10, 11]
    if enable_torque_for(target_ids):
        move_motors_slow(
                motor_ids=target_ids,
                goal_positions={3: 444, 4: 204, 5: 745, 9: 580, 10: 820, 11: 279},
                moving_speed=[50 * (36/233), 50 * (206/233), 50, 50 * (36/233), 50 * (206/233), 50],
            )
        time.sleep(7)  
        move_motors_slow(
                motor_ids=target_ids,
                goal_positions={3: DOF_POSITION[3], 4: DOF_POSITION[4], 5: DOF_POSITION[5], 
                                9: DOF_POSITION[9], 10: DOF_POSITION[10], 11: DOF_POSITION[11]},
                moving_speed=[50 * (36/233), 50 * (206/233), 50, 50 * (36/233), 50 * (206/233), 50],
            )
        
        
    close_port()

