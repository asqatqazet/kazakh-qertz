# Kazakh-QWERTZ 1.1.0

This release completes the Kazakh Cyrillic alphabet and makes Shift, Option, and Caps Lock consistent. All 42 letters, including the 33 Russian letters, are available in both cases.

## What changed

- Physical **F now types ы**, and **] now types я**. Backtick still types й.
- Option provides the other ten letters: **F→ф, H→һ, C→ц, X→щ, E→э, O→ё, W→ю, J→ч, B→ь, V→ъ**. Add Shift for capitals.
- **Shift+C now types Ң**. Caps Lock produces Cyrillic capitals while leaving digits and punctuation unshifted. Shift+Caps Lock keeps letters uppercase and uses shifted punctuation.
- **Caps Lock no longer switches to Latin letters.** Select ABC/English separately to type English. Physical Command shortcuts retain Latin QWERTY mappings.
- Option punctuation is entered immediately, without dead keys. The slash key produces `/`, or `?` with Shift.
- Hardware-specific mappings preserve the complete alphabet. JIS keyboards also have й/Й on the extra yen key.
- The installer includes English, Kazakh, and Chinese guides with the full mapping and manual test instructions.

## Install or upgrade

1. Download **Kazakh-QWERTZ-v1.1.0.dmg** from the release assets and open it.
2. Double-click **Install.command**. It installs or replaces this layout in your user's `~/Library/Keyboard Layouts/` folder.
3. **Log out and back in**, or restart your Mac, to load the updated layout.
4. If this is your first installation, open **System Settings → Keyboard → Input Sources → Edit → +**, choose **Kazakh → Kazakh-QWERTZ**, and add it.
5. Select **Kazakh-QWERTZ** from the input-source menu.

Alternatively, extract the ZIP asset and copy `Kazakh-QWERTZ.bundle` into `~/Library/Keyboard Layouts/`, then log out and back in. The files named **Source code** by GitHub are repository snapshots; the `.dmg` is the ready-to-use installer.

## Help test the layout

- In a text editor, type `Қазақстан қазақ ыстық ғылым білім жаңбыр әңгіме өрік үшін ұлт үй әй`.
- Check `ы/Ы`, `я/Я`, and `ң/Ң`; then check every Option letter in both cases.
- Try Caps Lock, Caps Lock+Option, and Shift+Caps Lock+Option. Caps Lock should affect letters only; Shift controls shifted punctuation.
- Check digits, `/ ?`, quotes, brackets, and the other punctuation listed in the included README.
- Try your usual Command shortcuts and switch to ABC/English for English typing.

Please [report problems](https://github.com/asqatqazet/kazakh-qertz/issues) with your macOS version, keyboard type (ANSI, ISO, or JIS), application, exact key combination, expected character, and actual result.

Automated source checks cover all 42 letters in both cases, all declared hardware mappings, 256 modifier combinations, punctuation, shortcuts, sample words, and regression cases. They do not replace manual typing tests in macOS applications.

The `SHA256SUMS` asset contains checksums for the DMG and ZIP downloads.
