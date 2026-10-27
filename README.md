[English](README.md) | [Қазақша](README.kk.md) | [中文](README.zh.md)

# Kazakh-QWERTZ

A macOS keyboard layout for typing **Kazakh (Cyrillic)** on a QWERTY physical keyboard. All **42 letters** of the modern Kazakh Cyrillic alphabet, including the 33 Russian letters, are available in lowercase and uppercase.

## Layout reference

Physical QWERTY key → letter. There are **32 letters on the base layer** and **10 additional letters on Option**. Punctuation key labels refer to US QWERTY positions; JIS keycap legends can differ.

```
Top row:    Q=ғ  W=у  E=е  R=р  T=т  Y=з  U=ұ  I=і  O=о  P=п  [=ү  ]=я
Home row:   A=а  S=с  D=д  F=ы  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
Bottom row: Z=и  X=ш  C=ң  V=в  B=б  N=н  M=м
Backtick:  `=й
```

- **Shift** uppercases letters, including `C=ң` → `Shift+C=Ң`.
- **Caps Lock** uppercases Cyrillic letters and leaves digits and punctuation unshifted. **Shift+Caps Lock** keeps letters uppercase; punctuation follows Shift.
- **Option** (⌥) provides the additional letters below. **Option+Shift** uppercases them. Letter keys without a separate Option assignment retain their base letters.
- **Caps Lock+Option** uppercases Option letters and leaves Option punctuation unchanged. **Shift+Caps Lock+Option** behaves like Shift+Option.
- **Command** shortcuts use physical Latin QWERTY keys, including combinations with Shift and Option. Select a separate **ABC/English input source** to type English; Caps Lock no longer selects Latin text.

### Additional letters

| Physical key | Option | Option+Shift |
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

### Numbers and punctuation

Digits remain available without modifiers. Shift uses the usual number-row symbols, including ASCII `^` on Shift+6. The slash key gives `/`, or `?` with Shift. Comma and period remain `,` and `.`; Shift+comma gives `"`, and Shift+period gives `:`.

Option restores the punctuation on keys occupied by letters:

| Physical key | Option | Option+Shift |
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

Other Option+digit combinations retain their digits, even with Shift. These text layers have **no dead keys**: every mapped character is entered immediately.

On JIS keyboards, the extra yen key also gives `й` (`Й` with Shift or Caps Lock); Option gives `\` and Option+Shift gives `|`. The extra underscore key gives `_` with or without Shift or Caps Lock; Option gives a backtick and Option+Shift gives `~`. The main letter positions follow the chart above.

## Install

```sh
git clone https://github.com/asqatqazet/kazakh-qertz.git
cd kazakh-qertz
./install.sh
```

Then:

1. **Log out and back in** (or restart your Mac) so macOS picks up the new bundle.
2. Open **System Settings → Keyboard → Input Sources → Edit → +**.
3. Pick **Kazakh** in the left list, then **Kazakh-QWERTZ** on the right, and click **Add**.
4. Switch to it from the menu bar input-source picker (or with `⌃Space` / `⌃⌥Space` if configured).

## Uninstall

```sh
./uninstall.sh
```

Then remove it from **System Settings → Keyboard → Input Sources** if it still appears.

## Install from DMG (no terminal)

1. Download `Kazakh-QWERTZ-<version>.dmg` from the [Releases page](https://github.com/asqatqazet/kazakh-qertz/releases).
2. Double-click the DMG.
3. Double-click `Install.command`. macOS may ask you to allow it the first time — see *System Settings → Privacy & Security* if it's blocked.
4. Log out and back in, then add the layout in *System Settings → Keyboard → Input Sources*.

## Manual install (without git)

Download the latest release zip from the [Releases page](https://github.com/asqatqazet/kazakh-qertz/releases), unzip, and copy `Kazakh-QWERTZ.bundle` into `~/Library/Keyboard Layouts/`.

To upgrade, update your checkout or download the new release and run `./install.sh` (or `Install.command`) again. Log out and back in if macOS still uses the previous layout.

## Verify the layout source

Run the tests:

```sh
python3 tests/test_coverage.py
```

The tests require all 42 letters in both cases, resolve inherited mappings for every hardware map, and check modifier behavior, punctuation, physical shortcut mappings, and duplicate key codes. They verify the layout source; they do **not** install it or confirm how an application handles the input source.

### Check the installed layout manually

After installing or upgrading, select Kazakh-QWERTZ in a text editor:

1. Type `Қазақстан қазақ ыстық ғылым білім жаңбыр әңгіме өрік үшін ұлт үй әй`. Check the new `F=ы`, unchanged backtick `й`, and `]=я`.
2. Type `ф һ ц щ э ё ю ч ь ъ` using Option, then `Ф Һ Ц Щ Э Ё Ю Ч Ь Ъ` using Option+Shift. Check `ң` and `Ң` with C and Shift+C, and `я` and `Я` with the right bracket key.
3. Turn on Caps Lock. Confirm that letters are uppercase while digits and punctuation stay unshifted. Check Shift+Caps Lock, Caps Lock+Option, and Shift+Caps Lock+Option against the rules above.
4. Try `/ ? " :`, the Option punctuation table, and then a normal letter after each punctuation key; no accent or quote should wait for a second key.
5. Check familiar physical shortcuts such as Command+A, Command+C, Command+V, Command+Z, and Command+Shift+Z where the application supports them. Check any Command+Option shortcuts you use, and switch to ABC/English to test English typing.

Repeat these checks on each keyboard type you use. Application shortcuts and macOS settings can affect the result; this checklist is for manual verification, not a claim that the native UI has been tested.

## Credits

Layout authored with [Ukelele](https://software.sil.org/ukelele/) by SIL International. Released under the [MIT License](LICENSE).
