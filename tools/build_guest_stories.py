"""Generate a five-step player-mediated South Vietnamese armistice chain.

The chain only handles an actual internal war between SVN and one regional
command. Every side gets a choice; acceptance ends only that command's war with
SVN, never its war against FNL. No ruler changes or date-based peace are used.
"""
from pathlib import Path
from long_foundation import loc_text

M = Path(__file__).resolve().parents[1] / 'mod'


def put(path, text):
    """Write only the generated guest-story files."""
    target = M / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + '\n', encoding='utf-8-sig' if str(path).endswith('.yml') else 'utf-8')


REGIONS = ('DNM', 'HLC', 'MKG', 'BHD')
ACTORS = ('SVN', 'PKS', 'PHQ', *REGIONS)
TARGET_FLAGS = {tag: f'v65_guest_target_{tag}' for tag in REGIONS}

# Full source passages are used as event prose. Each item was checked against
# the novel file; chapter titles remain here for reviewers, not shown in-game.
STORY_SOURCES = {
    1: (335, '我成委员长了？', '吴光长现在头皮头发麻了，他不想和杨文明的政变军打，可又不想让他们政变成功，而其寄希望于说合，因此，他绕过了南越国防部，直接给槟知城内的守军下达了全面警戒，但不准开第一枪的命令。'),
    2: (338, '时辰没算对！', '26日的政变行动，刚开始都还一切顺利，政变军顺利的占领了不少的政府机构，可等到吴光长通电表示，他要坚决站在阮文绍一方后，整个槟知的局面对于杨文明他们而言，那简直就是急转直下，特别是吴光长手中的第八装甲骑兵团进城后，大量政变军占领的据点都开始陆续丢失。'),
    3: (339, '新总统杨文明', '而危在旦夕的吴光长，在西贡陷落之后，便立即请李威炎从中说和。经过了长时间的沟通，当越共都已经开始尝试进攻吴光长的湄公河防线之后，双方总算是达成了一份协议。'),
    4: (342, '杨文明的大棋', '最后个大佬自然就是李威炎咯，李威炎可是富国岛的军政长官，富国岛现在的坚若磐石的局面，可完全是李威炎缔造的，名望在整个富国岛上简直是无人能比，在加上他背后有美国人和韩国人撑腰，因此李威炎在现在的南越政局的话语权最重。如果不是李威炎的身体不好，而且其本人也无意当什么总统，不然的话，李威炎完全可以在美国和韩国的支持下，成为南越总统。'),
    5: (349, '拿这考验我？', '更重要的是，如果失败了，最好能通过这场所谓的大反攻，大量消耗掉，杨文明和吴光长手中的兵力，让他们两人都变成光杆司令。那这越南共和国的总统位置，他阮文绍坐的，他杨文明坐的，我李威炎就坐不得了？也正是因为这个原因，富国岛这次派出的反攻部队，不同于杨文明和吴光长把自己的精锐部队派了上去，富国岛派出的部队，绝大部分都是临时从难民营里，临时组建的炮灰部队，富国岛真正的主力，可都在富国岛上面纹风不动呢。'),
    6: (294, '诉苦大会', '1975年3月16日，上午十时许，越南共和国，归仁市，第二战术区司令部，作战会议室内。第二战术区司令官阮文明上将，此刻正双手拄着自己的下巴，看着会议室内的各个长官。自从朴世诚司令官明确了将要逐步撤出第一、第二战术区后，情况最严重的第二战术区各部队便开始收缩防御，准备进行撤退了。'),
    7: (310, '小政变、朴问', '吴光长沉默了好一会，然后低声说道，“总长，现在阮总统晕倒的消息还没传出，就我个人认为，应该立即以阮总统的名义，发布转进命令，让部队迅速转进。”转进自然是应该的，可这用阮文绍的名义，就让高文园有些犯难了，以阮文绍的性格，要是知道了高文园这么干，后面不找高文园的麻烦那几乎是不可能的事。'),
    8: (327, '胜利回国、微妙的南越政治局面', '阮文绍在拿到了美国的投资之后（美国看到南越政权有稳住的迹象了，又开始重新注资了，只不过并不算太多，这次南越仅拿到了一笔价值5000万美元的援助，实际到账估计也就2000万吧，毕竟还有想要进步的美国专员嘛，而且这笔援助也不都是现金，还有不少是武器装备呢），做主把大头的金钱和武器装备都分配给了阮文明和吴光长，其中阮文明占了差不多一半分配比例。他杨文明和高文园几乎只拿到了很少的一些，这就让杨文明相当的不爽了。'),
}

