# GR III Firmware Research Skill (agent-first)
# GR III 固件研究 Skill（面向 Coding Agent）

> 一个供 Coding Agent 阅读和使用、fail-closed 的 RICOH GR III 固件研究 Skill。
> An agent-oriented, fail-closed research skill for studying supported RICOH GR III firmware and guiding local research workflows.

---

# 简体中文版

## 这是什么

这是一个给 Coding Agent 使用的 **RICOH GR III 固件研究 Skill**。

它整理了 GR III 2.10 的历史架构研究、六槽扩展、彩色原生 Grain、RAW Development、Playback、per-file identity 与持久化模型。具体版本、直接实机回执、继承证据与限制见 [证据台账](references/evidence-register.md)。v0.1 是 knowledge / evidence / research Skill，未提供固件生产流水线。

本项目不是一键刷机工具，**不提供、不托管、不分发任何原厂或修改后的 RICOH firmware，也不提供 firmware 修改服务**。

## ⚠️ WARNING（务必先读）

- **修改相机 firmware 可能导致相机永久变砖。**
- 可能失去保修和官方支持。
- 离线 validation 不等于真机安全。
- **本项目不提供修改固件；本项目不替用户刷机。**
- **Complete boot failure（完全无法启动）目前没有已验证的恢复路径（NO VERIFIED RECOVERY PATH）。**
- **如果不能接受损失这台设备，请不要进行任何实验。**

## 这不是什么

本项目明确不做，也不会成为：

- firmware modification service（firmware 修改服务）
- firmware hosting / mirror / download service（固件托管、镜像、下载服务）
- 代第三方生成 firmware 的服务
- 远程 firmware 修改；接收用户上传的 firmware；向用户返回修改后的 firmware 文件
- GUI / Web Editor / macOS App / Windows App
- one-click firmware tool / auto-flash / consumer wizard / installer
- ready-to-flash firmware 下载 / 预编译修改固件 / firmware pack / preset pack / LUT pack
- "小白三步刷机教程"

**不要把本项目建设成"上传 firmware → 网站帮你修改 → 下载 firmware"，也不要把仓库做成 firmware 下载站。**

## v0.1 可执行范围与扫描限制

本版仅保留文档 / evidence 检查、发布 containment scanners 与合成夹具生成器。**没有 candidate builder、repacker、固件安全 validator、SD staging 或 SD write 入口**；也没有固件 inspect / decode 工具。Agent 不得从私有工程或旧包重新接入这些入口。合成夹具只写入新建的系统临时目录，不是 firmware / preset 产品。

扫描器只报告发布内容检查结果，**不是刷写安全验证器（NOT A SAFETY VALIDATOR）**。本版 helper 不会产生可刷写文件，也不输出设备安全结论。

发布扫描器在本次实际扫描的 release tree 与归档内容中未发现命中项。扫描覆盖所有文件，并有边界地递归检查 ZIP、TAR、GZ、XZ 和 BZ2；缺失路径、无法检查的归档、未知二进制及超限输入失败。限制为每文件 8 MiB、累计处理 64 MiB、4096 项、四层归档及 200 倍解压比。它不能证明不存在任意私人信息、第三方内容或自定义编码；不检查外部文件系统、用户电脑、未来提交或无关私有历史。详见 [扫描策略](references/release-scan-policy.md)。

## 干净公开历史要求

**CLEAN_HISTORY_REQUIRED / CLEAN_PUBLIC_HISTORY_REQUIRED**：v0.1 必须从新建独立仓库、干净的第一次公开提交发布；不得导入私有开发 `.git` 或旧提交历史，不 fork 私有仓库，不推送旧历史。本 RC 没有公开 Git 历史；不得声称已经检查不存在的历史。后续发布阶段执行此要求。

## 适用人群 / Intended audience

- 熟悉 Coding Agent 与本地开发环境；
- 理解 firmware version、SHA-256、validation 与 recovery boundary；
- 明白修改 firmware 有真实硬件风险。

> 如果不熟悉以上任何一项，请不要用本项目进行实验。

## 使用方式：与 Coding Agent 配合

