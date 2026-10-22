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
            ('first_report', '归仁的第一份捷报', '“崔顺勇这下子立马就明白了，脸上的笑容也是止不住了，赶紧发问道，“大队长，那咱们报敌人有300多的伤亡？” 实际的伤亡肯定没有这么多，把所有的越共游击队和民兵算上连200人都没有，更何况还有不少人逃掉了，就算是把村里逃的比较慢的村民加上，也不会超过300人。”', 'ledger', '第8章', None),
            ('casualty_ledger', '另立伤亡账', '“”崔顺勇干嘛拿起自己手中的文件说道，“今早在西冶村西部的战斗中，歼灭的越共游击队员达到了53人，俘虏了11人，在战斗中我军伤亡110人，其中阵亡35人，受伤75人。” 这算个毛啊。 朴世诚一听到这满脸不在乎的摆手说道，“我还以为多大点事呢，不就伤亡比有些难看嘛，没事。””', 'ledger', '第26章', 100),
            ('share_credit', '把功劳分给签字的人', '“乔治继续说道，“这人到底是什么身份呢，对于我们来说其实并不重要，不过我个人认为，一个越共方面的高级将军，就这么轻松的被你们和南越方面抓获.........” 听到这朴世诚立马就明白了，他们大概率是知道了，自己指鹿为马的操作，但看起来好像并不打算拆穿自己，而是也要想要分润一些功劳呀。”', 'contracts', '第61章', 101),
            ('media_contract', '把英雄故事卖给日海', '“随着特战司的反制行动成功之后，朴世诚为了继续提升特战司的知名度，并进一步坐实反制行动的成功。 便直接以当初的那个剧本为题材，以宋康茂少领作为主角，准备来拍一些电影出来。 按照朴世诚的草案，电影要形成系列，也就是说有好几部，现在拍摄的第一部，剧情很简单，甚至是有点傻瓜。”', 'contracts', '第108章', 102),
            ('procurement', '把战果换成采购合同', '“这艘货车名为日出号，很显然它是日海公司的财产，就连其运输的弹药，也是日海公司在韩国国内军工厂生产的，同样还是走的特需的路子。 还是因为韩军主动参与到了越南战争，美国便开始大力扶持韩国的工业，朴世诚自然也抓准机会，通过驻越美军的路子，低价从日本和美国分别搞了一套二手的子弹生产线，在国内建立了日海公司自”', 'contracts', '第52章', None),
            ('fact_check', '保留一份真实记录', '朴世诚继续说道，“看到现在越共游击队如此猖狂，我认为，我们两方应该联合起来，对辖区里的各个村庄进行多次大规模的扫荡行动，判别那些村庄是安全村，那些村庄有通共的嫌疑。', 'command', '第26章', None),
            ('legacy', '让战报替本部说话', '我军获胜的消息，发送给带统领卡咔。”', 'ledger', '第68章', None),
        ],
    },
    "relations": {
        "title": "跨军区私人关系",
        "focuses": [
            ('officer_circle', '陆士同期的联络圈', '“朴灿烈其实也嫉妒过朴世诚的，可人家在越南取得的战功，以及回来后发起的顶上作战和反制行动，也让他心服口服。 更重要的一点是，只要跟着朴世诚混的人，都有很不错的前途，就比如徐泉这个朴世诚毫不起眼的小跟班。”', 'command', '第113章', None),
            ('patronage', '用职位换取支持', '“自从那场激烈的会议室‘战争’之后，第一旅团内部可谓是进行了一场风云突变般的换血，首先是朴世诚，直接以大领的军衔，代理了旅团长的职务，然后崔顺勇也跟着升任了旅团副参谋长，朴世诚的陆士同期同学，徐泉则调任了驻越韩国军司令部反谍科科长的位子，就是卢泰愚之前的岗位，他的军衔也相应地从尉官变成了校官，现在已经”', 'command', '第40章', 110),
            ('cia_channel', '接通CIA越南站', '乔治继续说道，“这人到底是什么身份呢，对于我们来说其实并不重要，不过我个人认为，一个越共方面的高级将军，就这么轻松的被你们和南越方面抓获.........”', 'contracts', '第61章', 111),
            ('south_partners', '让南越军官入账', '“这个城市管理大队成立后，在整个归仁市那可是横着走的存在，除了韩军和美军他们不敢去惹，以及南越政府官员和国军不去主动招惹以外，其他人都只有被他们欺负的份，平民们看到他们了，简直就跟遇到了瘟神一样，跑都来不及跑。”', 'proxy', '第65章', 112),
            ('special_command', '建立直属指挥渠道', '“过了半晌，朴正熙随手把文件丢在了身前的茶几上，很是淡然的对着金钟泌发问道，“就三个旅团的规模会不会太少了点？还有为什么特战司仍旧要隶属于陆军？” 金钟泌赶忙点了点头回答道，“卡咔，一开始组建特战司，就把部队扩充太多的话，很有可能会使得美方反对，规模小一点话，不至于过分刺激美方，后期等特战司组建完毕后”', 'command', '第63章', None),
            ('militia_terms', '以土地和头衔招揽团练', '“朴世诚在就任驻越韩国军机动部队司令官后，并没有在立即就出动部队，去开展扫荡行动，而是一方面集结部队之余，给整个平定省那帮土豪、大地主们发了一个意见征求，并且还说明，只要谁能把这份意见征求稿写的好，写得深合朴世诚司令官的心意的话，那就会被南越政府授予官位。”', 'proxy', '第137章', 113),
            ('network_compact', '把关系写成长期承诺', '““今天把大家召集在这里，主要是说两件事，一个就是刚刚阮上校问的，大家都不用担心我走了之后的收益，只要驻越韩国军还在越南一天，那每月都会有一笔钱，从日海公司划到诸位的账户之中。” 朴世诚这算是给在场的所有人都吃了一颗定心丸。”', 'contracts', '第68章', None),
        ],
    },
    "island": {
        "title": "私人生活与海岛",
        "focuses": [
            ('comfort_budget', '把军营过成官邸', '“如果没有紧急的事情，朴世诚最多每天就花个半小时到一小时的时间，对部队情况有个大致的了解，这就行了。 在加上特战司的组织模式，跟公司很像，大家都是各司其职，做好自己的那一块，做出成绩就够了，其他因素根本就用不着考虑，因此特战司办事的效率还特别的高。”', 'contracts', '第108章', 120),
            ('music_room', '留一间安静的休息室', '“带韩冥国驻越韩国军，首都机械化师团，第一机械化步兵旅团（白虎团）旅团长，猛虎地区特攻（韩国叫特种部队，一般称之为特攻部队，不过国内有时仍会翻译成特种部队）大队大队长（注1），朴世诚准将，正悠闲的躺在一把太阳伞下的椅子上，哼着只有自己熟知的小曲。”', 'ledger', '第41章', 121),
            ('private_dining', '只请熟人赴宴', '“今晚是延坪冲突后，金容培私人的‘庆功会’，虽然韩国的炮火反制只是帮朝鲜的农民松了松土地，但这并不妨碍，韩国方面大肆宣传己方的胜利。 嗯，这就是所谓的如胜。 金容培这次把朴世诚叫来的最主要原因，则是因为朴正熙认为己方的炮火反制取得的效果不佳，有一种再次派遣特攻队发起反制行动的想法，所以便把朴世诚叫来提”', 'contracts', '第115章', 122),
            ('household', '安排官邸日常', '“朴世诚翘着二郎腿，正悠闲的看着手中的报纸，在他身后朴世诚的第二任越南女仆，正用双手温柔的给他捏着肩膀。 朴世诚早晨的时候还在西冶村，这还没到中午就出现在了永盛乡，这可是朴世诚有怎么瞬移之类的超能力，而是朴世诚在今早，布置完战术后，就直接就乘坐着直升机回来了。”', 'command', '第26章', None),
            ('phu_quoc_plan', '把富国岛留作后方', '“李威炎听到富国岛的时候，眉头一下子就皱了起来，想了半晌才想起来，富国岛不就是越南最南边靠近柬埔寨的那个岛么，而且军政长官这个职位，在南越共和国里可没有啊，朴世诚这是让自己出大血，去主动创造一个职位。”', 'port', '第65章', 123),
            ('island_estate', '给日海留一块码头', '“”李明翰微微点了点头，然后赶紧说道，“司令官，目前富国岛上一共有三方部队，分别是美空军的一个联合作战联队，南越国军的富国岛守备司令部，以及我军的空输三旅团。” “目前富国岛的防御较为完备，面向柬埔寨大陆一侧的岸防工事已经构筑完毕，岛屿西南一侧有两个机场也已经投入使用，码头也早已建设完毕，目前南越国军”', 'port', '第134章', None),
            ('quiet_harbor', '建一处能继续经营的港口', '““如果搞不定的人或者事，那就找徐泉，他会找我的，我来负责解决。”朴世诚抖了抖手中的烟灰，淡淡的说道。 “还有.......” --------------------------- 1968年2月26日，上午十时许。”', 'proxy', '第68章', None),
        ],
    },
}