# Chapter 28 establishes that Li Wei-yan is a separate Chinese-Vietnamese
# business contact who has met Park Seong-cheol; this stays as source metadata.
IDENTITY_EVIDENCE = (
    28,
    '二鬼子遇见真汉奸',
    '进来的这人名叫李威炎，是个华人，祖籍在山东人，还在美国留过学，回到越南后成为了一个十分合格的美国买办，更重要的是，他是归仁市的华人商会（黑帮）的副会长，他们这个华人帮派，还和美国那边的洪门有千丝万缕的联系。',
    '李威炎和朴世诚也接触过一两次了，自然是知道朴世诚会说中文，虽然他也不知道韩国总统朴正熙的侄子，为什么中文会说的这么溜。',
)


def build_localisation():
    values = {
        'v65_guest_mediation': '南越军区停火斡旋',
        'v65guest.cancel': '撤回斡旋提案。',
        'v65_guest_mediation_desc': '需要西贡与至少一个地方军区实际交战，且富国岛特别区存在并控制本岛。发起方选择交战军区；军区、富国岛、西贡、军区依次答复。四方同意后，只结束该军区与西贡的战争；30天未完成则失效。',
        'v65guest.1.t': '吴光长不准先开第一枪', 'v65guest.1.a': '向岘港军区递交斡旋提案。', 'v65guest.1.b': '向西原军区递交斡旋提案。', 'v65guest.1.c': '向湄公河军区递交斡旋提案。', 'v65guest.1.e': '向东南军区递交斡旋提案。',
        'v65guest.2.t': '槟知政变急转直下', 'v65guest.2.a': '同意把条件交富国岛传递。', 'v65guest.2.b': '拒绝继续会谈。',
        'v65guest.3.t': '西贡陷落后的斡旋请求', 'v65guest.3.a': '接受斡旋，要求西贡书面答复。', 'v65guest.3.b': '拒绝介入。',
        'v65guest.4.t': '富国岛向西贡传话', 'v65guest.4.a': '接收条件，交由交战军区答复。', 'v65guest.4.b': '拒绝该项停火提议。',
        'v65guest.5.t': '富国岛保留岛上主力', 'v65guest.5.a': '接受双方已同意的内部停火。', 'v65guest.5.b': '拒绝停火，维持战争。',
        'v65guest.6.t': '归仁第二战术区收缩防线', 'v65guest.6.a': '要求前线核对撤退部署。', 'v65guest.6.b': '暂不调整防线。',
        'v65guest.7.t': '阮总统昏倒后的转进命令', 'v65guest.7.a': '讨论以总统名义发布命令。', 'v65guest.7.b': '暂缓发布命令。',
        'v65guest.8.t': '援助分配激化军区不满', 'v65guest.8.a': '召开军区协调会核对分配。', 'v65guest.8.b': '维持现有分配。',
    }
    for i, (_, _, quote) in STORY_SOURCES.items():
        values[f'v65guest.{i}.d'] = quote
    return values


