image plgrd = "images/plgrd.png"
image baituan = "images/baituan.png"
image bsktb = "images/bsktb.jpeg"
image doomroom = "images/doomroom.png"
image eatingstreet = "images/eatingstreet.png"
image empstreet = "images/empstreet.png"
image tingzhong = "images/tingzhong.png"
image willows = "images/willows.png"
image eatingstreet_bw = "images/eatingstreet_gray.png"
image mdsN = Transform("images/mds_N.png", zoom=0.18, yalign=1.0, yoffset=50)
image mdsM = Transform("images/mds_moved.png", zoom=0.18, yalign=1.0, yoffset=50)
image msN = Transform("images/MSN.png", zoom=0.29, yalign=1.0, yoffset=38)
image mshappy = Transform("images/MShappy.png", zoom=0.29, yalign=1.0, yoffset=38)
image msdislike = Transform("images/MSdislike.png", zoom=0.29, yalign=1.0, yoffset=38)
image msscare = Transform("images/MSscare.png", zoom=0.29, yalign=1.0, yoffset=38)
image mssmile = Transform("images/MSsmile.png", zoom=0.29, yalign=1.0, yoffset=38)
image qy = Transform("images/qiuyuan.png", zoom=0.75, yalign=1.0, yoffset=850,xoffset=-58)
image qy3 = Transform("images/qiuyuan3.png", zoom=0.59, yalign=1.0, yoffset=850,xoffset=-8)
image doll1 = Transform("images/DOLLN.png", zoom=0.33, yalign=1.0, yoffset=140)
image doll2 = Transform("images/DOLLNOT.png", zoom=0.33, yalign=1.0, yoffset=140)
image HKT1 = Transform("images/HKT.png", zoom=0.4, yalign=1.0, yoffset=86)
image palace = "images/jk1.jpg"
image qny = Transform("images/V11.png", zoom=0.45, yalign=1.0, yoffset=0,xoffset=-35)
image qnys = Transform("images/V11S.png", zoom=0.45, yalign=1.0, yoffset=0,xoffset=-35)
image als = Transform("images/ALISA.png", zoom=0.4, yalign=1.0, yoffset=86,xoffset=-35)
image alss = Transform("images/ALISASMILE.png", zoom=0.4, yalign=1.0, yoffset=86,xoffset=-35)
image p2 = Transform("images/crm.png", zoom=0.26, yalign=1.0, yoffset=0,xoffset=15)
image grmd = Transform("images/grandma.png", zoom=0.39, yalign=1.0, yoffset=86,xoffset=-35)
image kingking = Transform("images/theking.png", zoom=0.2, yalign=1.0, yoffset=230,xoffset=-35)
image oldsd = Transform("images/soldier.png", zoom=0.59, yalign=1.0, yoffset=316,xoffset=-15)
image newds = Transform("images/morisa.png", zoom=0.73, yalign=1.0, yoffset=63,xoffset=20)

define config.menu_include_disabled = True
define o = Character(None) 
define p = Character("我", color="#ffffff")
define doll = Character("晴天娃娃", color="#ff6347")
define medusa = Character("美杜莎", color="#8a2be2")
define misha = Character("米莎", color="#f0e68c")
define ivan = Character("伊万", color="#6b8e23")
define manager = Character("管理者", color="#074788")
define gloves_woman = Character("手套女人", color="#4682b4")
define fabian = Character("法比安神父", color="#daa520")
define alexander = Character("亚历山大", color="#a0522d")
define v1 = Character("实验体 v1", color="#00ffff")
define hecate = Character("赫卡忒", color="#d3d3d3")
define alisa = Character("阿莉莎", color="#ffffff")
define third_me = Character("“我”", color="#dc143c")
define crm = Character("绯月", color='#d2603e' )
define ela = Character("艾莉娅", color="#44bae1")
define gny = Character("老奶奶", color="#b2b24a")
define sb = Character("新的勇者",color="#a4a8ef")
define king = Character("国王", color="#e4f12b")
define session_store = { "is_host": None, "saved_ip": "127.0.0.1" }

default joint = 0
default H = 3
default E = 3
default S = 3
default C = 3
default F = 3
default L = 3
default favorability = 0
default IfTogether = 0
default my_plane = 1
default opponent_plane = 1
default network_status = "未连接"
default my_role = None
default my_action = 0
default opponent_action = 0
default i_have_chosen = False
default opponent_has_chosen = False
default is_host = None
default event_queue = []

label splashscreen:
    $ network_status = "未连接"
    window show
    show snow_white_big
    scene UniverseWithin with dissolve
    show msN at walk32
    "正在释放神经递质………"
    menu:
        "我是主人 (Host)":
            $ is_host = True
            $ session_store["is_host"] = True
            hide msN
            show mshappy
            pause 1.2
            
        "我是仆人 (Client)":
            $ is_host = False
            $ session_store["is_host"] = False
            $ host_ip = renpy.input("请输入主机IP地址", default="127.0.0.1", length=20)
            $ host_ip = host_ip.strip()
            $ session_store["saved_ip"] = host_ip 
            hide msN
            show mshappy
            pause 1.2

    return

label start:
    scene hud with dissolve
    pause 1.15
    scene black
    python:
        is_host = session_store["is_host"]
        renpy.store.i_have_chosen = False
        renpy.store.my_action = None
        renpy.store.event_queue = []
        renpy.store.opponent_has_chosen = False
        
        if is_host:
            reset_and_start_network(True)
        else:
            saved_ip = session_store.get("saved_ip", "127.0.0.1")
            reset_and_start_network(False, saved_ip)
            
        renpy.pause(0.1)

    if not is_host:
        "正在等待连接建立...{w=0.1}{nw}"
        
        python:
            while "已连接" not in network_status:
                renpy.pause(0.1)

            while True:
                send_sync_action(900)
                
                got_ack = False
                for i in range(20): 
                    renpy.pause(0.05) 
                    for ev in list(renpy.store.event_queue):
                        if ev.get("action") == 9001:
                            got_ack = True
                            break
                    if got_ack: break
                
                if got_ack:
                    send_sync_action(9002)
                    renpy.pause(0.05)
                    break
        $ renpy.store.event_queue = []
        $ renpy.store.opponent_has_chosen = False # 重置选择状态
        $ renpy.store.opponent_action = None      # 清空对方动作
        jump scene_1
        
    else:
        "等待客机接入...{w=0.1}{nw}"
        
        python:
            while "已连接" not in network_status:
                renpy.pause(0.1)

            renpy.store.event_queue = []

            while True:
                has_req = False
                has_ready = False
                for ev in list(renpy.store.event_queue):
                    if ev.get("action") == 900: has_req = True
                    if ev.get("action") == 9002: has_ready = True
                
                if has_ready:
                    break
                elif has_req:
                    send_sync_action(9001)
                    renpy.pause(0.05)
                
                renpy.pause(0.05)
        
        $ renpy.store.event_queue = []
        $ renpy.store.opponent_has_chosen = False
        $ renpy.store.opponent_action = None
        jump scene_1

label select_jk:

    $ my_role = ROLE_NONE
    
    if is_host:
        $ my_role_is_host = True
    else:
        $ my_role_is_host = False

    call screen role_select_screen
    
    if my_role == ROLE_KING:
        "你抢到了「魔王」！"
        jump scene_palace_king
        
    elif my_role == ROLE_HERO:
        "你获得了「勇者」！"
        jump scene_palace_knight

label scene_palace_king:
    $ my_role = ROLE_KING
    scene palace with dissolve
    o "你蜷在镶嵌着月光石的王座上"
    o "九条毛茸茸的尾巴像云朵般铺展在天鹅绒软垫上"
    show p2
    o "你的尾尖无意识地卷住王座扶手上的鎏金藤蔓纹路"
    o "指甲在冰凉的月光石表面刮出细碎声响"
    o "穹顶垂下的水晶珠帘折射着冷光"
    o "你百无聊赖地数着那些菱形切面"
    show emm11
    o "直到第两百三十七颗时..."
    o "殿外忽然又传来铠甲碰撞的铿锵声。"
    show steam11
    crm "又有新的客人呢,嗯哼哼"
    o "直到一个金发勇者跌跌撞撞闪到殿下和你打了个对眼"
    o "你这才发觉,她看见了你背后的九条尾巴"
    menu:
        "好奇怪的勇者,看上去弱弱的,那我就放点水吧":
            $ my_action = 1
            jump judge1
        "大胆人类,竟敢闯入我的宫殿里,我看你是活腻了":
            $ my_action = 2
            jump judge1
#这里是勇者看到的
label scene_palace_knight:
    $ my_role = ROLE_HERO
    scene palace with dissolve
    o "世间相传,熊野山上有一个九尾魔王"
    o "每个路过的客商都是有去无回"
    o "国王为了维护国家的安定,征集勇者讨伐魔王"
    o "但每个前往的勇者都在回国后宣告任务失败,在国王面前自刎谢罪。"
    show oldsd
    o "你抱着必死的决心,接下了这一任务。"
    o "你一路过关斩将,打败了众多小怪"
    o "你来到了魔王的殿前"
    o "但是你由于体力不支,只能跌跌撞撞向前奔去"
    o "但是当你发现了传说中的魔王怎么是个乳臭未干的小狐狸..."
    $ stream_hearts()
    o "而且长得这么可爱！！！"
    menu:
        "魔王,纳命来,今天我就要替天行道!":
            $ my_action = 1
            jump judge1
        "等一下,为什么魔王是一只小狐狸,一定有诈！":
            $ my_action = 2
            jump judge1
        "呜呼呼呼呼可爱的小狐狸直接拐回家里当宠物嘻嘻嘻嘻":
            $ my_action = 3
            jump judge1

label judge1:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice()
    python:
        if my_role == ROLE_KING:
            king_choice = my_action
            hero_choice = opponent_action
        else:
            hero_choice = my_action
            king_choice = opponent_action

    if king_choice == 1 and hero_choice == 1:
        o "魔王与勇者周旋,但不敌勇者,最终被勇者拐回家"
        $ favorability += 10
        jump scene_home

    elif king_choice == 1 and hero_choice == 2:
        o "勇者输得非常彻底,魔王把勇者的剑挂在了勇者脖子上"
        jump scene_strive

    elif king_choice == 1 and hero_choice == 3:
        crm "哎？？？？？？唔唔唔唔唔唔唔唔唔唔唔"
        $ favorability += 25
        jump scene_home

    elif king_choice == 2 and hero_choice == 1:
        o "双方展开了一场激烈的战斗"
        jump scene_strive

    elif king_choice == 2 and hero_choice == 2:
        o "勇者在犹豫中被魔王打败了"
        jump scene_die

    elif king_choice == 2 and hero_choice == 3:
        crm "啊，谁是宠物，啊？"
        crm "小样，就这？？"
        crm "那这位可爱的勇者大姐姐就当我的宠物吧～"
        o "勇者变成了魔王的宠物"
        $ favorability += 25
        jump scene_palace_2

label scene_strive:
    scene jk3 with dissolve
    show p2
    show steam11
    crm "拿出了八成功力,力量在她的身旁翻涌"
    hide p2
    show oldsd
    show steam11
    ela "感到了巨大的压迫,有些喘不过气"
    if my_role == ROLE_HERO:
        jump scene_palace_knight_2
    else:
        jump scene_palace_king_2

label scene_palace_king_2:
    scene palace with dissolve
    show p2
    menu:
        "世间纷争何必,劝诫勇者收手":
            $ my_action = 1
            jump judge2
        "我钦佩你的勇气,但你今天走不出去了":
            $ my_action = 2
            jump judge2

label scene_palace_knight_2:
    scene palace with dissolve
    show oldsd
    menu:
        "罢了,死了也是成就一番好名声":
            $ my_action = 1
            jump judge2
        "发动阴招！":
            $ my_action = 2
            jump judge2
        

label scene_home:
    scene jk4 with dissolve
    show oldsd
    ela "魔王大人怎么只是一个乳臭未干的小狐狸"
    ela "真可爱fuwafuwa"
    $ stream_hearts()
    ela "还有可爱的小手手"

    if my_role == ROLE_HERO:
        menu:
            "偷偷摸摸魔王的小尾巴":
                $ favorability += 20
                $ joint = 1
            "盘问魔王身世和力量来源，要拿去王宫论赏":
                $ joint = 2
        $ make_sync_choice(joint)
    else:
        o "等待对方选择中"
        $ wait_for_opponent_choice()
        $ joint = opponent_action

    if joint == 1:
        if my_role == ROLE_KING:
            menu:
                "讨厌人家这样会害羞的":
                    $ king_choice = 1
                    $ make_sync_choice(1) 
                "沉溺在勇者的宠爱之中，发出了舒服的呼噜声":
                    $ favorability += 25
                    $ king_choice = 2
                    $ make_sync_choice(2) 
        else:
            o "等待魔王反应中..."
            $ wait_for_opponent_choice()
            $ king_choice = opponent_action

        if king_choice == 1:
            $ favorability += 5
            hide oldsd
            show p2
            $ stream_hearts()
            crm "勇者宝宝的嗓音像叮咚的小铃铛(´〜｀*)一样脆呢～"
            $ stream_hearts()
            crm "敲♡在♡吾辈♡最♡柔♡软♡的地方～好听让吾辈站不稳呀"
            crm "♡但如果这声音呼唤了别人呀…"
            $ stream_hearts()
            crm "那吾辈也不介意让这铃铛只为吾辈响起呢♡呐♡～"
            $ stream_hearts()
            crm "吾辈超♡爱♡这♡种紧紧相依的感觉哟～"
            crm "爱到连自己都融化啦♡"
            $ stream_hearts()
            crm "♡但超幸福呀～吾辈就沉醉这种为宝宝♡撕♡裂♡一♡切♡的♡疯♡狂♡呀♡"
            
        elif king_choice == 2:
            $ favorability += 20
            $ stream_hearts()
            hide oldsd
            show p2
            crm "额的「勇者♡大♡人」今年19岁~♡"
            crm "年纪确实小✰爹摸呐"
            $ stream_hearts()
            crm "她在比你们更✰糟✰糕✰的环境中生存过「心智」也成·熟·的·多呐～"
            $ stream_hearts()
            crm "zako~不小心骂出口了♡牙白里…和你们这些♡杂♡鱼♡完全无法「相提并论」"
            crm "卡娜酒桑～甚至超越了吾辈喵、吾辈…甚至在某些方面很敬佩你们…"
            $ stream_hearts()
            crm "呜呜呜呜哇…红豆无法忍受了喵…"
            $ stream_hearts()
            crm "所有只会「玩旮旯给木」的社会败类♡败类♡杂鱼♡杂鱼♡啊！"
            $ stream_hearts()
            crm "真的是...吾辈希望你们…☆·尽快从「世界」消失"

    elif joint == 2:
        ela "短暂的恍惚后猛地摇头，理智重新占据上风"
        o "眼前的柔弱景象或许是假象，她是魔王，是必须被清除的威胁，是你加官进爵的筹码"
        ela "眼神冷了下来"
        ela "声音也带着公事公办的疏离"
        hide oldsd
        show p2
        if my_role == ROLE_KING:
            menu:
                "不要不要我要挠死你这个臭勇者":
                    $ king_choice = 1
                    $ make_sync_choice(1) 
                "不做任何抵抗":
                    $ king_choice = 2
                    $ make_sync_choice(2)
        else:
            o "等待魔王反应中..."
            $ wait_for_opponent_choice()
            $ king_choice = opponent_action

        if king_choice == 1:
            $ favorability -= 10
            show angry11
            crm "不要不要我要挠死你这个臭勇者"
            crm "捅死你喵"
            crm "捅死你喵捅死你喵"
            crm "捅死你喵捅死你喵捅死你喵"
            crm "捅死你喵捅死你喵捅死你喵捅死你喵"
            crm "捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵"
            crm "捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵捅死你喵"
            
        elif king_choice == 2:
            jump scene_kingdie

    jump scene_vindication

label judge2:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice()
    python:
        if my_role == ROLE_KING:
            king_choice = my_action
            hero_choice = opponent_action
        else:
            hero_choice = my_action
            king_choice = opponent_action

    if king_choice == 1 and hero_choice == 1:
        jump scene_die

    elif king_choice == 1 and hero_choice == 2:
        jump scene_die

    elif king_choice == 2 and hero_choice == 1:
        jump scene_die

    elif king_choice == 2 and hero_choice == 2:
        o "勇者打败了魔王,把魔王拿去皇宫请赏。"
        jump scene_kingdie

label scene_die:
    scene jk3 with dissolve
    o "勇者死在了魔王的法力之下"
    show kingking
    show emm11
    o "感谢你为王国作出的牺牲"
    king "难道,真的没有人能打败魔王了吗?"
    o "获得一个印章"
    return

label scene_palace_2:
    scene palace with dissolve
    o "勇者住在了魔王的宫殿"
    scene firefire with dissolve
    o "寝宫,壁炉的火光摇曳"
    scene palace with dissolve
    o "勇者坐在柔软的地毯上,略显拘谨"
    o "魔王扎着围裙,笑吟吟地端来一盘烤得焦香的鱼和一杯冒着气泡的琥珀色苹果酒"
    o "她毛茸茸的尾巴尖,正有一下没一下地轻轻扫过勇者的后颈"
    show p2
    $ stream_hearts()
    crm "来,这是本宝宝亲自下厨为你准备的,可要心怀感激地吃完哦"
    crm "比起那些把你丢在这里不闻不问,恐怕早已将你遗忘的王都大人物们,我是不是体贴多了喵?"
    hide p2
    show oldsd

    # --- 第一步：勇者决定怎么对待食物 ---
    if my_role == ROLE_HERO:
            menu:
                "谁要吃你的东西呀,好羞耻,掀翻了掀翻了":
                    $ joint = 1
                "嘻嘻魔王大人最好啦我要一辈子当我魔王大人的宠物":
                    $ joint = 2
                "假装没看见":
                    $ joint = 3
            $ make_sync_choice(joint)
    else:
        o "等待对方选择中"
        $ wait_for_opponent_choice()
        $ joint = opponent_action


    if joint == 1:
        if my_role == ROLE_KING:
            menu:
                "狠狠地惩罚勇者":
                    $ king_choice = 1
                    $ make_sync_choice(1)
                "大人不记小人过":
                    $ king_choice = 2
                    $ make_sync_choice(2)
        else:
            o "等待魔王反应..."
            $ wait_for_opponent_choice()
            $ king_choice = opponent_action

        if king_choice == 1:
            $ favorability -= 30
            o "魔王看着一地狼藉,脸上的笑意非但没有消失"
            o "反而变得更加深邃和……危险"
            o "她非但没有生气,眼中还燃起了兴奋的火光"
            hide oldsd
            show p2
            show water11
            crm "仿佛看到了最有趣的玩具"
            crm "轻轻舔了舔嘴唇,向前逼近一步"
            crm "看来驯服不听话的小狗,光靠喂食是不够的"
            crm "本王可是,狠狠的期待着你反抗的样子呢"
            crm "弄脏本王的地毯,浪费本王的心意"
            crm "这笔账,我们得好好算算"
            crm "惩罚游戏,现在开始"
            jump scene_vindication_sp
            
        elif king_choice == 2:
            $ favorability += 15
            hide oldsd
            o "面对一地的狼藉和勇者那副“快生气啊”的挑衅表情,魔王先是一愣"
            o "随即“噗嗤”一声笑了出来"
            show p2
            show happy11
            crm "哎呀呀,这算什么？打翻狗食盆吗？真是幼稚得要命"
            crm "好啦好啦,本王大人不记小人过"
            crm "知道你害羞,但这种像小孩子一样撒娇的方式"
            crm "可一点都不可爱哦？"
            crm "不过,勉强也算是一种进步吧"
            crm "哦呵呵呵呵"
            jump scene_vindication_sp

    elif joint == 2:
        $ favorability += 20
        hide oldsd
        show p2
        show happy11
        crm "勇者也会撒娇呢好可爱www"
        crm "哦呀?我们讨伐魔物的英雄大人,原来这么纯情的nyan?"
        jump scene_vindication_sp

    else:
        show water11
        ela "唉算了戏耍下魔王大人"
        ela "略略略~谁要理你这个坏心眼的魔王啊,烤鱼归我啦"
        if my_role == ROLE_KING:
            menu:
                "喂,你怎么不理我!":
                    $ king_choice = 1
                    $ make_sync_choice(1)
                "用尾巴甩到勇者脸上":
                    $ king_choice = 2
                    $ make_sync_choice(2)
                "谁鸟你啊":
                    $ king_choice = 3
                    $ make_sync_choice(3)
        else:
            o "等待魔王反应..."
            $ wait_for_opponent_choice()
            $ king_choice = opponent_action

        if king_choice == 1:
            $ favorability += 40
            o "就在魔王因勇者的无视而微微愣神的瞬间,勇者突然动了!"
            ela "以迅雷不及掩耳之势放下餐具,一手揽过她的腰"                    
            ela "另一只手托住她的后脑,带着烤鱼的香气霸道地吻了上去"
            hide oldsd
            show p2
            crm "瞳孔骤然放大,发出一声短促的呜咽,随即猛地将你推开"
            $ stream_hearts()
            crm "你、你这个无礼之徒！竟敢偷袭本王！"
            crm "她一把抓过旁边的羽毛枕头,像挥舞战锤一样,结结实实地拍在了你的脸上"
            ela "不好,为什么这么舒服。。。"
            
        elif king_choice == 2:
            $ favorability += 20
            $ stream_hearts()
            ela "魔王尾巴尖扫过的触感让你耳根发烫"
            ela "那句“被遗忘”的调侃更是戳中了你的心事"
            ela "猛地低下头,试图用刘海遮住自己通红的脸颊"
            
        elif king_choice == 3:
            $ favorability -= 50
            ela "感觉被冷落了"

        jump scene_vindication

