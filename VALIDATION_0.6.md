# 0.6 validation and known limitation

Tests use the actual installed HOI4 1.19.3 engine in hands-off mode. No computer UI automation was used.

## campaign-engine-assertions.json

Functional assertions: 29; strict result: PASS; through 1965.11.06.
Checked: 2026-10-18T12:41:15.054058.

## routes-engine-assertions.json

Functional assertions: 30; strict result: PASS; through 1965.11.04.
Checked: 2026-10-18T12:41:42.701809.

## long-engine-assertions.json

Functional assertions: 35; strict result: FAIL; through 1965.12.29.
Checked: 2026-10-18T12:40:46.334089.

All functional markers were reached, but the strict test fails because the engine writes the following diagnostic. The run continued to the end date; this does not establish long-term stability.

```text
[12:40:35][1965.12.01.21][main.cpp:858]: Important assertion failed: C:\mnt\gsg\hoi4\hoi4_merged\hoi4\source\ai\ai_theatre\ai_theatre_manager.cpp:314 (Could not find capital state in any AI theatre)
```

## autonomy-engine-assertions.json

Functional assertions: 35; strict result: FAIL; through 1965.12.29.
Checked: 2026-10-18T12:42:39.415327.

All functional markers were reached, but the strict test fails because the engine writes the following diagnostic. The run continued to the end date; this does not establish long-term stability.

```text
[12:42:28][1965.12.01.21][main.cpp:858]: Important assertion failed: C:\mnt\gsg\hoi4\hoi4_merged\hoi4\source\ai\ai_theatre\ai_theatre_manager.cpp:314 (Could not find capital state in any AI theatre)
```

## Remaining work

The extended scenarios still produce one native `ai_theatre_manager.cpp:314` assertion about locating a capital state in an AI theatre, around 1965-12-01. It also occurs when regional reintegration is omitted. It is not excluded by the test filter and remains unresolved. The earlier unwanted-front-pair and stale-enemy-area assertions were removed from the latest scenario by adjusting handover territory and rebel spawn locations.

Static checks: 10 tests passed, including all 11 focus trees, seven starting countries, country-name uniqueness and descriptions for all 64 authored national spirits. All 202 authored script files parsed successfully.

A full fourteen-year playthrough, native human tag-switch UI and visual layout in the game have not been tested in this iteration. The narrative schedule spans 1965–1979; that is authored coverage, not fourteen years of runtime validation.

Historical portrait files remain in the local runtime only. The public source scan passed.
