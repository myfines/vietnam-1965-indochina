# 0.9 验证记录

本机 HOI4 1.19.3；真实引擎通过命令行以 hands-off 模式运行，未操作桌面或游戏界面。

| 检查 | 结果 |
|---|---|
| Python 静态、内容和挂载回归 | 38项通过 |
| 原著摘录比对 | 55处通过；忽略换行、空白和外围摘录引号 |
| 原文数据哈希 / 本地化覆盖键 | 通过；所有覆盖键对应已有内容 |
| 出访、人物、通讯录、国策选择、接管与45天回访 | 30项真实引擎断言通过 |
| 内部停火条件、独立外战保留、冷却、北越与解放阵线各自事件 | 8项真实引擎断言通过 |
| 运行日志 | 上述最终运行无模组运行错误；外部已安装DLC/创意工坊描述符错误单独排除 |
| 本机安装一致性 | 无意外差异；15个PKS旗帜为预期的本地太极旗替换 |
| 重建幂等性 | 重建后已生成模组文件无变化 |
| 公共源码检查 | 通过；完整小说、私人笔记、下载的历史头像和游戏原图均未打包公开 |

引擎测试使用真实设立军区、抗命与起兵过程，建立军区对西贡、军区对解放阵线的两场战争后，调用正式停火效果。未同意、缺少中间人或中央同意、其他军区代签均不能停战；同意后只结束内部战争。

出访计时测试在出访后立即并入南越，继续运行到12月，确认原PKS消失后仍能解锁。开局司令蔡命新、出访不转移领土、私人账本保留、接管镜像跳过已领奖节点等均有对应断言。

UI只做离线渲染、节点几何与控件边界检查；决议分类插画使用核对过的原版sprite。未做游戏内人工视觉验收。三个1975年时局事件的脚本已加载解析，但未自然推进至1975年验证；十四年完整战局也未验证。旧版强制多军区整合场景曾出现AI战区断言，本轮没有将该旧场景宣称修复。

可复现入口：

```powershell
python -X utf8 tools/rebuild_campaign.py
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
python -X utf8 tools/install.py
$env:V65_GUEST_TEST='1'; python -X utf8 tools/campaign_smoke_test.py
Remove-Item Env:V65_GUEST_TEST
$env:V65_STORY_REVISION_TEST='1'; python -X utf8 tools/campaign_smoke_test.py
Remove-Item Env:V65_STORY_REVISION_TEST
python -X utf8 tools/render_command_preview.py
python -X utf8 tools/check_public.py
```

必须串行运行引擎测试；测试会保存并恢复原有挂载配置、删除临时场景并关闭自己启动的游戏进程。