def generate():
    war_any = 'OR = { ' + ' '.join(f'{t} = {{ exists = yes has_war_with = SVN NOT = {{ has_country_flag = v65_guest_mediated }} }}' for t in REGIONS) + ' }'
    shared = 'PHQ = { exists = yes controls_province = 361 NOT = { has_war_with = SVN } }'
    target_guard = 'OR = { ' + ' '.join(f'has_global_flag = {flag}' for flag in TARGET_FLAGS.values()) + ' }'
    war_target = 'OR = { ' + ' '.join(f'AND = {{ has_global_flag = {flag} {tag} = {{ exists = yes has_war_with = SVN }} }}' for tag, flag in TARGET_FLAGS.items()) + ' }'

    def dispatch(event_id):
        return ' '.join(
            f'if = {{ limit = {{ has_global_flag = {flag} {tag} = {{ has_war_with = SVN }} }} '
            f'{tag} = {{ country_event = {{ id = v65guest.{event_id} }} }} }}'
            for tag, flag in TARGET_FLAGS.items()
        )

    category = f'''v65_guest_stories = {{
 icon = GFX_decision_category_generic_political
 allowed = {{ OR = {{ {' '.join(f'tag = {tag}' for tag in ACTORS)} }} }}
 visible = {{ SVN = {{ exists = yes }} {shared} }}
}}'''
    # The initiator must be one of the actual parties; offer only a different
    # regional opponent when the initiating country itself is a region.
    target_options = []
    for letter, tag in zip('abce', REGIONS):
        target_options.append(f''' option = {{ trigger = {{ {tag} = {{ exists = yes has_war_with = SVN NOT = {{ has_country_flag = v65_guest_mediated }} }} NOT = {{ tag = {tag} }} }} name = v65guest.1.{letter}
  set_global_flag = {TARGET_FLAGS[tag]} {tag} = {{ country_event = {{ id = v65guest.2 }} }} }}''')
    decisions = f'''v65_guest_stories = {{
 v65_guest_mediation = {{
  icon = generic_political_discourse cost = 25
  visible = {{ OR = {{ {' '.join(f'tag = {tag}' for tag in ACTORS)} }} {war_any} {shared} NOT = {{ has_global_flag = v65_guest_talks_open }} }}
  available = {{ {war_any} {shared} NOT = {{ has_global_flag = v65_guest_cooldown }} }}
  days_re_enable = 30
  complete_effect = {{ set_global_flag = v65_guest_talks_open set_global_flag = v65_guest_cooldown country_event = {{ id = v65guest.1 }} country_event = {{ id = v65guest.99 days = 30 }} }}
  ai_will_do = {{ factor = 0 }}
 }}
}}'''
    effects = 'v65_guest_clear = { clr_global_flag = v65_guest_talks_open clr_global_flag = v65_guest_preliminary_agreed clr_global_flag = v65_guest_region_agreed clr_global_flag = v65_guest_island_agreed clr_global_flag = v65_guest_central_agreed ' + ' '.join(f'clr_global_flag = {flag}' for flag in TARGET_FLAGS.values()) + ' }'
    selected='OR = { '+' '.join(f'AND = {{ tag = {tag} has_global_flag = {flag} }}' for tag,flag in TARGET_FLAGS.items())+' }'
    effects += f'''\nv65_guest_finish = {{ if = {{ limit = {{
 has_global_flag = v65_guest_talks_open has_global_flag = v65_guest_region_agreed
 has_global_flag = v65_guest_island_agreed has_global_flag = v65_guest_central_agreed
 NOT = {{ has_country_flag = v65_guest_mediated }} {selected} {shared}
 has_war_with = SVN SVN = {{ exists = yes }}
 }} white_peace = SVN set_country_flag = v65_guest_mediated set_global_flag = v65_guest_success v65_guest_clear = yes }} }}'''
    target_guard = 'OR = { ' + ' '.join(f'has_global_flag = {flag}' for flag in TARGET_FLAGS.values()) + ' }'
    war_target = 'OR = { ' + ' '.join(f'AND = {{ has_global_flag = {flag} {tag} = {{ exists = yes has_war_with = SVN }} }}' for tag, flag in TARGET_FLAGS.items()) + ' }'
    events = ['add_namespace = v65guest']
    events.append('''country_event = { id = v65guest.1 title = v65guest.1.t desc = v65guest.1.d picture = GFX_report_event_generic_diplomacy is_triggered_only = yes
 trigger = { has_global_flag = v65_guest_talks_open ''' + war_any + ' ' + shared + ' }\n' + '\n'.join(target_options) + '\n option = { name = v65guest.cancel v65_guest_clear = yes }\n}')
    events.append(f'''country_event = {{ id = v65guest.2 title = v65guest.2.t desc = v65guest.2.d picture = GFX_report_event_generic_diplomacy is_triggered_only = yes
 trigger = {{ has_global_flag = v65_guest_talks_open {target_guard} {war_target} }}
 option = {{ name = v65guest.2.a ai_chance = {{ factor = 70 }} set_global_flag = v65_guest_preliminary_agreed PHQ = {{ country_event = {{ id = v65guest.3 }} }} }}
 option = {{ name = v65guest.2.b ai_chance = {{ factor = 30 }} v65_guest_clear = yes }} }}''')
    events.append(f'''country_event = {{ id = v65guest.3 title = v65guest.3.t desc = v65guest.3.d picture = GFX_report_event_generic_diplomacy is_triggered_only = yes
 trigger = {{ has_global_flag = v65_guest_talks_open has_global_flag = v65_guest_preliminary_agreed {war_target} SVN = {{ exists = yes }} }}
 option = {{ name = v65guest.3.a ai_chance = {{ factor = 75 }} set_global_flag = v65_guest_island_agreed SVN = {{ country_event = {{ id = v65guest.4 }} }} }}
 option = {{ name = v65guest.3.b ai_chance = {{ factor = 25 }} v65_guest_clear = yes }} }}''')
    events.append(f'''country_event = {{ id = v65guest.4 title = v65guest.4.t desc = v65guest.4.d picture = GFX_report_event_generic_diplomacy is_triggered_only = yes
 trigger = {{ has_global_flag = v65_guest_talks_open has_global_flag = v65_guest_island_agreed {war_target} }}
 option = {{ name = v65guest.4.a ai_chance = {{ factor = 80 }} set_global_flag = v65_guest_central_agreed {dispatch(5)} }}
 option = {{ name = v65guest.4.b ai_chance = {{ factor = 20 }} v65_guest_clear = yes }} }}''')
    events.append(f'''country_event = {{ id = v65guest.5 title = v65guest.5.t desc = v65guest.5.d picture = GFX_report_event_generic_diplomacy is_triggered_only = yes
 trigger = {{ has_global_flag = v65_guest_talks_open has_global_flag = v65_guest_central_agreed {target_guard} {war_target} SVN = {{ exists = yes }} }}
 option = {{ name = v65guest.5.a ai_chance = {{ factor = 75 }} set_global_flag = v65_guest_region_agreed v65_guest_finish = yes }}
 option = {{ name = v65guest.5.b ai_chance = {{ factor = 25 }} v65_guest_clear = yes }} }}''')
    # Independent, one-time snapshots follow source-chapter order. Their
    # on-action gate requires actual internal conflict or low central prestige.
    for event_id, earliest, flag in ((6, '1975.3.15', 'v65_guest_scene_294'), (7, '1975.4.01', 'v65_guest_scene_310'), (8, '1975.6.01', 'v65_guest_scene_327')):
        events.append(f'''country_event = {{ id = v65guest.{event_id} title = v65guest.{event_id}.t desc = v65guest.{event_id}.d picture = GFX_report_event_generic_diplomacy is_triggered_only = yes
 trigger = {{ NOT = {{ has_global_flag = {flag} }} date > {earliest} }}
 immediate = {{ set_global_flag = {flag} }}
 option = {{ name = v65guest.{event_id}.a }} }}''')
    events.append('''country_event = { id = v65guest.99 hidden = yes is_triggered_only = yes immediate = { v65_guest_clear = yes clr_global_flag = v65_guest_cooldown } }''')
    stress = f'SVN = {{ exists = yes }} OR = {{ {war_any} SVN = {{ check_variable = {{ v65_central_prestige < 30 }} }} }}'
    on_actions = f'''on_actions = {{
 on_daily = {{ effect = {{ if = {{ limit = {{
  OR = {{ has_global_flag = v65_guest_talks_open has_global_flag = v65_guest_cooldown }}
  OR = {{ NOT = {{ SVN = {{ exists = yes }} }} NOT = {{ {shared} }} }}
 }} v65_guest_clear = yes clr_global_flag = v65_guest_cooldown }} }} }}
 on_monthly = {{ effect = {{
  if = {{ limit = {{ date > 1975.3.15 NOT = {{ has_global_flag = v65_guest_scene_294 }} {stress} }} SVN = {{ country_event = {{ id = v65guest.6 }} }} }}
  else_if = {{ limit = {{ date > 1975.4.01 has_global_flag = v65_guest_scene_294 NOT = {{ has_global_flag = v65_guest_scene_310 }} {stress} }} SVN = {{ country_event = {{ id = v65guest.7 }} }} }}
  else_if = {{ limit = {{ date > 1975.6.01 has_global_flag = v65_guest_scene_310 NOT = {{ has_global_flag = v65_guest_scene_327 }} {stress} }} SVN = {{ country_event = {{ id = v65guest.8 }} }} }}
 }} }} }}'''
    for lang in ('simp_chinese', 'english'):
        put(Path(f'localisation/{lang}/zzzzzzzz_v65_guest_stories_l_{lang}.yml'), loc_text(build_localisation(), lang))
    put(Path('common/scripted_effects/v65_guest_stories.txt'), effects)
    put(Path('common/decisions/categories/v65_guest_stories.txt'), category)
    put(Path('common/decisions/v65_guest_stories.txt'), decisions)
    put(Path('events/v65_guest_stories.txt'), '\n'.join(events))
    put(Path('common/on_actions/v65_guest_stories.txt'), on_actions)
    print('Generated five-step mediation and three independent sourced situation events.')


if __name__ == '__main__':
    generate()