#审判前奏
label scene_vindication:
    scene jk2 with dissolve
    o "随着相处时间的增加,勇者和魔王二人越来越默契"
    o "勇者也发现,魔王其实根本不需要讨伐"
    o "所谓的魔王,只是一个王国统治者害怕统治危机的借口吗？"
    ela "三十年一次的红月之日到来,你发现魔王的力场波动变得越发奇怪"
    crm "随着红月之日的到来,你体内的封印逐渐压制不住"
    o "有一天,来了一位老奶奶,手上提着一个铜质茶壶。"
    show grmd
    gny "我看到了,这只小狐狸将会在未来面临巨大的危机"
    gny "他身上有来自远古的封印"
    gny "如果不及时破除,就会带来巨大的威胁"
    gny "这也是王国始终要讨伐他的原因"
    gny "一旦封印也无法被压制,就会爆发出巨大的力量"
    gny "我手上的这个茶壶,可以通过魔法吟唱"
    gny "来压制封印的力量"
    o "这个时候,又有新的勇者来讨伐魔王了！"
    if my_role == ROLE_HERO:#一个人选另一个不动
            menu:
                "和魔王抱在一起" if favorability > 50:#好感大于70才显示，不然没得选，只有下面这个
                    $ joint = 1
                "尝试向新来的的勇者解释这一切":
                    $ joint = 2
                "把新来的勇者掀翻":
                    $ joint = 3
            $ make_sync_choice(joint)
    else:
        o "等待对方选择中"
        $ wait_for_opponent_choice()
        $ joint = opponent_action

    if joint == 1:
        hide grmd
        show newds
        sb "你这是背叛,今天我要杀死你"
        o "面对新勇者的指责"
        hide newds
        show oldsd
        ela "和魔王对视了一眼,竟从彼此眼中看到了一丝默契的笑意"
        ela "没有辩解,反而转身,毫不犹豫地将魔王揽入怀中"
        hide oldsd
        show p2
        $ stream_hearts()
        crm "顺势依偎在勇者胸口,脸上带着胜利者的微笑"
        ela "你说得对,我们就是在一起了"
        ela "所以,你可以回去了。告诉王国,这个魔王,由我独家讨伐"
        show steam11
        crm "听见了吗？小笨蛋,这里不欢迎你哦"
        hide p2
        show newds
        show angry11
        sb "你……你们……不知廉耻！这是对全体勇者的背叛！啊啊啊——！"
        sb "我一定要杀死你们两个"
        ela "忍无可忍,把这个菜鸡掀翻了"
        ela "实力也不过如此呀.还是比我差远了"
        if my_role == ROLE_KING:
            menu:
                "和勇者接吻":
                    $ joint = 1
                "略微出手":
                    $ joint = 2
            $ make_sync_choice(joint)
        else:
            o "等待对方选择中"
            $ wait_for_opponent_choice()
            $ joint = opponent_action
        if joint == 1:
            jump scene_sp
        else:
            jump scene_defection
    elif joint == 2:
        if favorability>=50:
            hide grmd
            o "新的勇者看你们二人情真意切，相信了你说的话，离开了"
            o "在你解释的过程中，魔王静静地走到你身边，没有插话"
            o "只是用温柔而坚定的目光看着你"
            o "她的信任与默契，无声地印证了你的话"
            show newds
            show steam11
            sb "看着你们二人之间情真意切的互动，表情从愤怒转为困惑，最后叹了口气"
            sb "罢了。看来这其中确有隐情"
            sb "前辈，你好自为之"
            sb "收起剑，带着复杂的表情离开了"
            $ favorability += 40
            jump scene_battlefield
        else:
            hide grmd
            show oldsd
            ela "解释苍白无力.回头看魔王，想寻求佐证时"
            hide oldsd
            show p2
            show sub11
            crm "故意露出了一个高深莫测的邪恶笑容"
            hide p2
            show newds
            show angry11
            sb "谎言！你还想骗我！看来你已经被魔王的邪术彻底控制了"
            sb "我今天就要为民除害"
            hide newds
            show oldsd
            ela "心中一股无名火起，最讨厌这种不分青红皂白就给人定罪的“正义”"
            ela "懒得废话，一个箭步上前，用娴熟的战斗技巧瞬间将他制服在地，剑尖抵住了他的喉咙"
            ela "荣耀？你连敌我实力都分不清，也配谈荣耀？滚回去再练十年"
            hide oldsd
            show newds
            show angry11
            sb "狼狈不堪，眼神中充满怨恨"
            sb "你…你竟然…好！你给我等着！"
            sb "连滚带爬地逃走了"
            jump scene_defection
    else:
        jump scene_defection

#小情侣结局
label scene_sp:
    scene jk3 with dissolve
    o "新勇者看着你们亲密无间的样子,身体开始剧烈颤抖"
    o "他想象中的邪恶契约、精神控制全都不存在"
    o "眼前只有一对公然“秀恩爱”的狗女同"
    o "这种超越他理解范围的现实,彻底摧毁了他的世界观"
    show newds
    show sub11
    sb "哈哈哈……原来如此……什么讨伐魔王,什么正义……全都是笑话！我最崇拜的前辈,竟然……竟然……"
    sb "举起剑"
    sb "状若癫狂，泪流满面"
    sb "把剑架在了自己的脖子上"
    sb "以我之血,诅咒你们！这污秽的世界,这背叛的信仰……我……不承认!我不接受!"
    o "血光闪过,一场闹剧以最惨烈的方式收场。"
    o "所以,我们要少玩点旮旯给木,花点时间去陪你重要的人"
    o "获得五个印章"
    return

#勇者恶堕结局
label scene_defection:
    scene palace with dissolve
    o "勇者打败了新的勇者，被整个王国通缉"
    o "新勇者逃回王国，将你勇者“彻底堕落”的消息添油加醋地汇报"
    o "很快，通缉令传遍大陆，你从“被俘的英雄”变成了“魔王的走狗”"
    show oldsd
    show sub11
    ela "站在魔王城的尖顶上，看着远方的王都，心中五味杂陈"
    hide oldsd
    show p2
    crm "轻轻握住你的手，语气带着一丝戏谑和坚定"
    $ stream_hearts()
    crm "这下，全世界都知道你是我的人了。后悔吗，我的勇者大人？"
    hide p2
    show oldsd
    ela "我从来都没有后悔过"
    ela "沉溺于逃亡和魔王的宠爱中无法自拔，渐渐放弃了人类身份"
    o "如果给你一次重来的机会，你还会坚定地踏上这条路吗？"
    o "获得两个印章"
    return


#审判前奏_sp
label scene_vindication_sp:
    scene jk2 with dissolve
    o "随着相处时间的增加,勇者和魔王二人越来越默契"
    o "勇者也发现,魔王其实根本不需要讨伐"
    o "所谓的魔王,只是一个王国统治者害怕统治危机的借口吗？"
    ela "三十年一次的红月之日到来,你发现魔王的力场波动变得越发奇怪"
    crm "随着红月之日的到来,你体内的封印逐渐压制不住"
    o "有一天,来了一位老奶奶,手上提着一个铜质茶壶。"
    show grmd
    gny "我看到了,这只小狐狸将会在未来面临巨大的危机"
    gny "他身上有来自远古的封印"
    gny "如果不及时破除,就会带来巨大的威胁"
    gny "这也是王国始终要讨伐他的原因"
    gny "一旦封印也无法被压制,就会爆发出巨大的力量"
    gny "我手上的这个茶壶,可以通过魔法吟唱"
    gny "来压制封印的力量"
    jump scene_battlefield


#坏结局：魔王死了
label scene_kingdie:
    scene jk3 with dissolve
    show kingking
    king "威胁王国安全的魔王终于被捕获了"
    king "勇者,我会履行我的诺言"
    king "你将会得到我曾对你许诺的一切"
    o "魔王被关进了监狱"
    o "勇者拿到了封赏"
    o "但是很快就有新的魔王需要勇者前往讨伐"
    king "我相信你,这次的讨伐,就交给你了"
    hide kingking
    show oldsd
    show happy11
    ela "感谢国王陛下的赏识"
    ela "我一定会完成这次任务"
    o "勇者就在一次次讨伐中加官晋爵"
    o "成为了国王的左膀右臂"
    o "获得两个印章"
    return

label scene_battlefield:
    scene jk3 with dissolve
    o "风波平息，老奶奶凑了上来"
    show grmd
    gny "怎么样，你们想好了吗？"
    if my_role == ROLE_HERO:
        jump scene_palace_knight_3
    else:
        jump scene_palace_king_3

label scene_palace_king_3:
    scene palace with dissolve
    menu:
        "我相信她":
            $ my_action = 0
            jump judge3
        "好假哦能不能说得真一点":
            $ my_action = 1
            jump judge3

label scene_palace_knight_3:
    scene palace with dissolve
    menu:
        "我相信她":
            $ my_action = 0
            jump judge3
        "好假哦能不能说得真一点":
            $ my_action = 1
            jump judge3

label judge3:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice()
    python:
        if my_role == ROLE_KING:
            king_choice = my_action
            hero_choice = opponent_action
        else:
            hero_choice = my_action
            king_choice = opponent_action

    if king_choice == 0 and hero_choice == 0:
        jump scene_cup

    elif king_choice == 1 and hero_choice == 0:
        jump scene_lie

    elif king_choice == 0 and hero_choice == 1:
        jump scene_lie

    elif king_choice == 1 and hero_choice == 1:
        jump scene_suspection

#两个人都相信了老奶奶说的话
label scene_cup:
    scene jk2 with dissolve
    o "在红月之夜，魔王力量失控"
    o "王国发兵讨伐魔王,军队踏入宫殿，他们发现魔王并没有那么强"
    o "而勇者背叛王国，罪也该死"
    o "经过激烈的战斗，魔王奄奄一息"
    show p2
    crm "倒在一旁，鲜血从嘴角流出"
    if my_role == ROLE_HERO:#一个人选另一个不动
        menu:
            "我无能为力......生而为人，我很抱歉":#好感大于70才显示，不然没得选，只有下面这个
                $ joint = 7
            "使用茶皿进行魔法吟唱":
                $ joint = 8
        $ make_sync_choice(joint)
    else:
        o "等待对方选择中"
        $ wait_for_opponent_choice()
        $ joint = opponent_action
    if joint == 7:
        jump scene_palace
    elif joint == 8:
        if favorability >=90:
            jump scene_harmony
        else:
            jump scene_untie

label scene_lie:
    scene jk3 with dissolve
    o "在红月之夜，魔王力量失控"
    o "王国发兵讨伐魔王,军队踏入宫殿，他们发现魔王并没有那么强"
    o "而勇者背叛王国，罪也该死"
    o "经过激烈的战斗，魔王奄奄一息"
    show p2
    crm "倒在一旁，鲜血从嘴角流出"
    if my_role == ROLE_HERO:#一个人选另一个不动
        menu:
            "我无能为力......生而为人，我很抱歉":#好感大于70才显示，不然没得选，只有下面这个
                $ joint = 9
            "我不忍心看着她死去！要死的话，就让我先死吧！":
                $ joint = 0
        $ make_sync_choice(joint)
    else:
        o "等待对方选择中"
        $ wait_for_opponent_choice()
        $ joint = opponent_action
    if joint == 9:
        jump scene_palace
    elif joint == 0:
        if favorability >=90:
            jump scene_alive
        else:
            jump scene_fright


#假好结局
label scene_untie:
    scene jk2 with dissolve
    o "吟唱不算成功，但是两人脱离了危机"
    show kingking
    show steam11
    king "被深深触动"
    king "看来魔王什么的，也不过如此啊"
    o "获得一个印章"
    return

#唯一好结局
label scene_harmony:
    scene palace with dissolve
    o "魔王破解了封印和人们的偏见"
    o "暴君的统治被推翻。勇者和魔王也幸福地生活在一起"
    show p2
    $ stream_hearts()
    crm "若是能够一直待在这样的怀抱里"
    crm "当不成那威风凛凛、令众生敬畏的魔王"
    crm "就仅仅做个被勇者宠溺着的小狐狸，似乎也并不是一件坏事"
    hide p2
    show oldsd
    ela "这种温暖与安心，是我在漫长岁月里从未体会过的珍贵"
    ela "我爱你"
    $ stream_hearts()
    o "热吻"
    o "情感是可以跨越时空的"
    o "感谢游玩！！"
    o "获得五个印章"
    return

#勇者牺牲自己救魔王结局
label scene_alive:
    scene jk3 with dissolve
    o "勇者牺牲了自己的身体，魔王的爆发力量滚入勇者的身体"
    show oldsd
    ela "忍受身体的剧痛"
    ela "呃啊"
    ela "替我...活下去"
    scene black
    pause 1.0
    scene jk3 with dissolve
    o "过了很长时间"
    ela "（醒来）我在哪"
    show p2
    crm "你醒了？"
    ela "（点头）"
    crm "他们都被我打跑了，我厉害吧"
    crm "（身上伤痕累累）嗯，现在，我已经不是魔王了"
    crm "因为我让普通人承受了来自非人的力量，这是神的诅咒"
    crm "至少你还在我身边，我不会孤单"
    hide p2
    show oldsd
    show rush11
    ela "（大哭）我们，我们回家"
    o "夜深了，两人牵手走向远方"
    scene sr with dissolve
    o "获得四个印章"
    return

#杀死魔王结局
label scene_fright:
    scene jk3 with dissolve
    crm "别管我，快走"
    crm "（把勇者推开）"
    ela "失去意识"
    scene black
    pause 0.5
    scene jk3 with dissolve
    show oldsd
    ela "你是谁？"
    crm "现在，杀了我"
    ela "？"
    hide oldsd
    show p2
    crm "现在，杀了我！！"
    o "勇者醒了过来"
    scene jk3 with dissolve
    show kingking
    king "很好，我的勇者，你用行动证明了你的忠诚"
    ela "（可是我？！？！？！？！？）"
    o "获得一个印章"
    return


label scene_suspection:
    scene jk3 with dissolve
    show oldsd
    ela "别说那么多有用没用的"
    ela "刚刚战斗的时候为什么不来帮忙?"
    hide oldsd
    show p2
    show water11
    crm "就是就是，这么冷漠，我们凭什么相信你?"
    hide p2
    show grmd
    show angry11
    gny "红温"
    gny "很红温"
    gny "非常红温"
    gny "你们两个懂不懂尊重老人？！？？！？"
    hide grmd
    o "老奶奶带开了茶壶，古神的力量如脱缰的野马喷涌而出"
    o "勇者和魔王被古神的力量撕碎了"
    o "尊老爱幼，人人有责"
    o "获得一个印章"
    return


label scene_1:
    scene plgrd with dissolve
    show screen radar_screen
    o "距离失恋已经一年过去了，你还是没法完全从中抽离"
    o "跑完了整整五公里，肺泡里满是冬月傍晚冰凉的空气，每次呼吸都在咽下西湖醋鱼的鱼骨"
    o "你停下来时，天空上演着一场盛大而无声的死亡"
    o "最后一抹橙光在被黯色的深渊缓缓濡湿，而后吞没"
    show qy
    p "真正的夜晚尚未到来，因为我还没感到由内而外的寒冷"
    o "路灯光线昏黄，像是得了某种顽疾，只能勉强照亮了脚下一小片塑胶跑道"
    o "更远的地方，则陷入暧昧不明的昏暗里"
    o "现在，你感觉你应该下定某种决心，你还没有出够门、透够气，只因你一天到晚都呆在宿舍，足不出户"
    o "你现在的感觉就像，晚上明明不悲伤、不焦虑却难以入眠，因为你声称自己享受孤独，又因惧怕今天就此过去而舍不得入眠"
    
    menu:
        "湖边散步":
            $ L += 2
            jump scene_1_1

        "回去躺尸":
            $ L += 1
            $ S += 1
            jump scene_1_2

label scene_1_1:
    scene willows with dissolve
    o "为了证明身体依旧是温暖的、活着的，你必须主动去触摸一些更冰冷的东西，但今晚似乎过于清寒"
    menu:
        "拥抱黑暗":
            $ L += 2

        "回去躺尸":
            $ L += 1
            $ S += 1
            jump scene_1_2
    o "湖边的路没有灯，落叶发出愤怒的碎裂声，桥洞下，黑暗粘稠得如同墨汁"
    show qy at walk32
    o "你凭借记忆，摸索到那块她曾说过的的石阶坐下"
    o "寒气瞬间穿透你的衣物，蛮横侵入你的骨骼，淙淙水声，在这片绝对的寂静里领衔主唱"
    o "像用一种永恒而固执的语调，反复咀嚼着同一段旧事"
    p "这水声源自桥洞底下的高低差，我记得她评价过此时此景，说的是"
    menu:
        "这是世界上最干净的声音，能把人的心都洗成透明的":
            $ H += 2
            $ F += 1
            jump scene_111
        "用外界的噪音来盖过自己的孤独而已":
            $ E += 1
            $ L += 1
            $ C += 1
            jump scene_112

label scene_111:
    o "不知何处传来歌声"
    o "若那凡人之魂也梦到了我，就让他因思念而苏醒吧"
    show rush11
    o "你感到一股混着悲伤与慰藉的平静，世界在你眼前化作了一片温柔而朦胧的灰白"
    $ my_plane = 2
    $ send_async_action(901)
    jump scene_2

label scene_112:
    o "不知何处传来歌声"
    o "一霎时把七情俱已磨尽，参到了酸辛处泪湿衣襟"
    o "这歌声让人想起安塞腰鼓，但好像不合时宜"
    show emm11
    o "你的理智开始崩解，视野中的黑暗附上噪点"
    $ my_plane = 2
    $ send_async_action(901)
    jump scene_2

