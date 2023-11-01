from random import *
import farok_engine

#태엽장치 골렘

class Gearwork_golem(farok_engine.Enemy):
    myID = "gearworkgolem"
    intro = "태엽장치 골렘 전투 \n" \
            "당신은 모험가들과 함께 잊혀진 사막으로 진입했습니다. \n" \
            "사막의 모래바람이 당신의 살을 찢고, 점점 햇빛이 강해지는 것이 느껴집니다. \n" \
            "\n" \
            "...당신들은 거대한 성소에 도착하였습니다.\n" \
            "원정의 목적지에 도달한 당신들은, 조심스럽게 성자의 관이 놓여있는 함을 관찰합니다. \n" \
            "\n" \
            "그러나 그때, 옆에서 태엽장치가 맹렬히 돌아가는 소리를 내며 당신들을 덮쳐옵니다!\n" \
            "\n" \
            "\n" \
            "거구의 돌로 만들어진, 인간 형상의 수호자.\n" \
            "주인의 영원한 안식을 지키고자 태엽장치와 강철과 돌로 이루어진 몸을 일으켜 원정대의 앞을 막아섭니다.\n" \
            "<이곳을 지나갈 자, 그 누구도 없으리.>\n" \
            "전투 시작.\n"
    originfo = "태엽장치 골렘\n" \
           "턴 시작시 태엽 교체를 이용해 공격 패턴을 주기적으로 변환함.\n" \
           "출혈, 중독에 면역.\n" \
           "\n...숨겨진 정보가 더 있을것 같다.\n\n"
    info = None
    maxhp = 600
    hp = 600
    defaultinit = 2
    initiative = None
    defaultdmgrec = -0.15
    defaultdodge = 0.15
    type1 = farok_engine.stonework
    type2 = farok_engine.undead
    bleedres = 4000
    blightres = 4000
    corossionres = 40
    burnres = 40
    globalres = 60
    moveres = 1000
    status = "일반"
    has_bleed = 0
    has_blight = 0
    has_corrosion = 0
    has_burn = 0
    has_vuln = 0
    has_weak = 0
    has_capture = 0
    has_res = 0
    has_crit = 0
    has_restoration = 0  # 재생
    has_stun = 0
    has_guard = 0
    has_prot = 0
    has_protplus = 0
    has_dodge = 0
    has_dodgeplus = 0
    strength = 0
    speed = 3
    in_rank = 56
    turn_value = None
    guarded_by = "None" #XXX에 의해 보호됨
    #고유 코드
    forcecharge = 0
    wrathhigh = False #저압/고압 상태에서 사용시 태엽 효과
    agonylow = False
    forcehigh = False
    forcelow = False
    lamentlow = False
    mortality = 1000
    rage = 0
    gear = "일반"
    canusedestruction = False
    #사실 몬스터가 변경하는 값 외에는 넣을 필요 없으나 (예시: 0으로 되어있는 값들) 예시격으로 넣어둠
