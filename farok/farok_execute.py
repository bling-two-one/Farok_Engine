import farok_engine
import farok_gearworkgolem
import time
import pygame
from random import *

def wait():
    time.sleep(1.5)

print(  "FAROK ENGINE 1.0\n"
        "제작자: 노란하스터\n"
        "2023년 5월 30일 업데이트됨\n"
        "  ______      _____   ____  _  __       ______ _   _  _____ _____ _   _ ______ \n"
        " |  ____/\   |  __ \ / __ \| |/ /      |  ____| \ | |/ ____|_   _| \ | |  ____|\n"
        " | |__ /  \  | |__) | |  | | ' /       | |__  |  \| | |  __  | | |  \| | |__  \n"
        " |  __/ /\ \ |  _  /| |  | |  <        |  __| | . ` | | |_ | | | | . ` |  __|  \n"
        " | | / ____ \| | \ \| |__| | . \       | |____| |\  | |__| |_| |_| |\  | |____ \n"
        " |_|/_/    \_\_|  \_\\____/|_|\_\       |______|_| \_|\_____|_____|_| \_|______|\n")
while True:

    tut_input = input("환영합니다. 명령어 정보를 보고 싶다면 help를, 보스 전투를 시작하려면 bossfight를 입력해 주십시오.\n"
                      "campaign을 입력해 캠페인을 시작할 수 있습니다.\n"
                      "프로그램을 종료하려면 exit을 입력해 주십시오.\n")

    if tut_input == "help":
        while True:
            help_input = input("파록엔진을 사용해 주셔서 감사합니다!\n"
                               "파록엔진은 턴제 게임을 제작하고 플레이해 볼수 있는 엔진이며 (기능은 빈약하긴 하지만) 직접 여러가지 설정을 바꿀수 있습니다.\n"
                               "기본적으로 다키스트 던전, 다키스트 던전 2의 코드를 기반으로 하며, 여러 다른 게임의 메커니즘을 가져왔습니다. \n"
                               "다키스트 던전 시스템을 기반으로 하는 만큼 몇개의 변경점을 제외하면 많은 점이 유사하며, 따라서 다키스트 던전 모더들이 쉽게 엔진을 사용할 수 있습니다. \n"
                               "또한, 엔진 자체에 새로운 상태이상을 추가하거나 몬스터 행동방식에 큰 변화를 주는 등, 자유도가 높은 편입니다.\n"
                               "그래픽이 출력되지 않는 것은 아쉬운 사실이나, 추후 업데이트를 통해 개선할 수 있을지도 모릅니다.\n"
                               "아래는 상태이상 일람입니다.\n"
                               "(팁: 치명타, 받는 피해 증가를 제외한 대부분의 계산은 합연산입니다.)\n"
                               "\n"
                               "죽음의 문턱: 영웅 체력이 0이 되면 죽음의 문턱에 서게 됩니다. 죽음의 문턱 저항력에 따라 다음 공격으로 사망할 수 있습니다. (구현 예정)\n"
                               "기절: 이번 턴을 넘기게 됩니다.\n"
                               "위력 증가: 자신이 주는 피해가 증가합니다.\n"
                               "받는 피해 증가: 자신이 받는 피해가 증가합니다.\n"
                               "속박: 자신의 속도가 감소합니다.\n"
                               "취약: 받는 피해가 15% 증가합니다.\n"
                               "무력: 가하는 피해가 15% 감소합니다. (무력은 무시하더라도 제거되지 않습니다)\n"
                               "치명타: 다음 공격이 치명타로 적중합니다. 치명타는 저항치를 20% 무시하며, 150% 피해를 줍니다.\n"
                               "저항: 부정적 상태이상을 n회 무시합니다.\n"
                               "보호: 보호대상이 받을 공격을 대신 받습니다.\n"
                               "도발: 도발 토큰을 가진 대상이 무조건 다음 공격을 받습니다. 광역 공격시 도발을 무시합니다.\n"
                               "침잠: 피격시마다 정신 피해를 침잠 수만큼 받습니다.\n"
                               "방어: 다음 공격 피해를 50% 덜 받습니다.\n"
                               "방어+: 방어 토큰보다 먼저 소모됩니다. 다음 공격 피해를 75% 덜 받습니다.\n"
                               "회피: 다음 공격을 50% 확률로 회피합니다.\n"
                               "회피+: 회피 토큰보다 먼저 소모됩니다. 다음 공격을 75% 확률로 회피합니다.\n"
                               "힘: 다음 공격의 피해가 25% 증가합니다.\n"
                               "실명: 다음 공격이 25% 확률로 적중하지 못합니다. (실명은 무시하더라도 제거되지 않습니다)\n"
                               "공포: 턴당 공포 수치만큼의 정신력이 소모됩니다. 수치가 턴마다 줄어듭니다.\n"
                               "중독: 턴당 중독 수치만큼의 피해를 받습니다. 타 상태이상과 달리 중독량이 점차 줄어들지 않습니다. 이미 중독된 대상을 다시 중독시킬순 없습니다. (저항 토큰은 소모시킬수 있습니다.)\n"
                               "화상: 턴당 화상 수치만큼의 피해를 받습니다. 화상이 있는 동안 받는 피해가 15% 증가합니다.\n"
                               "출혈: 턴당 출혈 수치만큼의 피해를 받습니다. 출혈이 있는 동안 주는 피해가 10% 감소합니다.\n"
                               "부식: 턴당 부식 수치만큼의 피해를 받습니다. 부식은 최대 체력도 감소시킵니다.\n"
                               "공명: 공명이 쌓인 상태로 공명타 관련 스킬에 적중당할 시, 공명 만큼의 피해를 입습니다.(구현 예정)\n"
                               "폭발: 폭발이 쌓인 상태로 기폭 관련 스킬에 적중당할 시, 폭발 만큼의 피해를 아군에게 입힙니다.(구현 예정)\n"
                               "피로: 피로가 쌓인 상태로 정신붕괴 관련 스킬에 적중당할 시, 피로 만큼의 정신력을 잃습니다.(구현 예정)\n"
                               "돌파: 적중시 대상 방어/방어+ 토큰 1개를 무시하며 제거합니다. (기술 패러미터에 iB = True 설정 필요)\n"
                               "추적: 적중시 대상 회피/회피+ 토큰 1개를 무시하며 제거합니다. (기술 패러미터에 iD = True 설정 필요)\n"
                               "\n"
                               "영웅 스탯:\n"
                               "정신력: 최대 100까지 올라가며, 최소 -100까지 내려갈 수 있습니다. 정신력이 0일 때 붕괴 혹은 각성이 일어나며, -100일 때 심장마비가 일어나 체력이 즉시 1이 됩니다.\n"
                               "에너지: 최대 50, 최소 0까지 보유 가능합니다. 턴마다 5씩 충전됩니다. 몇몇 스킬을 사용하는데 일정 수치가 요구됩니다. (적들은 에너지 수치에 구애받지 않습니다.)\n"
                               "\n"
                               "(exit 입력으로 나가기)\n")
            if help_input == "exit":
                break

    if tut_input == "bossfight":
        while True:
            help_input = input("원하시는 몬스터 코드를 입력해 주세요. \n"
                               "코드 리스트:\n"
                               "1. 태엽장치 골렘 (보스) = gearworkgolem\n"
                               "\n"
                               "(exit 입력으로 나가기)\n")
            if help_input == "exit":
                break
            if help_input == "gearworkgolem":
                print("준비중\n")
                wait()
    if tut_input == "campaign":
        while True:
            help_input = input("시작하고 싶은 캠페인을 선택해 주세요.\n"
                               "리스트:\n"
                               "1. 앤시언트 던전 (기본 시나리오) = ancient\n"
                               "(exit 입력으로 나가기)\n")
    if tut_input == "exit":
        print("FAROK 엔진을 이용해 주셔서 감사합니다!")
        break

