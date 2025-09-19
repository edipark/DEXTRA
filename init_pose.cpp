#include "dynamixel_sdk/dynamixel_sdk.h"
#include <iostream>
#include <map>

int main()
{
    // 포트 및 통신 설정
    const char* PORT_NAME = "/dev/ttyUSB0";
    int BAUDRATE = 1000000;
    float PROTOCOL_VERSION = 1.0;

    // 모터 ID와 초기 위치 값
    std::map<int, int> INIT_POSITION = {
        {1, 512},
        {2, 512},
        {3, 480},
        {4, 410},
        {5, 582},
        {6, 512},
        {7, 512},
        {8, 512},
        {9, 544},
        {10, 614},
        {11, 442},
        {12, 512}
    };

    int ADDR_GOAL_POSITION = 30; // Goal Position 주소

    // 포트 핸들러 및 패킷 핸들러 생성
    dynamixel::PortHandler *portHandler = dynamixel::PortHandler::getPortHandler(PORT_NAME);
    dynamixel::PacketHandler *packetHandler = dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION);

    // 포트 열기
    if (!portHandler->openPort()) {
        std::cout << "포트 열기 실패" << std::endl;
        return 1;
    }

    // 보레이트 설정
    if (!portHandler->setBaudRate(BAUDRATE)) {
        std::cout << "보레이트 설정 실패" << std::endl;
        return 1;
    }

    // 각 모터에 초기 위치 명령 전송
    for (int motor_id = 1; motor_id <= 12; ++motor_id) {
        int goal_position = INIT_POSITION[motor_id];
        int dxl_comm_result = packetHandler->write2ByteTxRx(
            portHandler, motor_id, ADDR_GOAL_POSITION, goal_position
        );
        uint8_t dxl_error = packetHandler->getLastRxPacketError();

        if (dxl_comm_result != COMM_SUCCESS) {
            std::cout << "모터 " << motor_id << " 통신 오류: " << packetHandler->getTxRxResult(dxl_comm_result) << std::endl;
        } else if (dxl_error != 0) {
            std::cout << "모터 " << motor_id << " 오류: " << packetHandler->getRxPacketError(dxl_error) << std::endl;
        } else {
            std::cout << "모터 " << motor_id << " 초기화 완료: " << goal_position << std::endl;
        }
    }

    // 포트 닫기
    portHandler->closePort();
    return 0;
}