1. Clone / 下载本 Skill；
2. 把 Skill 交给**你自己的 Coding Agent**；
3. 用自然语言描述研究目标；
4. Agent 阅读 `SKILL.md` + `references/`，判断目标是否位于 verified boundary；
5. Agent 进行只读研究 / 分析；本版不生成 candidate、不修改固件、不写 SD；超出历史证据范围的目标进入 `RESEARCH_ONLY`；
6. **Agent 不得把未经证明的结果描述成"可安全刷写"。**

## 支持的设备与固件

- 仅支持**标准 RICOH GR III** 的**官方 firmware 2.10**（以 exact SHA-256 识别）。
- GR IIIx / GR IV / HDF 与其它版本不受支持。

**版本字符串不是 provenance**。Agent 不得只因为文件名是 `fwdc239b.bin`、相机 UI 显示 2.10、或用户口述"这是官方 2.10"，就认定 firmware 身份；应以 **exact SHA-256 + 产品/机型标识 + 已知官方来源**综合判断。对未知来源 firmware：

`UNKNOWN_FIRMWARE_LINEAGE` / `RESEARCH_ONLY` —— **不要继续 patch**。

## Verified boundary（已验证范围）

历史研究记录覆盖的架构范围（仅此基线；具体等级见证据台账，不代表本版工具能力）：

- 固件容器与双校验和（integrity checksum，非加密签名）；
- 六个新增 Image Control slots：public 30..35 / processing 26..31 / DNG `0x4f` 0x010C..0x0111；
- RAW selector 14..19（13 保留）；
- Shooting 参数持久化（RAM bank、私有 record、Grain key）；
- UserData / U / BOX 处理（custom 身份在写入 native schema 前规范化）；
- 彩色 Image Control 原生 Grain（含 per-file 编码与显示链）；
- JPEG / DNG per-file identity；
- RAW Development 集成（槽位、参数、Grain、As Shot 默认身份恢复）；
- Playback identity / DISP 参数 / per-file Grain（property37 / property140）；
- 相机仍可正常启动时的官方固件恢复路径。

超出以上范围的修改（例如 slot 7+、其它固件版本、其它机型、无关子系统）默认进入 **`RESEARCH_ONLY`**：只做只读研究，不生成可刷写结论，禁止套公式外推。

**设备验证口径**：核心功能路径有与具体版本绑定的实机验证，并配有大量静态 / 离线回归覆盖；**并非每一种功能组合都在相机上做过穷举测试**。最终 `93588df2…` 的直接回执覆盖彩色 Grain 修复；从 `a2fcd40b…` 保留的路径标为 **INHERITED BY STRUCTURAL EQUIVALENCE**，而非本版重新穷举实机验收。证据台账说明来源记录及本轮未在相机上独立重验的限制。

## 固件分发边界（Firmware distribution boundary）

本仓库**只提供**：

- 独立研究笔记、固件架构知识（地址 / 映射 / 语义）、已验证边界、证据方法论；
- fail-closed guardrails 与 Agent 指令；
- 本轮审查未发现专有固件数据的文档检查 / containment / 合成夹具辅助脚本。

本仓库**绝不提供、托管、镜像、打包、分发**：

- 原厂 RICOH firmware；修改后的 RICOH firmware；ready-to-flash firmware；
- 生成的 candidate firmware；decoded firmware 镜像；提取的 RTOS 镜像；
- 固件资源导出（含 ICONBIN dump）；固件备份镜像；recovery firmware 包；
- 私人 firmware 副本；第三方 custom firmware。

**不代用户取得 firmware**：本项目不代为下载、不抓取、不镜像 RICOH 官方 firmware；不附带下载包；不提供第三方下载来源。

> 本仓库不提供 RICOH 官方固件。用户如需进行本地研究，必须自行通过 RICOH IMAGING 官方渠道合法取得受支持的 firmware。

**不提供 firmware 修改服务**：本仓库不接收用户 firmware 后代为修改；不远程生成 customized firmware；不承诺提供 ready-to-flash 文件；不代用户刷入设备。

**本地研究模型（Local-only research model）**：如果用户自行决定进行实验，应在自己的电脑上，使用自己合法取得的官方固件，并由自己控制的本地 Agent / 工具执行。