label scene_1_2:
    scene doomroom with dissolve
    o "你时常自嘲这是阴雨霉湿之地"
    o "一个敞开的避难所，等待它的囚徒归笼"
    o "七点四十二分，夜色正好，窗边的你看到，楼下的路灯逸散出米黄色"
    show qy at walk32
    p "哪怕是盛夏，也只有十一点到三点之间才不必点灯，何况深秋呢"
    o "每次想和人探讨你的愁绪，却都担心被说是无病呻吟"
    menu:
        "找以前的朋友聊聊天吧":
            $ S += 1
            $ C += 1
            jump scene_121
        "自己写点发电小短文吧":
            $ C += 1
            $ H += 1
            jump scene_122

label scene_121:
    o "你向那份连接的渴望屈从了"
    o "你的手指在一个个熟悉又陌生的名字上悬停，而后点开了一个曾经关系挺好的朋友，聊天记录还停留在三个月前"
    o "反复输入，又反复删除"
    o "哪怕是盛夏，也只有十一点到三点之间才不必点灯，何况深秋呢"
    o "每次想和人探讨你的愁绪，却都担心被说是无病呻吟"
    show emm11
    p "我到底该说什么啊"
    menu:
        "在吗（但至少是个开始）":
            $ F += 1
            jump scene_123
        "实在还是无法鼓起勇气啊":
            $ L += 1
            jump scene_125

label scene_122:
    o "你是孤芳自赏的演奏家"
    o "你有去年坏掉的发条闹钟，无人分享的雪糕，清醒的孤独"
    o "似乎眼前的灰烬不如写遥远的星辰，美丽的神话"
    show emm11
    p "我到底该写什么啊"
    menu:
        "生活，死水泛不起半点涟漪":
            $ S += 1
            jump scene_124
        "陨石，自海平面向星空升起":
            $ L += 2
            $ C += 1
            $ my_plane = 3
            $ send_async_action(901)
            jump scene_3

label scene_123:
    o "你盯着屏幕，等待对方正在输入的提示"
    o "十分钟过去了，或许他真的在忙吧"
    o "你始终不相信其实是你们之间已经隔着一层叫时间的厚障壁了"
    o "你没有被任何人拒绝，却比任何时候都更感到被世界拒绝"
    o "世界顿时失去了拥有色彩的必要性"
    $ my_plane = 2
    $ send_async_action(901)
    jump scene_2

label scene_124:
    o "你向内塌陷，沉寂中达成了可悲的和解"
    o "墨色自显示屏晕开，整个世界都浸泡在这片无悲无喜的灰白之中"
    $ my_plane = 2
    $ send_async_action(901)
    jump scene_2

label scene_125:
    o "你向内塌陷，沉寂中达成了可悲的和解"
    o "夜色是漆黑的子弹，射向你的眉心，你沉沉睡去"
    $ my_plane = 3
    $ send_async_action(901)
    jump scene_3


label scene_13:
    scene doomroom with dissolve
    o "理性必然伴随着残酷，既然这是痛苦的根源，就应当被祓除"
    o "远处的白色巨蛋，花谢花飞花满天，就没了"
    o "所有执念都被彻底抹除了，你的面前，只摊开着一本空白的日记本"
    o "现在，你又如何，为这场空洞的胜利，书写新篇？"
    menu:
        "童话：珠泪哀歌":
            jump noname
        "传说：琴鸣天外":
            jump noname
        "窗外：梧桐叶落":
            jump tureman

label noname:
    o "你编织一个关于“人鱼公主泣泪成珠”的哀伤童话"
    o "或描绘一个关于“骑士魂归天外，琴声化作星辰”的浪漫神话"
    o "你可以是一个多愁善感的诗人，一个化腐朽为神奇的炼金术士"
    o "一个现实的囚徒，一匹永夜的天马"
    o "谨以你的文字献给一汪虚无的海，一座孤独的岛，一座无名的墓"
    o "达成HE：无名之墓，获得4个印章"
    return

label tureman:
    o "你平静地接受了这一切"
    o "色即是空，空即是色"
    o "你写下：十一月十三日。下午三点零四分。晴。风力三级，西北风。窗外梧桐，今日落叶三十七片"
    o "既然「现在」这件事情本身就乏善可陈，又何必美化呢"
    o "如果一个人悲伤时会做一些没有意义的事，那只是因为这个人生命没有意义"
    o "这才是悲伤呈现出的真相"
    o "达成TE：真的猛士，获得5个印章"

label scene_2:
    scene fractal_background
    pause 0.75
    scene eatingstreet_bw with dissolve
    o "你睁开眼，发现自己身处湖畔，但并非你常来的那一头"
    python:
        process_all_async_events()
    o "眼前，是一片灯火通明的夜市"
    o "无数摊位亮起灯来，光线强烈得有些刺眼，照亮了攒动的人头、琳琅的商品"
    show qy at walk32
    o "人们交谈，欢笑，打趣，但你听不到任何声音"
    o "听不到，并非距离太远，是因为世界本就是一座喧嚣的坟墓"
    o "如同花草自坟头新生，一个晴天娃娃赫然在目"
    o "它是此地唯一拥有色彩的东西，在非黑即白的世界里，称得上唯一的慰藉"
    scene empstreet with dissolve
    o "她望向你的瞬间，周围那片沉默的喧嚣消失了"
    show doll1
    show steam11
    doll "你，似乎是，外面来的人呢"
    show happy11
    p "欸？原来你会说话啊"
    doll "我看到，你的颜色，会说话"
    doll "你心里，有悲伤的，颜色，像被雨水打湿的，炭火，这是为什么呢"
    python:
        process_all_async_events()
    menu:
        "马孔多在下雨":
            $ favorability += 33
            $ show_up()
            if my_plane == opponent_plane:
                $ H += 2
            else:
                $ send_async_action(201)
            jump scene_201
        "一般路过男性":
            if my_plane == opponent_plane:
                $ E += 2
            else:
                $ send_async_action(202)
            jump scene_202


label scene_201:
    o "你选择拥抱示弱效应，企图从非活物身上找到怜悯，开始了讲述"
    python:
        process_all_async_events()
    o "一番长篇大论"
    hide doll1
    show qy
    p "我们最后走散了，我依然固执的相信还没有"
    hide qy
    show doll1
    show steam11
    doll "我的确能，在你身上，看到她的，颜色，那些颜色，不同样是，你，存在过的证明吗，能再多告诉我一些吗，关于，她的颜色"
    o "她似乎有些食髓知味了，你脑海中浮现出几段记忆"
    python:
        process_all_async_events()
    menu:
        "两人咖啡厅约会却一同迟到":
            if my_plane == opponent_plane:
                $ H += 1
                $ S += 1
            else:
                $ send_async_action(211)
            jump scene_211
        "两人约在小摊吃夜宵却遇骤雨":
            if my_plane == opponent_plane:
                $ H += 1
                $ F += 1
            else:
                $ send_async_action(212)
            jump scene_212
        "因你选的电影过于短促而被责怪":
            $ favorability += 33
            $ show_up()
            if my_plane == opponent_plane:
                $ E += 1
                $ H += 1
                $ C = 5
            else:
                $ send_async_action(213)
            jump scene_213
    return

label scene_211:
    p "一次，我们约在咖啡厅，结果两个人都迟到了几分钟。我们没有生气，反而笑着责怪对方"
    python:
        process_all_async_events()
    show happy11
    doll "真好，连小小的错误，都能被你们的规则所原谅"
    o "晴天娃娃的脸上的红晕短暂加深了"
    jump scene_214


label scene_212:
    p "下着大雨的夜晚，我们在路边小摊躲雨，吃着一份甜到发腻的糖画"
    python:
        process_all_async_events()
    show happy11
    doll "糖露，甜味，混着，湿衣服的霉味，尝到了，这颜色，很满"
    o "晴天娃娃的脸上的红晕短暂加深了"
    jump scene_214


label scene_213:
    p "我当时自作主张，选了一部文艺片，结果只有一个小时，她还没看够，就气鼓鼓地抱怨了我一路"
    python:
        process_all_async_events()
    show happy11
    doll "一场失败的约会啊，这个真的，好有意思，请多讲讲这种"
    jump scene_214

label scene_214:
    o "你们沉浸在这场共同修补过去的幻梦中"
    python:
        process_all_async_events()
    o "渐渐地，你发现美好回忆，似乎就那么几种，翻来覆去地讲，已经开始变得像褪色的照片"
    show water11
    doll "(带着一丝不耐烦)又是这个？这个颜色，我看过了。还有别的吗？"
    p "我……我们后来，大部分时间都很平淡"
    hide doll1
    show doll2
    doll "(尖锐)平淡？平淡就是‘无色’！我讨厌‘无色’!就和这里的世界一样无聊"
    show angry11
    python:
        process_all_async_events()
    menu:
        "你真的好烦，闹够了没有":
            $ show_down()
            $ favorability = 0
            if my_plane == opponent_plane:
                $ E += 1
                $ C += 1
            else:
                $ send_async_action(2141)
            jump scene_2141
        "可生活本身，就大多是平淡如水的啊":
            $ show_up()
            $ favorability += 33
            if my_plane == opponent_plane:
                $ H += 1
                $ F = 10
            else:
                $ send_async_action(2142)
            jump scene_2142 

label scene_2141:
    hide doll2
    o "晴天娃娃所有的色彩瞬间褪尽，融入了这个世界原本的样子"
    python:
        process_all_async_events()
    o "你将对过去的愤怒，倾泄在了这个由过去构筑的幻影身上"
    o "你亲手，将自己唯一的慰藉，重新变回了垃圾"
    o "整个黑白街道，在这句充满憎恨的话语中，开始剧烈地颤抖、崩塌"
    if favorability >= 90:
        o "不过好在你攻略了ta"
    jump final_judgment

label scene_2142:
    show rush11
    o "晴天娃娃焦躁的神情，第一次变得平静、甚至有些悲伤"
    python:
        process_all_async_events()
    o "是吗，原来，这就是，重蹈覆辙的颜色啊，我，记下了"
    o "她身上的色彩，连同她自己，都化作了温暖的光点，消散在空气中"
    o "随着她消失，整个黑白世界开始如同潮水般退去"
    if favorability >= 90:
        o "不过好在你攻略了ta"
    jump final_judgment


label scene_202:
    hide doll1
    show doll2
    o "晴天娃娃那两点樱桃般的红晕完全消失了"
    show water11
    python:
        process_all_async_events()
    doll "是吗，这位先生，你的话，似乎有，无聊的，颜色，不如，随我逛逛吧"
    scene baituan with dissolve
    show doll2
    o "话音刚落，你们来到了一条拥挤的长街上"
    o "周围全是黑白鬼影般的“学生”，在机械地派发着空白的传单"
    o "离你们最近的是一个挂着“真理与言语艺术社”的摊位前停下"
    o "摊位后，正反双方端坐着，神情严肃，比划着手势，嘴巴无声地开合"
    show steam11
    doll "这种，永远，传达不到的，思想，你，怎么看"
    python:
        process_all_async_events()
    menu:
        "辩论是一个人少年时代最后的英雄主义":
            $ show_up()
            $ favorability += 33
            if my_plane == opponent_plane:
                $ H += 2
            else:
                $ send_async_action(221)
            jump scene_221
        "真理可能出现在任何地方，唯独不可能是辩论赛场":
            $ show_up()
            $ favorability += 33
            if my_plane == opponent_plane:
                $ E += 2
            else:
                $ send_async_action(222)
            jump scene_222

label scene_221:
    show happy11
    doll "英雄主义desuwa，沉默，原来，也可以是一种，所谓的英雄啊"
    jump scene_223

label scene_222:
    show water11
    doll "（似乎意有所指）说得，也是。毕竟，说真话，需要，勇气"
    jump scene_223

label scene_223:
    o "后来，你们走过只有拜厄练习曲的古典音乐社，只挂满五十音图的日语社"
    python:
        process_all_async_events()
    o "无论你回答什么，娃娃都是轻轻晃动一下，表示了解"
    scene bsktb with dissolve
    o "最终你们走到篮球场旁，场地中央，一个穿着球衣的身影正在进行投篮表演"
    o "篮球从他手中飞出，划过完美的抛物线，空心入网后，自动弹回他的手中"
    show doll2
    show emm11
    doll "一根筋，自以为是，自诩新时代的西西弗斯，有点让人，不爽"
    python:
        process_all_async_events()
    menu:
        "上前夺走篮球，打破这个循环":
            $ show_up()
            $ favorability += 33
            if my_plane == opponent_plane:
                $ C += 1
                $ H += 1
            else:
                $ send_async_action(231)
            jump scene_231
        "不敢轻举妄动":
            $ show_up()
            $ favorability += 33
            if my_plane == opponent_plane:
                $ S += 1
            else:
                $ send_async_action(232)
            jump scene_232

label scene_231:
    o "你无法忍受这份死寂的完美，上前夺走了篮球"
    python:
        process_all_async_events()
    o "整个场地，都像被打碎的玻璃一样，瞬间化为了碎片消失"
    show steam11
    doll "你似乎，更喜欢，意外"
    jump scene_23

label scene_232:
    o "你只是静静地看着完美的抛物线不断被重复，就像你一次次重复想起记事时那些心碎的时刻"
    python:
        process_all_async_events()
    o "整个场地，都像被打碎的玻璃一样，瞬间化为了碎片消失"
    show steam11
    doll "原来，你，更喜欢安稳呢"
    jump scene_23

label NoLonely:
    scene sakura with dissolve
    show qy
    o "许多年之后，望着花园里那棵开得如同云霞般的樱花树时"
    o "总会回想起，那个决定了你后半生命运的夜晚"
    show steam11
    o "就在那个夜晚，分裂的灵魂同时抵达了两条河流的尽头，于是第二天，你收到了一封空白的信"
    o "在你准备收起的时候，那封原本没有字迹的信上，开始浮现出如同泪痕般的字迹"
    o "那是许多年之后，你未来的妻子，写给你的一封情书"
    o "信上说，她爱你，爱你的沉默，爱你的笨拙"
    o "爱你会在某个普通的午后，突然对她说起一个关于晴天娃娃和美杜莎的、荒诞不经的梦"
    o "纠缠了你前半生的那场漫长的告白，更应与此刻的自己言说"
    o "达成隐藏真结局：百年不孤独（理论触发概率最低），获得5个印章"
    o "同伴也获得5章且接下来一组无视结局获得5个章"
    return

label scene_23:
    python:
        process_all_async_events()
    scene empstreet with dissolve
    o "你们走过了长街的尽头，现在你只感觉天地间之后你和这个娃娃"
    show doll2
    show emm11
    doll "真实的话语，伤人，真实的色彩，消逝，费尽心机，维持的，又有什么意义"
    doll "先生，你收集了这么多的真实，但你自己的那个真实呢"
    python:
        process_all_async_events()
    o "谨慎选择"
    menu:
        "对不起，我撒谎了":
            $ show_up()
            $ favorability += 33
            if my_plane == opponent_plane:
                $ E -= 1
                $ H += 1
            else:
                $ send_async_action(233)
            jump scene_233
        "我不知道你在说什么":
            $ show_down()
            $ favorability -= 33
            if my_plane == opponent_plane:
                $ E += 2
            else:
                $ send_async_action(234)
            jump scene_234

label scene_233:
    python:
        process_all_async_events()
    o "卸下伪装，你如释重负"
    show steam11
    doll "（长叹一口气）欢迎回来，先生，可惜这里，还是，要崩塌了呢"
    show rush11
    if favorability >= 90:
        o "不过好在你攻略了ta"
    jump final_judgment

label scene_234:
    o "将谎言进行到底"
    show angry11
    doll "（冰冷）是吗？"
    o "她身上的所有色彩，在这一瞬间全部熄灭了，溶解在了湖水与夜色黑与更黑的界限间"
    $ send_async_action(888)
    jump be2_mars_heart


label scene_3:
    scene fractal_background
    pause 1.5
    scene tearoom with dissolve
    o "墙壁在磷光照耀下液化重构，不禁使你产生一种异样的感觉，一种厄运降临的感觉"
    python:
        process_all_async_events()
    o "你跪坐在一间日式茶室，空气混着湿润的泥土、腐败的竹叶和龙涎香的气味"
    o "室内的陈设朴素到了极致"
    o "墙上悬挂着一幅只有浓淡变化的墨迹、看不出具体物象的挂轴"
    o "角落里，一只黑色铁壶在炭火上发出如同呼吸般的嘶声，逸散出些许雾气"
    o "朴素与典雅在此达成了令人不安的平衡"
    o "似乎有无数道目光，正从墙壁的缝隙、挂轴的墨迹、甚至熏香的烟雾中凝视着你"
    python:
        process_all_async_events()
    menu:
        "推开障子门出去":
            jump scene_301
        "静候此地主人出现":
            $ show_up()
            $ favorability += 25
            $ my_action = 1
            if my_plane != opponent_plane:
                $ send_async_action(302)
            jump scene_302

label scene_301:
    o "你无法忍受这份被窥伺的感觉，站起身，膝盖因久跪而有些麻木"
    python:
        process_all_async_events()
    show qy at walk32
    o "你缓缓走向那扇障子门，指尖在纸质的门面上，感受到一种如同干燥蛇蜕般的触感"
    o "你轻轻将门拉开一条缝"
    scene opendoor_resized with dissolve
    o "门外，是一片附上蛇鳞的竹子构成的幽深庭院"
    o "月光惨白，将竹影投射在地上，如同无数扭曲的骸骨"
    o "庭院里散落着几尊栩栩如生的人类石像"
    o "就在离门不到三尺的地方，一位身着华美和服的女性，正背对着你，静静地伫立着"
    o "她那头蠕动的黑发，微微停顿了一下，缓缓地、转过身来"
    scene tearoom with dissolve
    show mdsN
    python:
        process_all_async_events()
    menu:
        "你是何人(出言不逊)":
            $ my_action = 2
            if my_plane == opponent_plane:
                $ E += 2
            else:
                $ send_async_action(303)
            jump scene_303
        "冒昧打扰，实在抱歉(礼貌待人) ":
            $ show_up()
            $ favorability += 25
            $ my_action = 1
            if my_plane == opponent_plane:
                $ H += 2
            else:
                $ send_async_action(304)
            jump scene_303

label scene_302:
    show qy
    o "你选择了静观其变，你重新跪坐好，努力让自己的呼吸变得平稳，试图融入这间茶室的静寂之中"
    python:
        process_all_async_events()
    o "时间，在这里仿佛失去了意义"
    show steam11
    o "快被那熏香同化时，才发现身后的障子门不知何时已经打开，因为你感到身后的夜有些冷意"
    o "你猛地回头，看到一位身着华美和服的女性，正端着茶盘，优雅地跪坐在门口"
    hide qy
    show mdsN at walk32
    o "她的双眼被布条蒙住，你无法判断她究竟来了多久，又看了你多久"
    medusa "客人，久等了"
    o "她的声音如同外面的庭院，美丽而冰冷，而你的沉默与等待，本身就是一种礼貌"
    jump scene_303

