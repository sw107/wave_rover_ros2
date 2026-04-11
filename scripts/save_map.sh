#!/bin/bash
# 지도 저장 스크립트
# 매핑 완료 후 실행하면 현재 디렉토리에 map.pgm, map.yaml 파일 저장
# 사용법: bash save_map.sh [저장할 파일 이름]
# 예시: bash save_map.sh my_map

MAP_NAME=${1:-map}  

echo "=== 지도 저장 시작: ${MAP_NAME} ==="
ros2 run nav2_map_server map_saver_cli -f ${MAP_NAME}
echo "=== 저장 완료: ${MAP_NAME}.pgm, ${MAP_NAME}.yaml ==="
