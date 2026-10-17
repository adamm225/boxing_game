#!/usr/bin/env python3
"""
BOXER - a tiny retro boxing game.

Starts in BAG mode (free practice on a heavy bag). Next to the BOXING GYM sign:
    SPAR      (or TAB)  a one-off fight against a computer opponent
    CAMPAIGN  (or C)    four fights back to back for the lightweight title belt
    BAG                 back to the heavy bag

    LEFT / RIGHT       move (you always face right)
    A                  jab
    S                  cross
    D                  body jab
    F                  body cross
    W                  slip  (dodges head shots; punch right after for a COUNTER)
    E  (hold)          high block   - stops head shots, body shots still land
    R  (hold)          low block    - stops body shots, head is open
                       Tap block just before a punch lands to PARRY it (attacker is stunned).
    BACKSPACE          reset bag / restart fight
    1 / 2 / 3          sparring difficulty (easy / normal / hard)
    ENTER              rematch after a fight
    M  mute     F11  fullscreen     ESC  quit

Sparring rules
    * Both fighters have HP. Go a few seconds without taking damage and you slowly heal,
      but only up to your healing cap (the white tick on your HP bar). Body shots lower the cap.
    * Blocking drains your GUARD bar (blue). Blocking punch after punch drains it faster -
      eat a flurry and your guard breaks, leaving you stunned and wide open.
    * Critical hits do extra damage. Hitting someone mid-punch (counter hit), after a slip,
      or while they are stunned makes crits much more likely (stunned = guaranteed).

Campaign
    * Rusty Rick -> Bruno "The Bulldozer" -> "Lightning" Lee -> Victor "The Crown" Reyes,
      the lightweight champion. Each has his own look, fighting style and trash talk.
    * You start every fight at full health. Lose once and you start over at fight 1.
    * ENTER / SPACE skips dialogue and moves on between fights.

Setup:   pip install pygame
Run:     python boxer_game.py            (optional: --scale=5 for a bigger window)

The character sprites are embedded at the bottom of this file, so this is the only file you need.
"""
import array
import base64
import io
import math
import random
import sys

import pygame

# ============================================================ screen / sprite layout
VW, VH = 320, 180            # internal pixel-art resolution (scaled up to the window)
FW, FH = 96, 80              # sprite frame size
HIP_X = 38                   # x of the hips inside a (right-facing) sprite frame
GROUND = 154                 # y of the floor line the boxers stand on
SPRITE_FEET = 76             # row inside the sprite that touches the floor
FPS = 60

MIN_X, STAGE_MAX_X = 26, VW - 26
WALK_FWD, WALK_BACK = 78.0, 62.0   # walking speed (internal px / second)

# ============================================================ bag mode
BAG_X = 236                  # bag pivot x
PIVOT_Y = 10                 # chain pivot y (just under the ceiling beam)
BAG_TOP = 78                 # y of the top of the bag at rest
BAG_H, BAG_W, BAG_HALF = 66, 30, 14
CHAIN_LEN = BAG_TOP - PIVOT_Y
MAX_X = BAG_X - 36           # closest the boxer can stand to the resting bag
REACH_SLACK = 4              # glove tip may be this many px short of the bag and still connect

# ============================================================ sparring tuning
MAX_HP = 100
REGEN_DELAY = 3.0            # (Y) seconds without taking damage before you start healing
REGEN_CAP = 70               # (X) natural healing stops at this much HP
REGEN_RATE = 3.0             # HP healed per second
BODY_CAP_LOSS = 3            # each clean body shot lowers the victim's healing cap by this much...
REGEN_CAP_MIN = 40           # ...but never below this
GUARD_MAX = 100
GUARD_REGEN = 35.0           # guard points per second
GUARD_REGEN_DELAY = 0.9      # seconds after your last blocked punch before guard refills
FLURRY_RAMP = 0.3            # every extra punch blocked in a row drains the guard 30% more
FLURRY_WINDOW = 0.8          # blocked punches less than this far apart count as "in a row"
GUARD_BREAK_STUN = 1.0       # seconds stunned when your guard breaks
PARRY_WINDOW = 0.15          # block must start this close to the punch landing to parry
PARRY_COOLDOWN = 0.4         # can't parry by mashing the block key
PARRY_STUN = 0.6             # attacker is stunned this long after being parried
CRIT_CHANCE = 0.07
CRIT_MULT = 1.8
COUNTER_HIT_MULT = 1.35      # hitting someone in the middle of throwing a punch
MIN_SEP = 40                 # closest two boxers can stand (hip to hip)
ROUND_TIME = 99
HURT = {"head": 12, "body": 11}   # how far in front of the hips the head / body can be hit
TARGET_Y = {"head": 30, "body": 46}

# ============================================================ animation frames
IDLE_SEQ = [0, 1, 2, 1]      # guard "breathing" frames
IDLE_MS = 200
WALK_BASE = 20               # first walk frame in the strip (6 frames)
WALK_FRAMES = 6
F_BLOCK_HIGH = (37, 38)
F_BLOCK_LOW = (39, 40)
F_HIT_HEAD = (41, 42)
F_HIT_BODY = (43, 44)
F_BLOCK_HIT_HIGH, F_BLOCK_HIT_LOW = 45, 46
F_STAGGER = (47, 48, 49, 48)
F_KO = (50, 51, 52)
F_WIN = (53, 54)

# Each action is a list of sprite frames with a duration (ms) per frame.
#   active : frames in which the glove can connect      cancel : index from which you can chain
#   lunge  : extra px slid forward on each frame         dmg/kick/shake/stop : bag-mode feel
#   target : head/body   spar_dmg : sparring damage   guard : guard drain when blocked
#   stun   : hit-stun on the victim (seconds)
ACTIONS = {
    "jab": dict(frames=[3, 4, 5, 6, 7], ms=[70, 90, 40, 120, 60], active={6}, cancel=4,
                lunge=[0, 1, 2, 2, 1], dmg=8, kick=0.7, shake=1, stop=0.045,
                target="head", spar_dmg=5, guard=14, stun=0.22),
    "cross": dict(frames=[12, 13, 14, 15, 16, 17], ms=[110, 40, 140, 90, 70, 80], active={14, 15},
                  cancel=4, lunge=[0, 1, 3, 3, 2, 1], dmg=22, kick=1.6, shake=3, stop=0.085,
                  target="head", spar_dmg=10, guard=26, stun=0.32),
    "body_jab": dict(frames=[26, 27, 28, 29, 30], ms=[60, 80, 40, 110, 70], active={29}, cancel=4,
                     lunge=[0, 1, 2, 2, 1], dmg=9, kick=0.75, shake=1, stop=0.05,
                     target="body", spar_dmg=5, guard=14, stun=0.26),
    "body_cross": dict(frames=[31, 32, 33, 34, 35, 36], ms=[60, 100, 40, 130, 80, 80], active={34},
                       cancel=4, lunge=[0, 0, 2, 3, 2, 1], dmg=24, kick=1.7, shake=3, stop=0.09,
                       target="body", spar_dmg=11, guard=26, stun=0.38),
    "slip": dict(frames=[8, 9, 10, 10, 9, 8], ms=[60, 60, 150, 100, 60, 70], active=set(),
                 cancel=3, lunge=[0, 0, -1, -1, 0, 0]),
}
PUNCHES = ("jab", "cross", "body_jab", "body_cross")
COUNTER_WINDOW = 0.6         # seconds after the bottom of a slip in which a punch is a counter
COUNTER_MULT = 1.5
BUFFER_TIME = 0.8            # a key pressed up to this long before you can act is queued (one action)

# ============================================================ computer opponent
#   react  : chance to try to defend a punch      delay : reaction time (s)
#   slip   : chance to slip a head shot instead of blocking     wrong : blocks the wrong height
#   parry  : chance a block is perfectly timed    atk : seconds between attack decisions
#   combo / flurry / punish : chance to throw combos / flurry a blocker / punish a whiff
#   guard_up : how often it just sits behind its guard
LEVELS = {
    "EASY": dict(react=0.30, delay=(0.13, 0.30), slip=0.15, wrong=0.30, parry=0.0, atk=(1.0, 2.2),
                 combo=0.20, flurry=0.25, punish=0.20, guard_up=0.10),
    "NORMAL": dict(react=0.65, delay=(0.07, 0.16), slip=0.25, wrong=0.12, parry=0.30, atk=(0.6, 1.4),
                   combo=0.35, flurry=0.50, punish=0.55, guard_up=0.20),
    "HARD": dict(react=0.8, delay=(0.04, 0.11), slip=0.30, wrong=0.06, parry=0.45, atk=(0.35, 0.95),
                 combo=0.50, flurry=0.70, punish=0.70, guard_up=0.25),
}
LEVEL_KEYS = ["EASY", "NORMAL", "HARD"]

# ============================================================ looks (palette swaps of the player sprite)
SRC = dict(  # the player's colours that get swapped
    glove=(224, 40, 52), glove_l=(255, 120, 108), glove_d=(150, 22, 44), glove_far=(180, 30, 50),
    glove_far_d=(120, 18, 42), glove_hl=(255, 176, 156),
    shorts=(46, 98, 208), shorts_s=(26, 56, 148), shorts_l=(104, 158, 248),
    skin=(240, 172, 114), skin_s=(198, 118, 78), skin_l=(255, 214, 158), skin_far=(206, 126, 86),
    skin_far_s=(160, 92, 66), skin_ol=(86, 42, 44), ear=(150, 80, 64),
    hair=(46, 32, 40), hair_s=(28, 18, 28), hair_l=(108, 80, 94),
    boot=(246, 246, 248), boot_s=(172, 178, 202), boot_far=(206, 210, 226), boot_far_s=(146, 152, 180),
    sole=(70, 72, 100),
)


def _mix(c, target, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c, target))


def lighten(c, t):
    return _mix(c, (255, 255, 255), t)


def darken(c, t):
    return _mix(c, (0, 0, 0), t)


def look_palette(glove=None, shorts=None, skin=None, hair=None, boots=None):
    """Recolour map (player colour -> new colour) built from a few base colours.
    Gloves also recolour the headband and boot stripes. hair="bald" shaves the head."""
    m = {}
    if glove:
        m.update({SRC["glove"]: glove, SRC["glove_l"]: lighten(glove, .45), SRC["glove_d"]: darken(glove, .35),
                  SRC["glove_far"]: darken(glove, .18), SRC["glove_far_d"]: darken(glove, .45),
                  SRC["glove_hl"]: lighten(glove, .65)})
    if shorts:
        m.update({SRC["shorts"]: shorts, SRC["shorts_s"]: darken(shorts, .38), SRC["shorts_l"]: lighten(shorts, .4)})
    skin = skin or SRC["skin"]
    m.update({SRC["skin"]: skin, SRC["skin_s"]: darken(skin, .2), SRC["skin_l"]: lighten(skin, .3),
              SRC["skin_far"]: darken(skin, .14), SRC["skin_far_s"]: darken(skin, .34),
              SRC["skin_ol"]: darken(skin, .62), SRC["ear"]: darken(skin, .4)})
    if hair == "bald":
        m.update({SRC["hair"]: darken(skin, .07), SRC["hair_s"]: darken(skin, .25), SRC["hair_l"]: lighten(skin, .35)})
    elif hair:
        m.update({SRC["hair"]: hair, SRC["hair_s"]: darken(hair, .4), SRC["hair_l"]: lighten(hair, .35)})
    if boots:
        m.update({SRC["boot"]: boots, SRC["boot_s"]: darken(boots, .3), SRC["boot_far"]: darken(boots, .16),
                  SRC["boot_far_s"]: darken(boots, .42),
                  SRC["sole"]: (150, 152, 172) if sum(boots) < 360 else (70, 72, 100)})
    return m


SPAR_LOOK = dict(glove=(52, 110, 230), shorts=(196, 40, 52), skin=(170, 108, 70), hair=(232, 196, 92),
                 boots=(64, 66, 90))