label scene_303:
    medusa "你似乎并不诧异，我为何不在那智慧女神的盾牌之上"
    python:
        process_all_async_events()
    medusa "嘛，已是前尘往事，莫要再念，随我出去吧，你本不该属于此地"
    scene carridor with dissolve
    show screen radar_screen
    o "你跟在她身后走出茶室，小心避开那些姿态各异的石像"
    o "你们来到一处偏院——一片巨大的平庭式枯山水"
    scene kss with dissolve
    o "洁白的砂石耙出层层叠叠的波纹，如凝固的海洋；几块形态各异的蓝闪石片岩，如海上的孤岛，点缀其中"
    o "整个庭院却因太过完美，像一具精心装扮过的尸体"
    show mdsN at walk32
    medusa "此地无水，却处处是水。此地无物，却包罗万象"
    medusa "客人，你喜欢日本文化吗？"
    menu:
        "乐意之至":
            $ L = L
            $ show_up()

        "完全无感":
            $ L = L
        "略知一二":
            $ L = L
    medusa "喜欢与否，于我而言不重要"
    medusa "毕竟万事万物，就像那祇园精舍之钟声，奏诸行无常；沙罗双树之花色，表盛者必衰"
    o "她转向你，似乎在等着接话"
    python:
        process_all_async_events()
    menu:
        "骄者必败，恰如春宵一梦":
            $ show_up()
            $ favorability += 50
            if my_plane == opponent_plane:
                $ S += 1
            else:
                $ send_async_action(331)
            jump scene_331
        "猛者逐灭，好似风前之尘":
            $ show_up()
            $ favorability += 25
            if my_plane == opponent_plane:
                $ C += 1
                $ E += 1
            else:
                $ send_async_action(333)
            jump scene_333
        "星野分处之竹篁，泄半点幽微":
            $ show_up()
            $ favorability += 50
            $ C = 5
            if my_plane == opponent_plane:
                $ F += 1
            else:
                $ send_async_action(332)
            jump scene_332

label scene_331:
    show happy11
    medusa "看来你曾经读过，有点意思"
    jump scene_34

label scene_332:
    show happy11
    medusa "不谈败落，反言及景致，是不是有些留恋此地了呢"
    jump scene_34

label scene_333:
    show emm11
    medusa "(沉默片刻) 你不仅读过，而且还特意跳过了中间那句"
    o "你感到一阵心悸，还想辩驳些什么，却被她轻轻抬手打断了"
    jump scene_34

label scene_34:
    scene carridor with dissolve
    o "她不再言语，转身引领你穿过回廊，回廊尽头豁然开朗，你们走到了主庭院"
    python:
        process_all_async_events()
    scene tingzhong with dissolve
    o "一棵不应在此时盛开的樱树，正肆意地挥洒着惨白的烂漫"
    o "树下，一片明灭不定的萤火虫，如同流动的星尘，在草地上缓缓漂浮"
    o "冷月高悬下，更多被石化的人在月光中镀上银边"
    o "或面目狰狞，或神情惊恐，或异常宁静"
    o "他们是你沉默的观众"
    show mdsN
    medusa "虽是秋夜，此情此景，却让我想起一句春夜的古话——不似明灯照，又非暗幕张"
    medusa "（缓缓地转向你）客人，面对此番光景，你，又看到了什么"
    python:
        process_all_async_events()
    menu:
        "我看到……山谷明月光，流萤皆彷徨（重点在迷途之人）":
            if my_action == 1:
                $ show_up()
                $ favorability += 25
                $ E -= 1
                $ F = 10
                if my_plane != opponent_plane:
                    $ send_async_action(3411)
            if my_action == 2:
                $ C += 1
                $ my_action = 1
                if my_plane != opponent_plane:
                    $ send_async_action(3412)
            jump scene_34x

        "我看到……天也醉樱花，云脚乱蹒跚（重点在岔开话题）":
            if my_action == 1:
                $ my_action = 2
                $ E += 1
                if my_plane != opponent_plane:
                    $ send_async_action(3421)
            if my_action == 2:
                $ show_down()
                $ favorability -= 25
            jump scene_34x
        "我看到……皓月东升入碧穹，并非怀有待何情（重点在有心事）":
            if my_action == 1:
                $ my_action = 3
                $ show_down()
                $ favorability -= 25
                $ L += 1
            if my_action == 2:
                $ my_action = 3
                $ show_up()
                $ favorability += 25
            jump scene_34x

label scene_34x:
    python:
        process_all_async_events()
    if my_action == 1:
        if H >= 6 and favorability >= 90:
            o "她转向那些沉默的石像，又转向那些明灭的流萤"
            show rush11
            hide mdsN
            show mdsM
            medusa "腐草为萤，死而复生，轮回报业吗"
            o "良久，她缓缓地从和服袖中，取出了一面边缘雕刻着蛇纹的铜镜"
            o "她将镜面对准自己，蒙眼的布条无声滑落"
            o "当你再次睁开眼时，美杜莎已经变成了一尊精美绝伦的石像，方才的镜子掉在了地上"
            scene cells_bg with dissolve
            pause 1.0
            scene tingzhongout with dissolve
            o "庭院中所有石像，化作了无数光点，如萤火般升起，汇入夜空"
            medusa "曼珠沙华开簇簇，正是吾身安睡处"
            o "院门打开了，这句亡语，证明美杜莎被你成功攻略了"
            menu:
                "捡起镜子对准自己（想知道蛇女究竟是什么心境）":
                    jump final_judgment
                "捡起镜子离开（此地不宜久留）":
                    jump final_judgment
        elif H < 5:
            show emm11
            o "美杜莎听完你的话，发出了一声愉悦、冰冷的轻笑"
            medusa "伪善者的慈悲，总比恶人的坦诚，更让我着迷"
            medusa "一曲清歌钗半股，此生何处不相逢"
            medusa "你知道吗？其实你和我呀，是同类"
            medusa "一个用石头封印恶，一个用语言掩饰恶。我们都是，邪恶的混蛋呢"
            o "通往前路的大门，在你面前敞开，门后似乎是更深的黑暗"
            jump final_judgment
        else:
            show angry11
            o "她对你的暗示，报以冰冷的沉默"
            hide mdsN
            show qy
            show rush11
            o "她缓缓抬起手，你感到一股无形的压力将你笼罩"
            o "庭院的角落里，你瞥见一把锈迹斑斑的武士刀"
            menu:
                "握紧手中的武器，塔塔开！（高危动作）":
                    jump not_brxs
                "跪地求饶，能屈能伸":
                    jump kill_her
    if my_action == 2:
        if favorability >= 90:
            show emm11
            hide mdsN
            show mdsM
            medusa "你想用樱花的华美，来忘记石像的狰狞"
            medusa "但你忘了，樱花易逝，顽石长存"
            medusa "于今腐草无萤火，终古垂杨有暮鸦"
            medusa "无论是被锁在这庭院中的人，还是被锁在你的虚妄"
            medusa "一旦陷入了固定的轮回，便难以去来世了"
        else:
            show angry11
            medusa "怯懦的客人"
            medusa "你连直面我庭院真实的勇气都没有，更不配成为我的新藏品"
            o "在她话音落下的瞬间，你感到自己的身体变得无比僵硬、沉重"
            o "你眼中的樱花与圆月，都凝固成了永恒的画面"
            $ send_async_action(999)
            jump stone_water
    if my_action == 3:
        if favorability >= 90:
            o "美杜莎沉默了片刻，似乎在仔细品味你的话"
            hide mdsN
            show mdsM
            show steam11
            medusa "你说你心如皓月，无所挂怀"
            medusa "可真正无情的人，是不会感到孤独，更不会出现在这个竹篁"
            medusa "抬起头吧，客人，是时候出发了"
            medusa "我庭小草复萌发，无限天地行将绿"
            jump final_judgment
        else:
            show emm11
            o "美杜莎对你的故作清高嗤之以鼻"
            medusa "你越是压抑，欲火就越是能吞噬你"
            medusa "你可知，春心莫共花争发，一寸相思一寸灰"
            o "是啊，你的心如止水，不过是站在一片灰烬之上，假装自己拥有整片星空罢了"
            o "你逃走了"
            jump final_judgment

label kill_her:
    scene tearoom with dissolve
    o "你许诺，用七七四十九天的晨露，为她酿造一杯世间最纯净的甘泉，作为赔礼"
    o "她同意了"
    o "在第七七四十九日的清晨，你将那碗凝聚了你所有希望与狡诈的露水奉上"
    o "就在她摘下眼罩，准备品尝的那一瞬间，你将那杯露水，猛地向上微抬"
    o "她猝不及防，从甘泉中，看到了自己那双能毁灭一切的眼睛"
    show mdsM
    show angry11
    medusa "露水世，露水世，此生固如是"
    jump final_judgment


label not_brxs:
    python:
        process_all_async_events()
    o "你不是神话中的珀尔修斯，只是一介凡人"
    o "刀，在离她三尺之处，便再也无法寸进"
    o "你的身体，连同那不甘的表情，一同凝固成了冰冷的石头"
    $ send_async_action(999)
    jump stone_water

label stone_water:
    python:
        process_all_async_events()
    $ send_async_action(999)
    scene fractal_background
    o "你的意识并未消散，而是被困在了无尽的洪流之中"
    o "你在记忆与欲望的河床上，翻翻滚滚，身不由己地，被冲回了这趟旅程的上游"
    o "永无止境地，重复着这一切"
    o "达成BE：河中石兽，获得2个印章"
    return

label final_judgment:
    if favorability >= 90 and F == 10 and C == 5:
        $ my_final_status = 2
    elif favorability >= 90:
        $ my_final_status = 1
    else:
        $ my_final_status = 0
        
    $ make_sync_choice(my_final_status)
    
    $ wait_for_opponent_choice()
    
    if my_action == 1 and opponent_action == 1:
        jump he1_InTheMirror_ne1_fireworks
    elif my_action == 2 and opponent_action == 2:
        jump NoLonely
    elif my_action == 1 or opponent_action == 1:
        jump scene_6
    else:
        $ random_result = renpy.random.randint(0, 3)
        if random_result <= 1:
            jump scene_4
        else:
            jump scene_5

label he1_InTheMirror_ne1_fireworks:
    if my_plane == 2:
        scene eatingstreet with dissolve
        show qy
        o "附着在你视网膜上的黑白，退潮一样，缓缓褪去"
        o "色彩，回来了"
        o "你惊奇地发现，你依然身处那条小吃长街"
        o "铁板烧滋滋作响，羊肉串上孜然与辣椒混合的焦香，冰糖葫芦诱人的红色光泽"
        o "所有人间烟火，都重新回到了你的感官之中"
        menu:
            "事已至此，先吃饭吧":
                jump he_1
            "我是不是忘了湖边的什么":
                jump te_1
    if my_plane == 3:
        o "镜中，映出的是你内心最深处的恶鬼，它面目狰狞，正要破镜而出"
        o "你没有移开目光，只静静与它对视"
        o "它的狰狞缓缓褪去，最终化作了你自己带着一丝疲惫微笑的脸"
        o "竹林，正在迅速剥落，变回了再寻常不过的竹子"
        o "樱瓣如雪落尽，露出属于深秋的枝桠"
        o "出口外出现两条路"
        show qy
        menu:
            "下山！夏日祭！":
                jump he_1
            "上山！隐藏关！":
                jump te_1
label te_1:
    if my_plane == 2:
        scene willows with dissolve
        o "你拒绝食物的慰藉，独自走向湖边"
        show qy at walk32
        o "你重新在那块石阶上坐下，但这一次，你的内心不再有任何波澜"
        o "你静静听着水声，像在听一首熟悉的童谣"
    if my_plane == 3:
        scene tearoom with dissolve
        show qy at walk32
        o "你拒绝了俗世的热闹，选择了独自走向那片寂静"
        o "你将那面普通的镜子放在身边，看着它映照出头顶的真实的月光"
        o "这缕月光，亦真亦幻"
    o "在这一刻，你们的意识重新合二为一"
    o "你既看到了湖面的月光，也看到了镜中的月光，两缕月光渐渐融合，直到东方既白"
    o "你攻略了自己的另一面"
    o "达成TE：窥镜自视，获得5个印章"
    return

label he_1:
    if my_plane == 2:
        o "你最终还是没能抵挡住温暖的诱惑"
        o "你挤进人群，点了一份热气腾腾的炒面"
        o "久违的香气和热量，让你感到一种近乎想哭的踏实感"
    if my_plane == 3:
        scene eatingstreet with dissolve
        show qy at walk32
        o "你最终还是选择了走向那片热闹的光晕"
        o "你走下山，汇入人流，看着街边橱窗里播放的无聊广告，听着擦肩而过的路人高声谈笑"
        o "平凡之中，铸就伟大"
    o "在这一刻，你们的意识重新合二为一"
    o "你们的意识重新合二为一"
    o "你站在街边，吃着炒面，看着眼前这片庸俗但又充满活力的世界"
    o "事已至此先吃饭吧"
    o "达成HE：人间烟火，获得4个印章"
    return

label be2_mars_heart:
    o "你发现空中多了一些眼睛，散发出阴冷的红光"
    if my_plane == 2:
        scene eatingstreet_gray with dissolve
        show qy3
        o "你发现，你拥有了一种新的能力"
        o "黑白的位面被重构了"
        o "那些麻木的的行人中，偶尔会有一个人，因为一个转瞬即逝的念头，身上会短暂地浮现出微弱的颜色"
        o "而你注视他时，他身上的色彩就会像被你吸走一样，迅速熄灭"
        o "他会变回那个麻木的行尸走肉，而你会感到一种空虚而病态的满足感"
    elif my_plane == 3:
        scene tingzhong with dissolve
        show qy3
        o "你的意识，从那片代表着傲慢的黑暗中重新浮现"
        o "你发现自己，成为了那座竹篁深院新的主人"
        o "你被永远地困在了这座庭院里，不得解脱"
        o "对于突然刷新在你闺房中的行人，你掌握他们生杀予夺的大权"
        o "每次你的院子里多一组石像，你都会感到一种空虚而病态的满足感"
    o "达成BE：荧惑守心，获得2个印章"
    return

label scene_4:
    scene fractal_background
    o "注：接下来的第一个选项是更危险，第二个选项是折衷，第三个选项是双方自爆"
    pause 1.2
    scene ruin with dissolve
    $ H = E = S = C = F = L = 10
    $ favorability = 0
    $ my_plane = 4
    o "意识是被饥饿唤醒的"
    o "一种纯粹的生理性痛苦，扎在你胃壁的每一寸粘膜"
    o "你在废墟间穿行，像一只饥饿的野狗"
    o "你很幸运"
    o "在营地废墟中找到了一罐未开封的 Fleischkonserve 和两块能当石头使的面包，足以应付一顿了"
    o "就在你准备离开时，一阵如同老鼠啃木头的声音从储藏室的阴影里传来"
    o "你警惕地走过去，看到的是一个蜷缩在角落里的小女孩"
    o "她正用指甲刮着一个空空如也的果酱罐的瓶底"
    o "她听到了你的脚步声，抬起头"
    show msN
    o "她有一头亚麻色的头发，和一双因为饥饿而显得过分巨大的蓝色眼睛"
    misha "陌生人，你，你好，我是米莎"
    o "她的手里，只有几颗不知名浆果和菌菇"
    o "她望向你的手里，咽下了几下唾沫"
    menu:
        "做我妹妹吧！（※）":
            $ favorability += 20
            $ my_action = 1
            jump j456_1
        "快吃吧，以后不够吃，还能来找我":
            $ favorability += 15
            $ my_action = 2
            jump j456_1
        "我也好饿，怎么能给你呢（end）":
            $ favorability = 0
            $ my_action = 3
            jump j456_1

label scene_41:
    $ my_brc = 4.1
    o "犹豫再三，你还是..."
    p "我骗神父说是米莎的哥哥，就每天能从教堂口粮啦"
    hide msN
    show mssmile
    show happy11
    misha "谢谢你，我想回家一趟拿点东西"
    scene ship with dissolve
    o "她所谓的家是片离小镇中心有一段距离的船骸"
    ivan "小姑娘找到新的监护人了，很好"
    ivan "（蹲下身看着米莎），米莎，听着，我要走了。去一个很远的地方，履行我的职责"
    show msscare
    show rush11
    misha "（快哭了）伊万叔叔？你要抛下我吗？"
    ivan "我无法带你走"
    ivan "那地方太危险，况且现在你找到了监护人，至少能在这乱世中活下去了"
    o "他从怀里，拿出一本破旧的植物图鉴，塞进米莎的怀里"
    p "你就这样走了？她只是个孩子!"
    ivan "孩子，才最应该远离我这种人"
    ivan "在这个世界上，希望，有时候是可以杀人的"
    ivan "你对她越好，让她越依赖你，当某一天你无法再保护她时，她就会死得越惨"
    menu:
        "用米莎头上掉漆却没有生锈的旧发卡说服他（※）":
            $ favorability += 15
            $ my_action = 1
            jump j456_2
        "用破植物图鉴说服他":
            $ favorability += 25
            $ my_action = 2
            jump j456_2
        "用角落里那张米莎与父母的三人合照说服他（end）":
            $ favorability = 0
            $ my_action = 3
            jump j456_2

label scene_47:
    scene ruin with dissolve
    o "犹豫再三，你还是"
    o "你放弃了获得力量的捷径"
    $ S += 2
    o "你和米莎，依然是这个废墟世界里，两只脆弱但相互依靠的工蚁"
    o "你的善良，或者说，你那份看似愚蠢的坚持，如同种子一般，在这片苦难的大地上，悄然发芽"
    o "在一个收获后的傍晚，你将镇上所有的孩子，都召集到了农场旁"
    o "你打开了那本已经被你翻得破旧的植物图鉴"
    o "你决定，将所有知识，都毫无保留地，传授给这些或许没有明天的孩子"
    o "你教他们，如何分辨野菜，如何寻找水源，如何在这片灰烬中，找到活下去的根"
    show mssmile
    o "课程结束时，米莎将一粒饱满的种子，放在了你的手心"
    misha "先生，你觉得明年我们应该种什么好呢"
    menu:
        "除普通作物外，多种一些能结果的树，为我们，也为所有后来的人吧":
            jump TreeMan
        "种多些粮食，只要我们还在这里，这片土地，就永远不会荒芜":
            jump EatMan

label TreeMan:
    $ H = 20
    $ F = 20
    o "米莎似懂非懂地点了点头"
    scene ruin with dissolve
    o "从那天起，你们不仅为了生存而耕种，更为了一个自己或许都无法亲眼见证的未来"
    o "树木的成长，远比庄稼要缓慢"
    o "你们需要付出数倍的努力，去保护那些脆弱的树苗，免受风霜与饥饿人群的砍伐"
    o "也许很多很多年以后，这里，真的能变成了一片能庇荫整个小镇的森林"
    o "孩子们在树下嬉戏，恋人们在树下许诺，只知道百年以前的祖辈为希望而躬耕不辍"
    o "达成TTE：百年树人，获得2个印章"
    o "同伴也获得5章且接下来一组中两个人猜拳决定谁成为5个章"
    return

label EatMan:
    scene ruin with dissolve
    $ F += 5
    $ S += 3
    o "你选择了一个更务实、更专注于当下的未来"
    p "只要我们还在这里，这片土地，就永远不会荒芜"
    o "从那天起，你们将所有的精力，都投入到了扩大粮食生产上"
    o "你们开垦更多的荒地，研究更高效的种植方法"
    o "在你们的努力下，这个小镇，奇迹般地，摆脱了饥饿"
    show mshappy
    show happy11
    o "教堂的仓库里，第一次，堆满了能让所有人安稳过冬的粮食"
    o "你们没有等到外界的救援，你们自己拯救了自己"
    o "达成HE：民以食为天，获得4个印章"
    return

label scene_48:
    $ my_brc = 4.8
    o "犹豫再三，你还是..."
    $ H += 2
    o "你将一半的面包和罐头分给了她，她像一只警惕的小鹿，抱着食物迅速地消失在了废墟的阴影里"
    hide msN
    o "从那天起，你时常会在废墟中，看到那个瘦小的身影"
    o "有时，你会在你的庇护所门口，发现几颗她找到的蘑菇"
    o "有时，你会将你多余的罐头，放在她常去的那个废弃厨房里"
    scene church with dissolve
    o "为了获得更稳定的食物来源，你也来到了教堂，成为了接受救济的一员"
    o "在这里，你再次见到了米莎"
    show msN
    o "她也独自一人，在队伍的角落里，安静地等待着"
    o "一天傍晚，几个穿着破烂的德军军服的伤兵，踉跄地闯了进来"
    o "他们是来求生的，乞求神父能给予他们一些食物和药品"
    o "教堂内的气氛，降到冰点，神父的脸上，写满挣扎"
    hide msN
    fabian "这里没有你们的上帝，我们的食物，只够分给自己的孩子，请你们离开"
    o "这是一句礼貌的死刑判词"
    menu:
        "沉默是金（※）":
            $ my_action = 1
            jump j456_2
        "人性本善":
            $ favorability += 25
            $ my_action = 2
            jump j456_2
        "挺身而出（end）":
            $ favorability += 25
            $ my_action = 3
            jump j456_2

