[English](README.md) | [Қазақша](README.kk.md) | [中文](README.zh.md)

# Kazakh-QWERTY / Kazakh-QWERTZ

Two macOS keyboard layouts for typing **Kazakh (Cyrillic)** on a QWERTY physical keyboard. Both provide all **42 letters** of the modern Kazakh Cyrillic alphabet, including the 33 Russian letters, in lowercase and uppercase.

## Choose a layout

**Kazakh-QWERTY** is the new variant in **v1.2.0**. **Kazakh-QWERTZ** keeps the existing layout unchanged. You can install both and select either as a separate input source.

| Physical key | Kazakh-QWERTY | Kazakh-QWERTZ |
| --- | --- | --- |
| Y | й | з |
| Z | з | и |
| V | и | в |
| Backtick | в | й |
| Option+I | и | і |

Both keep **I=і**, **F=ы**, and the same ten additional Option letters. In QWERTY, **Option+I** is another way to type **и**; Option+Shift+I or Caps Lock+Option+I gives **И**. The direct V key remains available for и.

## Layout reference

Physical QWERTY key → letter. Each variant has **32 letters on the base layer** and **10 additional letters on Option**. Punctuation key labels refer to US QWERTY positions; JIS keycap legends can differ.

### Kazakh-QWERTY

```
Top row:    Q=ғ  W=у  E=е  R=р  T=т  Y=й  U=ұ  I=і  O=о  P=п  [=ү  ]=я
Home row:   A=а  S=с  D=д  F=ы  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
Bottom row: Z=з  X=ш  C=ң  V=и  B=б  N=н  M=м
Backtick:   `=в
```

### Kazakh-QWERTZ

```
Top row:    Q=ғ  W=у  E=е  R=р  T=т  Y=з  U=ұ  I=і  O=о  P=п  [=ү  ]=я
Home row:   A=а  S=с  D=д  F=ы  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
Bottom row: Z=и  X=ш  C=ң  V=в  B=б  N=н  M=м
Backtick:   `=й
```

### Shared modifier behavior

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

On JIS keyboards, the extra yen key mirrors the backtick letter: **в/В in QWERTY**, **й/Й in QWERTZ**. Option gives `\` and Option+Shift gives `|` in both. The extra underscore key gives `_` with or without Shift or Caps Lock; Option gives a backtick and Option+Shift gives `~`. The main letter positions follow the charts above.

## Install from source

```sh
git clone https://github.com/asqatqazet/kazakh-qertz.git
cd kazakh-qertz
./install.sh qwerty
```

Use `./install.sh qwertz` for the original variant, or `./install.sh both` for both. Running `./install.sh` without an argument still installs QWERTZ.

Then:

1. **Log out and back in** (or restart your Mac) so macOS can load the new bundle.
2. Open **System Settings → Keyboard → Input Sources → Edit → +**.
3. Pick **Kazakh**, then **Kazakh-QWERTY** or **Kazakh-QWERTZ**, and click **Add**. Add each separately if you installed both.
4. Select the desired layout from the input-source menu (or use `⌃Space` / `⌃⌥Space` if configured).

Installing or upgrading one variant leaves the other installed. You can keep your existing QWERTZ input source while trying QWERTY.

## Install from DMG (no terminal)

1. Choose `Kazakh-QWERTY-v1.2.0.dmg` or `Kazakh-QWERTZ-v1.2.0.dmg` from the [Releases page](https://github.com/asqatqazet/kazakh-qertz/releases).
2. Double-click the DMG, then **Install.command**. Each installer installs its named variant only. macOS may ask you to allow it the first time — see *System Settings → Privacy & Security* if it is blocked.
3. Log out and back in (or restart), then add the matching input source under **Kazakh** as described above.

To install both, run each variant's installer. `SHA256SUMS` contains checksums for the two DMG and two ZIP assets. GitHub's **Source code** downloads are repository snapshots, not the prepared installers.

## Manual install from ZIP

Choose `Kazakh-QWERTY-v1.2.0.zip` or `Kazakh-QWERTZ-v1.2.0.zip` from the release assets. Extract it and copy its `Kazakh-QWERTY.bundle` or `Kazakh-QWERTZ.bundle` into `~/Library/Keyboard Layouts/`. Both bundles can be kept in that folder. Log out and back in (or restart), then add the desired input source.

To upgrade, download the matching release asset and run its installer again, or update your checkout and run `./install.sh qwerty`, `./install.sh qwertz`, or `./install.sh both`. Log out and back in if macOS still uses the previous version.

## Uninstall

```sh
./uninstall.sh qwerty
```

Use `./uninstall.sh qwertz` for QWERTZ or `./uninstall.sh both` for both. In a repository checkout, no argument defaults to QWERTZ. In a downloaded DMG or ZIP package, `install.sh` and `uninstall.sh` default to that package’s variant. Removing one variant leaves the other installed. Remove the corresponding input source from **System Settings → Keyboard → Input Sources** if it still appears.

## Verify the layout source

Run the tests:

```sh
python3 tests/test_coverage.py
python3 tests/test_install.py
```

On macOS, `test_install.py` checks isolated installation and packaged ZIPs without writing to your real Keyboard Layouts folder.

The tests check **both variants**: all 42 letters in both cases, inherited mappings for every hardware map, modifier behavior, punctuation, physical shortcut mappings, duplicate key codes, and the QWERTY Option+I alias. They verify the layout source; they do **not** install it or confirm how an application handles the input source.

### Check the installed layout manually

After installing or upgrading, select each installed variant in a text editor:

1. Type `Қазақстан қазақ ыстық ғылым білім жаңбыр әңгіме өрік үшін ұлт үй әй киім биік жиі сиыр вагон`. Check Y, Z, V, and backtick against the variant comparison above. In QWERTY, check both V and Option+I for `и`, including their uppercase forms; I must still give `і`.
2. Type `ф һ ц щ э ё ю ч ь ъ` using Option, then `Ф Һ Ц Щ Э Ё Ю Ч Ь Ъ` using Option+Shift. Check `ң` and `Ң` with C and Shift+C, and `я` and `Я` with the right bracket key.
3. Turn on Caps Lock. Confirm that letters are uppercase while digits and punctuation stay unshifted. Check Shift+Caps Lock, Caps Lock+Option, and Shift+Caps Lock+Option against the rules above.
4. Try `/ ? " :`, the Option punctuation table, and then a normal letter after each punctuation key; no accent or quote should wait for a second key.
5. Check familiar physical shortcuts such as Command+A, Command+C, Command+V, Command+Z, and Command+Shift+Z where the application supports them. Check any Command+Option shortcuts you use, and switch to ABC/English to test English typing.

Repeat these checks on each keyboard type you use. Application shortcuts and macOS settings can affect the result; this checklist is for manual verification, not a claim that the native UI has been tested.

## Credits

Layout authored with [Ukelele](https://software.sil.org/ukelele/) by SIL International. Released under the [MIT License](LICENSE).
