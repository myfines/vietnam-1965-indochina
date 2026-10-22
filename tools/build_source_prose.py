"""Build source-grounded localization overlays from a reviewed passage set.

This script parses chapter_scenes.py without importing it (or the campaign
generator), validates each mapped scene and passage, then writes a localization
overlay plus provenance manifests. It deliberately leaves unmatched text alone.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "novel-source-passages.json"
SCENES = ROOT / "tools" / "chapter_scenes.py"
OUTPUT = ROOT / "mod" / "localisation" / "simp_chinese" / "zzzzzzzzzzzzzz_v65_source_prose_l_simp_chinese.yml"
PRIVATE_NETWORK_LOC = ROOT / "mod" / "localisation" / "simp_chinese" / "zzzzzzzzzzzz_v65_personal_network_l_simp_chinese.yml"
MANIFEST = ROOT / "source-prose-manifest.json"

# Only replace scene bodies whose chapter and subject directly match the text.
SCENE_MAP = {
    5104: "ch147_quy_nhon_morning",
    5107: "ch165_island_assets",
    5113: "ch185_phu_quoc_101st",
    5114: "ch194_revolution_guard",
    5116: "ch211_hue_force_list",
    5119: "ch241_nguyen_minh_appointment",
    5121: "ch249_beach_vacation",
    5124: "ch280_special_operation_rationale",
}

FOCUS_MAP = {
    'V65_PKS_DESC':'ch3_park_battalion',
    'v65chapter_pks_root_desc':'ch3_park_battalion',
    "v65chapter_pks_relations_special_command_desc": "ch159_joint_command",
    "v65chapter_svn_relations_special_command_desc": "ch159_joint_command",
    "v65chapter_pks_relations_militia_terms_desc": "ch165_island_assets",
    "v65chapter_svn_relations_militia_terms_desc": "ch165_island_assets",
    "v65chapter_pks_island_phu_quoc_plan_desc": "ch165_island_command_meeting",
    "v65chapter_svn_island_phu_quoc_plan_desc": "ch165_island_command_meeting",
    "v65_DNM_hue_desc": "ch211_hue_force_list",
    "v65_NVN_hold_desc": "ch254_nvn_withdrawal_debate",
    "v65_NVN_rear_offensive_desc": "ch254_nvn_rear_guerilla_delay",
}
SPIRIT_MAP = {
    'v65_personal_staff_desc':'ch159_joint_command',
    'v65_daihai_contracts_desc':'ch165_island_assets',
    'v65_island_logistics_desc':'ch185_phu_quoc_101st',
    'v65_network_supply_desc':'ch165_island_assets',
    'v65_private_staff_desc':'ch249_beach_vacation',
    'v65_rotation_desc':'ch168_quy_nhon_withdrawal',
    'v65_park_shadow_ruler_desc':'ch194_revolution_guard',
    'v65_trail_network_desc':'ch216_trail_reinforcements',
}


def parse_scene_ids(path: Path) -> set[int]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "SCENES"
            for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            return {int(row[0]) for row in value}
    raise ValueError(f"SCENES assignment not found in {path}")


def loc_line(key: str, value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f' {key}:0 "{escaped}"'


def main() -> None:
    catalog = json.loads(DATA.read_text(encoding="utf-8"))
    passages = {item["id"]: item for item in catalog["passages"]}
    scene_ids = parse_scene_ids(SCENES)
    missing = sorted(set(SCENE_MAP) - scene_ids)
    if missing:
        raise ValueError(f"Mapped scenes do not exist: {missing}")

    loc: dict[str, str] = {}
    manifest_rows = []
    for scene_id, passage_id in SCENE_MAP.items():
        passage = passages[passage_id]
        quote = passage["quote"]
        digest = hashlib.sha256(quote.encode("utf-8")).hexdigest()
        if digest != passage["sha256"]:
            raise ValueError(f"SHA256 mismatch for {passage_id}")
        if not 100 <= len(quote) <= 250:
            raise ValueError(f"Passage length outside 100–250 for {passage_id}")
        loc[f"v65story.{scene_id}.d"] = quote
        manifest_rows.append({"loc_key": f"v65story.{scene_id}.d", "scene_id": scene_id,
                              "passage_id": passage_id, "chapter": passage["chapter"], "quote_sha256": digest})

    for key, passage_id in FOCUS_MAP.items():
        passage = passages[passage_id]
        digest = hashlib.sha256(passage["quote"].encode("utf-8")).hexdigest()
        if digest != passage["sha256"]:
            raise ValueError(f"SHA256 mismatch for {passage_id}")
        loc[key] = passage['quote']
        manifest_rows.append({"loc_key": key, "passage_id": passage_id,
                              "chapter": passage["chapter"], "quote_sha256": digest})

    # Keep the spirit's mechanics and append one narrowly relevant, sourced
    # description of the private command network. Other ideas remain untouched.
    network_text = PRIVATE_NETWORK_LOC.read_text(encoding="utf-8-sig")
    key = "v65_personal_connections_desc"
    marker = f" {key}:0 \""
    start = network_text.find(marker)
    if start < 0:
        raise ValueError(f"Could not find localization key {key}")
    value_start = start + len(marker)
    value_end = network_text.find('"', value_start)
    original = network_text[value_start:value_end].replace(r'\n','\n')
    passage = passages["ch185_phu_quoc_101st"]
    digest = hashlib.sha256(passage["quote"].encode("utf-8")).hexdigest()
    addition = '\n\n' + passage['quote']
    loc[key] = original + addition
    manifest_rows.append({"loc_key": key, "passage_id": passage["id"], "chapter": passage["chapter"],
                          "quote_sha256": digest, "preserved_existing_mechanics_text": True})

    for key, passage_id in SPIRIT_MAP.items():
        passage=passages[passage_id]
        digest = hashlib.sha256(passage["quote"].encode("utf-8")).hexdigest()
        if digest != passage["sha256"]:
            raise ValueError(f"SHA256 mismatch for {passage_id}")
        loc[key]=passage['quote']
        manifest_rows.append({'loc_key':key,'passage_id':passage_id,'chapter':passage['chapter'],'quote_sha256':digest})
    passage=passages['ch249_beach_vacation']
    loc['v65network.1.d']=passage['quote']
    loc['v65network.1.t']='忙碌之余'
    loc['v65network.1.a']='度假钓鱼。'
    manifest_rows.append({'loc_key':'v65network.1.d','passage_id':passage['id'],'chapter':passage['chapter'],'quote_sha256':passage['sha256']})
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("l_simp_chinese:\n" + "\n".join(loc_line(k, v) for k, v in loc.items()) + "\n", encoding="utf-8-sig")
    MANIFEST.write_text(json.dumps({"version": 1, "generated_by": "tools/build_source_prose.py",
                                    "localization_file": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
                                    "mappings": manifest_rows,
                                    "unmapped_scene_ids": sorted(scene_ids - set(SCENE_MAP))},
                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(loc)} localization keys from {len(set(SCENE_MAP.values()) | set(FOCUS_MAP.values()))} passages")


if __name__ == "__main__":
    main()