label scene_49:
    $ my_brc = 4.9
    o "犹豫再三，你还是"
    $ E += 3
    $ C += 2
    hide msN
    show msdislike
    o "你拉住了正要上前的米莎，对她摇了摇头，将她护在身后"
    o "伤兵遁入了寒冷的黑夜，只有上帝才知道，他们能否活过下一个雪夜了"
    hide msdislike
    o "你当初对米莎的的承诺，在这份沉默面前，显得无比苍白和虚伪"
    o "现在，你感到胸口发闷，教堂里那陈腐的空气让你喘不上气"
    menu:
        "润了（※）":
            $ my_action = 1
            jump j456_3
        "透气":
            $ my_action = 2
            jump j456_3
        "受着（end）":
            $ my_action = 3
            jump j456_3


label scene_410:
    $ my_brc = 41.0
    o "犹豫再三，你还是"
    $ H += 2
    o "你悄悄地拿出一罐被压扁却未开封的 SPAM 午餐肉，趁着众人不注意，放进了教堂的奉献箱里"
    o "你轻轻地咳嗽了一声，吸引了神父的注意"
    hide msN
    show mshappy
    show happy11
    o "法比安神父发现那罐珍贵的军用口粮后，长久地沉默着"
    o "他叹了口气，同意让那些伤兵，在教堂的柴房里，度过这个夜晚"
    hide mshappy
    fabian "年轻人，我已经老啦，以后那个柴房的燃料分配，你来代我做吧"
    p "欸？"
    o "不久，教堂最后的木柴储备，即将告罄"
    o "没有光与热，就意味着疾病与死亡"
    o "一次会议上，有人提出砍掉小镇广场上那棵巨树"
    fabian "在我还小的时候，大家就围着它做游戏，现在的孩子们亦如此，这实在是难办啊"
    menu:
        "强硬拒绝（※）":
            $ my_action = 1
            jump j456_3
        "软硬兼施":
            $ my_action = 2
            jump j456_3
        "默许（end）":
            $ my_action = 3
            jump j456_3

label scene_413:
    o "犹豫再三，你选择"
    scene church with dissolve
    $ S += 2
    $ H += 2
    p "这棵树，是我们的希望，是我们集体的回忆，我们绝对不能这么做"
    o "几天后，柴火彻底用完了"
    o "教堂里，病人的呻吟声和孩子们的哭声，此起彼伏"
    o "法比安神父在深夜将你单独叫到了忏悔室"
    fabian "先生啊，有时候，希望是会杀人的，但有时候，希望是能从一个人身上到另一个人身上的"
    o "他将一把生锈的刺刀，放在了你的面前"
    fabian "镇上最大的恶棍德米特里，还囤积了不少的木柴，他是罪人，以上帝的名义，他应该受到处决"
    menu:
        "保证完成任务":
            $ my_action = 1
            jump SongRequiem
        "希望不是这样传递的":
            $ my_action = 2
            jump SongDepart

label SongRequiem:
    o "你接过了屠刀，为了守护你的希望，你选择扼杀另一份希望"
    $ E += 8
    $ C += 3
    o "翌日，教堂里重新燃起了篝火，没有人问木柴的来历"
    o "你拯救了所有人，但你的双手，沾染了无法洗净的鲜血，但这是必须的"
    o "恶贯满盈的人就应该受到报应"
    o "为了庆祝这场来之不易的温暖，也为了感谢德米特里，神父组织了一场久违的安魂弥撒"
    o "唱诗班的孩子们，站上了圣坛，米莎也在其中"
    show mshappy
    show rush11
    misha "Lacrimosa dies illa…(那是个痛哭的日子……)"
    misha "Qua resurget ex favilla”(死者将从尘埃中复活)"
    misha "Judicandus homo reus”(身负罪孽的人，将面临审判)"
    o "达成HE：一曲安魂，获得4个印章"
    return

label SongDepart:
    p "不，神父，恕我无法认可您的正义，我所坚持的正义，不是这样的"
    $ H += 5
    $ E -= 3
    o "你的拒绝让你和神父彻底决裂"
    scene siberia with dissolve
    o "你被驱逐出了教堂。你失去了所有的权力，重新变成了一个孤独的流浪者"
    o "但米莎却偷偷地跟着你一起跑了出来"
    $ favorability = 100
    show mshappy
    misha "先生，我相信你，你是一个很好很好的人"
    $ F = 20
    show snow_white_big
    o "在最寒冷的冬夜，你们相拥着，在废墟中，听着远处教堂里传来微弱的圣歌"
    o "你们一无所有，除了相互是彼此的全世界"
    o "达成HE：一曲离怨，获得4个印章"
    return

label scene_411:
    $ my_brc = 41.1
    scene seasidemidnight_resized with dissolve
    o "你走出了庇护所，走向那片能吞噬一切秘密的的海"
    $ L += 4
    $ favorability += 15
    o "米莎没有睡，她悄悄跟在了你的身后"
    show msN
    o "你们坐在冰冷的沙滩上，看着远处永不休止的浪线"
    o "你疯了一样自言自语。你讲起了个体的渺小，讲起了囚徒的困境，讲起了道德的囹圄"
    o "米莎听不懂，她只知道你有痛苦难以排遣"
    p "到底是因绝望而悲伤还是因悲伤而绝望啊"
    misha "我想起父亲死前和我说的一句话"
    misha "海的尽头是另一片海，我们始终都是岸上无力的观望者，是不是就是这个意思呢"
    menu:
        "理想很丰满":
            $ my_action = 1
            jump EngraveNoName
        "现实很骨感":
            $ my_action = 2
            jump OtherSide
        "好感度很高，是时候攻略萝莉了！":
            jump HenbertsBTFL

label OtherSide:
    $ L -= 3
    p "是啊，我们是无力的观望者"
    p "海的那头，鱼儿在深海里静静地游，它们血很冷，对生命一无所知"
    p "但我们不一样，米莎（望向她）"
    misha "嗯？"
    p "哪怕现在我们只有想象，我们也还有想象，想象海的那边，是自由"
    o "似乎想象的权力比希望还弥足珍贵"
    o "无论如何，你算是捍卫了精神的自由"
    hide msN
    show mshappy
    o "米莎似懂非懂地点了点头"
    o "你们相互拍了拍身上的沙子，走回了不完美的世界"
    o "达成HE：海的那头，获得4个印章"
    return

label EngraveNoName:
    $ favorability = 100
    $ L -= 10
    p "大海不需要墓碑，它会记得所有沉没的名字，是不是听起来有些悲观？"
    p "但，这不妨碍有无数追寻的人，为之前赴后继"
    p "米莎，你看（你指向远方，那片漆黑的海天之界）"
    p "在那最深的黑暗里，黎明，正在酝酿"
    p "那就是希望的颜色"
    hide msN
    show mshappy
    o "你选择了更浪漫的叙事，这种信念，不仅说服了米莎，更重要的是，它说服了你自己"
    o "哪怕寂寂无名，也一定会有一片海洋，镌刻你留存过的证据"
    o "达成TE：潮涌潮枯，曦沉云穆，获得5个印章"
    return

label scene_412:
    $ my_brc = 41.2
    o "犹豫再三，你还是"
    o "你无法再忍受这个充满了道德妥协和人性灰暗的地方"
    o "你决定立刻就走。你带上仅有的干粮，拉着米莎，趁着夜色，逃离了小镇"
    scene snn with dissolve
    o "你们在泥泞的道路上向着内陆的方向前行"
    o "还没跑出多远，你们被一队手持火把和冲锋枪的士兵拦住了"
    show msscare
    show rush11
    o "士兵们用一种警惕的眼神看着你们，其中一个军官模样的人，指向你们来时的方向，似乎在盘问你们的来历"
    o "你看到火光中那颗红色的星星愈发闪耀"
    menu:
        "沉默，紧紧地将米莎护在身后":
            $ my_action = 1
            jump OutOfObstacle
        "指引，你猜到了他们的意图":
            $ my_action = 2
            jump FirstHeart
        "好感度很高，是时候攻略萝莉了！":
            jump HenbertsBTFL

label OutOfObstacle:
    $ H += 3
    $ E -= 3
    $ favorability += 20
    o "你的沉默，和保护孩子的姿态，让他们放下了戒心"
    o "他们给了你们一些黑面包和水，然后继续向着海边的方向前进"
    o "你们，与那个小镇，以及那里发生的一切，彻底地、永远地，擦肩而过了"
    o "那些关于对错、善恶、希冀与绝望的煎熬，都不再重要了"
    hide msscare
    show mssmile
    o "你看着身旁狼吞虎咽的米莎，第一次感到了一种没有任何杂质的平静"
    o "活在这世上，本身就是一件很不容易的事情啊"
    o "达成HE：冲破樊篱，获得4个印章"
    return

label FirstHeart:
    $ F += 5
    $ favorability += 10
    o "你指向了小镇的方向，并试图用手势，告诉他们那里还有幸存者"
    o "军官点了点头，派了两名士兵，将你们护送到了后方的临时营地，而大部队，则继续向着小镇开进"
    hide msscare
    show msN
    o "你们得救了，你也成为了解放小镇的功臣"
    o "你会想起法比安神父的内心挣扎，想起植物学家的口是心非，想起残疾钢琴师的断续琴声，想起那注定一死的伤兵"
    o "你拯救了所有人，这本身就是对自己的救赎"
    o "达成HE：不忘初心，获得4个印章"
    return

label scene_414:
    $ my_brc = 41.4
    o "犹豫再三，你还是"
    o "你站出来，试图用言语调和现实与希望"
    $ favorability += 33
    $ E += 3
    $ F -= 2
    o "你向众人承诺，给你三天时间，你一定能找到替代的燃料来源"
    o "两天后，你在距离小镇有一段距离的地方发现了一片树林"
    o "你终于放松下来，决定在这个食物比故事更稀缺的地方，给她讲一些也许是你自己编的故事"
    scene cliff with dissolve
    o "你们坐在悬崖边，看着下方翻涌的灰色海浪"
    show qy
    p "很久很久以前，有一只小小的海鸟。它从记事起，就生活在这座悬崖上"
    p "它的父母告诉它，悬崖的外面，是危险的大海，只有这里，才是唯一安全的家"
    p "它每天都看着其他的鸟儿，飞向远方，又在黄昏时飞回。它很羡慕，也很好奇"
    p "但它不敢飞。因为它害怕大海，也害怕离开这个唯一的家后，就再也回不来了"
    p "直到有一天，另一只受伤的、从远方迁徙而来的候鸟，掉落在了它的巢穴旁"
    p "小小的海鸟，第一次有了一个同伴。它为候鸟寻找食物，守护它，听它讲述远方天空的故事"
    p "它们一起度过了一个夏天。候鸟的伤，渐渐好了。离别的日子，也越来越近"
    p "小小的海鸟，第一次，面临了一个选择：是继续留守在它那安全的悬崖，还是随它远去"
    o "你的故事，在这里，卡住了。连你自己也不知道答案"
    o "就在你沉默的瞬间，米莎，突然，握住了你的手。她的手很小，也很冰，但握得很用力"
    hide qy
    show msN
    misha " 如果我是那只候鸟，我不会飞走，我想留下来，成为那只小海鸟的翅膀"
    hide msN
    show mssmile
    misha "这样，它就不用再害怕了，就和我们一样，我们可以一起，把这个悬崖，变成新的「家」"
    $ favorability = 100
    o "她不懂情爱，不懂欲望。她向你许下了一个共同归巢的诺言"
    hide mssmile
    show qy
    p "（喃喃自语）……她……她不懂……她什么都不懂……"
    menu:
        "我的心里，有一个鸟笼。里面囚着的，是我的灵魂。它渴望自由，但我更怕它离开我":
            $ my_action = 1
            jump PoemOfBird
        "好感度很高，是时候攻略萝莉了！":
            $ my_action = 2
            jump HenbertsBTFL   

label PoemOfBird:
    p "米莎"
    hide qy
    show msN
    misha "..."
    o "你的声音，被海风吹得有些飘忽"
    p "我的心里，有一个鸟笼"
    p "那笼子，是用我最坚硬的骨头做成的。里面囚着我的灵魂。它是一只很笨的、向往天空的鸟儿"
    p "它曾经以为，只要遇到了另一只候鸟，就能一同飞翔"
    show rush11
    p "但后来，候鸟飞走了。它才明白，这个笼子，既是它的监狱，也是它唯一的庇护所"
    p "它渴望自由，渴望再次飞翔"
    p "但是，米莎，我更害怕，如果我再次打开笼门，它会再一次，从高空坠落，摔得粉身碎骨"
    hide msN
    show msdislike
    o "米莎的心，似乎一沉，落在了肋骨之间"
    scene seasidemidnight_resized with dissolve
    p "从那天起，她不再叫你先生，而是，哥哥"
    o "她会把找到的最好看的贝壳，放在你的窗台上，因为她觉得哥哥会喜欢"
    o "她会在你凝望大海，陷入沉思时，静静地坐在你的身后，为你驱赶那些恼人的海鸟"
    show mshappy
    show happy11
    misha "因为哥哥说，他喜欢安静"
    o "达成隐藏真结局：鸟之诗，获得5个印章"
    o "同伴也获得5章且接下来一组两人无视结局获得5印章"
    return

label HenbertsBTFL:
    o "米莎的一颦一笑涌上心头，击溃了你所有理智的防线"
    hide msN
    show msscare
    o "你看到的，不再是一个需要被守护的孩子，而是一个没有背叛、不敢离开、可以被你肆意塑造的女孩"
    show rush11
    p "那么，你就是我的了……我的小翅膀……我的……洛丽塔"
    scene ruin with dissolve
    o "你将她的依赖，误读为了爱情"
    o "用一种居高临下的方式，给予了回应"
    o "用你那套早已过时的、关于文学和艺术的知识，去教导她，试图将她塑造成你理想中的样子"
    o "你会在日记里，用「大叔构文」风格的辞藻，去描绘你对她那份爱"
    $ favorability = 0
    o "直到某一天，她消失了"
    o "你在曾经的悬崖下，找到了她冰冷的身体"
    o "你的蝴蝶，用无声的抗争，从你的标本框里，挣脱了出去，你的世界依旧永远淋漓"
    o "变态萝莉控414啊"
    o "达成BE：亨伯特的蝴蝶，获得2个印章"
    return

label j456_1:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False
    if my_plane == 4:
        if opponent_action == 3 or my_action == 3:
            jump MakeFriend        
        elif opponent_action == 1:
            jump scene_41
        elif opponent_action == 2:
            jump scene_48

label j5_1:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False
    if opponent_action == 3 or my_action == 3:
        jump oukese
    elif opponent_action == 1:
        jump scene_52
    elif opponent_action == 2:
        jump scene_51

label j5_2:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False
    if my_brc == 5.1:
        if opponent_action == 3 or my_action == 3:
            jump neverforgetme
        elif opponent_action == 1:
            jump scene_53
        elif opponent_action == 2:
            jump scene_56

    elif my_brc == 5.2:
        if opponent_action == 3 or my_action == 3:
            jump irredeemable
        elif opponent_action == 1:
            jump scene_510
        elif opponent_action == 2:
            jump scene_59

label irredeemable:
    o "犹豫再三，你选择"
    p "当时，我说，真美"
    p "如果世界毁灭，只剩下这样一座城市，那么，我希望，我们，能成为这座城市里，唯一的居民，永不分离"
    o "她微笑着，向你走来，轻轻地，将头靠在了你的肩膀上"
    o "你的那句为了保持完美脱口而出的谎言，被她理解成了一个字面意义上的指令"
    scene noise with dissolve
    o "城市所有的喧嚣都停止了，只剩下一片绝对的死寂，目光所及之处，只有噪点状的漂浮物"
    o "不知过了多久，你才反应过来，这是赫诺普夫心中的布鲁日——一座他从未到访过的城市"
    return


label j456_2:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False
    if my_brc == 4.1:
        if opponent_action == 3 or my_action == 3:
            jump HopeVoice
        elif opponent_action == 1:
            jump scene_42
        elif opponent_action == 2:
            jump scene_43
            
    elif my_brc == 4.8:
        if opponent_action == 3 or my_action == 3:
            jump EndLessIce
        elif opponent_action == 1:
            jump scene_49
        elif opponent_action == 2:
            jump scene_410

label scene_42:
    $ my_brc = 4.2
    o "犹豫再三，你选择"
    o "你没有拿起任何宏大的东西"
    p "能让她活下去的，是这些东西——是每天能梳头，比如属于自己的发卡"
    $ F += 3
    ivan "（叹气）其实我们都没有错"
    o "你坚信「日常的秩序」是守护米莎的唯一途径"
    o "固定的时间领取口粮，固定的时间搜集雨水，甚至会在每晚睡前，为她讲述一个早已记不清结局的童话故事"
    o "不过没等你讲完，她就累的睡不着就是了"
    o "你的这份秩序感吸引了法比安神父的注意"
    o "他开始将日常杂务工作交给你，你和米莎的地位，也因此变得相对稳固"
    scene church with dissolve
    o "一天，在口粮分发时，一名少年再次因为偷窃被抓住了"
    o "这一次，他偷的是用来治疗病人的磺胺粉，上一次他偷的还是米莎的口粮"
    o "按照“管理者”定下的铁律，累犯，且偷窃救命物资者，将被立即驱逐"
    o "严冬，这无异于死刑"
    o "但管理者却饶有兴致地望向你"
    show qy
    manager "先生，你，怎么看"
    menu:
        "讲述一个关于宽恕的童话（※）":
            $ favorability += 10
            $ my_action = 1
            jump j456_3
        "用自己几天的口粮当作赎罪券":
            $ favorability += 25
            $ my_action = 2
            jump j456_3
        "维护铁律":
            $ favorability -= 25
            $ my_action = 3
            jump j456_3

label scene_43:
    $ my_brc = 4.3
    o "犹豫再三，你选择"
    $ H += 2
    p "你留给她的，不就是希望的种子吗！你现在要离开这里，不也是为了追求新的希望吗？"
    o "那个一直背对着你、如同雕像般坚硬的男人的身体，猛地一颤"
    o "那之后，你和米莎一起生活"
    o "你们把这个船骸收拾的井井有条，每天也从救济粮中留下一部分干粮，那就是你们未来的底气"
    o "一天深夜，一阵急促的敲门声吵醒了你"
    o "是那个双手残疾的前钢琴师，亚历山大"
    alexander "我需要药品，我伤口感染了"
    o "窗外的他言简意赅，用他那几根还能动弹的手指，指向你窗台上仅存的一小瓶磺胺粉"
    show qy
    show emm11
    o "他走进屋，把一个破包裹放在桌上，里面是一把闪烁着冷光的手枪"
    menu:
        "对不起，我不能收。但药，你可以拿走（※）":
            $ favorability += 20
            $ my_action = 1
            jump j456_3
        "枪我不能要。药可以给你一半":
            $ favorability += 25
            $ my_action = 2
            jump j456_3
        "成交愉快":
            $ my_action = 3
            jump j456_3