#전투 알고리즘 (개발중)
"""
tlist랑 plist 정의해줘야 함

if tut_input == "start":
    if help_input == "gearworkgolem":
        #각각 플레이어, 몹 종류와 위치 지정. 플레이어나 몹이 없을 경우 None으로 둘 것. 
        #클래스 변경시 괄호 안의 p1,p2,p3 등의 값은 그대로 두고, 앞의 클래스(양식: 모듈.클래스)와 이름 값만 변경할 것
        p1 = farok_engine.Player("player1", p2, p3, p4) #추가적 플레이어 캐릭터 설정시 해당 클래스 가져오기
        p2 = farok_engine.Player("player2", p1, p3, p4)
        p3 = farok_engine.Player("player3", p1, p2, p4)
        p4 = farok_engine.Player("player4", p1, p2, p3)
        monster1 = farok_gearworkgolem.Gearwork_golem(monster2, monster3, monster4) #몬스터 모듈 추가시 해당 모듈에서 클래스 가져오기
        monster2 = farok_gearworkgolem.Holy_grave(monster1,monster3,monster4)
        monster3 = None
        monster4 - None
        p1.in_rank = 1
        p2.in_rank = 2
        p3.in_rank = 3
        p4.in_rank = 4
        #몬스터 위치값은 미리 입력해 놓아야 함
        print(monster1.intro)
        targetleft = 0
        playerleft = 0
        if p1 != None:
            playerleft +=1
        if p2 != None:
            playerleft +=1
        if p3 != None:
            playerleft +=1
        if p4 != None:
            playerleft +=1
        if m1 != None:
            targetleft +=1
        if m2 != None:
            targetleft +=1
        if m3 != None:
            targetleft +=1
        if m4 != None:
            targetleft +=1        
        wait()
        
        #루프
        while True:
            self.speedcalc()
            for i in range(1,9):
                if p1.turn_value == i:
                    대충행동프로그램
                    if targetleft == 0:
                        end_game()
                        print("전투 승리!")
                    if playerleft == 0:
                        end_game("전투 패배!")
                if p2.turn_value == i:
                    대충행동프로그램
                    if targetleft == 0:
                        end_game()
                        print("전투 승리!")
                    if playerleft == 0:
                        end_game("전투 패배!")
                if p3.turn_value == i:
                    대충행동프로그램
                    if targetleft == 0:
                        end_game()
                        print("전투 승리!")
                    if playerleft == 0:
                        end_game("전투 패배!")
                if p4.turn_value == i:
                    대충행동프로그램
                    if targetleft == 0:
                        end_game()
                        print("전투 승리!")
                    if playerleft == 0:
                        end_game("전투 패배!")
                if m1.turn_value == i:
                    m1.monsterbrain(self,p1,p2,p3,p4,m2)
                    if targetleft == 0:
                        end_game()
                        print("전투 승리!")
                    if playerleft == 0:
                        end_game("전투 패배!")
                if m2.turn_value == i:
                    대충행동프로그램
                    if targetleft == 0:
                        end_game()
                        print("전투 승리!")
                    if playerleft == 0:
                        end_game("전투 패배!")
                if m3.turn_value == i:
                    대충행동프로그램
                    if targetleft == 0:
                        end_game()
                        print("전투 승리!")
                    if playerleft == 0:
                        end_game("전투 패배!")
                if m4.turn_value == i:
                    대충행동프로그램
                    if targetleft == 0:
                        end_game()
                        print("전투 승리!")
                    if playerleft == 0:
                        end_game("전투 패배!")
        
        턴 끝나서 행동권 0일 때까지 루프돌기
"""

