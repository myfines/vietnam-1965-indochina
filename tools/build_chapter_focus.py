"""Three event-driven PKS narrative lanes, mirrored after the SVN union."""
from pathlib import Path
import re
import sys,json
from build_campaign import M, R, put
from long_foundation import loc_text
sys.path.insert(0, str(R / "vendor"))
import pdx

# Chapter markers distinguish novel-derived scenes from alternate playable choices.
ROUTES = {
    "reports": {
        "title": "战报生意",
        "focuses": [
            ("first_report", "归仁的第一份捷报", "把阮家村战斗写成上级能看见的战果；每个数字都可能换来下一份任务。", "ledger", "1–10", None),
            ("casualty_ledger", "另立伤亡账", "一份报表交给司令部，另一份留给营地；隐去损失会让下一次增援继续落空。", "ledger", "22–27", 100),
            ("share_credit", "把功劳分给签字的人", "蔡命新、参谋与合作部队都在战报里留下名字，战果也成了讨价还价的筹码。", "contracts", "28–42, 61–62", 101),
            ("media_contract", "把英雄故事卖给日海", "电影和报纸能把战功讲得更久；故事越大，往后越需要新的胜利来支撑。", "contracts", "17, 108", 102),
            ("procurement", "把战果换成采购合同", "美援采购和军需承包连起前线与韩国工厂，利润能养兵，也会引来审查。", "contracts", "30–37, 62", None),
            ("fact_check", "保留一份真实记录", "把空袭、俘虏与阵亡分开登记；参谋部不必接受全部真相，但不能失去核对依据。", "command", "45–55, 75, 93–99", None),
            ("legacy", "让战报替本部说话", "给不同上级不同版本的胜利，维持日海合同与军官任命之间的平衡。", "ledger", "86–87, 101–107", None),
        ],
    },
    "relations": {
        "title": "跨军区私人关系",
        "focuses": [
            ("officer_circle", "陆士同期的联络圈", "同学、前辈和晋升者构成一张可调动的关系网，彼此都期待在战果里占一份。", "command", "21, 28–31, 113–114", None),
            ("patronage", "用职位换取支持", "让参谋、警卫与情报官各有去处，私人忠诚就能转化为部队里的实际权限。", "command", "31–40, 70–74", 110),
            ("cia_channel", "接通CIA越南站", "共享情报、空袭与战果的署名，换来美方庇护和日海工业投资。", "contracts", "61–63", 111),
            ("south_partners", "让南越军官入账", "地方军官需要军饷和装备，本部需要人手、港口和可被调用的番号。", "proxy", "64–67, 74, 100–102", 112),
            ("special_command", "建立直属指挥渠道", "特战司绕过常规军区程序后行动更快，也更依赖总统与朴系亲信的信任。", "command", "63, 70–74", None),
            ("militia_terms", "以土地和头衔招揽团练", "地方土豪愿意出钱出人，但会要求武器、辖权和家族安全作为交换。", "proxy", "137–140", 113),
            ("network_compact", "把关系写成长期承诺", "让各方在调兵、军饷和采购上有固定份额，保住网络也意味着要持续分账。", "contracts", "65–67, 110–114, 137–140", None),
        ],
    },
    "island": {
        "title": "私人生活与海岛",
        "focuses": [
            ("comfort_budget", "把军营过成官邸", "朴把日常事务交给亲信处理，留下时间安排私人起居；舒适生活需要稳定现金流。", "contracts", "26, 29–30, 108–110", 120),
            ("music_room", "留一间安静的休息室", "唱片、烟酒和清静的房间都能成为战地生活的一部分；经费也可以留给士兵。", "ledger", "29, 41, 108", 121),
            ("private_dining", "只请熟人赴宴", "一桌饭菜能维持亲信间的熟络，也能把日海合同和军中人事放到同一张桌上。", "contracts", "37–40, 59–60, 76–80", 122),
            ("household", "安排官邸日常", "女仆、警卫和司机让司令官的生活运转顺畅；薪酬与用人方式会影响外界观感。", "command", "3, 26, 29–30, 108", None),
            ("phu_quoc_plan", "把富国岛留作后方", "华人移民、训练基地和港口相互支撑，岛上职位也成为分配利益的新入口。", "port", "63–67, 74–75, 97–102", 123),
            ("island_estate", "给日海留一块码头", "军队轮训需要船期和仓库，财团则希望在岛上的货物流转中拿到稳定份额。", "port", "74, 85, 97–102, 110, 133–135", None),
            ("quiet_harbor", "建一处能继续经营的港口", "无论战线如何变化，岛上的基地、代理人和合同都能让朴系保持影响力。", "proxy", "68–74, 122–140", None),
        ],
    },
}