# ============================================================ campaign
#   look   : colours (see look_palette)          level/ai : AI difficulty + overrides (see LEVELS)
#   style  : how much he likes each punch        hp/power/speed/walk : health, punch damage,
#   taunt  : pre-fight animation                                       animation speed, footspeed
CAMPAIGN = [
    dict(name='RICK "RUSTY" MALONE', short="RUSTY RICK", title="JOURNEYMAN   -   RECORD 8-11",
         color=(150, 230, 160), look=dict(glove=(236, 236, 242), shorts=(56, 156, 84), skin=(250, 200, 156),
                                          hair=(196, 88, 40)),
         level="EASY", ai=dict(), style=dict(jab=1.6), hp=80, power=0.9, speed=1.0, walk=1.0, taunt="shadowbox",
         intro="Fresh meat! Hope you packed a lunch, 'cause you're about to get SERVED!",
         reply="Order up, Rusty. Hope you like it extra crispy.",
         win="Ha! Back to the punching bag, rookie!",
         lose="Ow... my everything..."),
    dict(name='BRUNO "THE BULLDOZER" KASK', short="BULLDOZER", title="HEAVY HITTER   -   RECORD 14-4",
         color=(255, 170, 90), look=dict(glove=(240, 128, 40), shorts=(52, 48, 64), skin=(214, 150, 100),
                                         hair="bald", boots=(52, 48, 64)),
         level="NORMAL", ai=dict(react=0.45, slip=0.08, parry=0.2, atk=(0.8, 1.6)),
         style=dict(jab=0.6, cross=2.5, body_cross=2.5), hp=120, power=1.2, speed=0.92, walk=0.85, taunt="roar",
         intro="NOTHING stops the Bulldozer! I'm gonna flatten you like a PANCAKE!",
         reply="Even bulldozers run out of gas, big guy.",
         win="FLATTENED! Somebody scrape this guy off my canvas!",
         lose="Who... turned off... the engine..."),
    dict(name='"LIGHTNING" LEE PARK', short="LIGHTNING LEE", title="SPEED DEMON   -   RECORD 19-2",
         color=(200, 160, 255), look=dict(glove=(150, 70, 214), shorts=(240, 206, 56), skin=(232, 182, 132),
                                          hair=(34, 34, 48)),
         level="NORMAL", ai=dict(react=0.78, slip=0.5, parry=0.35, delay=(0.05, 0.12), atk=(0.45, 1.0),
                                 combo=0.55, punish=0.65),
         style=dict(jab=2.5, body_jab=1.5), hp=95, power=1.0, speed=1.18, walk=1.35, taunt="weave",
         intro="Better not blink. I'll be done before your health bar even loads!",
         reply="Lightning never strikes twice. I do.",
         win="Too slow! Try again in slow motion.",
         lose="Impossible... nobody's faster than me!"),
    dict(name='VICTOR "THE CROWN" REYES', short="THE CROWN", title="LIGHTWEIGHT CHAMPION   -   RECORD 40-0",
         color=(255, 214, 90), champ=True,
         look=dict(glove=(44, 40, 54), shorts=(232, 180, 56), skin=(196, 128, 88), hair=(26, 22, 28)),
         level="HARD", ai=dict(parry=0.5), style=dict(), hp=130, power=1.12, speed=1.06, walk=1.1, taunt="belt",
         intro="Forty fights. Forty knockouts. You want my belt? Come and take it... if you dare.",
         reply="I didn't come here to lose. That belt is MINE.",
         win="You were never on my level.",
         lose="The crown... is yours, kid. Wear it well."),
]
LOSE_LINES = ["Dang it... I'll get 'em next time!", "Ugh. Back to the heavy bag...",
              "That one's on me. Run it back!"]
TAUNTS = {   # frame sequence, ms per frame
    "shadowbox": ([3, 4, 5, 6, 7, 0, 0, 12, 13, 14, 15, 16, 17, 0, 0, 0], 90),
    "roar": ([0, 0, 53, 54, 54, 54, 54, 54, 53, 0, 0, 0], 110),
    "weave": ([8, 9, 10, 9, 8, 0, 8, 9, 10, 9, 8, 0, 0, 0], 55),
    "belt": ([54, 54, 54, 54, 54, 54, 53, 54], 130),
    "reply": ([0, 37, 38, 38, 38, 38, 37, 0], 120),
    "champ": ([54, 54, 54, 53], 180),
}
CONFETTI = [(255, 90, 110), (255, 214, 90), (90, 200, 255), (130, 240, 140), (255, 255, 255), (200, 140, 255)]


# ============================================================ small helpers
def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def draw_text(surf, font, s, x, y, color, shadow=(20, 14, 30), center=False, right=False):
    img = font.render(s, False, color)
    sh = font.render(s, False, shadow)
    w = img.get_width()
    if center:
        x -= w // 2
    elif right:
        x -= w
    x, y = int(x), int(y)
    for dx, dy in ((1, 0), (0, 1), (1, 1)):
        surf.blit(sh, (x + dx, y + dy))
    surf.blit(img, (x, y))


def load_strip(b64):
    raw = base64.b64decode("".join(b64.split()))
    return pygame.image.load(io.BytesIO(raw), "strip.png").convert_alpha()