#속도 알고리즘

#최종 속도값(속박 약화 포함)/4 확률

def speedcalc(p1, p2, p3, p4, m1, m2, m3, m4):
    playerone = p1.speed + randint(1, 4)
    playertwo = p2.speed + randint(1, 4)
    playerthr = p3.speed + randint(1, 4)
    playerfou = p4.speed + randint(1, 4)
    mobone = m1.speed + randint(1, 4)
    mobtwo = m2.speed + randint(1, 4)
    mobthr = m3.speed + randint(1, 4)
    mobfou = m4.speed + randint(1, 4)

    sorted_l = sorted(zip([playerone, playertwo, playerthr, playerfou, mobone, mobtwo, mobthr, mobfou],
                             [p1.myID, p2.myID, p3.myID, p4.myID, m1.myID, m2.myID, m3.myID, m4.myID]))
    sorted_variable_names = [name for _, name in sorted_l]
    print(sorted_variable_names)
    for j in range(0, 8):
        if p1.myID == sorted_variable_names[j]:
            p1.turn_value = j+1
        if p2.myID == sorted_variable_names[j]:
            p2.turn_value = j+1
        if p3.myID == sorted_variable_names[j]:
            p3.turn_value = j+1
        if p4.myID == sorted_variable_names[j]:
            p4.turn_value = j+1
        if m1.myID == sorted_variable_names[j]:
            m1.turn_value = j+1
        if m2.myID == sorted_variable_names[j]:
            m2.turn_value = j+1
        if m3.myID == sorted_variable_names[j]:
            m3.turn_value = j+1
        if m4.myID == sorted_variable_names[j]:
            m4.turn_value = j+1