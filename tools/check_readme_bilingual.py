#!/usr/bin/env python3
"""README bilingual validation for the GR III public skill (v0.1).

Gate rule: the README must contain BOTH a complete Chinese section and a complete
English section, and BOTH must carry the key safety / legal / boundary / usage
concepts with equivalent strength. If any check fails, the public gate must FAIL.

Usage: python3 check_readme_bilingual.py path/to/README.md
Exit code: 0 = all checks pass; 1 = gate fail (details on stdout, JSON).
"""
import json, re, sys
from pathlib import Path

ZH_MARK = "# 简体中文版"
EN_MARK = "# English Version"

CHECKS = [
    ("product_definition", "research skill, not a service/flasher",
     [r"固件研究 Skill", r"不是一键刷机工具"],
     [r"firmware research Skill for coding agents|firmware research Skill",
      r"not.{0,40}one-click flashing tool"]),
    ("firmware_risk", "real risk of firmware modification / bricking",
     [r"永久变砖"],
     [r"permanently brick"]),
    ("no_ready_to_flash", "does not provide modified/ready-to-flash firmware",
     [r"本项目不提供修改固件"],
     [r"does not provide modified firmware"]),
    ("no_verified_recovery", "NO VERIFIED RECOVERY PATH statement",
     [r"NO VERIFIED RECOVERY PATH"], [r"NO VERIFIED RECOVERY PATH"]),
    ("supported_boundary", "supported model/firmware boundary",
     [r"标准 RICOH GR III|官方 firmware 2\.10"],
     [r"Standard RICOH GR III|official firmware 2\.10"]),
    ("research_only", "unsupported modifications go to RESEARCH_ONLY",
     [r"RESEARCH_ONLY"], [r"RESEARCH_ONLY"]),
    ("agent_usage", "agent-oriented usage model",
     [r"Coding Agent"], [r"coding agent"]),
    ("version_not_provenance", "version strings are not provenance / unknown lineage STOP",
     [r"版本字符串不是 provenance", r"UNKNOWN_FIRMWARE_LINEAGE"],
     [r"[Vv]ersion strings are not provenance", r"UNKNOWN_FIRMWARE_LINEAGE"]),
    ("no_acquisition_service", "no firmware acquisition / download service",
     [r"不代用户取得 firmware|不代为下载"],
     [r"[Nn]o firmware acquisition service"]),
    ("no_modification_service", "no firmware modification service; local-only model",
     [r"不提供 firmware 修改服务", r"自己的电脑上，使用自己合法取得的官方固件"],
     [r"[Nn]o firmware modification service", r"[Ll]ocal[ -]only research model"]),
    ("distribution_boundary", "never hosts/mirrors/redistributes firmware",
     [r"不提供、不托管、不分发"],
     [r"[Nn]ever provides, hosts, mirrors"]),
    ("legal_neutral", "neutral legal wording; user responsibility",
     [r"用户需自行遵守其司法辖区的适用法律", r"不构成法律意见"],
     [r"Users are responsible for complying with applicable law",
      r"[Nn]ot legal advice"]),
    ("user_responsibility", "user-supplied firmware/preset licensing responsibility",
     [r"用户自备的固件与 preset 数据均受其自身权利与条款约束"],
     [r"user-supplied firmware and preset data remain subject to their own rights"]),
    ("unofficial", "unofficial / not affiliated statement",
     [r"未获其背书"],
     [r"Not affiliated with or endorsed by RICOH"]),
    ("mit_scope", "MIT does not cover RICOH firmware",
     [r"不覆盖 RICOH firmware"], [r"does not cover RICOH firmware"]),
    ("device_scope", "device validation is not exhaustive",
     [r"并非每一种功能组合都在相机上做过穷举测试"],
     [r"[Nn]ot every possible feature combination has been exhaustively tested"]),
    ("raw_heap", "RAW ~0x800 transient heap; headroom not proven",
     [r"0x800-byte transient heap allocation", r"RAM headroom not proven"],
     [r"0x800-byte transient heap allocation", r"RAM headroom not proven"]),
    ("recovery_vs_state", "bootable vs complete-failure vs state compatibility",
     [r"[Bb]ootable recovery", r"NOT FULLY PROVEN"],
     [r"[Bb]ootable recovery", r"NOT FULLY PROVEN"]),
    ("related_projects", "related projects section, no primacy claims",
     [r"相关项目", r"不声称首创"], [r"Related Projects", r"claim no primacy"]),
    ("tiy_credit", "Tiy / DoYitNow prominently acknowledged",
     [r"Tiy / DoYitNow"], [r"Tiy / DoYitNow"]),
    ("lior_credit", "LiorMoment acknowledged",
     [r"LiorMoment"], [r"LiorMoment"]),
    ("nihil_credit", "idontknownihil acknowledged",
     [r"idontknownihil"], [r"idontknownihil"]),
    ("inspiration_not_copy", "inspiration != code reuse; no GPL code copied",
     [r"Inspiration ≠ Code Reuse|不复制"],
     [r"Inspiration ≠ Code Reuse|does not copy"]),
    ("future_work", "future work section, not a release condition",
     [r"未来工作"], [r"Future Work"]),
    ("executable_scope", "knowledge release without production/write paths",
     [r"没有 candidate builder", r"SD write", r"不是刷写安全验证器"],
     [r"No candidate builder", r"SD write", r"NOT A SAFETY VALIDATOR"]),
    ("official_agreement", "specific RICOH terms and official source",
     [r"第 4 项", r"第 6 项", r"https://www\.ricoh-imaging\.co\.jp/english/support/digital/gr3_s\.html"],
     [r"item 4", r"item 6", r"https://www\.ricoh-imaging\.co\.jp/english/support/digital/gr3_s\.html"]),
    ("local_risk", "local-only does not eliminate agreement risk",
     [r"并不意味着", r"合法取得副本不自动"],
     [r"does not eliminate agreement or legal risks", r"Lawful possession does not automatically"]),
    ("evidence_register", "registered historical evidence and inheritance",
     [r"references/evidence-register\.md", r"INHERITED BY STRUCTURAL EQUIVALENCE", r"93588df2", r"a2fcd40b"],
     [r"references/evidence-register\.md", r"INHERITED BY STRUCTURAL EQUIVALENCE", r"93588df2", r"a2fcd40b"]),
    ("scan_scope", "bounded release scans, not absence proof",
     [r"发布扫描器在本次实际扫描的 release tree 与归档内容中未发现命中项", r"不能证明"],
     [r"No findings were detected by the release scanner within the scanned release tree and archives", r"cannot prove"]),
    ("clean_history", "new independent repository and clean first public commit",
     [r"CLEAN_PUBLIC_HISTORY_REQUIRED", r"新建独立仓库", r"第一次公开提交"],
     [r"CLEAN_PUBLIC_HISTORY_REQUIRED", r"new independent repository", r"clean first public commit"]),
    ("linked_credits", "three clickable community repositories",
     [r"https://github\.com/DoYitNow/gr-custom-tool", r"https://github\.com/LiorMoment/darkslide-gr", r"https://github\.com/idontknownihil/gr3-film-mods"],
     [r"https://github\.com/DoYitNow/gr-custom-tool", r"https://github\.com/LiorMoment/darkslide-gr", r"https://github\.com/idontknownihil/gr3-film-mods"]),
    ("tiy_current_scope", "XMP/software fitting with measured limits",
     [r"XMP 导入", r"软件域拟合", r"Lightroom"],
     [r"XMP import", r"software-domain fitting", r"Lightroom"]),
    ("authorship_limit", "hashes establish identity, not authorship",
     [r"文件哈希仅证明文件身份，不证明原创性", r"合并前"],
     [r"File hashes establish file identity, not originality", r"before inclusion"]),

]