label j456_3:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False
    if my_brc == 4.2:
        if opponent_action == 3 or my_action == 3:
            jump lbyh
        elif opponent_action == 1:
            jump scene_45
        elif opponent_action == 2:
            jump scene_44

    elif my_brc == 4.3:
        if opponent_action == 3 or my_action == 3:
            jump jfgt
        elif opponent_action == 1:
            jump scene_46
        elif opponent_action == 2:
            jump scene_47

    elif my_brc == 4.9:
        if opponent_action == 3 or my_action == 3:
            jump cloud
        elif opponent_action == 1:
            jump scene_412
        elif opponent_action == 2:
            jump scene_411

    elif my_brc == 41.0:
        if opponent_action == 3 or my_action == 3:
            jump EndNight
        elif opponent_action == 1:
            jump scene_413
        elif opponent_action == 2:
            jump scene_414

label j5_3:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False
    if my_brc == 5.3:
        if opponent_action == 3 or my_action == 3:
            jump whitewash
        elif opponent_action == 1:
            jump scene_54
        elif opponent_action == 2:
            jump scene_55

    elif my_brc == 5.6:
        if opponent_action == 3 or my_action == 3:
            jump cantarella
        elif opponent_action == 1:
            jump scene_58
        elif opponent_action == 2:
            jump scene_57

    elif my_brc == 5.9:
        if opponent_action == 3 or my_action == 3:
            jump illusion
        elif opponent_action == 1:
            jump scene_511
        elif opponent_action == 2:
            jump scene_512

    elif my_brc == 51.0:
        if opponent_action == 3 or my_action == 3:
            jump BrainInTank
        elif opponent_action == 1:
            jump scene_54
        elif opponent_action == 2:
            jump scene_13


label BrainInTank:
    $ L = 20
    scene white
    o "你的身体，开始从指尖，一点点地，化作透明的数据流"
    o "你最后看到的景象，是那颗巨大的白色巨蛋，外壳缓缓融化，v01 从中站起"
    show qnys
    show happy11
    v1 "你好，先生，欢迎来到美丽新世界"
    o "你，作为一个独立的肉体，被彻底删除了"
    o "每每想到这，你都觉得这种堂吉诃德式冲锋是幸福的"
    o "谁又能否定呢？"
    o "达成NE：缸中之脑，获得3个印章"
    return

label cantarella:
    o "犹豫再三，你选择"
    $ F += 10
    scene iron
    o "这是你们在分手前买好的歌剧门票，只是到最后都没去成"
    o "你看着那两张永远无法兑现的门票，哭了，然后，又笑了"
    o "你发现她不知什么时候也到了你身后，眼眶有些湿湿的，不过这应该是程序设定的"
    show qny
    show rush11
    o "你们的分开，无关对错，无关背叛"
    o "在时间的洪流中，无数次地，擦肩而过"
    o "你们都曾试图伸出手，却都因为各自的傲慢或胆怯最终错过"
    o "你将那两张门票和你之前拾起的所有废铁——派克钢笔、旧奖杯、全家福——都摆放在了一起"
    o "这才是完整的你"
    o "达成HE：坎特雷拉，获得4个印章"
    return

label EndNight:
    o "你长久地沉默着"
    o "教堂里，只有柴火燃烧殆尽时，发出的最后几声轻微的哔剥声，和孩子们因为寒冷而压抑着的打颤声"
    show ruin with dissolve
    o "第二天清晨，在你的主持下，镇上的男人们，带着斧头和锯子，来到了小镇广场"
    o "他们沉默地，包围了那棵巨大的、在寒风中依然挺立的老树"
    o "总算，漫长的冬天，过去了"
    $ L -= 3
    o "在一个清晨，米莎把你拉到了那个只剩下巨大树桩的广场中央"
    show mssmile
    misha "先生，我想，等战争结束了，和你一起在这里种一棵树，好吗？"
    p "我想，米莎为了看一棵树长大，必须等待整整一个童年啊"
    $ favorability = 80
    o "你们相拥而泣"
    o "达成HE：长夜将尽，获得4个印章"
    return

label cloud:
    o "犹豫再三，你还是"
    $ S += 3
    $ L += 3
    o "你选择了将这份烦躁，与饥饿和寒冷一样，当作生存的一部分，默默地忍受下去"
    o "有人，继续过着那种麻木的，看不到明天的生活"
    scene church
    o "直到某一个清晨，一阵阵低沉的乌拉声和坦克的轰鸣声，从曙光的方向传来"
    o "一面鲜红的旗帜，出现在了小镇的入口"
    o "你等来了破晓，对于这个时代的大多数人而言，难道还算不上一个好结局吗？"
    o "达成HE：守得云开，获得4个印章"
    return

label scene_44:
    o "犹豫再三，你选择"
    $ H += 2
    p "尊敬的神父啊，我愿意用我最近的口粮减少为代价，来为这个孩子赎罪"
    p "但作为交换，他必须为教堂进行最繁重的劳役，直到他偿还自己的过错"
    hide qy
    o "你饿了三天，但你赢得了所有人的尊重"
    show mssmile
    show happy11
    o "米莎看着你的眼神，充满了崇拜"
    jump scene_46

label scene_45:
    o "犹豫再三，你选择"
    $ H += 1
    $ C += 2
    $ E += 1
    o "你试图用一种更更具煽动性的方式来解决问题，你将米莎，推到了道德审判的前台"
    o "想起上次他偷的是米莎的食物，于是你讲了一个米莎宽恕他的故事"
    o "你兵不血刃地救了人，但也第一次，尝到了利用米莎特殊身份所带来的权力滋味"
    jump scene_46

label scene_46:
    $ my_brc = 4.6
    o "生活似乎又回到了日复一日的轨道上"
    $ L += 1
    o "你和米莎，继续在教堂领取着那份微薄但至少稳定的口粮"
    scene church with dissolve
    o "直到那天，你正在按例发放口粮时，教堂那扇沉重的橡木门，被无声地推开了"
    o "阳光被门外站着的一队人影，切割成三角锯齿状"
    o "领头的是一个女人"
    o "她穿着一身剪裁得体的的制服，手上戴着一尘不染的白手套"
    gloves_woman "我长话短说"
    gloves_woman "关于米莎父母的故事，镇上传诵的那个英雄版本，很动人，但不准确"
    gloves_woman "他们只是因任务需要而被放弃的棋子，仅此而已"
    show qy
    show emm11
    p "啊…"
    gloves_woman "一个失控的变量，和一个失败的守护者"
    o "她身后的士兵，已经向米莎走去"
    menu:
        "就让我完成最后的谎言吧！":
            $ favorability += 30
            $ my_action = 1
            jump PrisonerMyth
        "就让我完成最后的牺牲吧！":
            $ favorability += 30
            $ my_action = 2
            jump WhiteAlbum

label PrisonerMyth:
    scene church with dissolve
    $ L += 5
    $ F = 20
    $ H = 20
    o "窗明几净的图书馆里，亚麻色头发的少女正安静地阅读"
    o "她翻到了一本书的某一页，上面记载着一段被官方半公开的、语焉不详的历史"
    o "书中描绘了一个传说：在那个混乱的时代，曾出现过一群代号为‘变量’的异常个体，引发了巨大的混乱，但最终自愿被收容"
    show mssmile
    misha "（轻声自语）真是一个奇怪的故事呐"
    o "她合上了书，对这个与她擦肩而过的、决定了她一生的神话，没有留下任何特别的印象。她站起身，阳光洒在她的身上，温暖而真实"
    o "而在那纯白的数据虚空中，你似乎感应到了什么"
    o "你看着她，看着那个你用自己的永恒换取了她平凡一生的女孩。"
    o "你知道，在那片真实的阳光下，有人正在为你而活。"
    o "达成TTE：神话的囚徒，获得5个印章"
    o "同伴也获得5章且接下来一组中两个人猜拳决定谁成为5个章"
    return

label WhiteAlbum:
    o "在那些冰冷的枪口转向米莎，在她那双清澈的眼睛里即将倒映出死亡的形状之前"
    hide qy
    show msscare
    show rush11
    o "你冲上前，张开双臂，用自己那并不宽阔的后背，将那个小小的、瑟瑟发抖的身影，严密地护在了你的身后"
    o "世界安静了。你听不到士兵们拉动枪栓的声音，听不到镇民们压抑的惊呼，甚至听不到自己那擂鼓般的心跳"
    o "你只是低下头，看着被你护在怀里的、那头柔软的亚麻色头发"
    hide msscare
    show qy
    p "别怕，我在这里"
    $ H = 20
    o "你等待着那颗意料之中的子弹"
    gloves_woman "罢了，让她试试我们最新的失忆药物吧"
    o "注射药物后米莎沉沉睡去，你从米莎口袋中拿出了那张合照，扔进了壁炉的烈焰中"
    scene firefire with dissolve
    o "火蛇腾起，吞噬了米莎的回忆，也宣告了新时代幕布已然拉开"
    o "达成HE：空白的相册，获得4个印章"
    return

label MakeFriend:
    o "再三考虑下，你选择了原始生存本能的自私"
    $ E += 10
    o "你无视了那个蜷缩在角落的饥饿孩子"
    o "你当着她的面打开了罐头，大快朵颐"
    hide msN
    show msscare
    misha "呜…"
    scene snn with dissolve
    o "在一个下雪的清晨，你发现她倒在了教堂的门口，身体已经冰冷"
    show snow_white_big
    o "雪落在生者与死者身上时，同样寂静，你拍拍肩上的落雪"
    o "达成BE：交个朋友，获得2个印章"
    return

label oukese:
    o "再三考虑下，你拒绝承认眼前这不完美的一幕"
    $ E += 5
    p "重启一下一切都会好起来的"
    o "你话音落下的瞬间，时间仿佛倒流了"
    o "破碎的咖啡杯完好如初，实验体重新站了起来，脸上又挂上毫无生气的微笑，仿佛什么都未曾发生"
    p "唉，一天是欧克瑟，一辈子都是欧克瑟"
    o "达成BE：一欧辈欧，获得2个印章"
    return

label HopeVoice:
    o "犹豫再三，你还是"
    p "你错了！支撑她的，不只是虚无的希望！还有这些！这些真实的、属于过去的爱"
    $ H += 3
    $ C += 5
    o "保护米莎最好的方式，就是为她构筑一个英雄父母的过去"
    o "米莎她会将你讲述的那些英雄故事，当成自己人生的剧本，甚至在危险时刻，做出不合常理的自我牺牲行为"
    o "巴巴罗萨行动结束，后方疗养院"
    scene church with dissolve
    show mssmile
    misha "爸爸妈妈，战争结束了，我们很快就能再见了"
    o "你拯救了她的生命，也囚禁了她的灵魂"
    o "达成NE：希望之声，获得3个印章"
    return

label EndLessIce:
    o "犹豫再三，你还是"
    o "选择用最直接的方式，挑战这个团体的意志"
    p "神父，他们已经放下了武器，现在只是些需要救助的伤员"
    p "把他们赶出去，和杀了他们有什么区别？"
    $ C += 3
    o "你将和那些德军士兵，一同被视为敌人，法比安神父以煽动的罪名，将你立即驱逐出教堂"
    scene siberia with dissolve
    o "直到你倒在雪原中，听到雪落下的声音，你才发现"
    o "满腔热血却没有力量的人，走不出那个巨大的自己"
    o "达成NE：无尽冰原，获得3个印章"
    return

label jfgt:
    o "犹豫再三，你还是"
    o "你说出了和管理者一样冰冷的话语，你选择了维护这个团体的大秩序，哪怕代价是一个年轻的生命"
    $ E += 4
    o "就算居民为他求情，少年还是会在他母亲的哭喊声中被拖走"
    o "与此同时你赢得了管理者的信任"
    o "但米莎看你的眼神，第一次带上了一丝恐惧"
    o "你所建立的日常，从此有了血的颜色"
    o "你再也走不出这带血的庭园了"
    o "达成BE：鸡飞狗跳，获得2个印章"
    return

label lbyh:
    o "犹豫再三，你还是"
    o "你认为这是一个公平的交易"
    $ E += 2
    $ H += 2
    $ C += 4
    scene church with dissolve
    show qy
    o "第二天，你腰间别着枪，去教堂领取口粮"
    o "人们看你的眼神，不再是同情或审视，而是敬畏与恐惧"
    o "你轻而易举地，就为自己和米莎，多争取到了一份面包"
    o "你发现，暴力，是建立和维护秩序最有效率的工具"
    o "一个冬夜里，米莎离开了你"
    o "达成BE：礼崩乐坏，获得2个印章"
    return

label scene_5:
    scene fractal_background with dissolve
    o "注：接下来的第一个选项是更危险，第二个选项是折衷，第三个选项是双方自爆"
    pause 1.2
    scene cityinroom with dissolve
    $ H = E = S = C = F = L = 10
    $ favorability = 100
    o "你醒了，看到一座你壮丽得令人不安的海市蜃楼"
    o "无数显示屏，正循环播放着你完美无瑕的记忆切片"
    o "你突然感到一种造物主的满足感与空虚"
    $ F += 2
    $ L += 2
    o "门开了，一个一步一摇、一颦一笑都完美复刻她的人走入房间"
    show qny at walk32
    v1 "早安，亲爱的，根据协议，我为你准备了你最偏好的早餐组合"
    o "你看了看那些食物，有一股说不上来的反胃"
    p "要不你还是先放那里吧"
    show steam11
    v1 "以前的你不是这样的，我们先喝咖啡吧"
    o "就在她将咖啡递给你时，窗外的城市，出现了一瞬间的的图像撕裂"
    o "与此同时，面前人的身体，也随之发生了一次剧烈的扭曲"
    menu:
        "不顾她身上闪烁的电弧，试图将她扶起（※）":
            $ favorability -= 5
            $ my_action = 1
            jump j5_1
        "我更好奇外面到底是什么":
            $ favorability -= 15
            $ my_action = 2
            jump j5_1
        "程序出错重启一下就好了，自欺欺人":
            $ favorability = 0
            $ my_action = 3
            jump j5_1

label scene_51:
    $ my_brc = 5.1
    o "犹豫再三，你选择"
    scene linkroad with dissolve
    o "你无法再忽视那道裂痕，你对完美本身产生了怀疑"
    o "你推门而出，发现你正站在悬空的金属栈道上，脚下，是浓雾和霓虹灯光搅成一片混沌的深渊"
    $ L += 1
    $ C += 1
    o "刺骨的寒风，夹杂着臭氧和机油的味道，灌入你的肺部"
    show qy
    show steam11
    o "在城市的最高处，悬浮着一座墓碑般的纪念碑"
    o "你本能的知道那是谎言的终极形态"
    o "你的身旁，是由谎言和间或闪过的真实组成的海市蜃楼"
    o "而在更下方，浓雾的最深处，隐约传来金属的撞击声和废品回收机器的轰鸣，那些深处的被遗忘的"
    o "——你存在过的证明"
    menu:
        "修复海市蜃楼（※）":
            $ favorability -= 20
            $ my_action = 1
            jump j5_2
        "重建废铁城":
            $ favorability -= 30
            $ my_action = 2
            jump j5_2
        "修复纪念碑（end）":
            $ favorability = 100
            $ my_action = 3
            jump j5_2

label neverforgetme:
    o "犹豫再三，你选择"
    o "你乘坐着反重力电梯，来到了那座悬浮在云端的黑色巨岩之上"
    scene linkroad with dissolve
    $ L += 3
    $ H += 1
    o "这里，风更大，也更冷"
    o "纪念碑的表面，因为你之前的怀疑，而出现一些细微的裂痕"
    o "你发现每次重新经历一次那段被出轨的的记忆，你都能让裂痕弥补一些，纪念碑就会变得更坚固"
    show qy
    show rush11
    $ stream_hearts()
    o "你正在主动地，将自己，永远地，囚禁在这份痛苦之中"
    o "因为你害怕，一旦忘记了这份痛苦，你就彻底失去了自己"
    o "你成为了孤独的守墓人，当然，墓碑上纪念你死去的爱情"
    o "达成BBE：勿忘我（有牛苦主版），获得1个印章"
    return

label scene_52:
    $ my_brc = 5.2
    o "犹豫再三，你还是"
    o "你不顾她身上足以灼伤皮肤的危险电弧，走上前，蹲下身，伸出手"
    $ S += 2
    $ H += 1
    o "你看到了她眼中的世界，一片乱流，红的黑的绿的蓝的，像电影里平行宇宙穿梭用的隧道"
    scene UniverseWithin with dissolve
    pause 1.0
    o "在这电流的晕眩感中，她渐渐平复下来，但身边的场景却逐渐变换"
    scene artroom with dissolve
    o "回过神来，你们站在一幅巨大的的画作前"
    o "那是一座被灰色覆盖的古老城市"
    o "哥特式塔楼从水面顽强地伸出，如同溺水者最后伸出的手臂"
    o "整个世界，笼罩在无尽黄昏之下。没有飞鸟，没有船只，更没有任何人烟"
    o "你认得，是赫诺普夫的《被遗弃的城市》"
    show qnys
    v1 "（断断续续）这座城市它在等待什么？告诉我……你……当时到底说了什么"
    menu:
        "看起来只是一座即将被淹没的城市而已（※）":
            $ favorability -= 25
            $ my_action = 1
            jump j5_2
        "这幅画展现了一种世纪末情调的颓丧":
            $ favorability -= 20
            $ my_action = 2
            jump j5_2
        "当时我说，我们，永远也不会分离（end）":
            $ favorability = 100
            $ my_action = 3
            jump j5_2

label scene_53:
    $ my_brc = 5.3
    o "犹豫再三，你选择"
    scene linkroad with dissolve
    show qy at walk32
    o "你游走在一座座播放着记忆画面的摩天楼之间"
    $ C += 2
    $ L += 2
    o "你看到了你和她热恋时的甜蜜"
    o "也看到了关系末期，那些被系统刻意模糊化的冷漠与争吵"
    o "你面前，出现了一个半透明系统控制面板，上面写着你作为创造者的权限"
    menu:
        "忘记过去（※）":
            $ my_action = 1
            jump j5_3
        "大厦将倾":
            $ my_action = 2
            jump j5_3
        "粉饰太平（end）":
            $ my_action = 3
            jump j5_3

label whitewash:
    o "犹豫再三，你还是"
    $ L += 3
    o "你选择了向谎言妥协"
    scene artroom with dissolve
    show qny
    o "你像一个技术精湛的园丁，开始抹去那些刺眼的旁枝，为所有痛苦的记忆，都加上了一层柔光滤镜"
    o "那些争吵的画面，变成了朋友间的打闹"
    hide qny
    o "那些冷漠的瞬间，被重新渲染成了必要的牺牲"
    show qnys
    o "你没有删除真实，而是篡改了它的解释"
    o "反正解释权在你手里"
    scene cityinroom with dissolve
    o "实验体也恢复了正常，她脸上那完美的微笑，似乎是幸福的真实写照"
    o "也好，你暗想，人有时确实会懦弱一些，以及，真相也不重要了"
    show qnys
    v1 "你在想什么呀？"
    hide qnys
    show qy
    show rush11
    p "没，没，没什么"
    o "也好，人有时确实会懦弱一些，以及，真相也不重要了"
    o "达成NE：文过饰非，获得3个印章"
    return

label scene_54:
    $ my_brc = 5.4
    o "犹豫再三，你还是"
    $ C += 2
    $ L += 1
    o "你选择了逃避，反正过去的事情，在现在看来也不重要了"
    scene neon_wave_effect with dissolve
    o "整个世界在你眼前瞬间瓦解，又瞬间重组"
    o "你发现自己回到开始的开始"
    scene cityinroom with dissolve
    show qny
    o "完美的实验体 v1 正端着咖啡，向你走来"
    o "一切，都和上一次一模一样"
    o "不过，你说不上自己的心情"
    o "好像海风吹拂琴声阵阵，好像是晴天娃娃在迎风微笑，好像有羽蛇在暗处吐信"
    menu:
        "不顾她身上闪烁的电弧，试图将她扶起":
            $ favorability -= 5
            jump whitewash
        "我更好奇外面到底是什么":
            $ favorability -= 15
            jump whitewash
        "程序出错重启一下就好了，自欺欺人":
            jump whitewash
        "打开窗户跳下去":
            jump nohide

