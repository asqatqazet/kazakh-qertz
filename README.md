[English](README.md) | [Қазақша](README.kk.md) | [中文](README.zh.md)

# Kazakh-QWERTZ

A macOS keyboard layout for typing **Kazakh (Cyrillic)** on a QWERTY physical keyboard, with QWERTZ-style positioning for the most common Kazakh letters.

## Layout reference

Default (no modifier) — physical QWERTY key → Kazakh letter:

```
Top row:    Q=ғ  W=у  E=е  R=р  T=т  Y=з  U=ұ  I=і  O=о  P=п  [=ү  ]=ч
Home row:   A=а  S=с  D=д  F=ф  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
Bottom row: Z=и  X=ш  C=ң  V=в  B=б  N=н  M=м
```

Hold **Shift** for uppercase. Hold **Option** (⌥) for special characters and Latin punctuation. Toggle **Caps Lock** for the Latin fallback layer (useful when mixing English into Kazakh text).

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

## Manual install (without git)

Download the latest release zip from the [Releases page](https://github.com/asqatqazet/kazakh-qertz/releases), unzip, and copy `Kazakh-QWERTZ.bundle` into `~/Library/Keyboard Layouts/`.

## Known gaps

The current layout does **not** map these letters from the modern Kazakh Cyrillic alphabet:

- Lowercase: `һ ц щ ъ ы ь э ю`
- Uppercase: `Ң Һ Ц Щ Ъ Ы Ь Э Ю Я`

Most are Russian-borrowed letters used only in loanwords, but `Ң` (uppercase of `ң`) is a core Kazakh letter and its absence is a real defect. Contributions to fix these are welcome — edit `Contents/Resources/Kazakh-QWERTZ.keylayout` in [Ukelele](https://software.sil.org/ukelele/) and remove the corresponding letters from `KNOWN_MISSING_*` in `tests/test_coverage.py`.

## Verify the install

Run the coverage test:

```sh
python3 tests/test_coverage.py
```

It checks that every letter that *should* be mapped is reachable, and that no key code is double-bound.

## Credits

Layout authored with [Ukelele](https://software.sil.org/ukelele/) by SIL International. Released under the [MIT License](LICENSE).
