# file-refine-organizer

> 文件夹 / 项目资料精细化整理技能（Agent Skill）——把「整理一下」从随手归拢升级为可复现的七步流程。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](./CHANGELOG.md)

**当前版本 v1.1.0**（2026-10-17）——版本号同步维护于三处：`SKILL.md` frontmatter 的 `version` 字段、本徽章、[CHANGELOG.md](./CHANGELOG.md)（每次变更记录内容）；Git 侧每个版本一个 tag（`git tag` / GitHub Releases）。**装了旧版的，更新时先看 CHANGELOG 确认差异，再 `git pull` 换新版。**

## 这是什么

一个给 AI Agent 用的技能包。当用户说「整理 XX 文件夹／项目／资料」「看看整理好没有」「拆分这个合订 PDF」「把散件归并」「统一命名」「查重」时，按本技能执行——而不是随手归拢了事。

核心主张：**先扫描诊断、列清单确认、再动手；每个编号金额都从原件目视提取；删除永远先进暂存区。**

## 六条铁律

1. **备份先行**——动任何台账／索引文件前先 `.bak-<日期>` 备份。
2. **先扫描列清单，确认后动手**——诊断完成后给选项让用户拍板，不擅自删改。
3. **数据目视提取，禁止估算**——发票号、金额、日期、单号一律渲染原件目视读取；扫描件无文本层也必须看。
4. **删除＝暂存区，不直删**——先移入暂存目录，用户确认无影响后才清空（进系统回收站）。
5. **跨文档交叉验证**——同一事实（金额、票号）至少两个来源比对；矛盾时停下并列差异清单交用户裁定。
6. **过程产物隔离**——脚本、渲染 PNG、暂存件一律放过程产物目录，不落正式资料库。

## 七步流程

```
Step 0 查规则与记忆 → Step 1 摸全貌找惯例 → Step 2 诊断五类问题
→ Step 3 列清单 AskUserQuestion 确认 → Step 4 执行（拆分/归并/改名/查重）
→ Step 5 终态校验（0 散件＋事项文件夹）→ Step 6 台账同步与沉淀
```

五类问题诊断：合订 PDF／散件／命名不规范／缺目录层错位／重复。

三个核心方法：

- **合订 PDF 四步拆分法**：摸结构（逐页文本量／图片数／页面尺寸）→ 渲染目视判界（100 DPI 看首页、疑似结尾页、横向发票页）→ 按页区间 `insert_pdf` 拆分 → 页数合计＋首页文本双校验。合同包按「组成合同的文件」条款保持整件不拆。
- **事项归并＋命名模板**：`日期_文档类型_项目简称_事项及批次_比例_金额_合同号或供应商`；主单 `00_`、附件 `附件N_`；仅下划线、金额纯数字——命名即索引。
- **查重三轨法**：MD5 → 同文件名／同大小交叉 → 渲染目视。跨批次共用材料（合同／审批表）保留；系统散件与拆分件同内容时留拆分件。

## 安装

### WorkBuddy

```bash
git clone https://github.com/joshua644/file-refine-organizer.git ~/.workbuddy/skills/file-refine-organizer
```

或下载 ZIP 解压到技能目录。**新技能需新开会话生效。**

### 其他 Agent 平台

任何采用「技能目录 + SKILL.md」结构的平台（如 Claude Code 的 `~/.claude/skills/`）均可使用：把本仓库放到技能目录下即可。`SKILL.md` 头部 frontmatter 含 `name` / `description` 触发声明，各平台按自身规范读取。

## 依赖与可选增强

| 类型 | 内容 | 说明 |
|---|---|---|
| 硬依赖 | 无 | 本技能自包含，零外部技能依赖即可完整运行 |
| 脚本依赖 | `PyMuPDF`（pip，装虚拟环境内，禁全局 pip） | 仅拆分／检查合订 PDF 时需要 |
| 可选增强 | 宪法审查类技能（如 `skills-constitution`） | Step 0 装了则按其流程执行三查；没装则读文件等效生效，不中断 |

Step 0 的实质动作（读目标库 `AGENTS.md`／知识目录／记忆文件）是纯文件操作——任何「技能目录 + SKILL.md」结构的平台，clone 下来就能用。

## 使用

触发语（任一句即可）：

- 「整理 XX 文件夹／项目／资料」「看看整理好没有」
- 「拆分这个合订 PDF／采购报销单」
- 「把散件按事项归并」「统一命名规范」
- 「查重，重复的删掉只留一份」

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/inspect_pdf.py` | 摸合订 PDF 结构：逐页文本量／图片数／尺寸，输出判界参考 |
| `scripts/split_pdf.py` | 按页区间拆分（`insert_pdf`）＋页数合计／首页文本双校验；页区间表在脚本头部 `JOBS` 改 |
| `scripts/to_recycle_bin.py` | Windows 回收站删除（SHFileOperationW + FOF_ALLOWUNDO），批量清暂存区专用 |

脚本依赖：`pip install PyMuPDF`（装虚拟环境内，禁全局 pip），仅拆分／检查合订 PDF 时需要；另两个脚本只用 Python 标准库（`to_recycle_bin.py` 仅 Windows 有效）。

## 目录结构

```
file-refine-organizer/
├── SKILL.md                     # 技能主文件（铁律＋七步流程＋version 字段）
├── CHANGELOG.md                 # 版本更新日志（升级前先看这里）
├── references/
│   └── 整理细则与案例.md         # 命名模板出处、四步拆分细节、查重判据表、台账坑、实证案例
└── scripts/
    ├── inspect_pdf.py
    ├── split_pdf.py
    └── to_recycle_bin.py
```

## 许可

MIT License，详见 [LICENSE](LICENSE)。