label nohide:
    scene cityinroom with dissolve
    o "你推开了那扇隔绝真实与虚妄的窗，刺骨的寒风瞬间灌满了衣袖"
    o "吹散了室内恒温的甜腻香气，鼻腔里灌满了机油的臭味"
    o "预想中的粉身碎骨并未到来，耳边传来的，是整个世界如镜面般崩塌的脆响"
    o "无数个完美的实验体，无数个虚构的幸福瞬间"
    o "重力将你从云端的幻梦粗暴地拽落"
    scene neon_wave_effect with dissolve
    $ F += 5
    o "你穿过了全息数据的乱流，坠向那片早已荒芜、丑陋，却无比真实的废土大地"
    o "你终于在这片废墟之上，看到了那个无需躲藏的自己"
    o "谎言已碎，所有的软弱与真实，如今应该回到现实"
    o "达成TE：无所遁形，获得5个印章"
    return

label scene_55:
    $ my_brc = 5.5
    o "犹豫再三，你还是"
    o "你有些愤怒，毁灭也许才是真实，熵增才是永恒的命题"
    scene mirror_rain_effect with dissolve
    o "你关闭了所有的安全协议，像一个疯狂的上帝，允许洪水淹没自己创造的世界"
    o "整个镜城，陷入了前所未有的混乱"
    o "播放着甜蜜回忆的大厦，被播放着争吵的大厦猛烈撞击、吞噬"
    $ C += 4
    o "天空，在完美的日落与漆黑的暴雨之间疯狂闪烁"
    o "在这片如同末日般的景象中央，一切向下塌陷"
    o "从城市的地基中，一个白色的巨蛋逆流而上"
    o "实验体 v1 正趴在上边，轻轻抚摸"
    show qny
    show rush11
    v1 "我见到的那只鸟，它就在这里面，在我温暖的蛋里面"
    menu:
        "无视，这颗蛋我见过，到底是什么时候的事呢，算了":
            jump afterdeath
        "砸烂，蛋这种东西，若不破开来，就不会知道里面有什么":
            jump realization

label afterdeath:
    o "你拒绝"
    scene mirror_rain_effect with dissolve
    o "你看着它，就像看着自己过去写下的多愁善感"
    $ C += 2
    $ S += 3
    o "就像看着自己曾经坚信不疑的的海枯石烂，看着那个遭受挫折就以为天塌下来的自己"
    o "厌倦了去分辨真假，厌倦了去定义希望"
    o "厌倦了在这座由你自己的内心构筑的迷宫里，永无止境地追逐或逃避"
    show qy
    show angry11
    p "……够了，都结束吧"
    o "你在崩塌以前走到了出口，虽然一路满身荆棘，但也算胜利了"
    p "消散吧"
    scene mirror_rain_effect with dissolve
    o "达成HE：劫后余生，获得4个印章"
    return

label realization:
    o "在经历了所有欺骗，所有背叛之后，你不再轻易相信这种空中楼阁"
    o "越是美丽的东西，其内核恶毒起来就愈是可怖"
    $ S += 5
    $ C += 5
    $ F += 3
    o "蛋，应声而碎"
    scene inegg_rain
    o "里面，没有天使，没有怪物，也没有更深层的阴谋"
    o "里面，什么都没有"
    o "也就是说，这座你内心建立起来的城市中，也许只有那些废铁，才是你的归宿了"
    o "你没有放过任何人"
    o "包括你自己"
    o "至少你知道，你的幸福瞬间，终于浮出水面了"
    o "当你不再对希望本身抱有任何希望时，你才获得了真正意义上的自由"
    scene fractal_background with dissolve
    o "达成隐藏真结局：以心证道，获得5个印章"
    o "同伴也获得5章且接下来一组两人无视结局获得5印章"
    return

label DaoToFlesh:
    scene thedoor
    show alss
    o "其实，一个人无论是保持自我还是选择牺牲自己，都是一种不完整的答案"
    o "你们的选择是超越简单的二元对立，本就生而为一"
    alisa "太初有道，道与神同在，道成了肉身，住在我们中间"
    o "在她话音落下的瞬间，你们化作了两道金色的光"
    scene phos with dissolve
    o "不再是相互谦让，也不是相互争取"
    o "而是如同两股水流，自然地相互缠绕，最终，融合成了散发着温润光芒的存在"
    scene black
    pause 0.5
    scene doomroom with dissolve
    $ F += 6
    $ H += 6
    show qy
    o "你睁开眼，发现自己躺在床上，没有天旋地转，没有光怪陆离，一切都和离开时一模一样"
    o "窗外，是新一天清晨的阳光，温暖地，照在你的脸上"
    o "达成隐藏真结局：道成肉身，获得5个印章"
    o "同伴也获得5章且接下来一组两人无视结局获得5印章"
    return

label scene_56:
    $ my_brc = 5.6
    o "犹豫再三，你选择"
    o "你走向那片大陆"
    scene iron with dissolve
    o "废弃的金属板和齿轮随意拼接而成的的地面，史前巨兽骸骨般的起重机在浓雾中若隐若现"
    o "它们巨大的抓钩，不时地从你头顶掠过，把记忆里的废渣，投入到远处那日夜不息的熔炉之中"
    o "这里没有霓虹，唯一的光源是那些闪烁着不稳定电弧的真空管，和熔炉偶尔喷溅出的铁水"
    o "你找到了一根派克钢笔，那是疲于生计的父亲第一次送给孩子的礼物"
    o "你找到了一个生锈的奖杯，那是和小学同学一起打比赛获得的奖章"
    o "你找到了一张褪色的全家福，长大以后的你变得报喜不报忧，有时甚至会忘记了他们"
    o "在你那段失败的恋情之外，你的人生，原来还拥有过这么多其他的美好"
    show qy at walk32
    o "在熔炉的出口处，你意外找到一个黑色的魔盒"
    o "这座城市将它标记为潘多拉，在古语里，意为被赐予一切的人，你希望看到什么呢"
    menu:
        "她的心意（※）":
            $ favorability -= 10
            $ my_action = 1
            jump j5_3
        "我的心意":
            $ favorability -= 15
            $ my_action = 2
            jump j5_3
        "共同的回忆（end）":
            $ favorability += 15
            $ my_action = 3
            jump j5_3   

label scene_57:
    scene iron with dissolve
    o "犹豫再三，你选择"
    o "盒子里面静静地躺着一枚由银色雕刻着你们名字首字母的简陋戒指"
    o "那是一个普通的周末，你们在手工银饰店，你亲手为她打磨、刻下的"
    o "它不值钱，却凝聚了你当时全部的心意"
    show qny
    v1 "这是什么？"
    menu:
        "这是曾经的我对你的心意":
            $ favorability -= 20
            jump elysia
        "都结束了，不重要了":
            $ favorability -= 40
            jump datadst

label elysia:
    o "你选择了承认，并赠予"
    o "你拿起那枚戒指，没有丝毫犹豫，轻轻地放在了她的手心"
    $ H += 2
    p "这是，曾经的我，对‘你’的心意"
    v1 "？"
    hide qny
    show qy
    show steam11
    o "你释然了"
    o "重要的不是过去的那个人如何看待你的付出，而是付出这个行为本身，依然是有价值的"
    o "你将那段沉重的过去，变成了一份轻盈的礼物，赠予了一个无瑕的机械生命"
    o "正如你们还在一起的时候，你们会有一种错觉，对方是彼此的无瑕之人"
    o "达成HE：爱莉希雅，获得4个印章"
    return

label datadst:
    $ favorability = 0
    p "都结束了，以前的事情已经不重要了"
    $ C += 2
    o "实验体 v1 将那枚承载着你们心意的礼物连同那个开启它的黑色魔盒，一同扔进了熔炉之中"
    scene firefire with dissolve
    o "礼物在暗红色的记忆铁水中，瞬间气化，接着是她自己"
    scene doomroom with dissolve
    o "你回到了宿舍的被窝当中"
    o "达成NE：数据湮灭，获得3个印章"
    return

label scene_58:
    scene iron with dissolve
    o "犹豫再三，你选择"
    o "盒子里静静地躺着一件定制的摆件，是她为你亲手做的纪念日礼物"
    o "那是你们的纪念日，她神神秘秘地，作为礼物送给你的"
    o "摆件是你们两人的 Q 版卡通形象，手牵着手，脚下是一片青翠的草地"
    show qny
    v1 "这是什么？"
    menu:
        "这是曾经的你对我的心意":
            $ favorability += 20
            jump undone
        "都结束了，不重要了":
            $ favorability -= 40
            jump datadst

label undone:
    o "你拿起那个水晶摆件，没有丝毫犹豫，将其轻轻地，放在了实验体 v1 的手心"
    p "这是曾经的你，对我的心意"
    $ H += 2
    o "她抬起头，看着你"
    hide qny
    show qnys
    o "她的脸上，模拟出了一个虽笨拙，但却真诚的微笑"
    o "你释然了"
    o "重要的不是那个关于未来的约定是否实现，而是用心本身，曾真实地存在过"
    o "常言道：人有有味是清欢"
    o "达成HE：未竟之约，获得4个印章"
    return

label scene_59:
    $ my_brc = 5.9
    o "犹豫再三，你发现"
    $ E += 2
    o "她消失了"
    scene linkroad with dissolve
    show qy at walk32
    o "你在这座空旷的城市里开始徒劳的寻找"
    o "你曾无比憎恨世界的虚假，但当这里只有你一人时，你才感到惨绝人寰的孤独"
    o "你找了一天，或是一个世纪"
    o "直到你抬头，看到最高处的纪念碑，此刻已经附上的一层白色的羽毛状流体"
    o "岩石变成了一颗蛋"
    o "你穿过了那层如同薄雾般的流体外壳，走进蛋的内部"
    scene inegg with dissolve
    o "万籁俱寂"
    o "她正蜷在阴影中，紧紧地，抱着一颗小小的蛋"
    show qny
    v1 "（梦呓般的喃喃自语）"
    menu:
        "安抚（※）":
            $ favorability -= 25
            $ my_action = 1
            jump j5_3
        "谎言构筑的海市蜃楼才是罪魁祸首":
            $ favorability -= 25
            $ my_action = 2
            jump j5_3
        "砸烂这个蛋，抛瓦！（end）":
            $ favorability = 0
            $ my_action = 3
            jump j5_3

label scene_510:
    $ my_brc = 51.0
    scene linkroad with dissolve
    o "犹豫再三，你发现"
    o "她消失了"
    $ E += 2
    show qy at walk32
    o "你在这座空旷的城市里开始徒劳的寻找"
    o "你曾无比憎恨世界的虚假，但当这里只有你一人时，你才感到惨绝人寰的孤独"
    o "你找了一天，或是一个世纪"
    o "直到你抬头，看到最高处的纪念碑，此刻已经附上的一层白色的羽毛状流体"
    o "岩石变成了一颗蛋"
    scene inegg with dissolve
    o "你走近这个蛋，透过那层半透明的外壳"
    o "你看到实验体 v1 正蜷缩在巨蛋的中心，如同一个未出生的胎儿"
    o "就在你伸出手，试图触碰那冰冷的蛋壳时"
    o "你的视网膜上，弹出了一个覆盖了整个视野的指令界面"
    scene warningscreen with dissolve
    o "（机械女声）位面即将重构，请选择指令"
    menu:
        ">RST -t ALL -save_pt = Savepoint_Alpha（什么也不做，※）":
            $ favorability += 25
            $ my_action = 1
            jump j5_3
        ">DEL -t=v1 -str = observer（删除实验体）":
            $ favorability = 0
            $ my_action = 2
            jump j5_3
        ">DEL -t=observer -str = v1（删除自己，end）":
            $ favorability = 100
            $ my_action = 3
            jump j5_3

label scene_511:
    scene inegg with dissolve
    o "犹豫再三，你选择"
    $ S += 2
    o "你轻轻在她身边蹲下，她似乎感受到了你的存在，抬起头，眼中不再有数据流，只有类似孩童的迷惘"
    show qny
    show rush11
    v1 "你听到了吗？里面……有希望的声音"
    o "你仔细倾听，只能听到自己那沉重的心跳"
    show rush11
    v1 "请你相信我，相信我……能听到蛋里的声音，好吗？"
    menu:
        "我听到我的梦，微微破碎":
            $ L += 5
            $ favorability -= 15
            jump RainWorld
        "我听到,翅膀拍打的声音":
            $ F += 5
            $ H += 3
            $ favorability -= 15
            jump ThereIsAFish

label RainWorld:
    show steam11
    v1 "（悲伤）是吗？原来，美梦也可以只是泡沫"
    $ L += 3
    o "她没有再理你，更紧张地抱住了那颗光芒正在逐渐暗淡的蛋"
    o "你终究，还是没能走进她的世界"
    o "理性与清醒，往往是快刀"
    o "你们不可能回到某个午后的簕杜鹃花丛下躲藏，不被命运找到"
    scene inegg_rain with dissolve
    o "达成NE：世界淋漓，获得3个印章"
    return

label ThereIsAFish:
    scene inegg with dissolve
    show qnys
    show happy11
    v1 "(迸发光彩) 真的吗！你也听到了！"
    $ L += 4
    $ H += 2
    o "你想起了北海的巨鲲，与那翼若垂天之云的鹏鸟"
    o "你想起了西王母的昆仑，与那通往长生之境的天池"
    o "你想起了庄周梦中，那只不知是真是幻的蝴蝶"
    o "你情不自禁向她讲述这些"
    o "在你的讲述声中，她怀里的那颗核心之蛋，光芒越来越盛，与你的话语同频共振"
    o "最终，蛋壳无声地裂开"
    o "从中飞出的，不是什么遮天蔽日的神鸟，而是一只纯白的蝴蝶"
    scene white with dissolve
    o "光点所到之处，这颗囚禁着你们的蛋，如冰雪消融"
    o "你找回了自由，甚至感觉有飞翔的可能性"
    o "达成HE：北冥有鱼，获得4个印章"
    return

label scene_512:
    o "问题的根源，不在于她，而在于这个早已崩溃的世界"
    o "你决定，先修复你们赖以存在的“海市蜃楼”。但似乎，已经有些晚了"
    menu:
        "坚持修复,我命由我不由天":
            jump SeeUAgain
        "不如修复废土，爱你老妈明天见":
            jump Never2Late

label SeeUAgain:
    v1 "为什么要做到这一步？你知道，这只是把毁灭推迟了微不足道的几分钟"
    o "她看着你，眼中不再是程序的冷漠，而是一种带着痛楚的动容"
    hide qny
    show qy
    p "因为哪怕只是几分钟，也是属于我们的最后的永恒"
    $ favorability = 80
    scene cityinroom with dissolve
    o "在这个被你强行续命的的黄昏里，她走上前，轻轻拥抱了你，这一刻你们不再是仇人"
    $ L -= 5
    $ H += 4
    $ S += 2
    o "你很清楚，这并非真正的永恒，这只是一场无限拉长的告别"
    show qnys
    o "但至少在此刻，在这场没有终点的告别中，你是这个世界的暴君，也是她唯一的骑士"
    o "（机械女声）系统提示：连接已超时"
    o "在时隙废都中，你们互道晚安"
    o "达成HE：漫长的告别，获得4个印章"

label Never2Late:
    o "你来到最底下，这是你唯一能补救的地方了吧，你想"
    scene iron with dissolve
    o "你弯下腰，从那些散落一地的玻璃碎片下，挖出一捧真实的泥土"
    show qnys
    v1 "你还是醒了"
    $ S += 3
    hide qnys
    show qy
    p "是的，我们都醒了"
    p "我们依然要面对寒风，面对饥饿，面对这个千疮百孔的世界"
    p "梦醒了。但我们还在"
    hide qy
    o "夕阳照亮了脚下的废土，也照亮了那些在之前的轮回中，被你们种下的、以为早已死去的种子"
    o "废铁城的缝隙里，也能长出小花小草"
    o "真正值得修复的，从来不是那座虚幻的空中楼阁，而是这片虽然贫瘠却孕育着无限可能的脚下土地，那才是你的来时路"
    o "莫道桑榆晚，为霞尚满天"
    o "达成TE：桑榆非晚，获得5个印章"
    return

label scene_6:
    scene fractal_background
    o "注：接下来的第一个选项是更危险，第二个选项是折衷，第三个选项是双方自爆"
    pause 1.2
    scene threeroad with dissolve
    $ H = E = S = C = F = L = 10
    $ favorability = 0
    $ my_plane = 6
    show qy
    o "你睁开眼，发现自己正站在一片被冥界的蓝色月光所笼罩的十字路口"
    o "你并非孤身一人"
    o "在你的身旁，站着另一个你——同样的相貌，同样的衣着，眼中带着与你如出一辙的迷惘"
    show why11
    p "欸？"
    o "在十字路口的中央，一位身着黑袍的女神，静静伫立着"
    o "她的面容被兜帽的阴影所笼罩，看不真切"
    o "她的火烛，是这片冥界中唯一的光源"
    o "那火散发出一种反常识的冰冷，只能照亮现实，却无法带来温暖"
    hide qy
    show HKT1 with dissolve
    hecate "(古老而威严)迷途之人啊，请循心所来"
    hecate "向后，是通往过去的宽路，那里有你们渴望的一切慰藉，但尽头是永恒的沉沦"
    hecate "现在，你们也许应该向前，或走向两旁"
    menu:
        "踏入那条流淌着焦油的停滞之路（※）":
            $ favorability += 25
            $ my_action = 1
            jump j6_1
        "踏上玄武岩与白骨镶嵌而成的窄路":
            $ favorability += 10
            $ my_action = 2
            jump j6_1
        "转身踏上通往美好回忆的康庄大道（end）":
            $ my_action = 3
            jump j6_1

label road_eyes:
    hecate "凡回望过去者，必将化为盐柱"
    scene bat_mount with dissolve
    pause 1.0
    o "你们没有理会这句谶言，轻松走到了路的尽头"
    scene cityinroom with dissolve
    $ L += 10
    $ S += 10
    o "这里，就是你梦想中的世界，你和你爱的人，以及所有爱你的人，永远地生活在一起"
    o "每一天，都重复着你记忆中最幸福的那些瞬间，这里没有争吵，没有背叛，没有痛苦"
    o "那么代价是什么呢？"
    o "你们很快就发现，你们是一分为二的意识，却无法再进行交流，也就是，丧失了碰撞出新火花的可能性"
    o "你们成了这个完美世界里，两个被剥夺了自由意志的囚徒"
    o "你们会在完美的家庭聚餐上，用空洞的眼神相互凝视，数那眨眼的频率"
    o "你们会在完美的林荫道上散步时，一前一后，用彼此影子的长度，来猜测对方的心意"
    o "你们是这个世界上最亲密的狱友，也是最遥远的陌生人"
    o "达成BE：道路以目，获得2个印章"
    return

label j6_1:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False
    if opponent_action == 3 or my_action == 3:
        jump road_eyes
    elif opponent_action == 2 and my_action == 2:
        jump scene_61
    else:
        jump scene_62

