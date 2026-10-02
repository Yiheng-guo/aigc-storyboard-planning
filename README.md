# 分镜与连续性规划 · `aigc-storyboard-planning`

从确认剧本生成镜头卡与角色、场景、道具状态表，检查相邻镜头连续性。用于漫剧、短剧分镜和图像视频生成准备。

**一个独立 Skill，一个独立仓库。** 本仓库只发布 `aigc-storyboard-planning`，入口为根目录 [SKILL.md](SKILL.md)。作者：郭一恒 / Yiheng-guo。创建于2026-10-02，独立发布于2026-10-03。

## 输入、输出与边界

完整流程见 [SKILL.md](SKILL.md)，输入字段、成功条件与失败回退见 [references/contract.md](references/contract.md)。实际样例、输出和检查记录见 [examples/CASE.md](examples/CASE.md)。合成样例不代表真实客户或历史实习成绩。

## 安装与使用

```bash
git clone https://github.com/Yiheng-guo/aigc-storyboard-planning.git
mkdir -p ~/.codex/skills
cp -R aigc-storyboard-planning ~/.codex/skills/
```

如果目标目录已存在，先检查版本并备份，避免混合不同版本。可对兼容Agent说：“使用 aigc-storyboard-planning，根据我的材料执行任务。”

## 本地运行

从仓库根目录运行，输出选择尚不存在的新文件：

```bash
python3 scripts/run.py examples/input.json --output /tmp/aigc-storyboard-planning-result.json
python3 scripts/run.py examples/failure-input.json --output /tmp/aigc-storyboard-planning-failure.json
```

核心工具Python 3.9+标准库可运行，无自动付费API调用。返回成功不等于所有语义判断或生产验收通过；应查看输出状态、未知项和限制。

## 检查

```bash
python3 -m unittest discover -s tests -v
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python validation/quick_validate.py .
```

规范校验与本地样例测试不能替代真实任务内容审核。原型浏览器验证、媒体完整解码等额外记录保留在examples目录；涉及模型、API和客户系统的任务需另提供权限、接口和预算。

## 开源来源与二次开发

[来源与改动](SOURCE.md)逐项说明采用的上游项目、固定版本与二开内容；[sources.json](sources.json)保留固定commit和文件路径；`third_party/`保留本Skill相关原始快照与许可证，`licenses/`便于独立安装时携带许可。上游内容遵循各自许可，不被根许可证覆盖。

本仓库来自原集合的独立拆分，修改的是发布结构。验证用的素材、脚本和来源已随仓库包含，不依赖原集合目录。
