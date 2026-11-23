# Kazakh-QWERTY / Kazakh-QWERTZ 1.2.0

This release adds **Kazakh-QWERTY** as a separate choice alongside **Kazakh-QWERTZ**. The existing QWERTZ letter layout is unchanged. Both provide all **42 Kazakh Cyrillic letters in both cases**, including the 33 Russian letters, and can be installed side by side.

## Choose your layout

| Physical key | Kazakh-QWERTY | Kazakh-QWERTZ |
| --- | --- | --- |
| Y | й | з |
| Z | з | и |
| V | и | в |
| Backtick | в | й |
| Option+I | и | і |

In QWERTY, **I still types і** and **F still types ы**. The additional **Option+I → и** mapping is an alternative to V, with **И** on Option+Shift+I or Caps Lock+Option+I.

The ten additional Option letters are unchanged in both layouts: **F→ф, H→һ, C→ц, X→щ, E→э, O→ё, W→ю, J→ч, B→ь, V→ъ**. Add Shift for capitals. Caps Lock, punctuation, and physical Command shortcuts retain their existing behavior. Use a separate ABC/English input source for English typing.

On JIS keyboards, the extra yen key mirrors the backtick letter: **в/В in QWERTY**, **й/Й in QWERTZ**. Its Option backslash and Option+Shift vertical bar are unchanged. Both installers include English, Kazakh, and Chinese guides with the complete mappings.

## Downloads

| Layout | Installer | Manual-install archive |
| --- | --- | --- |
| Kazakh-QWERTY | `Kazakh-QWERTY-v1.2.0.dmg` | `Kazakh-QWERTY-v1.2.0.zip` |
| Kazakh-QWERTZ | `Kazakh-QWERTZ-v1.2.0.dmg` | `Kazakh-QWERTZ-v1.2.0.zip` |

The **SHA256SUMS** asset contains checksums for all four files. GitHub's **Source code** downloads are repository snapshots; choose a named DMG or ZIP above for the prepared layout bundle.

## Install or upgrade

1. Download the DMG for your chosen layout and open it.
2. Double-click **Install.command**. It installs or replaces only that variant in your user's `~/Library/Keyboard Layouts/` folder. To install both, run both installers.
3. **Log out and back in**, or restart your Mac, so macOS can load the new layout.
4. Open **System Settings → Keyboard → Input Sources → Edit → +**, choose **Kazakh**, and add **Kazakh-QWERTY** or **Kazakh-QWERTZ**. Add each separately if you installed both.
5. Select the desired layout from the input-source menu. Your existing QWERTZ input source can remain available while you try QWERTY.

Alternatively, extract the matching ZIP and copy `Kazakh-QWERTY.bundle` or `Kazakh-QWERTZ.bundle` into `~/Library/Keyboard Layouts/`, then log out and back in. Both bundles can remain installed together.

From a repository checkout, use `./install.sh qwerty`, `./install.sh qwertz`, or `./install.sh both`. No argument defaults to QWERTZ. The uninstall script accepts the same choices; removing one variant leaves the other installed.

## Help test the layouts

- In each installed layout, type `Қазақстан қазақ ыстық ғылым білім жаңбыр әңгіме өрік үшін ұлт үй әй киім биік жиі сиыр вагон`.
- Check Y, Z, V, and backtick against the comparison table. In QWERTY, confirm both V and Option+I type **и**, and I still types **і**; check their capitals too.
- Check all ten additional Option letters in both cases, including **Option+V → ъ**, which is unchanged.
- Try Caps Lock, Caps Lock+Option, and Shift+Caps Lock+Option. Caps Lock affects letters; Shift controls shifted punctuation.
- Check digits, `/ ?`, quotes, brackets, and the other punctuation listed in the included README.
- Try your usual Command shortcuts and switch to ABC/English for English typing. If both variants are installed, confirm you can switch between them.

Please [report problems](https://github.com/asqatqazet/kazakh-qertz/issues) with the layout name, macOS version, keyboard type (ANSI, ISO, or JIS), application, exact key combination, expected character, and actual result.

Automated source checks cover both variants: all 42 letters in both cases, declared hardware mappings, modifier combinations, punctuation, shortcuts, sample words, and the QWERTY Option+I alias. These checks do not establish that native macOS input or application shortcuts have been tested; use the manual checks above after installation.