def main():
    if len(sys.argv) < 2:
        print("usage: check_readme_bilingual.py README.md"); sys.exit(2)
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    results = []
    ok = True
    has_zh, has_en = ZH_MARK in text, EN_MARK in text
    results.append(dict(id="sections_present", pass_=bool(has_zh and has_en),
                        detail=f"zh_mark={has_zh} en_mark={has_en}"))
    ok &= has_zh and has_en and text.index(ZH_MARK) < text.index(EN_MARK) and text.count(ZH_MARK) == text.count(EN_MARK) == 1
    if not (has_zh and has_en):
        emit(results, ok); return
    zh = text.split(ZH_MARK, 1)[1].split(EN_MARK, 1)[0]
    en = text.split(EN_MARK, 1)[1]
    for cid, desc, zh_pats, en_pats in CHECKS:
        zh_ok = all(re.search(p, zh) for p in zh_pats)
        en_ok = all(re.search(p, en) for p in en_pats)
        results.append(dict(id=cid, pass_=bool(zh_ok and en_ok), detail=f"zh={zh_ok} en={en_ok}", desc=desc))
        ok &= zh_ok and en_ok
    banned = ["their licenses (including GPL-2.0) do not bind", "All helpers are deterministic, documented and fail-closed"]
    no_overclaim = not any(t in text for t in banned)
    results.append(dict(id="no_old_overclaim", pass_=no_overclaim))
    ok &= no_overclaim
    emit(results, ok)

def emit(results, ok):
    out = dict(readme_pass=bool(ok), checks=results,
               gate="README_BILINGUAL_PASS" if ok else "README_BILINGUAL_FAIL")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
