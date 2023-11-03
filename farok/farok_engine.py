import pygame
from random import *
from math import *

"""
기본 클래스 설정
"""

"""
기본 열 계산: 
게임에서 기본적으로 계산되는 위치:
[4 3 2 1 vs 5 6 7 8]

4,3,2,1 = 플레이어 열
5,6,7,8 = 몹 열

몹 판정: 
    56 = 2열 차지 몬스터 (1,2열)
    67 = 2열 차지 몬스터 (2,3열)
    78 = 2열 차지 몬스터 (3,4열)
    567 = 3열 차지 몬스터 (1,2,3열)
    678 = 3열 차지 몬스터 (2,3,4열)
    5678 = 4열 전체 (1,2,3,4열)
"""


#존재 가능한 타입 종류: (주의: 타입은 두개까지만 설정할수 있음)

#공용
holy = "종교적"
unholy = "이교도"
tech = "기술"
magic = "마법"
human = "인간형"
undead = "언데드"
beast = "동물형"
eldritch = "이물"

#몹 전용
stonework = "석재"
ironwork = "철제"
woodwork = "목재"
lovecraft = "형언할 수 없음"


class Entity:
    myID = None #프로그램 내에서 호출시 코드
    maxhp = None #최대체력
    hp = None #체력 설정
    defaultinit = None #기본 행동권 (고유)
    initiative = None #현재 보유 행동권 (int)
    defaultdmgrec = None #기본 방어도 (받뎀감) (음수 float)
    defaultdodge = None #기본 회피
    type1 = None #속성 (str)
    type2 = None
    bleedres = None #출혈저항 (int 퍼센트)
    blightres = None #중독저항
    corrosionres = None #부식저항
    burnres = None #화상저항
    stunres = None #기절저항
    globalres = None #약화저항 (무력, 취약 등)
    sanityres = None #정신저항 (침잠, 공포 등)
    moveres = None #이동저항
    status = None #변신 기믹 활용시 필요 (str)
    has_bleed = None #현재 가진 상태이상 수치 체크 (int)
    has_blight = None
    dmg_blight = None #중독량
    has_corrosion = None
    has_burn = None
    has_vuln = None
    has_weak = None
    has_capture = None
    has_res = None
    has_crit = None
    has_horror = None
    has_sinking = None
    has_restoration = None #재생
    has_blind = None
    has_stun = None
    has_guard = None
    has_taunt = None #도발
    has_prot = None
    has_protplus = None
    has_dodge = None
    has_dodgeplus = None
    has_power = None #힘 토큰 (위력증가와 다름)
    has_resonance = None
    has_explode = None
    has_fatigue = None
    strength = None #현재 가진 위력 증가량 (int)
    speed = None  # 속도값
    in_rank = None  # 현재 열 (위치)
    turn_value = None #None으로 놔둘 것. 계산에 필요
    guarded_by = None  # XXX에 의해 보호됨
    immunity = None #면역정보
    durations = None #각종 약화 지속시간. 리스트: 0 = 중독, 다른거 약화

class Player(Entity): #디폴트 플레이어 설정
    lvl = None #레벨
    sanity = None #정신력 설정 (int)
    energy = None #에너지 충전
    defenergy = None #에너지 기본값 (기본 50)
    currentpath = None #영웅의 길
    path_list = None #영길 3개 ID 리스트 내에 저장
    selected_skills = None #선택된 스킬들 list, 최대 6
    equippeditemname = None #전투아이템
    trinket1 = None #trinketdict 문서 만들어서 호출할 예정
    trinket1applied = None #bool타입, 적용되었는지 확인
    trinket2 = None
    trinket2applied = None
    avail_skills = None #사용가능 스킬 list타입
    skilllist = None #list 타입 12개 스킬 ID 목록
    minmove = None
    maxmove = None
    codedictionary = None #dict타입으로 스킬이름

    def __init__(self,ally1, ally2, ally3):
        self.ally1 = ally1
        self.ally2 = ally2
        self.ally3 = ally3


