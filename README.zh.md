[English](README.md) | [Қазақша](README.kk.md) | [中文](README.zh.md)

# Kazakh-QWERTZ

一款在 QWERTY 物理键盘上输入**哈萨克语（西里尔字母）**的 macOS 键盘布局。支持现代哈萨克西里尔字母表的全部 **42 个字母**及其大小写，包括俄语的 33 个字母。

## 键位参考

QWERTY 物理键 → 字母。**基础层有 32 个字母**，其余 **10 个字母通过 Option 输入**。标点键名称按美式 QWERTY 位置标注；JIS 键盘的键帽标识可能不同。

```
上排：  Q=ғ  W=у  E=е  R=р  T=т  Y=з  U=ұ  I=і  O=о  P=п  [=ү  ]=я
中排：  A=а  S=с  D=д  F=ы  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
下排：  Z=и  X=ш  C=ң  V=в  B=б  N=н  M=м
反引号：`=й
```

- **Shift** 输入大写字母，例如 `C=ң`、`Shift+C=Ң`。
- **Caps Lock** 将西里尔字母变为大写，数字和标点保持未按 Shift 时的输出。**Shift+Caps Lock** 仍输入大写字母，标点则使用 Shift 层。
- **Option**（⌥）输入下表中的额外字母，**Option+Shift** 输入其大写形式。没有单独分配 Option 字母的字母键，仍输入基础层的字母。
- **Caps Lock+Option** 输入 Option 字母的大写形式，Option 标点不变。**Shift+Caps Lock+Option** 与 Shift+Option 相同。
- **Command** 快捷键使用物理 QWERTY 键的拉丁字母，包括与 Shift、Option 组合的快捷键。输入英文时，请切换到单独的 **ABC/英文输入源**；Caps Lock 不再切换到拉丁字母层。

### 额外字母

| 物理键 | Option | Option+Shift |
| --- | --- | --- |
| F | ф | Ф |
| H | һ | Һ |
| C | ц | Ц |
| X | щ | Щ |
| E | э | Э |
| O | ё | Ё |
| W | ю | Ю |
| J | ч | Ч |
| B | ь | Ь |
| V | ъ | Ъ |

### 数字与标点

数字无需修饰键即可输入。Shift 使用数字行的常规符号，包括 Shift+6 的 ASCII `^`。斜杠键输入 `/`，加 Shift 输入 `?`。逗号和句号键分别输入 `,` 和 `.`；Shift+逗号输入 `"`，Shift+句号输入 `:`。

对于被字母占用的标点键，Option 可输入原来的标点：

| 物理键 | Option | Option+Shift |
| --- | --- | --- |
| <code>&#96;</code> | <code>&#96;</code> | `~` |
| `[` | `[` | `{` |
| `]` | `]` | `}` |
| `;` | `;` | `:` |
| `'` | `'` | `"` |
| `\` | `\` | <code>&#124;</code> |
| `,` | `«` | `»` |
| `.` | `…` | `…` |
| `-` | `–` | `—` |
| `=` | `≠` | `±` |
| `3` | `№` | `№` |
| `4` | `₸` | `₸` |

其余 Option+数字组合即使加上 Shift 也仍输入数字。这些文本层**没有死键**：每个映射字符都会立即输入，不会等待下一次按键来组合重音。

JIS 键盘额外的日元键也输入 `й`（加 Shift 或 Caps Lock 输入 `Й`），Option 输入 `\`，Option+Shift 输入 `|`。额外的下划线键输入 `_`，Shift 和 Caps Lock 不改变它；Option 输入反引号，Option+Shift 输入 `~`。主要字母位置与上表一致。

## 安装

```sh
git clone https://github.com/asqatqazet/kazakh-qertz.git
cd kazakh-qertz
./install.sh
```

接着：

1. **注销并重新登录**（或重启 Mac）以让 macOS 识别新捆绑包。
2. 打开 **系统设置 → 键盘 → 输入法 → 编辑 → +**。
3. 在左侧选择 **Kazakh**，右侧选择 **Kazakh-QWERTZ**，点击 **添加**。
4. 通过菜单栏的输入法切换器（或 `⌃Space`）切换到该布局。

## 卸载

```sh
./uninstall.sh
```

如有需要，再到 **系统设置 → 键盘 → 输入法** 中手动移除。

## 通过 DMG 安装（无需终端）

1. 从 [Releases 页面](https://github.com/asqatqazet/kazakh-qertz/releases) 下载 `Kazakh-QWERTZ-<版本>.dmg`。
2. 双击 DMG。
3. 双击 `Install.command`。首次运行时 macOS 可能会要求授权 —— 如被拦截，请到 *系统设置 → 隐私与安全性* 中允许。
4. 注销并重新登录，然后在 *系统设置 → 键盘 → 输入法* 中添加该布局。

## 不使用 Git 安装

从 [Releases 页面](https://github.com/asqatqazet/kazakh-qertz/releases) 下载最新的 zip 包，解压后将 `Kazakh-QWERTZ.bundle` 复制到 `~/Library/Keyboard Layouts/`。

升级时，更新本地仓库或下载新版本，再次运行 `./install.sh`（或 `Install.command`）。如果 macOS 仍使用旧布局，请注销并重新登录。

## 验证布局源文件

运行测试：

```sh
python3 tests/test_coverage.py
```

测试要求全部 42 个字母的大小写都可用，解析每种硬件映射的继承关系，并检查修饰键行为、标点、物理快捷键映射及重复键码。测试仅验证布局源文件，**不会安装布局，也不能确认应用程序中的实际输入行为**。

### 手动检查已安装的布局

安装或升级后，在文本编辑器中选择 Kazakh-QWERTZ：

1. 输入 `Қазақстан қазақ ыстық ғылым білім жаңбыр әңгіме өрік үшін ұлт үй әй`。检查新的 `F=ы`、保持原位的反引号键 `й`，以及 `]=я`。
2. 用 Option 输入 `ф һ ц щ э ё ю ч ь ъ`，再用 Option+Shift 输入 `Ф Һ Ц Щ Э Ё Ю Ч Ь Ъ`。检查 C 和 Shift+C 分别输入 `ң`、`Ң`，右方括号键能输入 `я`、`Я`。
3. 开启 Caps Lock，确认字母大写，数字和标点不变。按上面的规则检查 Shift+Caps Lock、Caps Lock+Option、Shift+Caps Lock+Option。
4. 尝试 `/ ? " :` 以及表中的 Option 标点。每次输入标点后再输入普通字母，确认重音和引号不会等待第二次按键。
5. 在支持相应功能的应用中检查 Command+A、Command+C、Command+V、Command+Z、Command+Shift+Z 等物理快捷键，以及自己常用的 Command+Option 快捷键。切换至 ABC/英文输入源，检查英文输入。

请在自己使用的每种键盘类型上重复检查。应用快捷键和 macOS 设置可能影响结果；此清单用于手动验证，并不表示已完成系统界面实测。

## 致谢

布局由 SIL International 的 [Ukelele](https://software.sil.org/ukelele/) 编辑工具创建。以 [MIT 许可证](LICENSE) 发布。