#몬스터 설명용 변수들
    gearinfo = None
    rageinfo = None
    agonyinfo = None
    forceinfo = None
    lamentinfo = None
    destinfo = None
    mortalinfo = None

    def info_update(self,value):
        if value == "gear":
            self.gearinfo = "태엽 교체시마다 특정 강화, 특정 약화를 받는 것으로 보인다.\n 고압이나 저압 상태에서 태엽이 교체되면 부가 효과가 생긴다.\n"
        if value == "rage":
            self.rageinfo = "분노의 태엽을 끼우면 힘이 강해지고, 그만큼 취약해진다.\n강력한 내려찍기 공격을 사용하나, 가끔 증기 압축이 충분히 되지 않아 약한 공격을 한다.\n"
        if value == "agony":
            self.agonyinfo = "고뇌의 태엽을 끼우면 취약하고 무기력해 지지만, 존재 자체만으로도 정신에 막대한 피해를 입힌다.\n아군이 가진 공포를 이용해 그들의 정신을 파괴하는 것으로 보인다.\n"
        if value == "force":
            self.forceinfo = "강제의 태엽을 끼우면 힘을 극한으로 끌어내, 아무리 강인한 모험가라도 기절시킬 수 있다. 그 대가로 속도가 느려진다.\n찍어누르며 주변에 동시에 피해를 주는 기술을 사용하는 것으로 보인다.\n"
        if value == "lament":
            self.lamentinfo = "비탄의 태엽을 끼우면 내면에 잠든 인간의 후회와 슬픔을 끌어내 아군을 극한의 갈등과 공포로 내몬다.\n모든 아군에게 정신을 파괴하는 공격을 하는 것으로 보인다.\n"
        if value == "dest":
            self.destinfo = "주인의 마지막 휴식을 방해한 이들에게 골렘이 분노하며 태엽을 갈아끼운다.\n매우 강력한 공격을 사용하니 주의해야 한다.\n"
        if value == "mortal":
            self.mortalinfo = "파괴의 태엽에 새겨진 필멸의 표식이 점점 줄어들고 있다. 완전히 사라지는 순간 재앙이 덮칠 것이다."
        self.info == self.originfo + self.gearinfo + self.rageinfo + self.agonyinfo + self.forceinfo + self.lamentinfo + self.destinfo + self.mortalinfo

# 태엽
    def cleargear(self):
        if self.gear == "태엽: 분노":
            self.strength -= 3
            if self.wrathhigh == True:
                self.strength -= 1
        self.agonylow = False
        self.forcehigh = False
        self.forcelow = False
        self.lamentlow = False

    # 이펙트
    def eff_chargeremoval(self):
        if self.forcecharge != 0:
            self.forcecharge -= 1
        if self.forcecharge == 0:
            self.strength -= 6

    def eff_wrathselfharm(self):
        if self.gear == "태엽: 분노":
            self.hp -= randint(1, 4)

    def eff_enemylament(self, target1, target2, target3, target4):
        if self.gear == "태엽: 비탄":
            farok_engine.apply_sinking(self,120,1,target1)
            target1.sanityres -= 33
            farok_engine.apply_sinking(self,120,1,target2)
            target2.sanityres -= 33
            farok_engine.apply_sinking(self,120,1,target3)
            target3.sanityres -= 33
            farok_engine.apply_sinking(self,120,1,target4)
            target4.sanityres -= 33

    def eff_forcecapture(self):
        if self.gear == "태엽: 강제":
            self.has_capture += 1

    def eff_agonyweak(self):
        if self.gear == "태엽: 고뇌":
            farok_engine.apply_weak(self,1000,1,self)
            farok_engine.apply_weak(self, 1000, 1, self)
            if self.agonylow == True:
                farok_engine.apply_weak(self,1000,1,self)
    def eff_destr(self):
        if self.gear == "태엽: 파괴":
            self.defaultdmgrec += 0.07

#종합이펙트
    def gearworkgolem_check(self,target1,target2,target3,target4):
        self.eff_chargeremoval()
        self.eff_wrathselfharm()
        self.eff_enemylament(target1,target2,target3,target4)
        self.eff_forcecapture()
        self.eff_agonyweak()
        self.eff_destr()


#태엽 변경
    def gear_change(self):
        print("<태엽 교체>\n")
        self.info_update("gear")
        self.cleargear()
        self.rage = self.rage+5
        print(f"! 현재 누적 광폭: {self.rage} !\n")
        if self.canusedestruction == False:
            i = randint(1,100)
            if i >= 1 and i <= 30:
                self.gear = "태엽: 분노"
                print(f"{self.gear}\n")
                self.strength += 3
                if self.status == "고압":
                    self.strength += 1
                    farok_engine.apply_vuln(self,1000,2,self)
                    self.wrathhigh = True
            if i >= 31 and i <= 60:
                self.gear = "태엽: 고뇌"
                print(f"{self.gear}\n")
            if self.status == "저압":
                    self.agonylow = True
            if i >= 61 and i <= 90:
                self.gear = "태엽: 강제"
                print(f"{self.gear}\n")
                if self.status == "고압":
                    self.forcehigh = True
                if self.status == "저압":
                    self.forcelow = True
            if i >= 91 and i <= 100:
                self.gear = "태엽: 비탄"
                print(f"{self.gear}\n")
                self.hp -= 10
                farok_engine.apply_vuln(self,1000,5,self)
                if self.status == "저압":
                    self.lamentlow = True
        elif self.canusedestruction == True:
            self.gear = "태엽: 파괴"
            self.info_update("dest")
            print(f"{self.gear}\n")
            self.rage = 100
            self.status = "광분"
            self.hp = 300
            self.maxhp = 300
            self.defaultdmgrec = 0.2
            self.mortality = 3
            print(f"골렘이 무덤의 훼손에 크게 분노합니다! 현재 필멸 토큰: {self.mortality}")