class Enemy(Entity): #디폴트 적 설정. 수치값은 플레이어 참조바람
    intro = None #적 조우시 출력하는 텍스트
    originfo = None #처음 표시되는 기본 텍스트
    info = None #이후 기술로 인해 추가된 텍스트를 포함해서 전체 정보를 보여주는 변수

    def __init__(self, ally1, ally2, ally3):
        self.ally1 = ally1
        self.ally2 = ally2
        self.ally3 = ally3

    def info_update(self, value):
        print("")
    #순차적으로 공개되는 적 정보를 작성할때 사용. 코드는 태엽장치 골렘 참고

    def monsterbrain(self,targetlist):
        print("")
    #행동 AI. 만약 아군 상호작용이 있다면 target4 후에 기입해주면 됨

#공용 도트 이펙트
def eff_burn(self):
    if self.has_burn !=0:
        print(f"화상으로 {self.has_burn} 피해 입음")
        self.hp -= self.has_burn
        self.has_burn -= 1
    if self.has_burn == 0:
        self.defaultdmgrec -= 0.15

def eff_bleed(self):
    if self.has_bleed !=0:
        print(f"출혈으로 {self.has_bleed} 피해 입음")
        self.hp -= self.has_bleed
        self.has_bleed -= 1

def eff_blight(self):
    if self.has_blight !=0:
        print(f"중독으로 {self.dmg_blight} 피해 입음")
        self.hp -= self.dmg_blight
        self.has_blight -= 1
    if self.has_blight == 0:
        self.dmg_blight = 0

def eff_corrosion(self):
    if self.has_corrosion !=0:
        print(f"부식으로 {self.has_corrosion} 피해 입음")
        self.hp -= self.has_corrosion
        self.maxhp -= self.has_corrosion
        self.has_corrosion -= 1

def eff_horror(self):
    if self.has_horror !=0:
        print(f"공포로 {self.has_horror} 정신 피해 입음")
        self.sanity -= self.has_horror
        self.has_horror -= 1

def eff_restoration(self):
    if self.has_restoration !=0:
        print(f"재생으로 {self.has_restoration} 회복됨")
        self.hp += self.has_restoration
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        self.has_restoration -= 1


def eff_guard(self):
    if self.has_guard != 0:
        print(f"{self.guarded_by}에게 {self.has_guard}동안 보호받음")
        self.has_guard -= 1
        print(f"남은 보호: {self.has_guard}")
    if self.has_guard == 0:
        print(f"{self.guarded_by}에게 받는 보호 해제됨.")
        self.guarded_by = "None"


def eff_energyfill(self):
    if hasattr(self,'sanity'): #정신력 유무로 몹/플레이어 판단
        self.energy +=5
        if self.energy > self.defenergy:
            self.energy = self.defenergy


def stuncheck(self):
    if self.has_stun !=0:
        self.initiative = 0
        print("기절 해제됨.")
        self.has_stun -= 1