EVENTS = {
    100: {
        "title": "市府缴获的钱怎么分",
        "desc": "城里缴获的一笔巨款摆在桌上：军需官要补给，地方军官要分成，日海的人则已经带来一只‘代管’账箱。朴可以把账留在自己人手里，也可以先喂饱地方武装，省得他们另找收入。",
        "options": [
            ("交日海代管，底账留在司令部", "SVN = { add_to_variable = { v65_private_wealth = 12 v65_network_SVN = 5 v65_network_KHM = 8 } } add_to_variable = { v65_paper_victories = 1 } add_political_power = 15"),
            ("给地方军官分成，免得他们自筹", "SVN = { add_to_variable = { v65_network_DNM = 5 v65_network_HLC = 8 v65_network_MKG = 8 v65_network_BHD = 5 } } add_manpower = 1000 add_to_variable = { v65_personal_network = 2 }"),
        ],
        "source": "第51章",
    },
    101: {
        "title": "谁拿走空缺的战功",
        "desc": "阵亡、缴获和宣传稿各有一本账。把战功挂在中央军官名下，能换来下一季任命；让南越协同部队分走名额，则有人替朴守住地方征募和军需通道。",
        "options": [
            ("给蔡系军官留足晋升名额", "SVN = { add_to_variable = { v65_network_SVN = 10 v65_private_wealth = 5 } } add_to_variable = { v65_paper_victories = 2 } add_political_power = 20"),
            ("把署名与军需份额给盟军", "SVN = { add_to_variable = { v65_network_DNM = 8 v65_network_HLC = 5 v65_network_MKG = 5 v65_private_wealth = 3 } } add_to_variable = { v65_personal_network = 2 } add_manpower = 1000"),
        ],
        "source": "第45–62章",
    },
    102: {
        "title": "把宋康茂拍成英雄",
        "desc": "日海映像想把未经核实的战报拍成连续电影。观众会记住英雄，也可能记住片尾滚过的捐款与阵亡名单。",
        "options": [
            ("拍摄英雄系列片", "SVN = { add_to_variable = { v65_private_wealth = 10 } add_to_variable = { v65_private_comfort = 5 } add_to_variable = { v65_network_SVN = 5 } } add_stability = 0.03"),
            ("改拍部队纪实片", "SVN = { add_to_variable = { v65_network_SVN = 5 } add_to_variable = { v65_network_DNM = 5 } } army_experience = 10"),
        ],
        "source": "第17、78–79、108章",
    },
    110: {
        "title": "任命谁来守住关系网",
        "desc": "空输、情报和后勤军官都要求独立权限。亲信职位有限，选择会决定朴系将来更依靠中央军官还是地方代理。",
        "options": [
            ("把名额留给中央参谋", "SVN = { add_to_variable = { v65_network_SVN = 10 } add_to_variable = { v65_network_DNM = 5 } } add_command_power = 15"),
            ("让地方联络官带队", "SVN = { add_to_variable = { v65_network_HLC = 8 } add_to_variable = { v65_network_MKG = 8 } add_to_variable = { v65_network_BHD = 5 } } add_manpower = 1200"),
        ],
        "source": "第31–40、70–74、113–114章",
    },
    111: {
        "title": "与谁共享机密渠道",
        "desc": "CIA愿以庇护和工业投资换取情报与战果；富国岛军政长官则要求更多补给。两条关系都能用，资源却有限。",
        "options": [
            ("优先经营美方渠道", "SVN = { add_to_variable = { v65_network_SVN = 8 } add_to_variable = { v65_private_wealth = 12 } } add_political_power = 25"),
            ("把权限交给岛上代理", "SVN = { add_to_variable = { v65_network_PHQ = 12 } add_to_variable = { v65_network_KHM = 5 } } add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 500 producer = ROOT }"),
        ],
        "source": "第61–67、74、97–102章",
    },
    112: {
        "title": "接受南越军官的条件",
        "desc": "南越军官愿意交出兵员与地方头衔，但要求优先获得武器和家属保护。答应之后，归仁之外的武装也会有自己的主张。",
        "options": [
            ("给地方军官武器份额", "SVN = { add_to_variable = { v65_network_BHD = 8 } add_to_variable = { v65_network_MKG = 8 } add_to_variable = { v65_private_wealth = 5 } } add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 600 producer = ROOT }"),
            ("保留军火与任命权", "SVN = { add_to_variable = { v65_network_SVN = 10 } add_to_variable = { v65_network_PHQ = 4 } } add_political_power = 30"),
        ],
        "source": "第64–67、100–102、137–140章",
    },
    113: {
        "title": "团练要不要自己选头领",
        "desc": "地主愿意出钱组织地方武装，条件是头衔与指挥权按家产和贡献分配。中央可以接受这套秩序，也可以坚持统一任命。",
        "options": [
            ("承认地主推举的团练头领", "SVN = { add_to_variable = { v65_network_HLC = 8 } add_to_variable = { v65_network_MKG = 8 } add_to_variable = { v65_network_BHD = 8 } add_to_variable = { v65_private_wealth = 8 } } add_manpower = 2000"),
            ("团练归南越军区统一编组", "SVN = { add_to_variable = { v65_network_SVN = 10 } add_to_variable = { v65_network_DNM = 5 } } army_experience = 15"),
        ],
        "source": "第137–140章",
    },
    120: {
        "title": "三十分钟的每日简报",
        "desc": "第108章里朴把日常事务交给副官，每天只花半小时到一小时看概要，剩下时间留给自己；他抽着烟看窗外，还觉得特战司令官的日子过得太舒服。",
        "options": [
            ("继续把杂务交给副官", "SVN = { add_to_variable = { v65_private_comfort = 12 } add_to_variable = { v65_private_wealth = -4 } } add_political_power = 10"),
            ("把简报时间还给前线轮值", "SVN = { add_to_variable = { v65_network_SVN = 5 } } army_experience = 8"),
        ],
        "source": "第108章",
    },
    121: {
        "title": "归仁码头的遮阳伞",
        "desc": "第41章里朴在归仁码头钓鱼，遮阳伞下有越南女仆和警卫；他照着一份夸大的战绩簿，把这趟闲钓也过成司令官的待遇。",
        "options": [
            ("让警卫继续守着钓点", "SVN = { add_to_variable = { v65_private_comfort = 12 } add_to_variable = { v65_private_wealth = -5 } } add_political_power = 8"),
            ("借出行检查港口值勤", "SVN = { add_to_variable = { v65_network_PHQ = 6 v65_network_DNM = 3 } } army_experience = 8"),
        ],
        "source": "第41章",
    },
    122: {
        "title": "穿便服的庆功会",
        "desc": "第115章，延坪岛炮击回应乏力，朴世诚却和金勇培换上便服办起‘庆功会’。自掏腰包继续庆祝，或者让日海替这场胜利布置场面、收走宣传收益。",
        "options": [
            ("照旧庆祝，战报别提效果", "SVN = { add_to_variable = { v65_private_comfort = 10 } add_to_variable = { v65_private_wealth = -3 } } add_to_variable = { v65_personal_network = 2 }"),
            ("让日海把庆功会拍成胜利宣传", "SVN = { add_to_variable = { v65_private_wealth = 8 } add_to_variable = { v65_network_KHM = 6 } add_to_variable = { v65_network_SVN = 3 } } add_to_variable = { v65_paper_victories = 1 } add_stability = 0.01"),
        ],
        "source": "第115章",
    },
    123: {
        "title": "富国岛的钱投向哪里",
        "desc": "岛上的基地、码头和官邸都在扩建。把资源投向私人安稳，或把钱留给轮训和港口周转，都会改变这座岛的用途。",
        "options": [
            ("用私房钱修官邸", "SVN = { add_to_variable = { v65_private_comfort = 15 } add_to_variable = { v65_private_wealth = -8 } add_to_variable = { v65_network_PHQ = 5 } } add_stability = 0.02"),
            ("扩建仓库与轮训码头", "SVN = { add_to_variable = { v65_network_PHQ = 12 } add_to_variable = { v65_network_KHM = 5 } } add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 700 producer = ROOT } army_experience = 10"),
        ],
        "source": "第65–67、74、97–102、110、133–135章",
    },
}
EVENT_EN = {
    100: ("How to Divide the City Hall Money", "A large sum seized in the city draws the quartermasters, local officers and Daihai's custodians. Park can keep a side ledger or pay the proxies before they find their own income.", ["Let Daihai hold the money and keep a side ledger", "Pay the local officers their share"]),
    101: ("Who Gets the Unclaimed Victories", "Casualties, captured goods and publicity each have their own ledger. Promotion slots for central officers buy influence; allied shares keep local recruiting and supply channels open.", ["Reserve promotion slots for Cai's officers", "Give credit and supply shares to allies"]),
    102: ("Cast Song Kang-mo as a Hero", "Daihai Pictures wants to turn an unverified report into a film series. Audiences may remember the hero, or the names in the casualty roll.", ["Produce the hero series", "Make a unit documentary"]),
    110: ("Who Will Hold the Network Together?", "Airborne, intelligence and logistics officers all want independent authority. The choice decides whether Park relies on central officers or local agents.", ["Reserve posts for central staff", "Put local liaisons in command"]),
    111: ("Who Gets the Intelligence Channel?", "The CIA offers protection and industrial investment for intelligence and credit. The island administrator wants more supplies. Resources are limited.", ["Prioritize the American channel", "Give authority to the island agents"]),
    112: ("Accept the South Vietnamese Officers' Terms", "Local officers will provide manpower and titles, but ask for priority weapons and family protection. Their armed network will make demands of its own.", ["Allocate weapons to local officers", "Keep control of arms and appointments"]),
    113: ("Who Chooses the Militia Leaders?", "Landowners will fund local forces if rank and command follow their wealth and contributions. The center can accept their order or insist on unified appointments.", ["Recognize landowner-appointed leaders", "Place militias under the regional command"]),
    120: ("A Half-Hour Daily Briefing", "Park delegates routine work, spends only thirty minutes to an hour on summaries, smokes by the window and thinks command is almost too comfortable.", ["Keep delegating the routine", "Return briefing time to the duty roster"]),
    121: ("The Parasol at Quy Nhon Pier", "Park fishes beneath a parasol at the Quy Nhon pier, with Vietnamese maids and guards nearby, treating an inflated victory ledger as the warrant for a commander's outing.", ["Keep the guards at the fishing spot", "Inspect port duty during the outing"]),
    122: ("A Civilian-Dress Victory Party", "After the weak response to the Yeonpyeong shelling, Park and Kim Yongbae change into civilian clothes for a victory party. Keep it private, or let Daihai turn it into propaganda.", ["Celebrate and omit the results", "Let Daihai film the victory"]),
    123: ("Where Should Phu Quoc's Money Go?", "The base, quay and residence are all expanding. Spending on private comfort or on rotations and port capacity will shape the island's purpose.", ["Build a comfortable island residence", "Expand warehouses and the training quay"]),
}