#공용스킬
    def forced_charge(self):
        print("강제적 충전\n")
        self.strength += 6
        self.forcecharge = 2
        farok_engine.apply_vuln(self,1000,3,self)
        self.hp -= 10
        farok_engine.useinitiative(self)


    def pressure_high(self):
        print("압력 상승\n")
        if self.status == "일반":
            self.status = "고압"
            self.speed += 10
            farok_engine.apply_vuln(self,1000,1,self)
            print("고압 상태에 돌입합니다!\n")
        if self.status == "저압":
            print("저압 상태가 해제되었습니다!\n")
            self.status = "일반"
            self.speed += 6
            self.strength += 2
        farok_engine.useinitiative(self)


    def pressure_low(self):
        print("압력 하락\n")
        if self.status == "일반":
            self.status = "저압"
            self.speed -= 6
            self.strength -= 2
            farok_engine.apply_prot(self,1000,1,self)
            print("저압 상태에 돌입합니다!\n")
        if self.status == "고압":
            self.status = "일반"
            print("고압 상태가 해제되었습니다!\n")
            self.speed -= 10
        farok_engine.useinitiative(self)


    def protect_master(self, target):
        print("주인을 보호하라\n")
        farok_engine.apply_guard(self,1,target)
        farok_engine.apply_crit(self, 1000, 1, self)
        farok_engine.apply_res(self, 1000, 1, self)
        farok_engine.useinitiative(self)


    #태엽기술
    def material_pulverize(self, target):
        print("물질 파쇄\n")
        self.info_update("rage")
        farok_engine.apply_weak(self,1000,2,self)
        dmg = randint(1,10) + randint(1,10)
        farok_engine.attackcalc(self,target,20,dmg,False,True,False,False,"physic")
        farok_engine.useinitiative(self)


    def fright_glare(self, target, target2,other1,other2):
        print("섬뜩한 응시\n")
        self.info_update("agony")
        chance = 130
        if target.global_res < 100:
            chance += 1000000
        elif self.agonylow == True:
            chance += 1000000
        dmg = randint(1,5) + target.has_horror
        dmg2 = randint(1,5) + target2.has_horror
        ishit1 = farok_engine.attackcalc(self, target, 20, dmg, False, True, False, False, "magic")
        ishit2 = farok_engine.attackcalc(self, target2, 20, dmg2, False, True, False, False, "magic")
        if ishit1 == True:
            farok_engine.apply_sinking(self, chance, 2, target)
            farok_engine.apply_horror(self, chance, 3, target)
            farok_engine.Ppull(self,120,2,target,other1,other2,target2)
            farok_engine.stress(self, 140, 6, target)
        if ishit2 == True:
            farok_engine.apply_sinking(self, chance, 2, target2)
            farok_engine.apply_horror(self, chance, 3, target2)
            farok_engine.Ppull(self, 120, 2, target2,target,other1,other2)
            farok_engine.stress(self, 140, 6, target)
        farok_engine.useinitiative(self)


    def press_down(self, target, splashtarget, other1, other2):
        print("찍어누르기\n")
        self.info_update("force")
        dmg = randint(1,4) + 10
        if target.stunres < 60:
            dmg += 4
        chance = 100
        if self.forcelow == True:
            chance -=33
        if self.forcehigh == True:
            chance +=33
        ishit = farok_engine.attackcalc(self,target,0,dmg,False,False,False,False, "physic")
        if ishit == True:
            farok_engine.apply_stun(self,chance,target)
            farok_engine.apply_capture(self,chance,3,splashtarget)
            farok_engine.Ppull(self,110,2,target,other1,other2, splashtarget)
        farok_engine.useinitiative(self)


    def prisoner(self, p1,p2,p3,p4):
        print("나는 죄인이오니\n")
        self.info_update("lament")
        amount = 2
        if self.lamentlow == True:
            amount += 1
        dmg1 = 5 + randint(1, 3) + p1.has_sinking
        dmg2 = 5 + randint(1, 3) + p2.has_sinking
        dmg3 = 5 + randint(1, 3) + p3.has_sinking
        dmg4 = 5 + randint(1, 3) + p4.has_sinking
        hit1 = farok_engine.attackcalc(self,p1,20,dmg1,False,False,False,False,"magic")
        hit2 = farok_engine.attackcalc(self, p2, 20, dmg2, False, False, False, False,"magic")
        hit3 = farok_engine.attackcalc(self, p3, 20, dmg3, False, False, False, False,"magic")
        hit4 = farok_engine.attackcalc(self, p4, 20, dmg4, False, False, False, False,"magic")
        if hit1 == True:
            farok_engine.apply_horror(self,120,amount,p1)
            farok_engine.stress(self, 140, 11, p1)
        if hit2 == True:
            farok_engine.apply_horror(self, 120, amount, p2)
            farok_engine.stress(self, 140, 11, p2)
        if hit3 == True:
            farok_engine.apply_horror(self, 120, amount, p3)
            farok_engine.stress(self, 140, 11, p3)
        if hit4 == True:
            farok_engine.apply_horror(self, 120, amount, p4)
            farok_engine.stress(self, 140, 11, p4)
        farok_engine.useinitiative(self)


    #광폭화
    def highcrush(self,target):
        print("초고압 파쇄\n")
        mortch = 50
        ch = randint(1, 100)
        if ch >= (100 - mortch):
            self.mortality -=1
            self.info_update("mortal")
        dmg = randint(1,10) + randint(1,10) + randint(1,10) -6
        if dmg <= 0:
            dmg == 0
        ishit = farok_engine.attackcalc(self,target,20,dmg,False,False,False,False,"physic")
        if ishit == True:
            farok_engine.apply_horror(self,140,2,target)
            farok_engine.apply_capture(self,140,1,target)
            farok_engine.apply_weak(self,140,1,target)
        newch = 33
        ch = randint(1, 100)
        if ch >= (100 - newch):
            self.hp -= 15
        farok_engine.useinitiative(self)


    def prison_lament(self,p1,p2,p3,p4):
        print("죄인의 비탄\n")
        mortch = 50
        ch = randint(1, 100)
        if ch >= (100 - mortch):
            self.mortality -= 1
            self.info_update("mortal")
        dmg1 = randint(1,10)
        dmg2 = randint(1, 10)
        dmg3 = randint(1, 10)
        dmg4 = randint(1, 10)
        ishit1 = farok_engine.attackcalc(self,p1,20,dmg1,False,False,False,False,"magic")
        ishit2 = farok_engine.attackcalc(self, p2, 20, dmg2, False, False, False, False,"magic")
        ishit3 = farok_engine.attackcalc(self, p3, 20, dmg3, False, False, False, False,"magic")
        ishit4 = farok_engine.attackcalc(self, p4, 20, dmg4, False, False, False, False,"magic")
        if ishit1 == True:
            farok_engine.apply_sinking(self,140,2,p1)
            farok_engine.apply_horror(self,140,1,p1)
            farok_engine.apply_weak(self,140,2,p1)
            farok_engine.stress(self,140,10,p1)
        if ishit2 == True:
            farok_engine.apply_sinking(self,140,2,p2)
            farok_engine.apply_horror(self,140,1,p2)
            farok_engine.apply_weak(self,140,2,p2)
            farok_engine.stress(self, 140, 10, p2)
        if ishit3 == True:
            farok_engine.apply_sinking(self,140,2,p3)
            farok_engine.apply_horror(self,140,1,p3)
            farok_engine.apply_weak(self,140,2,p3)
            farok_engine.stress(self, 140, 10, p3)
        if ishit4 == True:
            farok_engine.apply_sinking(self,140,2,p4)
            farok_engine.apply_horror(self,140,1,p4)
            farok_engine.apply_weak(self,140,2,p4)
            farok_engine.stress(self, 140, 10, p4)
        newch = 33
        ch = randint(1, 100)
        if ch >= (100 - newch):
            self.hp -= 25
        farok_engine.useinitiative(self)


    def the_mortality(self,target):
        print("필멸\n")
        target.hp -= 9999999999999
        farok_engine.useinitiative2(self)
        farok_engine.apply_stun(self,200,self)
        farok_engine.apply_vuln(self,200,3,self)
        self.mortality = 3


    #알고리즘

    def monsterbrain(self,tlist,grave):
        target1 = tlist[0]
        target2 = tlist[1]
        target3 = tlist[2]
        target4 = tlist[3]
        print("태엽장치 골렘의 턴:\n")

        self.initiative = self.defaultinit
        while self.initiative != 0:
            farok_engine.effectcheck(self)
            self.gearworkgolem_check(target1,target2,target3,target4)
            ch = randint(1,100)
            if self.initiative != 0:
                if self.canusedestruction == False:
                    if ch <= 50:
                        self.gear_change()
                    ch = randint(1,100)
                    if ch > 20:
                        self.forced_charge()
                    if ch <= 20 and ch > 40:
                        self.pressure_high()
                    if ch <= 40 and ch > 60:
                        self.pressure_low()
                    if ch <= 60 and ch > 80:
                        self.protect_master(grave)
                    if ch <= 80:
                        if self.gear == "태엽: 분노":
                            target = farok_engine.targetting(target1, target2, None, None, False)
                            self.material_pulverize(target)
                        if self.gear == "태엽: 고뇌":
                            self.fright_glare(target4,target1,target2,target3)
                        if self.gear == "태엽: 강제":
                            target = farok_engine.targetting(target1, target2, target3, None, False)
                            spl = farok_engine.targetting(target1,target2,target3,target4, False)
                            other1 = farok_engine.targetother(target,spl,None)
                            other2 = farok_engine.targetother(target, spl, other1)
                            self.press_down(target,spl,other1,other2)
                        if self.gear == "태엽: 비탄":
                            self.prisoner(target1,target2,target3,target4)
                if self.canusedestruction == True:
                    self.gear_change()
                    if self.mortality == 0:
                        target = farok_engine.targetting(target1, target2, target3, target4, False)
                        self.the_mortality(target)
                    elif ch > 50:
                        target = farok_engine.targetting(target1, target2, target3, None, False)
                        self.highcrush(target)
                    elif ch <= 50:
                        self.prison_lament(target1,target2,target3,target4)
        print("턴 종료.")