#효과 적용
def apply_bleed(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1,100)
        if ch >= (100-(chance-target.bleedres)):
            target.has_bleed += amount
            print(f"대상 출혈을 {amount}만큼 변경.\n"
                  f"현재 출혈량 = {target.has_bleed}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_blight(self, chance, amount, dmg, target):
    if target.has_res == 0:
        if target.has_blight == 0:
            ch = randint(1, 100)
            if ch >= (100 - (chance - target.blightres)):
                target.has_blight += amount
                target.dmg_blight += dmg
                print(f"대상 중독을 {amount}만큼 변경.\n"
                      f"현재 중독량 = {target.dmg_blight}\n")
        else:
            print("대상이 이미 중독에 걸려 있어 중독 추가 불가능.")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_corrosion(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.corrosionres)):
            target.has_corrosion += amount
            print(f"대상 부식을 {amount}만큼 변경.\n"
                  f"현재 부식량 = {target.has_corrosion}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_burn(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.burnres)):
            target.defaultdmgrec += 0.15
            target.has_burn += amount
            print(f"대상 화상을 {amount}만큼 변경.\n"
                  f"현재 화상량 = {target.has_burn}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_vuln(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.globalres)):
            target.has_vuln += amount
            print(f"대상 취약을 {amount}만큼 변경.\n"
                  f"현재 취약량 = {target.has_vuln}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1
def apply_weak(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.globalres)):
            target.has_weak += amount
            print(f"대상 무력을 {amount}만큼 변경.\n"
                  f"현재 무력량 = {target.has_weak}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1
def apply_capture(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.globalres)):
            target.has_capture += amount
            print(f"대상 속박을 {amount}만큼 변경.\n"
                  f"현재 속박량 = {target.has_capture}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_stun(self, chance, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.stunres)):
            target.has_stun = 1
            print("기절!")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_crit(self, chance, amount, target):
    ch = randint(1,100)
    if ch >= (100-chance):
        target.has_crit += amount
        print(f"대상 치명타 토큰을 {amount}만큼 변경.\n"
              f"현재 치명타 토큰 = {target.has_crit}\n")

def apply_sinking(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.sanityres)):
            target.has_sinking += amount
            print(f"대상 침잠을 {amount}만큼 변경.\n"
                  f"현재 침잠량 = {target.has_sinking}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_horror(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.sanityres)):
            target.has_horror += amount
            print(f"대상 공포를 {amount}만큼 변경.\n"
                  f"현재 공포량 = {target.has_horror}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_restoration(self, chance, amount, target):
        ch = randint(1, 100)
        if ch >= (100 - chance):
            target.has_restoration += amount
            print(f"대상 재생을 {amount}만큼 변경.\n"
                  f"현재 재생량 = {target.has_restoration}\n")

def apply_guard(self, amount, target):
    target.guarded_by = self.myID
    target.has_guard += amount
    print(f"대상을 {amount}라운드간 보호.")

def apply_res(self, chance, amount, target):
    ch = randint(1,100)
    if ch >= (100-chance):
        target.has_res += amount
        print(f"대상 저항 토큰을 {amount}만큼 변경.\n"
              f"현재 저항 토큰 = {target.has_res}\n")

def apply_prot(self, chance, amount, target):
    ch = randint(1,100)
    if ch >= (100-chance):
        target.has_prot += amount
        print(f"대상 방어 토큰을 {amount}만큼 변경.\n"
              f"현재 방어 토큰 = {target.has_prot}\n")

def apply_protplus(self, chance, amount, target):
    ch = randint(1,100)
    if ch >= (100-chance):
        target.has_protplus += amount
        print(f"대상 방어+ 토큰을 {amount}만큼 변경.\n"
              f"현재 방어+ 토큰 = {target.has_protplus}\n")

def apply_dodge(self, chance, amount, target):
    ch = randint(1,100)
    if ch >= (100-chance):
        target.has_dodge += amount
        print(f"대상 회피 토큰을 {amount}만큼 변경.\n"
              f"현재 회피 토큰 = {target.has_dodge}\n")

def apply_dodgeplus(self, chance, amount, target):
    ch = randint(1,100)
    if ch >= (100-chance):
        target.has_dodgeplus += amount
        print(f"대상 회피+ 토큰을 {amount}만큼 변경.\n"
              f"현재 회피+ 토큰 = {target.has_dodgeplus}\n")

def apply_power(self, chance, amount, target):
    ch = randint(1,100)
    if ch >= (100-chance):
        target.has_power += amount
        print(f"대상 힘 토큰을 {amount}만큼 변경.\n"
              f"현재 힘 토큰 = {target.has_power}\n")

def apply_blind(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.globalres)):
            target.has_blind += amount
            print(f"대상 실명을 {amount}만큼 변경.\n"
                  f"현재 실명량 = {target.has_blind}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

def apply_resonance(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.globalres)):
            target.has_resonance += amount
            print(f"대상 공명을 {amount}만큼 변경.\n"
                  f"현재 공명 중첩량 = {target.has_blind}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1
def apply_explode(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.globalres)):
            target.has_explode += amount
            print(f"대상 폭발을 {amount}만큼 변경.\n"
                  f"현재 폭발 중첩량 = {target.has_blind}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1
def apply_fatigue(self, chance, amount, target):
    if target.has_res == 0:
        ch = randint(1, 100)
        if ch >= (100 - (chance - target.sanityres)):
            target.has_fatigue += amount
            print(f"대상 피로를 {amount}만큼 변경.\n"
                  f"현재 피로 중첩량 = {target.has_blind}\n")
    else:
        print(f"저항으로 인해 효과 차단됨. \n"
              f"현재 남은 저항: {target.has_res}\n")
        target.has_res -= 1

#당기기/밀기
def pull(target, other1, other2, other3, amount):
    amount = target.in_rank - amount
    if amount <= 1:
        amount = 1
    amount -= 1
    instance_list = [target, other1, other2, other3]
    sorted_list = sorted(instance_list, key=lambda x: x.in_rank)
    if target in sorted_list:
        sorted_list.remove(target)
    sorted_list.insert(amount, target)
    for i, instance in enumerate(sorted_list):
        instance.in_rank = i + 1

def push(target, other1, other2, other3, amount):
    amount = target.in_rank + amount
    if amount >= 4:
        amount = 4
    amount -= 1
    instance_list = [target, other1, other2, other3]
    sorted_list = sorted(instance_list, key=lambda x: x.in_rank)
    if target in sorted_list:
        sorted_list.remove(target)
    sorted_list.insert(amount, target)
    for i, instance in enumerate(sorted_list):
        instance.in_rank = i + 1

#회복
def heal(self, chance, amount, target):
    ch = randint(1, 100)
    if ch >= (100 - chance):
        target.hp += amount
        if target.hp > target.maxhp:
            target.hp = target.maxhp
#퍼센트힐 (값을 1 이하의 소수로 입력해줘야함 ex: 0.1, 0.3)
def healpercent(self, chance, amount, target):
    ch = randint(1, 100)
    if ch >= (100 - chance):
        target.hp += (target.maxhp * amount)
        if target.hp > target.maxhp:
            target.hp = target.maxhp

#스트레스
def stress(self,chance,amount,target):
    ch = 10+ randint(1,100) - target.sanityres
    if ch >= (100-chance):
        target.sanity -= amount
def stressheal(self,chance,amount,target):
    ch = randint(1,100)
    if ch >= (100-chance):
        target.sanity += amount
        if target.sanity > 100:
            target.sanity = 100
#행동권
def useinitiative(self):
    self.initiative -= 1
    print(f"남은 행동권: {self.initiative}")
def useinitiative2(self):
    self.initiative -= 2
    print(f"남은 행동권: {self.initiative}")
def plusinitiative(self):
    self.initiative += 1
    print(f"남은 행동권: {self.initiative}")

#공격값 알고리즘
def dmgcalc(self, target, damage, iW, iP):
    ignore_weak = iW
    ignore_prot = iP
    df_dmg = (1+target.defaultdmgrec) * (damage+self.strength)
    df_mod = 1
    if self.has_bleed !=0:
        df_mod -= 0.1
        print(f"공격자 출혈으로 인해 가하는 피해 10% 차감, 남은 출혈 {self.has_bleed}")
    if self.has_weak !=0:
        if ignore_weak == False:
            df_mod -= 0.15
            print(f"공격자 무력 토큰으로 인해 가하는 피해 15% 차감, 남은 무력 토큰 {self.has_weak}")
            self.has_weak -= 1
        if ignore_weak == True:
            print(f"공격자 무력 토큰 무시, 남은 무력 토큰 {self.has_weak}")
    if target.has_vuln !=0:
        df_mod += 0.15
        print(f"대상 취약 토큰으로 인해 가하는 피해 15% 증가, 남은 취약 토큰 {target.has_vuln}")
        target.has_vuln -= 1
    if target.has_protplus != 0:
        if ignore_prot == True:
            target.has_protplus -=1
            print(f"돌파 공격으로 인해 대상 방어+ 토큰 무시 및 차감, 남은 방어+ 토큰 {target.has_protplus}")
        if ignore_prot == False:
            df_mod -= 0.75
            target.has_protplus -= 1
            print(f"대상 방어+ 토큰으로 인해 피해 75% 차감, 남은 방어토큰 {target.has_protplus}")
    elif target.has_prot != 0:
        if ignore_prot == True:
            target.has_prot -= 1
            print(f"돌파 공격으로 인해 대상 방어 토큰 무시 및 차감, 남은 방어 토큰 {target.has_prot}")
        if ignore_prot == False:
            df_mod -= 0.5
            target.has_prot -= 1
            print(f"대상 방어 토큰으로 인해 피해 50% 차감, 남은 방어토큰 {target.has_prot}")
    if self.has_power != 0:
        df_mod += 0.25
        self.has_power -= 1
        print(f"공격자 힘 토큰으로 인해 피해 25% 증가, 남은 힘 토큰 {self.has_power}")
    if target.has_sinking !=0:
        print(f"침잠으로 {target.has_sinking} 정신 피해 입힘")
        target.sanity -= target.has_sinking
        target.has_sinking -= 1
    if df_mod < 0:
        df_mod = 0
    df_dmg *= df_mod
    if self.has_crit != 0:
        df_dmg *= 1.5
        self.has_crit -= 1
        print(f"치명타! (남은 치명타 토큰: {self.has_crit}")
    ceil(df_dmg)
    return df_dmg
#명중률 알고리즘
def attackcalc(self,target,accmod,calculated_value,iW,iP,iB,iD,skilltype):
    ignore_blind = iB
    ignore_dodge = iD
    stp = skilltype
    if stp != target.immunity:
        df_acc = 100-target.defaultdodge+accmod
        df_accmod = 1
        ishit = False
        if self.has_blind != 0:
            if ignore_blind == True:
                print(f"공격자 실명 토큰 무시, 남은 실명 토큰 {self.has_blind}")
            if ignore_blind == False:
                df_accmod -= 0.25
                print(f"공격자 실명 토큰으로 인해 명중률 25% 감소, 남은 실명 토큰 {self.has_blind}")
        if target.has_dodgeplus != 0:
            if ignore_dodge == True:
                target.has_dodgeplus -= 1
                print(f"추적 공격으로 인해 대상 회피+ 토큰 무시 및 차감, 남은 회피+ 토큰 {target.has_dodgeplus}")
            if ignore_dodge == False:
                df_accmod -= 0.75
                print(f"대상 회피+ 토큰으로 인해 명중률 75% 감소, 남은 회피+ 토큰 {target.has_dodgeplus}")
        elif target.has_dodge != 0:
            if ignore_dodge == True:
                target.has_dodge -= 1
                print(f"추적 공격으로 인해 대상 회피 토큰 무시 및 차감, 남은 회피 토큰 {target.has_dodge}")
            if ignore_dodge == False:
                df_accmod -= 0.5
                print(f"대상 회피 토큰으로 인해 명중률 50% 감소, 남은 회피 토큰 {target.has_dodge}")

        if df_accmod < 0:
            df_accmod = 0
        df_acc *= df_accmod
        ch = randint(1,100)
        if ch >= 100-df_acc:
            target.hp -= self.dmgcalc(self,target,calculated_value,iW,iP)
            ishit = True
            return ishit
        else:
            print("빗나감!")
            ishit = False
            return ishit
    else:
        if target.immunity == "magic":
            stp = "주술/마법"
        if target.immunity == "physic":
            stp = "물리"
        print(f"대상이 {stp} 공격에 면역 상태임!")
    # calculated_value값 넣을때 항상 미리 상태별 추가피해/랜덤피해 계산 필요 (예시: 1d3 + 대상 정신력만큼 피해일 시 1d3+정신력 을 미리 변수에 할당해 놓을 것)
"""
예시 공격 알고리즘:
farok_engine.attackcalc(self,대충타겟,대충명중률보너스,미리 계산해둔 값(랜덤값 계산 + 공격별 상태이상 중첩만큼 추가피해 등),무력무시,방어무시,실명무시,회피무시, 공격타입)
"""

def statusplayer(self):
    im = None
    if self.immunity == "magic":
        im = "주술/마법"
    if self.immunity == "physic":
        im = "물리"
    print(f"현재 상태: {self.status}\n"
          f"현재 체력: {self.hp}/{self.maxhp}\n"
          f"현재 정신력: {self.sanity}/50\n"
          f"\n저항력 정보\n"
          f"출혈 저항: {self.bleedres}%\n"
          f"중독 저항: {self.blightres}%\n"
          f"부식 저항: {self.corrosionres}%\n"
          f"화상 저항: {self.burnres}%\n"
          f"기절 저항: {self.stunres}%\n"
          f"약화 저항: {self.globalres}%\n"
          f"정신 저항: {self.sanityres}%\n"
          f"\n"
          f"현재 상태: {self.status}\n"
          f"받는 피해 배율: +{self.defaultdmgrec}\n"
          f"기본 회피: {self.defaultdodge}\n"
          f"위력 증가량: {self.strength}\n"
          f"속도: {self.speed}\n"
          f"현재 위치: {self.in_rank}열\n"
          f"\n"
          f"현재 가진 상태이상/토큰:\n")
    if self.has_bleed !=0:
        print(f"출혈: {self.has_bleed}\n")
    if self.has_blight != 0:
        print(f"중독: {self.has_blight}\n")
    if self.has_corrosion != 0:
        print(f"부식: {self.has_corrosion}\n")
    if self.has_burn != 0:
        print(f"화상: {self.has_burn}\n")
    if self.has_vuln != 0:
        print(f"취약: {self.has_vuln}\n")
    if self.has_weak != 0:
        print(f"무력: {self.has_weak}\n")
    if self.has_capture != 0:
        print(f"속박: {self.has_capture}\n")
    if self.has_blind != 0:
        print(f"실명: {self.has_blind}\n")
    if self.has_horror != 0:
        print(f"공포: {self.has_horror}\n")
    if self.has_sinking != 0:
        print(f"침잠: {self.has_sinking}\n")
    if self.has_crit != 0:
        print(f"치명타: {self.has_crit}\n")
    if self.has_power != 0:
        print(f"힘: {self.has_power}\n")
    if self.has_res != 0:
        print(f"저항: {self.has_res}\n")
    if self.has_guarded != 0:
        print(f"{self.guarded_by}에게 보호받음: {self.has_guard}\n")
    if self.has_prot != 0:
        print(f"방어: {self.has_prot}\n")
    if self.has_protplus != 0:
        print(f"방어+: {self.has_protplus}\n")
    if self.has_dodge != 0:
        print(f"회피: {self.has_dodge}\n")
    if self.has_dodgeplus != 0:
        print(f"회피+: {self.has_dodgeplus}\n")
    if self.has_restoration != 0:
        print(f"재생: {self.has_restoration}\n")
    if self.has_resonance != 0:
        print(f"공명 중첩: {self.has_resonance}")
    if self.has_explode != 0:
        print(f"폭발 중첩: {self.has_explode}")
    if self.has_fatigue != 0:
        print(f"피로 중첩: {self.has_fatigue}")
    if self.immunity != None:
        print(f"현재 {im} 피해에 면역 상태임")

def statusmonster(self):
    im = None
    if self.immunity == "magic":
        im = "주술/마법"
    if self.immunity == "physic":
        im = "물리"
    print(f"현재 상태: {self.status}\n"
          f"현재 체력: {self.hp}/{self.maxhp}\n"
          f"\n저항력 정보\n"
          f"출혈 저항: {self.bleedres}%\n"
          f"중독 저항: {self.blightres}%\n"
          f"부식 저항: {self.corrosionres}%\n"
          f"화상 저항: {self.burnres}%\n"
          f"기절 저항: {self.stunres}%\n"
          f"약화 저항: {self.globalres}%\n"
          f"정신 저항: {self.sanityres}%\n"
          f"\n"
          f"현재 상태: {self.status}\n"
          f"받는 피해 배율: +/- {self.defaultdmgrec}\n"
          f"기본 회피: {self.defaultdodge}\n"
          f"위력 증가량: {self.strength}\n"
          f"속도: {self.speed}\n"
          f"현재 위치: {self.in_rank}열\n"
          f"\n"
          f"현재 가진 상태이상/토큰:\n")
    if self.has_bleed !=0:
        print(f"출혈: {self.has_bleed}\n")
    if self.has_blight != 0:
        print(f"중독: {self.has_blight}\n")
    if self.has_corrosion != 0:
        print(f"부식: {self.has_corrosion}\n")
    if self.has_burn != 0:
        print(f"화상: {self.has_burn}\n")
    if self.has_vuln != 0:
        print(f"취약: {self.has_vuln}\n")
    if self.has_weak != 0:
        print(f"무력: {self.has_weak}\n")
    if self.has_capture != 0:
        print(f"속박: {self.has_capture}\n")
    if self.has_blind != 0:
        print(f"실명: {self.has_blind}\n")
    if self.has_crit != 0:
        print(f"치명타: {self.has_crit}\n")
    if self.has_power != 0:
        print(f"힘: {self.has_power}\n")
    if self.has_res != 0:
        print(f"저항: {self.has_res}\n")
    if self.has_guarded != 0:
        print(f"{self.guarded_by}에게 보호받음: {self.has_guard}\n")
    if self.has_prot != 0:
        print(f"방어: {self.has_prot}\n")
    if self.has_protplus != 0:
        print(f"방어+: {self.has_protplus}\n")
    if self.has_dodge != 0:
        print(f"회피: {self.has_dodge}\n")
    if self.has_dodgeplus != 0:
        print(f"회피+: {self.has_dodgeplus}\n")
    if self.has_restoration != 0:
        print(f"재생: {self.has_restoration}\n")
    if self.has_resonance != 0:
        print(f"공명 중첩: {self.has_resonance}")
    if self.has_explode != 0:
        print(f"폭발 중첩: {self.has_explode}")
    if self.has_fatigue != 0:
        print(f"피로 중첩: {self.has_fatigue}")
    if self.immunity != None:
        print(f"현재 {im} 피해에 면역 상태임")

#보호/도발
def guardcalc(precalctarget,tlist,isFriendly):
    t1 = tlist[0]
    t2 = tlist[1]
    t3 = tlist[2]
    t4 = tlist[3]
    target = precalctarget
    if isFriendly == False:
        if t1.has_taunt != 0:
            print(f"도발로 인해 {t1.myID}에게 강제 공격")
            target = t1
            target.has_taunt -= 1
        elif t2.has_taunt != 0:
            print(f"도발로 인해 {t2.myID}에게 강제 공격")
            target = t2
            target.has_taunt -= 1
        elif t3.has_taunt != 0:
            print(f"도발로 인해 {t3.myID}에게 강제 공격")
            target = t3
            target.has_taunt -= 1
        elif t4.has_taunt != 0:
            print(f"도발로 인해 {t4.myID}에게 강제 공격")
            target = t4
            target.has_taunt -= 1
        if precalctarget.guarded_by == t1.myID:
            print(f"보호로 인해 {t1.myID}에게 강제 공격")
            target = t1
        elif precalctarget.guarded_by == t2.myID:
            print(f"보호로 인해 {t2.myID}에게 강제 공격")
            target = t2
        elif precalctarget.guarded_by == t3.myID:
            print(f"보호로 인해 {t3.myID}에게 강제 공격")
            target = t3
        elif precalctarget.guarded_by == t4.myID:
            print(f"보호로 인해 {t4.myID}에게 강제 공격")
            target = t4
    return target

#몹 AI 타게팅
def targetting(tlist, isFriendly):
    t1 = tlist[0]
    t2 = tlist[1]
    t3 = tlist[2]
    t4 = tlist[3]
    isF = isFriendly
    target = randint(1,4)
    if t1 == None and target == 1:
        target = randint(1,4)
    elif target == 1:
        target = t1
    elif t2 == None and target == 2:
        target = randint(1,4)
    elif target == 2:
        target = t2
    elif t3 == None and target == 3:
        target = randint(1, 4)
    elif target == 3:
        target = t3
    elif t4 == None and target == 4:
        target = randint(1,4)
    elif target == 4:
        target = t4
    target = guardcalc(target,t1,t2,t3,t4,isF)
    return target

def targetother(input,spl,spl2):
    a = input.in_rank
    if spl != None:
        b = spl.in_rank
    else:
        b = None
    if spl2 != None:
        c = spl2.in_rank
    else:
        c = None
    if a is not None and b is not None and c is not None:
        if a != 1 and b != 1 and c != 1:
            return 1
        if a != 2 and b != 2 and c != 2:
            return 2
        if a != 3 and b != 3 and c != 3:
            return 3
        if a != 4 and b != 4 and c != 4:
            return 4
    elif a is not None and b is not None and c is None:
        if a != 1 and b != 1:
            return 1
        if a != 2 and b != 2:
            return 2
        if a != 3 and b != 3:
            return 3
        if a != 4 and b != 4:
            return 4
    elif a is not None and b is None and c is not None:
        if a != 1 and c != 1:
            return 1
        if a != 2 and c != 2:
            return 2
        if a != 3 and c != 3:
            return 3
        if a != 4 and c != 4:
            return 4
    elif a is None and b is not None and c is not None:
        if b != 1 and c != 1:
            return 1
        if b != 2 and c != 2:
            return 2
        if b != 3 and c != 3:
            return 3
        if b != 4 and c != 4:
            return 4
    elif a is None and b is None and c is not None:
        if c != 1:
            return 1
        if c != 2:
            return 2
        if c != 3:
            return 3
        if c != 4:
            return 4
    elif a is None and b is not None and c is None:
        if b != 1:
            return 1
        if b != 2:
            return 2
        if b != 3:
            return 3
        if b != 4:
            return 4
    elif a is not None and b is None and c is None:
        if a != 1:
            return 1
        if a != 2:
            return 2
        if a != 3:
            return 3
        if a != 4:
            return 4
    elif a and b and c is None:
        print("시스템 오류: 타게팅 값이 존재하지 않음")

def resonancedmg(self,target,chance):
    if target.has_resonance != 0:
        ch = randint(1, 100)
        if ch >= (100 - chance):
            dmgcalc(self,target,target.has_resonance,False,False)
            target.has_resonance = 0
            print("공명 폭발!")

def explodedmg(self,target,other1,other2,other3,chance):
    if target.has_explode != 0:
        ch = randint(1, 100)
        if ch >= (100 - chance):
            dmgcalc(self,other1,target.has_explode,False,False)
            dmgcalc(self, other2, target.has_explode, False, False)
            dmgcalc(self, other3, target.has_explode, False, False)
            target.has_explode = 0
            print("기폭!")

def fatiguedmg(self,target,chance):
    if target.has_fatigue != 0:
        ch = randint(1, 100)
        if ch >= (100 - chance):
            target.sanity -= target.has_fatigue
            target.has_fatigue = 0
            print("정신 붕괴!")

#스킬 선택창
def playerskillinput(self,tlist,plist):
    t1 = tlist[0]
    t2 = tlist[1]
    t3 = tlist[2]
    t4 = tlist[3]
    p1 = plist[0]
    p2 = plist[1]
    p3 = plist[2]
    p4 = plist[3]
    print("행동을 선택하세요:\n")
    m = None
    move = input(f"1. {self.skill1name}\n"
                  f"2. {self.codedictionary[self.skill2name]}\n"
                  f"3. {self.codedictionary[self.skill3name]}\n"
                  f"4. {self.codedictionary[self.skill4name]}\n"
                  f"5. {self.codedictionary[self.skill5name]}\n"
                  f"6. {self.codedictionary[self.skill6name]}\n"
                  f"7. 이동\n"
                  f"8. 전투 아이템 사용: {self.equippeditemname}\n"
                  f"9. 넘기기\n"
                 f"원하시는 행동의 번호를 입력해주세요.\n")
    if move == 1:
        self.useskill1(self,tlist,plist)
    if move == 2:
        self.useskill2(self, tlist, plist)
    if move == 3:
        self.useskill3(self,tlist,plist)
    if move == 4:
        self.useskill4(self,tlist,plist)
    if move == 5:
        self.useskill5(self,tlist,plist)
    if move == 6:
        self.useskill6(self,tlist,plist)
    if move == 7:
        amount = input("이동하고 싶으신 값을 입력해 주세요. (음수는 뒤로, 양수는 앞으로)")
        if self.minmove <= amount <= self.maxmove:
            self.moveskill(self,amount)
            print(f"이동: 현재 {self.in_rank}열에 있습니다.")
    if move == 8:
        self.useitem(tlist,plist)
    if move == 9:
        self.useinitiative(self)
        print("넘기기")