NETWORKS = ["SVN", "DNM", "HLC", "MKG", "BHD", "PHQ", "KHM"]
VARIABLES = ["v65_private_wealth", "v65_private_comfort"] + [f"v65_network_{tag}" for tag in NETWORKS]
ROUTE_FLAGS = {key: f"v65chapter_route_{key}" for key in ROUTES}


def normalize_event_effect(effect):
    def split_block(match):
        pairs = re.findall(r"([A-Za-z0-9_]+)\s*=\s*(-?\d+)", match.group(1))
        return " ".join(f"add_to_variable = {{ {key} = {value} }}" for key, value in pairs)
    effect = re.sub(r"add_to_variable = \{([^{}]*)\}", split_block, effect)
    return effect


def launch_event(event_id):
    return (
        f"if = {{ limit = {{ NOT = {{ has_global_flag = v65chapter_event_{event_id}_launched }} }} "
        f"set_global_flag = v65chapter_event_{event_id}_launched country_event = {{ id = v65chapter.{event_id} }} }}"
    )


def route_access(route, mirrored):
    # The three lanes stay independently playable; branch mutual exclusion is local.
    return "always = yes"


def focus_nodes(tag, mirrored=False):
    tree = []
    root_id = f"v65chapter_{tag.lower()}_root"
    root_available = " available = { has_country_flag = v65_union_complete }" if mirrored else ""
    root_bypass = " bypass = { has_global_flag = v65chapter_root_claimed }" if mirrored else ""
    tree.append(f" focus = {{ id = {root_id} icon = GFX_v65_detail_command x = 28 y = 18 cost = 2{root_available}{root_bypass} completion_reward = {{ if = {{ limit = {{ NOT = {{ has_global_flag = v65chapter_root_claimed }} }} set_global_flag = v65chapter_root_claimed add_political_power = 20 }} }} }}")
    # Fill the open area below the initial campaign, beside the dated left lane.
    lane_x = {"reports": 16, "relations": 28, "island": 40}
    for route, data in ROUTES.items():
        nodes = data["focuses"]
        lane = lane_x[route]
        for index, item in enumerate(nodes):
            slug, title, desc, icon, source, event_id = item
            focus_id = f"v65chapter_{tag.lower()}_{route}_{slug}"
            x = lane if index in (0, 3, 6) else lane + (-3 if index in (1, 4) else 3)
            y = 18 + {0: 2, 1: 6, 2: 6, 3: 10, 4: 14, 5: 14, 6: 18}[index]
            reward = [f"if = {{ limit = {{ NOT = {{ has_global_flag = v65chapter_focus_{route}_{slug}_claimed }} }} set_global_flag = v65chapter_focus_{route}_{slug}_claimed"]
            if index == 0:
                reward.append(f"set_global_flag = {ROUTE_FLAGS[route]}")
            if route == "reports":
                reward.append("add_to_variable = { v65_paper_victories = 1 }")
            if route == "relations":
                reward.append("SVN = { add_to_variable = { v65_network_SVN = 2 } }")
            if route == "island":
                reward.append("SVN = { add_to_variable = { v65_private_wealth = 2 } }")
            if index == 3:
                # Choices made at the first fork alter the later merged focus.
                choice_event = {"reports": 100, "relations": 110, "island": 120}[route]
                reward.extend([
                    f"if = {{ limit = {{ has_global_flag = v65chapter_event_{choice_event}_choice_a }} add_to_variable = {{ v65_paper_victories = 1 }} }}" if route == "reports" else
                    f"if = {{ limit = {{ has_global_flag = v65chapter_event_{choice_event}_choice_a }} SVN = {{ add_to_variable = {{ v65_network_SVN = 3 }} }} }}",
                    f"if = {{ limit = {{ has_global_flag = v65chapter_event_{choice_event}_choice_b }} SVN = {{ add_to_variable = {{ v65_network_DNM = 3 }} }} }}",
                ])
            if event_id is not None:
                reward.append(launch_event(event_id))
            reward.append("v65chapter_clamp = yes }")
            if index == 0:
                prerequisite = f"prerequisite = {{ focus = {root_id} }}"
            elif index in (1, 2):
                prerequisite = f"prerequisite = {{ focus = v65chapter_{tag.lower()}_{route}_{nodes[0][0]} }}"
            elif index == 3:
                prerequisite = f"prerequisite = {{ focus = v65chapter_{tag.lower()}_{route}_{nodes[1][0]} focus = v65chapter_{tag.lower()}_{route}_{nodes[2][0]} }}"
            elif index in (4, 5):
                prerequisite = f"prerequisite = {{ focus = v65chapter_{tag.lower()}_{route}_{nodes[3][0]} }}"
            else:
                prerequisite = f"prerequisite = {{ focus = v65chapter_{tag.lower()}_{route}_{nodes[4][0]} focus = v65chapter_{tag.lower()}_{route}_{nodes[5][0]} }}"
            mirrored_gate = " AND = { has_country_flag = v65_union_complete }" if mirrored else ""
            exclusive = ""
            if index in (1, 4):
                sibling = nodes[index + 1][0]
                exclusive = f" mutually_exclusive = {{ focus = v65chapter_{tag.lower()}_{route}_{sibling} }}"
            elif index in (2, 5):
                sibling = nodes[index - 1][0]
                exclusive = f" mutually_exclusive = {{ focus = v65chapter_{tag.lower()}_{route}_{sibling} }}"
            bypass = f" bypass = {{ has_global_flag = v65chapter_focus_{route}_{slug}_claimed }}" if mirrored else ""
            tree.extend([
                " focus = {", f"  id = {focus_id}", f"  icon = GFX_v65_detail_{icon}",
                f"  x = {x} y = {y} cost = 4 {prerequisite}{exclusive}{bypass}",
                f"  available = {{ always = yes{mirrored_gate} }}",
                "  completion_reward = { " + " ".join(reward) + " }", " }",
                f" # Source chapters: {source}",
            ])
    return "\n".join(tree)


