[English](README.md) | [Қазақша](README.kk.md) | [中文](README.zh.md)

# Kazakh-QWERTY / Kazakh-QWERTZ

两款在 QWERTY 物理键盘上输入**哈萨克语（西里尔字母）**的 macOS 键盘布局。两款都支持现代哈萨克西里尔字母表的全部 **42 个字母**及其大小写，包括俄语的 33 个字母。

## 选择布局

**Kazakh-QWERTY** 是 **v1.2.0** 新增的布局。**Kazakh-QWERTZ** 保留原有键位。两款可同时安装，作为独立输入源选择。

| 物理键 | Kazakh-QWERTY | Kazakh-QWERTZ |
| --- | --- | --- |
| Y | й | з |
| Z | з | и |
| V | и | в |
| 反引号 | в | й |
| Option+I | и | і |

两款均保留 **I=і**、**F=ы** 以及相同的十个 Option 额外字母。QWERTY 中，**Option+I** 也可输入 **и**；Option+Shift+I 或 Caps Lock+Option+I 输入 **И**。仍可直接按 V 输入 и。

## 键位参考

QWERTY 物理键 → 字母。每款布局的**基础层均有 32 个字母**，其余 **10 个字母通过 Option 输入**。标点键名称按美式 QWERTY 位置标注；JIS 键盘的键帽标识可能不同。

### Kazakh-QWERTY

```
上排： Q=ғ  W=у  E=е  R=р  T=т  Y=й  U=ұ  I=і  O=о  P=п  [=ү  ]=я
中排： A=а  S=с  D=д  F=ы  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
下排： Z=з  X=ш  C=ң  V=и  B=б  N=н  M=м
反引号： `=в
```

### Kazakh-QWERTZ

```
上排： Q=ғ  W=у  E=е  R=р  T=т  Y=з  U=ұ  I=і  O=о  P=п  [=ү  ]=я
中排： A=а  S=с  D=д  F=ы  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
下排： Z=и  X=ш  C=ң  V=в  B=б  N=н  M=м
反引号： `=й
```

### 两款共用的修饰键规则

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