class Holy_grave(farok_engine.Enemy):
    myID = "holygrave"  # 프로그램 내에서 호출시 코드
    intro = None  # 적 조우시 출력하는 텍스트
    originfo = "심상치 않은 기운이 뿜어져 나오는 성소.\n" \
               "누군가가 이곳에서 안식을 취하고 있는 듯 하다.\n" \
               "...뭔가 숨겨진 정보가 더 있는것 같다.\n"   # 처음 표시되는 기본 텍스트
    info = None  # 이후 기술로 인해 추가된 텍스트를 포함해서 전체 정보를 보여주는 변수
    maxhp = 90 # 최대체력
    hp = 90  # 체력 설정
    # 몹은 정신력이 존재하지 않음. 침잠/공포 없음
    defaultinit = 1  # 기본 행동권 (고유)
    initiative = None  # 행동권 (현재 보유중)
    defaultdmgrec = 0  # 기본 방어도 (받뎀감)
    defaultdodge = 0  # 기본 회피
    type1 = "holy"  # 몬스터 속성
    type2 = "stonework"
    bleedres = 4000  # 출혈저항
    blightres = 4000  # 중독저항
    corrosionres = 0  # 부식저항
    burnres = 0  # 화상저항
    stunres = 4000
    globalres = 4000  # 약화저항 (무력, 취약 등)
    moveres = 4000  # 이동저항
    status = None  # 변신 기믹 활용시 필요
    has_bleed = 0  # 현재 가진 상태이상 체크
    has_blight = 0
    dmg_blight = 0  # 중독량
    has_corrosion = 0
    has_burn = 0
    has_vuln = 0
    has_weak = 0
    has_capture = 0
    has_res = 0
    has_crit = 0
    has_restoration = 0 # 재생
    has_blind = 0
    has_stun = 0
    has_guard = 0
    has_taunt = 0  # 도발
    has_prot = 0
    has_protplus = 2
    has_dodge = 0
    has_dodgeplus = 0
    has_power = 0
    strength = 0  # 현재 가진 위력 증가량
    speed = 3  # 속도값
    in_rank = 78  # 현재 열 (위치)
    turn_value = None  # None으로 놔둘것. 계산에 필요
    guarded_by = "None"  # XXX에 의해 보호됨
    immunity = "None"
    gearinfo = None
    rageinfo = None
    agonyinfo = None
    forceinfo = None
    lamentinfo = None
    destinfo = None
    mortalinfo = None

    def info_update(self,value):
        if value == "gear":
            self.gearinfo = "태엽 교체시마다 특정 강화, 특정 약화를 받는 것으로 보인다.\n 고압이나 저압 상태에서 태엽이 교체되면 부가 효과가 생긴다.\n"
        if value == "rage":
            self.rageinfo = "분노의 태엽을 끼우면 힘이 강해지고, 그만큼 취약해진다.\n강력한 내려찍기 공격을 사용하나, 가끔 증기 압축이 충분히 되지 않아 약한 공격을 한다.\n"
        if value == "agony":
            self.agonyinfo = "고뇌의 태엽을 끼우면 취약하고 무기력해 지지만, 존재 자체만으로도 정신에 막대한 피해를 입힌다.\n아군이 가진 공포를 이용해 그들의 정신을 파괴하는 것으로 보인다.\n"
        if value == "force":
            self.forceinfo = "강제의 태엽을 끼우면 힘을 극한으로 끌어내, 아무리 강인한 모험가라도 기절시킬 수 있다. 그 대가로 속도가 느려진다.\n찍어누르며 주변에 동시에 피해를 주는 기술을 사용하는 것으로 보인다.\n"
        if value == "lament":
            self.lamentinfo = "비탄의 태엽을 끼우면 내면에 잠든 인간의 후회와 슬픔을 끌어내 아군을 극한의 갈등과 공포로 내몬다.\n모든 아군에게 정신을 파괴하는 공격을 하는 것으로 보인다.\n"
        if value == "dest":
            self.destinfo = "주인의 마지막 휴식을 방해한 이들에게 골렘이 분노하며 태엽을 갈아끼운다.\n매우 강력한 공격을 사용하니 주의해야 한다.\n"
        if value == "mortal":
            self.mortalinfo = "파괴의 태엽에 새겨진 필멸의 표식이 점점 줄어들고 있다. 완전히 사라지는 순간 재앙이 덮칠 것이다."
        self.info == self.originfo + self.gearinfo + self.rageinfo + self.agonyinfo + self.forceinfo + self.lamentinfo + self.destinfo + self.mortalinfo

    def untouchable_aura(self, target1,target2,target3,target4):
        ch = randint(1,3)
        if ch == 1:
            self.immunity = "magic"
        if ch == 2:
            self.immunity = "physic"
        if ch == 3:
            farok_engine.apply_sinking(self,120,1,target1)
            farok_engine.apply_sinking(self, 120, 1, target2)
            farok_engine.apply_sinking(self, 120, 1, target3)
            farok_engine.apply_sinking(self, 120, 1, target4)