effects = [
    "v65chapter_clamp = {",
    " if = { limit = { SVN = { exists = yes } } SVN = {",
]
for variable in VARIABLES:
    effects.append(f"  clamp_variable = {{ var = {variable} min = 0 max = 100 }}")
effects.extend([" } }", "}"])
put(Path("common/scripted_effects/v65_chapter_focus.txt"), "\n".join(effects))


def append_focus_nodes(tag, mirrored=False, tree_file=None):
    path = M / "common/national_focus" / (tree_file or f"v65_{tag}.txt")
    blocks = pdx.read(path)
    focus_tree = next(value for key, _, value in blocks if key == "focus_tree")
    focus_tree[:] = [
        (key, op, value)
        for key, op, value in focus_tree
        if not (
            key == "focus"
            and isinstance(value, list)
            and any(k == "id" and str(v).startswith("v65chapter_") for k, _, v in value)
        )
    ]
    focus_tree.extend(pdx.parse(focus_nodes(tag, mirrored)))
    path.write_text(pdx.dump(blocks), encoding="utf-8")


append_focus_nodes("PKS")
append_focus_nodes("SVN", mirrored=True, tree_file="v65_PARK_GOVERNMENT.txt")

# Triggered chapter events. Every event has two choices; global guards stop the
# mirrored SVN tree from issuing the same narrative reward a second time.
event_text = ["add_namespace = v65chapter"]
loc = {}
for event_id, event in EVENTS.items():
    loc[f"v65chapter.{event_id}.t"] = event["title"]
    loc[f"v65chapter.{event_id}.d"] = event["desc"]
    event_text.extend([
        f"# Source chapters: {event['source']}",
        f"country_event = {{ id = v65chapter.{event_id} title = v65chapter.{event_id}.t desc = v65chapter.{event_id}.d picture = GFX_report_event_generic_read_write is_triggered_only = yes",
        " trigger = { NOT = { has_global_flag = v65chapter_event_" + str(event_id) + "_resolved } }",
    ])
    for option_index, (option_name, option_effect) in enumerate(event["options"], start=1):
        suffix = chr(96 + option_index)
        loc[f"v65chapter.{event_id}.{suffix}"] = option_name
        cost = {(120, 1): 4, (121, 1): 5, (122, 1): 3, (123, 1): 8}.get((event_id, option_index))
        trigger = f"trigger = {{ SVN = {{ check_variable = {{ v65_private_wealth > {cost - 1} }} }} }} " if cost else ""
        event_text.append(
            f" option = {{ {trigger}name = v65chapter.{event_id}.{suffix} {normalize_event_effect(option_effect)} "
            f"set_global_flag = v65chapter_event_{event_id}_choice_{suffix} set_global_flag = v65chapter_event_{event_id}_resolved v65chapter_clamp = yes }}"
        )
    event_text.append("}")
