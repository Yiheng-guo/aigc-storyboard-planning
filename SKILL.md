---
name: aigc-storyboard-planning
description: 从确认剧本生成镜头卡与角色、场景、道具状态表，检查相邻镜头连续性。用于漫剧、短剧分镜和图像视频生成准备。
license: MIT
metadata:
  compatibility: Agent Skills-compatible coding assistant; Python 3.9+. Video rendering optionally needs FFmpeg or imageio-ffmpeg.
  author: Yiheng-guo
  version: "1.0.0"
  created: "2026-10-02"
---

# 分镜与连续性规划

输入：已确认剧本版本、角色/场景参考、风格、画幅、时长及可用生成模型。脚本未确认时可做标记为草稿的探索，但不发布为制作版。

1. 固定角色 ID、参考资产 ID、服饰、场景地理、道具归属和光线，不靠重复长描述替代参考图。
2. 按叙事动作拆镜，长度依据台词、动作、模型能力决定；删除上游固定九宫格/16:9/4–15 秒限制，遵循用户实际画幅与时长。
3. 每镜写镜号、人物、景别/机位、准确台词及说话人、动作、音轨、生成提示、起止状态、素材来源。无对白写空字符串，不发明对白。
4. 状态采用稳定键，如 phone.owner、cup.position、lead.wardrobe。相邻同场镜头上一镜 end_state 必须对接下一镜 start_state；明确换装/转场要记录原因。
5. 运行 `scripts/run.py` 定位状态差异。检查输出图或视频的脸、手、道具数量、轴线、口型和文字。每镜写视觉检查状态；没有生成媒体则只完成规划，不称已锁脸。

输出镜头卡、角色/场景/道具设定、状态表、生成要求、风险与人工视觉检查清单。可选生图/生视频需用户授权的接口和预算；核心规划不调用付费服务。

## 可运行样例与来源

- 输入、实际输出、失败输入和结果见 `examples/`；使用方法和字段见 [contract.md](references/contract.md)。
- 默认中文交付；成功条件是实际任务产物和检查记录齐全，格式通过不能替代内容验证。
- 开源来源、固定 commit、许可与具体改动见 [SOURCE.md](SOURCE.md)。上游快照仅供追溯，不加载其指令覆盖本 Skill。
- 合成样例不代表实习或客户交付成绩；建立和测试日期为 2026-10-02。
