[English](README.md) | [Қазақша](README.kk.md) | [中文](README.zh.md)

# Kazakh-QWERTZ

QWERTY физикалық пернетақтасында **қазақ тілінде (кириллица)** теруге арналған macOS пернетақта орналасуы. Көп қолданылатын қазақ әріптері QWERTZ стилінде орналастырылған.

## Орналасу кестесі

Қалыпты режим (модификаторсыз) — QWERTY пернесі → қазақ әрпі:

```
Жоғ. қатар:  Q=ғ  W=у  E=е  R=р  T=т  Y=з  U=ұ  I=і  O=о  P=п  [=ү  ]=ч
Орт. қатар:  A=а  S=с  D=д  F=ф  G=г  H=қ  J=ж  K=к  L=л  ;=ө  '=ә  \=х
Төм. қатар:  Z=и  X=ш  C=ң  V=в  B=б  N=н  M=м
```

Бас әріптер үшін **Shift** басып тұрыңыз. Арнайы таңбалар үшін **Option** (⌥) пернесін қолданыңыз. Латын әрпімен араластырып теру үшін **Caps Lock** қосыңыз.

## Орнату

```sh
git clone https://github.com/asqatqazet/kazakh-qertz.git
cd kazakh-qertz
./install.sh
```

Содан кейін:
1. **Жүйеден шығып, қайта кіріңіз** (немесе Mac-ты қайта қосыңыз).
2. **System Settings → Keyboard → Input Sources → Edit → +** ашыңыз.
3. Сол жақтан **Kazakh**, оң жақтан **Kazakh-QWERTZ** таңдап, **Add** басыңыз.
4. Меню жолағындағы тіл таңдағыштан ауысыңыз (немесе `⌃Space` арқылы).

## Жою

```sh
./uninstall.sh
```

Қажет болса, **System Settings → Keyboard → Input Sources** ішінен қолмен өшіріңіз.

## Git-сіз орнату

[Releases бетінен](https://github.com/asqatqazet/kazakh-qertz/releases) соңғы zip-ті жүктеп алыңыз, ашыңыз және `Kazakh-QWERTZ.bundle` қалтасын `~/Library/Keyboard Layouts/` ішіне көшіріңіз.

## Жетіспейтін әріптер

Қазіргі нұсқада қазіргі қазақ алфавитінің мына әріптері **жоқ**:

- Кіші: `һ ц щ ъ ы ь э ю`
- Бас: `Ң Һ Ц Щ Ъ Ы Ь Э Ю Я`

Көбі — кірме сөздерде қолданылатын орыс әріптері. Бірақ `Ң` (ң-нің бас әрпі) — негізгі қазақ әрпі, оның болмауы — нақты ақау. Түзетуге үлес қосуға болады: [Ukelele](https://software.sil.org/ukelele/) арқылы `Contents/Resources/Kazakh-QWERTZ.keylayout` файлын өңдеп, `tests/test_coverage.py` ішіндегі `KNOWN_MISSING_*` тізімінен әріптерді алып тастаңыз.

## Орнатуды тексеру

Тестті іске қосыңыз:

```sh
python3 tests/test_coverage.py
```

Әрбір күтілетін әріптің қол жетімді екенін және бірде-бір перненің қос байланыста еместігін тексереді.

## Алғыс

Орналасу [Ukelele](https://software.sil.org/ukelele/) (SIL International) арқылы жасалған. [MIT лицензиясы](LICENSE) бойынша таратылады.