put(Path("events/v65_chapter_focus.txt"), "\n".join(event_text))

for tag in ["simp_chinese", "english"]:
    translations = {}
    for route, data in ROUTES.items():
        suffix = "_sv" if tag == "english" else ""
        translations[f"v65chapter_{route}"] = data["title"] if tag == "simp_chinese" else {
            "reports": "War Reports for Sale",
            "relations": "Personal Ties Across Commands",
            "island": "Private Life and the Island",
        }[route]
        translations[f"v65chapter_{route}_desc"] = {
            "simp_chinese": {
                "reports": "战果、军需和媒体可以互相换取资源，也让虚报与真实伤亡同时留在账本里。",
                "relations": "朴世诚在中央军官、南越代理与岛上势力之间分配职位、合同和指挥权。",
                "island": "私人舒适、日海收益与富国岛基地争用同一笔资金和关系网。",
            },
            "english": {
                "reports": "Victories, procurement and media can be traded for resources, leaving false claims beside real losses.",
                "relations": "Park distributes posts, contracts and command authority among central officers, South Vietnamese proxies and island partners.",
                "island": "Private comfort, Daihai profits and the Phu Quoc base compete for the same money and relationships.",
            },
        }[tag][route]
    translations.update(loc)
    translations["v65chapter_pks_root"] = "归仁的个人网络" if tag == "simp_chinese" else "Park's Network in Quy Nhon"
    translations["v65chapter_svn_root"] = "接管朴系遗产" if tag == "simp_chinese" else "Take Over the Park Network"
    translations["v65chapter_pks_root_desc"] = "从战报、军官关系或富国岛生意中选择一条路线。" if tag == "simp_chinese" else "Choose a route through war reports, officer ties or the Phu Quoc enterprise."
    translations["v65chapter_svn_root_desc"] = "接管后延续既有路线；已领取的剧情奖励不会重复发放。" if tag == "simp_chinese" else "Continue the existing route after unification; claimed story rewards cannot be claimed again."
    if tag == "english":
        for event_id, (title, desc, options) in EVENT_EN.items():
            translations[f"v65chapter.{event_id}.t"] = title
            translations[f"v65chapter.{event_id}.d"] = desc
            for option_index, option in enumerate(options, start=1):
                translations[f"v65chapter.{event_id}.{chr(96 + option_index)}"] = option
    english_focus = {
        "reports": {
            "first_report": ("The First Quy Nhon Report", "Turn the battle at Nguyen village into a result headquarters can see; every number may bring another assignment."),
            "casualty_ledger": ("A Second Casualty Ledger", "One report goes to headquarters and another stays in camp; hidden losses can leave the next rotation short."),
            "share_credit": ("Share Credit with the Signatories", "Cai, staff officers and allied units all want their names in the dispatch. Credit becomes bargaining power."),
            "media_contract": ("Sell the Hero's Story to Daihai", "Films and newspapers can keep a victory alive. The larger the story, the more it demands another victory."),
            "procurement": ("Turn Victories into Contracts", "American procurement connects the front to Korean factories. Profits sustain the force and invite scrutiny."),
            "fact_check": ("Keep a Record of the Real Losses", "Track air strikes, prisoners and casualties separately. Staff need a basis for checking the next report."),
            "legacy": ("Let the Dispatch Speak for the Command", "Different patrons receive different versions of victory, balancing contracts against appointments."),
        },
        "relations": {
            "officer_circle": ("The Classmate Network", "Classmates, patrons and rising officers form a network that expects a share of every victory."),
            "patronage": ("Trade Posts for Support", "Give staff, guards and intelligence officers a place in the command, and private loyalty becomes authority."),
            "cia_channel": ("Open a CIA Vietnam Channel", "Share intelligence, air strikes and credit in exchange for protection and industrial investment."),
            "south_partners": ("Bring South Vietnamese Officers into the Ledger", "Local officers need pay and equipment; the command needs manpower, ports and usable unit designations."),
            "special_command": ("Build a Direct Command Channel", "Special Forces can move faster outside normal channels, but depend on the president and Park's circle."),
            "militia_terms": ("Recruit Landed Militia Leaders", "Local magnates will provide men and money, but demand weapons, authority and family security."),
            "network_compact": ("Put the Network in Writing", "Set regular shares for orders, pay and procurement. Preserving the network means paying it continually."),
        },
        "island": {
            "comfort_budget": ("Make Camp Life a Commander's Residence", "Park delegates routine work and keeps time for private comfort, supported by a steady flow of cash."),
            "music_room": ("Keep a Quiet Room", "Records and a private room make life at the front feel easy; the budget could also fund troop rest."),
            "private_dining": ("A Dinner for Familiar Faces", "A small dinner keeps classmates, quartermasters and business partners close."),
            "household": ("Run the Residence", "Servants, guards and drivers keep the commander's household moving; hiring and pay shape its public image."),
            "phu_quoc_plan": ("Keep Phu Quoc as a Rear Base", "Chinese migration, a training base and a port reinforce one another; island offices also distribute influence."),
            "island_estate": ("Reserve a Quay for Daihai", "Training rotations need ships and warehouses; Daihai wants a reliable share of island trade."),
            "quiet_harbor": ("Build a Harbor that Can Outlast the War", "A base, agents and contracts on the island keep Park's network influential as the front shifts."),
        },
    }
    for route, data in ROUTES.items():
        for slug, title, desc, icon, source, event_id in data["focuses"]:
            for focus_tag in ["pks", "svn"]:
                key = f"v65chapter_{focus_tag}_{route}_{slug}"
                if tag == "simp_chinese":
                    translations[key] = title
                    translations[key + "_desc"] = desc
                else:
                    translations[key], translations[key + "_desc"] = english_focus[route][slug]
    put(Path(f"localisation/{tag}/zzzz_v65_chapter_focus_l_{tag}.yml"), loc_text(translations, tag))