## 非官方声明

本项目是**独立的社区研究项目，与 RICOH IMAGING 无关联、未获其背书**。"RICOH"、"GR" 等商标归其各自权利人所有。

## 法律与责任（中性表述）

> This repository is provided for independent technical research and education. Users are responsible for complying with applicable law, license terms and agreements in their jurisdiction.
>
> 本仓库用于独立技术研究与教育用途。用户需自行遵守其司法辖区的适用法律、许可条款与协议。

本项目**不作任何法律保证**：不声称"完全合法"；不声称 RICOH EULA 一定无效；不声称 reverse engineering 在所有地区一定合法；不声称写了免责条款就不存在责任。本 README 不构成法律意见。

许可范围：本仓库的 MIT License **仅覆盖项目原创代码与文档**，**不覆盖 RICOH firmware**；用户自备的固件与 preset 数据均受其自身权利与条款约束。

RICOH 官方 GR III 固件下载页所附软件协议的第 4 项限制修改及逆向工程，第 6 项限制向第三方转交软件或副本及转授许可。请阅读 [RICOH 官方固件与软件许可页面](https://www.ricoh-imaging.co.jp/english/support/digital/gr3_s.html)。

本项目不分发、不接收、不远程修改 firmware，可以减少某些分发与服务层面的风险面，但**并不意味着用户在本地修改或逆向官方 firmware 涉及的协议或法律风险消失**。合法取得副本不自动授予修改、逆向或再分发权利。使用这些研究前，请审查适用的 RICOH 软件许可条款及所在司法辖区法律；本项目不判断条款在各地区的可执行性或法定例外。

## Recovery（恢复）与状态兼容

**Bootable recovery（可启动恢复）**：只有相机仍能正常启动时官方回刷成功的历史报告；现有回执未闭合精确来源候选 SHA，不作为最终 golden 的直接恢复验收。证据台账按该精确归属标为 UNKNOWN。

**Complete failure（完全失败）**：complete boot failure / interrupted flashing / flash corruption / bootloader failure 当前：

`NO VERIFIED RECOVERY PATH`

**Persistent-state compatibility（持久化状态兼容）**：不要声称"任何 custom 状态下回刷官方都绝对安全"。当前设计上自定义身份在写入 native schema 前会被规范化为合法值、自定义状态保存在私有域，但**未经系统性实机回刷验证**：

`NOT FULLY PROVEN`

回退前建议（非强制）：在相机 UI 中把当前 Image Control 切回原厂身份并保存。

## RAM / 资源说明

RAW workflow 存在约 **0x800-byte transient heap allocation**（RAW 参数对象为运行时动态分配、销毁释放）。**heap peak not measured；stack peak not measured；fragmentation not measured；RAM headroom not proven。** 不要表述为"RAM delta = 0 所以安全"。

## Related Projects（相关项目）

本项目不是社区中孤立的成果；相关项目各有明确、独立的定位。**我们不声称首创（not first / not only）**，也不把任何项目包装成竞争关系：

- **Tiy 的 [gr-custom-tool](https://github.com/DoYitNow/gr-custom-tool)**（GitHub: DoYitNow）：面向 **GR IV** 的本地固件编辑器 / 研究工具。公开能力涉及固件容器处理、版本策略、回退（rollback）策略与工作流、裁切比例、关机画面、以及 XMP 导入、本地模拟 / 软件域拟合与校色、可选 Windows Lightroom Classic 目标链路及滤镜资源写入。当前公开 README 表示真实 Lightroom 渲染与设备实测尚未完成；GPL-2.0-only。**本项目不是它的 fork。**
- **LiorMoment 的 [Darkslide GR](https://github.com/LiorMoment/darkslide-gr)**：面向 **GR III 2.10** 的本地**图标 / 名称编辑**工具（把预设换上自定义图标与名称；不修改色彩效果）；强调 exact 官方固件校验与"从原件重新生成 + 独立复核"；GPL-2.0-only。
- **idontknownihil 的 [gr3-film-mods](https://github.com/idontknownihil/gr3-film-mods)**：面向 **GR III 2.10** 的 image-pipeline 逆向工程工具（new Image Control entries、look matrix / tone curves / hue sectors、RAW Development、maker-note identity 等）。与本项目技术重叠相对最大；其容器 codec 依赖 [gr-custom-tool](https://github.com/DoYitNow/gr-custom-tool)（GPL-2.0 子模块）；其拟合数据按分量使用 CC BY-SA 4.0 / CC BY-NC-SA 4.0 等许可。
- **本项目（GR III Firmware Research Skill）**：不是 GUI editor、不是 preset collection、不是某个 film-look pack、不是 firmware download site。重点是把已经验证的 GR III 固件架构——six-slot architecture、native color Grain、per-file identity、RAW Development、Playback、UserData / U / BOX persistence——连同 evidence model、verified boundaries、fail-closed stop conditions 与研究方法论，整理成 **Coding Agent 能理解和继续工作的 Skill**。

> We focus on making the verified GR III firmware research architecture understandable and usable by coding agents, rather than shipping a GUI editor or prebuilt firmware.

> 我们更关注把已经验证的 GR III 固件架构、证据链和安全边界整理成 Coding Agent 能理解和继续工作的 Skill，而不是提供 GUI 编辑器或预编译固件。

## Acknowledgements（致谢）

本项目并不是在真空中完成的。GR 系列固件研究社区已经有多位开发者公开了非常有价值的研究成果。

**特别感谢 Tiy / DoYitNow 以及他的 [gr-custom-tool](https://github.com/DoYitNow/gr-custom-tool)。**该项目在 RICOH 固件容器处理、本地固件研究、版本识别、回退策略以及滤镜相关探索等方面给了本项目很多启发，也促使我们重新思考 firmware provenance、回退安全以及 Public Skill 的边界设计。

感谢 **LiorMoment 的 [Darkslide GR](https://github.com/LiorMoment/darkslide-gr)**：其在 GR III 2.10 上的本地编辑研究（图标 / 名称修改）、exact 官方固件校验与本地构建 / 验证工作流，为本项目提供了有价值的参考。

感谢 **idontknownihil 的 [gr3-film-mods](https://github.com/idontknownihil/gr3-film-mods)**：其 GR III image pipeline 逆向工程、film look 研究、新 Image Control 条目、RAW Development、maker-note identity 与 hue-sector 研究，为本项目提供了重要的领域参考。

**Inspiration ≠ Code Reuse**：本 v0.1 发布审查未发现打包的上述项目源代码、二进制或数据；各项目继续适用其各自许可证。此结论基于可获得的来源审查与发布扫描，不构成对所有内容著作权归属的普遍法律认定。未来如复用第三方材料，必须在合并前重新进行 provenance 与 license review，并遵守相应许可证。文件哈希仅证明文件身份，不证明原创性。

## Future Work（未来工作）

v0.1 主要是**研究 / Agent 知识 Skill**；端到端的通用 build automation 属于未来工作：

- direct-from-factory generic builder（本版不提供；需独立开发与审查）；
- recipe / config interface；
- automated validation 扩展；
- 更多固件版本与机型（需各自独立的证据）。

**不承诺任何日期**；以上均不是 v0.1 的发布条件。

## License

项目原创代码与文档采用标准 [MIT License](LICENSE)（不修改正文）。MIT **不覆盖 RICOH firmware**。详见 [NOTICE](NOTICE) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

---

# English Version

## What this is

This is a **RICOH GR III firmware research Skill for coding agents**.

It organizes historical research on the GR III 2.10 architecture: six additional Image Control slots, native color Grain, RAW Development, Playback, per-file identity and persistence. See the [evidence register](references/evidence-register.md) for exact versions, direct device reports, inherited evidence and limitations. v0.1 is a knowledge / evidence / research Skill, without a firmware production pipeline.

It is **not** a one-click flashing tool, and it **does not provide, host or distribute any official or modified RICOH firmware, nor a firmware modification service**.

## ⚠️ WARNING (read first)

- **Modifying camera firmware can permanently brick the camera.**
- It may void warranty and official support.
- Offline validation is not real-device safety.
- **This repository does not provide modified firmware and does not flash devices for you.**
- **Complete boot failure currently has NO VERIFIED RECOVERY PATH.**
- **If you cannot accept losing the device, do not experiment.**

## What this is NOT

This project explicitly does not and will not become:

- a firmware modification service;
- firmware hosting / mirror / download service;
- a service that generates firmware for third parties;
- remote firmware modification; receiving user firmware uploads; returning modified firmware files to users;
- a GUI / Web Editor / macOS App / Windows App;
- a one-click firmware tool / auto-flash / consumer wizard / installer;
- ready-to-flash firmware downloads / prebuilt modified firmware / firmware packs / preset packs / LUT packs;
- a "three-step flashing tutorial for beginners".

**Do not productize this Skill as "upload firmware → website modifies it → download firmware", and do not turn the repository into a firmware download site.**

## v0.1 executable scope and scan limits

This release retains documentation / evidence checks, release containment scanners and synthetic fixture generators only. **No candidate builder, repacker, firmware safety validator, SD staging or SD write entrypoints** are included; there is no firmware inspect / decode tool either. Agents must not reconnect these paths from private engineering or old packages. Synthetic fixtures write only to fresh system-temporary directories; they are not firmware or preset products.

Scanners report release-content checks and are **NOT A SAFETY VALIDATOR** for flashing. These helpers neither produce flashable files nor issue device-safety verdicts.

No findings were detected by the release scanner within the scanned release tree and archives. All files are classified, with bounded recursion through ZIP, TAR, GZ, XZ and BZ2. Missing paths, uninspected archives, unknown binaries and exceeded limits fail. Limits are 8 MiB per file, 64 MiB total processed data, 4096 items, four archive layers and a 200:1 decompression ratio. This cannot prove the absence of arbitrary private information, third-party content or custom encodings; it does not check external filesystems, user machines, future commits or unrelated private history. See the [scan policy](references/release-scan-policy.md).

## Clean public history requirement

**CLEAN_HISTORY_REQUIRED / CLEAN_PUBLIC_HISTORY_REQUIRED**: publish v0.1 in a new independent repository with a clean first public commit. Do not import private development `.git` or old commits, fork a private repository, or push old history. This RC has no public Git history; do not claim to have checked nonexistent history. The later publication stage must enforce this requirement.

## Intended audience

- Comfortable with coding agents and local development environments;
- Understands firmware versions, SHA-256, validation and recovery boundaries;
- Understands that modifying firmware carries real hardware risk.

> If any of the above does not describe you, do not experiment with this project.

## Using with a coding agent

1. Clone / download this Skill;
2. Hand it to **your own coding agent**;
3. Describe your research goal in natural language;
4. The agent reads `SKILL.md` + `references/`, and checks whether the goal lies inside the verified boundary;
5. The agent performs read-only research / analysis; this release does not generate candidates, modify firmware or write SD cards; goals outside historical evidence go to `RESEARCH_ONLY`;
6. **The agent must never describe unproven results as "safe to flash".**

## Supported devices & firmware

- **Standard RICOH GR III** only, with **official firmware 2.10** (identified by exact SHA-256).
- GR IIIx / GR IV / HDF and other versions are not supported.

**Version strings are not provenance.** The agent must not infer firmware identity from a file name (`fwdc239b.bin`), a camera-UI "2.10" display, or a user statement; identity requires **exact SHA-256 + product/model identity + known official provenance**. Unknown firmware:

`UNKNOWN_FIRMWARE_LINEAGE` / `RESEARCH_ONLY` — **do not continue patching**.

## Verified boundary

Historically reported architecture scope (this exact baseline only; see the register for levels, not current helper capabilities):

- firmware container and dual integrity checksums (not cryptographic signatures);
- six additional Image Control slots: public 30..35 / processing 26..31 / DNG `0x4f` 0x010C..0x0111;
- RAW selector 14..19 (13 reserved);
- Shooting parameter persistence (RAM banks, private records, Grain keys);
- UserData / U / BOX handling (custom identities normalized before any native-schema write);
- native color Grain (including per-file encoding and display chain);
- JPEG / DNG per-file identity;
- RAW Development integration (slots, parameters, Grain, As Shot default restoration);
- Playback identity / DISP parameters / per-file Grain (property37 / property140);
- the official restore path while the camera remains bootable.

Modifications beyond this scope (e.g. slot 7+, other firmware versions, other models, unrelated subsystems) default to **`RESEARCH_ONLY`**: read-only research only; no flashable conclusions; no formula extrapolation.

**Device validation scope**: Core feature paths have version-linked device validation and extensive static/offline regression coverage. Not every possible feature combination has been exhaustively tested on-device. The direct report for `93588df2…` covers the color Grain correction; retained paths from `a2fcd40b…` are **INHERITED BY STRUCTURAL EQUIVALENCE**, not a new exhaustive device acceptance. The register explains source records and the absence of an independent camera retest in this review.

## Firmware distribution boundary

This repository **provides only**: independent research notes, firmware architecture knowledge (addresses / mappings / semantics), verified boundaries, evidence methodology, fail-closed guardrails and agent instructions, and documentation, containment and synthetic-fixture helpers in which this review found no proprietary firmware data.

It **never provides, hosts, mirrors, packages or distributes**: original RICOH firmware; modified RICOH firmware; ready-to-flash firmware; generated candidate firmware; decoded firmware images; extracted RTOS images; firmware resource dumps (incl. ICONBIN dumps); firmware backup images; recovery firmware packages; private firmware copies; third-party custom firmware.

**No firmware acquisition service**: this project does not download, scrape or mirror RICOH firmware; it ships no firmware packages and offers no third-party download sources.

> This repository does not provide RICOH firmware. Users who choose to perform local research must obtain the supported firmware themselves directly from official RICOH IMAGING channels.

**No firmware modification service**: this repository does not accept user firmware for modification; does not remotely generate customized firmware; does not promise ready-to-flash files; does not flash devices on users' behalf.

**Local-only research model**: users who choose to experiment must do so locally, using firmware they obtained themselves and tools running under their own control.

## Unofficial / not affiliated

This is an **independent community research project. Not affiliated with or endorsed by RICOH IMAGING.** "RICOH", "GR" and related marks belong to their respective owners.

## Legal & responsibility (neutral wording)

> This repository is provided for independent technical research and education. Users are responsible for complying with applicable law, license terms and agreements in their jurisdiction.

This project makes **no legal guarantees**: it does not claim legality everywhere, does not claim any EULA is unenforceable, does not claim reverse engineering is legal in all jurisdictions, and does not claim that a disclaimer eliminates liability. This README is not legal advice.

License scope: the MIT License of this repository covers **only original project code and documentation** and **does not cover RICOH firmware**; user-supplied firmware and preset data remain subject to their own rights and terms.

The agreement on RICOH’s official GR III download page restricts modification and reverse engineering (item 4), and third-party transfer and sublicensing (item 6). Read the [official RICOH firmware and software license page](https://www.ricoh-imaging.co.jp/english/support/digital/gr3_s.html).

Not distributing, accepting or remotely modifying firmware reduces some distribution/service exposure, but **does not eliminate agreement or legal risks of local modification or reverse engineering**. Lawful possession does not automatically grant modification, reverse-engineering or redistribution rights. Before using this research with RICOH firmware, review the applicable RICOH software license terms and applicable law in your jurisdiction. This project does not determine enforceability or statutory exceptions across jurisdictions.

## Recovery & state compatibility

**Bootable recovery**: historical reports describe successful official restoration while the camera still boots normally; the exact source-candidate SHA binding is incomplete, so this is not direct recovery acceptance of the final golden. The register marks that precise attribution UNKNOWN.

**Complete failure**: complete boot failure / interrupted flashing / flash corruption / bootloader failure currently:

`NO VERIFIED RECOVERY PATH`

**Persistent-state compatibility**: do not claim that rolling back to official firmware is absolutely safe under any custom state. By design, custom identities are normalized before any native-schema write and custom state lives in private domains, but there has been no systematic on-device rollback validation:

`NOT FULLY PROVEN`

Recommended (not mandatory) before rolling back: switch the active Image Control back to a factory identity in the camera UI and save.

## RAM / resource note

The RAW workflow incurs a **~0x800-byte transient heap allocation** (the RAW parameter object is allocated at runtime and released on destruction). **Heap peak not measured; stack peak not measured; fragmentation not measured; RAM headroom not proven.** Do not state "RAM delta = 0, therefore safe".

## Related Projects

This project is not an isolated effort; the related projects below have their own, distinct positioning. **We claim no primacy (not first / not only)** and frame no project as a competitor:

- **Tiy's [gr-custom-tool](https://github.com/DoYitNow/gr-custom-tool)** (GitHub: DoYitNow): a local firmware editor / research tool targeting **GR IV**. Public capabilities involve firmware container handling, version strategy, rollback strategy and workflow, crop ratios, shutdown images, XMP import, local simulation / software-domain fitting and calibration, an optional Windows Lightroom Classic target path, and filter-resource writes. Its current README says real Lightroom rendering and device measurement remain unverified; GPL-2.0-only. **This project is not its fork.**
- **LiorMoment's [Darkslide GR](https://github.com/LiorMoment/darkslide-gr)**: a local **icon / name editing** tool for **GR III 2.10** (custom preset icons and names; it does not modify color effects); emphasizes exact-firmware validation and "regenerate from the original + independent re-verification"; GPL-2.0-only.
- **idontknownihil's [gr3-film-mods](https://github.com/idontknownihil/gr3-film-mods)**: GR III 2.10 image-pipeline reverse-engineering tools (new Image Control entries, look matrices / tone curves / hue sectors, RAW Development, maker-note identity). Technically the closest overlap with this project; its container codec depends on [gr-custom-tool](https://github.com/DoYitNow/gr-custom-tool) (GPL-2.0 submodule); its fit data is licensed per part (CC BY-SA 4.0 / CC BY-NC-SA 4.0, etc.).
- **This project (GR III Firmware Research Skill)**: not a GUI editor, not a preset collection, not a specific film-look pack, not a firmware download site. It focuses on making the verified GR III firmware architecture — six-slot architecture, native color Grain, per-file identity, RAW Development, Playback, UserData / U / BOX persistence — together with the evidence model, verified boundaries, fail-closed stop conditions and research methodology, understandable and usable by **coding agents**.

> We focus on making the verified GR III firmware research architecture understandable and usable by coding agents, rather than shipping a GUI editor or prebuilt firmware.

## Acknowledgements

This project was not built in a vacuum. Several developers in the GR firmware research community have published highly valuable work.

**Special thanks to Tiy / DoYitNow and his [gr-custom-tool](https://github.com/DoYitNow/gr-custom-tool).** It inspired this project in RICOH firmware container handling, local firmware research, version identification, rollback strategy and filter-related exploration, and it prompted us to rethink firmware provenance, rollback safety, and the boundary design of this Public Skill.

Thanks to **LiorMoment's [Darkslide GR](https://github.com/LiorMoment/darkslide-gr)** for its local editing research on GR III 2.10 (icon / name modification), exact-firmware validation and its local build / verification workflow.

Thanks to **idontknownihil's [gr3-film-mods](https://github.com/idontknownihil/gr3-film-mods)** for its GR III image-pipeline reverse engineering, film look research, new Image Control entries, RAW Development, maker-note identity and hue-sector research.

**Inspiration ≠ Code Reuse**: the v0.1 release review found no bundled source code, binaries or data copied from the projects above. Those projects remain subject to their own licenses. This conclusion uses available provenance review and release scans; it is not a universal legal determination of authorship. Future reuse requires provenance and license review before inclusion and compliance with the applicable license. File hashes establish file identity, not originality.

## Future Work

v0.1 is primarily a **research / agent knowledge skill**; end-to-end generic build automation is future work:

- direct-from-factory generic builder (not included; requires separate development and review);
- recipe / config interface;
- extended automated validation;
- more firmware versions and models (each requiring its own independent evidence).

**No dates are promised**; none of the above is a release condition for v0.1.

## License

Original project code and documentation are released under the standard [MIT License](LICENSE) (unmodified text). MIT **does not cover RICOH firmware**. See [NOTICE](NOTICE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