def split(strip, flip=False):
    frames = [strip.subsurface((i * FW, 0, FW, FH)).copy() for i in range(strip.get_width() // FW)]
    return [pygame.transform.flip(f, True, False) for f in frames] if flip else frames


def recolor(strip, mapping):
    """Exact colour swap (via temporary colours, so swaps can't chain into each other)."""
    s = strip.copy()
    pa = pygame.PixelArray(s)
    temps = []
    for k, (src, dst) in enumerate(mapping.items()):
        tmp = (k + 1, 1, 3)
        pa.replace(src, tmp)
        temps.append((tmp, dst))
    for tmp, dst in temps:
        pa.replace(tmp, dst)
    pa.close()
    return s


def wrap(font, text, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if font.size(trial)[0] <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def make_belt():
    s = pygame.Surface((36, 13), pygame.SRCALPHA)
    ol, gold, gold_l, gold_d = (24, 14, 34), (236, 184, 56), (255, 232, 140), (170, 118, 30)
    s.fill(ol, (0, 3, 36, 7))
    s.fill((48, 30, 44), (1, 4, 34, 5))
    s.fill((84, 56, 70), (1, 4, 34, 1))
    for x in (3, 32):
        s.set_at((x, 6), gold_l)
    for x in (5, 27):
        s.fill(ol, (x, 2, 5, 9))
        s.fill(gold, (x + 1, 3, 3, 7))
        s.fill(gold_l, (x + 1, 3, 3, 1))
        s.fill(gold_d, (x + 1, 9, 3, 1))
    pygame.draw.ellipse(s, ol, (10, 0, 16, 13))
    pygame.draw.ellipse(s, gold_d, (11, 1, 14, 11))
    pygame.draw.ellipse(s, gold, (11, 1, 13, 10))
    pygame.draw.ellipse(s, gold_l, (13, 2, 7, 4))
    pygame.draw.circle(s, (220, 36, 60), (18, 6), 2)
    s.set_at((17, 5), (255, 170, 180))
    return s


def fist_point(frame):
    """Right-most opaque pixel of a frame = the glove tip (x), plus the glove's average height (y)."""
    best = -1
    for x in range(FW - 1, -1, -1):
        if any(frame.get_at((x, y)).a > 0 for y in range(FH)):
            best = x
            break
    ys = []
    for x in range(best - 3, best + 1):
        ys += [y for y in range(FH) if frame.get_at((x, y)).a > 0]
    return best, sum(ys) / len(ys)


def time_to_active(f):
    """Seconds until fighter f's current punch reaches its first active frame."""
    spec = ACTIONS[f.action]
    first = next(i for i, fr in enumerate(spec["frames"]) if fr in spec["active"])
    if f.idx >= first:
        return 0.0
    return (sum(spec["ms"][f.idx:first]) - f.t) / 1000.0 / f.speed


# ============================================================ sound (synthesised, no files)
def make_sounds():
    snd = {}
    try:
        init = pygame.mixer.get_init()
        if not init:
            return snd
        rate, fmt, ch = init
        if fmt != -16:
            return snd
    except pygame.error:
        return snd

    def synth(dur, fn):
        n = int(dur * rate)
        buf = array.array("h")
        for i in range(n):
            v = clamp(fn(i / rate, i / n), -1.0, 1.0)
            s = int(v * 32767 * 0.55)
            for _ in range(ch):
                buf.append(s)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def whoosh(dur, lo, hi, vol):
        state = [0.0]

        def fn(t, u):
            a = lo + (hi - lo) * u
            state[0] += (random.uniform(-1, 1) - state[0]) * a
            return state[0] * (math.sin(math.pi * u) ** 2) * vol * 3.0
        return synth(dur, fn)

    def thump(dur, f0, f1, vol, crack):
        ph = [0.0]

        def fn(t, u):
            f = f1 + (f0 - f1) * math.exp(-t * 30)
            ph[0] += 2 * math.pi * f / rate
            body = math.sin(ph[0]) * math.exp(-t * 16)
            click = random.uniform(-1, 1) * math.exp(-t * 60) * crack
            return body * vol + click
        return synth(dur, fn)

    def bell(dur, base, vol):
        def fn(t, u):
            v = (math.sin(2 * math.pi * base * t) + 0.5 * math.sin(2 * math.pi * base * 1.5 * t)
                 + 0.3 * math.sin(2 * math.pi * base * 2.76 * t))
            return v * math.exp(-t * 3.2) * vol * 0.5
        return synth(dur, fn)

    try:
        snd["swish"] = whoosh(0.11, 0.55, 0.12, 0.35)
        snd["slip"] = whoosh(0.20, 0.25, 0.08, 0.28)
        snd["hit_jab"] = thump(0.16, 190, 80, 0.9, 0.35)
        snd["hit_cross"] = thump(0.24, 150, 50, 1.0, 0.6)
        snd["crit"] = thump(0.32, 130, 38, 1.0, 0.95)
        snd["block"] = thump(0.09, 320, 200, 0.45, 0.5)
        snd["parry"] = bell(0.30, 1250, 0.8)
        snd["guard_break"] = thump(0.35, 260, 60, 0.9, 1.0)
        snd["bell"] = bell(1.2, 880, 1.0)

        def tones(notes, wave, vol):
            starts, acc = [], 0.0
            for _, d, _ in notes:
                starts.append(acc)
                acc += d
            ph = [0.0]

            def fn(t, u):
                i = 0
                while i + 1 < len(notes) and t >= starts[i + 1]:
                    i += 1
                f, d, vib = notes[i]
                lt = t - starts[i]
                if vib:
                    f *= 1 + 0.04 * math.sin(2 * math.pi * 5.5 * lt) * min(1.0, lt / 0.25)
                ph[0] += 2 * math.pi * f / rate
                env = min(1.0, lt / 0.02) * (1.0 - 0.45 * lt / d)
                if lt > d - 0.03:
                    env *= max(0.0, (d - lt) / 0.03)
                return wave(ph[0]) * env * vol
            return synth(acc, fn)

        def brass(p):
            return 0.55 * math.sin(p) + 0.3 * math.sin(2 * p) + 0.18 * math.sin(3 * p) + 0.1 * math.sin(4 * p)

        def square(p):
            return 0.45 if math.sin(p) >= 0 else -0.45

        snd["sad"] = tones([(233, .34, 0), (220, .34, 0), (208, .34, 0), (196, 1.1, 1)], brass, 0.8)
        snd["fanfare"] = tones([(523, .12, 0), (659, .12, 0), (784, .12, 0), (1047, .26, 0), (784, .12, 0),
                                (1047, .7, 1)], square, 0.5)
        snd["blip"] = tones([(900, .022, 0)], square, 0.22)
        crowd_state = [0.0, 0.0]

        def crowd(t, u):
            crowd_state[0] += (random.uniform(-1, 1) - crowd_state[0]) * 0.35
            crowd_state[1] += (crowd_state[0] - crowd_state[1]) * 0.5
            swell = 0.7 + 0.3 * math.sin(2 * math.pi * 1.3 * t) * math.sin(2 * math.pi * 0.7 * t)
            env = min(1.0, t / 0.4) * min(1.0, (2.6 - t) / 0.9)
            return crowd_state[1] * 2.2 * swell * env
        snd["crowd"] = synth(2.6, crowd)
    except pygame.error:
        return {}
    return snd


# ============================================================ scenery
SIGN_POS = (88, 17)


def make_background():
    rnd = random.Random(7)
    bg = pygame.Surface((VW, VH))
    bg.fill((30, 34, 58))
    wall_bottom = 134

    bw, bh = 20, 9
    base = (54, 60, 92)
    for row in range(wall_bottom // bh + 1):
        y = row * bh
        off = (row % 2) * (bw // 2)
        for bx in range(-bw, VW + bw, bw):
            v = rnd.randint(-5, 5) + int(-16 + 24 * (y / wall_bottom))
            col = tuple(clamp(c + v, 0, 255) for c in base)
            bg.fill(col, (bx + off, y, bw - 1, bh - 1))

    y, i = 141, 0
    while y < VH:
        h = 5 + min(i // 2, 5)
        bg.fill((92, 64, 78) if i % 2 == 0 else (101, 71, 85), (0, y, VW, h - 1))
        bg.fill((62, 42, 58), (0, y + h - 1, VW, 1))
        off = (i * 37) % 48
        for x in range(-off, VW, 48):
            bg.fill((62, 42, 58), (x, y, 1, h - 1))
        y += h
        i += 1

    bg.fill((36, 28, 48), (0, 134, VW, 7))
    bg.fill((86, 72, 108), (0, 134, VW, 1))
    bg.fill((26, 22, 36), (0, 0, VW, 9))
    bg.fill((70, 60, 88), (0, 9, VW, 1))
    for x in range(14, VW, 52):
        bg.fill((44, 38, 58), (x, 0, 2, 9))
    bg.fill((70, 66, 92), (BAG_X - 4, 8, 8, 4))
    bg.fill((30, 26, 44), (BAG_X - 4, 11, 8, 1))

    for (px, py, pw, ph, col) in ((22, 40, 30, 40, (196, 56, 66)), (118, 46, 26, 34, (226, 190, 120)),
                                  (262, 42, 28, 38, (76, 120, 196))):
        bg.fill((20, 14, 30), (px - 1, py - 1, pw + 2, ph + 2))
        bg.fill(col, (px, py, pw, ph))
        bg.fill((255, 255, 255), (px + 4, py + 5, pw - 8, 3))
        bg.fill((255, 255, 255), (px + 4, py + 11, pw - 14, 2))
        pygame.draw.circle(bg, (24, 16, 34), (px + pw // 2, py + ph - 14), 6)
        bg.fill((24, 16, 34), (px + pw // 2 - 8, py + ph - 8, 16, 8))

    glow = pygame.Surface((VW, VH), pygame.SRCALPHA)
    for lx in (70, 176, 300):
        bg.fill((20, 16, 28), (lx, 9, 1, 38))
        pygame.draw.polygon(bg, (214, 182, 96), [(lx - 6, 52), (lx + 6, 52), (lx + 3, 47), (lx - 3, 47)])
        bg.fill((255, 244, 190), (lx - 4, 52, 8, 1))
        pygame.draw.polygon(glow, (255, 240, 190, 14), [(lx - 5, 53), (lx + 5, 53), (lx + 62, 138), (lx - 62, 138)])
        pygame.draw.ellipse(glow, (255, 240, 190, 20), (lx - 60, 146, 120, 26))
    bg.blit(glow, (0, 0))

    f = pygame.font.Font(None, 20)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        bg.blit(f.render("BOXING GYM", False, (120, 28, 72)), (SIGN_POS[0] + dx, SIGN_POS[1] + dy))
    bg.blit(f.render("BOXING GYM", False, (255, 110, 160)), SIGN_POS)

    vig = pygame.Surface((VW, VH), pygame.SRCALPHA)
    for x in range(VW):
        d = abs(x - VW / 2) / (VW / 2)
        vig.fill((0, 0, 0, int(70 * d * d)), (x, 0, 1, VH))
    bg.blit(vig, (0, 0))
    return bg


def make_bag_surface():
    """Chain + bag on one tall surface; row 0 is the pivot, so the bag can be bent row by row."""
    w, h = BAG_W, CHAIN_LEN + BAG_H
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    cx = w // 2
    ol = (24, 14, 34)

    for r in range(CHAIN_LEN):
        k = r % 6
        if k < 3:
            s.fill((54, 58, 84), (cx - 2, r, 1, 1))
            s.fill((54, 58, 84), (cx + 1, r, 1, 1))
            s.fill((196, 202, 220), (cx - 1, r, 2, 1))
        else:
            s.fill((54, 58, 84), (cx, r, 1, 1))
            s.fill((128, 134, 160), (cx - 1, r, 1, 1))
    s.fill((54, 58, 84), (cx - 3, 0, 6, 2))
    s.fill((150, 156, 182), (cx - 2, 0, 4, 1))

    base, light, shade, dark = (178, 52, 58), (232, 112, 102), (122, 32, 48), (88, 22, 42)
    navy, navy_s = (50, 56, 108), (32, 38, 74)
    tan, tan_l, tan_s = (222, 184, 116), (246, 218, 150), (170, 130, 84)

    def inset(j):
        top = [5, 3, 2, 1, 1, 0]
        if j < 6:
            return top[j]
        if j >= BAG_H - 6:
            return top[BAG_H - 1 - j]
        return 0

    def band(t, pal):
        b, l, sh, dk = pal
        if t < 0.12:
            return b
        if t < 0.32:
            return l
        if t < 0.62:
            return b
        if t < 0.85:
            return sh
        return dk

    for j in range(BAG_H):
        y = CHAIN_LEN + j
        x0, x1 = 1 + inset(j), w - 1 - inset(j)
        n = x1 - x0
        in_cap = j < 7 or j >= BAG_H - 8
        strap = any(a <= j < a + 3 for a in (12, 34, 56))
        if in_cap:
            pal = (navy, (84, 94, 156), navy_s, (22, 26, 52))
        elif strap:
            pal = (tan, tan_l, tan_s, (126, 94, 62))
        else:
            pal = (base, light, shade, dark)
        for x in range(x0, x1):
            s.set_at((x, y), band((x - x0) / max(1, n - 1), pal))
        s.set_at((x0, y), ol)
        s.set_at((x1 - 1, y), ol)
        if j == 0 or j == BAG_H - 1 or j in (7, BAG_H - 8):
            s.fill(ol, (x0, y, n, 1))
        if not in_cap and not strap and j in (11, 15, 33, 37, 55, 59):
            s.fill((60, 28, 40), (x0 + 1, y, n - 2, 1))
    for a in (12, 34, 56):
        for x in range(4, w - 4, 3):
            s.set_at((x, CHAIN_LEN + a + 1), (120, 88, 56))
    for p in ((cx - 7, CHAIN_LEN + 18), (cx - 7, CHAIN_LEN + 19), (cx - 6, CHAIN_LEN + 18)):
        s.set_at(p, (255, 190, 170))
    return s


class Bag:
    W0 = 3.8          # pendulum frequency (rad/s) - higher = snappier swing
    DAMP = 0.45       # air resistance
    LIMIT = 0.62      # max swing angle (rad)

    def __init__(self):
        self.surf = make_bag_surface()
        self.flash_surf = self.surf.copy()
        self.flash_surf.fill((62, 56, 56, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.reset()

    def reset(self):
        self.theta = 0.0
        self.omega = 0.0
        self.flash = 0.0

    def kick(self, impulse):
        self.omega += impulse

    def update(self, dt):
        self.flash = max(0.0, self.flash - dt)
        steps = max(1, int(dt / 0.004))
        h = dt / steps
        for _ in range(steps):
            acc = -self.W0 * self.W0 * math.sin(self.theta) - self.DAMP * self.omega
            self.omega += acc * h
            self.theta += self.omega * h
        if abs(self.theta) > self.LIMIT:
            self.theta = math.copysign(self.LIMIT, self.theta)
            self.omega *= -0.3
        if abs(self.theta) < 0.002 and abs(self.omega) < 0.01:
            self.theta = self.omega = 0.0

    def x_at(self, y):
        return BAG_X + (y - PIVOT_Y) * math.tan(self.theta)

    def top_bottom(self):
        c = math.cos(self.theta)
        return PIVOT_Y + CHAIN_LEN * c, PIVOT_Y + (CHAIN_LEN + BAG_H) * c

    def bottom_x(self):
        return BAG_X + (CHAIN_LEN + BAG_H) * math.sin(self.theta)

    def draw(self, out):
        src = self.flash_surf if self.flash > 0 else self.surf
        s, c = math.sin(self.theta), math.cos(self.theta)
        w = src.get_width()
        for r in range(src.get_height()):
            out.blit(src, (BAG_X - w // 2 + round(r * s), PIVOT_Y + round(r * c)), (0, r, w, 1))


# ============================================================ a boxer (you or the computer)
class Fighter:
    def __init__(self, game, frames, facing):
        self.game = game
        self.frames = frames
        self.facing = facing           # +1 faces right, -1 faces left
        self.configure()
        self.reset(72)

    def configure(self, max_hp=MAX_HP, power=1.0, speed=1.0, walk=1.0):
        """Per-boxer stats: health, punch damage multiplier, animation speed, footspeed."""
        self.max_hp, self.power, self.speed, self.walk = float(max_hp), power, speed, walk

    def reset(self, x):
        self.x = float(x)
        self.action, self.idx, self.t = None, 0, 0.0
        self.idle_i, self.idle_t = 0, 0.0
        self.walk_i, self.walk_t = 0, 0.0
        self.moving = 0
        self.buffer, self.buffer_age = None, 0.0
        self.counter_t, self.is_counter = 0.0, False
        self.hit_done = False
        self.attack_id = 0
        self.hp = self.hp_lag = self.max_hp
        self.regen_cap = self.max_hp * REGEN_CAP / MAX_HP
        self.pose_override = None      # a fixed frame (taunts, celebrations)
        self.belt = False              # holding the title belt overhead
        self.since_damage = 99.0
        self.healing = False
        self.guard, self.guard_t = float(GUARD_MAX), 99.0
        self.block_chain, self.block_chain_t = 0, 0.0
        self.block, self.want_block, self.block_t = None, None, 0.0
        self.parry_ready, self.parry_cd = False, 0.0
        self.parry_ok = True           # the AI clears this for blocks it didn't time on purpose
        self.block_hit_t = 0.0
        self.react, self.react_t, self.react_total = None, 0.0, 0.0
        self.hitstun = 0.0
        self.stun_t, self.stun_el = 0.0, 0.0
        self.ko = self.won = False
        self.end_t = 0.0
        self.ghosts = []

    # ------------------------------------------------------------ state queries
    def busy(self):
        return self.ko or self.won or self.stun_t > 0 or self.hitstun > 0

    def slipping(self):
        return self.action == "slip" and 1 <= self.idx <= 4

    def in_startup(self):
        """Throwing a punch that has not landed yet (can be counter-hit)."""
        if self.action not in PUNCHES or self.hit_done:
            return False
        spec = ACTIONS[self.action]
        last = max(i for i, fr in enumerate(spec["frames"]) if fr in spec["active"])
        return self.idx <= last

    def can_start(self, name):
        if self.busy():
            return False
        if self.action is None:
            return True
        return self.idx >= ACTIONS[self.action]["cancel"]

    # ------------------------------------------------------------ actions
    def press(self, name):
        if self.can_start(name):
            self.start(name)
        else:
            self.buffer, self.buffer_age = name, 0.0

    def start(self, name):
        self.action, self.idx, self.t = name, 0, 0.0
        self.hit_done = False
        self.buffer = None
        self.moving = 0
        self.block = None
        if name == "slip":
            self.counter_t = 0.0
            self.ghosts.append(self.make_ghost())
            self.game.snd("slip")
        else:
            self.attack_id += 1
            self.is_counter = self.counter_t > 0
            self.counter_t = 0.0
            self.game.snd("swish")

    def finish_action(self):
        self.action, self.idx, self.t = None, 0, 0.0
        self.idle_t = self.walk_t = 0.0

    def get_hit(self, target, stun):
        self.finish_action()
        self.block = None
        self.buffer = None
        self.stun_t = 0.0
        self.hitstun = stun
        self.react = F_HIT_HEAD if target == "head" else F_HIT_BODY
        self.react_t, self.react_total = 0.0, stun

    def stagger(self, dur):
        self.finish_action()
        self.block = None
        self.buffer = None
        self.hitstun = 0.0
        self.stun_t, self.stun_el = dur, 0.0

    def push(self, px):
        self.x = clamp(self.x - self.facing * px, MIN_X, STAGE_MAX_X)

    def make_ghost(self, frame=None):
        img = self.frames[IDLE_SEQ[self.idle_i] if frame is None else frame].copy()
        img.fill((50, 80, 150, 0), special_flags=pygame.BLEND_RGB_ADD)
        return dict(img=img, x=self.sprite_x(), t=0.0, life=0.26)

    # ------------------------------------------------------------ geometry
    def lunge(self):
        return ACTIONS[self.action]["lunge"][self.idx] if self.action else 0

    def sprite_x(self):
        if self.facing > 0:
            return int(round(self.x)) - HIP_X + self.lunge()
        return int(round(self.x)) - (FW - 1 - HIP_X) - self.lunge()

    def tip(self, frame):
        fx, fy = self.game.fist[frame]
        return self.x + self.facing * (fx - HIP_X + self.lunge()), GROUND - SPRITE_FEET + fy

    def current_frame(self):
        if self.pose_override is not None:
            return self.pose_override
        if self.ko:
            return F_KO[0] if self.end_t < 0.12 else (F_KO[1] if self.end_t < 0.45 else F_KO[2])
        if self.won and self.end_t >= 0:
            return F_WIN[0] if self.end_t < 0.12 else F_WIN[1]
        if self.stun_t > 0:
            return F_STAGGER[int(self.stun_el * 7) % len(F_STAGGER)]
        if self.hitstun > 0 and self.react:
            return self.react[0] if self.react_t < self.react_total * 0.55 else self.react[1]
        if self.action:
            return ACTIONS[self.action]["frames"][self.idx]
        if self.block:
            hit_f, frames = (F_BLOCK_HIT_HIGH, F_BLOCK_HIGH) if self.block == "high" else (F_BLOCK_HIT_LOW, F_BLOCK_LOW)
            if self.block_hit_t > 0:
                return hit_f
            return frames[0] if self.block_t < 0.05 else frames[1]
        if self.moving:
            return WALK_BASE + self.walk_i
        return IDLE_SEQ[self.idle_i]

    # ------------------------------------------------------------ update
    def update(self, dt, move, min_x, max_x):
        self.counter_t = max(0.0, self.counter_t - dt)
        self.parry_cd = max(0.0, self.parry_cd - dt)
        self.block_hit_t = max(0.0, self.block_hit_t - dt)
        for g in self.ghosts:
            g["t"] += dt
        self.ghosts = [g for g in self.ghosts if g["t"] < g["life"]]

        # healing: after REGEN_DELAY seconds untouched, heal up to the cap
        self.since_damage += dt
        self.healing = (not self.ko and self.hp > 0 and self.since_damage >= REGEN_DELAY
                        and self.hp < self.regen_cap)
        if self.healing:
            self.hp = min(float(self.regen_cap), self.hp + REGEN_RATE * dt)
        if self.hp_lag > self.hp:
            self.hp_lag = max(self.hp, self.hp_lag - 30 * dt)
        else:
            self.hp_lag = self.hp

        # guard meter
        self.guard_t += dt
        self.block_chain_t -= dt
        if self.block_chain_t <= 0:
            self.block_chain = 0
        if self.guard_t >= GUARD_REGEN_DELAY:
            self.guard = min(float(GUARD_MAX), self.guard + GUARD_REGEN * dt)

        if self.ko or self.won:
            self.end_t += dt
            self.moving = 0
            return
        if self.stun_t > 0:
            self.stun_t -= dt
            self.stun_el += dt
            self.moving = 0
            return
        if self.hitstun > 0:
            self.hitstun -= dt
            self.react_t += dt
            self.moving = 0
            return

        if self.buffer:
            self.buffer_age += dt
            if self.buffer_age > BUFFER_TIME:
                self.buffer = None
            elif self.can_start(self.buffer):
                self.start(self.buffer)

        if self.action and self.want_block and self.idx >= ACTIONS[self.action]["cancel"]:
            self.finish_action()            # cancel punch recovery into a block
        if self.action:
            self.update_action(dt)
            return

        if self.want_block:
            if self.block != self.want_block:
                if self.block is None:
                    self.parry_ready = self.parry_cd <= 0 and self.parry_ok
                    self.parry_cd = PARRY_COOLDOWN
                    self.block_t = 0.0
                else:
                    self.parry_ready = False
                self.block = self.want_block
            self.block_t += dt
            if self.block_t > PARRY_WINDOW:
                self.parry_ready = False
            self.moving = 0
            return
        self.block = None
        self.update_locomotion(dt, move, min_x, max_x)

    def update_action(self, dt):
        spec = ACTIONS[self.action]
        self.t += dt * 1000.0 * self.speed
        while self.action and self.t >= spec["ms"][self.idx]:
            self.t -= spec["ms"][self.idx]
            self.idx += 1
            if self.idx >= len(spec["frames"]):
                self.check_miss(len(spec["frames"]))
                self.finish_action()
                break
            self.check_miss(self.idx)
            if self.action == "slip" and self.idx == 2:
                self.counter_t = COUNTER_WINDOW

    def check_miss(self, new_idx):
        if self.action not in PUNCHES or self.hit_done:
            return
        spec = ACTIONS[self.action]
        prev = spec["frames"][new_idx - 1]
        nxt = spec["frames"][new_idx] if new_idx < len(spec["frames"]) else None
        if prev in spec["active"] and nxt not in spec["active"]:
            self.hit_done = True
            self.game.on_miss(self, prev)

    def update_locomotion(self, dt, move, min_x, max_x):
        moved, fwd = False, True
        if move:
            fwd = move == self.facing
            speed = (WALK_FWD if fwd else WALK_BACK) * self.walk
            if move > 0:      # never pushed backwards by a limit, only stopped by it
                nx = max(self.x, min(self.x + speed * dt, max_x))
            else:
                nx = min(self.x, max(self.x - speed * dt, min_x))
            moved = abs(nx - self.x) > 1e-6
            self.x = nx
        if moved:
            self.moving = 1 if fwd else -1
            self.walk_t += dt * 1000.0
            step = 85.0 if fwd else 95.0
            while self.walk_t >= step:
                self.walk_t -= step
                self.walk_i = (self.walk_i + self.moving) % WALK_FRAMES
        else:
            self.moving = 0
            self.walk_t = 0.0
            self.idle_t += dt * 1000.0
            while self.idle_t >= IDLE_MS:
                self.idle_t -= IDLE_MS
                self.idle_i = (self.idle_i + 1) % len(IDLE_SEQ)

    # ------------------------------------------------------------ drawing
    def draw(self, c):
        sy = GROUND - SPRITE_FEET
        c.blit(self.game.shadow, (int(self.x) - 24 + 3 * self.facing, GROUND - 5))
        for g in self.ghosts:
            g["img"].set_alpha(int(120 * (1 - g["t"] / g["life"])))
            c.blit(g["img"], (g["x"], sy))
        frame, sx = self.current_frame(), self.sprite_x()
        if self.belt:                  # drawn first so the gloves grip it
            top, cx = self.game.frame_top(self.frames, frame)
            b = self.game.belt
            c.blit(b, (sx + cx - b.get_width() // 2, sy + top - 1))
        c.blit(self.frames[frame], (sx, sy))


# ============================================================ the computer's brain
class AI:
    def __init__(self, game, me, foe):
        self.game, self.me, self.foe = game, me, foe
        self.set_level("NORMAL")
        self.reset()

    def set_level(self, name, overrides=None, style=None):
        self.level = name
        self.params = dict(LEVELS[name], **(overrides or {}))
        self.style = dict(style or {})

    def reset(self):
        L = self.params
        self.atk_t = random.uniform(*L["atk"]) + 0.4
        self.plan = []
        self.def_plan = None
        self.seen = -1
        self.move = 0
        self.retreat_t = 0.0
        self.step_t, self.step_dir = 0.0, 0
        self.guard_t, self.guard_level = 0.0, "high"
        self.punish = False
        self.foe_body = []
        self.foe_times = []
        self.clock = 0.0

    def choose_attack(self, L, foe):
        if foe.block and foe.block_t > 0.3 and random.random() < L["flurry"]:
            seq = [random.choice(["jab", "jab", "body_jab"]) for _ in range(random.randint(3, 5))]
            seq.append("body_cross" if foe.block == "high" else "cross")
            return seq
        if random.random() < L["combo"]:
            return random.choice([["jab", "cross"], ["jab", "jab", "cross"], ["jab", "body_cross"],
                                  ["body_jab", "cross"], ["jab", "body_jab", "cross"], ["cross", "body_jab"]])
        if foe.block == "high":
            w = dict(jab=1, cross=0.5, body_jab=3, body_cross=3)
        elif foe.block == "low":
            w = dict(jab=3, cross=3, body_jab=0.5, body_cross=0.3)
        else:
            w = dict(jab=4, cross=2, body_jab=2, body_cross=1.5)
        w = {n: v * self.style.get(n, 1.0) for n, v in w.items()}
        names = list(w)
        return [random.choices(names, weights=[w[n] for n in names])[0]]

    def update(self, dt):
        me, foe, L = self.me, self.foe, self.params
        R = self.game.ranges
        self.move = 0
        self.clock += dt
        if me.busy():
            self.plan.clear()
            self.def_plan = None
            self.guard_t = 0.0
            me.want_block = None
            return
        dist = me.x - foe.x

        # --- notice punches coming in
        if foe.action in PUNCHES and foe.attack_id != self.seen:
            self.seen = foe.attack_id
            target = ACTIONS[foe.action]["target"]
            self.foe_body = (self.foe_body + [target == "body"])[-4:]
            self.foe_times = [t for t in self.foe_times if self.clock - t < 1.2] + [self.clock]
            react = (L["react"] + (0.15 if me.hp < 0.35 * me.max_hp else 0.0)
                     + (0.2 if len(self.foe_times) >= 3 else 0.0))
            if dist <= R[foe.action] + 6 and random.random() < react:
                if target == "head" and random.random() < L["slip"]:
                    kind = "slip"
                else:
                    kind = "high" if target == "head" else "low"
                    if random.random() < L["wrong"]:
                        kind = "low" if kind == "high" else "high"
                if kind != "slip" and random.random() < L["parry"]:
                    wait = max(0.0, time_to_active(foe) - 0.06)
                    me.parry_ok = True
                else:
                    wait = random.uniform(*L["delay"])
                    me.parry_ok = False
                self.def_plan = [kind, wait, 0.4]
                self.plan.clear()

        # --- defend
        blocking = None
        if self.def_plan:
            kind = self.def_plan[0]
            if self.def_plan[1] > 0:
                self.def_plan[1] -= dt
            elif kind == "slip":
                me.press("slip")
                self.def_plan = None
            elif self.punish and not foe.in_startup():
                self.def_plan = None              # punch blocked - drop the guard and punish
            else:
                blocking = kind
                self.def_plan[2] -= dt
                if self.def_plan[2] <= 0 and not (foe.action in PUNCHES and not foe.hit_done):
                    self.def_plan = None
        if blocking is None and self.guard_t > 0:
            self.guard_t -= dt
            if foe.busy() or self.punish:
                self.guard_t = 0.0
            else:
                blocking = self.guard_level
        me.want_block = blocking
        if blocking:
            return

        # --- offence
        if me.counter_t > 0 and not self.plan and dist <= R["cross"]:
            self.plan = [random.choice(["cross", "body_cross", "cross"])]
        if self.punish:
            self.punish = False
            if random.random() < L["punish"] and dist <= R["cross"] + 4:
                self.plan = ["cross"] if random.random() < 0.6 else ["jab", "cross"]
        if foe.stun_t > 0 and not self.plan and dist <= R["cross"]:
            self.plan = random.choice([["cross", "body_cross"], ["jab", "cross", "jab"], ["body_cross", "cross"]])
        self.atk_t -= dt
        if self.atk_t <= 0 and not self.plan and not me.action:
            self.atk_t = random.uniform(*L["atk"]) * (1.4 if me.hp < 0.3 * me.max_hp else 1.0)
            if dist <= R["jab"] + 2:
                self.plan = self.choose_attack(L, foe)
            else:
                self.atk_t *= 0.3
        if self.plan and me.can_start(self.plan[0]):
            me.press(self.plan.pop(0))
            if not self.plan and random.random() < 0.3:
                self.retreat_t = random.uniform(0.25, 0.5)
            return
        if me.action:
            return

        # --- sometimes just sit behind the guard (low guard if you keep going to the body)
        if dist <= R["cross"] + 6 and random.random() < L["guard_up"] * dt * 2:
            self.guard_t = random.uniform(0.5, 1.1)
            self.guard_level = "low" if sum(self.foe_body) >= 2 else "high"

        # --- footwork
        desired = R["jab"] - 6
        if self.retreat_t > 0:
            self.retreat_t -= dt
            self.move = 1
        elif me.hp < 0.3 * me.max_hp and me.hp < me.regen_cap and random.random() < 0.5 * dt:
            self.retreat_t = 1.4                 # back off to try to heal
        elif self.step_t > 0:
            self.step_t -= dt
            self.move = self.step_dir
        elif dist > desired + 3:
            self.move = -1
        elif random.random() < 0.8 * dt:
            self.step_t = random.uniform(0.12, 0.3)
            self.step_dir = random.choice([-1, 1])


# ============================================================ speech bubbles
class Bubble:
    CPS = 38          # characters per second (typewriter)
    HOLD = 1.6        # seconds it stays up after the text finishes

    def __init__(self, game, who, text, min_top=48):
        self.game, self.who, self.text = game, who, text
        self.min_top = min_top          # keep clear of the HUD / banners above
        self.t = 0.0
        self.last = 0
        self.lines = wrap(game.font_s, text, 170)

    def shown(self):
        return min(len(self.text), int(self.t * self.CPS))

    def typed(self):
        return self.shown() >= len(self.text)

    def finished(self):
        return self.t >= len(self.text) / self.CPS + self.HOLD

    def advance(self):
        self.t = len(self.text) / self.CPS if not self.typed() else 1e9

    def update(self, dt):
        self.t += dt
        n = self.shown()
        if n // 3 > self.last // 3 and n < len(self.text):
            self.game.snd("blip")
        self.last = n

    def draw(self, c):
        g, who = self.game, self.who
        font = g.font_s
        lh = 10
        w = max(font.size(l)[0] for l in self.lines) + 10
        h = lh * len(self.lines) + 6
        top, cx = g.frame_top(who.frames, who.current_frame())
        head_x = who.sprite_x() + cx
        bottom = GROUND - SPRITE_FEET + top - (9 if who.belt else 0) - 7
        x = int(clamp(head_x - w // 2, 4, VW - 4 - w))
        y = int(max(bottom - h, self.min_top))
        bottom = y + h
        ol, paper, ink = (24, 14, 34), (250, 248, 240), (34, 26, 48)
        tx = int(clamp(head_x, x + 7, x + w - 7))
        pygame.draw.polygon(c, ol, [(tx - 5, bottom - 1), (tx + 4, bottom - 1), (tx - 1, bottom + 6)])
        c.fill(ol, (x - 1, y, w + 2, h))
        c.fill(ol, (x, y - 1, w, h + 2))
        c.fill(paper, (x, y, w, h))
        pygame.draw.polygon(c, paper, [(tx - 3, bottom - 1), (tx + 2, bottom - 1), (tx - 1, bottom + 3)])
        c.fill((214, 210, 226), (x, y + h - 1, w, 1))
        left = self.shown()
        for i, line in enumerate(self.lines):
            part = line[:max(0, left)]
            left -= len(line) + 1
            if part:
                c.blit(font.render(part, False, ink), (x + 5, y + 3 + i * lh))
        if self.typed() and int(self.t * 3) % 2 == 0:
            c.fill(ink, (x + w - 6, y + h - 4, 3, 2))       # "more" marker


# ============================================================ the game
class Game:
    def __init__(self, sounds=True):
        strip = load_strip(STRIP_B64)
        frames = split(strip)
        self.spar_frames = split(recolor(strip, look_palette(**SPAR_LOOK)), flip=True)
        self.campaign_frames = [split(recolor(strip, look_palette(**o["look"])), flip=True) for o in CAMPAIGN]
        self.belt = make_belt()
        self.belt_small = pygame.transform.scale(self.belt, (18, 7))
        self._tops = {}
        self.fist = {i: fist_point(frames[i]) for i in (6, 14, 15, 29, 34)}
        self.ranges = {}
        for n in PUNCHES:
            spec = ACTIONS[n]
            reach = max(self.fist[fr][0] - HIP_X + spec["lunge"][i]
                        for i, fr in enumerate(spec["frames"]) if fr in spec["active"])
            self.ranges[n] = reach + HURT[spec["target"]] + 3

        self.bg = make_background()
        self.bag = Bag()
        self.canvas = pygame.Surface((VW, VH))
        self.font_s = pygame.font.Font(None, 14)
        self.font_m = pygame.font.Font(None, 18)
        self.font_l = pygame.font.Font(None, 22)
        self.font_xl = pygame.font.Font(None, 28)
        self.font_huge = pygame.font.Font(None, 44)
        self.sounds = make_sounds() if sounds else {}
        self.muted = False
        self.shadow = pygame.Surface((48, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(self.shadow, (14, 10, 24, 90), (0, 0, 48, 8))
        self.bag_shadow = pygame.Surface((40, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(self.bag_shadow, (14, 10, 24, 70), (0, 0, 40, 8))
        sign_w = pygame.font.Font(None, 20).size("BOXING GYM")[0]
        self.button = pygame.Rect(SIGN_POS[0] + sign_w + 6, SIGN_POS[1] - 2, 30, 13)
        cw = self.font_s.size("CAMPAIGN")[0] + 8
        self.campaign_button = pygame.Rect(self.button.right + 3, self.button.y, cw, 13)
        self.hover = None

        self.player = Fighter(self, frames, 1)
        self.cpu = Fighter(self, self.spar_frames, -1)
        self.ai = AI(self, self.cpu, self.player)
        self.clock = 0.0
        self.mode = "bag"
        self.stage = 0
        self.opp = CAMPAIGN[0]
        self.bubble = None
        self.confetti = []
        self.phase, self.phase_t = "intro", 0.0
        self.reset_bag()

    def frame_top(self, frames, i):
        """(top row, x-centre of the top rows) of a frame's opaque pixels - where the gloves/head are."""
        key = (id(frames), i)
        if key not in self._tops:
            f = frames[i]
            rects = pygame.mask.from_surface(f).get_bounding_rects()
            top = min(r.top for r in rects)
            xs = [x for y in range(top, min(FH, top + 5)) for x in range(FW) if f.get_at((x, y)).a > 0]
            self._tops[key] = (top, (min(xs) + max(xs)) // 2)
        return self._tops[key]

    # ------------------------------------------------------------ modes
    def clear_fx(self):
        self.texts, self.parts, self.stars = [], [], []
        self.shake, self.shake_t, self.hitstop, self.flash_t = 0, 0.0, 0.0, 0.0
        self.combo, self.combo_t = 0, 0.0

    def reset_bag(self):
        self.mode = "bag"
        self.bag.reset()
        self.player.reset(72)
        self.damage, self.best = 0, 0
        self.clear_fx()

    def start_spar(self):
        self.mode = "spar"
        self.cpu.frames = self.spar_frames
        self.cpu.configure()
        self.ai.set_level(self.ai.level if self.ai.level in LEVELS else "NORMAL")
        self.player.reset(96)
        self.cpu.reset(224)
        self.ai.reset()
        self.phase, self.phase_t = "intro", 0.0
        self.round_time = float(ROUND_TIME)
        self.result = None
        self.end_reason = None
        self.bubble = None
        self.best = 0
        self.clear_fx()
        self.snd("bell")

    # ------------------------------------------------------------ campaign
    def start_campaign(self):
        self.mode = "campaign"
        self.stage = 0
        self.begin_stage()

    def begin_stage(self):
        o = self.opp = CAMPAIGN[self.stage]
        p, c = self.player, self.cpu
        c.frames = self.campaign_frames[self.stage]
        c.configure(o["hp"], o["power"], o["speed"], o["walk"])
        p.reset(96)
        c.reset(372)                       # off screen - walks in
        self.ai.set_level(o["level"], o.get("ai"), o.get("style"))
        self.ai.reset()
        self.phase, self.phase_t = "walkin", 0.0
        self.round_time = float(ROUND_TIME)
        self.result = None
        self.end_reason = None
        self.bubble = None
        self.confetti = []
        self.step = 0
        self.taunt_i = -1
        self.ghost_t = 0.0
        self.fw_t = 0.0
        self.best = 0
        self.clear_fx()

    def taunt_frame(self, kind, t):
        seq, ms = TAUNTS[kind]
        i = int(t * 1000 / ms) % len(seq)
        return seq[i], i

    def update_campaign(self, dt, move, want):
        p, c, o = self.player, self.cpu, self.opp
        if self.bubble:
            self.bubble.update(dt)
        if self.phase in ("intro", "fight", "ko"):
            self.update_spar(dt, move, want)
            if self.phase == "result":
                self.after_fight()
            return
        self.phase_t += dt
        p.want_block = c.want_block = None
        ph = self.phase

        if ph == "walkin":
            c.walk = 1.6 * o["walk"]
            c.update(dt, -1, p.x + MIN_SEP, 400)
            c.walk = o["walk"]
            if c.x <= 224:
                c.x, c.moving = 224.0, 0
                self.phase, self.phase_t = "talk", 0.0
                self.bubble = Bubble(self, c, o["intro"])
                if o.get("champ"):
                    self.snd("crowd")
        elif ph == "talk":
            c.pose_override, i = self.taunt_frame(o["taunt"], self.phase_t)
            c.belt = bool(o.get("champ"))
            if o["taunt"] == "roar" and i == 3 and self.taunt_i != 3:
                self.shake, self.shake_t = 2, 0.2              # the Bulldozer shakes the room
            if o["taunt"] == "weave":
                self.ghost_t -= dt
                if self.ghost_t <= 0:
                    self.ghost_t = 0.09
                    c.ghosts.append(c.make_ghost(c.pose_override))
            if o["taunt"] == "belt" and random.random() < dt * 14:
                top, cx = self.frame_top(c.frames, c.pose_override)
                self.parts.append([c.sprite_x() + cx + random.uniform(-16, 16), GROUND - SPRITE_FEET + top + 4,
                                   random.uniform(-10, 10), random.uniform(-60, -20), random.uniform(0.2, 0.45),
                                   random.choice([(255, 244, 168), (255, 255, 255)])])
            self.taunt_i = i
            if self.bubble.finished():
                c.pose_override, c.belt = None, False
                self.phase, self.phase_t = "reply", 0.0
                self.bubble = Bubble(self, p, o["reply"])
        elif ph == "reply":
            p.pose_override, _ = self.taunt_frame("reply", self.phase_t)
            if self.bubble.finished():
                p.pose_override = None
                self.bubble = None
                self.phase, self.phase_t = "intro", 0.0
                self.snd("bell")
        elif ph == "victory":
            if self.bubble and self.bubble.finished():
                self.bubble = None
        elif ph == "defeat":
            if self.step == 0 and self.phase_t > 0.6:
                self.bubble = Bubble(self, c, o["win"])
                self.step = 1
            elif self.step == 1 and self.bubble.finished():
                self.bubble = Bubble(self, p, random.choice(LOSE_LINES), min_top=66)
                self.step = 2
            elif self.step == 2 and self.bubble.finished():
                self.bubble = None
                self.step = 3
        elif ph == "champion":
            p.pose_override, _ = self.taunt_frame("champ", self.phase_t)
            p.belt = True
            n = 70 * dt
            for _ in range(int(n) + (1 if random.random() < n % 1 else 0)):
                self.confetti.append([random.uniform(0, VW), -4.0, random.uniform(-12, 12), random.uniform(22, 42),
                                      random.choice(CONFETTI), random.uniform(0, 6.3)])
            for k in self.confetti:
                k[0] += k[2] * dt + math.sin(k[5]) * 0.3
                k[1] += k[3] * dt
                k[5] += dt * 6
            self.confetti = [k for k in self.confetti if k[1] < GROUND + 8]
            self.fw_t -= dt
            if self.fw_t <= 0:
                self.fw_t = random.uniform(0.35, 0.8)
                self.firework(random.uniform(30, VW - 30), random.uniform(48, 88))
            if self.step == 0 and self.phase_t > 1.0:
                self.bubble = Bubble(self, p, "WHO'S THE CHAMP NOW?!", min_top=58)
                self.step = 1
            elif self.step == 1 and self.bubble.finished():
                self.bubble = None
                self.step = 2
            if int(self.phase_t / 3.0) != int((self.phase_t - dt) / 3.0):
                self.snd("crowd")
        # keep everyone breathing / kneeling / celebrating
        p.update(dt, 0, MIN_X, c.x - MIN_SEP)
        if ph != "walkin":
            c.update(dt, 0, p.x + MIN_SEP, STAGE_MAX_X)

    def after_fight(self):
        p, c = self.player, self.cpu
        self.phase_t, self.step = 0.0, 0
        self.bubble = None
        if self.result == "YOU WIN!":
            if self.stage == len(CAMPAIGN) - 1:
                self.phase = "champion"
                p.won, p.end_t = True, max(p.end_t, 0.0)
                self.confetti = []
                self.snd("fanfare")
                self.snd("crowd")
            else:
                self.phase = "victory"
                self.bubble = Bubble(self, c, self.opp["lose"], min_top=80)
        else:
            self.phase = "defeat"
            if not c.won:
                c.won, c.end_t = True, 0.0
            if not p.ko:
                p.ko, p.end_t = True, 0.6
            self.snd("sad")

    def firework(self, x, y):
        col = random.choice(CONFETTI)
        for k in range(26):
            a = k * math.pi * 2 / 26 + random.uniform(-0.1, 0.1)
            sp = random.uniform(55, 95)
            self.parts.append([x, y, math.cos(a) * sp, math.sin(a) * sp - 50, random.uniform(0.45, 0.8),
                               col if k % 3 else (255, 255, 255)])
        self.stars.append(dict(x=x, y=y, t=0.0, life=0.14, big=False, kind="hit"))

    # ------------------------------------------------------------ mode switching
    def toggle_mode(self):
        if self.mode == "bag":
            self.start_spar()
        else:
            self.reset_bag()

    def reset(self):
        if self.mode == "bag":
            self.reset_bag()
        elif self.mode == "spar":
            self.start_spar()
        else:
            self.start_campaign()

    def set_level(self, name):
        if self.mode == "campaign":
            return
        self.ai.set_level(name)
        if self.mode == "spar":
            self.start_spar()

    def confirm(self):
        if self.mode == "spar" and self.phase == "result":
            self.start_spar()
        elif self.mode == "campaign":
            ph = self.phase
            if ph in ("talk", "reply") and self.bubble:
                self.bubble.advance()
            elif ph == "victory" and self.phase_t > 0.5:
                self.stage += 1
                self.begin_stage()
            elif ph == "defeat":
                if self.step < 3 and self.bubble:
                    self.bubble.advance()
                elif self.step >= 3 or self.phase_t > 0.6:
                    self.start_campaign()             # lose = back to fight 1
            elif ph == "champion" and self.phase_t > 1.5:
                self.start_campaign()

    def mouse(self, x, y, click):
        self.hover = None
        if self.button.collidepoint(x, y):
            self.hover = "main"
        elif self.mode == "bag" and self.campaign_button.collidepoint(x, y):
            self.hover = "campaign"
        if click and self.hover == "main":
            self.toggle_mode()
        elif click and self.hover == "campaign":
            self.start_campaign()

    # ------------------------------------------------------------ input
    def press(self, name):
        if self.mode != "bag" and self.phase != "fight":
            return
        self.player.press(name)

    def snd(self, name):
        s = self.sounds.get(name)
        if s and not self.muted:
            s.play()

    def toggle_mute(self):
        self.muted = not self.muted

    def say(self, s, x, y, color, font=None, vy=-22, life=0.8):
        self.texts.append(dict(s=s, x=x, y=y, vy=vy, t=0.0, life=life, color=color, font=font or self.font_m))

    def on_miss(self, f, frame):
        wx, wy = f.tip(frame)
        self.say("miss", wx - 8, wy - 8, (150, 156, 182), self.font_s, vy=-14, life=0.6)
        if f is self.player and self.mode != "bag":
            self.ai.punish = True

    # ------------------------------------------------------------ update
    def update(self, dt, left=False, right=False, down=False, block=False):
        self.clock += dt
        self.update_fx(dt)
        if self.hitstop > 0:
            self.hitstop -= dt
            return
        self.combo_t -= dt
        if self.combo_t <= 0:
            self.combo = 0
        move = (1 if right else 0) - (1 if left else 0)
        want = ("low" if down else "high") if block else None
        if self.mode == "bag":
            self.bag.update(dt)
            self.player.want_block = want
            limit = max(MAX_X, self.bag.x_at(BAG_TOP + BAG_H / 2) - (BAG_X - MAX_X))
            self.player.update(dt, move, MIN_X, limit)
            self.check_bag_hit()
        elif self.mode == "campaign":
            self.update_campaign(dt, move, want)
        else:
            self.update_spar(dt, move, want)

    def update_spar(self, dt, move, want):
        p, c = self.player, self.cpu
        self.phase_t += dt
        if self.phase == "fight":
            self.round_time -= dt
            p.want_block = want
            self.ai.update(dt)
            p.update(dt, move, MIN_X, c.x - MIN_SEP)
            c.update(dt, self.ai.move, p.x + MIN_SEP, STAGE_MAX_X)
            self.resolve(p, c)
            self.resolve(c, p)
            self.separate()
            for f in (p, c):
                if f.healing and random.random() < dt * 3:
                    self.say("+", f.x + random.uniform(-8, 8), GROUND - 74, (120, 240, 140), self.font_m,
                             vy=-16, life=0.6)
            if self.round_time <= 0 and self.phase == "fight":
                self.round_time = 0.0
                self.end_fight(by_time=True)
        else:
            p.want_block = c.want_block = None
            p.update(dt, 0, MIN_X, c.x - MIN_SEP)
            c.update(dt, 0, p.x + MIN_SEP, STAGE_MAX_X)
            if self.phase == "intro" and self.phase_t > 1.8:
                self.phase, self.phase_t = "fight", 0.0
            elif self.phase == "ko" and self.phase_t > 1.6:
                self.phase, self.phase_t = "result", 0.0

    def end_fight(self, by_time=False, loser=None):
        p, c = self.player, self.cpu
        if by_time:
            pr, cr = p.hp / p.max_hp, c.hp / c.max_hp          # decision on % of health left
            if abs(pr - cr) < 0.005:
                self.result = "DRAW"
            else:
                self.result = "YOU WIN!" if pr > cr else "YOU LOSE"
                winner = p if pr > cr else c
                winner.won, winner.end_t = True, 0.0
            self.end_reason = "time"
            if self.mode == "campaign":
                self.phase, self.phase_t = "ko", 0.0
            else:
                self.phase, self.phase_t = "result", 0.0
                self.say("TIME!", VW // 2 - 22, 70, (255, 232, 130), self.font_xl, vy=0, life=1.5)
        else:
            self.end_reason = "ko"
            winner = c if loser is p else p
            winner.won, winner.end_t = True, -0.9
            self.result = "YOU WIN!" if loser is c else "YOU LOSE"
            self.phase, self.phase_t = "ko", 0.0
        self.snd("bell")

    def separate(self):
        p, c = self.player, self.cpu
        gap = c.x - p.x
        if gap < MIN_SEP:
            need = MIN_SEP - gap
            room_p, room_c = p.x - MIN_X, STAGE_MAX_X - c.x
            mp = min(room_p, need / 2)
            mc = min(room_c, need - mp)
            mp = min(room_p, need - mc)
            p.x -= mp
            c.x += mc

    # ------------------------------------------------------------ sparring hits
    def resolve(self, att, d):
        if att.action not in PUNCHES or att.hit_done or d.ko:
            return
        spec = ACTIONS[att.action]
        frame = spec["frames"][att.idx]
        if frame not in spec["active"]:
            return
        target = spec["target"]
        reach = self.fist[frame][0] - HIP_X + att.lunge()
        dist = (d.x - att.x) * att.facing
        if dist <= 0 or reach + HURT[target] + 3 < dist:
            return                                    # not there yet - "miss" if it never gets there
        hx = d.x + d.facing * HURT[target]
        hy = GROUND - SPRITE_FEET + TARGET_Y[target]
        if target == "head" and d.slipping():
            att.hit_done = True
            d.counter_t = COUNTER_WINDOW
            self.say("SLIP!", hx - 12, hy - 18, (120, 220, 255), self.font_m, vy=-18, life=0.7)
            return
        att.hit_done = True
        blocked = d.block is not None and ((d.block == "high") == (target == "head"))
        if blocked:
            self.blocked(att, d, spec, hx, hy)
        else:
            self.clean_hit(att, d, spec, target, hx, hy)

    def blocked(self, att, d, spec, hx, hy):
        if d.parry_ready and d.block_t <= PARRY_WINDOW:
            d.parry_ready = False
            att.stagger(PARRY_STUN)
            d.counter_t = COUNTER_WINDOW
            self.stars.append(dict(x=hx, y=hy, t=0.0, life=0.28, big=True, kind="parry"))
            self.say("PARRY!", hx - 20, hy - 26, (130, 240, 255), self.font_l, vy=-20, life=0.9)
            self.hitstop = 0.09
            self.snd("parry")
            return
        d.guard -= spec["guard"] * (1 + FLURRY_RAMP * d.block_chain)
        d.block_chain += 1
        d.block_chain_t = FLURRY_WINDOW
        d.guard_t = 0.0
        d.block_hit_t = 0.12
        d.push(1.5)
        self.stars.append(dict(x=hx, y=hy, t=0.0, life=0.12, big=False, kind="block"))
        self.hitstop = 0.03
        self.snd("block")
        if d is self.cpu:
            self.ai.punish = True          # fire back while the attacker recovers
        if d.guard <= 0:
            d.guard = 0.0
            d.stagger(GUARD_BREAK_STUN)
            self.say("GUARD BREAK!", hx - 34, hy - 30, (255, 150, 90), self.font_l, vy=-16, life=1.1)
            self.shake, self.shake_t = 3, 0.18
            self.snd("guard_break")

    def clean_hit(self, att, d, spec, target, hx, hy):
        mult, chance, tags = 1.0, CRIT_CHANCE, []
        crit = d.stun_t > 0                       # hitting a stunned boxer is always critical
        if d.in_startup():
            mult *= COUNTER_HIT_MULT
            chance += 0.12
            tags.append(("COUNTER HIT", (255, 200, 90)))
        if att.is_counter:
            mult *= COUNTER_MULT
            chance += 0.2
            tags.append(("COUNTER!", (120, 220, 255)))
        crit = crit or random.random() < chance
        if crit:
            mult *= CRIT_MULT
        dmg = max(1, int(round(spec["spar_dmg"] * mult * att.power)))
        d.hp = max(0.0, d.hp - dmg)
        d.since_damage = 0.0
        if target == "body":
            scale = d.max_hp / MAX_HP
            d.regen_cap = max(REGEN_CAP_MIN * scale, d.regen_cap - BODY_CAP_LOSS * scale)
        d.get_hit(target, spec["stun"] + (0.25 if crit else 0.0))
        d.push(12 if crit else (7 if spec["guard"] > 20 else 4))
        if d is self.player:
            self.combo, self.combo_t = 0, 0.0
        else:
            self.combo += 1
            self.combo_t = 1.0
            self.best = max(self.best, self.combo)

        big = crit or spec["guard"] > 20
        self.stars.append(dict(x=hx, y=hy, t=0.0, life=0.2 if crit else 0.16, big=big, kind="crit" if crit else "hit"))
        for _ in range(18 if crit else (12 if big else 7)):
            a = random.uniform(-1.2, 1.2) + (0 if d.facing < 0 else math.pi)
            sp = random.uniform(40, 170 if crit else 110)
            self.parts.append([hx, hy, math.cos(a) * sp, math.sin(a) * sp - 30, random.uniform(0.18, 0.4),
                               random.choice([(255, 226, 120), (255, 255, 255), (255, 140, 100)])])
        col = (255, 232, 130) if not crit else (255, 110, 70)
        self.say(str(dmg), hx - 6, hy - 14, col, self.font_xl if crit else self.font_l, vy=-26)
        y = hy - 30
        if crit:
            self.say("CRITICAL!", hx - 28, y, (255, 120, 60), self.font_l, vy=-20, life=1.0)
            y -= 13
            self.flash_t = 0.08
        for s, c in tags:
            self.say(s, hx - 26, y, c, self.font_m, vy=-18, life=0.9)
            y -= 12
        self.hitstop = 0.12 if crit else spec["stop"]
        self.shake = 4 if crit else spec["shake"]
        self.shake_t = 0.18 if crit else 0.12
        self.snd("crit" if crit else ("hit_cross" if big else "hit_jab"))
        if d.hp <= 0:
            d.ko, d.end_t = True, 0.0
            d.hitstun = 0.0
            self.hitstop = 0.25
            self.end_fight(loser=d)

    # ------------------------------------------------------------ bag hits
    def check_bag_hit(self):
        p = self.player
        if p.action not in PUNCHES or p.hit_done:
            return
        spec = ACTIONS[p.action]
        frame = spec["frames"][p.idx]
        if frame not in spec["active"]:
            return
        wx, wy = p.tip(frame)
        top, bottom = self.bag.top_bottom()
        if not (top - 2 <= wy <= bottom + 2):
            return
        bx = self.bag.x_at(wy)
        if bx - BAG_HALF - REACH_SLACK <= wx <= bx + BAG_HALF:
            self.bag_connect(p.action, spec, wx, wy, bx)

    def bag_connect(self, name, spec, wx, wy, bx):
        p = self.player
        p.hit_done = True
        counter = p.is_counter
        self.combo += 1
        self.combo_t = 1.4
        self.best = max(self.best, self.combo)
        mult = COUNTER_MULT if counter else 1.0
        dmg = int(spec["dmg"] * mult * (1 + 0.08 * min(self.combo - 1, 10)))
        self.damage += dmg

        self.bag.kick(spec["kick"] * (1.35 if counter else 1.0))
        self.bag.flash = 0.07
        self.hitstop = spec["stop"]
        self.shake = int(spec["shake"] * (1.3 if counter else 1.0))
        self.shake_t = 0.12

        px, py = min(wx, bx - BAG_HALF + 3), wy
        big = spec["guard"] > 20 or counter
        self.stars.append(dict(x=px, y=py, t=0.0, life=0.16, big=big, kind="hit"))
        for _ in range(14 if big else 8):
            a = random.uniform(-1.2, 1.2) + math.pi
            sp = random.uniform(40, 150 if big else 100)
            self.parts.append([px, py, math.cos(a) * sp, math.sin(a) * sp - 30, random.uniform(0.18, 0.4),
                               random.choice([(255, 226, 120), (255, 255, 255), (255, 140, 100)])])
        self.say(str(dmg), px - 6, py - 12, (255, 232, 130) if not big else (255, 150, 110), self.font_l, vy=-26)
        if counter:
            self.say("COUNTER!", px - 20, py - 28, (120, 220, 255), self.font_m, vy=-18, life=0.9)
        self.snd("hit_cross" if big else "hit_jab")

    # ------------------------------------------------------------ effects
    def update_fx(self, dt):
        for t in self.texts:
            t["t"] += dt
            t["y"] += t["vy"] * dt
        self.texts = [t for t in self.texts if t["t"] < t["life"]]
        for p in self.parts:
            p[4] -= dt
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[3] += 260 * dt
        self.parts = [p for p in self.parts if p[4] > 0]
        for s in self.stars:
            s["t"] += dt
        self.stars = [s for s in self.stars if s["t"] < s["life"]]
        if self.shake_t > 0:
            self.shake_t -= dt
        self.flash_t = max(0.0, self.flash_t - dt)

    # ------------------------------------------------------------ drawing
    def draw(self, out):
        c = self.canvas
        c.blit(self.bg, (0, 0))
        p = self.player
        champ = self.mode == "campaign" and self.phase == "champion"
        if champ:
            self.draw_spotlight(c, p.x + 4)
        if self.mode == "bag":
            c.blit(self.bag_shadow, (int(self.bag.bottom_x()) - 20, GROUND - 4))
            self.bag.draw(c)
            p.draw(c)
            if p.counter_t > 0 and int(p.counter_t * 14) % 2 == 0:
                draw_text(c, self.font_s, "COUNTER READY", p.x + 6, GROUND - 96, (120, 220, 255), center=True)
        else:
            cpu = self.cpu
            order = [cpu, p] if not (cpu.action in PUNCHES and p.action not in PUNCHES) else [p, cpu]
            for f in order:
                f.draw(c)
            if p.counter_t > 0 and int(p.counter_t * 14) % 2 == 0 and self.phase == "fight":
                draw_text(c, self.font_s, "COUNTER READY", p.x + 6, GROUND - 96, (120, 220, 255), center=True)
        if self.mode == "campaign" and self.phase == "defeat":
            self.draw_defeat_mood(c)

        for s in self.stars:
            self.draw_star(c, s)
        for x, y, _, _, life, col in self.parts:
            sz = 2 if life > 0.2 else 1
            c.fill(col, (int(x), int(y), sz, sz))
        for t in self.texts:
            if t["t"] > t["life"] * 0.7 and int(t["t"] * 30) % 2:
                continue
            draw_text(c, t["font"], t["s"], t["x"], t["y"], t["color"])
        for x, y, _, _, col, ph in self.confetti:
            c.fill(col, (int(x), int(y), 2, 1) if math.sin(ph) > 0 else (int(x), int(y), 1, 2))
        if self.bubble:
            self.bubble.draw(c)

        if self.mode == "bag":
            self.draw_bag_hud(c)
        else:
            self.draw_spar_hud(c)
        self.draw_button(c)
        self.draw_controls(c)

        if self.flash_t > 0:
            fl = pygame.Surface((VW, VH), pygame.SRCALPHA)
            fl.fill((255, 255, 255, int(110 * self.flash_t / 0.08)))
            c.blit(fl, (0, 0))

        out.fill((20, 16, 28))
        ox = oy = 0
        if self.shake_t > 0 and self.shake > 0:
            ox = random.randint(-self.shake, self.shake)
            oy = random.randint(-self.shake, self.shake)
        out.blit(c, (ox, oy))

    def draw_star(self, c, s):
        k = s["t"] / s["life"]
        kind = s["kind"]
        if kind == "parry":
            r = int(4 + 16 * k)
            pygame.draw.circle(c, (130, 240, 255), (int(s["x"]), int(s["y"])), r, 1)
            pygame.draw.circle(c, (255, 255, 255), (int(s["x"]), int(s["y"])), max(1, r - 4), 1)
            return
        scale = {"hit": 1.0, "crit": 1.8, "block": 0.7}[kind] * (1.4 if s["big"] and kind == "hit" else 1.0)
        c1, c2 = ((176, 208, 236), (255, 255, 255)) if kind == "block" else ((255, 244, 168), (255, 255, 255))
        if kind == "crit":
            c1 = (255, 150, 90)
        inner = 2 + 3 * k
        outer = (7 + 8 * k) * scale * (1.0 - 0.4 * k)
        for i in range(8):
            a = i * math.pi / 4 + 0.3
            r0 = inner if i % 2 == 0 else inner + 1
            r1 = outer if i % 2 == 0 else outer * 0.62
            pygame.draw.line(c, c1 if i % 2 == 0 else c2, (s["x"] + math.cos(a) * r0, s["y"] + math.sin(a) * r0),
                             (s["x"] + math.cos(a) * r1, s["y"] + math.sin(a) * r1))
        if kind != "block":
            r = max(1, int((3.5 - 3 * k) * scale))
            pygame.draw.circle(c, (255, 226, 120), (int(s["x"]), int(s["y"])), r)
            pygame.draw.circle(c, (255, 255, 255), (int(s["x"]), int(s["y"])), max(1, r - 2))

    def draw_button(self, c):
        def button(r, label, hover, face, face_hi, top, bottom, shadow):
            pygame.draw.rect(c, (20, 14, 30), r.inflate(2, 2))
            pygame.draw.rect(c, face_hi if hover else face, r)
            c.fill(top, (r.x, r.y, r.w, 1))
            c.fill(bottom, (r.x, r.bottom - 1, r.w, 1))
            draw_text(c, self.font_s, label, r.centerx, r.y + 3, (255, 255, 255), shadow=shadow, center=True)

        button(self.button, "SPAR" if self.mode == "bag" else "BAG", self.hover == "main",
               (206, 66, 122), (255, 120, 170), (255, 190, 214), (120, 28, 72), (110, 24, 64))
        if self.mode == "bag":
            button(self.campaign_button, "CAMPAIGN", self.hover == "campaign",
                   (196, 140, 30), (240, 186, 60), (255, 226, 140), (120, 80, 16), (100, 62, 10))

    def draw_spotlight(self, c, x):
        glow = pygame.Surface((VW, VH), pygame.SRCALPHA)
        sway = math.sin(self.clock * 1.7) * 6
        pygame.draw.polygon(glow, (255, 236, 170, 34), [(x - 8 + sway, 0), (x + 8 + sway, 0), (x + 44, GROUND + 4),
                                                         (x - 44, GROUND + 4)])
        pygame.draw.ellipse(glow, (255, 236, 170, 46), (x - 46, GROUND - 6, 92, 14))
        c.blit(glow, (0, 0))

    def draw_defeat_mood(self, c):
        a = int(min(1.0, self.phase_t / 0.8) * 110)
        dim = pygame.Surface((VW, VH), pygame.SRCALPHA)
        dim.fill((8, 6, 24, a))
        c.blit(dim, (0, 0))
        if self.phase_t < 0.5:
            return
        p = self.player                               # a little rain cloud over the loser
        cx, cy = int(p.x) + 8, GROUND - SPRITE_FEET + 14
        for x in range(-10, 11, 2):
            for k in range(3):
                yy = cy + 4 + ((self.clock * 70 + x * 7 + k * 9) % 22)
                c.fill((120, 150, 210), (cx + x + (k % 2), int(yy), 1, 2))
        for (dx, dy, r) in ((-7, 1, 5), (0, -2, 7), (7, 1, 5), (-2, 2, 6), (4, 2, 6)):
            pygame.draw.circle(c, (40, 40, 58), (cx + dx, cy + dy), r + 1)
        for (dx, dy, r) in ((-7, 1, 5), (0, -2, 7), (7, 1, 5), (-2, 2, 6), (4, 2, 6)):
            pygame.draw.circle(c, (104, 108, 132), (cx + dx, cy + dy), r)
        pygame.draw.circle(c, (140, 144, 168), (cx - 2, cy - 4), 3)

    def draw_name_card(self, c):
        o = self.opp
        k = clamp(1 - self.phase_t / 0.35, 0.0, 1.0)
        off = int(k * k * VW)
        y, h = 50, 44
        band = pygame.Surface((VW, h), pygame.SRCALPHA)
        band.fill((10, 8, 20, 190))
        c.blit(band, (off, y))
        edge = (255, 214, 90) if o.get("champ") else o["color"]
        c.fill(edge, (off, y, VW, 1))
        c.fill(edge, (off, y + h - 1, VW, 1))
        draw_text(c, self.font_s, "FIGHT %d OF %d" % (self.stage + 1, len(CAMPAIGN)), 12 + off, y + 4, (170, 180, 215))
        draw_text(c, self.font_l, o["name"], 12 + off, y + 14, o["color"])
        draw_text(c, self.font_s, o["title"], 12 + off, y + 31, (255, 214, 90) if o.get("champ") else (230, 232, 250))
        if o.get("champ"):
            c.blit(self.belt, (VW - 50 + off, y + 15))

    def draw_controls(self, c):
        bar = pygame.Surface((VW, 22), pygame.SRCALPHA)
        bar.fill((10, 8, 20, 175))
        c.blit(bar, (0, VH - 22))
        col = (200, 206, 232)
        draw_text(c, self.font_s, "ARROWS MOVE   A JAB   S CROSS   D BODY JAB   F BODY CROSS",
                  VW // 2, VH - 20, col, center=True)
        mode = "SPAR" if self.mode == "bag" else "BAG"
        draw_text(c, self.font_s, "W SLIP   E BLOCK   R LOW BLOCK   BKSP RESET   TAB " + mode,
                  VW // 2, VH - 11, col, center=True)

    def draw_bag_hud(self, c):
        label, gold = (170, 180, 215), (255, 232, 130)
        draw_text(c, self.font_s, "DAMAGE", 8, 13, label)
        draw_text(c, self.font_l, "%06d" % self.damage, 8, 22, gold)
        val = "x%d" % self.best                       # one line, below the mode buttons
        draw_text(c, self.font_m, val, VW - 8, 31, gold, right=True)
        draw_text(c, self.font_s, "BEST COMBO", VW - 12 - self.font_m.size(val)[0], 33, label, right=True)
        if self.combo >= 2:
            draw_text(c, self.font_xl, "%d HIT COMBO!" % self.combo, VW // 2, 64, (255, 120, 100), center=True)

    def draw_bar(self, c, x, y, w, f, mirror):
        h = 6

        def seg(v0, v1, col, yy=y, hh=h):
            a, b = int(round(w * v0)), int(round(w * v1))
            if b <= a:
                return
            c.fill(col, ((x + w - b) if mirror else (x + a), yy, b - a, hh))

        pygame.draw.rect(c, (20, 14, 30), (x - 1, y - 1, w + 2, h + 2))
        c.fill((52, 40, 62), (x, y, w, h))
        hp, lag = f.hp / f.max_hp, f.hp_lag / f.max_hp
        seg(hp, lag, (255, 255, 255))
        col = (90, 220, 110) if hp > 0.5 else ((240, 210, 70) if hp > 0.25 else (236, 70, 60))
        if f.healing and int(self.clock * 8) % 2:
            col = (160, 255, 170)
        seg(0, hp, col)
        seg(0, hp, tuple(min(255, v + 50) for v in col), y, 1)
        cap = f.regen_cap / f.max_hp
        tx = x + (w - int(round(w * cap)) if mirror else int(round(w * cap)))
        c.fill((236, 240, 255), (tx, y - 2, 1, h + 4))
        gy = y + h + 3
        pygame.draw.rect(c, (20, 14, 30), (x - 1, gy - 1, w + 2, 5))
        c.fill((40, 40, 64), (x, gy, w, 3))
        gcol = (90, 170, 255) if f.guard > 30 else ((255, 120, 90) if int(self.clock * 8) % 2 else (200, 80, 60))
        seg(0, f.guard / GUARD_MAX, gcol, gy, 3)

    def draw_spar_hud(self, c):
        label = (170, 180, 215)
        camp = self.mode == "campaign"
        draw_text(c, self.font_s, "YOU", 8, 13, label)
        name = self.opp["short"] if camp else "CPU  " + self.ai.level
        draw_text(c, self.font_s, name, VW - 8, 13, self.opp["color"] if camp else label, right=True)
        if camp and self.opp.get("champ"):
            c.blit(self.belt_small, (VW - 8 - self.font_s.size(name)[0] - 21, 13))
        self.draw_bar(c, 8, 24, 76, self.player, False)
        self.draw_bar(c, VW - 8 - 76, 24, 76, self.cpu, True)
        secs = int(math.ceil(self.round_time))
        tcol = (255, 232, 130) if secs > 10 or int(self.clock * 4) % 2 else (255, 90, 80)
        draw_text(c, self.font_l, "%02d" % secs, VW // 2, 32, tcol, center=True)
        if camp:
            draw_text(c, self.font_s, "FIGHT %d/%d" % (self.stage + 1, len(CAMPAIGN)), VW // 2 - 14, 36, label,
                      right=True)
        if self.combo >= 2 and self.phase == "fight":
            draw_text(c, self.font_xl, "%d HIT COMBO!" % self.combo, VW // 2, 64, (255, 120, 100), center=True)

        gold, white = (255, 214, 90), (230, 232, 250)
        if self.phase == "intro":
            self.banner(c, 50, 44)
            msg = "ROUND 1" if self.phase_t < 0.9 else "FIGHT!"
            draw_text(c, self.font_huge, msg, VW // 2, 54, (255, 232, 130), center=True)
            sub = ("FIGHT %d OF %d" % (self.stage + 1, len(CAMPAIGN))) if camp else "1 EASY   2 NORMAL   3 HARD"
            draw_text(c, self.font_s, sub, VW // 2, 83, label, center=True)
        elif self.phase == "ko":
            msg = "TIME!" if self.end_reason == "time" else "K.O.!"
            draw_text(c, self.font_huge, msg, VW // 2, 58, (255, 90, 80), center=True)
        elif self.phase == "walkin":
            self.draw_name_card(c)
        elif self.phase == "victory":
            self.banner(c, 40, 36)
            draw_text(c, self.font_xl, "VICTORY!", VW // 2, 43, (120, 240, 140), center=True)
            nxt = CAMPAIGN[self.stage + 1]
            draw_text(c, self.font_s, "%d OF %d DOWN   -   NEXT UP: %s" % (self.stage + 1, len(CAMPAIGN), nxt["short"]),
                      VW // 2, 63, white, center=True)
            if int(self.clock * 2.5) % 2 == 0:
                draw_text(c, self.font_s, "PRESS ENTER FOR THE NEXT FIGHT", VW // 2, 66 + 10, gold, center=True)
        elif self.phase == "defeat" and self.step >= 2:
            self.banner(c, 36, 28)
            draw_text(c, self.font_l, "DEFEATED", VW // 2, 38, (255, 90, 80), center=True)
            draw_text(c, self.font_s, "ENTER  TRY AGAIN FROM FIGHT 1        TAB  BACK TO BAG", VW // 2, 52, white,
                      center=True)
        elif self.phase == "champion":
            pulse = (255, 214, 90) if int(self.clock * 4) % 2 else (255, 250, 200)
            draw_text(c, self.font_l, "NEW LIGHTWEIGHT CHAMPION!", VW // 2, 40, pulse, center=True)
            if self.phase_t > 1.5 and self.step >= 2:
                draw_text(c, self.font_s, "ENTER  DEFEND YOUR TITLE (NEW CAMPAIGN)        TAB  BAG", VW // 2, 58,
                          white, center=True)
        elif self.phase == "result":
            self.banner(c, 46, 56)
            col = (120, 240, 140) if self.result == "YOU WIN!" else ((255, 232, 130) if self.result == "DRAW" else (255, 90, 80))
            draw_text(c, self.font_huge, self.result, VW // 2, 49, col, center=True)
            draw_text(c, self.font_m, "ENTER  REMATCH        TAB  BACK TO BAG", VW // 2, 78, (230, 232, 250), center=True)
            draw_text(c, self.font_s, "1 EASY   2 NORMAL   3 HARD", VW // 2, 91, label, center=True)

    def banner(self, c, y, h):
        band = pygame.Surface((VW, h), pygame.SRCALPHA)
        band.fill((10, 8, 20, 160))
        c.blit(band, (0, y))
        c.fill((255, 110, 160), (0, y, VW, 1))
        c.fill((255, 110, 160), (0, y + h - 1, VW, 1))


# ============================================================ window / main loop
def present(screen, canvas):
    sw, sh = screen.get_size()
    s = max(1, min(sw // VW, sh // VH))
    big = pygame.transform.scale(canvas, (VW * s, VH * s))
    ox, oy = (sw - VW * s) // 2, (sh - VH * s) // 2
    screen.fill((0, 0, 0))
    screen.blit(big, (ox, oy))
    pygame.display.flip()
    return s, ox, oy


PUNCH_KEYS = {pygame.K_a: "jab", pygame.K_s: "cross", pygame.K_d: "body_jab", pygame.K_f: "body_cross",
              pygame.K_w: "slip"}
HIGH_BLOCK_KEY, LOW_BLOCK_KEY = pygame.K_e, pygame.K_r


def handle_key(game, key):
    """One key press. Returns False if the game should quit."""
    if key == pygame.K_ESCAPE:
        return False
    if key in PUNCH_KEYS:
        game.press(PUNCH_KEYS[key])
    elif key == pygame.K_TAB:
        game.toggle_mode()
    elif key == pygame.K_c:
        game.start_campaign()
    elif key == pygame.K_BACKSPACE:
        game.reset()
    elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
        game.confirm()
    elif key in (pygame.K_1, pygame.K_2, pygame.K_3):
        game.set_level(LEVEL_KEYS[key - pygame.K_1])
    elif key == pygame.K_m:
        game.toggle_mute()
    elif key == pygame.K_F11:
        pygame.display.toggle_fullscreen()
    return True


def held_input(keys):
    """(left, right, low, block) from the keys currently held down."""
    low = keys[LOW_BLOCK_KEY]
    return keys[pygame.K_LEFT], keys[pygame.K_RIGHT], low, keys[HIGH_BLOCK_KEY] or low


def main():
    scale = 4
    for a in sys.argv[1:]:
        if a.startswith("--scale="):
            scale = max(1, int(a.split("=", 1)[1]))
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption("BOXER")
    screen = pygame.display.set_mode((VW * scale, VH * scale), pygame.RESIZABLE)
    game = Game()
    canvas = pygame.Surface((VW, VH))
    clock = pygame.time.Clock()
    view = (scale, 0, 0)

    def to_canvas(pos):
        s, ox, oy = view
        return (pos[0] - ox) // s, (pos[1] - oy) // s

    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEMOTION:
                game.mouse(*to_canvas(e.pos), False)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                game.mouse(*to_canvas(e.pos), True)
            elif e.type == pygame.KEYDOWN:
                running = handle_key(game, e.key) and running
        game.update(dt, *held_input(pygame.key.get_pressed()))
        game.draw(canvas)
        view = present(screen, canvas)
    pygame.quit()


# ============================================================ embedded sprites (PNG, base64)
STRIP_B64 = """
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
j380209ok7eni0RO4fISf/Zj7XyedyErZp3X9D+LLkOy54R4drNiL38JmXcjxuFi137z1n3Nugu6ZV+q6fZBpeG5B/adD6uThMbt
r/iSOdN3yfLV+SFM0it33tNF8tUwdc6ehibbJvlknD+uXCgdZ7kJ4aKT4a6HnYVEPnMOQxrUQ6FJoHkH4i5dLupzoj2+eZ25b0xl
kt0W1Tf0ecJUPXOENEiC2Lyyd8CXBBfNqHIW+OT8I/0EhwtnV8W7kI777nxw6tH+7+d6/6GuKmH6KLsnpzZM3+alU+d0bGJHb7y0
1vu++fXrunPnrTqhG1q7es37d924cWumDO7tnbujDEq4e8+l8j2gLvPnqJPiFcX/Zk7qeUvqH8B1cv6R0o7OB6ce1fz6dS2urWd+
Sb1K6vDeHfrk6uo2Bl/xyuJvx972y6kZ/XJqpn/46PSNdTafR7h9epAxu6jCyYu/NFwGxD9MaOylXsfIdfm+h/uL8K7la+ssAHj8
duXCNlPPhNT5btwv3/dwfzL0ydVlkv005OT8I1p891NJcfXQe7/+F73363/RR488qI8eeVDPHr5fj967a9tvVy5sM21x2a9O/ge3
kKplYZj2QGJzUChinlboYMs9APDwzOBWgJDkk7TFxbwHADZvXvjs6PH+xofZnRN6b+Hk0J93D+DN3Dahp7ZPaPfkcGKrcZW3edzu
jxbx3fp496OH+l9Dc8xk0JeOHx3aAETyyWpixwCGbwwmZdtexr7NWHn7Yq0J0JW3L+rVZw/kzln4cICsmK9MzOfsry2cXe3/Wrp0
PfOr7P1gfJbP1FVF70ZZedjlYsbI8+u9ctm356Dm16/n/hrnsoitj9y+lLt2YJj+LHEesJ/zGO7Y2B6rmbk66pQs5v9HA+tfabH+
OxrK6nxfGUi9Oof41xM6Fs4rA96BZoS2w0WxJ/7VVK1/eParMf3P2PbXRv8zXpU50KK9EOYSHkl6cOXNzPex9lWu6fVHs/ZlJ59E
M3xrMdr95f5elPd+/S+SipOx2vuzWKMs51uztNeDJXnXg6VBIsQy41oOv3nlp1p891M99/h01GEvu/6Xeu+Cm3yyyLi2C02tP+a1
vyj2u9NnKv25Lx0/2v+92/YazN/HsQ9C5nHr/tu/9Qvd/q1f6I///Nf63f/0l3r6/hn98rbP9cvbPtehN5d0Yult/eWv/5ehRDVu
+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
W+2v/T3E36+NvYfEPlwXdY9E+5unqbrHff5NwkPj2MQOnX94luff0WT+h8N7N5/rtezn59ev69jEjt4Hx56r+RPfXNpuexeXz2XH
YcTfy1cOnx6c0Ts/f3Ho7On+p1/QLdM/zXyvuXDKLg/mIdL47Ohx7Trq/9qTm7/27Tmo2ZkHB/USGrF06bo+/lHveTdJQGd3Tkhr
0vyl63rQeRd4Bzh/kRrxL5f0Z3YXfd3BVl7w8xLQLL/1vsShi2C+RfeQMiD+7cpLvmEQ/3Ihk/9Fm06KGoC8pFfEv1wTh3998Tex
5/BFTxMHT/Ni6RsAUw9lxcY/NPY+lMOwKou/vr6PNHygi+e/uroJyKRsrLf6AKwNRc9+aPwN952g71NdzOEL3+13ZbGn71POlME7
P3+xdMO5kbf5kDo/ntn0Hzr2kobbX8qgGffOHdGRr9yr9996cyjhhstug3kX4j362E905tV/yP36iwsvBpeDRBk0req7IFEfVeVL
/FkU+6JxgI3+ULmidjhkHMw4oD3M/3eD9a+0WP9Nzy6DmMSTkvTJ1dVteksb0nACyj98dLn/+92TUxufXF2lLc5R5T2wN4TaiScN
cyPq3/7sr4j9ptIk9Jt9on/41a/12Pe+o8N7B5sI7fj7LsKjHmpOUZ3EuLcdIXWQxLxDl/L2oDD2qid2DUwaTgJRtAcFzSaAk9iH
FavqJWyu2ARAtAU9XSRfIu71VLn0SCLudTSR9I16P0zZePdT9cqj7NI1iXKoK3T9tywZtMSerBhNvQO+iwDsREw24h4udg2G+Yfm
xMz52J8n9s3g2R9dRXsQaW/rqXMGYPfk1AbxL1f1/GPIGjD1T7kq8S9b96X+b0bd+of4t6+o/SX+9TW9902SufSU/SYF6tQ97Dtp
X9neWzuxGLGPVzX/wydXV7fNK5sA155/Y89/c2h7mxF7AaTvwqmPzx/1ngWWmIeI4SbPNg7v3aGlS9f12smXtWt6pvDv+NLxo/3k
h5L03sJJ3Tt3JPM9xyZ2aH79ukyiYuqjHjf+MX3ET195bCj5pNFPQrl+3dseIB/nL9Ii/olytry+tKIbP39R9/3sR/rJR2uZQ6em
0yPlV955DS/CFMVfKi8D4l/P60sremRzIHbyK/dKCl/8lYh/Xe85h97dDPNGbCI4lKt78B3NqHPw1KAeqs4X/9jnvWxBHsWKykAq
LwfiHq+JBGS2rT4A61pI/KWw2wcRp4nDF6jHlEHohnMXdX49JumYPr9RmHCsaOxFGYQrOvjyzs9f1PubiTbsfo8P8xDVmUQ9eWVR
pxwog3BtvQuUQb6yjbj3zh3pxX6zLSiKPfNAzSlrh2PGwYjD/H9arH+lxfpver4ykOLmoIsOYX95zy5JvU2iy2xM96r7Hki9zSi8
D+GKxgCPHJ6W3l3WrHpJKH/yve94N8qx7tIO3/uQ9x4Q+2ZUrYOIf3W+NZjQSxdQX8w6jFsurIM1p2oCOFQXk3y16BJmG21BNVUP
ARvEvZr3Fk7q3s25t6L9n1Jc4luU8106FZr0rcMf86ZRlvjwxub8f0jyScqhmrL1X0n9NZhQ7MkKF/oOxF48WIZ3JZ/bBrMG0x3W
X9Ji/TGtkPV3if5OW8r2oFc9j4QwoW1v3qV31D/1FMWf9rd9desf4l9P3faX+FdXp+95eO8OzV/KJvpBnDp1D+1vfey9TatO/geT
LI76pzra3m5UvQDSXYfJSz6JcL6y+PTgjN75+Yv6yfe+0//c5ZVlbxLKyyv+vRIm+eTi2novEaKyCRHR48Z/8Y339ZPvfWdDiksA
6iafRDXM/6dF/AeSJKB85PC0Xl9a0aGP1iRJj524oMN7e5nl60w0zzzwNf3Nz/+j/vZnf9VflOfQy7Ci+EvVy4D4hzHxv1e9jSdG
3UO/xD+Mib+Jva/yl6q/B/amIOKf5R58l/yTblL+Apjv7+XZD2MmIO47OKOfbNb/TScboCzyFcW/6UV2ysHPLADLk/iE579dZfW/
UWfzj2kjiPkwN/72hGcTCaDp++QzsX9k8+OYwxdFG82pbwbKJv5NGbz/xOOSig85xjz/lMFAaNIxaXjuwWD8W1/ZwRezAJaXaKMq
ymFYUVm0UQ6UQVaKd4Ey6Ck6AHbnu8vSG+9Lam7DP3HviWmHm5r7JPblmP9Pi/WvtFj/TS+vDGLj/9zP5vX8z495v2aSUNrlQnkM
NPEenDl4SIdKvoc5uZ6QRBCGNR6Ifmaph6rxvQ/Evl1ttcXUOfnMHPR9c0f6a8DS8BhMiisDnv0wvnWYouQzofMSVvxZgyzgrr+7
a2B1ExDwHuSzk68WaSLpGOXg59t/0uTlL+Me96prwLS/zYi5dEoqX4MPLQPinxUz3i1L9lylHWAMMFBUFne+u6x/eON9Pfa97+hV
z5+dvn+fpOoJuce5L1r2Drjrj0V4/sPFtsFNrT/a/775/bjFvkxbcz4GsS/W1vqjQfyLhay/S5z/akvIGYA65zGIf7G22l7GX2GK
4s/+h/a1Vf8Q/zBttb/Ev1ydvmfohRe0v/na7vtIxL8Ie2/TIv9DWrS96cVcAinVn/eXxrcsiuah7TNfX6y8oFumfzqUhDIv+WSe
xbX1/u95H/zxn334azq/Z2dQAlAT/8+OHteuo/5/48nNX/v2HOwnJ6Y+ysf5i7SI/0BrP1xIBmhjMyNuULB2T05tfO2Bh7yHXv7w
0eX+oRdJWn7rff3tz/5q5AuhDcQ/LeKfTkjszQDAxD708N3uyamNvBsYiH9PWfztwZcdf6m8Ac6LP7EfKIv/60sreuTwtKS4usf9
N6iH8hWVwetLK7p37kim/qkaG8phWEj9b94Bnv/m1an/jbx2gPq/WJW+z6vPHuh/rWgBgL5PuSrPvh1/m73pn/omjIlT0YELX9/f
x/f8UwblQsrAiG1/KYN4ZeVRpQ9EOVRTVBa8C+1rMv7230cZ5AtpD3j2mxfaDhP75jH/nxbxT4v4p9dWGbj/Rl55uMaxPNouA+bk
4plnVlLlPin1UDVNvA/EPk7TdRB1Trkq6zD0f5rTxBqkEboORvx7qqy/u2tgZYfweA+Kle0/cff/+NYgQ5KOUQ7Dqjz/sQloiHu+
KuuPMfs/iXuxqvH3YQ2+vtD137wykNgL1JSQ9Ue3HOa+MdX/vdsvoi8apuk9EDz/xdreA0Tsi7W5/kLsyxH/tIh/WnXn32L3/0vE
32hzzZHxV5jQMiD+7Wiz/iH+5dj/k07b9T/tb7G26h7zdxP/YtQ9aZH/IS2e//Ri8z+4l3BKw4lZ7XeDdqBcURn46iBJumX6p97v
/2LlBX38o1l9eOb80NcW19Y1u3Oi//v59es68dtXxr4MQuLvi71JQmmSTxbF3jBxN+/EuL8DtAFpEf8wt7T5lz/62E+Cvs9kIg65
XeGTq6vb7Mzdti/v2aU/fHS5/7HJCBry996MiH9axD+dstibzqeJ/dKl67X/TeI/UBR/O/O/Hf862Z+JfVZR/M3mcymu7rFRD+Ur
63w+cnh6qP6pGhvKwa+s/jfvAM9/O6rW/+ZX7L9HzAdi+z6PnbighbOr/UnOKmVA/Adin307/vYvuwyob8KYOIWUQV7dk/f8UwZh
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
"""


if __name__ == "__main__":
    main()