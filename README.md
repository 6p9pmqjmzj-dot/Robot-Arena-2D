# Robot Arena / ساحة الروبوتات

## العربية

**Robot Arena** لعبة بقاء وقتال ثنائية الأبعاد بمنظور علوي، مكتوبة بـ Python و` turtle` فقط للرسم. تحكم بروبوت أزرق، دمر الروبوتات المعادية، اجمع الطاقة والعناصر، وارفع الـScore قبل أن تنفد الصحة. لا تحتاج اللعبة إلى صور أو ملفات صوتية كي تبدأ.

### التثبيت والتشغيل

يتطلب المشروع Python 3.10 أو أحدث وواجهة Tk المرفقة عادة مع Python.

```bash
python -m pip install -r requirements.txt
python main.py
```

### طريقة اللعب والتحكم

| المفتاح | الوظيفة |
|---|---|
| W/A/S/D أو الأسهم | الحركة، بما فيها القطرية |
| Space | إطلاق طلقة طاقة (20 damage) |
| E | موجة خاصة دائرية: 30 Energy و5 ثوانٍ cooldown |
| P | إيقاف/استئناف |
| R | بدء جديد بعد Game Over |
| Q | خروج |

اللاعب يبدأ بـ100 HP و100 Energy. الطاقة تعود تلقائيًا. بعد الضرر توجد حماية قصيرة، وShield يمنع الضرر مؤقتًا. Damage Boost يزيد ضرر الطلقات 50% لمدة 8 ثوانٍ وSpeed Boost يزيد السرعة 30% لمدة 6 ثوانٍ.

### الأعداء والمستويات والنقاط

BasicBot (50 HP، 100 نقطة) يطارد اللاعب؛ FastBot (30 HP، 150) سريع؛ ShooterBot (70 HP، 250) يحافظ على مسافة ويطلق؛ TankBot (150 HP، 300) ثقيل وبطيء. يبدأ كل مستوى جديد كل 30 ثانية، يزيد معدل الظهور والصحة والسرعة، ويفتح الأنواع تدريجيًا. توجد مكافأة 500 نقطة للمستوى، ونقطة لكل ثانية بقاء. القتل المتتالي خلال 3 ثوانٍ يضاعف قيمة القتل حسب الـCombo.

Health Pack يعيد 25 HP، Energy Cell يعيد 30 Energy، بالإضافة إلى عناصر Damage/Speed/Shield. تسجل اللعبة أفضل نتيجة في `highscore.txt`؛ غيابه أو عدم إمكان قراءته لا يمنع التشغيل.

### التصميم والبنية

الواجهة تستخدم `ontimer()` بسرعة مستهدفة 60FPS ولا توجد حلقة `while` حاجبة. يرصد `InputManager` المفاتيح المضغوطة، و`Collision.py` يقدم AABB، و`HUD.py` منفصل للواجهة. تستخدم المقذوفات والأعداء والانفجارات والعناصر `ObjectPool` لإخفاء وإعادة استعمال Turtle objects بدلاً من إنشاء آلاف الكائنات. الساحة الصناعية، الشبكة، الأضواء، التحذيرات، والعوائق كلها رسوم برمجية.

```text
Robot Arena 2D/
├── main.py                 # نقطة التشغيل الوحيدة
├── Game.py                 # منسق اللعبة
├── requirements.txt
├── highscore.txt
├── Core/                   # entities, input, HUD, collision, pools
├── Player/RobotPlayer.py
├── Enemies/                # أربعة أنواع وEnemyManager
├── Projectiles/            # مقذوفات اللاعب والعدو ومديرها
├── Items/                  # العناصر القابلة للجمع
├── Environment/            # arena, decoration, obstacles
├── Effects/Explosion.py
└── assets/                 # اختياري فقط
```

### إضافة Assets لاحقًا

اللعبة تعمل بلا Assets. إن أضفت GIF متوافقًا مع Turtle، سجله عبر `screen.register_shape()` ثم مرره كـframe إلى `AnimatedEntity`. يمكن استعمال Pillow لتحويل صور PNG إلى GIF عند الحاجة فقط.

Prompts مقترحة للفن الأصلي: `small blue combat robot, top-down view, compact mechanical body, glowing cyan screen, pixel art, transparent background`؛ `small red combat robot, top-down view, mechanical body, glowing red core, pixel art, transparent background`؛ `large heavy armored robot, top-down view, gray metal armor, red energy core, pixel art, transparent background`؛ `robot explosion energy effect, orange yellow and white particles, 5 animation frames, pixel art, transparent background`.

### مشاكل محتملة وأفكار مستقبلية

إذا ظهر خطأ متعلق بـTk، أعد تثبيت Python مع Tcl/Tk. على Linux ثبّت حزمة `python3-tk`. عند فتح النافذة لا تستعمل الطرفية لإيقاف البرنامج؛ استخدم Q. أفكار لاحقة: أصوات اختيارية منفصلة، boss، خرائط، مسار AI حول العوائق، وإعدادات قابلة للحفظ.

---

## English

**Robot Arena** is a top-down 2D survival shooter made with Python and Turtle rendering. Pilot the blue combat robot, destroy hostile bots, collect power-ups, manage energy, and chase a high score. It runs with no external art or sound files.

### Install and run

Python 3.10+ (with Tk) is required.

```bash
python -m pip install -r requirements.txt
python main.py
```

### Gameplay and controls

Use **WASD** or **arrow keys** for diagonal-capable movement, **Space** to fire, **E** for the 30-energy radial special attack, **P** to pause, **R** to restart after game over, and **Q** to quit. The player has 100 HP and 100 regenerating Energy. Health Pack restores HP, Energy Cell restores Energy, Damage Boost lasts 8 seconds, Speed Boost lasts 6 seconds, and Shield protects for 5 seconds.

BasicBot, FastBot, ShooterBot, and TankBot unlock across levels. A new level occurs every 30 seconds and adds spawn pressure, modest stat scaling, and 500 score. Consecutive kills within three seconds build Combo multipliers. Survival adds one score per second. High score is safely loaded/saved in `highscore.txt`.

### Architecture, assets, and troubleshooting

The non-blocking `ontimer()` loop targets 60 FPS. Input, collision, HUD, entities, enemy spawning, projectiles, effects, and environment are isolated by folder. AABB collision covers all gameplay interactions. Object pools reuse projectiles, enemies, effects, and pickups to avoid Turtle-object churn. The industrial arena is drawn programmatically.

Assets are optional. Add Turtle-compatible GIF frames later with `screen.register_shape()` and `AnimatedEntity`; Pillow may be used to prepare PNG-to-GIF assets. If Tk is missing, reinstall Python with Tcl/Tk (or install `python3-tk` on Linux). Future ideas include optional isolated sound, bosses, maps, pathfinding, and settings.
