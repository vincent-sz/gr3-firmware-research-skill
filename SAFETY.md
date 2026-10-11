# Safety / 安全边界

## 简体中文

v0.1 是 knowledge / evidence / research Skill。没有 candidate builder、repacker、固件安全 validator 或 SD 写入能力；发布检查只检查内容和文档，不能使刷写安全。

- 修改相机固件可能永久变砖，并影响保修和官方支持；不能接受损失设备时不要实验。
- 本仓库不托管、镜像、代下载、接收、远程修改、分发 firmware，也不替用户刷机。
- 仅有相机仍正常启动时官方回刷的历史报告；完整失败：**NO VERIFIED RECOVERY PATH**。
- 回退后的持久化状态兼容 **NOT FULLY PROVEN**；回退前切回原厂身份并保存只是建议，不能消除全部风险。
- RAW 对象约 0x800 bytes，为瞬时 heap allocation；heap / stack peak、fragmentation、RAM headroom 未证明。
- 设备测试非穷举；直接与继承证据见 [证据台账](references/evidence-register.md)。本次未在相机上重验历史结论。

RICOH 官方 GR III 下载协议限制修改、逆向工程（第 4 项）和第三方转交 / 转授许可（第 6 项）。见 [RICOH 官方页面](https://www.ricoh-imaging.co.jp/english/support/digital/gr3_s.html)。不分发、本地研究可减少部分分发 / 服务风险面，但不消除本地研究中的协议或法律风险；取得副本不自动取得修改 / 逆向 / 分发授权。使用前审查适用的 RICOH 条款及所在地区法律。本项目不提供法律保证或各地可执行性结论。

发布扫描器在本次实际扫描的 release tree 与归档内容中未发现命中项，不是不存在任意私密 / 第三方内容的证明。未知格式或超限输入必须失败；不检查外部文件系统、用户机器、未来提交或无关私有历史。见 [扫描策略](references/release-scan-policy.md)。

## English

v0.1 is a knowledge / evidence / research Skill. It contains no candidate builder,
repacker, firmware safety validator or SD-write capability. Release checks inspect
content and documentation; they cannot make flashing safe.

- Modifying firmware can permanently brick the camera and affect warranty/support.
  If you cannot accept losing the device, do not experiment.
- No hosting, mirroring, downloading for users, uploads, remote modification,
  firmware distribution or flashing for users.
- Historical official restore reports presume a normally bootable camera; complete
  failure has **NO VERIFIED RECOVERY PATH**.
- Persistent-state rollback compatibility is **NOT FULLY PROVEN**. Switching back to
  factory identity and saving is only a recommendation, not risk elimination.
- RAW uses an approximately 0x800-byte transient heap object; heap/stack peaks,
  fragmentation and RAM headroom are not proven.
- Device testing is not exhaustive. See the [evidence register](references/evidence-register.md)
  for direct/inherited scope. This review did not retest historical camera behavior.

RICOH's official GR III agreement restricts modification/reverse engineering (item 4)
and third-party transfer/sublicensing (item 6). See the [official source](https://www.ricoh-imaging.co.jp/english/support/digital/gr3_s.html).
No distribution and local research reduce some service/distribution exposure but do
not eliminate agreement/legal risks. Possession does not automatically grant
modification/reverse-engineering/distribution rights. Before using this research with
RICOH firmware, review the applicable RICOH software license terms and applicable law
in your jurisdiction. This project gives no legal guarantee or enforceability finding.

No findings were detected by the release scanner within the scanned release tree and
archives. This is not proof of absence of arbitrary private or third-party content.
Unknown formats and exceeded limits fail. External filesystems, user machines, future
commits and unrelated private history are outside scope. See the [scan policy](references/release-scan-policy.md).
