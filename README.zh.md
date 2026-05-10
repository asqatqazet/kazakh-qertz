[English](README.md) | [Қазақша](README.kk.md) | [中文](README.zh.md)

# Kazakh-QWERTZ

一款 macOS 键盘布局，让你在 QWERTY 物理键盘上输入**哈萨克语（西里尔字母）**。常用字母按 QWERTZ 风格摆放。

## 键位参考

默认状态（无修饰键）—— QWERTY 物理键 → 哈萨克字母：

```
上排：  Q=ғ  W=у  E=е  R=р  T=т  Y=з  U=ұ  I=і  O=о  P=п  [=ү  ]=ч
中排：  A=а  S=с  D=д  F=ф  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
下排：  Z=и  X=ш  C=ң  V=в  B=б  N=н  M=м
```

按住 **Shift** 输入大写。按住 **Option**（⌥）输入特殊字符与拉丁标点。打开 **Caps Lock** 切换到拉丁字母回退层（在哈萨克语中混排英文时使用）。

## 安装

```sh
git clone https://github.com/asqatqazet/kazakh-qertz.git
cd kazakh-qertz
./install.sh
```

接着：
1. 打开 **系统设置 → 键盘 → 输入法 → 编辑 → +**。
2. 在左侧选择 **Kazakh**，右侧选择 **Kazakh-QWERTZ**，点击 **添加**。
3. 通过菜单栏的输入法切换器（或 `⌃Space`）切换到该布局。

安装脚本会重启 `cfprefsd`，因此布局通常**无需注销**即可立即出现。如果没出现，注销并重新登录一次即可。

## 卸载

```sh
./uninstall.sh
```

如有需要，再到 **系统设置 → 键盘 → 输入法** 中手动移除。

## 通过 DMG 安装（无需终端）

1. 从 [Releases 页面](https://github.com/asqatqazet/kazakh-qertz/releases) 下载 `Kazakh-QWERTZ-<版本>.dmg`。
2. 双击 DMG。
3. 双击 `Install.command`。首次运行时 macOS 可能会要求授权 —— 如被拦截，请到 *系统设置 → 隐私与安全性* 中允许。
4. 在 *系统设置 → 键盘 → 输入法* 中添加该布局。多数情况下无需注销 —— 详见上面的说明。

## 不使用 Git 安装

从 [Releases 页面](https://github.com/asqatqazet/kazakh-qertz/releases) 下载最新的 zip 包，解压后将 `Kazakh-QWERTZ.bundle` 复制到 `~/Library/Keyboard Layouts/`。

## 已知缺失字母

当前布局**未**映射现代哈萨克西里尔字母表中的以下字母：

- 小写：`һ ц щ ъ ы ь э ю`
- 大写：`Ң Һ Ц Щ Ъ Ы Ь Э Ю Я`

大多数是仅用于外来词的俄语借入字母，但 `Ң`（即 `ң` 的大写）是核心哈萨克字母，缺失它确属缺陷。欢迎提交修复：用 [Ukelele](https://software.sil.org/ukelele/) 编辑 `Contents/Resources/Kazakh-QWERTZ.keylayout`，并从 `tests/test_coverage.py` 的 `KNOWN_MISSING_*` 集合中删除对应字母。

## 验证安装

运行覆盖率测试：

```sh
python3 tests/test_coverage.py
```

它会检查每个应被映射的字母是否可达，以及是否存在重复键位绑定。

## 致谢

布局由 SIL International 的 [Ukelele](https://software.sil.org/ukelele/) 编辑工具创建。以 [MIT 许可证](LICENSE) 发布。