SUBJECTS={'first_report':'ledger','casualty_ledger':'inspect','share_credit':'payroll',
 'media_contract':'press','procurement':'contracts','fact_check':'inspect','legacy':'mandate',
 'officer_circle':'academy','patronage':'adviser','cia_channel':'intelligence','south_partners':'proxy',
 'special_command':'staff','militia_terms':'garrison','network_compact':'treaty',
 'comfort_budget':'housing','music_room':'leisure','private_dining':'funds','household':'housing',
 'phu_quoc_plan':'port','island_estate':'contracts','quiet_harbor':'warehouse'}
art={f'v65chapter_{tag}_{route}_{row[0]}':SUBJECTS[row[0]]
     for tag in ['pks','svn'] for route,data in ROUTES.items() for row in data['focuses']}
art.update({f'v65chapter_{tag}_root':'command' for tag in ['pks','svn']})
(R/'chapter-focus-manifest.json').write_text(json.dumps(dict(art=art,unique_plot_focuses=22,
    mirrored_plot_focuses=22,choice_events=len(EVENTS),sources={str(k):v['source'] for k,v in EVENTS.items()}),ensure_ascii=False,indent=2),encoding='utf-8')
print(f"Chapter focus module: 44 focuses, {len(EVENTS)} two-choice events, 3 shared routes")