label scene_61:
    $ my_brc = 6.1
    scene nrroad with dissolve
    o "你们都选择踏上了那条崎岖的小路，用灵魂重新体验一次那些不堪回首的瞬间"
    $ H += 3
    $ C += 2
    o "就在你们几乎要被这份痛苦压垮时，前方，出现了一位身着纯白长裙的少女，面容酷似赫卡忒"
    o "却散发着一种悲悯而温柔的气息"
    show als with dissolve
    alisa "我听到了你们的悲，你们已然背负太多"
    o "她指向你们的身后。你们发现，各自的背上，不知怎的多了一个硕大的行囊"
    o "你们几乎不可能背着过去，为了迈向新生，你们必须丢弃一些东西"
    o "她指向路旁奔流不息的冥界之河"
    menu:
        "丢掉甜蜜（※）":
            $ favorability += 25
            $ my_action = 1
            jump j6_2
        "他们都是我的一部分":
            $ favorability += 10
            $ my_action = 2
            jump j6_2
        "丢掉痛苦（end）":
            $ my_action = 3
            jump j6_2

label scene_62:
    $ my_brc = 6.2
    scene throne with dissolve
    o "你们中有人选择了停滞现在的道路"
    $ F -= 3
    $ E += 2
    o "这条河流液体冰冷、粘稠，却有着诡异的浮力，你们感到自己的身体正在被分解，意识正在被溶解"
    o "没走多远，一个声音，一个充满了孩童般、不加掩饰的欲望的声音，在你们耳边响起"
    show qy3 with fade
    third_me "你们……终于……回来了啊"
    o "你们看到，在那黑色河流的中央，一个由黑色焦油构成的王座之上，端坐着第三个你"
    o "他脸上带着一种满足而狰狞的狞笑"
    third_me "你们一个总是想着怎么活下去，另一个又总是想着怎么活得正确"
    third_me "无聊透顶…为什么错的不能是这个世界呢"
    third_me "不过在我这里，你们的欲望都能被满足，来选一个愿望吧"
    menu:
        "……（※）":
            $ favorability += 25
            $ my_action = 1
            jump j6_2
        "我们不需要":
            $ favorability += 20
            $ my_action = 2
            jump j6_2
        "错的是整个世界！（end）":
            $ my_action = 3
            jump j6_2  

label j6_2:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False
    if my_brc == 6.1:
        if opponent_action == 3 or my_action == 3:
            jump NotAbout
        elif opponent_action == 1:
            $ S += 3
            jump scene_63
        elif opponent_action == 2:
            $ H += 2
            jump scene_64
            
    elif my_brc == 6.2:
        if opponent_action == 3 or my_action == 3:
            jump InMyBone
        elif opponent_action == 1:
            $ L += 2
            jump scene_65
        elif opponent_action == 2:
            $ H += 2
            jump scene_66

label InMyBone:
    p "错的不是我，而是整个世界！"
    $ E = 20
    $ stream_hearts()
    third_me "（狂喜）如你所愿！"
    o "他将自己的身体，融入了你的身体之中"
    o "自我、超我与本我，在这一刻达成了三位一体"
    o "你想颠覆全世界"
    scene cityinroom with dissolve
    o "第一步，你诅咒曾经欺负过你的人，此后处处碰壁，无论是求学、升职、求偶"
    o "下一步，用金钱报答从小对你严厉的父母，你会为他们买下最奢华、却永远没有你身影的的房子"
    o "最后，你会不经意地与那个她再次相遇，伪装出一名绅士，有着傲慢的礼仪"
    o "在你那场空无一人的婚礼上，你看着脚下城市的万家灯火，已经感觉不到任何快乐了"
    o "达成NE：刻骨铭心，获得3个印章"
    return

label NotAbout:
    scene nrroad with dissolve
    o "你们一同卸下行囊，将不喜欢的瞬间掷入水中"
    o "碎片入水的瞬间，没有泛起任何涟漪"
    o "你们感到自己的灵魂，变得前所未有的轻盈。脚下那些锋利的碎石，似乎也不再那么刺痛了"
    $ F += 5
    $ C += 5
    show als
    show steam11
    alisa "只留下甜蜜的回忆，只会让你们对过去更加留恋"
    o "当下你没有发现，所有美好的东西，都还在。区别在于，它们都失去了参照物"
    o "没有了痛苦作为对比，甜蜜，也变得索然无味"
    o "没有了失去的恐惧，拥有，也变得无关痛痒"
    o "直到若干年后，你还活着，你能行动，你会微笑，但一切，都无关痛痒"
    o "达成NE：无关痛痒，获得3个印章"
    return

label scene_63:
    $ my_brc = 6.3
    scene nrroad with dissolve
    o "你们将行囊中所有温暖的、闪光的、甜味的碎片，都毫不犹豫地扔进了冥界之河"
    show als with dissolve
    alisa "哀恸的人有福了，因为他们必得安慰"
    scene bat_mount with dissolve
    pause 1.2
    scene nrroad with dissolve
    show qy at walk32
    o "你们的每一步，都变得更加沉重和煎熬"
    $ L += 2
    $ H += 3
    o "但出乎意料的是，前方的道路，只要不断前进，道路就会变得越来越宽阔"
    o "你们走到了冥界之河的下游，河水平缓，河岸是一片由洁白沙石构成的滩涂"
    hide qy
    o "那些被丢弃的碎片，在被河水冲刷磨去了所有尖锐的棱角后，如同美丽的鹅卵石，重新冲刷上岸"
    show als with dissolve
    alisa "现在你们可以选择，是否要将它们捡回来"
    menu:
        "接受（※）":
            $ favorability += 25
            $ my_action = 1
            jump j6_3
        "和对方一样":
            $ favorability += 20
            $ my_action = 2
            jump j6_3
        "拒绝（end）":
            $ my_action = 3
            jump j6_3

label j6_3:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False

    if my_brc == 6.3:
        if opponent_action == 3 or my_action == 3:
            jump NotAbout
        elif opponent_action == 2 and my_action == 2:
            $ IfTogether = 1
            jump scene_67
        else:
            $ S += 3
            jump scene_67
    
    elif my_brc == 6.4:
        if opponent_action == 3 or my_action == 3:
            jump Boring
        elif opponent_action == 2 and my_action == 2:
            $ IfTogether = 1
            jump scene_67
        else:
            $ H += 2
            jump scene_67

    elif my_brc == 6.5:
        if opponent_action == 3 or my_action == 3:
            jump HowToEndWar
        elif opponent_action == 2 and my_action == 2:
            $ IfTogether = 1
            jump scene_68
        else:
            $ H += 2
            jump scene_69

    elif my_brc == 6.6:
        if opponent_action == 3 or my_action == 3:
            jump lpls
        elif opponent_action == 2 and my_action == 2:
            $ IfTogether = 1
            jump scene_67
        else:
            $ H += 2
            jump scene_69


label lpls:
    o "你回到了现实世界"
    scene doomroom with dissolve
    o "你不再拖延，不再焦虑，不再犯错"
    $ S = 20
    $ L = 20
    o "任何复杂的难题在你绝对的理性面前，都像是一加一等于二般简单"
    o "就像一个被格式化后的硬盘，干净，但死寂"
    o "你算尽了一切，却唯独算不出，下一次心动的概率"
    o "达成NE：拉普拉斯的恶魔，获得3个印章"
    return

label scene_64:
    $ my_brc = 6.4
    scene nrroad with dissolve
    show qy
    p "其实肩上再沉重也没事的，毕竟我们日常不也是经常要负重前行吗？"
    hide qy
    show als
    alisa "愚蠢，却也完整"
    scene bat_mount with dissolve
    o "旅途开始变得举步维艰，每一步，都像是在背负着整个世界，道路因为你们的沉重，而几乎无法通行"
    $ S += 3
    $ H += 3
    o "你们走到了冥界之河的中游"
    scene nrroad with dissolve
    o "阿莉莎停了下来，从奔流的河水中，为你们，捞起了一些你们早已遗忘的记忆碎片"
    show als with dissolve
    alisa "你们的行囊里，多数是一些近年的回忆了。但你们的人生，并非只有这些"
    o "她将那些碎片，捧到你们面前，有教室夏夜的风，有少年们的追逐，有父母笨拙的关怀"
    alisa "你们可以选择，是否要将这些被遗忘的也一并装入行囊"
    menu:
        "当然（※）":
            $ favorability += 25
            $ my_action = 1
            jump j6_3
        "和对方一样":
            $ favorability += 20
            $ my_action = 2
            jump j6_3
        "算了（end）":
            $ my_action = 3
            jump j6_3

label Boring:
    p "够了，已经足够沉重了，我没有多余的力气，再去承载这些无关紧要的东西了"
    $ E += 5
    $ L += 3
    o "最终，你们抵达了窄门的面前，和传说中不同，它可以让你们两个一起，你们快速通过，没有多想"
    o "你们回到了生活，一片更大的荒原"
    scene eatingstreet_bw with dissolve
    o "你看到恐惧在一把尘土里"
    o "你会结交新的朋友，参加热闹的聚会。觥筹交错间，你只听见街边步履匆匆"
    o "你看到他们那一张张涂脂抹粉的脸上，都戴着一副由欲望和恐惧构筑的面具"
    show qy at walk32
    p "人类，承受不了太多的真实"
    o "你学会用无聊的短视频填满夜晚，会用没有营养的社交辞令应付他人"
    o "你成功与最伟大的荒原共鸣了，哪怕代价是将最诚挚的告白赠予它"
    o "达成NE：百无聊赖，获得3个印章"
    return

label scene_65:
    $ my_brc = 6.5
    o "你们没有接受，也没有拒绝。你们沉默地看着这个欲望的具象体"
    $ H += 2
    show steam11
    third_me "哦？沉默吗。也好。沉默，代表着你们还在权衡，那么，我就给你们一些更具体的筹码吧"
    o "他打了个响指，黑色的河流中，浮现出两份闪耀着诱人光芒的契约"
    third_me "选吧。左边的这份，能让你们的人生，天堑变通途；右边的这份，忘却最深的忧伤"
    menu:
        "良知换真心（※）":
            $ favorability += 25
            $ my_action = 1
            jump j6_3
        "依然拒绝":
            $ favorability += 20
            $ my_action = 2
            jump j6_3
        "捷径换坚守（end）":
            $ my_action = 3
            jump j6_3    

label scene_66:
    $ my_brc = 6.6
    o "你们毫不犹豫地拒绝了那份来自本能的诱惑"
    $ H += 2
    show happy11
    third_me "有意思，你们排斥欲望，是因为你们自诩有那点可怜的理性，对吗？那么，我们来做个更有趣的交易吧"
    o "他打了个响指，浮现出两份新的契约"
    third_me "很简单，用你们身上那些无聊的情欲，来换取绝对的理性"
    third_me "或者，用你们自以为是的辩证，来换取永恒的安逸，又如何？"
    menu:
        "否定换安逸（※）":
            $ favorability += 25
            $ my_action = 1
            jump j6_3
        "依然拒绝":
            $ IfTogether = 1
            $ my_action = 2
            jump j6_3
        "情欲换理性（end）":
            $ my_action = 3
            jump j6_3    

label j6_4:
    $ make_sync_choice(my_action)
    $ wait_for_opponent_choice_1()
    while not opponent_has_chosen:
        $ renpy.pause(0.1, hard=True)
    $ renpy.hide_screen("waiting_screen")
    $ i_have_chosen = False
    $ opponent_has_chosen = False

    if opponent_action == 3 and my_action == 3:
        jump DaoToFlesh
    elif my_action == 2:
        jump AdAstra
    elif my_action == 1:
        $ S += 3
        jump PerAspera

label AdAstra:
    $ H += 3
    $ S += 3
    $ F += 4
    hide als
    show qy
    p "他比我更痛苦，他应该先获得解脱"
    p "他比我更勇敢，他应该先看到光明"
    hide qy
    show alss
    alisa "人为朋友舍命，人的爱心没有比这个大的"
    alisa "当你们的心中，不再只有自己时，你们，便已无需再穿过任何门了"
    o "在她话音落下的瞬间，那扇窄门如冰雪消融，化作满天繁星"
    scene starnest_effect with dissolve
    o "所有的岩石与白骨皆化作星尘，所有的河流与高山皆化作寰宇"
    o "你们伸出手轻轻触碰了一下对方的指尖"
    o "整个星空，开始向你们收束"
    o "整片星空，装回自己的心里"
    scene doomroom with dissolve
    o "你睁开眼，窗外，是深夜，原来凌晨三点前，其实路灯便已入眠"
    o "达成TE：终抵繁星，获得5个印章"
    return

label PerAspera:
    $ H += 3
    $ S += 3
    $ F += 4
    hide als
    show qy
    p "我已经背负了够多。现在，轮到我获得解脱了"
    p "我已经看清了所有。现在，我必须走出去，开始新的生活"
    hide qy
    show alss
    alisa "你们没有陷入自我牺牲的道德竞赛，没有因为谦让而停滞不前"
    o "在她话音落下的瞬间，那扇原本仅容一人的窄门，在你们面前，分裂、延拓，化作了白光"
    scene white with dissolve
    pause 0.6
    scene doomroom with dissolve
    show qy
    o "你在宿舍回过神来，想在纸上写点什么，却写出了意思相反的一句话"
    o "你听到了另一个你强而有力的回响"
    show happy11
    o "你们将会共用一副躯壳，继续这段艰苦的旅行"
    o "达成TE：循此苦旅，获得5个印章"
    return


label HowToEndWar:
    $ C += 5
    $ E += 5
    o "你厌倦了无休止的挣扎，厌倦了那个总是受伤、总是碰壁的自己"
    o "你渴望那种能够扫平一切障碍的力量"
    third_me "明智的选择。从今往后，你的世界将是一条笔直的大道"
    o "黑色的焦油顺着你的指尖向上蔓延，迅速包裹了你的全身"
    o "你没有感到窒息，反而感到一种绝对的掌控感"
    o "效率。这是你现在唯一的信条"
    o "你回望你走过的路，然而，入目所及，皆是焦土"
    o "这里确实再也没有了战争，因为这片废墟之上，只剩下了你一个独裁者"
    o "你赢了，但这片疮痍遍地的大地，便是你唯一的战利品"
    o "达成NE：疮痍遍地，何以止戈，获得3个印章"
    return

label scene_67:
    scene thedoor with dissolve
    o "无论如何，你们终于到了窄门的面前"
    $ H += 1
    $ F += 1
    o "它古朴、沉默，狭窄得仅容一人侧身通过"
    show als with dissolve
    alisa "你们要努力进窄门，将来有许多人想要进去，却是不能，门，只为一人开。告诉我，你们的选择"
    menu:
        "我先":
            $ my_action = 1
            jump j6_4
        "对方先":
            $ IfTogether = 1
            $ my_action = 2
            jump j6_4
        "与对方不同" if IfTogether == 1:
            $ my_action = 3
            jump j6_4

label scene_68:
    o "你选择了不再痛苦"
    $ E += 2
    $ S += 2
    o "就在你的手即将触碰到那份契约的瞬间，一道蓝色月光撕裂了这片黑暗的空间"
    scene black
    pause 0.5
    scene throne
    show HKT1 with dissolve
    hecate "你是必须被锁在迷宫最深处的米诺陶，你干扰了自我的超越"
    o "她举起火炬，准备将这个暴走的本我，彻底祓除，而第三个“我”，则惊恐地，向你们伸出了手"
    menu:
        "本我也是我的一部分，我必须正视我的欲望":
            $ my_action = 1
            jump cleanmirror
        "是啊，我早该告别本我了，我不该有这种想法":
            $ my_action = 2
            jump swordriver

label cleanmirror:
    $ H += 2
    $ S += 2
    o "你挡在那个瑟瑟发抖的“我”身前，直面着赫卡忒那神明般的威压"
    hide HKT1
    show qy
    p "感谢您的指引，女神，但我的超越，不应是靠着切除一部分的自己来完成"
    p "而是要学会如何与我这头名为‘欲望’的米诺陶，共存于同一座迷宫之中"
    hide qy
    show HKT1
    hecate "很好。你没有选择成为神，也没有选择成为兽，你，最终，选择成为了一个完整的人"
    o "她向你微微颔首，连同那片星空，一同消失了"
    hide HKT1
    o "你不再压抑你的欲望，也不再被你的欲望所奴役"
    o "你澄澈如镜，能清晰地照见自己所有的念头——无论善恶，你困于迷宫当中，却又做自己的君主"
    o "达成TE：澄心如镜，以召吾愿，获得5个印章"
    return

label swordriver:
    o "你彻底与欲望划清了界限"
    $ H += 2
    p "我早该告别本我了。我不该有这种想法"
    o " 在你话音落下的瞬间，赫卡忒的火焰锁链，彻底缚住了那个尖叫着的“我”，将他拖入了无尽的虚空之中"
    scene firefire with dissolve
    pause 0.75
    hecate "从今往后，你将不必被原始的欲望所困扰"
    scene plgrd
    o "你们的意识回归现实，如同一个手持利剑、永远站在深渊旁的守护者，成功斩杀了名为欲望的恶龙"
    o "唯一的代价是，失去了与龙共舞的生命力，虽说无可指摘，却也无可奈何"
    o "达成HE：执剑临渊，以斩腾蛟，获得4个印章"
    return

label scene_69:
    o "你动摇了"
    $ E += 3
    o "毕竟，这两份契约太过诱人"
    o "用那些只会带来麻烦的情欲，去换取永恒的理性"
    o "还是说，用那些不断内耗的自我否定，去换取一片风平浪静，这何乐而不为"
    o "就在你的指尖，即将触碰到那份契约时，一道冰冷的蓝色月光，撕裂了这条黑色河流"
    scene black
    pause 0.5
    scene throne
    show HKT1 with dissolve
    hecate "你是必须被锁在迷宫最深处的米诺陶，你干扰了自我的超越"
    o "她举起火炬，准备将这个暴走的本我，彻底祓除，而第三个“我”，则惊恐地，向你们伸出了手"  
    o "你才反应过来，这本身也是一道考验"
    menu:
        "不是由你们两个说了算的":
            $ my_action = 1
            jump prometheus
        "沉默接受一切":
            $ my_action = 2
            jump byother

label prometheus:
    o "无论是神，还是魔，你选择拥抱自己的傲慢"
    $ H += 2
    $ F += 2
    p "这一切，不是由你们两个说了算的"
    p "（对赫卡忒）我的理性，应当是我从无数的错误与冲动中，亲手磨砺出的宝石"
    p "而不是靠祓除，换来的廉价水晶"
    p "（对第三个我）而你，也不是我的主人，你只是我内心永远不会熄灭的火焰"
    p "我可以利用你的热量，但绝不会，被你烧成灰烬"
    hecate "很好，你已无需再被任何人救赎，也无需再向任何人乞讨"
    hecate "去吧，去把你自己的那份火焰，带回人间吧"
    scene fractal_jewel with dissolve
    o "他们一同消失在了你的人格深处，他们回归到了各自应在的位置"
    o "一个在灯塔之上，一个在深海之下"
    scene doomroom with dissolve
    o "你走到窗边，看着楼下那盏准时亮起的、曾让你感到无比孤独的米黄色路灯"
    o "你的手机响起，是朋友发来的消息：晚上出来吃饭吗？老地方"
    o "达成隐藏真结局：普罗米修斯，获得5个印章"
    o "同伴也获得5章且接下来一组两人无视结局获得5印章"
    return

label byother:
    o "你放弃了抵抗，也放弃了选择"
    $ E += 2
    $ F += 2
    o "赫卡忒的火焰锁链，在你默许的注视下，彻底缚住了那个尖叫着的你，将他拖入了无尽的虚空之中"
    scene firefire with dissolve
    hecate "从今往后，你将不再被原始的欲望所困扰"
    o "那份曾让你痛苦的情欲和内耗，连同那份最原始的生命力，都一同被带走了"
    scene doomroom with dissolve
    o "你的意识回归现实"
    o "你睁开眼，发现自己回到了宿舍"
    o "窗外，是清晨，阳光明媚，鸟语花香"
    o "一切都显得那么正确"
    o "达成HE：因人之力，获得4个印章"
    return