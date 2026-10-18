"""Author the 0.4 campaign. All prose and game logic here are original."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];M=R/'mod'
def put(path,text):
 p=M/path;p.parent.mkdir(parents=True,exist_ok=True);text='\n'.join(line.rstrip() for line in text.splitlines()).rstrip();p.write_text(text+'\n',encoding='utf-8-sig' if str(path).endswith('.yml') else 'utf-8')

# Each branch occupies its own six-column lane. Descriptions are narrative,
# while the game's completion tooltip lists the actual scripted rewards.
DATA={
'SVN':[
('command','西贡的战争','前线的战报与乡村的传闻指向两个不同的战场。总统府必须先弄清自己还能指挥哪些部队。','radio',[
('roster','清点军区名册','编制表上的番号并不等于听令的兵力。把军饷和实际驻地对照，才能重建中央的命令链。','command'),
('reports','让真实战报抵达西贡','层层修饰的捷报正在掩盖伤亡。允许前线越级报告，会触怒军官，却能减少下一次误判。','intel'),
('liaison','驻军联络官','省长、军区与警察使用不同的消息网络。派出联络官，将他们的承诺变成可以核查的调动。','command'),
('reserve','中央机动预备队','每次危机都向别的军区借兵，中央就欠下一笔政治债。西贡需要一支能立即出动的预备队。','training'),
('unity','重新签署军区协议','岘港和归仁的司令官不会交出全部权力。以军费换取共同作战，可以先保住脆弱的联盟。','civil')]),
('front','守住十七度线','北部阵地承受着最直接的压力。这里的任务是守住屏障，避免把整场战争押在一次北进上。','shield',[
('dmz','广治防御工事','工兵把道路、村庄与火力点编入同一张图。防线的价值在于赢得时间，而非制造漂亮的进攻箭头。','fort'),
('hue','顺化补给仓','广治阵地一旦缺粮，顺化就会成为下一道战线。先让后方仓库储满弹药，再谈反击。','supply'),
('rotation','轮换疲惫的营','连续驻防正在耗尽基层骨干。把部队轮出阵地整训，才能让下一批增援不再只是填补伤亡。','training'),
('corridor','一号公路护送队','沿海交通线将北部驻军与港口连在一起。运输护送应成为常设任务，而不是临时拼凑。','road'),
('hold_line','有限战争指令','总参谋部正式放弃冒进的时间表。将防御纵深与机动预备队结合，使战线能够承受一次挫折。','defence')]),
('villages','乡村不是空白地带','离开公路，政府的印章往往失去效力。争取村庄的合作，比在地图上涂满颜色更难。','tree',[
('register','重新核查乡村户籍','虚假的名册既方便侵吞援助，也方便地下组织隐蔽。核查工作需要地方协助，不能只靠军警。','intel'),
('patrols','分区巡逻制度','守住县城而放弃夜间道路，等于把主动权让给游击队。让小部队熟悉自己的责任区。','training'),
('amnesty','有条件的归顺','并非每个帮助游击队的家庭都愿意继续战争。给愿意交出武器的人一条可以兑现的出路。','civil'),
('countertrail','切断秘密联络站','与其盲目扫荡整片森林，不如追踪运输和接头网络。情报的价值应体现在减少下一次突袭。','countertrail'),
('rural_pact','乡村重建契约','保护、税收和征兵必须有清楚的边界。只有兑现承诺，地方合作才不会在部队离开后立即瓦解。','pacify')]),
('economy','援助如何变成战力','港口里的物资不会自行抵达部队。围绕仓库、工坊和公路展开建设，才能缩短这段距离。','factory',[
('roads','修复交通干线','被破坏的桥梁让每次增援都变成冒险。先恢复中央掌握地区的运输能力。','road'),
('workshops','扩充军械工坊','损坏的步枪和车辆堆满营地。建立修械能力，比等待下一批进口装备更可靠。','arms'),
('supplies','统一军需账目','同一批物资可能在三本账里重复出现。把仓储和部队收据对上，减少补给线上的失踪。','supply'),
('industry','战时民用生产','军队的需求正在挤压城市生活。扩大基础生产，让战争之外的日常生活还能维持。','industry'),
('port','西贡港周转计划','船期、铁路和卡车应当按同一套时刻表运行。缩短物资在码头停留的时间。','transport')]),
('politics','军政权力的裂缝','胜利时可以搁置的矛盾，会在败报到来后同时爆发。西贡的统治不能只依靠军官之间的口头保证。','landmark',[
('civil','给地方行政留出空间','行政官员不该只在征粮时才出现。让地方政府恢复办事能力，为危机留下协商渠道。','civil'),
('crisis','败报后的追责会议','北部阵地失守，或南方腹地遭到严重突破，都会让责任之争进入总统府。军方开始讨论谁应该下台。','crisis'),
('radio','控制西贡广播台','在军营知道命令真假之前，广播先定义了局势。谁掌握电台，谁就能让观望者听见自己的版本。','radio'),
('bargain','首都驻军的承诺','西宁、边和、头顿与美萩的指挥官各有价码。军费与职位必须换来明确的行动承诺。','lobby'),
('martial_focus','全国戒严令','政府选择以军令维持秩序，非军事区仍被列为例外。没有忠诚的执行者，命令也可能成为另一派的武器。','martial')])],
'PKS':[
('command','归仁的年轻指挥官','朴世诚抵达越南时，掌握的只是一个大队。战争却提供了把番号、声望与私人关系连接起来的机会。','helmet',[
('battalion','整顿第一三三大队','先让基层军官了解指挥官的作战方式。可靠的骨干，比纸面上的机械化番号更重要。','training'),
('quynhon','归仁预备队营地','营地既要接收补给，也要联络附近村庄。归仁将成为这支部队真正的权力起点。','road'),
('tiger','猛虎师协同演练','与师部保持协同，可以借到炮兵和运输力量。每次配合也都是争取上级信任的机会。','command'),
('fieldstaff','建立直属参谋班子','战场情报不能完全依赖友军转交。培养一批只对本部负责的参谋和通信人员。','intel'),
('elite','机械化突击骨干','把经验最丰富的营编成机动核心。在关键时刻集中使用，才能放大有限装备的作用。','training')]),
('reputation','战报与晋升','战场上的小胜需要被远方的上级看见。宣传能换来资源，也会制造必须兑现的期待。','radio',[
('war_reports','第一份归仁战报','把作战结果整理成可以送往师部的报告。文字背后的伤亡，不应从参谋的账簿里消失。','influence'),
('press','记者抵达营地','镜头选择了整齐的队列和收缴的武器。指挥官开始学习如何安排公众看到的战争。','influence'),
('patron','争取蔡命新支持','远征军上级需要可以向国内交代的成绩。表现出可靠，比过早展示野心更有利。','command'),
('palace','通往青瓦台的信件','归仁的名字终于出现在更高层的案头。政治庇护能够保护部队，也会要求回报。','patron'),
('promotion','以战功换指挥权','新的任命带来更多部队和更重的责任。声望必须转化为能执行命令的组织。','influence')]),
('villages','良民证的代价','证件、地方警察和驻军共同决定村庄的日常生活。短期收入与长期敌意之间没有免费的选择。','scroll',[
('fees','清点办证收入','收入进入正规账目，才能避免被每一层经手者截留。军营的收益也由此与村庄捆在一起。','funds'),
('police','地方警察联络网','军队离开以后，村庄仍由地方势力掌握。建立联络可以减少误报，也会让部队卷入旧日恩怨。','intel'),
('village_bargain','以保护换取合作','把合作条件摆到台面上，减少随意索取。少一点眼前收益，可以换来更可靠的情报。','pacify'),
('inspection','清查办证灰色收入','对收入的追查触动了军官和地方官员。若不限制这条利益链，任何治安成果都可能被抵消。','civil'),
('trusted_villages','可信的后方村庄','合作不再只依靠一张纸。稳定的采购和保护关系，使营地附近逐渐形成真正的后方。','defence')]),
('business','日海的军需合同','运输和修械合同给部队带来另一种力量。企业网络可以维持独立性，也可能让战争变成生意。','factory',[
('trucks','承包运输车队','让货物沿既定路线运转，并留下可核查的单据。运输能力成为本部与友军讨价还价的筹码。','transport'),
('repair','营地修械工场','战损车辆不必全部送往远方。训练技工，建立自己的备件和维修体系。','arms'),
('company','日海集团的第一间工厂','合同利润回流到生产设施。公司开始拥有军营之外的雇员、账目和利益。','industry'),
('contracts','扩大军需采购权','以稳定交付换取更多采购合同。资源集中到手中时，监管和政治依赖也随之加深。','funds'),
('independent','维持独立补给','无论西贡还是远征军司令部发生变化，本部都需要继续领饷。建立一份能撑过危机的储备。','supply')]),
('power','把声望变成权力','私人追随者正在形成自己的升迁网络。朴世诚必须决定，这支部队最终为哪一种秩序服务。','landmark',[
('guards','直属警卫与通信网','警卫保护的不只是营地。把通信、档案和军官任命掌握在可信的人手中。','guards'),
('intelligence','特战司的雏形','精选人员承担侦察和联络任务。一个独立的情报中枢开始超出普通大队的职权范围。','intel'),
('capital_links','在西贡寻找盟友','年轻军官、商人和驻军都在观察首都局势。建立联系，才可能在危机时得到回应。','influence'),
('remain','在越南扎根','将经营重点留在归仁与沿海。选择长期建设，就意味着暂时放弃干预西贡最高权力的机会。','stay'),
('yushin','以秩序之名进军西贡','只有前线败局已经动摇政府，公开夺权才有借口。朴世诚选择让自己的部队回答首都的危机。','usurp')])],
'NVN':[
('command','河内的持久战争','正面战线只是战争的一部分。河内需要同时维持北方、运输线与南方组织的运转。','landmark',[
('staff','统一前线指挥','把分散的计划汇入总参谋部，避免各部队争用同一批运输和补给。','command'),('reserve','北方战略预备队','准备能够轮换和增援的骨干部队，而不是将全部兵力压到边界。','training'),('supply','洞海的隐蔽仓库','分散储存弹药与粮食，降低一次破坏造成的损失。','supply'),('fort','十七度线阵地群','掩体和交通壕能够节约守军兵力，让更多人力支援南方。','fort'),('hold','避免消耗性的北线冒进','边界上的胜负不应吞噬整场战争的资源。将防线作为长期斗争的支点。','defence')]),
('trail','穿越森林的道路','山地运输线连接着两个相隔遥远的战场。每一座仓库都需要当地向导和持续维护。','truck',[
('trail_depots','分散式转运仓','小型仓库降低暴露风险，并允许运输队分段行动。','trail'),('guides','山地向导网络','只有熟悉山路和水源的人，才能把地图上的细线变成真正的通道。','trail'),('repair','雨季道路养护','季风会摧毁一条刚刚打通的便道。持续维修比一次性动员更重要。','road'),('signals','跨区通信联络','以固定联络周期减少误会，让南方据点知道下一批物资何时到达。','intel'),('rear_offensive','将增援送往南方','通道的目的不是在北部堆积更多部队，而是维持敌后据点的作战能力。','infiltration')]),
('south','与南方解放阵线协同','南方的组织有自己的经验和利益。援助必须通过可以持续合作的联络体系交付。','tree',[
('liaison','派遣南方联络员','建立固定接头规则，避免各单位在秘密运输线上互相误认。','infiltration'),('cadres','补充基层骨干','向南方提供经过训练的组织者，使当地据点能够承受损失。','fnl_training'),('arms','缴获武器再分配','把可使用的武器优先交给缺乏装备的南方部队。','fnl_arms'),('coordination','南北联合行动窗口','选择配合时机，令正面牵制与敌后行动相互支援。','infiltration'),('political_front','保留统一战线的空间','南方联盟不仅由军人组成。保护民事联系，才能使据点获得补给和情报。','civil')]),
('economy','支撑长期动员','北方的工厂、农田和运输系统必须承担超出日常生活的需求。','factory',[
('workshops','地方修械作坊','让更多县份具备修理基本武器的能力，减少对集中工厂的依赖。','arms'),('rails','修复运输节点','工人和铁路兵优先处理瓶颈，让北方仓库与前线保持联系。','transport'),('industry','扩大后方生产','将有限资源用于能持续交付的基础工业，而不是宏大的纸面计划。','industry'),('civil','保障生产人员生活','稳定的口粮与医疗有助于减少工人流失。','civil'),('reserves','为下一轮战争储备','将新生产的装备留出一部分储存，避免每次作战都耗尽库存。','supply')])],
'FNL':[
('command','南方的地下战争','白天属于驻军的道路，夜晚可能通往另一个政府。解放阵线从地方据点开始组织自己的战争。','tree',[
('cells','重建乡村支部','将联络人员分成彼此有限知情的小组，减少一人被捕造成的损失。','intel'),('cadres','地方干部训练班','基层干部既要分配粮食，也要维持队伍纪律。训练应从日常组织能力开始。','training'),('villages','村庄的隐蔽粮仓','把补给分散在多个地点，避免部队因一个仓库暴露而挨饿。','supply'),('political','统一战线代表会议','地方组织需要一个能够表达诉求的渠道，而不只是接收军事命令。','civil'),('network','地下行政联络网','在相隔的据点之间建立稳定的民事联系，维持长时间的隐蔽活动。','command')]),
('guerrilla','公路之外的机动','游击战不要求守住每一块土地。让对手不断分兵，才是小部队存在的意义。','helmet',[
('caches','隐藏武器窖','武器和人员分开转移，减少白天行动暴露的风险。','arms'),('night','夜间集结','通过熟悉地形的向导，将分散的小队在短时间内组织起来。','training'),('ambush','伏击运输车队','打击补给比占领一处无力防守的城镇更有价值。','infiltration'),('disperse','打散再集结','结束作战后重新融入据点，避免与优势部队进行持久阵地对抗。','guerrilla'),('rear','在南方腹地建立新据点','当敌军集中到北部时，南方组织可以用一次局部行动迫使他们回头。','infiltration')]),
('trail','接上胡志明小道','敌后组织不能永远依靠缴获。与北方保持联系，才有持续作战的物资基础。','truck',[
('runners','接头员的路线图','把联络点与备用路线分开记录，减少消息在途中失踪。','trail'),('border','边境秘密转运点','运输在边境分段交接，避免一支队伍掌握全部路线。','trail'),('medics','丛林救护站','让伤员有机会返回部队，比不断招募新人更能保住经验。','defence'),('liaison','与北方协调增援','明确所需装备和接收地点，使援助能够抵达真正缺乏物资的地区。','supply'),('depots','南方仓库网络','分散的粮食、药品和弹药储备，让各据点能够等待下一次机会。','infiltration')]),
('future','为南方争取政治地位','军事合作并不自动解决未来政府的组成。解放阵线也需要维护自己的政治发言权。','landmark',[
('assembly','地方代表会议','让各据点带来自己的诉求和损失清单，避免远方命令脱离当地情况。','civil'),('land','乡村土地争议委员会','对土地的承诺必须转化为能够执行的办法，否则会制造新的地方冲突。','civil'),('recruit','扩大地方武装','以熟悉当地的人员补充队伍，同时保留农业生产需要的劳动力。','manpower'),('negotiation','保留谈判渠道','战争之外的联系能够保护组织，也为未来的政治变化留下空间。','command'),('administration','南方联合行政','将军事据点的合作变成能够长期运作的民事机构。','industry')])],
'DNM':[
('command','岘港军区的账本','军区需要西贡的拨款，西贡需要军区的兵。沿海司令部在这场交换中保留着自己的筹码。','helmet',[
('officers','重新确认军官效忠','分清职务关系与私人追随，才能判断哪一支营能在危机时调动。','command'),('reserve','军区直属预备队','保留一支不必向地方借调的机动力量，减少紧急命令遭到拖延的风险。','training'),('hue','与顺化驻军建立协同','岘港不能独自维持北方门户。联络官需要把两地的预备方案接起来。','defence'),('reports','军区战情汇报','让基层的粮弹与伤亡进入司令部的日常判断。','intel'),('agreement','重订中央军费协议','军区将明确出兵义务，中央也必须明确支付军费的责任。','civil')]),
('defence','中部沿海防线','港口、公路与山口共同组成军区的生命线。只盯住北面的敌人，会忽略侧后的危险。','shield',[
('fort','岘港环形工事','围绕交通节点设置工事，使守军能够互相支援。','fort'),('patrol','山口巡逻部队','把熟悉山路的小部队放到交通要道，减少后方突然出现敌军的机会。','training'),('supply','军区弹药储备','补给计划要能承受一段时间的交通中断。','supply'),('road','沿海交通修复','道路施工优先服务伤员后送和紧急增援。','road'),('elastic','保留机动纵深','不在孤立据点消耗全部兵力，让预备队能够应对真正的突破。','defence')]),
('port','港口城市的战争','远征军、商人和地方行政都在使用同一座码头。有效的协调比更多临时命令更有用。','factory',[
('dock','岘港码头调度','将军需船期和道路运输接起来，减少仓库拥堵。','transport'),('repair','港区修械厂','让港口能够处理车辆和轻武器维修，缩短送返后方的时间。','arms'),('industry','维持城市生产','军区的长期存在需要城市维持就业和粮食供应。','industry'),('police','城市警务协调','地方警察与守军交换线索，避免各自维护一份互不相通的名单。','intel'),('civic','城市重建基金','将部分资源交给民事设施，减少战争对港口生活的破坏。','civil')]),
('politics','西贡来电','来自首都的命令并不总是一致。军区司令部必须决定，在中央危机中如何保护自己的部队。','radio',[
('neutral','军区不卷入私人争斗','将军官的私人立场与部队命令分开，先保证防区继续运转。','civil'),('liaison','首都联络代表','让军区在各派之间保留消息来源，不把未来押在单一联系人身上。','command'),('loyal','公开确认共同战线','表明军区将继续抵抗外敌，避免中央动荡直接演变成前线真空。','defence'),('autonomy','军区行政自主','以承担本地行政责任为代价，争取更多资源支配空间。','industry'),('refuge','接收溃散部队','为撤下前线的士兵重新登记和补装，防止他们流入首都的派系争斗。','manpower')])],
'KHM':[
('command','金边的中立账本','边境战争正在挤压中立的空间。每一次让步都可能换来眼前安全与下一次要求。','landmark',[
('border','重新勘定边境哨所','明确巡逻和报告职责，减少边境部队在遭遇事件后各自行动。','command'),('patrol','地方边防训练','以训练和通信改善边防，而不是给边境增加无法补给的大部队。','training'),('reports','向金边报告越境事件','让外交判断建立在可以核实的报告上，减少地方谣言左右政策。','intel'),('neutrality','公开重申中立','向各方说明可以接受的边界，为下一轮交涉保留空间。','civil'),('mediation','金边斡旋渠道','将不公开的联络固定下来，使边境摩擦不必立即变成全面战争。','command')]),
('economy','战争边缘的建设','道路与港口能带来收入，也会被交战各方视作补给通道。建设需要与边境政策同时考虑。','factory',[
('roads','乡间道路工程','连接农产区和市场，让地方经济不至于完全依附边境走私。','road'),('industry','基础加工工业','将有限资本用于能服务民生和基本军需的设施。','industry'),('repair','边防修械所','让哨所不必因一批损坏的武器而失去行动能力。','arms'),('port','西哈努克港的货单','对进入港口的物资建立稳定账目，减少秘密运输对财政的侵蚀。','transport'),('reserve','建立应急物资库存','为边境关闭或运输中断保留一定时间的生活与军需储备。','supply')]),
('security','防止战争越过边界','军方对边境局势有自己的判断。政府需要既能执行命令，也能受到约束的安全机构。','shield',[
('staff','整编军队参谋机构','让调动、补给和军费不再依靠临时口头协调。','command'),('training','训练边境预备队','以可持续的规模维持预备兵力，避免动员掏空农业劳动力。','training'),('fort','保护关键渡口','渡口和道路节点比漫长边界上的每一处丛林更值得优先防护。','fort'),('police','行政与警务联合报告','使地方政府能够及时报告军警争执和人口流动。','intel'),('control','确立军队调动程序','把部队调动纳入明确程序，减少政治危机中出现彼此矛盾的命令。','defence')]),
('society','让金边之外的地方运转','地方社会不能只在边境危机时被记起。稳定的行政和生产，是中立政策真正的后方。','tree',[
('rice','恢复农产品流通','减少地方关卡对市场的阻隔，让农户愿意把粮食运出村庄。','civil'),('schools','培训基层行政人员','让地方具备处理账目、登记和民事争议的基本能力。','civil'),('health','省级救护体系','边境难民与伤员需要持续照顾，不能完全交给临时征用。','defence'),('budget','公开地方建设预算','把项目与拨款对照，使中央能够判断资源是否抵达目的地。','command'),('settlement','中立国家的长期安排','把边境管理、财政与地方建设编入同一份计划，避免每次危机都从头开始。','industry')])]
}
CN={};EN={};manifest=[]
def loc(key,cn,en=None):CN[key]=cn;EN[key]=en or cn
REWARDS={
'command':'add_political_power = 75', 'training':'army_experience = 20',
'intel':'add_political_power = 40 add_ideas = v65_intelligence_network',
'civil':'add_stability = 0.04', 'supply':'add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 1200 producer = ROOT }',
'road':'capital_scope = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }',
'arms':'capital_scope = { add_building_construction = { type = arms_factory level = 1 instant_build = yes } }',
'industry':'capital_scope = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }',
'transport':'add_equipment_to_stockpile = { type = motorized_equipment_1 amount = 150 producer = ROOT }',
'fort':'capital_scope = { every_state_province = { add_province_modifier = { static_modifiers = { v65_defensive_position } } } }',
'defence':'add_ideas = v65_prepared_defence', 'pacify':'add_stability = 0.03 FNL = { subtract_from_variable = { v65_infiltration = 1 } clamp_variable = { var = v65_infiltration min = 0 max = 3 } }',
'countertrail':'NVN = { subtract_from_variable = { v65_trail_level = 1 } clamp_variable = { var = v65_trail_level min = 0 max = 5 } } FNL = { subtract_from_variable = { v65_infiltration = 1 } clamp_variable = { var = v65_infiltration min = 0 max = 3 } }',
'crisis':'add_political_power = 50', 'radio':'24 = { add_to_variable = { v65_loyalty = 15 } }',
'lobby':'23 = { add_to_variable = { v65_loyalty = 15 } } 27 = { add_to_variable = { v65_loyalty = 15 } }',
'martial':'v65_enact_martial_law = yes', 'influence':'add_to_variable = { v65_park_influence = 1 } add_political_power = 50',
'funds':'add_political_power = 75 add_stability = -0.02', 'patron':'add_ideas = v65_park_patron',
'guards':'add_ideas = v65_guard_network', 'stay':'add_ideas = v65_regional_network add_stability = 0.05',
'usurp':'v65_park_intervention = yes', 'trail':'NVN = { add_to_variable = { v65_trail_level = 1 } clamp_variable = { var = v65_trail_level min = 0 max = 5 } }',
'infiltration':'FNL = { add_to_variable = { v65_infiltration = 1 } clamp_variable = { var = v65_infiltration min = 0 max = 3 } }',
'fnl_training':'FNL = { army_experience = 25 }', 'fnl_arms':'FNL = { add_equipment_to_stockpile = { type = infantry_equipment_2 amount = 1800 producer = NVN } }',
'guerrilla':'add_ideas = v65_guerrilla_network', 'manpower':'add_manpower = 8000'
}
# Use stable, documented country-scope effects for construction; forts are
# separately placed at the actual DMZ province IDs in state history below.
REWARDS['fort']='add_ideas = v65_prepared_defence army_experience = 10'
for tag,branches in DATA.items():
 root=f'v65_{tag}_briefing';loc(root,{'SVN':'两场战争，一个西贡','PKS':'朴世诚：从归仁开始','NVN':'持久战争的两条战线','FNL':'南方的星火','DNM':'岘港军区的抉择','KHM':'战火边缘的王国'}[tag])
 loc(root+'_desc',{'SVN':'北部的阵地与南方的乡村同时需要兵力。中央还要面对军区、远征军和首都驻军各自的利益。','PKS':'这是一条小说人物的架空路线。朴世诚从归仁出发，在战功、企业与私人部队之间积累力量。','NVN':'北方需要守住阵地，南方需要能够生存的据点。把两者联系起来，才能让战争摆脱单一的正面推进。','FNL':'在金瓯、山地和首都外围之间，联络人员维持着松散的地下网络。让这些据点有能力独立行动。','DNM':'岘港拥有自己的驻军与港口。军区既是北部防线的后方，也在等待首都权力斗争的结果。','KHM':'柬埔寨希望维持中立，但邻国战争正通过边境与港口进入国内。金边必须同时处理建设和安全。'}[tag])
 tree=f'focus_tree = {{\n id = v65_{tag}_tree\n country = {{ factor = 0 modifier = {{ add = 100 tag = {tag} }} }}\n default = no\n reset_on_civilwar = no\n continuous_focus_position = {{ x = 0 y = 1500 }}\n'
 tree+=f' focus = {{ id = {root} icon = GFX_v65_focus_flag x = {(len(branches)-1)*4} y = 0 cost = 2 completion_reward = {{ add_political_power = 50 }} }}\n'
 for col,(branch,name,story,icon,entries) in enumerate(branches):
  # The introductory branch node is selectable and unlocks its own five steps.
  nodes=[(branch,name,story,'command')]+entries;parent=root
  for row,(key,name,story,reward) in enumerate(nodes):
   fid=f'v65_{tag}_{key}';loc(fid,name);loc(fid+'_desc',story)
   available='';exclusive=''
   if tag=='SVN' and key=='crisis':available='available = { custom_trigger_tooltip = { tooltip = v65_requires_front_defeat has_country_flag = v65_front_defeat } }'
   if tag=='PKS' and key=='yushin':
    available='available = { SVN = { has_country_flag = v65_front_defeat exists = yes } NOT = { has_war_with = SVN } }';exclusive='mutually_exclusive = { focus = v65_PKS_remain }'
   if tag=='PKS' and key=='remain':exclusive='mutually_exclusive = { focus = v65_PKS_yushin }'
   # A mutually exclusive fork must share a parent, not depend on its sibling.
   if tag=='PKS' and key=='yushin':parent='v65_PKS_capital_links'
   x=col*8
   if tag=='PKS' and key=='remain':x-=3
   if tag=='PKS' and key=='yushin':x+=3;row-=1
   if tag=='SVN' and key=='martial_focus':x-=3;exclusive='mutually_exclusive = { focus = v65_SVN_civilian }'
   node_icon={'training':'helmet','intel':'radio','civil':'tree','supply':'truck','road':'truck','arms':'factory','industry':'factory','transport':'truck','fort':'shield','defence':'shield','pacify':'tree','countertrail':'radio','crisis':'landmark','radio':'radio','lobby':'scroll','martial':'landmark','influence':'radio','funds':'scroll','patron':'landmark','guards':'shield','stay':'tree','usurp':'landmark','trail':'truck','infiltration':'tree','fnl_training':'helmet','fnl_arms':'factory','guerrilla':'tree','manpower':'helmet'}.get(reward,icon)
   tree+=f' focus = {{\n  id = {fid}\n  icon = GFX_v65_focus_{node_icon}\n  x = {x} y = {2+row*2} cost = {3 if row<2 else 5}\n  prerequisite = {{ focus = {parent} }}\n  {available}\n  {exclusive}\n  completion_reward = {{ {REWARDS[reward]} }}\n  ai_will_do = {{ factor = 1 }}\n }}\n'
   manifest.append({'tag':tag,'id':fid,'x':x,'y':2+row*2,'icon':node_icon});parent=fid
 if tag=='SVN':
  fid='v65_SVN_civilian';loc(fid,'由文官监督军方');loc(fid+'_desc','前线失利并不意味着军令应当接管所有生活。让文官主持危机调查，以公开程序换取驻军和地方的合作。')
  tree+=' focus = { id = v65_SVN_civilian icon = GFX_v65_focus_scroll x = 35 y = 12 cost = 5 prerequisite = { focus = v65_SVN_bargain } mutually_exclusive = { focus = v65_SVN_martial_focus } completion_reward = { v65_lift_martial_law = yes add_ideas = v65_civil_admin 26 = { add_to_variable = { v65_loyalty = 15 } } } }\n'
  manifest.append({'tag':tag,'id':fid,'x':35,'y':12,'icon':'scroll'})
 put(Path(f'common/national_focus/v65_{tag}.txt'),tree+'}')

for lang,items in [('simp_chinese',CN),('english',EN)]:
 put(Path(f'localisation/{lang}/v65_focus_l_{lang}.yml'),'l_'+lang+':\n'+'\n'.join(f' {k}:0 "{v}"' for k,v in items.items()))
 # Remove the earlier overlay's focus strings so each ID has one source.
 for p in (M/f'localisation/{lang}').glob('*.yml'):
  if p.name.startswith('v65_focus_'):continue
  lines=p.read_text(encoding='utf-8-sig').splitlines();lines=[s for s in lines if not re.match(r'\s*v65_(?:SVN|NVN|KHM|PKS|FNL|DNM)_[a-z_]+(?:_desc)?:\d',s)]
  p.write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')

TAGS={'NVN':('北越','North Vietnam',5,'communism','190 40 40'),'SVN':('越南共和国','Republic of Vietnam',25,'neutrality','224 184 67'),'KHM':('柬埔寨王国','Kingdom of Cambodia',32,'neutrality','60 110 180'),'PKS':('朴世诚远征集团','Park Expeditionary Group',15,'neutrality','70 148 130'),'FNL':('南方民族解放阵线','National Liberation Front',30,'communism','166 65 115'),'DNM':('岘港军区','Da Nang Military Command',12,'neutrality','220 140 65'),'XTR':('外围地带','Outer Region',44,'neutrality','65 70 65')}
put(Path('common/country_tags/v65.txt'),'\n'.join(f'{t} = "countries/{t}.txt"' for t in TAGS))
for tag,(cn,en,capital,ideology,rgb) in TAGS.items():
 if tag in ['PKS','FNL','DNM']:put(Path(f'common/countries/{tag}.txt'),f'graphical_culture = asian_gfx\ngraphical_culture_2d = asian_2d\ncolor = {{ {rgb} }}')
 if tag=='XTR':continue
 hist=M/f'history/countries/{tag} - Theater.txt'
 if tag in ['PKS','FNL','DNM']:
  hist.write_text(f'capital = {capital}\noob = "{tag}_1965"\nset_research_slots = 3\nset_stability = 0.55\nset_war_support = 0.65\nset_politics = {{ ruling_party = {ideology} elections_allowed = no }}\nset_popularities = {{ {ideology} = 100 }}\nset_technology = {{ infantry_weapons = 1 infantry_weapons1 = 1 infantry_weapons2 = 1 tech_support = 1 tech_trucks = 1 }}\nadd_ideas = {{ limited_conscription partial_economic_mobilisation export_focus }}\nadd_political_power = 150\nadd_equipment_to_stockpile = {{ type = infantry_equipment_2 amount = 8000 producer = {tag} }}\nadd_equipment_to_stockpile = {{ type = motorized_equipment_1 amount = 200 producer = {tag} }}\n',encoding='utf-8')
 # Remove obsolete generic leaders. Named characters are recruited below.
 s=hist.read_text(encoding='utf-8-sig');s=re.sub(r'create_country_leader\s*=\s*\{[^}]*\}','',s);hist.write_text(s,encoding='utf-8')
for state,owner in [(12,'DNM'),(15,'PKS'),(30,'FNL')]:
 p=M/f'history/states/{state}.txt';s=p.read_text(encoding='utf-8-sig');s=s.replace('owner = SVN',f'owner = {owner} add_core_of = {owner}');p.write_text(s,encoding='utf-8')
# Build genuine defensive depth on both banks of the 17th-parallel sector.
for sid in [9,10]:
 p=M/f'history/states/{sid}.txt';s=p.read_text(encoding='utf-8-sig');s=re.sub(r'\d+ = \{ bunker = 4 \}\s*','',s);ids=re.search(r'provinces = \{([^}]+)',s)[1].split();s=s.replace('buildings = {','buildings = { '+' '.join(f'{i} = {{ bunker = 4 }}' for i in ids),1);p.write_text(s,encoding='utf-8')

template='division_template = { name = "Theater Infantry" regiments = { infantry = { x = 0 y = 0 } infantry = { x = 0 y = 1 } infantry = { x = 0 y = 2 } infantry = { x = 1 y = 0 } infantry = { x = 1 y = 1 } infantry = { x = 1 y = 2 } } }'
units={'SVN':[183,184,187,203,215,222,228,242,261,269,277,282,302,305,311,331], 'PKS':[213,214,215], 'DNM':[191,193,195,198], 'FNL':[353,355,359,360,243,287,316]}
# Resolve locations from state histories instead of hard-coding the wrong town.
for tag,state in [('PKS',15),('DNM',12)]:
 ids=[int(x) for x in re.search(r'provinces = \{([^}]+)',(M/f'history/states/{state}.txt').read_text(encoding='utf-8-sig'))[1].split()];units[tag]=ids[:4]
for tag,ids in units.items():
 names={'PKS':'133rd Battalion Group','DNM':'I Corps Regiment','FNL':'Liberation Detachment','SVN':'ARVN Regiment'}
 put(Path(f'history/units/{tag}_1965.txt'),template+'\nunits = {\n'+'\n'.join(f' division = {{ name = "{names[tag]} {n+1}" location = {pid} division_template = "Theater Infantry" start_experience_factor = {0.45 if tag=="PKS" else 0.3} start_equipment_factor = {0.7 if tag=="FNL" else 1} }}' for n,pid in enumerate(ids))+'\n}')

bookmark='bookmarks = { bookmark = { name = V65_BOOKMARK desc = V65_BOOKMARK_DESC date = 1965.10.28.12 picture = GFX_select_date_1936 default_country = SVN default = yes\n'
for tag in ['SVN','NVN','FNL','PKS','DNM','KHM']:bookmark+=f' {tag} = {{ history = V65_{tag}_DESC ideology = {TAGS[tag][3]} }}\n'
put(Path('common/bookmarks/v65.txt'),bookmark+'} }')
for lang in ['simp_chinese','english']:
 l={}
 for tag,(cn,en,*_) in TAGS.items():
  for suffix in ['','_DEF','_ADJ','_neutrality','_neutrality_DEF','_communism','_communism_DEF','_democratic','_democratic_DEF','_fascism','_fascism_DEF']:l[tag+suffix]=cn if lang=='simp_chinese' else en
  if tag!='XTR':l[f'V65_{tag}_DESC']=CN[f'v65_{tag}_briefing_desc']
 l['V65_BOOKMARK']='1965：战线与暗流' if lang=='simp_chinese' else '1965: Fronts and Undercurrents'
 l['V65_BOOKMARK_DESC']='六个可玩势力。北方阵地对峙，南方游击据点交错；朴世诚与各军区拥有独立的政治路线。前线失利将把战争带入首都。' if lang=='simp_chinese' else 'Six playable factions, a fortified northern front, southern guerrilla enclaves and defeat-driven political crises.'
 put(Path(f'localisation/{lang}/zzzz_v65_campaign_l_{lang}.yml'),'l_'+lang+':\n'+'\n'.join(f' {k}:0 "{v}"' for k,v in l.items()))

(R/'campaign-manifest.json').write_text(json.dumps({'version':'0.4.0','focuses':manifest,'factions':{t:{'name':v[0],'capital':v[2]} for t,v in TAGS.items() if t!='XTR'}},indent=2,ensure_ascii=False),encoding='utf-8')
print('Authored campaign:',len(manifest)+6,'focuses; six playable factions')