EVENTS = {
    100: {
        "title": "市府缴获的钱怎么分",
        "desc": '“正当卢泰愚在纠结要不要把自己那份给吐出来的时候，突然又朴世诚继续说道，“都送到日海公司去，这笔钱肯定是归仁市政府的公共资金，我先暂时帮南越政府保管一下，毕竟这兵荒马乱的，万一遗失了，那可就不好了。” “耶、耶。”卢泰愚这才如梦初醒的赶忙回应道。”',
        "options": [
            ("交日海代管，底账留在司令部", "SVN = { add_to_variable = { v65_private_wealth = 12 v65_network_SVN = 5 v65_network_KHM = 8 } } add_to_variable = { v65_paper_victories = 1 } add_political_power = 15"),
            ("给地方军官分成，免得他们自筹", "SVN = { add_to_variable = { v65_network_DNM = 5 v65_network_HLC = 8 v65_network_MKG = 8 v65_network_BHD = 5 } } add_manpower = 1000 add_to_variable = { v65_personal_network = 2 }"),
        ],
        "source": '第51章',
    },
    101: {
        "title": "谁拿走空缺的战功",
        "desc": '“乔治继续说道，“这人到底是什么身份呢，对于我们来说其实并不重要，不过我个人认为，一个越共方面的高级将军，就这么轻松的被你们和南越方面抓获.........” 听到这朴世诚立马就明白了，他们大概率是知道了，自己指鹿为马的操作，但看起来好像并不打算拆穿自己，而是也要想要分润一些功劳呀。”',
        "options": [
            ("给蔡系军官留足晋升名额", "SVN = { add_to_variable = { v65_network_SVN = 10 v65_private_wealth = 5 } } add_to_variable = { v65_paper_victories = 2 } add_political_power = 20"),
            ("把署名与军需份额给盟军", "SVN = { add_to_variable = { v65_network_DNM = 8 v65_network_HLC = 5 v65_network_MKG = 5 v65_private_wealth = 3 } } add_to_variable = { v65_personal_network = 2 } add_manpower = 1000"),
        ],
        "source": '第61章',
    },
    102: {
        "title": "把宋康茂拍成英雄",
        "desc": '“随着特战司的反制行动成功之后，朴世诚为了继续提升特战司的知名度，并进一步坐实反制行动的成功。 便直接以当初的那个剧本为题材，以宋康茂少领作为主角，准备来拍一些电影出来。 按照朴世诚的草案，电影要形成系列，也就是说有好几部，现在拍摄的第一部，剧情很简单，甚至是有点傻瓜。”',
        "options": [
            ("拍摄英雄系列片", "SVN = { add_to_variable = { v65_private_wealth = 10 } add_to_variable = { v65_private_comfort = 5 } add_to_variable = { v65_network_SVN = 5 } } add_stability = 0.03"),
            ("改拍部队纪实片", "SVN = { add_to_variable = { v65_network_SVN = 5 } add_to_variable = { v65_network_DNM = 5 } } army_experience = 10"),
        ],
        "source": '第108章',
    },
    110: {
        "title": "任命谁来守住关系网",
        "desc": '“自从那场激烈的会议室‘战争’之后，第一旅团内部可谓是进行了一场风云突变般的换血，首先是朴世诚，直接以大领的军衔，代理了旅团长的职务，然后崔顺勇也跟着升任了旅团副参谋长，朴世诚的陆士同期同学，徐泉则调任了驻越韩国军司令部反谍科科长的位子，就是卢泰愚之前的岗位，他的军衔也相应地从尉官变成了校官，现在已经”',
        "options": [
            ("把名额留给中央参谋", "SVN = { add_to_variable = { v65_network_SVN = 10 } add_to_variable = { v65_network_DNM = 5 } } add_command_power = 15"),
            ("让地方联络官带队", "SVN = { add_to_variable = { v65_network_HLC = 8 } add_to_variable = { v65_network_MKG = 8 } add_to_variable = { v65_network_BHD = 5 } } add_manpower = 1200"),
        ],
        "source": '第40章',
    },
    111: {
        "title": "与谁共享机密渠道",
        "desc": '“乔治继续说道，“这人到底是什么身份呢，对于我们来说其实并不重要，不过我个人认为，一个越共方面的高级将军，就这么轻松的被你们和南越方面抓获.........” 听到这朴世诚立马就明白了，他们大概率是知道了，自己指鹿为马的操作，但看起来好像并不打算拆穿自己，而是也要想要分润一些功劳呀。”',
        "options": [
            ("优先经营美方渠道", "SVN = { add_to_variable = { v65_network_SVN = 8 } add_to_variable = { v65_private_wealth = 12 } } add_political_power = 25"),
            ("把权限交给岛上代理", "SVN = { add_to_variable = { v65_network_PHQ = 12 } add_to_variable = { v65_network_KHM = 5 } } add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 500 producer = ROOT }"),
        ],
        "source": '第61章',
    },
    112: {
        "title": "接受南越军官的条件",
        "desc": '“已经成为南越国军归仁市守备司令官的阮文武少将，这时突然带着有些阴沉的语气，说道，“司令官、先生们，我也有个建议，为了以防出现，有人投降的情况发生，还应该让那些人把家眷，都送到富国岛去，只要他们这些留在南越地区的抵抗的人，有谁胆敢向越共投降，那就杀他们全家。””',
        "options": [
            ("给地方军官武器份额", "SVN = { add_to_variable = { v65_network_BHD = 8 } add_to_variable = { v65_network_MKG = 8 } add_to_variable = { v65_private_wealth = 5 } } add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 600 producer = ROOT }"),
            ("保留军火与任命权", "SVN = { add_to_variable = { v65_network_SVN = 10 } add_to_variable = { v65_network_PHQ = 4 } } add_political_power = 30"),
        ],
        "source": '第137章',
    },
    113: {
        "title": "团练要不要自己选头领",
        "desc": '“朴世诚在就任驻越韩国军机动部队司令官后，并没有在立即就出动部队，去开展扫荡行动，而是一方面集结部队之余，给整个平定省那帮土豪、大地主们发了一个意见征求，并且还说明，只要谁能把这份意见征求稿写的好，写得深合朴世诚司令官的心意的话，那就会被南越政府授予官位。”',
        "options": [
            ("承认地主推举的团练头领", "SVN = { add_to_variable = { v65_network_HLC = 8 } add_to_variable = { v65_network_MKG = 8 } add_to_variable = { v65_network_BHD = 8 } add_to_variable = { v65_private_wealth = 8 } } add_manpower = 2000"),
            ("团练归南越军区统一编组", "SVN = { add_to_variable = { v65_network_SVN = 10 } add_to_variable = { v65_network_DNM = 5 } } army_experience = 15"),
        ],
        "source": '第137章',
    },
    120: {
        "title": "三十分钟的每日简报",
        "desc": '“如果没有紧急的事情，朴世诚最多每天就花个半小时到一小时的时间，对部队情况有个大致的了解，这就行了。 在加上特战司的组织模式，跟公司很像，大家都是各司其职，做好自己的那一块，做出成绩就够了，其他因素根本就用不着考虑，因此特战司办事的效率还特别的高。”',
        "options": [
            ("继续把杂务交给副官", "SVN = { add_to_variable = { v65_private_comfort = 12 } add_to_variable = { v65_private_wealth = -4 } } add_political_power = 10"),
            ("把简报时间还给前线轮值", "SVN = { add_to_variable = { v65_network_SVN = 5 } } army_experience = 8"),
        ],
        "source": '第108章',
    },
    121: {
        "title": "归仁码头的遮阳伞",
        "desc": '“带韩冥国驻越韩国军，首都机械化师团，第一机械化步兵旅团（白虎团）旅团长，猛虎地区特攻（韩国叫特种部队，一般称之为特攻部队，不过国内有时仍会翻译成特种部队）大队大队长（注1），朴世诚准将，正悠闲的躺在一把太阳伞下的椅子上，哼着只有自己熟知的小曲。”',
        "options": [
            ("让警卫继续守着钓点", "SVN = { add_to_variable = { v65_private_comfort = 12 } add_to_variable = { v65_private_wealth = -5 } } add_political_power = 8"),
            ("借出行检查港口值勤", "SVN = { add_to_variable = { v65_network_PHQ = 6 v65_network_DNM = 3 } } army_experience = 8"),
        ],
        "source": '第41章',
    },
    122: {
        "title": "穿便服的庆功会",
        "desc": '“今晚是延坪冲突后，金容培私人的‘庆功会’，虽然韩国的炮火反制只是帮朝鲜的农民松了松土地，但这并不妨碍，韩国方面大肆宣传己方的胜利。 嗯，这就是所谓的如胜。 金容培这次把朴世诚叫来的最主要原因，则是因为朴正熙认为己方的炮火反制取得的效果不佳，有一种再次派遣特攻队发起反制行动的想法，所以便把朴世诚叫来提”',
        "options": [
            ("照旧庆祝，战报别提效果", "SVN = { add_to_variable = { v65_private_comfort = 10 } add_to_variable = { v65_private_wealth = -3 } } add_to_variable = { v65_personal_network = 2 }"),
            ("让日海把庆功会拍成胜利宣传", "SVN = { add_to_variable = { v65_private_wealth = 8 } add_to_variable = { v65_network_KHM = 6 } add_to_variable = { v65_network_SVN = 3 } } add_to_variable = { v65_paper_victories = 1 } add_stability = 0.01"),
        ],
        "source": '第115章',
    },
    123: {
        "title": "富国岛的钱投向哪里",
        "desc": '“”李明翰微微点了点头，然后赶紧说道，“司令官，目前富国岛上一共有三方部队，分别是美空军的一个联合作战联队，南越国军的富国岛守备司令部，以及我军的空输三旅团。” “目前富国岛的防御较为完备，面向柬埔寨大陆一侧的岸防工事已经构筑完毕，岛屿西南一侧有两个机场也已经投入使用，码头也早已建设完毕，目前南越国军”',
        "options": [
            ("用私房钱修官邸", "SVN = { add_to_variable = { v65_private_comfort = 15 } add_to_variable = { v65_private_wealth = -8 } add_to_variable = { v65_network_PHQ = 5 } } add_stability = 0.02"),
            ("扩建仓库与轮训码头", "SVN = { add_to_variable = { v65_network_PHQ = 12 } add_to_variable = { v65_network_KHM = 5 } } add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 700 producer = ROOT } army_experience = 10"),
        ],
        "source": '第134章',
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
    loc[f"v65chapter.{event_id}.d"] = event["desc"].strip('\u201c\u201d ')
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
    translations["v65chapter_pks_root"] = "朴的私人网络" if tag == "simp_chinese" else "Park's Personal Network"
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
                    translations[key + "_desc"] = desc.strip('\u201c\u201d ')
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
