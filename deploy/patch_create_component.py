#!/usr/bin/env python3
"""
Patch create-Cemunwmn.js (the create-new-game page component chunk) so that
its inlined English default translation object becomes Chinese.

This object is the fallback i18n resource for the "create" namespace; by
localising it, the New Campaign / New Game UI renders in Chinese even when the
main zh chunk is not loaded for this namespace.
"""
import re, pathlib, sys

src_path = pathlib.Path(sys.argv[1])
dst_path = pathlib.Path(sys.argv[2])
src = src_path.read_text()

# ---------- Parse the inlined translation object (Vs) ----------
name_match = re.search(r'([A-Za-z]+)=\{[^}]*advancedRulesConfiguration', src)
if not name_match:
    raise RuntimeError('Could not find create translation object')
obj_name = name_match.group(1)
brace_start = name_match.start(0) + name_match.group(0).index('{')
brace = 1
j = brace_start + 1
while j < len(src) and brace > 0:
    if src[j] == '{': brace += 1
    elif src[j] == '}': brace -= 1
    j += 1
obj_text = src[brace_start:j]

# Map every leaf key in the object to the variable that holds its value
key_to_var = {}
def parse_vars(text, prefix=''):
    body = text[1:-1]
    pos = 0
    while pos < len(body):
        while pos < len(body) and body[pos] in ' \t,':
            pos += 1
        if pos >= len(body):
            break
        m = re.match(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', body[pos:])
        if not m:
            pos += 1
            continue
        key = m.group(1)
        pos += m.end()
        while pos < len(body) and body[pos] in ' \t':
            pos += 1
        if body[pos] == '{':
            brace = 1
            p = pos + 1
            while p < len(body) and brace > 0:
                if body[p] == '{': brace += 1
                elif body[p] == '}': brace -= 1
                p += 1
            parse_vars(body[pos:p], f'{prefix}{key}.')
            pos = p
        else:
            m2 = re.match(r'([a-zA-Z_$][a-zA-Z0-9_$]*)', body[pos:])
            if m2:
                key_to_var[f'{prefix}{key}'] = m2.group(1)
            pos += len(m2.group(0)) if m2 else 1

parse_vars(obj_text)

# ---------- Chinese translations ----------
zh = {
    "newGame": "新游戏",
    "numberOfPlayers": "玩家人数",
    "withFriends": "与好友同乐",
    "multihandedSolo": "单人多控",
    "switchingPerspectives": "切换视角",
    "switchingPerspectivesDescription": "在单人多控模式中，你有时需要从特定调查员的角度进行操作。使用玩家标签中的<strong>眼睛</strong>图标切换到该调查员的视角。",
    "campaign": "战役",
    "standalone": "独立剧本",
    "sideStory": "支线故事",
    "requiresInvestigator": "需要 {name}",
    "alphaWarning": "该功能正在开发中，可能尚无法正常运行，请勿针对此功能提交 bug。",
    "betaWarning": "该功能已可测试，但游戏可能会频繁中断。",
    "betaWarningScenario": "该场景已可测试，但游戏可能会频繁中断。",
    "normal": "标准",
    "returnTo": "重返……",
    "fullCampaign": "完整剧本",
    "bothScenarios": "双场景（战役）",
    "scenarios": "场景",
    "partialCampaign": "部分剧本",
    "multiplayerVariant": "多人变体",
    "campaignType": "战役类型",
    "pickScenario": "选择场景",
    "difficulty": "难度",
    "Easy": "简单",
    "Standard": "普通",
    "Hard": "困难",
    "Expert": "专家",
    "includeTarotReadings": "使用塔罗牌解牌",
    "playMode": "游戏模式",
    "singleGroupMode": "单组模式",
    "epicMultiplayerMode": "史诗多人模式",
    "singleScenarioMode": "单场冒险",
    "miniCampaignMode": "迷你战役",
    "miniCampaignDescription": "<p>连续游玩三场游戏——每个组各一场，顺序由你决定。与正常战役不同：</p><ul><li>使用独立剧本的牌组构筑规则，无需从 0 经验开始。</li><li>玩家可以在场景之间更换调查员和/或牌组。</li><li>场景之间不会获得或花费经验。</li><li>没有战役日志；调查员不会获得创伤，被击杀或疯狂的调查员仍可在其他场景中使用。</li></ul>",
    "numberOfGroups": "组数",
    "groupName": "组名",
    "groupPlayers": "玩家",
    "imposeTimeLimit": "设置时间限制",
    "timeLimitMinutes": "时间限制（分钟）",
    "gameName": "游戏名称",
    "create": "创建",
    "chooseYourDeck": "选择你的牌组{s}",
    "tabooList": "禁忌列表：{tabooList}",
    "useExistingDeck": "使用现有牌组",
    "loadNewDeck": "加载新牌组",
    "selectADeck": "-- 选择牌组 --",
    "deckUrlPlaceholder": "ArkhamDB 或 arkham.build 牌组链接",
    "choose": "选择",
    "variant": "战役变体",
    "advancedRulesConfiguration": "高级规则配置",
    "rulesPresets": "预设",
    "presetCustom": "自定义",
    "chapter1Heading": "第一章",
    "chapter2Heading": "第二章",
    "sideStoriesHeading": "支线故事",
    "challengeScenariosHeading": "挑战场景",
    "asIfAtBehavior": "“视作在”行为",
    "asIfAtChapter1": "第一章规则",
    "asIfAtChapter1Description": "“视作在”一个地点的效果在整段卡牌或能力持续期间生效，包括来自其他卡牌的触发窗口。",
    "asIfAtChapter2": "第二章规则",
    "asIfAtChapter2Description": "“视作在”一个地点的效果只在指定能力或行动的结算期间生效。其他卡牌能力和触发窗口仍按实际游戏状态结算。",
    "recommendedOptions": "推荐选项",
    "preset.chapter1.name": "第一章",
    "preset.chapter1.description": "推荐用于第一章战役。",
    "preset.chapter2.name": "第二章",
    "preset.chapter2.description": "推荐用于第二章战役。",
    "recommendedOption.PlayersDoNotControlStoryAssetClues.title": "玩家不控制故事支援上的线索",
    "recommendedOption.PlayersDoNotControlStoryAssetClues.description": "自《铁杉谷盛宴》起，玩家可以控制他们所控制支援上的线索，但这与本战役存在一些奇怪的交互，因此建议启用此选项以将故事支援排除在该规则之外。",
    "recommendedOption.UseSwarmPlaceholders.title": "使用占位卡代替虫群",
    "recommendedOption.UseSwarmPlaceholders.description": "不再使用主调查员牌组中的卡牌作为虫群占位，而是生成不属于任何调查员牌组的占位卡。",
    "fullCampaignOption.theDreamEaters": "The Dream-Eaters<br><small>8 部战役</small>",
    "fullCampaignOption.theDreamQuest": "The Dream-Quest<br><small>4 部战役</small>",
    "fullCampaignOption.theWebOfDreams": "The Web of Dreams<br><small>4 部战役</small>",
}

def js_escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

def translate_object_text(text, prefix):
    body = text[1:-1]
    parts = []
    pos = 0
    while pos < len(body):
        while pos < len(body) and body[pos] in ' \t,':
            pos += 1
        if pos >= len(body):
            break
        m = re.match(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', body[pos:])
        if not m:
            pos += 1
            continue
        key = m.group(1)
        pos += m.end()
        while pos < len(body) and body[pos] in ' \t':
            pos += 1
        if body[pos] == '{':
            brace = 1
            p = pos + 1
            while p < len(body) and brace > 0:
                if body[p] == '{': brace += 1
                elif body[p] == '}': brace -= 1
                p += 1
            nested = body[pos:p]
            parts.append(f'{key}:{translate_object_text(nested, f"{prefix}{key}.")}')
            pos = p
        else:
            m3 = re.match(r'"([^"]*)"', body[pos:])
            if m3:
                val = zh.get(f'{prefix}{key}', m3.group(1))
                parts.append(f'{key}:"{js_escape(val)}"')
                pos += m3.end()
            else:
                m4 = re.match(r"'([^']*)'", body[pos:])
                if m4:
                    val = zh.get(f'{prefix}{key}', m4.group(1))
                    parts.append(f'{key}:"{js_escape(val)}"')
                    pos += m4.end()
                else:
                    pos += 1
    return '{' + ','.join(parts) + '}'

# ---------- Apply patches ----------
new_src = src
replaced = 0

for key, var in key_to_var.items():
    if key not in zh:
        continue
    target = zh[key]
    # Try string assignment (double or single quotes)
    pattern = rf'(?<![a-zA-Z0-9_$])({re.escape(var)})=(["\'])(.*?)\2'
    m = re.search(pattern, new_src)
    if m:
        quote = m.group(2)
        if quote == '"':
            repl_val = js_escape(target)
        else:
            repl_val = target.replace("\\", "\\\\").replace("'", "\\'")
        new_src = new_src[:m.start()] + f'{var}={quote}{repl_val}{quote}' + new_src[m.end():]
        replaced += 1
        continue
    # Try object assignment
    obj_pattern = rf'(?<![a-zA-Z0-9_$])({re.escape(var)})=\{{'
    m2 = re.search(obj_pattern, new_src)
    if m2:
        brace = 1
        p = m2.end()
        while p < len(new_src) and brace > 0:
            if new_src[p] == '{': brace += 1
            elif new_src[p] == '}': brace -= 1
            p += 1
        obj_text = new_src[m2.end()-1:p]
        new_obj = translate_object_text(obj_text, key + '.')
        new_src = new_src[:m2.start()] + f'{var}={new_obj}' + new_src[p:]
        replaced += 1

if replaced < 60:
    raise RuntimeError(f'Only {replaced}/62 translations applied')

dst_path.write_text(new_src)
print(f'create component patched: {replaced} keys -> {dst_path}')