JIS 键盘额外的日元键与反引号键输入相同的字母：**QWERTY 为 в/В，QWERTZ 为 й/Й**。两款均用 Option 输入 `\`，Option+Shift 输入 `|`。额外的下划线键输入 `_`，Shift 和 Caps Lock 不改变它；Option 输入反引号，Option+Shift 输入 `~`。主要字母位置与上表一致。

## 从源码安装

```sh
git clone https://github.com/asqatqazet/kazakh-qertz.git
cd kazakh-qertz
./install.sh qwerty
```

安装原有布局用 `./install.sh qwertz`，同时安装两款用 `./install.sh both`。不加参数运行 `./install.sh` 仍默认安装 QWERTZ。

接着：

1. **注销并重新登录**（或重启 Mac），让 macOS 加载新布局。
2. 打开 **系统设置 → 键盘 → 输入法 → 编辑 → +**。
3. 在 **Kazakh** 下选择 **Kazakh-QWERTY** 或 **Kazakh-QWERTZ**，点击 **添加**。安装两款后，请分别添加。
4. 通过菜单栏的输入源菜单选择所需布局，也可使用已配置的 `⌃Space` / `⌃⌥Space`。

安装或升级其中一款不会移除另一款。尝试 QWERTY 时可以保留现有的 QWERTZ 输入源。

## 通过 DMG 安装（无需终端）

1. 从 [Releases 页面](https://github.com/asqatqazet/kazakh-qertz/releases) 选择 `Kazakh-QWERTY-v1.2.0.dmg` 或 `Kazakh-QWERTZ-v1.2.0.dmg`。
2. 双击 DMG，再双击 **Install.command**。每个安装程序只安装其名称对应的布局。首次运行时 macOS 可能要求授权；如被拦截，请到 *系统设置 → 隐私与安全性* 中允许。
3. 注销并重新登录（或重启），再按上面的步骤添加 **Kazakh** 下对应的输入源。

要同时安装两款，请分别运行各自的安装程序。`SHA256SUMS` 包含两个 DMG 和两个 ZIP 的校验和。GitHub 的 **Source code** 下载项是仓库快照，不是打包好的安装程序。

## 从 ZIP 手动安装

选择发布附件中的 `Kazakh-QWERTY-v1.2.0.zip` 或 `Kazakh-QWERTZ-v1.2.0.zip`。解压后，将其中的 `Kazakh-QWERTY.bundle` 或 `Kazakh-QWERTZ.bundle` 复制到 `~/Library/Keyboard Layouts/`。两个包可同时保留在该目录。注销并重新登录（或重启），然后添加需要的输入源。

升级时，下载对应布局的新版本并再次运行其安装程序；也可更新本地仓库后运行 `./install.sh qwerty`、`./install.sh qwertz` 或 `./install.sh both`。如果 macOS 仍使用旧版本，请注销并重新登录。

## 卸载

```sh
./uninstall.sh qwerty
```

卸载 QWERTZ 用 `./uninstall.sh qwertz`，两款一起卸载用 `./uninstall.sh both`。在仓库目录中，不加参数默认选择 QWERTZ；下载的 DMG 或 ZIP 包中的 `install.sh` 和 `uninstall.sh` 则默认选择该包对应的布局。移除其中一款不会移除另一款。如果对应输入源仍显示在**系统设置 → 键盘 → 输入法**中，请手动移除。

## 验证布局源文件

运行测试：

```sh
python3 tests/test_coverage.py
python3 tests/test_install.py
```

在 macOS 上，`test_install.py` 检查隔离环境中的安装和打包 ZIP，不会写入你实际使用的 Keyboard Layouts 文件夹。

测试覆盖**两款布局**：全部 42 个字母的大小写、每种硬件映射的继承关系、修饰键行为、标点、物理快捷键映射、重复键码，以及 QWERTY 的 Option+I 替代键位。测试仅验证布局源文件，**不会安装布局，也不能确认应用程序中的实际输入行为**。

### 手动检查已安装的布局

安装或升级后，在文本编辑器中分别选择已安装的布局：

1. 输入 `Қазақстан қазақ ыстық ғылым білім жаңбыр әңгіме өрік үшін ұлт үй әй киім биік жиі сиыр вагон`。按上面的比较表检查 Y、Z、V 和反引号键。QWERTY 中，检查 V 和 Option+I 都能输入 `и` 及对应大写；I 仍须输入 `і`。
2. 用 Option 输入 `ф һ ц щ э ё ю ч ь ъ`，再用 Option+Shift 输入 `Ф Һ Ц Щ Э Ё Ю Ч Ь Ъ`。检查 C 和 Shift+C 分别输入 `ң`、`Ң`，右方括号键能输入 `я`、`Я`。
3. 开启 Caps Lock，确认字母大写，数字和标点不变。按上面的规则检查 Shift+Caps Lock、Caps Lock+Option、Shift+Caps Lock+Option。
4. 尝试 `/ ? " :` 以及表中的 Option 标点。每次输入标点后再输入普通字母，确认重音和引号不会等待第二次按键。
5. 在支持相应功能的应用中检查 Command+A、Command+C、Command+V、Command+Z、Command+Shift+Z 等物理快捷键，以及自己常用的 Command+Option 快捷键。切换至 ABC/英文输入源，检查英文输入。

请在自己使用的每种键盘类型上重复检查。应用快捷键和 macOS 设置可能影响结果；此清单用于手动验证，并不表示已完成系统界面实测。

## 致谢

布局由 SIL International 的 [Ukelele](https://software.sil.org/ukelele/) 编辑工具创建。以 [MIT 许可证](LICENSE) 发布。
