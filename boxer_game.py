#!/usr/bin/env python3
"""
BOXER - a tiny retro boxing game.

Starts in BAG mode (free practice on a heavy bag). Next to the BOXING GYM sign:
    SPAR      (or TAB)  a one-off fight against a computer opponent
    CAMPAIGN  (or C)    four fights back to back for the lightweight title belt
    BAG                 back to the heavy bag

    i  (bottom-left)   the controls panel - hover it, click it, or press I / F1
    ARROWS             move anywhere on the canvas - the ring has depth now. You always face
                       your man, and the sprites turn with you: side-on, three-quarter, back to
                       the camera when you're nearest it, face-on when you're up by the far ropes.
                       Close to him, a sideways arrow CIRCLES him at the same range; keep holding
                       it and you go all the way round.
    W + ARROW          side-step: a quick step off his line - beats head AND body shots if timed
                       (punches keep turning after you, so walking round him won't beat one -
                        but they can't follow a sudden step)
    X                  pivot: roll round him toward the open ring (off the ropes / out of a corner)
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

Wind (stamina)
    * Every punch costs wind - a cross costs twice a jab. Blocking and walking cost a little too.
      Stop punching and it comes back; stand still and breathe and it comes back faster.
    * Empty the tank and you are GASSED: slower hands, weaker punches, a guard that caves in and
      a chin that will not hold up. Pace yourself. Rushing in is how you lose a fight you were winning.

Feints
    * SHIFT (or G) + a punch key throws a FEINT: the first half of the punch, snapped back. It can't
      hurt anyone and costs almost no wind - but he has to respect it.
    * If he commits to a block or a slip that was never needed, you've got him: land in the next
      moment and the punch does far more damage ("FEINTED HIM!").
    * Keep throwing the same feint and he stops biting. Space them out and they work again.

He is watching you
    * The computer learns what you throw. Lean on one punch and he starts slipping it and
      countering; he also learns which punch you like to follow it with. "HE'S READING YOU" means
      mix it up. The harder the opponent, the faster he reads you.

Clinch and ropes
    * Q grabs hold of him. You both get tied up until the referee breaks it, and while you are in
      there you get your wind and your head back. Grab from too far out and you're wide open.
    * Backed onto the ropes you cannot retreat and punches land much harder. Cut the ring off.

Sparring rules
    * Both fighters have HP. Go a few seconds without taking damage and you slowly heal,
      but only up to your healing cap (the white tick on your HP bar). Body shots lower the cap.
    * Blocking drains your GUARD bar (blue). Blocking punch after punch drains it faster -
      eat a flurry and your guard breaks, leaving you stunned and wide open.
    * Critical hits do extra damage. Hitting someone mid-punch (counter hit), after a slip,
      or while they are stunned makes crits much more likely (stunned = guaranteed).

Knockdowns and knockouts
    * Run out of health and you go DOWN, you don't lose. The referee counts. MASH A/S/D/F
      to beat the count; you get up with less health and he finishes a standing eight count.
      Stay down until 10 and it's a K.O.  Three knockdowns in one fight = T.K.O.
    * Every clean punch has an IMPACT. Big impact = a flash knockdown, or knocked OUT COLD
      on the spot, even with health left. Impact goes up for:
        - power punches (cross, body cross) over jabs
        - landing at the end of your reach (flush) instead of smothered up close
        - counter hits: catching him mid-punch or walking forward into it
        - punching right after a slip or a parry, or into a broken guard
        - a fighter who is HURT (wobbling, gloves down), worn out, or already been down
        - long runs of unanswered punches
      Head shots also build up a hidden daze: too many and he's HURT, more and he drops.
      Body shots build up too - a hard body cross on a battered body is a LIVER SHOT.
    * If a HURT fighter keeps eating punches without firing back, the referee stops it (T.K.O.).
    * Go the distance and the judges decide (knockdowns count for a lot).

Career (story mode)
    * CAMPAIGN (or C) opens your career: twelve fights from a club show to the world title,
      with your trainer Doc Hayes in the corner and a conversation before and after every one.
    * Lose and the story does NOT reset - you take a tune-up fight to rebuild, then get the man
      who beat you again. Three losses and the commission pulls your licence: that career is over.
    * Win the belt and you get the ending. What is said on the boat depends on whether you
      got there unbeaten or the hard way.
    * After any fight: ENTER carries on, S saves your career and drops you back at the gym.
      Next time you press CAMPAIGN you can continue where you left off or start a new career.

Setup:   pip install pygame
Run:     python boxer_game.py            (optional: --scale=5 for a bigger window)

The character sprites are embedded at the bottom of this file, so this is the only file you need.
"""
import array
import base64
import io
import json
import math
import os
import random
import sys
import tempfile

import pygame

# ============================================================ screen / sprite layout
VW, VH = 320, 180            # internal pixel-art resolution (scaled up to the window)
FW, FH = 96, 80              # sprite frame size
HIP_X = 38                   # x of the hips inside a (right-facing) sprite frame
GROUND = 154                 # y of the floor line the boxers stand on (the middle of the ring's depth)

# ============================================================ the ring is a floor, not a line
# Fighters stand anywhere on the canvas: x across, z in depth (+ toward the camera). Feet are drawn at
# GROUND + z * ZK, so the far side of the ring is higher up the screen. Each man turns to face the other,
# and his sprite turns with him: side-on, three-quarter, face-on (walking away from you / backed up
# against the far ropes) or back-on (with his back to you, nearest the camera).
ZK = 0.5                     # one step toward the camera moves your feet half a pixel down the screen
Z_MIN, Z_MAX = -84, 26       # far ropes .. near ropes
Z_START = -30                # where they square off: the middle of the ring
LAT_HIT = 12                 # a punch lands if he is within this of the line it is thrown along
TRACK_SNAP = 0.5             # a punch is thrown at where he is right now (this much turn is instant)...
TRACK_MAX = 0.32             # ...and keeps turning after him while it travels, up to this much in all...
TRACK_RATE = 1.4             # ...at this many radians a second. Walking round him won't beat it; a side-step will
TURN_RATE = 9.0              # how fast you turn to face him otherwise (rad / s)
ORBIT_RANGE = 120            # inside this range, stepping sideways circles round him at the same distance
VIEW_STICK = 7               # degrees of stickiness before the sprite swaps to a new angle
SIDESTEP = 26                # W + an arrow: a quick step off his line...
SIDESTEP_TIME = 0.17         # ...this fast (it beats head AND body shots if you time it)
SIDESTEP_CD = 0.55
SIDESTEP_STAM = 6.0
DOUBLE_TAP = 0.26            # two taps inside this many seconds
FRONT_FADE = 150             # alpha of the nearer man when he is standing right in front of the other
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

# ============================================================ knockdowns / knockouts
# A clean punch's IMPACT starts from its power and is multiplied by everything that made it land
# hard (see Game.impact). Divided by the victim's chin, it's compared with these thresholds.
POWER = {"jab": 1.0, "cross": 2.0, "body_jab": 0.9, "body_cross": 2.0}
KD_IMPACT = 3.6              # from here a clean head shot can drop him (flash knockdown)
KO_IMPACT = 5.0              # from here it can switch the lights off (out cold, no count)
DAZE_HURT = 60               # daze meter: HURT (wobbling) from here...
DAZE_DROP = 100              # ...and down he goes from here
DAZE_DECAY = 13.0            # daze lost per second once he's had a breather...
DAZE_DELAY = 1.4             # ...of this many seconds without a head shot
HURT_EXIT = 38               # stops wobbling when daze drops below this
LIVER_BODY = 34              # body damage soaked up before a body cross can fold him
BODY_DECAY = 2.0             # body damage healed per second
MAX_DOWNS = 3                # third knockdown = T.K.O.
RISE_HP = (0.6, 0.38)        # health after getting up from the 1st / 2nd knockdown (x max HP)
COUNT_START = 1.15           # seconds after the knockdown before the referee says "one"
COUNT_DT = 0.72              # seconds per count
STANDING_COUNT = 8           # a fighter who gets up still takes a count to eight
MASH_NEED = 8                # key presses to get up from your first knockdown (more for later ones)
MASH_DECAY = 1.1             # the get-up meter drains this many presses per second
# ============================================================ clinch and ropes
CLINCH_RANGE = 14            # how far past touching distance you can reach to tie him up
CLINCH_TIME = 1.25           # seconds before the referee pulls you apart
PIVOT_TIME = 0.34            # seconds to roll round him
PIVOT_CD = 1.6               # you cannot spin all night
PIVOT_STAM = 15.0            # what it costs you
PIVOT_GAP = 6                # where you come up relative to him
PIVOT_ROOM = 34             # how much open floor counts as 'off the ropes' when choosing where to roll
CLINCH_CD = 2.6              # you can't just hold on all night
CLINCH_CD_ROPES = 1.0        # ...but with your back on the ropes you can grab him again sooner
CLINCH_STAM = 26.0           # wind recovered per second while you're holding on
CLINCH_DAZE = 34.0           # dizziness cleared per second while you're holding on
CLINCH_WHIFF = 0.55          # grabbed at air: that long wide open
ROPE_ZONE = 16               # within this of the ring edge you are ON THE ROPES
ROPE_IMPACT = 1.3            # punches land this much harder on a man pinned there
ROPE_SHOVE = 2.2             # extra push into the ropes

# ============================================================ stamina
# Every punch costs wind. Stand off and it comes back; throw non-stop and you GAS OUT:
# slower hands, weaker punches, a softer chin and a guard that drains faster.
STAM_MAX = 100
STAM_COST = {"jab": 5.0, "cross": 11.0, "body_jab": 5.5, "body_cross": 12.0, "slip": 3.5, "feint": 2.0}
STAM_MISS = 1.5              # extra cost for a punch that hits nothing (wild swings tire you out)
STAM_BLOCK = 7.0             # cost of soaking up a punch on the gloves
STAM_HIT = 4.0               # cost of taking one clean
STAM_HOLD = 14.0              # cost per second of sitting behind a high/low guard
STAM_MOVE = 1.6              # cost per second of walking
STAM_REGEN = 11.5            # recovered per second when you give yourself a breather...
STAM_REGEN_DELAY = 0.55      # ...this long after your last punch
STAM_REGEN_IDLE = 1.8        # standing still (not walking, not blocking) recovers this much faster
GAS_LINE = 30                # below this you are GASSED
STAM_GUARD_REGEN = 1.1       # YOU get your wind back behind a high/low guard (you aren't punching)...
STAM_MOVE_REGEN = 1.0        # ...and on the move. Taking one clean stops it for a moment:
STAM_HIT_PAUSE = 0.9         # seconds of no recovery after you get caught
STAM_DOWN_COST = 22          # a knockdown takes it out of you
STAM_RISE = 55               # stamina you get up with
PLAYER_CHIN = 1.1            # your chin (the computer boxers' chins are in CAMPAIGN; sparring CPU = 1.0)
STOPPAGE_HITS = 5            # unanswered clean shots on a HURT fighter before the ref stops it

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
#   reach  : extra hit distance on top of the sprite's own reach (the long, snapping jab)
#   target : head/body   spar_dmg : sparring damage   guard : guard drain when blocked
#   stun   : hit-stun on the victim (seconds)
ACTIONS = {
    "jab": dict(frames=[3, 4, 5, 6, 7], ms=[70, 90, 40, 120, 60], active={6}, cancel=4,
                lunge=[0, 2, 5, 7, 4], reach=5, dmg=8, kick=0.7, shake=1, stop=0.045,
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

# ============================================================ feints
# A feint is the first half of a punch, snapped back before it lands. It costs almost no wind and
# can't hurt anyone - but the other guy reacts to it, and reacting is what you're hunting for.
FEINT_OF = {}                # feint action name -> the punch it imitates
for _n in PUNCHES:
    _p = ACTIONS[_n]
    ACTIONS["feint_" + _n] = dict(frames=[_p["frames"][0], _p["frames"][1], _p["frames"][0]],
                                  ms=[50, 85, 80], active=set(), cancel=2,
                                  lunge=[_p["lunge"][0], _p["lunge"][1], 0], target=_p["target"])
    FEINT_OF["feint_" + _n] = _n
FEINTS = tuple(FEINT_OF)
THREATS = PUNCHES + FEINTS   # everything the other man has to respect
BAIT_WINDOW = 0.75           # land a punch this soon after he bites on a feint and you've FEINTED him
BAIT_MULT = 1.45             # impact bonus for that punch
COUNTER_WINDOW = 0.6         # seconds after the bottom of a slip in which a punch is a counter
COUNTER_MULT = 1.5
BUFFER_TIME = 0.8            # a key pressed up to this long before you can act is queued (one action)

# ============================================================ computer opponent
#   react  : chance to try to defend a punch      delay : reaction time (s)
#   slip   : chance to slip a head shot instead of blocking     wrong : blocks the wrong height
#   parry  : chance a block is perfectly timed    atk : seconds between attack decisions
#   combo / flurry / punish : chance to throw combos / flurry a blocker / punish a whiff
#   guard_up : how often it just sits behind its guard    learn : how fast it reads your habits
#   feint    : how often it throws feints of its own      pace : how well it rations its wind
LEVELS = {
    "EASY": dict(react=0.30, delay=(0.18, 0.34), slip=0.15, wrong=0.38, parry=0.0, atk=(1.0, 2.2),
                 combo=0.20, flurry=0.25, punish=0.20, guard_up=0.10, learn=0.3, feint=0.0, pace=0.45),
    "NORMAL": dict(react=0.63, delay=(0.12, 0.22), slip=0.25, wrong=0.18, parry=0.30, atk=(0.6, 1.4),
                   combo=0.35, flurry=0.50, punish=0.55, guard_up=0.20, learn=1.0, feint=0.18, pace=0.8),
    "HARD": dict(react=0.76, delay=(0.09, 0.17), slip=0.30, wrong=0.12, parry=0.45, atk=(0.45, 1.1),
                 combo=0.50, flurry=0.70, punish=0.70, guard_up=0.25, learn=1.5, feint=0.3, pace=1.0),
}
LEVEL_KEYS = ["EASY", "NORMAL", "HARD"]
# He is never certain. However good he is, there is always a way through - and sustained pressure
# makes his reads worse, not better, which is what lets volume punching work.
REACT_CAP = 0.82             # the most often any fighter will try to defend a punch
REACT_PRESSURE = 0.12        # how much a sustained burst degrades his reading
PARRY_SCALE = 0.72           # how much of a fighter's parry rating actually fires
PARRY_JITTER = (-0.06, 0.11) # his timing is human: some parries come early, some come late
BLOCK_REST = 0.16            # after he blocks he is briefly committed - that is your turn
PIN_PATIENCE = 1.5           # seconds he will pin you on the ropes before resetting
PIN_RESET = (0.55, 0.85)       # ...and how long he backs off for
GLANCE_CHANCE = 0.55         # chance of rolling with a punch you are already moving away from
GLANCE_DMG = 0.4             # what a glancing blow is worth
DMG_VARIANCE = 0.12          # no two punches land exactly the same

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

# ============================================================ the cast
#   look   : colours (see look_palette)          level/ai : AI difficulty + overrides (see LEVELS)
#   style  : how much he likes each punch        hp/power/speed/walk : health, punch damage,
#   taunt  : pre-fight animation                                      animation speed, footspeed
#   chin   : how much punishment his head takes  heart : how hard he fights to beat the count
#   wind   : his gas tank                        champ : wears the belt
FIGHTERS = {
    "rusty": dict(name='RICK "RUSTY" MALONE', short="RUSTY RICK", title="JOURNEYMAN   -   RECORD 8-11",
                  color=(150, 230, 160),
                  look=dict(glove=(236, 236, 242), shorts=(56, 156, 84), skin=(250, 200, 156), hair=(196, 88, 40)),
                  level="EASY", ai=dict(pace=0.4), style=dict(jab=1.6),
                  hp=80, power=0.9, speed=1.0, walk=1.0, chin=0.85, heart=0.8, wind=0.75, taunt="shadowbox",
                  intro="Fresh meat! Hope you packed a lunch, 'cause you're about to get SERVED!",
                  reply="Order up, Rusty. Hope you like it extra crispy.",
                  win="Ha! Back to the punching bag, rookie!",
                  lose="Ow... my everything..."),
    "pike": dict(name='TOMMY "TWO-TON" PIKE', short="TWO-TON PIKE", title="CLUB FIGHTER   -   RECORD 11-6",
                 color=(180, 200, 240),
                 look=dict(glove=(60, 70, 110), shorts=(200, 206, 230), skin=(238, 190, 146), hair=(120, 96, 60),
                           boots=(60, 70, 110)),
                 level="EASY", ai=dict(react=0.42, pace=0.45, atk=(0.8, 1.8)), style=dict(cross=2.0, body_cross=1.6),
                 hp=105, power=1.1, speed=0.88, walk=0.8, chin=1.1, heart=1.0, wind=0.7, taunt="roar",
                 intro="They call me Two-Ton 'cause that's what it feels like. Ask my last four opponents.",
                 reply="Two tons of slow. I'll be gone before it lands.",
                 win="Timber! Hah! Down like a tree.",
                 lose="Heavy hands... ain't worth much... if they don't land..."),
    "dunne": dict(name='MARCUS "THE MECHANIC" DUNNE', short="THE MECHANIC", title="TECHNICIAN   -   RECORD 15-3",
                  color=(140, 220, 230),
                  look=dict(glove=(40, 150, 160), shorts=(28, 36, 54), skin=(150, 100, 66), hair=(26, 22, 30),
                            boots=(230, 232, 240)),
                  level="NORMAL", ai=dict(react=0.7, parry=0.35, wrong=0.08, atk=(0.7, 1.4), pace=0.85, feint=0.2),
                  style=dict(jab=2.4, cross=1.2), hp=100, power=0.95, speed=1.05, walk=1.1,
                  chin=1.0, heart=1.1, wind=1.1, taunt="shadowbox",
                  intro="I don't brawl. I take men apart, one bolt at a time. Hold still.",
                  reply="I've seen your tape, Marcus. Everything you throw, I've already read.",
                  win="Dismantled. Nothing personal - just engineering.",
                  lose="You... changed the pattern. Nobody changes the pattern..."),
    "cruz": dict(name='DANTE "SUGAR" CRUZ', short="SUGAR CRUZ", title="UNBEATEN PROSPECT   -   RECORD 17-0",
                 color=(255, 170, 215),
                 look=dict(glove=(236, 90, 160), shorts=(250, 246, 240), skin=(206, 140, 96), hair=(30, 24, 32),
                           boots=(236, 90, 160)),
                 level="NORMAL", ai=dict(react=0.72, slip=0.45, parry=0.35, delay=(0.05, 0.13), atk=(0.5, 1.1),
                                         combo=0.5, punish=0.6, pace=1.0, feint=0.28, learn=1.1, step=0.2),
                 style=dict(jab=2.0, cross=1.4), hp=100, power=1.0, speed=1.12, walk=1.25,
                 chin=0.95, heart=1.2, wind=1.2, taunt="weave",
                 intro="Everybody gets one night that matters. This is yours. Enjoy it - I'm taking it.",
                 reply="You've been handed everything, Sugar. I've been taking mine.",
                 win="Nothing personal. Somebody's got to be the guy on my record.",
                 lose="How... I've never even been DOWN before..."),
    "cruz2": dict(name='DANTE "SUGAR" CRUZ', short="SUGAR CRUZ", title="TOP CONTENDER   -   RECORD 24-1",
                  color=(255, 170, 215),
                  look=dict(glove=(236, 90, 160), shorts=(250, 246, 240), skin=(206, 140, 96), hair=(30, 24, 32),
                            boots=(236, 90, 160)),
                  level="HARD", ai=dict(react=0.76, slip=0.45, parry=0.38, atk=(0.55, 1.15), combo=0.5, punish=0.65,
                                        pace=1.0, feint=0.3, learn=1.2, step=0.22),
                  style=dict(jab=1.8, cross=1.5, body_cross=1.2), hp=106, power=1.04, speed=1.12, walk=1.25,
                  chin=1.0, heart=1.3, wind=1.2, taunt="weave",
                  intro="I've thought about you every day since. Tonight I take it all back.",
                  reply="Then you already know how this ends, Dante.",
                  win="Told you. The first one wasn't the fluke - YOU were.",
                  lose="Go get him, man. Go take that belt. You earned it twice."),
    "bulldozer": dict(name='BRUNO "THE BULLDOZER" KASK', short="BULLDOZER", title="HEAVY HITTER   -   RECORD 14-4",
                      color=(255, 170, 90),
                      look=dict(glove=(240, 128, 40), shorts=(52, 48, 64), skin=(214, 150, 100), hair="bald",
                                boots=(52, 48, 64)),
                      level="NORMAL", ai=dict(react=0.45, slip=0.08, parry=0.2, atk=(0.8, 1.6), pace=0.5, feint=0.08),
                      style=dict(jab=0.6, cross=2.5, body_cross=2.5), hp=120, power=1.12, speed=0.92, walk=0.85,
                      chin=1.2, heart=1.2, wind=0.8, taunt="roar",
                      intro="NOTHING stops the Bulldozer! I'm gonna flatten you like a PANCAKE!",
                      reply="Even bulldozers run out of gas, big guy.",
                      win="FLATTENED! Somebody scrape this guy off my canvas!",
                      lose="Who... turned off... the engine..."),
    "razor": dict(name='KENJI "RAZOR" WATANABE', short="RAZOR", title="COUNTER PUNCHER   -   RECORD 20-2",
                  color=(190, 220, 255),
                  look=dict(glove=(190, 212, 240), shorts=(160, 30, 46), skin=(232, 186, 140), hair=(24, 22, 30),
                            boots=(160, 30, 46)),
                  level="NORMAL", ai=dict(react=0.66, slip=0.32, parry=0.33, delay=(0.05, 0.13), atk=(0.8, 1.7),
                                          punish=0.6, pace=0.9, feint=0.22, learn=1.1),
                  style=dict(jab=1.6, cross=1.8), hp=96, power=1.02, speed=1.08, walk=1.15,
                  chin=0.92, heart=1.05, wind=1.1, taunt="shadowbox",
                  intro="Throw whatever you like. Every punch you throw, I throw back sharper.",
                  reply="Then I'll make you lead for once.",
                  win="You kept giving me openings. I only needed the one.",
                  lose="You never... gave me anything to counter..."),
    "lee": dict(name='"LIGHTNING" LEE PARK', short="LIGHTNING LEE", title="SPEED DEMON   -   RECORD 19-2",
                color=(200, 160, 255),
                look=dict(glove=(150, 70, 214), shorts=(240, 206, 56), skin=(232, 182, 132), hair=(34, 34, 48)),
                level="NORMAL", ai=dict(react=0.78, slip=0.5, parry=0.35, delay=(0.05, 0.12), atk=(0.45, 1.0),
                                        combo=0.55, punish=0.65, pace=1.0, feint=0.3, learn=1.2, step=0.28),
                style=dict(jab=2.5, body_jab=1.5), hp=95, power=1.0, speed=1.18, walk=1.35,
                chin=0.92, heart=1.0, wind=1.35, taunt="weave",
                intro="Better not blink. I'll be done before your health bar even loads!",
                reply="Lightning never strikes twice. I do.",
                win="Too slow! Try again in slow motion.",
                lose="Impossible... nobody's faster than me!"),
    "preacher": dict(name='ELI "THE PREACHER" BOONE', short="THE PREACHER", title="OLD LION   -   RECORD 38-12",
                     color=(230, 220, 190),
                     look=dict(glove=(90, 72, 56), shorts=(40, 38, 48), skin=(120, 78, 54), hair=(220, 220, 226),
                               boots=(90, 72, 56)),
                     level="NORMAL", ai=dict(react=0.76, slip=0.3, parry=0.42, atk=(0.85, 1.8), punish=0.7,
                                             guard_up=0.3, pace=1.05, feint=0.3, learn=1.25),
                     style=dict(jab=1.8, body_jab=1.8, body_cross=1.6), hp=100, power=0.98, speed=0.98, walk=0.95,
                     chin=1.1, heart=1.3, wind=1.2, taunt="belt",
                     intro="Fifty fights, son. I have been hit by better men than you on worse nights than this.",
                     reply="Respect, old man. But you're standing in my doorway.",
                     win="Patience, son. You'll learn it. Everybody does, eventually.",
                     lose="Took you long enough... now go on. Go take the thing I never got."),
    "sal": dict(name='BIG SAL MARCONI', short="BIG SAL", title="THE GATEKEEPER   -   RECORD 26-5",
                color=(255, 140, 120),
                look=dict(glove=(170, 32, 40), shorts=(30, 32, 44), skin=(224, 168, 120), hair=(70, 50, 36),
                          boots=(170, 32, 40)),
                level="HARD", ai=dict(react=0.7, slip=0.1, parry=0.3, atk=(0.6, 1.2), flurry=0.8, combo=0.6,
                                      pace=0.7, feint=0.15),
                style=dict(cross=2.0, body_cross=2.2, body_jab=1.4), hp=126, power=1.1, speed=0.95, walk=0.9,
                chin=1.2, heart=1.25, wind=0.85, taunt="roar",
                intro="Nobody gets past me without paying the toll. Cash, or blood. Your pick.",
                reply="Put it on my tab, Sal.",
                win="Toll's paid. In blood. Come back when you can afford it.",
                lose="Gate's... open, kid. Don't make me regret it."),
    "volkov": dict(name='DMITRI "THE SIBERIAN" VOLKOV', short="VOLKOV", title="FINAL ELIMINATOR   -   RECORD 29-1",
                   color=(170, 220, 255),
                   look=dict(glove=(220, 226, 238), shorts=(36, 70, 130), skin=(238, 206, 180), hair=(226, 220, 200),
                             boots=(36, 70, 130)),
                   level="HARD", ai=dict(react=0.78, parry=0.4, atk=(0.55, 1.15), combo=0.55, punish=0.68,
                                         pace=1.05, feint=0.28, learn=1.3),
                   style=dict(jab=1.4, cross=1.8, body_cross=1.5), hp=118, power=1.08, speed=1.02, walk=1.0,
                   chin=1.12, heart=1.35, wind=1.15, taunt="shadowbox",
                   intro="One of us fights for the title. The other one goes home. I am not going home.",
                   reply="Neither am I, Dmitri. Let's find out who's lying.",
                   win="Go home. The title was never yours to want.",
                   lose="Cold... I have never felt cold... in the ring before..."),
    "reyes": dict(name='VICTOR "THE CROWN" REYES', short="THE CROWN",
                  title="LIGHTWEIGHT CHAMPION   -   RECORD 40-0", champ=True, color=(255, 214, 90),
                  look=dict(glove=(44, 40, 54), shorts=(232, 180, 56), skin=(196, 128, 88), hair=(26, 22, 28)),
                  level="HARD", ai=dict(parry=0.5, pace=1.1, feint=0.34, step=0.18), style=dict(),
                  hp=126, power=1.08, speed=1.06, walk=1.1, chin=1.14, heart=1.45, wind=1.15, taunt="belt",
                  intro="Forty fights. Forty knockouts. You want my belt? Come and take it... if you dare.",
                  reply="I didn't come here to lose. That belt is MINE.",
                  win="You were never on my level.",
                  lose="The crown... is yours, kid. Wear it well."),
    # --- tune-up opponents: who you get when you have to rebuild
    "joe": dict(name='JOE "HAMMERS" HENDRY', short="HAMMERS JOE", title="SHORT NOTICE   -   RECORD 9-9",
                color=(200, 190, 160),
                look=dict(glove=(150, 140, 110), shorts=(90, 70, 50), skin=(246, 196, 150), hair=(150, 120, 70),
                          boots=(150, 140, 110)),
                level="EASY", ai=dict(react=0.4, pace=0.45), style=dict(cross=1.6),
                hp=92, power=1.0, speed=0.95, walk=0.95, chin=0.95, heart=0.9, wind=0.8, taunt="shadowbox",
                intro="Took this on three days' notice. No hard feelings - I just need the purse.",
                reply="Same, Joe. Let's make it quick and clean.",
                win="Sorry, pal. I needed it more.",
                lose="No shame in it. Go get your career back."),
    "rios": dict(name='CARLOS "EL TORO" RIOS', short="EL TORO", title="COMEBACK BOUT   -   RECORD 13-8",
                 color=(255, 180, 140),
                 look=dict(glove=(220, 60, 40), shorts=(240, 200, 60), skin=(180, 118, 76), hair=(30, 26, 30),
                           boots=(220, 60, 40)),
                 level="NORMAL", ai=dict(react=0.46, slip=0.12, atk=(0.85, 1.7), flurry=0.5, pace=0.5),
                 style=dict(cross=1.8, body_cross=1.8), hp=98, power=1.0, speed=0.96, walk=1.0,
                 chin=1.0, heart=1.05, wind=0.8, taunt="roar",
                 intro="They tell me you lost. Good. I eat men who are already bleeding.",
                 reply="Then you're going to choke, Carlos.",
                 win="El Toro doesn't lose to damaged goods.",
                 lose="You had nothing left... and you still had more than me."),
    # --- your corner. Not a fighter any more, but he was.
    "doc": dict(name="DOC HAYES", short="DOC", title="YOUR TRAINER", color=(255, 226, 150),
                look=dict(glove=(120, 120, 130), shorts=(60, 58, 74), skin=(176, 124, 86), hair=(226, 226, 232),
                          boots=(60, 58, 74))),
    "you": dict(name="YOU", short="YOU", title="", color=(130, 200, 255), look=None),
}

# ============================================================ the road to the title
#   opp   : who you fight          bout : how the bout is billed
#   pre   : the scene before it    won / lost : the scene after it
CAREER = [
    dict(opp="rusty", act=1, bout="PRO DEBUT   -   4 ROUNDS",
         pre=[("doc", "Four years in my gym and you still can't leave the heavy bag alone."),
              ("doc", "Tonight that stops. Club show, forty people, a guy who's lost eleven."),
              ("you", "Forty people is thirty-nine more than usually watch me."),
              ("doc", "Then give 'em something. Jab, breathe, don't fall in love with the big one.")],
         won=[("doc", "That's a pro record now, kid. 1 and 0."),
              ("you", "Felt like it took an hour."),
              ("doc", "It took ninety seconds. You'll learn the difference.")],
         lost=[("doc", "Hey. Look at me. Everybody loses. The ones who matter lose EARLY."),
               ("you", "That's supposed to help?"),
               ("doc", "No. This is: I got you another one. Six weeks. Don't waste 'em.")]),
    dict(opp="pike", act=1, bout="4 ROUNDS   -   LIGHTWEIGHT",
         pre=[("doc", "Pike's a big slow kid with a hammer in his right hand."),
              ("doc", "He only lands it on people who stand still. So don't."),
              ("you", "Move, jab, don't be where the hammer is."),
              ("doc", "Now you're a boxer.")],
         won=[("doc", "See? He got tired carrying all that beef around."),
              ("you", "He hit me once and I saw my whole childhood."),
              ("doc", "Then stop getting hit.")],
         lost=[("doc", "You stood in front of him. I TOLD you about standing in front of him."),
               ("you", "...I know."),
               ("doc", "Good. Knowing's the cheap part. Now go pay for it in the gym.")]),
    dict(opp="dunne", act=1, bout="6 ROUNDS   -   LIGHTWEIGHT",
         pre=[("doc", "Marcus Dunne. Technician. He finds your pattern and he lives in it."),
              ("you", "So I don't give him one."),
              ("doc", "Attaboy. Mix the levels. Feint him - make him commit to nothing.")],
         won=[("doc", "You feinted a man who reads patterns into reading one that wasn't there."),
              ("you", "That's the first time I've out-THOUGHT somebody."),
              ("doc", "Won't be the last. People are starting to call about you.")],
         lost=[("doc", "He solved you by the third. Read you like a bus timetable."),
               ("you", "He knew the cross was coming before I did."),
               ("doc", "Then throw something else. That's the whole lesson. That's it.")]),
    dict(opp="cruz", act=1, bout="MAIN EVENT   -   8 ROUNDS", rival=True,
         pre=[("doc", "They offered us Sugar Cruz. Seventeen and oh. Promoter's golden boy."),
              ("doc", "They want a name on his record. They picked you."),
              ("you", "Then they picked wrong."),
              ("doc", "...You know what? Say that again in the ring.")],
         won=[("doc", "You just took an unbeaten man's 0. Do you understand what you did?"),
              ("you", "I think I'm going to be sick."),
              ("doc", "Be sick in the car. There's six promoters outside and they ALL want you now.")],
         lost=[("doc", "He was better tonight. That's all that was."),
               ("you", "He didn't even look tired, Doc."),
               ("doc", "He will. Guys like that burn bright. We'll see him again - and we'll be ready.")]),
    dict(opp="bulldozer", act=2, bout="RANKED BOUT   -   8 ROUNDS",
         pre=[("doc", "Welcome to the rankings, kid. They start you with the Bulldozer."),
              ("doc", "He throws everything for six minutes and then he's a statue."),
              ("you", "So I survive six minutes."),
              ("doc", "You survive six minutes and then you go hunting.")],
         won=[("doc", "He emptied the tank and you were still breathing. That's conditioning."),
              ("you", "That's three months of running, is what that is."),
              ("doc", "Keep running.")],
         lost=[("doc", "He caught you early and you never got your legs back."),
               ("you", "I couldn't BREATHE, Doc."),
               ("doc", "Then we fix the engine. Wind beats power - every single time.")]),
    dict(opp="razor", act=2, bout="RANKED BOUT   -   10 ROUNDS",
         pre=[("doc", "Kenji Watanabe. Razor. He doesn't lead - he answers."),
              ("doc", "Whatever you throw, he throws it back sharper and a half-beat later."),
              ("you", "So I make him lead."),
              ("doc", "Feints, kid. Make him answer a question you never asked.")],
         won=[("doc", "He spent ten rounds waiting for a punch you never threw."),
              ("you", "I've never been that patient in my life."),
              ("doc", "Patience is the last thing a fighter learns. You're ahead of schedule.")],
         lost=[("doc", "Every time you led, he was already there."),
               ("you", "I walked onto every single one."),
               ("doc", "So stop walking. Next time you make HIM move first.")]),
    dict(opp="lee", act=2, bout="RANKED BOUT   -   10 ROUNDS",
         pre=[("doc", "Lightning Lee. Fastest hands in the division and he knows it."),
              ("you", "Can I outrun him?"),
              ("doc", "No. Nobody can. So cut the ring off and make him fight in a phone booth.")],
         won=[("doc", "You took away the ring and he had nowhere to be fast."),
              ("you", "He was still a blur. I just knew where the blur had to go."),
              ("doc", "Ring generalship. Write that down.")],
         lost=[("doc", "You chased him for ten rounds and caught air."),
               ("you", "He was never where I threw."),
               ("doc", "Because you chased. Next time you CUT. There's a difference.")]),
    dict(opp="preacher", act=2, bout="RANKED BOUT   -   10 ROUNDS",
         pre=[("doc", "Eli Boone. We came up together. He's forty-one and he's still here."),
              ("you", "You don't sound happy about this one."),
              ("doc", "He's the best man I ever knew in a ring. And he never got a title shot."),
              ("doc", "Beat him. He'd be insulted by anything less.")],
         won=[("doc", "He hugged you at the end. You know he's never done that?"),
              ("you", "He told me to go get the thing he never got."),
              ("doc", "...Yeah. That's Eli.")],
         lost=[("doc", "Forty-one years old and he schooled you. Don't you dare be ashamed."),
               ("you", "He knew everything I was going to do."),
               ("doc", "He's known it for twenty years. Go learn some of it.")]),
    dict(opp="sal", act=2, bout="ELIMINATOR   -   10 ROUNDS",
         pre=[("doc", "Big Sal Marconi. The gatekeeper. Nobody gets a title shot without going through him."),
              ("doc", "Five men have tried this year. Five men went home."),
              ("you", "Then it's time somebody paid the toll."),
              ("doc", "He's bigger, he's stronger, and he fades. Body. All night. Body.")],
         won=[("doc", "You put eighty punches into that man's ribs and he just... folded."),
              ("you", "I couldn't feel my hands by the sixth."),
              ("doc", "Doesn't matter. The gate's open, kid. We're in the top five.")],
         lost=[("doc", "He leaned on you for ten rounds and you let him."),
               ("you", "He was so HEAVY."),
               ("doc", "They all are. You go to the body until heavy men get light.")]),
    dict(opp="volkov", act=3, bout="FINAL ELIMINATOR   -   12 ROUNDS",
         pre=[("doc", "This is it. Winner fights for the title. Loser goes back to the queue."),
              ("doc", "Volkov. Twenty-nine and one. Cold as the day is long."),
              ("you", "Doc... I've been doing this for four years for exactly tonight."),
              ("doc", "Then quit talking and go be the man who deserves it.")],
         won=[("doc", "Twelve rounds. TWELVE. And you were the one still walking forward."),
              ("you", "Say it, Doc."),
              ("doc", "You're fighting for the lightweight championship of the world, kid.")],
         lost=[("doc", "Twelve rounds and three points. Three."),
               ("you", "I was RIGHT THERE."),
               ("doc", "You were. And that's why they'll give us another one. Breathe. We go again.")]),
    dict(opp="cruz2", act=3, bout="TITLE ELIMINATOR   -   12 ROUNDS", rival=True,
         pre=[("doc", "Guess who the sanctioning body put in front of us. One last time."),
              ("you", "Sugar."),
              ("doc", "Twenty-four and one. And the one still eats at him every night."),
              ("doc", "He's not a golden boy any more, kid. He's dangerous now.")],
         won=[("doc", "He shook your hand and told you to go take the belt. He MEANT it."),
              ("you", "Four years ago he wouldn't look at me in a weigh-in."),
              ("doc", "Four years ago you were nobody. Look at you now.")],
         lost=[("doc", "He wanted it more tonight. That's an ugly sentence and it's the true one."),
               ("you", "I'm running out of road, Doc."),
               ("doc", "Then stop wasting it. Gym. Tomorrow. Six AM.")]),
    dict(opp="reyes", act=3, bout="FOR THE WORLD TITLE   -   12 ROUNDS", title_fight=True,
         pre=[("doc", "Forty fights. Forty knockouts. Victor Reyes has never heard a final bell."),
              ("doc", "Kid... whatever happens after tonight, I want you to know something."),
              ("you", "Doc, don't do a speech."),
              ("doc", "I waited thirty years for a fighter like you. Go on. Go get it.")],
         won=[], lost=[]),
]

REBUILDS = ("joe", "rios")      # the fights you take to climb back after a loss
MAX_LOSSES = 3                  # three on the record and the commission pulls your licence

# ============================================================ the scenes that aren't fights
SCENES = dict(
    open=[("doc", "IRON JAW GYM. 5:40 AM. Same as every morning for four years."),
          ("doc", "You've beaten every sparring partner I can find in this city."),
          ("doc", "So either you turn pro tonight, or you stay here and get old hitting a bag."),
          ("you", "...Where do I sign?")],
    setback=[("doc", "Sit down. Ice on that. Listen to me."),
             ("doc", "You're not the first good fighter to get beat and you won't be the last."),
             ("doc", "But a loss on the record means we go the long way round now."),
             ("doc", "Tune-up fight. Look sharp. Remind people who you are.")],
    rebuilt=[("doc", "That's the one. Looked like you again out there."),
             ("you", "Can we get the big one back?"),
             ("doc", "Already made the call. They're giving you the rematch.")],
    last_chance=[("doc", "Two losses, kid. Two."),
                 ("doc", "One more and the commission pulls your licence for the year."),
                 ("you", "Then I don't lose again."),
                 ("doc", "No. You don't.")],
    title_lost=[("doc", "Nobody has ever taken Victor Reyes past the eighth. Nobody."),
                ("you", "I didn't come for a moral victory, Doc."),
                ("doc", "I know. But the whole world just watched you go in there and MAKE him work."),
                ("doc", "They want it again. Rematch. Six months. Go earn it properly this time.")],
)

# ============================================================ endings
RETIRE_SCENE = [("doc", "Commission pulled the licence this morning. Twelve months minimum."),
                ("you", "Twelve months."),
                ("doc", "You had it, kid. On your night, you had it as much as any of them."),
                ("doc", "Come work the corner with me. Teach some other punk what it cost you."),
                ("you", "...Yeah. Yeah, okay, Doc."),
                ("doc", "Lights off when you leave. You know where the key goes.")]

# Dialogue on the boat. The first list is for an unbeaten run, the second for a road with losses on it.
YACHT_CLEAN = [("doc", "Forty-one fights I worked corners. Never once been on a boat."),
               ("you", "You've never even been in the ocean, Doc."),
               ("doc", "I've been in the ocean. There was a bucket of ice involved and you were bleeding."),
               ("you", "Fair."),
               ("doc", "Not one loss. You went through that entire division and not ONE man beat you."),
               ("you", "Somebody would have, eventually. Everybody gets got."),
               ("doc", "Maybe. But not yet, champ."),
               ("you", "...Hey, Doc?"),
               ("doc", "Mm."),
               ("you", "Thanks for the 5:40s."),
               ("doc", "Thanks for showing up to 'em.")]
YACHT_ROAD = [("doc", "You know what I keep thinking about? Not the belt."),
              ("you", "No?"),
              ("doc", "The night you lost and you were sat on that bench and you couldn't look at me."),
              ("you", "I remember the bench."),
              ("doc", "Everybody remembers the wins, kid. I remember you coming back in at 5:40 the next morning."),
              ("you", "Where else was I gonna go?"),
              ("doc", "A thousand guys would've gone anywhere else. That's the whole story. That right there."),
              ("you", "...Pass me the sunglasses."),
              ("doc", "Get 'em yourself, champ. I'm retired.")]

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


class FrameSet(list):
    """A strip cut into frames, plus how it is anchored: flipped (faces left) and the row its feet are on."""
    flip = False
    feet = SPRITE_FEET


def split(strip, flip=False, feet=SPRITE_FEET):
    frames = [strip.subsurface((i * FW, 0, FW, FH)).copy() for i in range(strip.get_width() // FW)]
    out = FrameSet(pygame.transform.flip(f, True, False) for f in frames) if flip else FrameSet(frames)
    out.flip, out.feet = flip, feet
    return out


VIEW_FEET = {"f": 72, "b": 72, "fq": 73, "bq": 73}   # the turned views stand a little higher in their frames


def make_views(strips, mapping=None):
    """{"side": (right, left), "fq": (right, left), "bq": (right, left), "f": set, "b": set}, recoloured."""
    out = {}
    for key, strip in strips.items():
        base = strip if not mapping else recolor(strip, mapping)
        feet = VIEW_FEET.get(key, SPRITE_FEET)
        if key in ("f", "b"):
            out[key] = split(base, feet=feet)
        else:
            out[key] = (split(base, feet=feet), split(base, True, feet))
    return out


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
    return (sum(spec["ms"][f.idx:first]) - f.t) / 1000.0 / f.spd()


# ============================================================ sound (synthesised, no files)
class BandPass:
    """Resonant band-pass filter (biquad) - turns white noise into vowels, crowds, smacks."""

    def __init__(self, rate, freq, q):
        w = 2 * math.pi * freq / rate
        alpha = math.sin(w) / (2 * q)
        a0 = 1 + alpha
        self.b0, self.b2 = alpha / a0, -alpha / a0
        self.a1, self.a2 = -2 * math.cos(w) / a0, (1 - alpha) / a0
        self.x1 = self.x2 = self.y1 = self.y2 = 0.0

    def __call__(self, x):
        y = self.b0 * x + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
        self.x2, self.x1, self.y2, self.y1 = self.x1, x, self.y1, y
        return y


def make_sounds(background=True):
    """All sound effects. The crowd recordings take a moment to synthesise, so by default they're
    made on a background thread and appear in the dict when ready."""
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
    rnd = random.Random(1234)
    noise = rnd.uniform
    TAU = 2 * math.pi

    def fade(vals, secs=0.03):
        """Fade the last few ms out so nothing ends with a click."""
        k = min(len(vals), int(secs * rate))
        for i in range(k):
            vals[len(vals) - k + i] *= 1 - (i + 1) / k
        return vals

    def lowpass(vals, cutoff, passes=2):
        a = 1 - math.exp(-TAU * cutoff / rate)
        for _ in range(passes):
            y = 0.0
            for i, x in enumerate(vals):
                y += (x - y) * a
                vals[i] = y
        return vals

    def to_sound(vals, gain=0.55):
        buf = array.array("h")
        for v in vals:
            s = int(clamp(v, -1.0, 1.0) * 32767 * gain)
            for _ in range(ch):
                buf.append(s)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def synth(dur, fn):
        n = int(dur * rate)
        return to_sound([fn(i / rate, i / n) for i in range(n)])

    def reverb(vals, delays=(0.031, 0.047, 0.071), fb=0.32, tail=0.4):
        out = list(vals) + [0.0] * int(tail * rate)
        for d in delays:
            k = int(d * rate)
            for i in range(k, len(out)):
                out[i] += out[i - k] * fb
        peak = max(1e-6, max(abs(v) for v in out))
        return fade([v / max(1.0, peak) for v in out], 0.15)

    def whoosh(dur, lo, hi, vol):
        state = [0.0]

        def fn(t, u):
            a = lo + (hi - lo) * u
            state[0] += (noise(-1, 1) - state[0]) * a
            return state[0] * (math.sin(math.pi * u) ** 2) * vol * 3.0
        return synth(dur, fn)

    def punch(dur, f0, f1, thud, smack, tone, sub=0.0, drive=1.6, decay=18):
        """Layered glove impact: pitched thud + band-passed leather smack + transient click
        (+ an optional sub-boom), soft-clipped together."""
        n = int(dur * rate)
        bp = BandPass(rate, tone, 1.1)
        ph = 0.0
        vals = []
        norm = math.tanh(drive)
        for i in range(n):
            t = i / rate
            f = f1 + (f0 - f1) * math.exp(-t * 38)
            ph += TAU * f / rate
            r = noise(-1, 1)
            v = (math.sin(ph) * math.exp(-t * decay) * thud
                 + bp(r) * 3.2 * math.exp(-t * 55) * smack
                 + r * math.exp(-t * 420) * 0.45
                 + math.sin(TAU * 46 * t) * math.exp(-t * 6.5) * sub * min(1.0, t * 400))
            vals.append(math.tanh(v * drive) / norm)
        return fade(vals)

    def ring_bell(base, dur, vol=1.0):
        """Boxing-ring bell: hard strike + inharmonic partials that ring on."""
        parts = ((1.0, 1.0, 2.2), (2.32, 0.55, 3.4), (4.25, 0.32, 5.0), (6.63, 0.2, 7.5), (0.5, 0.25, 1.6))
        n = int(dur * rate)
        vals = []
        for i in range(n):
            t = i / rate
            v = sum(a * math.sin(TAU * base * m * t) * math.exp(-t * d) for m, a, d in parts)
            v += noise(-1, 1) * math.exp(-t * 300) * 0.6
            vals.append(v * 0.42 * vol)
        return fade(vals, 0.08)

    def mix(*layers):
        """layers: (start seconds, sample list, gain)"""
        n = max(int(s * rate) + len(v) for s, v, _ in layers)
        out = [0.0] * n
        for s, v, gn in layers:
            o = int(s * rate)
            for i, x in enumerate(v):
                out[o + i] += x * gn
        return out

    def crowd_noise(dur, formants, env, chatter=0.0, seed=0, lp=None):
        """Lots of people at once: noise through vowel formants, with a slow random swell."""
        r = random.Random(seed)
        n = int(dur * rate)
        filt = [(BandPass(rate, f, q), a) for f, q, a in formants]
        lfo = [r.uniform(0, TAU) for _ in range(3)]
        vals = []
        g = 0.0
        gate = 1.0
        for i in range(n):
            t = i / rate
            x = r.uniform(-1, 1)
            v = sum(f(x) * a for f, a in filt)
            if chatter:                      # syllable-ish flutter from individual voices
                if i % 600 == 0:
                    gate = r.uniform(1 - chatter, 1.0)
                g += (gate - g) * 0.004
                v *= g
            sw = 1 + 0.18 * math.sin(TAU * 0.31 * t + lfo[0]) + 0.1 * math.sin(TAU * 0.83 * t + lfo[1])
            vals.append(v * sw * env(t, i / n))
        return lowpass(vals, lp) if lp else vals

    def voices(dur, count, lo, hi, contour, env, vib=5.0, seed=0, bright=0.35):
        """A few dozen 'singing' voices sliding together - the OOOH / YEAH of a crowd."""
        r = random.Random(seed)
        n = int(dur * rate)
        blk = 32                                 # pitch / loudness only change every 32 samples
        nb = n // blk + 1
        cont = [contour(min(1.0, b / nb)) for b in range(nb)]
        envs = [env(min(1.0, b / nb)) for b in range(nb)]
        out = [0.0] * (nb * blk)
        sin = math.sin
        for _ in range(count):
            f0, p0, sp, late = r.uniform(lo, hi), r.uniform(0, TAU), r.uniform(0.85, 1.15), r.randint(-nb // 16, nb // 16)
            ph = p0
            for b in range(nb):
                j = min(nb - 1, max(0, b - late))
                f = f0 * cont[j] * (1 + 0.02 * sin(TAU * vib * sp * b * blk / rate + p0))
                inc = TAU * f / rate
                e = envs[j]
                o = b * blk
                for i in range(o, o + blk):
                    ph += inc
                    s = sin(ph)
                    out[i] += (s + bright * s * s * s) * e
        k = 1.0 / count
        return [v * k for v in out[:n]]

    try:
        snd["swish"] = whoosh(0.11, 0.55, 0.12, 0.35)
        snd["slip"] = whoosh(0.20, 0.25, 0.08, 0.28)
        snd["hit_jab"] = to_sound(punch(0.16, 210, 95, 0.75, 0.7, 1900, drive=1.4))
        snd["hit_cross"] = to_sound(punch(0.28, 170, 62, 1.0, 0.9, 1500, sub=0.35, drive=2.0))
        snd["hit_body"] = to_sound(punch(0.22, 120, 55, 1.0, 0.45, 650, sub=0.25, drive=1.8, decay=12))
        snd["hit_body_big"] = to_sound(punch(0.34, 105, 42, 1.1, 0.5, 520, sub=0.6, drive=2.4, decay=9))
        snd["crit"] = to_sound(reverb(punch(0.36, 160, 40, 1.1, 1.0, 1300, sub=0.8, drive=3.0), tail=0.25))
        snd["block"] = to_sound(punch(0.10, 340, 220, 0.4, 0.9, 2600, drive=1.2, decay=30))
        snd["parry"] = to_sound(mix((0, punch(0.08, 400, 300, 0.4, 1.0, 3000, drive=1.2), 0.8),
                                    (0.01, ring_bell(1500, 0.35, 0.6), 0.6)))
        snd["guard_break"] = to_sound(punch(0.38, 260, 60, 0.9, 1.0, 1100, sub=0.4, drive=2.5))
        ding = ring_bell(760, 1.6)
        snd["bell"] = to_sound(ding)
        snd["bell3"] = to_sound(fade(mix((0, ding, 0.8), (0.3, ding, 0.8), (0.6, ding, 0.9)), 0.1))
        clap = []
        for i in range(int(0.16 * rate)):
            t = i / rate
            burst = sum(math.exp(-max(0.0, t - o) * 140) * (t >= o) for o in (0.0, 0.009, 0.019))
            clap.append(noise(-1, 1) * burst * 0.5)
        bp = BandPass(rate, 1400, 0.9)
        clap = [bp(v) * 3 for v in clap]
        snd["count"] = to_sound(mix((0, clap, 1.0), (0, punch(0.12, 160, 110, 0.6, 0.0, 800, drive=1.2), 0.6)))
        fall = punch(0.6, 90, 38, 1.2, 0.6, 400, sub=0.9, drive=2.4, decay=7)
        rattle = [math.sin(TAU * 1830 * i / rate) * math.exp(-i / rate * 5) * 0.12 * (1 + 0.5 * math.sin(TAU * 13 * i / rate))
                  for i in range(int(0.7 * rate))]
        snd["canvas"] = to_sound(fade(mix((0, fall, 1.0), (0.02, fade(rattle), 1.0))))
        snd["ko_boom"] = to_sound(reverb(punch(0.6, 140, 34, 1.2, 1.0, 1100, sub=1.2, drive=3.5, decay=6),
                                         delays=(0.043, 0.067, 0.097, 0.131), fb=0.38, tail=0.9))
        beat = punch(0.18, 70, 45, 1.0, 0.1, 200, drive=1.5, decay=16)
        snd["heartbeat"] = to_sound(mix((0, beat, 0.9), (0.2, beat, 0.6)), gain=0.7)
        snd["ringing"] = synth(1.8, lambda t, u: (math.sin(TAU * 3650 * t) + 0.4 * math.sin(TAU * 3712 * t))
                               * min(1.0, t / 0.05) * (1 - u) ** 2 * 0.22)

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
                    f *= 1 + 0.04 * math.sin(TAU * 5.5 * lt) * min(1.0, lt / 0.25)
                ph[0] += TAU * f / rate
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

    except pygame.error:
        return {}

    def crowd_sounds():
        loop_len, xf = 6.0, 0.6
        murmur = crowd_noise(loop_len + xf, ((420, 2.2, 1.0), (1050, 2.6, 0.55), (2400, 3.0, 0.18)),
                             lambda t, u: 1.0, chatter=0.6, seed=3, lp=1500)
        k = int(xf * rate)
        n = int(loop_len * rate)
        for i in range(k):                       # cross-fade the tail into the head = seamless loop
            a = i / k
            murmur[i] = murmur[i] * a + murmur[n + i] * (1 - a)
        murmur = murmur[:n]
        peak = max(abs(v) for v in murmur)
        snd["crowd_loop"] = to_sound([v / peak * 0.55 for v in murmur], gain=0.6)

        def swell(a, r):
            return lambda u: min(1.0, u / a) * (1 - max(0.0, (u - r) / (1 - r))) ** 1.5

        ooh = mix((0, voices(1.4, 14, 150, 300, lambda u: 1.0 + 0.18 * math.sin(math.pi * min(1, u * 1.4)) - 0.12 * u,
                             swell(0.15, 0.45), seed=5, bright=0.15), 1.0),
                  (0, crowd_noise(1.4, ((380, 3.5, 1.0), (800, 4.0, 0.4)), lambda t, u: swell(0.15, 0.45)(u),
                                  seed=6, lp=1100), 0.25))
        peak = max(abs(v) for v in ooh)
        snd["ooh"] = to_sound([v / peak * 0.8 for v in ooh], gain=0.6)

        def cheer(dur, seed, whistles):
            env = swell(0.08, 0.35)
            layers = [(0, crowd_noise(dur, ((750, 1.6, 1.0), (1250, 2.0, 0.7), (2600, 2.5, 0.25)),
                                      lambda t, u: env(u), chatter=0.25, seed=seed, lp=2600), 1.0),
                      (0, voices(dur, 10, 180, 380, lambda u: 1.0 + 0.25 * min(1, u * 5), env, vib=7, seed=seed + 1,
                                 bright=0.5), 0.5)]
            r = random.Random(seed)
            for w in range(whistles):        # two-finger whistles
                st, ln, fq = r.uniform(0.05, dur * 0.5), r.uniform(0.25, 0.5), r.uniform(2100, 3000)
                wv = [math.sin(TAU * fq * (i / rate) * (1 + 0.08 * min(1, i / rate / 0.08)))
                      * min(1, i / rate / 0.03) * (1 - i / (ln * rate)) for i in range(int(ln * rate))]
                layers.append((st, wv, 0.12))
            out = mix(*layers)
            peak = max(abs(v) for v in out)
            return [v / peak * 0.85 for v in out]

        snd["cheer"] = to_sound(cheer(2.2, 11, 2), gain=0.6)
        snd["roar"] = to_sound(cheer(3.6, 21, 5), gain=0.7)
        snd["crowd"] = snd["cheer"]

    def safe():
        try:
            crowd_sounds()
        except pygame.error:
            pass
    if background:
        import threading
        threading.Thread(target=safe, daemon=True).start()
    else:
        safe()
    return snd


# ============================================================ scenery
SIGN_POS = (88, 17)


def make_background(ring=False):
    rnd = random.Random(7)
    bg = pygame.Surface((VW, VH))
    bg.fill((30, 34, 58))
    wall_bottom = 134 if not ring else 92

    bw, bh = 20, 9
    base = (54, 60, 92)
    for row in range(wall_bottom // bh + 1):
        y = row * bh
        off = (row % 2) * (bw // 2)
        for bx in range(-bw, VW + bw, bw):
            v = rnd.randint(-5, 5) + int(-16 + 24 * (y / wall_bottom))
            col = tuple(clamp(c + v, 0, 255) for c in base)
            bg.fill(col, (bx + off, y, bw - 1, bh - 1))

    y, i = wall_bottom + 7, 0
    while y < VH:
        h = 5 + min(i // 2, 5)
        bg.fill((92, 64, 78) if i % 2 == 0 else (101, 71, 85), (0, y, VW, h - 1))
        bg.fill((62, 42, 58), (0, y + h - 1, VW, 1))
        off = (i * 37) % 48
        for x in range(-off, VW, 48):
            bg.fill((62, 42, 58), (x, y, 1, h - 1))
        y += h
        i += 1

    bg.fill((36, 28, 48), (0, wall_bottom, VW, 7))
    bg.fill((86, 72, 108), (0, wall_bottom, VW, 1))
    bg.fill((26, 22, 36), (0, 0, VW, 9))
    bg.fill((70, 60, 88), (0, 9, VW, 1))
    for x in range(14, VW, 52):
        bg.fill((44, 38, 58), (x, 0, 2, 9))
    bg.fill((70, 66, 92), (BAG_X - 4, 8, 8, 4))
    bg.fill((30, 26, 44), (BAG_X - 4, 11, 8, 1))

    posters = ((22, 40, 30, 40, (196, 56, 66)), (118, 46, 26, 34, (226, 190, 120)), (262, 42, 28, 38, (76, 120, 196)))
    if ring:
        posters = ((22, 24, 30, 40, (196, 56, 66)), (118, 30, 26, 34, (226, 190, 120)), (262, 26, 28, 38, (76, 120, 196)))
    for (px, py, pw, ph, col) in posters:
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
        if not ring:
            pygame.draw.ellipse(glow, (255, 240, 190, 20), (lx - 60, 146, 120, 26))
    if ring:
        draw_ring(bg, (118, 128, 150), (160, 168, 186), (70, 76, 100), (120, 110, 100),
                  ((196, 56, 66), (76, 120, 196)), (70, 56, 80))
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


# ============================================================ the arena (campaign)
RING_BACK = 104              # y of the back edge of the ring canvas
RING_INSET = 20              # the far edge of the canvas is narrower (perspective)
ROPES = (70, 82, 94)         # y of the back ropes
POSTS = (RING_INSET, VW - 1 - RING_INSET)   # x of the far ring posts
BOARDS_Y = 79                # top of the sponsor boards behind the ring
NEAR_Y = GROUND + int(Z_MAX * ZK) + 5       # the near ropes
RING_ROPE_COLS = ((220, 50, 60), (240, 240, 246), (60, 100, 220))
ARENA_SIGN = "FIGHT NIGHT"
CROWD_ROWS = ((45, 0.50, 7, 0), (54, 0.62, 8, 0), (63, 0.76, 9, 1), (74, 0.92, 10, 1))   # head y, light, spacing, size
SHIRTS = [(200, 60, 70), (60, 110, 200), (230, 230, 236), (40, 40, 52), (226, 180, 60), (70, 160, 90),
          (150, 80, 180), (230, 120, 50), (90, 190, 210), (120, 120, 140), (190, 60, 120)]
SKINS = [(240, 196, 150), (214, 160, 112), (180, 120, 80), (130, 84, 56), (96, 62, 44), (250, 214, 176)]
HAIRS = [(30, 24, 30), (80, 50, 30), (200, 160, 80), (140, 60, 30), (160, 160, 170), (20, 20, 24)]


def arena_tint(c, light):
    """Crowd colours sit in the dark: dimmed and pushed toward the arena blue."""
    return tuple(int(clamp(v * light * 0.82 + b * (1 - light) * 0.35, 0, 255)) for v, b in zip(c, (40, 46, 90)))


def draw_ring(bg, top, bottom, edge, post, pads, skirt, logo=None):
    """The ring seen from the stands: the canvas narrows toward the far ropes, posts and ropes at the
    back, side ropes running off toward the camera, the near ropes and apron along the bottom."""
    for y in range(RING_BACK, VH):
        k = (y - RING_BACK) / (VH - RING_BACK)
        inset = max(0, int(round(RING_INSET * (1 - k * 2.4))))
        bg.fill(_mix(top, bottom, k), (inset, y, VW - 2 * inset, 1))
        if inset > 0:
            bg.fill(edge, (inset, y, 1, 1))
            bg.fill(edge, (VW - 1 - inset, y, 1, 1))
    bg.fill(edge, (RING_INSET, RING_BACK, VW - 2 * RING_INSET, 1))
    if logo:
        bg.blit(logo, (VW // 2 - logo.get_width() // 2, GROUND + int(Z_START * ZK) - logo.get_height() // 2))
    # side ropes, from the far posts off toward the near corners (off screen)
    for i, (ry, col) in enumerate(zip(ROPES, RING_ROPE_COLS)):
        for px, sgn in ((POSTS[0], -1), (POSTS[1], 1)):
            end = (px + sgn * 44, ry + 80)
            pygame.draw.line(bg, (20, 18, 30), (px, ry + 1), (end[0], end[1] + 1), 3)
            pygame.draw.line(bg, col, (px, ry), end, 2)
    draw_back_ropes(bg, post, pads)
    near = NEAR_Y
    bg.fill(skirt, (0, near + 3, VW, VH - near - 3))
    bg.fill(lighten(skirt, 0.3), (0, near + 3, VW, 1))
    for ry, col in ((near, RING_ROPE_COLS[0]), (near - 2, RING_ROPE_COLS[1])):
        bg.fill((20, 18, 30), (0, ry - 1, VW, 3))
        bg.fill(col, (0, ry - 1, VW, 2))
        bg.fill(lighten(col, 0.5), (0, ry - 1, VW, 1))


def draw_back_ropes(bg, post, pads):
    """The far posts and ropes (also drawn on their own over the crowd, which stands behind them)."""
    for px, pad in zip(POSTS, pads):
        bg.fill((20, 18, 30), (px - 2, ROPES[0] - 12, 5, RING_BACK - ROPES[0] + 16))
        bg.fill(post, (px - 1, ROPES[0] - 12, 3, RING_BACK - ROPES[0] + 15))
        bg.fill(lighten(post, 0.3), (px - 1, ROPES[0] - 12, 1, RING_BACK - ROPES[0] + 15))
        for ry in ROPES:
            bg.fill((20, 18, 30), (px - 4, ry - 3, 9, 7))
            bg.fill(pad, (px - 3, ry - 2, 7, 5))
            bg.fill(lighten(pad, 0.4), (px - 3, ry - 2, 7, 1))
    for ry, col in zip(ROPES, RING_ROPE_COLS):
        bg.fill((20, 18, 30), (POSTS[0] + 4, ry - 1, POSTS[1] - POSTS[0] - 8, 3))
        bg.fill(col, (POSTS[0] + 4, ry - 1, POSTS[1] - POSTS[0] - 8, 2))
        bg.fill(lighten(col, 0.5), (POSTS[0] + 4, ry - 1, POSTS[1] - POSTS[0] - 8, 1))


ARENA_POST, ARENA_PADS = (150, 150, 170), ((210, 40, 56), (50, 90, 210))


def make_rope_overlay():
    s = pygame.Surface((VW, RING_BACK + 4), pygame.SRCALPHA)
    draw_back_ropes(s, ARENA_POST, ARENA_PADS)
    return s


def make_arena_background(button_x):
    rnd = random.Random(11)
    bg = pygame.Surface((VW, VH))
    for y in range(VH):                                   # dark bowl, a little lighter low down
        k = y / VH
        bg.fill((int(12 + 14 * k), int(10 + 12 * k), int(26 + 26 * k)), (0, y, VW, 1))

    # upper deck: rows of far-away fans, aisles and stairs
    for y in range(12, 34, 4):
        light = 0.18 + 0.3 * (y - 12) / 22
        bg.fill(arena_tint((60, 60, 90), light), (0, y + 2, VW, 1))
        x = rnd.uniform(0, 3)
        while x < VW:
            col = arena_tint(rnd.choice(SHIRTS), light * 0.9)
            bg.fill(col, (int(x), y + 1, 2, 2))
            bg.fill(arena_tint(rnd.choice(SKINS), light), (int(x), y, 2, 1))
            x += rnd.uniform(2.6, 4.2)
    for ax in (52, 160, 268):                              # aisles
        bg.fill((14, 12, 28), (ax - 4, 11, 8, 24))
        for y in range(13, 34, 3):
            bg.fill((34, 32, 56), (ax - 4, y, 8, 1))
    bg.fill((26, 22, 44), (0, 34, VW, 3))                 # balcony front
    bg.fill((70, 64, 110), (0, 34, VW, 1))
    for x in range(4, VW, 22):
        bg.fill((255, 214, 120), (x, 35, 2, 1))           # little balcony lamps

    # rafters / lighting truss
    bg.fill((8, 8, 16), (0, 0, VW, 9))
    for x in range(0, VW, 6):
        pygame.draw.line(bg, (40, 40, 60), (x, 1), (x + 6, 7))
    bg.fill((56, 56, 80), (0, 1, VW, 1))
    bg.fill((56, 56, 80), (0, 7, VW, 1))
    for lx in (34, 96, 160, 224, 286):
        bg.fill((20, 20, 30), (lx - 4, 7, 9, 5))
        bg.fill((255, 250, 220), (lx - 2, 11, 5, 1))

    # sponsor boards behind the ring, then the dark floor round it
    bf = pygame.font.Font(None, 13)
    bg.fill((14, 16, 40), (0, BOARDS_Y, VW, 14))
    bg.fill((60, 70, 140), (0, BOARDS_Y, VW, 1))
    ads = [("KO COLA", (236, 70, 70)), ("IRONJAW GYM", (240, 210, 90)), ("PUNCH TV", (110, 200, 255)),
           ("BOXER", (255, 120, 170)), ("GLOVE-X", (140, 230, 150))]
    x, i = 2, 0
    while x < VW:
        text, col = ads[i % len(ads)]
        img = bf.render(text, False, col)
        bg.blit(img, (x, BOARDS_Y + 3))
        x += img.get_width() + 16
        bg.fill((40, 46, 90), (x - 9, BOARDS_Y + 2, 1, 10))
        i += 1
    bg.fill((22, 18, 36), (0, BOARDS_Y + 14, VW, RING_BACK - BOARDS_Y - 14))
    bg.fill((70, 26, 44), (RING_INSET, RING_BACK - 5, VW - 2 * RING_INSET, 5))     # far apron
    bg.fill((120, 40, 60), (RING_INSET, RING_BACK - 5, VW - 2 * RING_INSET, 1))

    # the ring
    logo = pygame.Surface((150, 26), pygame.SRCALPHA)
    pygame.draw.ellipse(logo, (120, 40, 70, 60), (0, 0, 150, 26))
    pygame.draw.ellipse(logo, (255, 255, 255, 40), (8, 3, 134, 20), 1)
    lf = pygame.font.Font(None, 20)
    t = lf.render("CHAMPIONSHIP", False, (255, 255, 255))
    t.set_alpha(70)
    logo.blit(t, (75 - t.get_width() // 2, 7))
    draw_ring(bg, (146, 154, 184), (212, 216, 230), (96, 104, 140), ARENA_POST, ARENA_PADS, (160, 30, 50), logo)

    # sign next to the mode button
    f = pygame.font.Font(None, 20)
    w = f.size(ARENA_SIGN)[0]
    sx = button_x - 6 - w
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        bg.blit(f.render(ARENA_SIGN, False, (110, 60, 10)), (sx + dx, SIGN_POS[1] + dy))
    bg.blit(f.render(ARENA_SIGN, False, (255, 214, 90)), (sx, SIGN_POS[1]))
    return bg


def make_arena_lights():
    """Additive light: beams from the truss onto the ring + a pool of light on the canvas."""
    s = pygame.Surface((VW, VH))                     # added on top (BLEND_RGB_ADD): keep it dark
    for lx in (96, 160, 224):
        cone = pygame.Surface((VW, VH))
        pygame.draw.polygon(cone, (9, 8, 6), [(lx - 3, 12), (lx + 3, 12), (lx + 70, GROUND + 4), (lx - 70, GROUND + 4)])
        s.blit(cone, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    pool = pygame.Surface((VW, VH))
    pygame.draw.ellipse(pool, (16, 15, 12), (20, RING_BACK + 4, VW - 40, 62))
    s.blit(pool, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    pool.fill((0, 0, 0))
    pygame.draw.ellipse(pool, (14, 13, 10), (60, RING_BACK + 16, VW - 120, 38))
    s.blit(pool, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    return s


def make_person(rnd, size, light):
    """One fan, arms down and arms up (13 x 22, head near the top)."""
    imgs = []
    head_r = 2 if size == 0 else 3
    skin = arena_tint(rnd.choice(SKINS), light)
    shirt = arena_tint(rnd.choice(SHIRTS), light)
    hair = arena_tint(rnd.choice(HAIRS), light)
    cap = rnd.random() < 0.18
    capc = arena_tint(rnd.choice(SHIRTS), light)
    bw = rnd.randint(7, 9) if size else rnd.randint(6, 7)
    ol = arena_tint((10, 8, 18), light)
    for arms_up in (False, True):
        s = pygame.Surface((13, 22), pygame.SRCALPHA)
        cx, hy = 6, 7
        s.fill(ol, (cx - bw // 2 - 1, hy + head_r, bw + 2, 22))
        s.fill(shirt, (cx - bw // 2, hy + head_r + 1, bw, 22))
        s.fill(lighten(shirt, 0.15), (cx - bw // 2, hy + head_r + 1, bw, 1))
        if arms_up:
            for ax in (cx - bw // 2, cx + bw // 2 - 1):
                s.fill(ol, (ax - 1, 0, 3, hy + head_r + 2))
                s.fill(shirt, (ax, 2, 1, hy + head_r))
                s.fill(skin, (ax, 0, 1, 2))
        pygame.draw.circle(s, ol, (cx, hy), head_r + 1)
        pygame.draw.circle(s, skin, (cx, hy), head_r)
        if cap:
            s.fill(capc, (cx - head_r, hy - head_r, head_r * 2 + 1, 2))
        else:
            s.fill(hair, (cx - head_r + 1, hy - head_r, head_r * 2 - 1, 1 if size == 0 else 2))
        imgs.append(s)
    return imgs


class Crowd:
    """Rows of fans behind the ring. They bob, stand, throw their arms up and pop camera flashes
    depending on how excited they are (hype 0..1)."""

    def __init__(self):
        rnd = random.Random(5)
        self.people = []
        for row, (y, light, sp, size) in enumerate(CROWD_ROWS):
            x = rnd.uniform(-6, 0) - (row % 2) * sp / 2
            while x < VW + 6:
                down, up = make_person(rnd, size, light)
                sign = None
                if row >= 2 and rnd.random() < 0.07:
                    sign = pygame.Surface((14, 8))
                    sign.fill(arena_tint((20, 18, 30), light))
                    sign.fill(arena_tint((240, 240, 236), light), (1, 1, 12, 6))
                    sign.fill(arena_tint(rnd.choice(SHIRTS), light), (3, 3, rnd.randint(5, 8), 2))
                self.people.append([x, y - 7, down, up, rnd.uniform(0, 6.28), rnd.uniform(0.4, 1.0), sign,
                                    rnd.uniform(0.8, 1.25)])
                x += sp + rnd.uniform(-1.5, 1.5)
        self.flashes = []

    def update(self, dt, hype):
        rate = 0.5 + 22 * hype * hype
        n = rate * dt
        for _ in range(int(n) + (1 if random.random() < n % 1 else 0)):
            pr = random.choice(self.people)
            self.flashes.append([pr[0] + 6 + random.randint(-2, 2), pr[1] + random.randint(2, 8), 0.0])
        for f in self.flashes:
            f[2] += dt
        self.flashes = [f for f in self.flashes if f[2] < 0.08]

    def draw(self, c, clock, hype):
        speed = 5 + 7 * hype
        stand = 2 if hype > 0.75 else (1 if hype > 0.5 else 0)
        for x, y, down, up, ph, ex, sign, sp in self.people:
            wave = math.sin(clock * speed * sp + ph)
            bob = int(round(wave * (0.35 + 2.4 * hype * ex)))
            arms = hype * ex > 0.42 and math.sin(clock * speed * 0.5 * sp + ph) > -0.2
            yy = y - stand - max(0, bob)
            c.blit(up if arms else down, (int(x), yy))
            if sign is not None:
                c.blit(sign, (int(x) - 1, yy - 7 - (2 if arms else 0)))
        for x, y, t in self.flashes:
            k = 1 - t / 0.08
            col = (255, 255, int(220 + 35 * k))
            c.fill(col, (x - 1, y, 3, 1))
            c.fill(col, (x, y - 1, 1, 3))
            if k > 0.5:
                c.fill((255, 255, 255), (x - 2, y, 5, 1))
                c.fill((255, 255, 255), (x, y - 2, 1, 5))


# ============================================================ the referee
REF_POSES = ("idle", "walk", "up", "down", "wave_a", "wave_b", "point")


def make_referee():
    """Pixel referee (white shirt, bow tie, black slacks), one surface per pose, facing right.
    Surface is 44 x 66; the feet are on the bottom row, x = 22 is his centre."""
    ol, shirt, shirt_s = (24, 14, 34), (236, 238, 248), (176, 182, 206)
    pants, pants_l, skin, skin_s = (40, 40, 54), (74, 74, 96), (232, 176, 128), (190, 130, 92)
    hair = (150, 150, 162)
    arms = {   # (shoulder->elbow->hand) for the front arm, then the back arm
        "idle": (((25, 26), (26, 34), (26, 41)), ((17, 26), (16, 34), (16, 41))),
        "walk": (((25, 26), (28, 33), (29, 40)), ((17, 26), (14, 33), (13, 40))),
        "up": (((25, 26), (30, 19), (31, 10)), ((17, 26), (16, 34), (16, 41))),
        "down": (((25, 26), (32, 30), (38, 35)), ((17, 26), (16, 34), (16, 41))),
        "wave_a": (((25, 26), (31, 19), (25, 12)), ((17, 26), (12, 19), (18, 12))),
        "wave_b": (((25, 26), (33, 22), (40, 17)), ((17, 26), (9, 22), (2, 17))),
        "point": (((25, 26), (33, 25), (41, 24)), ((17, 26), (16, 34), (16, 41))),
    }
    out = {}
    for pose in REF_POSES:
        s = pygame.Surface((44, 66), pygame.SRCALPHA)
        front, back = arms[pose]

        def arm(pts, sleeve, hand):
            pygame.draw.lines(s, sleeve, False, pts, 3)
            hx, hy = pts[-1]
            s.fill(hand, (hx - 1, hy - 1, 3, 3))
        arm(back, shirt_s, skin_s)
        stride = 3 if pose == "walk" else 0
        s.fill(pants, (17 - stride, 42, 4, 20))          # legs
        s.fill(pants, (22 + stride, 42, 4, 20))
        s.fill(pants_l, (22 + stride, 42, 1, 20))
        s.fill((20, 20, 26), (15 - stride, 62, 7, 4))      # shoes
        s.fill((20, 20, 26), (22 + stride, 62, 8, 4))
        s.fill((90, 90, 110), (23 + stride, 62, 5, 1))
        s.fill(shirt, (16, 23, 11, 19))                    # torso
        s.fill(shirt_s, (16, 23, 2, 19))
        s.fill((30, 30, 40), (16, 40, 11, 2))              # belt
        s.fill(skin, (20, 20, 4, 4))                       # neck
        s.fill((20, 20, 26), (19, 23, 6, 2))               # bow tie
        s.fill((20, 20, 26), (21, 22, 2, 4))
        pygame.draw.ellipse(s, skin, (16, 7, 11, 14))      # head
        s.fill(skin_s, (16, 14, 2, 4))
        s.fill(hair, (16, 6, 10, 4))
        s.fill(hair, (16, 6, 3, 8))
        s.fill((30, 20, 30), (24, 12, 1, 2))               # eye
        s.fill(skin_s, (25, 17, 2, 1))                     # mouth
        arm(front, shirt, skin)
        if pose == "up":                                   # fingers up for the count
            s.fill(skin, (30, 7, 1, 3))
            s.fill(skin, (32, 7, 1, 3))
        sil = pygame.mask.from_surface(s).to_surface(setcolor=ol, unsetcolor=(0, 0, 0, 0))
        o = pygame.Surface((44, 66), pygame.SRCALPHA)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            o.blit(sil, (dx, dy))
        o.blit(s, (0, 0))
        out[pose] = (o, pygame.transform.flip(o, True, False))
    return out


class Referee:
    SPEED = 170.0

    def __init__(self, game):
        self.game = game
        self.imgs = make_referee()
        self.hide()

    def hide(self):
        self.on = False
        self.x = self.tx = -60.0
        self.z = 0.0
        self.facing = 1
        self.pose, self.pose_t = "idle", 0.0
        self.leaving = False

    def enter(self, from_x, to_x, facing):
        if not self.on:
            self.x = from_x
        self.on, self.leaving = True, False
        self.tx, self.facing = to_x, facing
        self.pose, self.pose_t = "walk", 0.0

    def leave(self):
        if self.on:
            self.leaving = True
            self.tx = VW + 60 if self.x > VW / 2 else -60
            self.facing = 1 if self.tx > self.x else -1

    def set_pose(self, pose, hold=0.0):
        self.pose, self.pose_t = pose, hold

    def arrived(self):
        return self.on and abs(self.x - self.tx) < 1

    def update(self, dt):
        if not self.on:
            return
        self.pose_t = max(0.0, self.pose_t - dt)
        d = self.tx - self.x
        if abs(d) > 0.5:
            self.x += clamp(d, -self.SPEED * dt, self.SPEED * dt)
        elif self.leaving:
            self.hide()

    def draw(self, c, clock):
        if not self.on:
            return
        moving = abs(self.tx - self.x) > 0.5
        pose = self.pose
        face = self.facing
        if moving and self.pose_t <= 0:
            pose = "walk" if int(clock * 8) % 2 else "idle"
            face = 1 if self.tx > self.x else -1
        elif pose in ("wave_a", "wave_b"):
            pose = "wave_a" if int(clock * 7) % 2 else "wave_b"
        img = self.imgs[pose][0 if face > 0 else 1]
        gy = GROUND + int(round(self.z * ZK))
        c.blit(self.game.shadow, (int(self.x) - 24, gy - 5))
        c.blit(img, (int(self.x) - 22, gy - 65))


# ============================================================ story scenes
PORTRAIT_W, PORTRAIT_H = 30, 28
PORTRAIT_FRAME = 47          # the one frame where the gloves are down and you can see his face
SAVE_NAME = ".boxer_career.json"


def save_path():
    for base in (os.path.expanduser("~"), os.path.dirname(os.path.abspath(__file__)), tempfile.gettempdir()):
        try:
            if os.path.isdir(base) and os.access(base, os.W_OK):
                return os.path.join(base, SAVE_NAME)
        except OSError:
            continue
    return os.path.join(tempfile.gettempdir(), SAVE_NAME)


def load_career():
    """The saved career, or None. A broken save is simply ignored."""
    try:
        with open(save_path()) as fh:
            d = json.load(fh)
        return d if isinstance(d, dict) and "idx" in d else None
    except (OSError, ValueError):
        return None


def save_career(data):
    try:
        with open(save_path(), "w") as fh:
            json.dump(data, fh)
        return True
    except OSError:
        return False


def clear_career():
    try:
        os.remove(save_path())
    except OSError:
        pass


class Scene:
    """A between-fights conversation: portrait, name, and typed-out dialogue."""
    CPS = 42
    CARD = pygame.Rect(10, 104, VW - 20, 52)
    CARD_TOP = pygame.Rect(10, 6, VW - 20, 46)

    def __init__(self, game, lines, top=False):
        self.game = game
        self.CARD = self.CARD_TOP if top else Scene.CARD
        self.lines = [l for l in lines if l]
        self.i = 0
        self.t = 0.0
        self.last = 0
        self.wrapped = self.wrap(0)

    def wrap(self, i):
        if i >= len(self.lines):
            return []
        return wrap(self.game.font_s, self.lines[i][1], self.CARD.w - PORTRAIT_W - 22)

    def who(self):
        return self.lines[self.i][0] if self.i < len(self.lines) else "doc"

    def text(self):
        return self.lines[self.i][1] if self.i < len(self.lines) else ""

    def shown(self):
        return min(len(self.text()), int(self.t * self.CPS))

    def typed(self):
        return self.shown() >= len(self.text())

    def done(self):
        return self.i >= len(self.lines)

    def advance(self):
        """Enter: finish typing this line, or move to the next one."""
        if not self.typed():
            self.t = len(self.text()) / self.CPS
            return
        self.i += 1
        self.t = 0.0
        self.last = 0
        self.wrapped = self.wrap(self.i)

    def update(self, dt):
        if self.done():
            return
        self.t += dt
        n = self.shown()
        if n // 3 > self.last // 3 and n < len(self.text()):
            self.game.snd("blip")
        self.last = n

    def draw(self, c):
        if self.done():
            return
        g = self.game
        who = self.who()
        spk = FIGHTERS.get(who, FIGHTERS["doc"])
        r = self.CARD
        plate = pygame.Surface(r.size, pygame.SRCALPHA)
        plate.fill((12, 10, 24, 238))
        c.blit(plate, r.topleft)
        pygame.draw.rect(c, (92, 80, 120), r, 1)
        c.fill(spk["color"], (r.x + 1, r.y, r.w - 2, 1))
        c.blit(g.portrait(who), (r.x + 5, r.y + 5))
        tx = r.x + 10 + PORTRAIT_W
        draw_text(c, self.font_name(), spk["name"], tx, r.y + 5, spk["color"])
        for k, line in enumerate(self.wrapped):
            left = self.shown() - sum(len(x) + 1 for x in self.wrapped[:k])
            if left <= 0:
                break
            c.blit(g.font_s.render(line[:left], False, (232, 236, 250)), (tx, r.y + 18 + k * 10))
        if self.typed() and int(g.clock * 3) % 2 == 0:
            draw_text(c, g.font_s, "ENTER", r.right - 8, r.bottom - 11, (255, 214, 90), right=True)

    def font_name(self):
        return self.game.font_s


# ============================================================ the yacht (the good ending)
SEA_Y = 88                   # horizon
DECK_Y = 120                 # where the deck starts
SKY = ((24, 20, 54), (86, 46, 94), (198, 94, 96), (248, 160, 92), (255, 214, 130))


def make_yacht_sky():
    s = pygame.Surface((VW, VH))
    for y in range(SEA_Y + 2):
        u = y / float(SEA_Y + 2)
        k = u * (len(SKY) - 1)
        i = min(len(SKY) - 2, int(k))
        s.fill(_mix(SKY[i], SKY[i + 1], k - i), (0, y, VW, 1))
    sun_y = SEA_Y - 13
    for r in range(26, 0, -1):                                  # haze around the sun
        a = int(5 + 40 * (1 - r / 26.0))
        glow = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 210, 140, a), (r, r), r)
        s.blit(glow, (VW // 2 + 54 - r, sun_y - r), special_flags=pygame.BLEND_RGBA_ADD)
    pygame.draw.circle(s, (255, 236, 176), (VW // 2 + 54, sun_y), 11)
    pygame.draw.circle(s, (255, 250, 220), (VW // 2 + 54, sun_y), 8)
    rnd = random.Random(21)
    for _ in range(14):                                          # long flat clouds
        cx, cy = rnd.uniform(0, VW), rnd.uniform(12, SEA_Y - 20)
        w, h = rnd.uniform(18, 54), rnd.uniform(2, 4)
        col = _mix((255, 196, 150), (120, 70, 110), (cy - 12) / 60.0)
        pygame.draw.ellipse(s, col, (cx, cy, w, h))
        pygame.draw.ellipse(s, lighten(col, 0.25), (cx + 3, cy, w * 0.6, max(1, h - 1)))
    for i, (x, w, h) in enumerate(((22, 46, 9), (250, 60, 12))):   # islands on the horizon
        pts = [(x, SEA_Y), (x + w * 0.3, SEA_Y - h), (x + w * 0.55, SEA_Y - h * 0.6),
               (x + w * 0.75, SEA_Y - h * 1.1), (x + w, SEA_Y)]
        pygame.draw.polygon(s, (74, 52, 86), pts)
    return s


def make_deck():
    """The foredeck of the boat: planks, rail, and the shadow under the awning."""
    s = pygame.Surface((VW, VH - DECK_Y), pygame.SRCALPHA)
    h = s.get_height()
    for y in range(h):
        u = y / float(h)
        s.fill(_mix((214, 182, 136), (154, 118, 80), u), (0, y, VW, 1))
    for x in range(-8, VW, 17):                                  # planking
        off = int((x // 17) % 2)
        s.fill((126, 94, 62), (x + off, 0, 1, h))
    for y in range(3, h, 9):
        s.fill((178, 146, 104), (0, y, VW, 1))
    s.fill((248, 246, 240), (0, 0, VW, 2))                       # the gunwale cap
    s.fill((176, 172, 166), (0, 2, VW, 1))
    return s


class Yacht:
    """The last scene: champion, trainer, open water, nothing left to prove."""

    def __init__(self, game):
        self.game = game
        self.sky = make_yacht_sky()
        self.deck = make_deck()
        self.t = 0.0
        self.gulls = [[random.uniform(0, VW), random.uniform(20, 56), random.uniform(7, 16), random.uniform(0, 6.3)]
                      for _ in range(5)]
        self.glints = []

    def reset(self):
        self.t = 0.0
        self.glints = []

    def update(self, dt):
        self.t += dt
        for g in self.gulls:
            g[0] += g[2] * dt
            if g[0] > VW + 10:
                g[0] = -10
                g[1] = random.uniform(20, 56)
            g[3] += dt * 5
        if random.random() < dt * 22:
            self.glints.append([random.uniform(0, VW), random.uniform(SEA_Y + 2, DECK_Y - 2), 0.0,
                                random.uniform(0.4, 0.9)])
        for s in self.glints:
            s[2] += dt
        self.glints = [s for s in self.glints if s[2] < s[3]]

    def draw(self, c):
        t = self.t
        c.blit(self.sky, (0, 0))
        # --- the sea: bands of moving water, brightest under the sun
        for y in range(SEA_Y, DECK_Y):
            u = (y - SEA_Y) / float(DECK_Y - SEA_Y)
            base = _mix((52, 58, 120), (28, 32, 78), u)
            c.fill(base, (0, y, VW, 1))
        for y in range(SEA_Y, DECK_Y, 2):
            u = (y - SEA_Y) / float(DECK_Y - SEA_Y)
            amp = 3 + 16 * u
            ph = t * (0.7 + u * 1.5) + y * 0.7
            x = int(VW // 2 + 54 + math.sin(ph) * amp)
            w = int(10 + 44 * u)
            col = _mix((255, 196, 140), (226, 128, 110), u)
            c.fill(col, (x - w // 2, y, w, 1))
            c.fill(_mix(col, (255, 255, 255), 0.4), (x - w // 6, y, max(1, w // 3), 1))
        for x, y, el, life in self.glints:
            k = 1 - el / life
            c.fill((255, 240, 210) if k > 0.5 else (210, 200, 230), (int(x), int(y), 2, 1))
        for gx, gy, _, ph in self.gulls:                          # distant birds
            flap = math.sin(ph) * 2
            x, y = int(gx), int(gy)
            pygame.draw.line(c, (40, 36, 60), (x - 3, y + flap), (x, y))
            pygame.draw.line(c, (40, 36, 60), (x, y), (x + 3, y + flap))
        c.blit(self.deck, (0, DECK_Y))
        self.draw_rail(c)
        self.draw_furniture(c)

    def draw_rail(self, c):
        y = DECK_Y - 22
        for x in range(10, VW, 36):                               # stanchions
            c.fill((40, 38, 50), (x, y, 3, 24))
            c.fill((214, 216, 226), (x, y, 2, 24))
            c.fill((255, 255, 255), (x, y, 1, 24))
        for yy, th in ((y, 2), (y + 9, 1)):                       # top rail and the wire below it
            c.fill((40, 38, 50), (0, yy + th, VW, 1))
            c.fill((226, 228, 238), (0, yy, VW, th))

    def draw_furniture(self, c):
        g = self.game
        deck = DECK_Y + 28                                   # the line the feet stand on
        # --- you, out on the planks with the belt round your waist
        frames = g.frames
        fr = IDLE_SEQ[int(self.t * 3.4) % len(IDLE_SEQ)]
        sx = 74
        sy = deck - SPRITE_FEET
        c.blit(g.shadow, (sx - 24, deck - 6))
        c.blit(frames[fr], (sx - HIP_X, sy))
        c.blit(g.belt, (sx - HIP_X + 21, sy + 41 + int(math.sin(self.t * 1.3))))
        # --- a little table with two cold ones between you
        tx, ty = 138, deck - 20
        c.fill((30, 26, 38), (tx - 1, ty + 7, 30, 15))
        c.fill((236, 232, 224), (tx, ty + 6, 28, 4))
        c.fill((186, 180, 172), (tx + 11, ty + 10, 6, 12))
        c.fill((30, 26, 38), (tx + 9, ty + 21, 10, 2))
        for i, dx in enumerate((4, 20)):
            c.fill((30, 26, 38), (tx + dx - 1, ty - 2, 6, 10))
            c.fill((255, 226, 140) if i == 0 else (190, 232, 255), (tx + dx, ty - 1, 4, 8))
            c.fill((255, 255, 255), (tx + dx, ty - 1, 4, 1))
            c.fill((255, 120, 140), (tx + dx + 2, ty - 3, 2, 2))
        # --- Doc, flat out in a lounger, finally off his feet
        self.draw_doc(c, 196, deck - 24)

    def draw_doc(self, c, x, y):
        """A lounger with the old man in it, straw hat tipped down over the eyes."""
        ol, canvas, canvas_s = (34, 28, 44), (84, 142, 206), (56, 102, 156)
        shirt, flower1, flower2 = (250, 242, 206), (236, 120, 110), (132, 198, 148)
        skin, skin_s, hair = (176, 124, 86), (138, 94, 64), (228, 228, 234)
        pygame.draw.polygon(c, ol, [(x - 3, y + 34), (x + 20, y + 4), (x + 28, y + 10), (x + 7, y + 37)])
        pygame.draw.polygon(c, canvas, [(x, y + 33), (x + 20, y + 7), (x + 25, y + 11), (x + 6, y + 35)])
        pygame.draw.polygon(c, canvas_s, [(x + 2, y + 34), (x + 22, y + 9), (x + 25, y + 11), (x + 6, y + 35)])
        c.fill(ol, (x + 5, y + 32, 52, 8))
        c.fill(canvas, (x + 6, y + 33, 50, 6))
        c.fill(canvas_s, (x + 6, y + 37, 50, 2))
        for lx in (x + 10, x + 50):
            c.fill(ol, (lx, y + 39, 4, 9))
            c.fill((70, 66, 84), (lx + 1, y + 39, 2, 9))
        c.fill(ol, (x + 11, y + 15, 21, 20))                  # reclined torso
        c.fill(shirt, (x + 12, y + 16, 19, 18))
        for row, col in ((y + 18, flower1), (y + 23, flower2), (y + 28, flower1)):
            for sx2 in range(x + 13, x + 30, 5):
                c.fill(col, (sx2, row, 2, 2))
        c.fill(ol, (x + 29, y + 30, 28, 9))                   # legs along the seat
        c.fill((68, 88, 148), (x + 29, y + 31, 26, 7))
        c.fill((52, 68, 120), (x + 29, y + 36, 26, 2))
        c.fill(ol, (x + 53, y + 29, 9, 9))                    # white sneakers, always
        c.fill((238, 234, 228), (x + 54, y + 30, 7, 7))
        c.fill((186, 182, 176), (x + 54, y + 35, 7, 2))
        c.fill(ol, (x + 7, y + 24, 7, 11))                    # near arm hanging off the side
        c.fill(shirt, (x + 8, y + 25, 5, 6))
        c.fill(skin, (x + 8, y + 31, 5, 4))
        pygame.draw.circle(c, ol, (x + 13, y + 10), 8)        # head
        pygame.draw.circle(c, skin, (x + 13, y + 10), 7)
        c.fill(skin_s, (x + 8, y + 11, 3, 4))
        c.fill(hair, (x + 7, y + 5, 12, 3))
        c.fill(skin_s, (x + 15, y + 14, 4, 1))                # the line of a mouth
        c.fill(ol, (x + 2, y + 1, 23, 5))                     # straw hat, pulled down
        c.fill((242, 230, 192), (x + 3, y + 2, 21, 3))
        c.fill((214, 194, 152), (x + 3, y + 4, 21, 1))
        c.fill((196, 90, 90), (x + 5, y + 2, 17, 1))
        c.fill((30, 26, 38), (x + 14, y + 9, 6, 3))           # sunglasses
        c.fill((90, 150, 210), (x + 15, y + 9, 2, 1))


# ============================================================ the info button
INFO_CENTER = (15, VH - 13)      # the little "i" in the bottom-left corner
INFO_D, INFO_D_HOVER = 17, 21    # its size normally / under the pointer
INFO_PANEL = pygame.Rect(8, 2, VW - 16, 156)
MOVE_ROWS = (("ARROWS", "MOVE / CIRCLE"), ("A", "JAB"), ("S", "CROSS"), ("D", "BODY JAB"), ("F", "BODY CROSS"),
             ("W (+DIR)", "SLIP / STEP"), ("E / R HOLD", "BLOCK HI / LOW"), ("SHIFT+A..F", "FEINT"),
             ("Q", "CLINCH"), ("X", "PIVOT"))
FIGHT_TIPS = ("Slip then punch = COUNTER", "Block late = PARRY", "Step off his line: W + ARROW",
              "Body shots cut healing", "Feint him, then land big", "Guard up = wind back",
              "X pivots you off the ropes", "3 knockdowns = T.K.O.", "Mash A S D F to get up")


def make_info_icon(d, fill, ring, glyph, ring_w=1, halo=3):
    """A round, see-through "i" badge, on a soft dark halo so it reads over anything."""
    pad = 4
    s = pygame.Surface((d + pad * 2, d + pad * 2), pygame.SRCALPHA)
    r = d // 2
    mid = (d // 2 + pad, d // 2 + pad)
    for k in range(halo, 0, -1):                                 # soft shadow around the badge
        pygame.draw.circle(s, (6, 5, 14, 42), mid, r + k)
    pygame.draw.circle(s, fill, mid, r)
    pygame.draw.circle(s, ring, mid, r, ring_w)
    w = int(round(d / 8.0))
    x = mid[0] - w // 2
    s.fill(glyph, (x, int(mid[1] - d * 0.28), w, w))             # the dot
    s.fill(glyph, (x, int(mid[1] - d * 0.08), w, int(d * 0.36)))  # the stem
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
    def __init__(self, game, frames, facing, sets=None, views=None):
        self.game = game
        self.ang = 0.0 if facing > 0 else math.pi    # which way he faces, in the ring (0 = right, +pi/2 = toward you)
        self.view = "side"
        self.views = views or {"side": sets or (frames, frames)}
        self.frames = frames
        self.pro_regen = False         # True for YOU: blocking and footwork give wind back
        self.configure()
        self.reset(72)

    # --- which way he faces. `facing` is the left/right half of it, kept for everything 2D.
    @property
    def facing(self):
        return 1 if math.cos(self.ang) >= 0 else -1

    @facing.setter
    def facing(self, d):
        self.ang = 0.0 if d > 0 else math.pi
        self.pick_view()

    def u(self):
        return math.cos(self.ang), math.sin(self.ang)

    def configure(self, max_hp=MAX_HP, power=1.0, speed=1.0, walk=1.0, chin=1.0, heart=1.0, wind=1.0):
        """Per-boxer stats: health, punch damage multiplier, animation speed, footspeed,
        chin (how much his head can take), heart (how hard he fights to beat the count)
        and wind (his gas tank: how slowly he tires and how fast he gets his breath back)."""
        self.max_hp, self.power, self.speed, self.walk = float(max_hp), power, speed, walk
        self.chin, self.heart, self.wind = chin, heart, wind

    def reset(self, x, z=Z_START):
        self.x = float(x)
        self.z = float(z)              # depth: + toward the camera (feet drawn at GROUND + z * ZK)
        self.track_left = 0.0          # how much more this punch may turn after him
        self.side_t, self.side_cd = 0.0, 0.0
        self.side_v = (0.0, 0.0)       # direction of the side-step
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
        self.ko_style = "kneel"        # how a finished fighter is shown: kneel / stand (ref stoppage)
        self.end_t = 0.0
        self.ghosts = []
        # --- clinch
        self.clinch = False
        self.clinch_t = 0.0
        self.clinch_cd = 0.0
        # --- pivot: a quick roll round him
        self.pivot_t = 0.0             # >0 while rolling round him
        self.pivot_cd = 0.0
        self.pivot_c = (0.0, 0.0)      # the man you are rolling round
        self.pivot_a0 = self.pivot_a1 = 0.0
        self.pivot_r = 0.0
        # --- feints
        self.bait_t = 0.0              # >0: he bit on your feint, hit him NOW
        self.feinted_t = 0.0           # >0: you just threw a feint
        # --- stamina
        self.stam = float(STAM_MAX)
        self.stam_t = 99.0             # seconds since the last punch thrown
        self.gassed = False
        self.puff_t = 0.0              # breathing-hard puffs
        # --- knockdown system
        self.daze, self.daze_t = 0.0, 99.0   # hidden concussion meter (head shots)
        self.body_dmg = 0.0                  # hidden body damage (for liver shots)
        self.hurt = False                    # wobbling: gloves down, slow, wide open
        self.downs = 0                       # times knocked down this fight
        self.kds = 0                         # knockdowns scored on the other guy
        self.dealt = 0.0                     # damage landed (judges' scorecards)
        self.unanswered = 0                  # clean shots taken in a row without landing one back
        self.down = False                    # on the canvas, being counted
        self.down_t = 0.0
        self.rising_t = -1.0                 # >= 0 while getting back up
        self.out_cold = False                # flat on his back - fight over
        self.fall_t = 0.0
        self.liver_t = 0.0                   # >0: about to fold from a liver shot
        self.pick_view()

    # ------------------------------------------------------------ views
    def set_views(self, views):
        """views: {"side": (right, left), "fq": (right, left), "bq": (right, left), "f": set, "b": set}"""
        self.views = views
        self.pick_view(force=True)

    def set_sets(self, right, left):
        """Side-on sprites only (no turning toward / away from the camera)."""
        self.set_views({"side": (right, left)})

    def pick_view(self, force=False):
        """Choose the drawing for the way he is facing: side-on, three-quarter, face-on or back-on.
        A few degrees of stickiness at the edges stop him flickering between two drawings."""
        vs = getattr(self, "views", None)
        if not vs:
            return
        deg = math.degrees(math.atan2(math.sin(self.ang), math.cos(self.ang)))
        if len(vs) == 1 or getattr(self.game, "mode", "bag") == "bag" or getattr(self, "out_cold", False):
            key = "side"
        else:
            def sector(d):
                a = abs(d)
                if a <= 22.5 or a >= 157.5:
                    return "side"
                if 67.5 <= a <= 112.5:
                    return "f" if d > 0 else "b"
                return "fq" if d > 0 else "bq"
            key = sector(deg)
            if not force and key != self.view:
                # only switch once he is clearly into the new sector
                if sector(deg + VIEW_STICK) == self.view or sector(deg - VIEW_STICK) == self.view:
                    key = self.view
        self.view = key
        v = vs.get(key) or vs["side"]
        if isinstance(v, tuple):
            self.frames = v[0] if math.cos(self.ang) >= 0 else v[1]
        else:
            self.frames = v

    def side_frames(self):
        right, left = self.views["side"]
        return right if self.facing > 0 else left

    # ------------------------------------------------------------ state queries
    def busy(self):
        return (self.ko or self.won or self.stun_t > 0 or self.hitstun > 0 or self.down or self.out_cold
                or self.liver_t > 0 or self.clinch or self.pivot_t > 0 or self.side_t > 0)

    def sidestep(self, vec):
        """A quick step off his line in direction vec (world x, z)."""
        if self.busy() or self.side_cd > 0 or self.stam < SIDESTEP_STAM or self.action not in (None,) + PUNCHES:
            return False
        if self.action and self.idx < ACTIONS[self.action]["cancel"]:
            return False
        vx, vz = vec
        l = math.hypot(vx, vz) or 1.0
        vx, vz = vx / l, vz / l
        ex, ez = self.x + vx * SIDESTEP, self.z + vz * SIDESTEP
        if not (MIN_X <= ex <= STAGE_MAX_X and Z_MIN <= ez <= Z_MAX):
            vx, vz = -vx, -vz                       # no room that way: go the other
        self.finish_action()
        self.block = None
        self.side_t, self.side_v, self.side_cd = SIDESTEP_TIME, (vx, vz), SIDESTEP_CD
        self.spend(SIDESTEP_STAM)
        self.ghosts.append(self.make_ghost())
        self.game.snd("slip")
        return True

    def gy(self):
        """The floor line this fighter is standing on."""
        return GROUND + int(round(self.z * ZK))

    def foe(self):
        return self.game.cpu if self is self.game.player else self.game.player

    def face(self, d):
        """Turn square to face left / right at once (walk-ins, the bag)."""
        if d and not self.action and not self.clinch:
            self.ang = 0.0 if d > 0 else math.pi
            self.pick_view()

    def turn_to(self, target, rate, dt):
        """Turn toward angle `target` at up to `rate` rad/s. Returns how much he turned."""
        diff = (target - self.ang + math.pi) % math.tau - math.pi
        step = clamp(diff, -rate * dt, rate * dt) if dt is not None else diff
        self.ang = (self.ang + step + math.pi) % math.tau - math.pi
        return abs(step)

    def angle_to(self, other):
        return math.atan2(other.z - self.z, other.x - self.x)

    def spd(self):
        """Animation speed right now: hurt and gassed fighters punch slower."""
        return self.speed * (0.82 if self.hurt else 1.0) * (0.78 if self.gassed else 1.0)

    def on_ropes(self):
        """Backed up against the ring edge with nowhere to go: the ropes are right behind him."""
        ux, uz = self.u()
        bx, bz = self.x - ux * ROPE_ZONE, self.z - uz * ROPE_ZONE
        return bx < MIN_X or bx > STAGE_MAX_X or bz < Z_MIN or bz > Z_MAX

    def gas(self):
        """0 at full wind, 1 when the tank is empty - how far into the red he is."""
        if self.stam >= GAS_LINE:
            return 0.0
        return (GAS_LINE - self.stam) / GAS_LINE

    def punch_power(self):
        """Damage multiplier: tired arms don't carry the same snap."""
        return self.power * (1.0 - 0.3 * self.gas())

    def spend(self, amount):
        self.stam = max(0.0, self.stam - amount / self.wind)
        self.gassed = self.stam < GAS_LINE

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
        self.spend(STAM_COST["feint"] if name in FEINTS else STAM_COST.get(name, 5.0))
        self.stam_t = 0.0
        self.track_left = TRACK_MAX if name in PUNCHES or name in FEINTS else 0.0
        if self.game.mode != "bag":
            o = self.foe()
            # you throw it at where he is NOW (you were already facing him, near enough)
            self.track_left -= self.turn_to(self.angle_to(o), TRACK_SNAP, 1.0)
            self.track_left = max(0.0, self.track_left)
        if name in FEINTS:
            self.attack_id += 1        # it looks exactly like the real thing coming
            self.feinted_t = 0.4
            self.game.snd("swish")
            return
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
        pair = F_HIT_HEAD if target == "head" else F_HIT_BODY
        self.react = pair if random.random() < 0.6 else (pair[1], pair[0])
        self.react_t, self.react_total = 0.0, stun

    def stagger(self, dur):
        self.finish_action()
        self.block = None
        self.buffer = None
        self.hitstun = 0.0
        self.stun_t, self.stun_el = dur, 0.0

    def push(self, px):
        """Knocked straight back (away from where he faces), stopped by the ropes."""
        ux, uz = self.u()
        self.x = clamp(self.x - ux * px, MIN_X, STAGE_MAX_X)
        if self.game.mode != "bag":
            self.z = clamp(self.z - uz * px, Z_MIN, Z_MAX)

    def make_ghost(self, frame=None):
        img = self.frames[IDLE_SEQ[self.idle_i] if frame is None else frame].copy()
        img.fill((50, 80, 150, 0), special_flags=pygame.BLEND_RGB_ADD)
        return dict(img=img, x=self.sprite_x(), y=self.sprite_y(), t=0.0, life=0.26)

    # ------------------------------------------------------------ geometry
    def lunge(self):
        return ACTIONS[self.action]["lunge"][self.idx] if self.action else 0

    def sprite_x(self):
        ux, _ = self.u()
        x = int(round(self.x + ux * self.lunge()))
        return x - (FW - 1 - HIP_X if getattr(self.frames, "flip", False) else HIP_X)

    def sprite_y(self):
        _, uz = self.u()
        return GROUND + int(round((self.z + uz * self.lunge()) * ZK)) - getattr(self.frames, "feet", SPRITE_FEET)

    def tip(self, frame):
        """Where the glove is at the end of a punch, on screen."""
        fx, fy = self.game.fist[frame]
        ux, uz = self.u()
        out = fx - HIP_X + self.lunge()
        return self.x + ux * out, GROUND + (self.z + uz * out) * ZK - SPRITE_FEET + fy

    def current_frame(self):
        if self.pose_override is not None:
            return self.pose_override
        if self.out_cold:
            return F_HIT_HEAD[1]                 # drawn rotated, flat on his back
        if self.down:
            if self.rising_t >= 0:
                r = self.rising_t
                return F_KO[2] if r < 0.2 else (F_KO[1] if r < 0.42 else F_KO[0])
            return F_KO[0] if self.down_t < 0.12 else (F_KO[1] if self.down_t < 0.42 else F_KO[2])
        if self.clinch:
            return F_BLOCK_HIGH[1]
        if self.side_t > 0:
            return ACTIONS["slip"]["frames"][1]
        if self.pivot_t > 0:
            k = 1.0 - self.pivot_t / PIVOT_TIME
            return ACTIONS["slip"]["frames"][min(len(ACTIONS["slip"]["frames"]) - 1, int(k * 5))]
        if self.liver_t > 0:
            return F_HIT_BODY[1]
        if self.ko and self.ko_style == "stand":
            return F_STAGGER[int(self.end_t * 5) % len(F_STAGGER)]
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
        if self.hurt:                            # gloves down, wobbling
            return F_STAGGER[int(self.game.clock * 4.5 + self.x) % len(F_STAGGER)]
        return IDLE_SEQ[self.idle_i]

    # ------------------------------------------------------------ update
    def update(self, dt, move, min_x, max_x, zmove=0):
        self.counter_t = max(0.0, self.counter_t - dt)
        self.bait_t = max(0.0, self.bait_t - dt)
        self.clinch_cd = max(0.0, self.clinch_cd - dt)
        self.pivot_cd = max(0.0, self.pivot_cd - dt)
        self.side_cd = max(0.0, self.side_cd - dt)
        self.feinted_t = max(0.0, self.feinted_t - dt)
        self.parry_cd = max(0.0, self.parry_cd - dt)
        self.block_hit_t = max(0.0, self.block_hit_t - dt)
        for g in self.ghosts:
            g["t"] += dt
        self.ghosts = [g for g in self.ghosts if g["t"] < g["life"]]
        self._update(dt, move, min_x, max_x, zmove)
        self.pick_view()

    def _update(self, dt, move, min_x, max_x, zmove):
        # healing: after REGEN_DELAY seconds untouched, heal up to the cap
        self.since_damage += dt
        self.healing = (not self.ko and not self.down and self.hp > 0 and self.since_damage >= REGEN_DELAY
                        and self.hp < self.regen_cap)
        if self.healing:
            self.hp = min(float(self.regen_cap), self.hp + REGEN_RATE * dt)
        if self.hp_lag > self.hp:
            self.hp_lag = max(self.hp, self.hp_lag - 30 * dt)
        else:
            self.hp_lag = self.hp

        # stamina: recovers once you stop punching, fastest when you stand off and breathe
        self.stam_t += dt
        if self.stam_t >= STAM_REGEN_DELAY and not (self.down or self.out_cold):
            rate = STAM_REGEN * self.wind
            if self.block:
                rate *= STAM_GUARD_REGEN if self.pro_regen else 1.0
            elif self.moving:
                rate *= STAM_MOVE_REGEN if self.pro_regen else 1.0
            elif not self.action:
                rate *= STAM_REGEN_IDLE
            self.stam = min(float(STAM_MAX), self.stam + rate * dt)
        if not self.pro_regen:                     # the computer still burns wind holding on
            if self.block:
                self.spend(STAM_HOLD * dt)
            elif self.moving:
                self.spend(STAM_MOVE * dt)
        self.gassed = self.stam < GAS_LINE
        if self.gassed and not (self.down or self.out_cold or self.ko):
            self.puff_t -= dt
            if self.puff_t <= 0:
                self.puff_t = random.uniform(0.35, 0.6)
                self.game.puff(self)

        # concussion / body damage wear off slowly
        self.daze_t += dt
        if self.daze_t >= DAZE_DELAY:
            self.daze = max(0.0, self.daze - DAZE_DECAY * dt)
        if self.hurt and self.daze < HURT_EXIT:
            self.hurt = False
            self.unanswered = 0
        self.body_dmg = max(0.0, self.body_dmg - BODY_DECAY * dt)
        if self.side_t > 0:                      # stepping off his line
            step = min(self.side_t, dt) / SIDESTEP_TIME * SIDESTEP
            self.x = clamp(self.x + self.side_v[0] * step, MIN_X, STAGE_MAX_X)
            self.z = clamp(self.z + self.side_v[1] * step, Z_MIN, Z_MAX)
            self.side_t = max(0.0, self.side_t - dt)
            self.moving = 2
            if self.side_t <= 0:
                self.counter_t = max(self.counter_t, COUNTER_WINDOW * 0.6)   # step off, fire back
            return
        if self.pivot_t > 0:                     # rolling round him: untouchable, and moving
            self.pivot_t = max(0.0, self.pivot_t - dt)
            k = 1.0 - self.pivot_t / PIVOT_TIME
            ease = k * k * (3 - 2 * k)
            a = self.pivot_a0 + (self.pivot_a1 - self.pivot_a0) * ease
            cx, cz = self.pivot_c
            self.x = clamp(cx + math.cos(a) * self.pivot_r, MIN_X, STAGE_MAX_X)
            self.z = clamp(cz + math.sin(a) * self.pivot_r, Z_MIN, Z_MAX)
            self.ang = math.atan2(cz - self.z, cx - self.x)           # eyes on him all the way round
            if random.random() < dt * 40:
                self.ghosts.append(self.make_ghost(self.current_frame()))
            self.moving = 0
            if self.pivot_t <= 0:
                self.counter_t = COUNTER_WINDOW   # come up off the pivot and he is yours
            return
        if self.clinch:                          # tied up: catch your breath and clear your head
            self.stam = min(float(STAM_MAX), self.stam + CLINCH_STAM * dt)
            self.gassed = self.stam < GAS_LINE
            self.daze = max(0.0, self.daze - CLINCH_DAZE * dt)
            if self.hurt and self.daze < HURT_EXIT:
                self.hurt = False
            self.moving = 0
            return
        if self.down or self.out_cold:
            self.down_t += dt
            self.fall_t += dt
            if self.rising_t >= 0:
                self.rising_t += dt
            self.moving = 0
            return
        if self.liver_t > 0:                     # doubled over, about to go down (Game counts it down)
            self.moving = 0
            return

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
        self.update_locomotion(dt, move, min_x, max_x, zmove)

    def update_action(self, dt):
        spec = ACTIONS[self.action]
        if self.track_left > 0 and not self.hit_done and self.game.mode != "bag":
            # the punch keeps turning after him - but only so fast, and only so far
            o = self.foe()                       # (a sudden side-step is too quick to follow)
            turned = self.turn_to(self.angle_to(o), TRACK_RATE * (0.25 if o.side_t > 0 else 1.0), dt)
            self.track_left = max(0.0, self.track_left - turned)
        self.t += dt * 1000.0 * self.spd()
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

    def update_locomotion(self, dt, move, min_x, max_x, zmove=0):
        """Walk in any direction on screen (move = left/right, zmove = up/down the ring).
        Close to him, the sideways part of a step goes ROUND him, so you circle at the same range."""
        if self.game.mode == "bag":
            zmove = 0
        mx, mz = float(move), float(zmove)
        l = math.hypot(mx, mz)
        if l < 1e-6:
            self.moving = 0
            self.walk_t = 0.0
            self.idle_t += dt * 1000.0
            while self.idle_t >= IDLE_MS:
                self.idle_t -= IDLE_MS
                self.idle_i = (self.idle_i + 1) % len(IDLE_SEQ)
            return
        mx, mz = mx / max(1.0, l), mz / max(1.0, l)
        ux, uz = self.u()
        along = (mx * ux + mz * uz) / max(1e-6, math.hypot(mx, mz))
        fwd = along > -0.35
        speed = (WALK_FWD if fwd else WALK_BACK) * self.walk * (0.6 if self.hurt else 1.0)
        dx, dz = mx * speed * dt, mz * speed * dt
        o = self.foe() if self.game.mode != "bag" else None
        if o is not None and self.game.phase == "fight" and not (o.down or o.out_cold or o.ko):
            rx, rz = self.x - o.x, self.z - o.z
            r = math.hypot(rx, rz)
            if 1.0 < r < ORBIT_RANGE:
                nx, nz = rx / r, rz / r                  # out from him
                radial = dx * nx + dz * nz
                tang = dx * -nz + dz * nx                # round him
                a = math.atan2(rz, rx) + tang / r
                r2 = r + radial
                dx = o.x + math.cos(a) * r2 - self.x
                dz = o.z + math.sin(a) * r2 - self.z
        ox, oz = self.x, self.z
        self.x = clamp(self.x + dx, min_x, max_x)
        if self.game.mode != "bag":
            self.z = clamp(self.z + dz, Z_MIN, Z_MAX)
        moved = abs(self.x - ox) + abs(self.z - oz) > 1e-6
        if moved:
            self.moving = 2 if abs(along) < 0.45 else (1 if fwd else -1)    # 2 = circling / stepping across
            self.walk_t += dt * 1000.0
            step = 85.0 if fwd else 95.0
            while self.walk_t >= step:
                self.walk_t -= step
                self.walk_i = (self.walk_i + (-1 if self.moving == -1 else 1)) % WALK_FRAMES
        else:
            self.moving = 0
            self.walk_t = 0.0

    # ------------------------------------------------------------ drawing
    def fall_angle(self):
        """Out cold: tips over backwards like a felled tree, with a little bounce."""
        t = self.fall_t
        if t < 0.42:
            k = t / 0.42
            return 90 * k * k
        if t < 0.62:
            return 90 - 9 * math.sin((t - 0.42) / 0.2 * math.pi)
        return 90

    def lying(self):
        """(image, x, y) of the out-cold fighter, kept on screen and resting on the canvas."""
        ang = int(round(self.fall_angle() / 6)) * 6
        r = self.game.rotated(self.side_frames(), F_HIT_HEAD[1], ang * self.facing, self.facing)
        x = int(self.x) - r["px"]
        y = min(self.gy() - r["py"], self.gy() + 1 - r["bottom"])    # pivot on the floor, never sink into it
        x = int(clamp(x, 2 - r["left"], VW - 2 - r["right"]))
        return r["img"], x, y

    def head_pos(self):
        """Where his head is right now (for dizzy stars, speech bubbles, the rain cloud)."""
        if self.out_cold:
            img, x, y = self.lying()
            w = img.get_width()
            hx = x + (10 if self.facing > 0 else w - 10)
            return hx, self.gy() - 10
        top, cx = self.game.frame_top(self.frames, self.current_frame())
        return self.sprite_x() + cx, self.sprite_y() + top + 5

    def draw(self, c, alpha=255):
        if self.out_cold:
            img, x, y = self.lying()
            sh = pygame.transform.scale(self.game.shadow, (img.get_width(), 8))
            c.blit(sh, (x, self.gy() - 5))
            c.blit(img, (x, y))
            return
        c.blit(self.game.shadow, (int(self.x) - 24 + 3 * self.facing, self.gy() - 5))
        for g in self.ghosts:
            g["img"].set_alpha(int(120 * (1 - g["t"] / g["life"])))
            c.blit(g["img"], (g["x"], g["y"]))
        frame, sx, sy = self.current_frame(), self.sprite_x(), self.sprite_y()
        if self.belt:                  # drawn first so the gloves grip it
            top, cx = self.game.frame_top(self.frames, frame)
            b = self.game.belt
            c.blit(b, (sx + cx - b.get_width() // 2, sy + top - 1))
        img = self.frames[frame]
        if alpha < 255:
            img = img.copy()
            img.set_alpha(alpha)
        c.blit(img, (sx, sy))


def edge_room(f):
    """How far he is from the nearest rope."""
    return min(f.x - MIN_X, STAGE_MAX_X - f.x, f.z - Z_MIN, Z_MAX - f.z)


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
        self.learn_rate = self.params.get("learn", 1.0)

    def reset(self):
        L = self.params
        self.atk_t = random.uniform(*L["atk"]) + 0.4
        self.plan = []
        self.def_plan = None
        self.seen = -1
        self.move = 0
        self.zmove = 0
        self.circle_t, self.circle_dir = 0.0, 1  # circling round you
        self.retreat_t = 0.0
        self.step_t, self.step_dir = 0.0, 0
        self.guard_t, self.guard_level = 0.0, "high"
        self.punish = False
        self.foe_body = []
        self.foe_times = []
        self.clock = 0.0
        # --- reading the man in front of him
        self.habit = {n: 1.0 for n in PUNCHES}   # decaying count of what the other guy throws
        self.last_punch = None
        self.pairs = {}                          # (punch, next punch) -> how often he does it
        self.expect = None                       # the punch he is expecting next
        self.feint_wise = 0.0                    # how wise he currently is to your feints (it fades)
        self.block_rest = 0.0                    # just blocked: committed for a moment
        self.pin_t = 0.0                         # how long he has had you stuck on the ropes
        self.reset_t = 0.0                       # backing off out of range to let it breathe
        self.read_t = 0.0                        # >0 while he has your number (shown on screen)

    def toward(self, foe):
        """Which way is the other man from here (+1 right, -1 left)."""
        return 1 if foe.x > self.me.x else -1

    def learn(self, name):
        """Remember what he keeps throwing, and what he likes to throw after it."""
        for k in self.habit:
            self.habit[k] *= 0.93                # old habits fade
        self.habit[name] = self.habit.get(name, 1.0) + 1.0
        if self.last_punch:
            key = (self.last_punch, name)
            self.pairs[key] = self.pairs.get(key, 0.0) + 1.0
            nxt = max(((v, k[1]) for k, v in self.pairs.items() if k[0] == name), default=(0, None))
            self.expect = nxt[1] if nxt[0] >= 2.5 else None
        self.last_punch = name

    def share(self, name):
        tot = sum(self.habit.values())
        return self.habit.get(name, 0.0) / tot if tot else 0.25

    def read_bonus(self, name):
        """How well he has your number on this punch: 0 if you mix it up, up to ~0.3 if you spam one."""
        over = self.share(name) - 0.33
        if self.expect == name:
            over += 0.1                          # and he saw this one coming in the combo
        b = clamp(over * 0.9 * self.learn_rate, 0.0, 0.3)
        if b > 0.16:
            self.read_t = 1.2
        return b

    def choose_attack(self, L, foe):
        pace = L.get("pace", 1.0)
        if self.me.stam < 45 * pace:              # low on wind: pick your shots, mostly jabs
            if self.me.stam < 26 * pace:
                return ["jab"]
            return random.choice([["jab"], ["jab"], ["jab", "jab"], ["body_jab"], ["jab", "cross"]])
        if foe.hurt:                              # smells blood: power shots to finish him
            return random.choice([["jab", "cross", "cross"], ["cross", "body_cross", "cross"], ["jab", "cross"],
                                  ["body_jab", "cross", "cross"], ["cross", "cross"]])
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

    def vec(self, radial, tang):
        """'In / out' and 'round him' turned into a direction on the floor.
        tang > 0 goes round him one way (anticlockwise on screen), < 0 the other."""
        me, foe = self.me, self.foe
        rx, rz = foe.x - me.x, foe.z - me.z
        r = math.hypot(rx, rz) or 1.0
        nx, nz = rx / r, rz / r
        return nx * radial + nz * tang, nz * radial - nx * tang

    def go(self, radial, tang=0.0):
        self.move, self.zmove = self.vec(radial, tang)

    def to_middle(self, f=None):
        """Which way round (+1 / -1) heads toward the middle of the ring."""
        me = f or self.me
        cx, cz = (MIN_X + STAGE_MAX_X) / 2, (Z_MIN + Z_MAX) / 2
        a, b = self.vec(0, 1)
        return 1 if a * (cx - me.x) + b * (cz - me.z) >= 0 else -1

    def cut_off(self):
        """Step round so you stand between him and the middle of the ring: cutting off the ring."""
        me, foe = self.me, self.foe
        cx, cz = (MIN_X + STAGE_MAX_X) / 2, (Z_MIN + Z_MAX) / 2
        want = math.atan2(cz - foe.z, cx - foe.x)
        now = math.atan2(me.z - foe.z, me.x - foe.x)
        diff = (want - now + math.pi) % math.tau - math.pi
        if abs(diff) < 0.3:
            return 0
        return 1 if diff > 0 else -1

    def on_line(self, slack=0.0):
        """Squared up on him, so a punch thrown now is going at him."""
        me = self.me
        diff = abs((me.angle_to(self.foe) - me.ang + math.pi) % math.tau - math.pi)
        return diff <= 0.3 + slack * 0.03

    def update(self, dt):
        me, foe, L = self.me, self.foe, self.params
        R = self.game.ranges
        self.move = self.zmove = 0
        self.clock += dt
        self.read_t = max(0.0, self.read_t - dt)
        self.block_rest = max(0.0, self.block_rest - dt)
        self.feint_wise = max(0.0, self.feint_wise - 0.3 * dt)   # space them out and they work again
        # --- he will not tee off on a man in the corner forever: after a sustained burst he
        #     steps back out to mid-range and makes you come to him.
        if foe.on_ropes() and self.game.dist() < MIN_SEP + 20 and me.action in PUNCHES:
            self.pin_t += dt
        else:
            self.pin_t = max(0.0, self.pin_t - dt * 0.8)
        if self.pin_t > PIN_PATIENCE and self.reset_t <= 0:
            self.pin_t = 0.0
            self.reset_t = random.uniform(*PIN_RESET)
        if self.reset_t > 0:
            self.reset_t -= dt
            self.go(-1, 0.5 * self.circle_dir)   # give him room to come off the ropes
            if self.reset_t > 0.25:
                return
        if me.busy():
            self.plan.clear()
            self.def_plan = None
            self.guard_t = 0.0
            me.want_block = None
            return
        dist = self.game.dist()
        aimed = abs((foe.angle_to(me) - foe.ang + math.pi) % math.tau - math.pi) < 0.6

        # --- notice punches (and feints) coming in
        if foe.action in THREATS and foe.attack_id != self.seen:
            self.seen = foe.attack_id
            feint = foe.action in FEINTS
            real = FEINT_OF.get(foe.action, foe.action)
            target = ACTIONS[foe.action]["target"]
            self.foe_body = (self.foe_body + [target == "body"])[-4:]
            self.foe_times = [t for t in self.foe_times if self.clock - t < 1.2] + [self.clock]
            react = (L["react"] + (0.08 if me.hp < 0.35 * me.max_hp else 0.0)
                     + (0.1 if me.hurt else 0.0) + self.read_bonus(real))
            if len(self.foe_times) >= 3:
                react -= REACT_PRESSURE        # you are letting your hands go: his reads start to go
            react = clamp(react, 0.04, REACT_CAP)
            if feint:
                react *= clamp(1.0 - self.feint_wise * 0.15, 0.3, 1.0)    # he wises up to repeated feints
            if dist <= R[real] + 6 and aimed and random.random() < react:
                if random.random() < L.get("step", 0.1) and me.side_cd <= 0:
                    kind = "step"
                elif target == "head" and random.random() < L["slip"] + 0.5 * self.read_bonus(real):
                    kind = "slip"
                else:
                    kind = "high" if target == "head" else "low"
                    if random.random() < max(0.0, L["wrong"] - self.read_bonus(real)):
                        kind = "low" if kind == "high" else "high"
                if kind not in ("slip", "step") and random.random() < L["parry"] * PARRY_SCALE:
                    # he TRIES to time it, but he is guessing at your rhythm - early is a plain
                    # block, late and the punch is already through him
                    wait = (max(0.0, time_to_active(foe) - 0.06 + random.uniform(*PARRY_JITTER))
                            if not feint else random.uniform(*L["delay"]))
                    me.parry_ok = not feint
                else:
                    wait = random.uniform(*L["delay"])
                    me.parry_ok = False
                self.def_plan = [kind, wait, 0.4]
                self.plan.clear()
                if feint:                       # he bought it - the opening is right now
                    self.feint_wise += 1
                    foe.bait_t = BAIT_WINDOW
                    self.game.on_bait(me, foe)
            if not feint:
                self.learn(real)

        # --- defend
        blocking = None
        if self.def_plan:
            kind = self.def_plan[0]
            if self.def_plan[1] > 0:
                self.def_plan[1] -= dt
            elif kind == "slip":
                me.press("slip")
                self.def_plan = None
            elif kind == "step":
                if me.sidestep(self.vec(0, self.to_middle())):
                    self.def_plan = None
                else:                            # couldn't step (cooldown / tired): cover up instead
                    tgt = ACTIONS[foe.action]["target"] if foe.action in THREATS else "head"
                    self.def_plan[0] = "high" if tgt == "head" else "low"
            elif self.punish and not foe.in_startup():
                self.def_plan = None              # punch blocked - drop the guard and punish
            else:
                blocking = kind
                self.def_plan[2] -= dt
                if self.def_plan[2] <= 0 and not (foe.action in PUNCHES and not foe.hit_done):
                    self.def_plan = None
        if (dist <= MIN_SEP + CLINCH_RANGE and me.clinch_cd <= 0 and not foe.clinch
                and (me.hurt or me.stam < 20) and random.random() < 1.3 * dt * 60 * dt):
            self.game.try_clinch(me)              # tie him up and get your head clear
            return
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
        if foe.hurt and self.atk_t > 0.5 and dist <= R["cross"] + 4 and me.stam > 35 * L.get("pace", 1.0):
            self.atk_t = random.uniform(0.2, 0.5)    # go for the finish
        self.atk_t -= dt
        if self.atk_t <= 0 and not self.plan and not me.action and not self.on_line():
            self.atk_t = 0.12                    # line him up first
        if self.atk_t <= 0 and not self.plan and not me.action:
            self.atk_t = (random.uniform(*L["atk"]) * (1.4 if me.hp < 0.3 * me.max_hp else 1.0)
                          * (1.8 if me.hurt else 1.0) * (0.6 if foe.hurt else 1.0)
                          * (1.0 + 1.6 * me.gas()))     # blowing hard: throw less, breathe more
            if dist <= R["jab"] + 2:
                self.plan = self.choose_attack(L, foe)
            else:
                self.atk_t *= 0.3
        if self.block_rest > 0:
            return
        if self.plan and not self.on_line(4):
            self.plan.clear()                    # you stepped off his line mid-combo
        if self.plan and me.can_start(self.plan[0]):
            nxt = self.plan[0]
            if (nxt in PUNCHES and me.stam > 35 and foe.block is None and not foe.busy()
                    and random.random() < L.get("feint", 0.0)):
                me.press("feint_" + nxt)          # sell it first, then throw it
                return
            me.press(self.plan.pop(0))
            if not self.plan and random.random() < 0.3:
                self.retreat_t = random.uniform(0.25, 0.5)
            return
        if me.action:
            return

        # --- sometimes just sit behind the guard (low guard if you keep going to the body)
        if (dist <= R["cross"] + 6 and me.stam > 30 * L.get("pace", 1.0)
                and random.random() < L["guard_up"] * dt * (8 if me.hurt else 2)):
            self.guard_t = random.uniform(0.5, 1.1)
            self.guard_level = "low" if sum(self.foe_body) >= 2 else "high"

        # --- footwork: in and out to hold his range, and ROUND him. Near the ropes he cuts the ring off;
        #     hurt or tired he gets on his bike and circles out toward the middle.
        desired = R["jab"] - 6 if not foe.hurt else R["cross"] - 10
        radial, tang = 0, 0.0
        if me.hurt and self.retreat_t <= 0 and random.random() < 1.5 * dt:
            self.retreat_t = random.uniform(0.5, 1.0)    # hurt: get on the bike and survive
        if self.retreat_t > 0:
            self.retreat_t -= dt
            radial = -1
            tang = 0.8 * self.to_middle() if edge_room(me) < 40 else 0.5 * self.circle_dir
        elif me.stam < 24 * L.get("pace", 1.0) and not foe.hurt and random.random() < 2.2 * dt:
            self.retreat_t = random.uniform(0.8, 1.6)    # circle away and get the breath back
        elif me.hp < 0.3 * me.max_hp and me.hp < me.regen_cap and random.random() < 0.5 * dt:
            self.retreat_t = 1.4                 # back off to try to heal
        elif self.step_t > 0:
            self.step_t -= dt
            radial = self.step_dir
        elif dist > desired + 3:
            radial = 1
        elif random.random() < 0.8 * dt:
            self.step_t = random.uniform(0.12, 0.3)
            self.step_dir = random.choice([-1, 1])
        if self.retreat_t <= 0:
            self.circle_t -= dt
            cut = L.get("cut", 0.7)
            if edge_room(foe) < 46 and cut > 0 and dist < desired + 30:
                tang = self.cut_off() * 0.8 * cut       # keep him on the ropes: step where he wants to go
            elif self.circle_t > 0:
                tang = self.circle_dir * 0.75
            elif random.random() < L.get("circle", 0.9) * dt:
                self.circle_t = random.uniform(0.35, 1.0)
                self.circle_dir = random.choice([-1, 1])
        if radial or tang:
            self.go(radial, tang)

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
        bottom = who.gy() - SPRITE_FEET + top - (9 if who.belt else 0) - 7
        if who.out_cold:
            head_x, hy = who.head_pos()
            bottom = hy - 12
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
        self.strips = {"side": strip, "f": load_strip(VIEW_F_B64), "b": load_strip(VIEW_B_B64),
                       "fq": load_strip(VIEW_FQ_B64), "bq": load_strip(VIEW_BQ_B64)}
        self.strip = strip
        self.player_views = make_views(self.strips)
        self.spar_views = make_views(self.strips, look_palette(**SPAR_LOOK))
        frames = self.player_views["side"][0]
        self.frames = frames
        self.player_sets = self.player_views["side"]
        self.spar_sets = self.spar_views["side"]
        self.spar_frames = self.spar_sets[1]
        self._fset, self._fviews, self._port = {}, {}, {}
        self.belt = make_belt()
        self.belt_small = pygame.transform.scale(self.belt, (18, 7))
        self._tops = {}
        self._rot = {}
        self.fist = {i: fist_point(frames[i]) for i in (6, 14, 15, 29, 34)}
        self.ranges = {}
        for n in PUNCHES:
            spec = ACTIONS[n]
            reach = max(self.fist[fr][0] - HIP_X + spec["lunge"][i]
                        for i, fr in enumerate(spec["frames"]) if fr in spec["active"])
            self.ranges[n] = reach + spec.get("reach", 0) + HURT[spec["target"]] + 3

        self.bg = make_background()
        self.spar_bg = make_background(ring=True)
        self.bag = Bag()
        self.crowd = Crowd()
        self.lights = make_arena_lights()
        self.rope_overlay = make_rope_overlay()
        self.sweep_glow = pygame.Surface((56, 86))
        pygame.draw.ellipse(self.sweep_glow, (34, 31, 24), (2, 0, 52, 84))
        pygame.draw.ellipse(self.sweep_glow, (64, 60, 48), (14, 16, 28, 56))
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
        self.arena_bg = make_arena_background(self.button.x)
        self.hover = None
        self.info_icon = make_info_icon(INFO_D, (14, 12, 26, 120), (186, 194, 220, 175), (216, 222, 242, 195))
        self.info_icon_hi = make_info_icon(INFO_D_HOVER, (9, 7, 18, 220), (255, 232, 130, 255),
                                           (255, 244, 200, 255), ring_w=2)
        self.info_rect = pygame.Rect(0, 0, INFO_D_HOVER + 4, INFO_D_HOVER + 4)
        self.info_rect.center = INFO_CENTER
        self.info_open = False
        self.info_t = 0.0          # 0 shut, 1 fully open
        self.info_seen = False     # has the player opened it yet?
        self._panel = {}
        self.ref = Referee(self)
        self.hype = 0.0
        self.zmove = 0
        self._taps = {}
        self.busy = 0.0
        self.seen_ids = [0, 0]
        self.clinch_by = None
        self.slowmo = 0.0
        self.dn = None
        self.mash, self.mash_need = 0.0, MASH_NEED
        self.beat_t = 0.0
        self.thud_pending = None
        self.ko_hold = 2.2
        self.method = None
        self.crowd_ch = None
        if self.sounds:
            try:
                pygame.mixer.set_num_channels(24)
                pygame.mixer.set_reserved(1)
                self.crowd_ch = pygame.mixer.Channel(0)
            except pygame.error:
                self.crowd_ch = None

        self.player = Fighter(self, frames, 1, views=self.player_views)
        self.player.pro_regen = True
        self.player.configure(chin=PLAYER_CHIN)
        self.player.reset(72)
        self.cpu = Fighter(self, self.spar_frames, -1, views=self.spar_views)
        self.ai = AI(self, self.cpu, self.player)
        self.clock = 0.0
        self.mode = "bag"
        self.idx, self.wins, self.losses, self.kos = 0, 0, 0, 0
        self.flags = set()
        self.rebuild = None
        self.scene = None
        self.scene_after = (None, None)
        self.ending = None
        self.save_data = None
        self.saved_t = 0.0
        self.menu_i = 0
        self.yacht = None
        self.card_t = 0.0
        self.round_time = float(ROUND_TIME)
        self.result = None
        self.end_reason = None
        self.opp = FIGHTERS["rusty"]
        self.opp_key = "rusty"
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

    def rotated(self, frames, i, angle, facing):
        """Frame i rotated by angle (degrees, + = counter-clockwise) about the feet, cached.
        px/py: where the feet pivot ended up; bottom/left/right: opaque bounds."""
        key = (id(frames), i, angle)
        if key not in self._rot:
            f = frames[i]
            pivot = pygame.math.Vector2(HIP_X if facing > 0 else FW - 1 - HIP_X, SPRITE_FEET)
            img = pygame.transform.rotate(f, angle)
            centre = pygame.math.Vector2(FW / 2, FH / 2)
            off = (pivot - centre).rotate(-angle)
            new_c = pygame.math.Vector2(img.get_width() / 2, img.get_height() / 2)
            p = new_c + off
            rects = pygame.mask.from_surface(img).get_bounding_rects()
            u = rects[0].unionall(rects[1:])
            self._rot[key] = dict(img=img, px=int(round(p.x)), py=int(round(p.y)), bottom=u.bottom,
                                  left=u.left, right=u.right)
        return self._rot[key]

    # ------------------------------------------------------------ modes
    def clear_fx(self):
        self.texts, self.parts, self.stars = [], [], []
        self.shake, self.shake_t, self.hitstop, self.flash_t = 0, 0.0, 0.0, 0.0
        self.combo, self.combo_t = 0, 0.0
        self.slowmo = 0.0
        self.busy = 0.0
        self.seen_ids = [0, 0]
        self.clinch_by = None
        self.dn = None
        self.mash = 0.0
        self.thud_pending = None
        self.method = None
        if hasattr(self, "ref"):
            self.ref.hide()
            self.ref.SPEED = Referee.SPEED

    @property
    def arena(self):
        return self.mode == "campaign"

    def hype_base(self):
        if self.mode != "campaign":
            return 0.0
        champ = self.opp.get("champ")
        if self.phase in ("walkin", "talk", "reply"):
            return 0.2 if champ else 0.1
        if self.phase == "champion":
            return 0.95
        if self.phase == "defeat":
            return 0.04
        base = 0.1 if champ else 0.05            # a fairly quiet crowd...
        if self.phase == "fight":
            base += min(0.4, self.busy * 0.5)    # ...that gets loud when it's a brawl
        return base

    def reset_bag(self):
        self.mode = "bag"
        self.bag.reset()
        self.player.reset(72, 0.0)
        self.player.facing = 1
        self.damage, self.best = 0, 0
        self.clear_fx()

    def start_spar(self):
        self.mode = "spar"
        self.cpu.set_views(self.spar_views)
        self.cpu.configure()
        self.ai.set_level(self.ai.level if self.ai.level in LEVELS else "NORMAL")
        self.player.reset(96)
        self.cpu.reset(224)
        self.face_off()
        self.ai.reset()
        self.phase, self.phase_t = "intro", 0.0
        self.round_time = float(ROUND_TIME)
        self.result = None
        self.end_reason = None
        self.bubble = None
        self.best = 0
        self.clear_fx()
        self.snd("bell")

    # ------------------------------------------------------------ career
    def fighter_frames(self, key, facing=-1):
        """Sprite set for one fighter, recoloured on first use and kept, in both orientations."""
        if key not in self._fset:
            look = FIGHTERS[key].get("look")
            base = self.strip if look is None else recolor(self.strip, look_palette(**look))
            self._fset[key] = (split(base), split(base, flip=True))
        pair = self._fset[key]
        return pair[0] if facing > 0 else pair[1]

    def fighter_views(self, key):
        """Every angle of one fighter (side, three-quarter, face-on, back-on), recoloured once and kept."""
        if key not in self._fviews:
            look = FIGHTERS[key].get("look")
            self._fviews[key] = make_views(self.strips, None if look is None else look_palette(**look))
        return self._fviews[key]

    def portrait(self, key):
        """A head-and-shoulders crop of a fighter, for the story cards."""
        if key not in self._port:
            frames = self.frames if key == "you" else self.fighter_frames(key, -1)
            f = frames[PORTRAIT_FRAME]
            top, cx = self.frame_top(frames, PORTRAIT_FRAME)
            if key == "you":
                cx = FW - 1 - cx                        # your sprite faces the other way
                f = pygame.transform.flip(f, True, False)
            box = pygame.Surface((PORTRAIT_W, PORTRAIT_H), pygame.SRCALPHA)
            box.fill((18, 16, 32))
            box.blit(f, (PORTRAIT_W // 2 - cx, 3 - top), (0, 0, FW, FH))
            pygame.draw.rect(box, (92, 80, 120), (0, 0, PORTRAIT_W, PORTRAIT_H), 1)
            self._port[key] = box
        return self._port[key]

    def career_reset(self, keep_record=False):
        if not keep_record:
            self.idx, self.wins, self.losses = 0, 0, 0
            self.flags = set()
            self.kos = 0
        self.rebuild = None
        self.scene = None
        self.ending = None

    def start_campaign(self):
        """Opens the career. If there is a save on disk, ask first."""
        self.mode = "campaign"
        self.career_reset()
        data = load_career()
        if data:
            self.save_data = data
            self.phase, self.phase_t = "menu", 0.0
            self.menu_i = 0
            self.clear_fx()
            self.bubble = None
            return
        self.new_career()

    def new_career(self):
        self.mode = "campaign"
        self.career_reset()
        self.play_scene(SCENES["open"], "first_fight")

    def continue_career(self):
        d = self.save_data or {}
        self.mode = "campaign"
        self.career_reset()
        self.idx = clamp(int(d.get("idx", 0)), 0, len(CAREER) - 1)
        self.wins = int(d.get("wins", 0))
        self.losses = int(d.get("losses", 0))
        self.kos = int(d.get("kos", 0))
        self.flags = set(d.get("flags", []))
        self.rebuild = d.get("rebuild") or None
        if self.rebuild not in FIGHTERS:
            self.rebuild = None
        self.begin_fight()

    def save_career(self):
        ok = save_career(dict(idx=self.idx, wins=self.wins, losses=self.losses, kos=self.kos,
                              flags=sorted(self.flags), rebuild=self.rebuild))
        self.saved_t = 2.2 if ok else -2.2
        self.snd("bell" if ok else "block")
        return ok

    def record(self):
        return "%d-%d" % (self.wins, self.losses)

    def bout(self):
        return CAREER[self.idx]

    # ------------------------------------------------------------ scenes
    def play_scene(self, lines, after, arg=None):
        self.scene = Scene(self, lines)
        self.scene_after = (after, arg)
        self.phase, self.phase_t = "scene", 0.0
        self.bubble = None
        self.clear_fx()
        self.player.reset(96)
        self.cpu.reset(372)

    def scene_done(self):
        what, arg = self.scene_after
        self.scene = None
        if what == "first_fight":
            self.begin_fight()
        elif what == "next_fight":
            self.begin_fight()
        elif what == "setback":
            self.rebuild = REBUILDS[min(self.losses - 1, len(REBUILDS) - 1)]
            if self.losses == MAX_LOSSES - 1:
                self.play_scene(SCENES["last_chance"], "next_fight")
            else:
                self.begin_fight()
        elif what == "yacht":
            self.start_yacht()
        else:
            self.begin_fight()

    def begin_fight(self):
        key = self.rebuild or CAREER[self.idx]["opp"]
        o = self.opp = dict(FIGHTERS[key])
        self.opp_key = key
        p, c = self.player, self.cpu
        c.set_views(self.fighter_views(key))
        c.configure(o["hp"], o["power"], o["speed"], o["walk"], o.get("chin", 1.0), o.get("heart", 1.0),
                    o.get("wind", 1.0))
        p.reset(96)
        c.reset(372)                       # off screen - walks in
        self.face_off()
        self.ai.set_level(o["level"], o.get("ai"), o.get("style"))
        self.ai.reset()
        self.phase, self.phase_t = "walkin", 0.0
        self.round_time = float(ROUND_TIME)
        self.result = None
        self.end_reason = None
        self.method = None
        self.bubble = None
        self.scene = None
        self.confetti = []
        self.step = 0
        self.taunt_i = -1
        self.ghost_t = 0.0
        self.fw_t = 0.0
        self.best = 0
        self.clear_fx()

    def after_fight(self):
        """A fight just finished: bank it, then line up whatever the story does next."""
        p, c = self.player, self.cpu
        self.phase_t, self.step = 0.0, 0
        self.bubble = None
        self.ref.leave()
        won = self.result == "YOU WIN!"
        if won:
            self.wins += 1
            if self.method in ("KO", "OUT COLD", "TKO", "STOPPAGE"):
                self.kos += 1
            if not self.rebuild:
                self.flags.add("beat_" + self.opp_key)
            if not self.rebuild and self.bout().get("title_fight"):
                self.phase = "champion"
                p.won, p.end_t = True, max(p.end_t, 0.0)
                self.confetti = []
                self.flags.add("champion")
                self.save_career()
                self.snd("fanfare")
                self.snd("roar")
                return
            self.phase = "victory"
            self.bubble = Bubble(self, c, self.opp["lose"], min_top=88)
        else:
            self.losses += 1
            self.phase = "defeat"
            if not c.won:
                c.won, c.end_t = True, 0.0
            if not p.ko:
                p.ko, p.end_t = True, 0.6
            self.snd("sad")

    def after_result(self):
        """Pressing on past the victory / defeat screen puts the story in motion."""
        if self.result == "YOU WIN!":
            if self.rebuild:
                self.rebuild = None
                self.play_scene(SCENES["rebuilt"], "next_fight")
            else:
                lines = list(self.bout().get("won", ()))
                self.idx = min(self.idx + 1, len(CAREER) - 1)
                nxt = CAREER[self.idx]
                self.play_scene(lines + list(nxt.get("pre", ())), "next_fight")
        else:
            if self.losses >= MAX_LOSSES:
                self.start_retire()
            elif self.rebuild:
                self.rebuild = REBUILDS[min(self.losses - 1, len(REBUILDS) - 1)]
                self.play_scene(SCENES["setback"], "next_fight")
            elif self.bout().get("title_fight"):
                self.play_scene(SCENES["title_lost"], "next_fight")
            else:
                lines = list(self.bout().get("lost", ())) + list(SCENES["setback"])
                self.play_scene(lines, "setback")

    def start_retire(self):
        self.ending = "retire"
        self.scene = Scene(self, RETIRE_SCENE)
        self.scene_after = (None, None)
        self.phase, self.phase_t = "retire", 0.0
        self.card_t = 0.0
        self.bubble = None
        self.clear_fx()
        self.snd("sad")

    def start_yacht(self):
        self.ending = "champion"
        self.yacht = self.yacht or Yacht(self)
        self.yacht.reset()
        self.scene = Scene(self, YACHT_CLEAN if self.losses == 0 else YACHT_ROAD, top=True)
        self.scene_after = (None, None)
        self.phase, self.phase_t = "yacht", 0.0
        self.card_t = 0.0
        self.bubble = None
        self.clear_fx()
        self.snd("fanfare")

    def save_and_quit(self):
        """Bank the career where it stands and step out to the gym."""
        if self.save_career():
            self.reset_bag()
            self.saved_t = 2.2

    def menu_pick(self):
        if self.menu_i == 0 and self.save_data:
            self.continue_career()
        else:
            clear_career()
            self.new_career()

    def menu_move(self, d):
        if self.phase == "menu":
            self.menu_i = (self.menu_i + d) % 2
            self.snd("blip")

    def next_label(self):
        """What the victory screen says is coming up."""
        if self.rebuild:
            return "BACK TO: " + FIGHTERS[CAREER[self.idx]["opp"]]["short"]
        if self.bout().get("title_fight"):
            return "THE TITLE"
        nxt = CAREER[min(self.idx + 1, len(CAREER) - 1)]
        return "NEXT UP: " + FIGHTERS[nxt["opp"]]["short"]

    def taunt_frame(self, kind, t):
        seq, ms = TAUNTS[kind]
        i = int(t * 1000 / ms) % len(seq)
        return seq[i], i

    def update_campaign(self, dt, move, want):
        p, c, o = self.player, self.cpu, self.opp
        if self.bubble:
            self.bubble.update(dt)
        if self.phase in ("intro", "fight", "ko", "down"):
            self.update_spar(dt, move, want)
            if self.phase == "result":
                self.after_fight()
            return
        self.phase_t += dt
        self.saved_t -= dt if self.saved_t > 0 else -dt if self.saved_t < 0 else 0
        if self.phase in ("scene", "menu", "retire", "yacht"):
            if self.scene:
                self.scene.update(dt)
                if self.scene.done() and self.phase == "scene":
                    self.scene_done()
            if self.phase == "yacht" and self.yacht:
                self.yacht.update(dt)
            if self.phase in ("retire", "yacht") and (not self.scene or self.scene.done()):
                self.card_t += dt            # the final card has been up this long
            return
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
                self.parts.append([c.sprite_x() + cx + random.uniform(-16, 16), c.gy() - SPRITE_FEET + top + 4,
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
        if ph in ("walkin", "talk", "reply"):
            self.face_off()
        p.update(dt, 0, MIN_X, STAGE_MAX_X)
        if ph != "walkin":
            c.update(dt, 0, MIN_X, STAGE_MAX_X)
        self.ref.update(dt)

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
            self.new_career()

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
                self.after_result()
            elif ph == "defeat":
                if self.step < 3 and self.bubble:
                    self.bubble.advance()
                elif self.step >= 3 or self.phase_t > 0.6:
                    self.after_result()
            elif ph == "scene" and self.scene:
                self.scene.advance()
                if self.scene.done():
                    self.scene_done()
            elif ph == "menu":
                self.menu_pick()
            elif ph == "champion" and self.phase_t > 1.5:
                self.start_yacht()
            elif ph in ("retire", "yacht"):
                if self.scene and not self.scene.done():
                    self.scene.advance()
                elif self.card_t > 0.5:
                    clear_career()
                    self.reset_bag()

    def mouse(self, x, y, click):
        self.hover = None
        if self.info_rect.collidepoint(x, y):
            self.hover = "info"
        elif self.info_open:
            if click:
                self.toggle_info()        # click anywhere off the panel to shut it
            return
        elif self.button.collidepoint(x, y):
            self.hover = "main"
        elif self.mode == "bag" and self.campaign_button.collidepoint(x, y):
            self.hover = "campaign"
        if not click:
            return
        if self.hover == "info":
            self.toggle_info()
        elif self.hover == "main":
            self.toggle_mode()
        elif self.hover == "campaign":
            self.start_campaign()

    def toggle_info(self):
        self.info_open = not self.info_open
        if self.info_open:
            self.info_seen = True
        self.player.want_block = self.cpu.want_block = None
        self.player.buffer = self.cpu.buffer = None
        self.snd("blip")

    # ------------------------------------------------------------ input
    def step_vec(self, f, d, dx=0):
        """A side-step for fighter f: square off his line, on the side the arrow points to
        (d = -1 up / +1 down the screen, dx = -1 left / +1 right)."""
        o = f.foe()
        rx, rz = o.x - f.x, o.z - f.z
        r = math.hypot(rx, rz) or 1.0
        px, pz = -rz / r, rx / r                    # one of the two ways off his line
        want_x, want_z = float(dx), float(d)
        if px * want_x + pz * want_z < 0:
            px, pz = -px, -pz
        if abs(px * want_x + pz * want_z) < 0.2:     # arrow points along the line: step toward the middle
            cx, cz = (MIN_X + STAGE_MAX_X) / 2, (Z_MIN + Z_MAX) / 2
            if px * (cx - f.x) + pz * (cz - f.z) < 0:
                px, pz = -px, -pz
        return px, pz

    def side_step(self, d, dx=0):
        if self.info_open or self.mode == "bag" or self.phase != "fight":
            return
        if self.player.sidestep(self.step_vec(self.player, d, dx)):
            self.say("STEP", self.player.x - 10, self.player.gy() - 70, (150, 230, 255), self.font_s,
                     vy=-14, life=0.45)

    def tap_depth(self, d):
        """UP / DOWN pressed: two quick taps the same way is a side-step."""
        if self.info_open or self.mode == "bag" or self.phase != "fight":
            return
        now = self.clock
        last = self._taps.get(d, -9.0)
        self._taps[d] = now
        if now - last <= DOUBLE_TAP:
            self._taps[d] = -9.0
            self.side_step(d)

    def pivot(self):
        """Roll round him - a quarter-turn and more - and come up square on his flank. How you get
        off the ropes: you always roll toward the open ring."""
        if self.info_open or self.mode == "bag" or self.phase != "fight":
            return
        p, c = self.player, self.cpu
        if p.busy() or p.pivot_cd > 0 or p.stam < PIVOT_STAM or c.down or c.out_cold or c.ko:
            if p.pivot_cd > 0 or p.stam < PIVOT_STAM:
                self.say("NO LEGS" if p.stam < PIVOT_STAM else "NOT YET",
                         p.x - 16, p.gy() - 68, (190, 190, 210), self.font_s, vy=-14, life=0.5)
            return
        r = MIN_SEP + PIVOT_GAP
        a0 = math.atan2(p.z - c.z, p.x - c.x)
        best = None
        for k in range(6, 16):                      # anywhere from a third to most of the way round him
            for sweep in (k * 0.2, -k * 0.2):
                a1 = a0 + sweep
                ex, ez = c.x + math.cos(a1) * r, c.z + math.sin(a1) * r
                room = min(ex - MIN_X, STAGE_MAX_X - ex, ez - Z_MIN, Z_MAX - ez, PIVOT_ROOM)
                score = room - 2.0 * abs(sweep)
            if best is None or score > best[0]:
                best = (score, a1)
        p.finish_action()
        p.block = p.want_block = None
        p.buffer = None
        p.hitstun = p.stun_t = 0.0
        p.react = None
        p.pivot_c, p.pivot_a0, p.pivot_a1, p.pivot_r = (c.x, c.z), a0, best[1], r
        p.pivot_t = PIVOT_TIME
        p.pivot_cd = PIVOT_CD
        p.spend(PIVOT_STAM)
        for k in range(3):
            p.ghosts.append(p.make_ghost())
        self.ai.plan.clear()
        self.ai.def_plan = None
        self.ai.pin_t = 0.0
        self.say("PIVOT!", p.x - 16, p.gy() - 72, (150, 230, 255), self.font_m, vy=-16, life=0.7)
        self.snd("slip")

    def clinch(self):
        if self.info_open:
            return
        if self.mode != "bag" and self.phase == "fight":
            self.try_clinch(self.player)

    def press(self, name):
        if self.info_open:
            return                                # the fight is paused while you read
        if self.mode == "bag" and name in FEINTS:
            name = FEINT_OF[name]                 # nothing to feint on a heavy bag
        if self.phase == "down" and self.mode != "bag" and self.dn and self.dn["who"] is self.player:
            if self.player.down and self.player.rising_t < 0:
                self.mash += 1                    # mash to beat the count
                self.snd("blip")
            return
        if self.mode != "bag" and self.phase != "fight":
            return
        self.player.press(name)

    def update_audio(self, dt):
        base = self.hype_base()
        for f in (self.player, self.cpu):        # punches thrown by either boxer make the fight 'busy'
            if f.attack_id != self.seen_ids[f is self.cpu]:
                self.seen_ids[f is self.cpu] = f.attack_id
                self.busy = min(1.0, self.busy + 0.11)
        self.busy = max(0.0, self.busy - 0.22 * dt)
        self.hype += (base - self.hype) * min(1.0, dt * (0.4 if self.hype > base else 1.5))
        if self.mode == "campaign":
            self.crowd.update(dt, self.hype)
        ch, loop = self.crowd_ch, self.sounds.get("crowd_loop")
        if not ch or not loop:
            return
        if self.mode == "campaign" and not self.muted:
            if not ch.get_busy():
                ch.play(loop, loops=-1, fade_ms=600)
            ch.set_volume(0.09 + 0.85 * self.hype)
        elif ch.get_busy():
            ch.fadeout(400)

    def snd(self, name):
        s = self.sounds.get(name)
        if s and not self.muted:
            s.play()

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.stop()

    def say(self, s, x, y, color, font=None, vy=-22, life=0.8):
        self.texts.append(dict(s=s, x=x, y=y, vy=vy, t=0.0, life=life, color=color, font=font or self.font_m))

    def on_miss(self, f, frame):
        f.spend(STAM_MISS)
        wx, wy = f.tip(frame)
        o = f.foe() if self.mode != "bag" else None
        off = o is not None and self.off_line(f, o) > LAT_HIT
        self.say("off line" if off else "miss", wx - 12, wy - 8, (150, 156, 182), self.font_s, vy=-14, life=0.6)
        if f is self.player and self.mode != "bag":
            self.ai.punish = True

    # ------------------------------------------------------------ update
    def update(self, dt, left=False, right=False, down=False, block=False, far=False, near=False):
        if self.saved_t:
            self.saved_t = max(0.0, self.saved_t - dt) if self.saved_t > 0 else min(0.0, self.saved_t + dt)
        self.info_t = clamp(self.info_t + (dt * 6.5 if self.info_open else -dt * 7.5), 0.0, 1.0)
        if self.info_open:                        # reading the controls pauses the fight
            self.clock += dt
            return
        if self.slowmo > 0:                       # slow motion on the big moments
            self.slowmo -= dt
            dt *= 0.35
        self.clock += dt
        self.update_audio(dt)
        self.update_fx(dt)
        if self.hitstop > 0:
            self.hitstop -= dt
            return
        self.combo_t -= dt
        if self.combo_t <= 0:
            self.combo = 0
        move = (1 if right else 0) - (1 if left else 0)
        self.zmove = (1 if near else 0) - (1 if far else 0)
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
            self.face_off(dt)
            self.ai.update(dt)
            mx, mz = self.player_steer(move, self.zmove)
            p.update(dt, mx, MIN_X, STAGE_MAX_X, mz)
            c.update(dt, self.ai.move, MIN_X, STAGE_MAX_X, self.ai.zmove)
            self.resolve(p, c)
            self.resolve(c, p)
            self.separate()
            self.update_clinch(dt)
            for f, o in ((p, c), (c, p)):
                if f.liver_t > 0 and self.phase == "fight":
                    f.liver_t -= dt
                    if f.liver_t <= 0:
                        self.knockdown(f, o, "liver", 3.0)
                if f.healing and random.random() < dt * 3:
                    self.say("+", f.x + random.uniform(-8, 8), f.gy() - 74, (120, 240, 140), self.font_m,
                             vy=-16, life=0.6)
            if p.hurt and self.phase == "fight":     # your heart pounding while you're hurt
                self.beat_t -= dt
                if self.beat_t <= 0:
                    self.beat_t = 0.85
                    self.snd("heartbeat")
            if self.round_time <= 0 and self.phase == "fight":
                self.round_time = 0.0
                self.end_fight(by_time=True)
        elif self.phase == "down":
            self.update_down(dt)
        else:
            p.want_block = c.want_block = None
            if self.phase == "intro":
                self.face_off(dt)
            p.update(dt, 0, MIN_X, STAGE_MAX_X)
            c.update(dt, 0, MIN_X, STAGE_MAX_X)
            if self.phase == "intro" and self.phase_t > 1.8:
                self.phase, self.phase_t = "fight", 0.0
            elif self.phase == "ko":
                t = self.thud_pending
                if t is not None and t.fall_t >= 0.42:
                    self.thud_pending = None
                    self.snd("canvas")
                    self.dust(t.head_pos()[0], t.gy())
                if self.phase_t > 0.5 and self.ref.arrived() and self.ref.pose not in ("wave_a", "wave_b"):
                    self.ref.set_pose("wave_a", 99)
                if self.phase_t > self.ko_hold:
                    self.phase, self.phase_t = "result", 0.0
        self.ref.update(dt)

    def end_fight(self, by_time=False, loser=None, method="KO"):
        p, c = self.player, self.cpu
        if by_time:
            # judges' scorecards: punches landed, and a knockdown is worth a lot
            sp, sc = p.dealt + 30 * p.kds, c.dealt + 30 * c.kds
            if abs(sp - sc) < 3:
                self.result = "DRAW"
            else:
                self.result = "YOU WIN!" if sp > sc else "YOU LOSE"
                winner = p if sp > sc else c
                winner.won, winner.end_t = True, 0.0
                loser = c if winner is p else p
            self.method = "DECISION" if self.result != "DRAW" else "DRAW"
            self.end_reason = "time"
            self.ko_hold = 1.6
        else:
            self.end_reason = "ko"
            self.method = method
            winner = c if loser is p else p
            winner.won, winner.end_t = True, -0.9
            loser.ko = True
            loser.ko_style = "stand" if method == "STOPPAGE" else "kneel"
            if loser.down:                          # stays kneeling where he was counted out
                loser.down, loser.end_t = False, 0.6
            self.result = "YOU WIN!" if loser is c else "YOU LOSE"
            self.ko_hold = 2.8 if method == "OUT COLD" else 2.2
            if loser is not None:
                self.call_ref(loser, wave=True)
            self.excite(1.0)
            self.snd("roar" if self.arena else "crowd")
        self.phase, self.phase_t = "ko", 0.0
        self.snd("bell3")

    METHOD_TEXT = {"KO": "K.O.!", "OUT COLD": "OUT COLD!", "TKO": "T.K.O.!", "STOPPAGE": "T.K.O.!",
                   "DECISION": "DECISION", "DRAW": "DRAW"}
    METHOD_SUB = {"KO": "COUNTED OUT", "OUT COLD": "KNOCKED OUT COLD", "TKO": "THREE KNOCKDOWNS",
                  "STOPPAGE": "THE REFEREE STOPS IT", "DECISION": "THE JUDGES' DECISION", "DRAW": "THE JUDGES CALL IT A DRAW"}

    def face_off(self, dt=None):
        """Both men turn to face each other (dt=None: at once). A punch in flight turns on its own terms
        (see Fighter.update_action), and nobody turns while tied up or on the floor."""
        p, c = self.player, self.cpu
        if math.hypot(c.x - p.x, c.z - p.z) < 2:
            return
        for f, o in ((p, c), (c, p)):
            if f.action or f.clinch or f.down or f.out_cold or f.pivot_t > 0 or (f.ko and dt is not None):
                continue
            f.turn_to(f.angle_to(o), TURN_RATE * (0.6 if f.hurt or f.stun_t > 0 else 1.0), dt)
            f.pick_view(force=dt is None)

    def player_steer(self, move, zmove):
        """Arrows are screen directions. But if you start a step that goes ROUND him, holding the same
        arrow keeps taking you round him (all the way round, if you like) instead of drifting off
        in a straight line as the angle changes. Change the arrows to change what you're doing."""
        p, c = self.player, self.cpu
        key = (move, zmove)
        if not (move or zmove):
            self._strafe = (key, 0)
            return 0, 0
        rx, rz = c.x - p.x, c.z - p.z
        r = math.hypot(rx, rz) or 1.0
        nx, nz = rx / r, rz / r                      # toward him
        tx, tz = nz, -nx                             # round him
        held, rot = getattr(self, "_strafe", (None, 0))
        if held != key:
            l = math.hypot(move, zmove)
            radial = (move * nx + zmove * nz) / l
            tang = (move * tx + zmove * tz) / l
            rot = (1 if tang > 0 else -1) if abs(tang) > 0.7 and r < ORBIT_RANGE else 0
            self._strafe = (key, rot)
        if rot and r < ORBIT_RANGE and not (c.down or c.out_cold):
            return tx * rot, tz * rot
        return move, zmove

    def dist(self):
        p, c = self.player, self.cpu
        return math.hypot(c.x - p.x, c.z - p.z)

    def off_line(self, att, d):
        """How far d is to the side of the line att is punching along."""
        ux, uz = att.u()
        vx, vz = d.x - att.x, d.z - att.z
        return abs(vx * uz - vz * ux)

    def separate(self):
        """Two bodies can't stand in the same spot: push them apart (the one with the ropes behind him moves least)."""
        p, c = self.player, self.cpu
        if p.pivot_t > 0 or c.pivot_t > 0:
            return                                  # let him roll round
        dx, dz = c.x - p.x, c.z - p.z
        d = math.hypot(dx, dz)
        if d >= MIN_SEP:
            return
        if d < 1e-3:
            dx, dz, d = 1.0, 0.0, 1.0
        nx, nz = dx / d, dz / d
        need = MIN_SEP - d
        for f, sgn, share in ((p, -1, 0.5), (c, 1, 0.5)):
            f.x = clamp(f.x + sgn * nx * need * share, MIN_X, STAGE_MAX_X)
            f.z = clamp(f.z + sgn * nz * need * share, Z_MIN, Z_MAX)
        dx, dz = c.x - p.x, c.z - p.z           # one of them hit the ropes: the other gives the rest
        d = math.hypot(dx, dz)
        if d < MIN_SEP - 0.5 and d > 1e-3:
            need = MIN_SEP - d
            nx, nz = dx / d, dz / d
            for f, sgn in ((p, -1), (c, 1)):
                f.x = clamp(f.x + sgn * nx * need, MIN_X, STAGE_MAX_X)
                f.z = clamp(f.z + sgn * nz * need, Z_MIN, Z_MAX)
                dx, dz = c.x - p.x, c.z - p.z
                if math.hypot(dx, dz) >= MIN_SEP - 0.5:
                    break

    # ------------------------------------------------------------ clinch
    def try_clinch(self, f):
        """Grab hold of the other man. In range it ties you both up; short and you're wide open."""
        o = self.cpu if f is self.player else self.player
        if f.busy() or self.phase != "fight" or o.down or o.out_cold or o.ko:
            return
        cd = CLINCH_CD_ROPES if f.on_ropes() else CLINCH_CD   # stuck on the ropes? grab him sooner
        if f.clinch_cd > CLINCH_CD - cd:
            return
        f.finish_action()
        f.block = f.want_block = None
        f.buffer = None
        f.clinch_cd = CLINCH_CD
        if math.hypot(o.x - f.x, o.z - f.z) > MIN_SEP + CLINCH_RANGE or o.clinch:
            f.stagger(CLINCH_WHIFF)               # grabbed at thin air
            self.say("WHIFF!", f.x - 14, f.gy() - 62, (170, 180, 215), self.font_s, vy=-14, life=0.6)
            self.snd("swish")
            return
        mx, mz = (f.x + o.x) / 2.0, (f.z + o.z) / 2.0
        a = math.atan2(o.z - f.z, o.x - f.x)
        half = (MIN_SEP - 2) / 2.0
        for g, sgn in ((f, -1), (o, 1)):
            g.finish_action()
            g.block = g.want_block = None
            g.buffer = None
            g.hitstun = g.stun_t = 0.0
            g.react = None
            g.x = clamp(mx + sgn * math.cos(a) * half, MIN_X, STAGE_MAX_X)     # chest to chest
            g.z = clamp(mz + sgn * math.sin(a) * half, Z_MIN, Z_MAX)
            g.clinch, g.clinch_t = True, 0.0
        f.ang, o.ang = a, a + math.pi
        f.pick_view(True)
        o.pick_view(True)
        o.clinch_cd = max(o.clinch_cd, 0.9)
        self.ai.plan.clear()
        self.ai.def_plan = None
        self.clinch_by = f
        self.say("CLINCH", (f.x + o.x) / 2 - 16, min(f.gy(), o.gy()) - 74, (200, 206, 232), self.font_m, vy=-10, life=0.8)
        self.snd("block")

    def update_clinch(self, dt):
        p, c = self.player, self.cpu
        if not (p.clinch or c.clinch):
            return
        p.clinch_t += dt
        c.clinch_t += dt
        t = max(p.clinch_t, c.clinch_t)
        if t > CLINCH_TIME * 0.45 and not self.ref.on:
            self.call_ref(self.cpu if self.clinch_by is self.player else self.player)
        if t >= CLINCH_TIME:
            for g in (p, c):
                was_roped = g.on_ropes()
                g.clinch, g.clinch_t = False, 0.0
                g.push(-18 if was_roped else -6)   # the ref shoves them apart, off the ropes
            self.ref.set_pose("wave_b", 0.35)
            self.ref.leave()
            self.say("BREAK!", VW // 2 - 22, 72, (255, 232, 130), self.font_l, vy=-8, life=0.8)
            self.snd("count")

    def excite(self, amount):
        self.hype = min(1.0, self.hype + amount)

    # ------------------------------------------------------------ sparring hits
    def resolve(self, att, d):
        if att.action not in PUNCHES or att.hit_done or d.ko or d.down or d.out_cold or d.clinch:
            return
        spec = ACTIONS[att.action]
        frame = spec["frames"][att.idx]
        if frame not in spec["active"]:
            return
        target = spec["target"]
        reach = self.fist[frame][0] - HIP_X + att.lunge() + spec.get("reach", 0)
        ux, uz = att.u()
        dist = (d.x - att.x) * ux + (d.z - att.z) * uz      # how far along the punch's line he is
        full = reach + HURT[target] + 3
        if dist <= 0 or full < dist:
            return                                    # not there yet - "miss" if it never gets there
        if self.off_line(att, d) > LAT_HIT or d.side_t > 0:
            return                                    # off his line / stepping off it - it sails past
        hx, hy = self.hit_point(d, target)
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
            # how far into the punch it landed: 1 = at the end of his reach (flush), 0 = smothered
            ext = clamp((dist - MIN_SEP) / max(1.0, self.ranges[att.action] - MIN_SEP), 0.0, 1.0)
            self.clean_hit(att, d, spec, target, hx, hy, ext)

    def hit_point(self, d, target):
        """Where on screen a punch to d's head / body lands (just in front of him)."""
        ux, uz = d.u()
        return (d.x + ux * HURT[target],
                GROUND + (d.z + uz * HURT[target]) * ZK - SPRITE_FEET + TARGET_Y[target])

    def blocked(self, att, d, spec, hx, hy):
        if d.parry_ready and d.block_t <= PARRY_WINDOW:
            d.parry_ready = False
            att.stagger(PARRY_STUN)
            d.counter_t = COUNTER_WINDOW
            self.stars.append(dict(x=hx, y=hy, t=0.0, life=0.28, big=True, kind="parry"))
            self.say("PARRY!", hx - 20, hy - 26, (130, 240, 255), self.font_l, vy=-20, life=0.9)
            self.hitstop = 0.09
            self.snd("parry")
            self.excite(0.12)
            return
        d.unanswered = max(0, d.unanswered - 1)    # covering up shows the referee he's still in it
        d.spend(STAM_BLOCK)
        d.guard -= spec["guard"] * (1 + FLURRY_RAMP * d.block_chain) * (1 + 0.6 * d.gas())
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
            self.ai.block_rest = BLOCK_REST
        if d.guard <= 0:
            d.guard = 0.0
            d.stagger(GUARD_BREAK_STUN)
            self.say("GUARD BREAK!", hx - 34, hy - 30, (255, 150, 90), self.font_l, vy=-16, life=1.1)
            self.shake, self.shake_t = 3, 0.18
            self.snd("guard_break")
            self.excite(0.25)

    def impact(self, att, d, name, ext, counter_hit, walking_in, slip_counter, crit, stunned):
        """How HARD a clean punch landed, divided by the victim's chin. Compared with KD_IMPACT /
        KO_IMPACT to decide flash knockdowns and one-punch knockouts. Returns (impact, notes)."""
        k = POWER[name] * att.punch_power() ** 0.7
        k *= 0.78 + 0.37 * ext                    # flush at the end of the punch vs smothered
        if counter_hit:
            k *= 1.45                             # caught him mid-punch: he never saw it
        if walking_in:
            k *= 1.15                             # stepped forward into it
        if stunned:
            k *= 1.25                             # parried / guard broken: nothing to absorb it
        elif slip_counter:
            k *= 1.35                             # slipped and came back with it
        if crit and not stunned:
            k *= 1.35                             # right on the button (a stunned man is always 'crit')
        if d.hurt:
            k *= 1.25                             # already wobbling
        k *= 1 + 0.3 * (1 - d.hp / d.max_hp)      # worn down
        k *= 1 + 0.12 * d.downs                   # been down before
        k *= 1 + 0.05 * min(d.unanswered, 4)      # eating punch after punch
        if d.on_ropes():
            k *= ROPE_IMPACT                      # nowhere to roll with it
        k *= 1 + 0.35 * d.gas()                   # a gassed fighter's legs and neck can't hold him up
        k *= random.uniform(0.9, 1.1)
        return k / d.chin

    def clean_hit(self, att, d, spec, target, hx, hy, ext=0.6):
        name = att.action
        mult, chance, tags = 1.0, CRIT_CHANCE, []
        stunned = d.stun_t > 0
        crit = stunned                            # hitting a stunned boxer is always critical
        counter_hit = d.in_startup()
        walking_in = d.moving == 1
        # rolling with it: a punch you are already moving away from does not land clean
        glancing = (d.moving == -1 and not stunned and random.random() < GLANCE_CHANCE)
        if counter_hit:
            mult *= COUNTER_HIT_MULT
            chance += 0.12
            tags.append(("COUNTER HIT", (255, 200, 90)))
        if att.is_counter:
            mult *= COUNTER_MULT
            chance += 0.2
            tags.append(("COUNTER!", (120, 220, 255)))
        if glancing:
            crit, chance, tags = False, 0.0, []
            mult *= GLANCE_DMG
        crit = crit or random.random() < chance
        if crit:
            mult *= CRIT_MULT
        baited = att.bait_t > 0
        if baited:
            att.bait_t = 0.0
            mult *= 1.2
            chance += 0.14
            tags.insert(0, ("FEINTED HIM!", (160, 255, 190)))
        if counter_hit and ext > 0.7 and POWER[name] >= 2:
            tags.insert(0, ("PERFECT TIMING!", (255, 255, 160)))
        imp = self.impact(att, d, name, ext, counter_hit, walking_in, att.is_counter, crit, stunned)
        if baited:
            imp *= BAIT_MULT
        if glancing:
            imp *= 0.35
        dmg = max(1, int(round(spec["spar_dmg"] * mult * att.punch_power()
                                * random.uniform(1 - DMG_VARIANCE, 1 + DMG_VARIANCE))))
        d.hp = max(0.0, d.hp - dmg)
        d.spend(STAM_HIT)
        if d.pro_regen:
            d.stam_t = min(d.stam_t, STAM_REGEN_DELAY - STAM_HIT_PAUSE)   # caught clean: no breather
        d.since_damage = 0.0
        att.dealt += dmg
        att.unanswered = 0
        d.unanswered += 1
        if target == "head":
            d.daze += dmg * (0.8 + 0.45 * imp) / d.chin * (1.15 if d.hurt else 1.0)
            d.daze_t = 0.0
        else:
            d.body_dmg += dmg * (0.8 + 0.3 * imp)
            scale = d.max_hp / MAX_HP
            d.regen_cap = max(REGEN_CAP_MIN * scale, d.regen_cap - BODY_CAP_LOSS * scale)
        d.get_hit(target, spec["stun"] * (0.45 if glancing else 1.0) + (0.25 if crit else 0.0))
        d.push((12 if crit else (7 if spec["guard"] > 20 else 4)) + (ROPE_SHOVE if not d.on_ropes() else 0))
        if d is self.player:
            self.combo, self.combo_t = 0, 0.0
        else:
            self.combo += 1
            self.combo_t = 1.0
            self.best = max(self.best, self.combo)

        big = (crit or spec["guard"] > 20) and not glancing
        self.stars.append(dict(x=hx, y=hy, t=0.0, life=0.2 if crit else 0.16, big=big, kind="crit" if crit else "hit"))
        for _ in range(18 if crit else (12 if big else 7)):
            a = random.uniform(-1.2, 1.2) + (0 if d.facing < 0 else math.pi)
            sp = random.uniform(40, 170 if crit else 110)
            self.parts.append([hx, hy, math.cos(a) * sp, math.sin(a) * sp - 30, random.uniform(0.18, 0.4),
                               random.choice([(255, 226, 120), (255, 255, 255), (255, 140, 100)])])
        if imp >= 2.6 and target == "head":       # sweat spray off a big head shot
            for _ in range(10):
                a = random.uniform(-0.9, 0.9) + (0 if d.facing < 0 else math.pi)
                sp = random.uniform(60, 140)
                self.parts.append([hx, hy - 4, math.cos(a) * sp, math.sin(a) * sp - 50, random.uniform(0.3, 0.55),
                                   random.choice([(200, 230, 255), (255, 255, 255)])])
        col = (255, 232, 130) if not crit else (255, 110, 70)
        if glancing:
            col = (190, 196, 220)
            self.say("GRAZED", hx - 20, hy - 26, col, self.font_s, vy=-16, life=0.6)
        self.say(str(dmg), hx - 6, hy - 14, col, self.font_m if glancing else (self.font_xl if crit else self.font_l),
                 vy=-26)
        y = hy - 30
        if crit:
            self.say("CRITICAL!", hx - 28, y, (255, 120, 60), self.font_l, vy=-20, life=1.0)
            y -= 13
            self.flash_t = 0.08
        for s, cc in tags:
            self.say(s, hx - 26, y, cc, self.font_m, vy=-18, life=0.9)
            y -= 12
        self.hitstop = (spec["stop"] * 0.4) if glancing else (0.12 if crit else spec["stop"])
        self.shake = 1 if glancing else (4 if crit else spec["shake"])
        self.shake_t = 0.08 if glancing else (0.18 if crit else 0.12)
        if glancing:
            self.snd("block")
        elif crit:
            self.snd("crit")
        elif target == "body":
            self.snd("hit_body_big" if big else "hit_body")
        else:
            self.snd("hit_cross" if big else "hit_jab")
        if not glancing:
            self.excite(0.015 + 0.012 * imp * imp)    # jabs barely stir them; big shots really do
        if self.arena and imp >= 2.7:
            self.snd("ooh")

        outcome = self.judge(att, d, name, target, imp)
        if outcome == "cold":
            self.knock_out_cold(d, att)
        elif outcome == "down":
            self.knockdown(d, att, "kd", imp)
        elif outcome == "liver":
            d.liver_t = 0.45
            d.hitstun = 0.0
            self.say("LIVER SHOT!", hx - 30, hy - 34, (255, 140, 200), self.font_l, vy=-14, life=0.5)
            self.hitstop = 0.18
            self.excite(0.4)
        elif outcome == "hurt":
            d.hurt = True
            d.unanswered = 1
            hx2, hy2 = d.head_pos()
            self.say("HURT!" if d is self.cpu else "YOU'RE HURT!", hx2 - 18, hy2 - 22, (255, 170, 60), self.font_l,
                     vy=-12, life=1.2)
            self.excite(0.35)
            if d is self.player:
                self.snd("ringing")
                self.beat_t = 0.0
        elif outcome == "stop":
            self.hitstop = 0.2
            self.end_fight(loser=d, method="STOPPAGE")

    def judge(self, att, d, name, target, imp):
        """What a clean punch does beyond damage: None / hurt / down / liver / cold / stop."""
        if target == "head":
            if imp >= KO_IMPACT and random.random() < clamp(0.3 + (imp - KO_IMPACT) / 2.0, 0.0, 0.9):
                return "cold"
            if d.hp <= 0:
                if imp >= KO_IMPACT * 0.88 and random.random() < 0.35:
                    return "cold"
                return "down"
            if d.daze >= DAZE_DROP:
                return "down"
            if imp >= KD_IMPACT and random.random() < clamp(0.3 + (imp - KD_IMPACT) / 1.2, 0.0, 1.0):
                return "down"
            if d.daze >= DAZE_HURT and not d.hurt:
                return "hurt"
        else:
            if (name == "body_cross" and d.body_dmg >= LIVER_BODY * d.chin
                    and random.random() < clamp(0.25 + (d.body_dmg - LIVER_BODY * d.chin) / 40 + (imp - 2) / 4, 0.0, 0.85)):
                return "liver"
            if d.hp <= 0:
                return "down"
        if d.hurt and d.unanswered >= STOPPAGE_HITS:
            return "stop"
        return None

    # ------------------------------------------------------------ knockdowns
    def corner_pos(self, f):
        """The neutral corner furthest from the man on the floor."""
        o = self.cpu if f is self.player else self.player
        corners = [(MIN_X + 14, Z_MIN + 12), (STAGE_MAX_X - 14, Z_MIN + 12),
                   (MIN_X + 14, Z_MAX - 10), (STAGE_MAX_X - 14, Z_MAX - 10)]
        return max(corners, key=lambda q: math.hypot(q[0] - o.x, (q[1] - o.z) * 1.4))

    def call_ref(self, d, wave=False):
        """Referee steps in over the fighter d (from the side away from him)."""
        o = self.cpu if d is self.player else self.player
        side = 1 if o.x >= d.x else -1
        tx = clamp(d.x + side * 34, 24, VW - 24)
        self.ref.z = clamp(d.z - 8, Z_MIN, Z_MAX)            # just behind his line, so you can still see him
        if not self.ref.on:
            start = VW + 40 if side > 0 else -40
            self.ref.enter(start, tx, -side)
        else:
            self.ref.tx, self.ref.facing = tx, -side
        if wave:
            self.ref.set_pose("wave_a", 99)
            self.ref.SPEED = 260.0

    def fall_down(self, d):
        d.finish_action()
        d.block = d.want_block = None
        d.buffer = None
        d.hitstun = d.stun_t = 0.0
        d.liver_t = 0.0
        d.react = None
        d.ghosts = []

    def knockdown(self, d, att, kind, imp):
        o = att
        self.fall_down(d)
        d.down, d.down_t, d.rising_t = True, 0.0, -1.0
        d.spend(STAM_DOWN_COST)
        d.downs += 1
        o.kds += 1
        final = d.downs >= MAX_DOWNS
        self.dn = dict(who=d, other=o, kind=kind, count=0, up=False, up_t=0.0, box_t=-1.0, final=final,
                       thud=False, imp=imp, next=None)
        self.mash = 0.0
        if d is self.player:
            self.mash_need = MASH_NEED + 6 * (d.downs - 1) + (5 if kind == "liver" else 0) + int(3 * max(0.0, imp - KD_IMPACT))
        else:
            stay = 0.04 + 0.24 * (d.downs - 1) + (0.18 if kind == "liver" else 0.0) + clamp((imp - KD_IMPACT) / 3, 0, 0.25)
            stay += 0.1 if d.hp <= 0 else 0.0
            stay /= d.heart
            if random.random() < stay:
                self.dn["rise_at"] = None
            else:
                self.dn["rise_at"] = min(9, random.randint(3, 6) + d.downs + (2 if kind == "liver" else 0)
                                         - (1 if d.heart > 1.3 else 0))
        self.phase, self.phase_t = "down", 0.0
        self.hitstop = 0.22
        self.slowmo = 0.5
        self.shake, self.shake_t = 5, 0.3
        self.flash_t = 0.08
        hx, hy = d.head_pos()
        word = "DOWN GOES " + ("YOU" if d is self.player else self.opp_short()) + "!"
        if kind == "liver":
            word = "HE FOLDS!" if d is self.cpu else "DOUBLED OVER!"
        self.say("KNOCKDOWN!", VW // 2 - self.font_xl.size("KNOCKDOWN!")[0] // 2, 50, (255, 90, 80), self.font_xl,
                 vy=-4, life=1.15)
        self.say(word, VW // 2 - self.font_m.size(word)[0] // 2, 70, (255, 232, 130), self.font_m, vy=-4, life=1.15)
        self.snd("ko_boom")
        self.snd("roar" if self.arena else "crowd")
        self.excite(1.0)
        self.combo = 0

    def knock_out_cold(self, d, att):
        self.fall_down(d)
        d.out_cold, d.fall_t = True, 0.0
        d.downs += 1
        att.kds += 1
        self.dn = None
        self.hitstop = 0.3
        self.slowmo = 1.2
        self.shake, self.shake_t = 7, 0.45
        self.flash_t = 0.08
        self.thud_pending = d
        self.snd("ko_boom")
        self.end_fight(loser=d, method="OUT COLD")

    def opp_short(self):
        return self.opp["short"] if self.mode == "campaign" else "THE CPU"

    def update_down(self, dt):
        dn = self.dn
        d, o = dn["who"], dn["other"]
        # the man still standing goes to a neutral corner
        o.want_block = None
        cx, cz = self.corner_pos(o)
        vx, vz = cx - o.x, cz - o.z
        far = math.hypot(vx, vz)
        if far < 3 or self.phase_t < 0.4:
            vx = vz = 0.0
        o.update(dt, vx / max(far, 1e-6), MIN_X, STAGE_MAX_X, vz / max(far, 1e-6))
        if not o.moving:
            o.turn_to(o.angle_to(d), TURN_RATE, dt)       # watching him from the corner
            o.pick_view()
        d.update(dt, 0, MIN_X, STAGE_MAX_X)
        self.separate()
        if not dn["thud"] and d.down_t >= 0.42:
            dn["thud"] = True
            self.snd("canvas")
            self.dust(d.x - d.facing * 10, d.gy())
        if self.phase_t > 0.55 and not self.ref.on:
            self.call_ref(d)

        if dn["final"]:                          # third knockdown: the referee waves it off
            if self.phase_t > 1.3:
                self.end_fight(loser=d, method="TKO")
            return

        if dn["next"] is None and self.phase_t >= COUNT_START and self.ref.arrived():
            dn["next"] = self.phase_t
        if (dn["next"] is not None and self.phase_t >= dn["next"] and dn["count"] < 10
                and (not dn["up"] or dn["count"] < STANDING_COUNT)):
            dn["next"] += COUNT_DT
            dn["count"] += 1
            self.ref.set_pose("down", 0.28)
            self.snd("count")
            self.excite(0.08)
            if dn["count"] >= 10 and not dn["up"] and d.rising_t < 0:
                self.end_fight(loser=d, method="KO")
                return
        elif self.ref.arrived() and self.ref.pose_t <= 0 and dn["box_t"] < 0:
            self.ref.set_pose("up")

        if not dn["up"]:
            if d.rising_t < 0:
                if d is self.player:
                    self.mash = max(0.0, self.mash - MASH_DECAY * dt)
                    if self.mash >= self.mash_need and dn["count"] >= 2:
                        d.rising_t = 0.0
                elif dn.get("rise_at") is not None and dn["count"] >= dn["rise_at"]:
                    d.rising_t = 0.0
            elif d.rising_t >= 0.55:
                self.get_up(d)
        else:
            dn["up_t"] += dt
            if dn["box_t"] < 0 and dn["count"] >= STANDING_COUNT and dn["up_t"] > 0.5:
                dn["box_t"] = 0.0
                self.ref.set_pose("point", 0.6)
                self.say("BOX!", VW // 2 - 18, 70, (255, 232, 130), self.font_huge, vy=-8, life=0.9)
                self.snd("bell")
            if dn["box_t"] >= 0:
                dn["box_t"] += dt
                if dn["box_t"] > 0.55:
                    self.face_off()
                    self.ref.leave()
                    self.phase, self.phase_t = "fight", 0.0
                    self.dn = None
                    self.ai.plan.clear()
                    self.ai.def_plan = None
                    self.player.buffer = None

    def get_up(self, d):
        dn = self.dn
        d.down, d.rising_t = False, -1.0
        dn["up"], dn["up_t"] = True, 0.0
        frac = RISE_HP[min(d.downs - 1, len(RISE_HP) - 1)]
        after = d.max_hp * frac if d.hp <= 0 else min(d.hp, d.max_hp * (frac + 0.15))
        d.hp = d.hp_lag = after
        scale = d.max_hp / MAX_HP
        d.regen_cap = max(REGEN_CAP_MIN * scale, min(d.regen_cap, after + 10 * scale))
        d.daze, d.hurt = 30.0, False
        d.stam = max(d.stam, float(STAM_RISE))
        d.gassed = d.stam < GAS_LINE
        d.body_dmg *= 0.5
        d.guard = float(GUARD_MAX)
        d.unanswered = 0
        d.since_damage = 0.0
        hx, hy = d.head_pos()
        self.say("YOU'RE UP!" if d is self.player else "HE'S UP!", hx - 24, hy - 24, (150, 240, 160), self.font_l,
                 vy=-10, life=1.2)
        self.snd("cheer" if self.arena else "block")
        self.excite(0.5)

    def on_bait(self, biter, feinter):
        """The other man committed to defending a punch that was never coming."""
        hx, hy = biter.head_pos()
        self.say("BIT ON IT!", hx - 26, hy - 20, (160, 255, 190), self.font_m, vy=-14, life=0.7)
        if feinter is self.player:
            self.excite(0.06)

    def puff(self, f):
        """A little breath cloud off a fighter who is sucking wind."""
        hx, hy = f.head_pos()
        self.parts.append([hx + f.facing * 6, hy + 2, f.facing * random.uniform(14, 26),
                           random.uniform(-26, -12), random.uniform(0.3, 0.5), (210, 225, 245)])

    def dust(self, x, y=GROUND):
        for _ in range(16):
            a = random.uniform(math.pi * 1.05, math.pi * 1.95)
            sp = random.uniform(20, 70)
            self.parts.append([x + random.uniform(-14, 14), y - 1, math.cos(a) * sp, math.sin(a) * sp * 0.5,
                               random.uniform(0.25, 0.5), random.choice([(214, 214, 230), (180, 182, 204)])])

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
        wx += spec.get("reach", 0)
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
    STORY_PHASES = ("scene", "menu", "retire", "yacht")

    def draw(self, out):
        c = self.canvas
        p = self.player
        if self.mode == "campaign" and self.phase in self.STORY_PHASES:
            self.draw_story(c)
            self.draw_info(c)
            out.fill((20, 16, 28))
            out.blit(c, (0, 0))
            return
        if self.arena:
            c.blit(self.arena_bg, (0, 0))
            self.crowd.draw(c, self.clock, self.hype)
            self.draw_sweep(c)
            c.blit(self.arena_bg, (0, BOARDS_Y), (0, BOARDS_Y, VW, VH - BOARDS_Y))   # boards, ropes, ring in front of the fans
            c.blit(self.rope_overlay, (0, 0))
            c.blit(self.lights, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        else:
            c.blit(self.bg if self.mode == "bag" else self.spar_bg, (0, 0))
        champ = self.mode == "campaign" and self.phase == "champion"
        if champ:
            self.draw_spotlight(c, p.x + 4, p.gy())
        if self.mode == "bag":
            c.blit(self.bag_shadow, (int(self.bag.bottom_x()) - 20, GROUND - 4))
            self.bag.draw(c)
            p.draw(c)
            if p.counter_t > 0 and int(p.counter_t * 14) % 2 == 0:
                draw_text(c, self.font_s, "COUNTER READY", p.x + 6, p.gy() - 96, (120, 220, 255), center=True)
        else:
            cpu = self.cpu
            if self.phase in ("fight", "down"):
                self.draw_ropes_flex(c, back=True)
            def depth_key(f):                      # far first; the puncher wins a tie
                return (round(f.z, 1), 1 if f.action in PUNCHES else 0, 0 if f.out_cold else 1)
            order = sorted([cpu, p], key=depth_key)
            back, front = order
            # standing right in front of him? see through yourself a little so you can read him
            fade = 255
            if (front.z - back.z > 8 and abs(front.x - back.x) < 34 and not back.out_cold
                    and self.phase in ("fight", "down", "intro")):
                fade = FRONT_FADE
            layers = [(f.z, 0, f) for f in order]
            if self.ref.on:
                layers.append((self.ref.z, -1, self.ref))
            for _, _, thing in sorted(layers, key=lambda t: (t[0], t[1])):
                if thing is self.ref:
                    thing.draw(c, self.clock)
                else:
                    thing.draw(c, fade if thing is front else 255)
            for f in order:
                self.draw_dizzy(c, f)
            if p.counter_t > 0 and int(p.counter_t * 14) % 2 == 0 and self.phase == "fight":
                draw_text(c, self.font_s, "COUNTER READY", p.x + 6, p.gy() - 96, (120, 220, 255), center=True)
        if self.mode != "bag" and self.phase in ("fight", "down"):
            self.draw_ropes_flex(c)
        if self.mode == "campaign" and self.phase == "defeat":
            self.draw_defeat_mood(c)
        if self.mode != "bag" and p.hurt and self.phase == "fight":
            self.draw_hurt_vignette(c)

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
        if self.saved_t > 0:
            self.chip(c, "CAREER SAVED", VW // 2, 44, (150, 240, 160), center=True)
        elif self.saved_t < 0:
            self.chip(c, "COULD NOT SAVE", VW // 2, 44, (255, 130, 120), center=True)
        self.draw_info(c)

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

    def draw_ropes_flex(self, c, back=False):
        """The ropes bow outward behind a fighter who is pinned on them (back=True: the far ropes,
        drawn before the fighters since they are behind him; otherwise the side ropes)."""
        for f in (self.player, self.cpu):
            if not f.on_ropes() or f.down or f.out_cold:
                continue
            ux, uz = f.u()
            bx, bz = f.x - ux * ROPE_ZONE, f.z - uz * ROPE_ZONE
            x = int(f.x)
            if bz < Z_MIN:                                   # the far ropes, behind him
                if not back:
                    continue
                for ry, col in zip(ROPES, RING_ROPE_COLS):
                    pts = [(x - 26, ry), (x, ry - 3), (x + 26, ry)]
                    pygame.draw.lines(c, (20, 18, 30), False, [(a, b + 1) for a, b in pts], 3)
                    pygame.draw.lines(c, col, False, pts, 2)
            elif back:
                continue
            elif bx < MIN_X or bx > STAGE_MAX_X:              # the side ropes
                side = -1 if bx < MIN_X else 1
                gy = f.gy()
                for k, col in enumerate(RING_ROPE_COLS):
                    y = gy - 16 - 12 * k
                    pts = [(x + side * 10, y - 14), (x + side * 4, y), (x + side * 10, y + 14)]
                    pygame.draw.lines(c, (20, 18, 30), False, [(a + 1, b) for a, b in pts], 3)
                    pygame.draw.lines(c, col, False, pts, 2)

    def draw_story(self, c):
        """Between-fights screens: the conversation, the save menu and the two endings."""
        ph = self.phase
        if ph == "yacht":
            self.yacht.draw(c)
        else:
            c.blit(self.arena_bg if (self.bout().get("act", 1) > 1 or ph == "menu") else self.bg, (0, 0))
            if ph != "menu":
                self.crowd.draw(c, self.clock * 0.25, 0.0) if False else None
            dim = pygame.Surface((VW, VH), pygame.SRCALPHA)
            dim.fill((8, 6, 18, 222 if ph == "retire" else 206))
            c.blit(dim, (0, 0))
        gold, white, label = (255, 214, 90), (232, 236, 250), (170, 180, 215)
        if ph == "menu":
            self.draw_menu(c)
            return
        if ph in ("scene", "retire"):                      # chapter heading
            band = pygame.Surface((VW, 20), pygame.SRCALPHA)
            band.fill((10, 8, 20, 190))
            c.blit(band, (0, 14))
            c.fill((92, 80, 120), (0, 14, VW, 1))
            c.fill((92, 80, 120), (0, 33, VW, 1))
            if ph == "retire":
                draw_text(c, self.font_m, "THE END OF THE ROAD", VW // 2, 19, (255, 120, 110), center=True)
            else:
                draw_text(c, self.font_m, "ACT %s" % ("I" * self.bout().get("act", 1)), 10, 18, gold)
                draw_text(c, self.font_s, "RECORD  %s" % self.record(), VW - 10, 20, label, right=True)
                draw_text(c, self.font_s, self.bout().get("bout", ""), VW // 2, 20, white, center=True)
        if self.scene and not self.scene.done():
            self.scene.draw(c)
            return
        if ph == "retire":
            self.end_card(c, "CAREER OVER", (255, 120, 110),
                          "FINAL RECORD  %s   -   %d BY KNOCKOUT" % (self.record(), self.kos),
                          "ENTER  BACK TO THE GYM")
        elif ph == "yacht":
            sub = "UNDEFEATED  %s" % self.record() if self.losses == 0 else "RECORD  %s" % self.record()
            self.end_card(c, "LIGHTWEIGHT CHAMPION OF THE WORLD", gold,
                          "%s   -   %d BY KNOCKOUT" % (sub, self.kos), "ENTER  BACK TO THE GYM")

    def end_card(self, c, title, col, sub, prompt):
        band = pygame.Surface((VW, 54), pygame.SRCALPHA)
        band.fill((10, 8, 20, 205))
        c.blit(band, (0, 50))
        c.fill(col, (0, 50, VW, 1))
        c.fill(col, (0, 103, VW, 1))
        font = self.font_l if self.font_l.size(title)[0] < VW - 16 else self.font_m
        draw_text(c, font, title, VW // 2, 58, col, center=True)
        draw_text(c, self.font_s, sub, VW // 2, 78, (232, 236, 250), center=True)
        if int(self.clock * 2.5) % 2 == 0:
            draw_text(c, self.font_s, prompt, VW // 2, 91, (255, 214, 90), center=True)

    def draw_menu(self, c):
        d = self.save_data or {}
        gold, white, label = (255, 214, 90), (232, 236, 250), (170, 180, 215)
        draw_text(c, self.font_l, "YOUR CAREER", VW // 2, 26, gold, center=True)
        i = clamp(int(d.get("idx", 0)), 0, len(CAREER) - 1)
        opp = FIGHTERS[d.get("rebuild") or CAREER[i]["opp"]]["short"]
        rows = [("CONTINUE CAREER", "ACT %s   %s   RECORD %d-%d" % (
            "I" * CAREER[i].get("act", 1), opp, int(d.get("wins", 0)), int(d.get("losses", 0)))),
            ("NEW CAREER", "start again from the first night - erases the save")]
        for k2, (name, sub) in enumerate(rows):
            r = pygame.Rect(34, 52 + k2 * 36, VW - 68, 30)
            on = k2 == self.menu_i
            plate = pygame.Surface(r.size, pygame.SRCALPHA)
            plate.fill((26, 22, 44, 240) if on else (14, 12, 26, 210))
            c.blit(plate, r.topleft)
            pygame.draw.rect(c, gold if on else (74, 66, 96), r, 1)
            draw_text(c, self.font_m, name, r.x + 10, r.y + 5, gold if on else white)
            draw_text(c, self.font_s, sub, r.x + 10, r.y + 18, label)
            if on and int(self.clock * 3) % 2 == 0:
                draw_text(c, self.font_m, ">", r.x - 9, r.y + 5, gold)
        draw_text(c, self.font_s, "UP / DOWN  CHOOSE        ENTER  START        TAB  BACK TO BAG",
                  VW // 2, VH - 34, label, center=True)

    def draw_sweep(self, c):
        """Two search lights sweeping the crowd before the fight and during the celebrations."""
        if self.phase not in ("walkin", "talk", "reply", "intro", "champion"):
            return
        for k, sp in ((0, 0.7), (1, -0.55)):
            x = VW / 2 + math.sin(self.clock * sp + k * 2.1) * VW * 0.45
            glow = self.sweep_glow
            c.blit(glow, (int(x) - glow.get_width() // 2, 18), special_flags=pygame.BLEND_RGB_ADD)

    def draw_dizzy(self, c, f):
        """Little stars circling the head of a hurt / downed / knocked-out fighter."""
        if not (f.hurt or f.down or f.out_cold or (f.ko and not f.won)):
            return
        hx, hy = f.head_pos()
        n = 3 if f.hurt and not (f.down or f.out_cold or f.ko) else 4
        for i in range(n):
            a = self.clock * 5 + i * math.tau / n
            x = hx + math.cos(a) * 9
            y = hy - 8 + math.sin(a) * 3
            col = (255, 236, 110) if i % 2 == 0 else (255, 255, 255)
            if math.sin(a) < 0:
                col = darken(col, 0.35)
            c.fill(col, (int(x), int(y) - 1, 1, 3))
            c.fill(col, (int(x) - 1, int(y), 3, 1))

    def draw_hurt_vignette(self, c):
        k = 0.5 + 0.5 * math.sin(self.clock * 7.4)
        a = int(40 + 50 * k)
        v = pygame.Surface((VW, VH), pygame.SRCALPHA)
        for i in range(10):
            col = (180, 10, 20, max(0, a - i * 9))
            pygame.draw.rect(v, col, (i, i, VW - 2 * i, VH - 2 * i), 1)
        c.blit(v, (0, 0))

    def draw_count(self, c):
        dn = self.dn
        if not dn:
            return
        d = dn["who"]
        n = dn["count"]
        gold, white = (255, 232, 130), (230, 232, 250)
        if dn["final"]:
            if self.phase_t > 0.6:
                draw_text(c, self.font_l, "THIRD KNOCKDOWN!", VW // 2, 52, (255, 90, 80), center=True)
            return
        if n > 0:
            k = clamp((self.phase_t - (dn["next"] - COUNT_DT)) / 0.25, 0.0, 1.0) if dn["next"] else 1.0
            font = self.font_huge if k >= 1 else self.font_xl
            col = (255, 90, 80) if n >= 8 and not dn["up"] else gold
            draw_text(c, font, str(n), VW // 2, 46 if k >= 1 else 50, col, center=True)
        if d is self.player and not dn["up"]:
            if d.rising_t >= 0:
                draw_text(c, self.font_m, "GETTING UP...", VW // 2, 78, (150, 240, 160), center=True)
            else:
                blink = int(self.clock * 6) % 2 == 0
                draw_text(c, self.font_m, "MASH  A  S  D  F  TO GET UP!", VW // 2, 78, gold if blink else white,
                          center=True)
                w = 110
                x = VW // 2 - w // 2
                pygame.draw.rect(c, (20, 14, 30), (x - 1, 91, w + 2, 7))
                c.fill((52, 40, 62), (x, 92, w, 5))
                f = clamp(self.mash / self.mash_need, 0.0, 1.0)
                c.fill((120, 230, 140) if n >= 2 or f < 1 else (240, 210, 70), (x, 92, int(w * f), 5))
                c.fill((200, 255, 210), (x, 92, int(w * f), 1))
        elif dn["up"] and n < STANDING_COUNT:
            draw_text(c, self.font_s, "STANDING EIGHT COUNT", VW // 2, 78, white, center=True)

    def chip(self, c, text, x, y, col, center=False, right=False):
        """Small label on its own dark plate, so warnings stay readable over the crowd."""
        w = self.font_s.size(text)[0]
        bx = x - w // 2 - 3 if center else (x - w - 3 if right else x - 2)
        plate = pygame.Surface((w + 6, 11), pygame.SRCALPHA)
        plate.fill((12, 10, 24, 205))
        c.blit(plate, (bx, y - 1))
        c.fill(darken(col, 0.55), (bx, y - 1, w + 6, 1))
        c.fill(darken(col, 0.55), (bx, y + 9, w + 6, 1))
        draw_text(c, self.font_s, text, bx + 3, y + 1, col)

    def draw_kd_pips(self, c, f, x, y, right):
        for i in range(MAX_DOWNS):
            px = (x - 7 * i - 5) if right else (x + 7 * i)
            pygame.draw.rect(c, (20, 14, 30), (px - 1, y - 1, 7, 5))
            if i < f.downs:
                c.fill((236, 70, 60), (px, y, 5, 3))
                c.fill((255, 160, 140), (px, y, 5, 1))
            else:
                pygame.draw.rect(c, (120, 112, 150), (px, y, 5, 3), 1)

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

    def draw_spotlight(self, c, x, gy=GROUND):
        glow = pygame.Surface((VW, VH), pygame.SRCALPHA)
        sway = math.sin(self.clock * 1.7) * 6
        pygame.draw.polygon(glow, (255, 236, 170, 34), [(x - 8 + sway, 0), (x + 8 + sway, 0), (x + 44, gy + 4),
                                                         (x - 44, gy + 4)])
        pygame.draw.ellipse(glow, (255, 236, 170, 46), (x - 46, gy - 6, 92, 14))
        c.blit(glow, (0, 0))

    def draw_defeat_mood(self, c):
        a = int(min(1.0, self.phase_t / 0.8) * 110)
        dim = pygame.Surface((VW, VH), pygame.SRCALPHA)
        dim.fill((8, 6, 24, a))
        c.blit(dim, (0, 0))
        if self.phase_t < 0.5:
            return
        p = self.player                               # a little rain cloud over the loser
        cx, cy = int(p.x) + 8, p.gy() - SPRITE_FEET + 14
        if p.out_cold:
            hx, hy = p.head_pos()
            cx, cy = int(hx) + 4, int(hy) - 34
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
        draw_text(c, self.font_s, self.bout_line(), 12 + off, y + 4, (170, 180, 215))
        draw_text(c, self.font_l, o["name"], 12 + off, y + 14, o["color"])
        draw_text(c, self.font_s, o["title"], 12 + off, y + 31, (255, 214, 90) if o.get("champ") else (230, 232, 250))
        if o.get("champ"):
            c.blit(self.belt, (VW - 50 + off, y + 15))

    def panel_surface(self):
        """The contents of the open panel (cached; only the mode word changes)."""
        mode = "SPAR" if self.mode == "bag" else "BAG"
        if mode in self._panel:
            return self._panel[mode]
        w, h = INFO_PANEL.size
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        gold, white, label = (255, 214, 90), (232, 236, 250), (165, 175, 210)
        draw_text(s, self.font_m, "CONTROLS & MOVES", w // 2, 3, gold, center=True)
        s.fill((70, 60, 92), (10, 18, w - 20, 1))
        lx, rx = 8, 154
        draw_text(s, self.font_s, "YOUR MOVES", lx, 23, label)
        draw_text(s, self.font_s, "HOW TO WIN", rx, 23, label)
        for i, (key, what) in enumerate(MOVE_ROWS):
            y = 36 + i * 9
            draw_text(s, self.font_s, key, lx, y, gold)
            draw_text(s, self.font_s, what, lx + 56, y, white)
        for i, tip in enumerate(FIGHT_TIPS):
            y = 36 + i * 9
            s.fill((120, 110, 150), (rx + 1, y + 4, 2, 2))
            draw_text(s, self.font_s, tip, rx + 7, y, white)
        s.fill((70, 60, 92), (10, h - 25, w - 20, 1))
        draw_text(s, self.font_s, "TAB  %s        C  CAMPAIGN        BKSP  RESET" % mode,
                  w // 2, h - 22, label, center=True)
        draw_text(s, self.font_s, "ENTER CONTINUE   S SAVE CAREER   M MUTE   ESC CLOSE",
                  w // 2, h - 12, label, center=True)
        self._panel[mode] = s
        return s

    def draw_info(self, c):
        t = self.info_t
        if t > 0:
            ease = 1 - (1 - t) ** 3
            dim = pygame.Surface((VW, VH), pygame.SRCALPHA)
            dim.fill((6, 5, 16, int(165 * t)))
            c.blit(dim, (0, 0))
            r = pygame.Rect(0, 0, int(self.info_rect.w + (INFO_PANEL.w - self.info_rect.w) * ease),
                            int(self.info_rect.h + (INFO_PANEL.h - self.info_rect.h) * ease))
            r.centerx = int(self.info_rect.centerx + (INFO_PANEL.centerx - self.info_rect.centerx) * ease)
            r.centery = int(self.info_rect.centery + (INFO_PANEL.centery - self.info_rect.centery) * ease)
            plate = pygame.Surface(r.size, pygame.SRCALPHA)
            plate.fill((14, 12, 26, 244))
            c.blit(plate, r.topleft)
            pygame.draw.rect(c, (92, 80, 120), r, 1)
            c.fill((255, 214, 90), (r.x + 1, r.y, r.w - 2, 1))
            if t > 0.5:
                body = self.panel_surface()
                body.set_alpha(int(255 * min(1.0, (t - 0.5) / 0.4)))
                c.set_clip(r)
                c.blit(body, INFO_PANEL.topleft)
                c.set_clip(None)
        hot = self.hover == "info" or self.info_open
        img = self.info_icon_hi if hot else self.info_icon
        c.blit(img, img.get_rect(center=INFO_CENTER))
        if not self.info_seen and t <= 0 and self.clock < 30:
            fade = min(1.0, (30 - self.clock) / 3.0) * (0.55 + 0.45 * math.sin(self.clock * 3))
            a = int(215 * fade)
            hx, hy = INFO_CENTER[0] + 15, INFO_CENTER[1] - 4
            for col, off in (((10, 8, 20), (1, 1)), ((214, 220, 240), (0, 0))):
                hint = self.font_s.render("CONTROLS", False, col)
                hint.set_alpha(a)
                c.blit(hint, (hx + off[0], hy + off[1]))

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
        sy = gy + 4                                      # wind (stamina)
        pygame.draw.rect(c, (20, 14, 30), (x - 1, sy - 1, w + 2, 5))
        c.fill((46, 42, 36), (x, sy, w, 3))
        if f.gassed:
            scol = (255, 180, 60) if int(self.clock * 7) % 2 else (190, 120, 40)
        else:
            scol = (240, 214, 110)
        seg(0, f.stam / STAM_MAX, scol, sy, 3)
        gx = x + (w - int(round(w * GAS_LINE / STAM_MAX)) if mirror else int(round(w * GAS_LINE / STAM_MAX)))
        c.fill((120, 100, 70), (gx, sy, 1, 3))

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
        self.draw_kd_pips(c, self.player, 8, 44, False)
        self.draw_kd_pips(c, self.cpu, VW - 8, 44, True)
        secs = int(math.ceil(self.round_time))
        tcol = (255, 232, 130) if secs > 10 or int(self.clock * 4) % 2 else (255, 90, 80)
        draw_text(c, self.font_l, "%02d" % secs, VW // 2, 32, tcol, center=True)
        if camp:
            draw_text(c, self.font_s, "%d-%d" % (self.wins, self.losses), VW // 2 - 14, 36, label, right=True)
        if self.phase == "fight":
            for f, fx, rt in ((self.player, 8, False), (self.cpu, VW - 8, True)):
                warn = None
                if f.gassed:
                    warn, wcol = "GASSED", (255, 190, 70)
                elif f.on_ropes() and not f.clinch:
                    warn, wcol = "ON THE ROPES", (255, 130, 120)
                if warn and int(self.clock * 3) % 2:
                    self.chip(c, warn, fx, 50, wcol, right=rt)
            if self.ai.read_t > 0 and int(self.clock * 4) % 2:
                self.chip(c, "HE'S READING YOU - MIX IT UP", VW // 2, 88, (255, 160, 100), center=True)
        if self.combo >= 2 and self.phase == "fight":
            draw_text(c, self.font_xl, "%d HIT COMBO!" % self.combo, VW // 2, 64, (255, 120, 100), center=True)

        gold, white = (255, 214, 90), (230, 232, 250)
        if self.phase == "intro":
            self.banner(c, 50, 44)
            msg = "ROUND 1" if self.phase_t < 0.9 else "FIGHT!"
            draw_text(c, self.font_huge, msg, VW // 2, 54, (255, 232, 130), center=True)
            sub = self.bout_line() if camp else "1 EASY   2 NORMAL   3 HARD"
            draw_text(c, self.font_s, sub, VW // 2, 83, label, center=True)
        elif self.phase == "down":
            self.draw_count(c)
        elif self.phase == "ko":
            if self.end_reason == "time":
                draw_text(c, self.font_huge, "TIME!", VW // 2, 52, (255, 90, 80), center=True)
                if self.phase_t > 0.7:
                    draw_text(c, self.font_s, "GOING TO THE JUDGES' SCORECARDS...", VW // 2, 82, white, center=True)
            elif self.phase_t > 0.25:
                pulse = (255, 90, 80) if int(self.clock * 6) % 2 else (255, 200, 90)
                draw_text(c, self.font_huge, self.METHOD_TEXT[self.method], VW // 2, 50, pulse, center=True)
                draw_text(c, self.font_s, self.METHOD_SUB[self.method], VW // 2, 80, white, center=True)
        elif self.phase == "walkin":
            self.draw_name_card(c)
        elif self.phase == "victory":
            self.banner(c, 40, 36)
            draw_text(c, self.font_xl, "VICTORY!", VW // 2, 43, (120, 240, 140), center=True)
            draw_text(c, self.font_s, "%s   -   %s" % (self.method_line(), self.next_label()),
                      VW // 2, 63, white, center=True)
            if int(self.clock * 2.5) % 2 == 0:
                draw_text(c, self.font_s, "ENTER  CARRY ON        S  SAVE AND STOP HERE", VW // 2, 76, gold,
                          center=True)
        elif self.phase == "defeat" and self.step >= 2:
            self.banner(c, 36, 28)
            draw_text(c, self.font_l, "DEFEATED", VW // 2, 38, (255, 90, 80), center=True)
            left = MAX_LOSSES - self.losses
            tail = ("THAT IS YOUR LICENCE GONE" if left <= 0 else
                    ("ONE MORE LOSS ENDS YOUR CAREER" if left == 1 else "RECORD %s" % self.record()))
            draw_text(c, self.font_s, tail, VW // 2, 52, (255, 170, 120), center=True)
            draw_text(c, self.font_s, "ENTER  CARRY ON        S  SAVE AND STOP HERE", VW // 2, 62, white,
                      center=True)
        elif self.phase == "champion":
            pulse = (255, 214, 90) if int(self.clock * 4) % 2 else (255, 250, 200)
            draw_text(c, self.font_l, "NEW LIGHTWEIGHT CHAMPION!", VW // 2, 40, pulse, center=True)
            if self.phase_t > 1.5 and self.step >= 2:
                draw_text(c, self.font_s, "ENTER  ...", VW // 2, 58, white, center=True)
        elif self.phase == "result":
            self.banner(c, 46, 56)
            col = (120, 240, 140) if self.result == "YOU WIN!" else ((255, 232, 130) if self.result == "DRAW" else (255, 90, 80))
            draw_text(c, self.font_huge, self.result, VW // 2, 47, col, center=True)
            draw_text(c, self.font_s, self.method_line(), VW // 2, 69, label, center=True)
            draw_text(c, self.font_m, "ENTER  REMATCH        TAB  BACK TO BAG", VW // 2, 80, (230, 232, 250), center=True)
            draw_text(c, self.font_s, "1 EASY   2 NORMAL   3 HARD", VW // 2, 92, label, center=True)

    def bout_line(self):
        """How tonight's fight is billed."""
        if self.rebuild:
            return "TUNE-UP BOUT   -   RECORD %s" % self.record()
        b = self.bout()
        return "ACT %s   -   %s" % ("I" * b.get("act", 1), b.get("bout", "LIGHTWEIGHT"))

    def method_line(self):
        m = self.method or "DECISION"
        if m == "DECISION":
            return "WON ON THE JUDGES' SCORECARDS" if self.result == "YOU WIN!" else "LOST ON THE JUDGES' SCORECARDS"
        if m == "DRAW":
            return "SCORED A DRAW"
        return "BY %s  -  %s" % (self.METHOD_TEXT[m].rstrip("!"), self.METHOD_SUB[m])

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
FEINT_KEYS = (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_g)   # hold + a punch = feint it
CLINCH_KEY = pygame.K_q
PIVOT_KEY = pygame.K_x                            # roll round him and off the ropes
INFO_KEYS = (pygame.K_i, pygame.K_F1)             # open the controls panel


def handle_key(game, key):
    """One key press. Returns False if the game should quit."""
    if key in INFO_KEYS:
        game.toggle_info()
        return True
    if key == pygame.K_ESCAPE:
        if game.info_open:
            game.toggle_info()                    # shut the panel first, quit on the next press
            return True
        return False
    if game.info_open:
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            game.toggle_info()
        elif key == pygame.K_m:
            game.toggle_mute()
        elif key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
        return True
    if key in PUNCH_KEYS and not (game.mode == "campaign" and game.phase in ("victory", "defeat", "scene", "menu")):
        name = PUNCH_KEYS[key]
        held = pygame.key.get_pressed()
        arrows = (held[pygame.K_UP], held[pygame.K_DOWN], held[pygame.K_LEFT], held[pygame.K_RIGHT])
        if name == "slip" and any(arrows) and game.mode != "bag":
            game.side_step((1 if arrows[1] else 0) - (1 if arrows[0] else 0),
                           (1 if arrows[3] else 0) - (1 if arrows[2] else 0))   # step to the side, off his line
            return True
        if name != "slip" and any(held[k] for k in FEINT_KEYS):
            name = "feint_" + name
        game.press(name)
    elif key == CLINCH_KEY:
        game.clinch()
    elif key == PIVOT_KEY:
        game.pivot()
    elif key == pygame.K_s and game.mode == "campaign" and game.phase in ("victory", "defeat", "scene"):
        game.save_and_quit()
    elif key in (pygame.K_UP, pygame.K_DOWN) and game.mode == "campaign" and game.phase == "menu":
        game.menu_move(1 if key == pygame.K_DOWN else -1)
    elif key in (pygame.K_UP, pygame.K_DOWN):
        game.tap_depth(1 if key == pygame.K_DOWN else -1)
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
    """(left, right, low, block, far, near) from the keys currently held down."""
    low = keys[LOW_BLOCK_KEY]
    return (keys[pygame.K_LEFT], keys[pygame.K_RIGHT], low, keys[HIGH_BLOCK_KEY] or low,
            keys[pygame.K_UP], keys[pygame.K_DOWN])


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
QsrAiG1/KYN4ZeVRpQ9EOVRTFDfehfYVvQu8B+0IaQ949psX2g4T+3Yw/58W8U+L+KfXRhnYTHk897N5Pfez+Uo/482u7TLIw/vg
Z55Z0zfylc/iG+/r5IsnS/8OH+JerO77QOzjdVUHEf+B2HUY+j/NqrsGGbsORvwHYtff3TWwstjzHuQr239y79yR/u+L1iBDnn3K
wS/2+bfrnpC/n7jnq7L+GLr/k7iXqxp/1uDbEbr+m1cG7AVqTsj6r1sOMf0igzLIamMPRB5i3+4eoCLEfqDreWdin0X80yL+adWZ
f6vy7xH/gbaefcZf4dj/nFYb9Q/xD8f+n3RS7Dkh/gNd930k4m+j7kmL/A9p8fyPrkcOT+u9hd7eQhP//U+fyXyPST4ZsxZvUBbV
fHDqUX2x8kLp9939/LO6+9FD/Y9nd05ocW098z2UQRjz/Evqx/7yynI/+WQe8/6YuM/unNCxiR2anXlQEvGXaANSI/7lWktAGbMA
GaMo87OkTAbQcUb80yL+6aSKvUT8JZ791NqKv42yKNZm7G2UwzCe/7So/9OpGvuyxS/6PmHqxj9v0z/Pfjjqn/TsMmiyHCiDapp+
JyiHepooB8qgmibfBcogTNPtAXEP00Y7TOzL0QdNi/inRfzT62Ie1P537ESUbjLK5bfe19kzZ1r9OUZRm2XAnFx1n1xd3eZLRGl+
nXzxpN5/683c22Oph6pp4n0g9nG6HO9KxF+i/5Ma8U+niTWwsu+lHIqFHgCzVUk6RjkMY/9JetT/abH+O1oYA4yWmHJgT1AzupoP
lYi91E68qXvCdPms24h9D89+Wjz/afH8p5NyzZH49zD/kBbxT4v4p8P597SIf1rUPWkR/7SI/2goir99CaSx8vbF/i9JuRdO0Q7U
8/rSijcJ7v6nz/STULq/bB8+d0Ifnjlf+u9QBn558Zc0FOsvVl7Qxz+aHfo7fO+PLwnluKINSIv4h2ktAaU0vAklrzAW33hfJ188
Gfz3uodb8ozroReD+KdF/NPxxd4X/7ZiLxF/nv10QjeAxsbfRln4xXQ+68TfoByGtVX/2Ih7Pur/dOj7pMWzn15IGVSp+ymDcL4E
Dy7KoDt5/dKqfSDKoZomy4EyqMZXBrwH7XLbAxvPfnvK2mFi3w7GAWkR/7SIf3pdzIOaf8duZ9xklGfPnClM6Hcza7MMmJOrx/fc
ml9lzyr1UDVNvA/EPk6TdRB1Thj6P2kR/3RYf0+H/Sfp8fynxxpwWqz/jpYU644S5eBi/TcdYt+tNtpg6p4wjH/TaiP+PPvheP7T
4vlPp60zABLPfyjmH9Ki/k+L+KeTOvYS8Sf+6aSO/zjHXiL+qRH/tMrW4H2XQC6cXc38KroEknag2O7JqY3VT1a8X7t37oheX/J/
TZI+OPXo0C9JeunUucJ/c3FtPfdr41YGVePvJgA1QhJ+Ev8s2oC0iH+5Tg6D7J6c2jC//9oDD3m/J+Zwyu7JqY2vPfCQnv/5sczn
fQEf10MvNuKfFvFPx4695I9/E7GXiL8Pz35aJv55sZeqx4myKGbiU6ZubCiHfE3XP+7fTdyLUf+nQ98nLZ799MrKIDZOlEE1Rf1Q
yqBbvn5plThRDvU0UQ6UQT1uGfAedINnP428dpjYt4dxQFrEPy3in16b86Ah/6aksS+HNsqAObl0qIfqqfM+EPtqmqiDqHPi0P9J
i/inw/p7Ouw/SY/nPz3WgNNj/Xd0tLn2IlEOoVgDS4fYd6vJNpi6Jw7j37SajD/Pfjye/7R4/tNp+gyA+Tt5/sMx/5AW9X9axD+d
rmIvEX8f4p8WdU9axD8t4p+WO8985tV/yHzdJB9j/aVZJj5uvCXp04MzmQSgdhmYZJO2lbcvSpIeO3FBxyZ2aHbnxND3mOSH8+vX
tbh8buzLoKn473/6jD7+0aw+PHNedz//rHT+vUwyysW19X55LK6tE38P2oC0iH++zn8wd0LUqHro1/X+W2/W+ntvdsQ/LeKfli/+
TcVeIv5FePbTyYu9VC9OlEWxorgbTcSGcijXVP3j/p3EPQz1f1r0fdLh2U+vieff/D2UQTWUwWhoKjkM5VBPE+VAGdRjlwHvQXd4
9tMh9mkwDkiL+KdF/NNrYx4UcZosA+bk0qEeakaV94HY11OnDqLOqYb+T1rEPx3W37vH/pPRwfOfHuuPaRH/0dDm/L9EOYRiHSYd
Yp8G+xDTYfybVhPx59mvjuc/LZ7/tBh/pUX806L+T4v4p9N27CXiX4T4p0XdkxbxT4v4p9F0Anr776UdyOdLgrj4xvu672c/0pGv
3Jv53rLkkwtnV/XblQvbdk9ObbhJKO3kk3Z5jHsZNBF/OwGljy8BpSmDcY+/D21AWsQ/a6R/uDJNTeahGuKfFvFPh0N8afHsjw7K
YjRQDmkQ9+4R83To+6TFs58eZZAeZTAaKIf0KIP0KIM0iHs6xD4dYp8W8U+L+AM9zMmlQz2UDrFPhzonLZ79tIj/aKAcRgPlkAZx
T4O4p0X802MMMBp4F9Ih9mlQ96TFc58Oz356PP/p8Pynx/OfFvFPi/inRfzTof1Ni/inRd2TFvFPi/hX03TcaAeK+RK1uUnaJOnV
Zw/k/h0m+aT9dx6b2JH5nvn160N/jjKIi//0/fuGPr//6TNyE37aTAJKOwmoQfzbRRuQ1s0Q/y31wwIAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAYfW6iNl+StiemD3gTeUrKJJ+M+TvRkxcrN+Zz35jy/vnHTlzITUJpEk9KveSTlAOwdfCyAgAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAMAYyksCunTpuiTp2MSO3D9L8klg6/n/A3+Ha/Q8holbAAAAAElFTkSuQmCC
"""
VIEW_F_B64 = """
iVBORw0KGgoAAAANSUhEUgAAFKAAAABQCAYAAACAcsl9AABuuUlEQVR4nO3db2jd153v+09MyAg1KMYYI/uYSdg1xezRSYsxwScI
EUIIB2FyjK9x+6CY1icEn54yiDD0mMH4gQjFt/QGUebGxmSMCXkwDcboBqMHwQQjhMcEYzIejzCDRzRFJMEY4RpFbAYT3Qdba2vt
3/79//fdkt4vMK2lbXX3u5fWb/3Wn8/vGQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEGN4qLHq//3bJwvPWL0XAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC2nmes3wAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAEA/Gx5qrLr//u2ThQ2Z5bgh3zQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEDVXPDkh9u3S5Lm
llu6/LQlaeMFUW6oNwsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFCH4aHGqgueDHJBlBsphHKb9RsAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAABAtQigBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8AwPNVY/3L498vujzw/oF88OaHiosVrf
uyrmWes3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUIawQMhvnyw8Y/Fe+g0BlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAYMMbHmqsfvOr8a6vnb90Q5NqrBJCSQAlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADY4Pzwya+mb3W+Pr5jQFoS
IZTqswDK4aHGatjXt/qHBAAAAAAAAAAAAAAbDeu/tqg/tjLavy3qDwAAAAAAAAAAgM2E9S8AAAAAAFC1tPMPYa9jjqKbHz6pQz/R
i0oOodyK8z998X/MFf7Y66M935ue/VxPnz4naXN/EP1gK/4C9BPqb4v626L+tqg/tjLaPwAAAAAAqBrzD7aovw3Wf21R//5A/2OD
9m+L+vcH+h8AAAAAAFA15h8AAKgf118brH8BAGCH8Q+2Mto/AGwtWeYfhocaqx9u3971mrnlli4/bXGdWOOHT/qhk2FmllqabK1I
Sq6/JAVr75tbbknShvoszN/k8FBj1S/87JdfhL5u6cmynj59bsMUdiNhAtQW9bdF/W1Rf1vUvz8wAWSD9g8AgB3GP7aoPwBsTfT/
Nph/sEX97bD+a4v626P/sUP7t0X97dH/9AfuvwAAqB/XXwAA6sP8Q39g/IOtjPaPrYjrrx3WvwAAsMH4B1sZ7R8Atp6s8w9RAYiE
UK5zAZRJ4ZPSegCl+wyS6v/g6zuxP2/fngMb6jMwfaN+448qvI9JuPIxAWqL+tui/raovy3qb48JIDu0fwAAbDD+sUX9AVjjAIAN
+n87zD/Yov52WP+1Rf3t0f/Yof3bov726H/scf8FAFsb8582uP4CAFAv5h/sMf7BVkb7x1bF9dcO618AANhg/NM/WP+qH+0fALae
LPMPD5f+MzJ80iGEsi1PAOWuHc8lvjZNCCUBlCllnXxzGAiVhwlQW9TfFvW3Rf1tUX97TADZof33FyagAVih/6kf4x9b1L9/0P9g
K+IAgB36fzvMP9ii/nZY/7VF/e3R/9ih/dui/vbof+xx/9U/mH8DUDfmP+1w/e0fXH8BYGtg/sEe45/+wfinfrT//kH7rxfXXzus
fwHd6P9tUX9b1L9ejH/6A+tfNmj/ALD1lB0+6RBC2a7t2YFBje8YiH3dzFJLklIHUErr1+Dg5zG33P5ZG632Jm/UJYQWsfuDmQ1V
6H7DBKgt6m+L+tui/raovz0mgOzQ/vsHE9D9gQUwbEX0PzYY/9ii/v2B/qc/MP6pHwcA7ND/22H+wRb1t8P6ry3qb4/+xw7t3xb1
t0f/Y4/7r/7A/Ft/YP4NWw3zn3a4/vYHrr8ArDH+rA/zD/YY//QHxj82aP/9gfZfP66/dlj/AtbR/9ui/raof/0Y//QH1r9s0P4B
YOvJOv+w+4MZAigzGh5qrN7asyP2NTNLLU22VpRnLsj/TPzwybG9g/pk/t6Gqb1ZAOWtPTt06OulzteSPixJnde7f7vVG3leTIDa
ov62qL8t6m+L+ttjAsgO7b9/MAFtjwUwbFX0PzYY/9ii/v2B/sce4x8bHACwQ/9vh/kHW9TfFuu/tqi/LfofW7R/W9TfFv2PPe6/
+gPzb/aYf+sPBDDVi/lPO1x/+wPX3/5B/4+tiPFnvZh/sMf4pz8w/rFB++8PtP/6cf21xfoX0Eb/b4v626L+9WP80x9Y/7JB+weA
rSnr/MOhr5cIoMxoeKix+uDrO4mv27fngKR88z+/eHag873LT1s699ZLmrnzcEMFUD5r9T88s9RO7RzbO6jXHq3/Pc7ZgUFNtlZS
vRbxvpq+VWgCFMVQf1vU3xb1t0X97fRMAO1/I/PP2P3BzOpWH+QXQfu3l2UCesfQ81p6sqzhoQbtvkRJC2A7hp6XJGpfAw4A1Iv+
xwbjH1vUvz/Q/9hj/GMjzwEAfgfKQf9vj/kHW9TfFuu/tqi/LfofW7R/W9TfFv2PHe6/+gPzb/aYf7OXFMDkvk/ty8P8px2uv/2B
629/oP/HVsX40wbzD3YY//QHxj82aP/9gfZvh+uvLda/sNXR/9ui/raovx3GP7ZY/7JF+weArSnP/AOqcXZgMNf8z+Wn6/9mZuKg
7i48quw9VsUsgPK3Tx9Lek5/vPKuJOkv8/dS/bvJk9Odf4v8mAC1Rf1tUX9b1N8W9bfFBJAt2r8tJqDtsQDWHzgAUD/6H1uMf2xR
f1v0P/YY/9jgAIA9+n9bzD/Yov62WP+1Rf1t0f/Yov3bov626H9scf9li/k3e8y/2SOAqX7Mf9rj+muL629/oP/vHzyAtl6MP+0w
/2CL8Y8txj+2aP+2aP+2uP7aYv2r/3D/VR/6f1vU3xb1t8X4xw7rX/Zo//2H8SeAOrg5hNnFFc0Gvnf/0pGuv0+enNbcckujzw/U
9O42h48aoxrfEV4z/xr6v268m2v+Z2biYAnv0pbZhW14qLE6tnew8/eLk29q/8npzt/vXzrS9Xf/tbOLK1yUCxgeaqw+++x/6unT
5/TNrTOS0k+A7j85Lfdv+Qzyof62qL8t6m+L+tsaHmqsuskcNwGU1mRrpTMRRP3zof3b6pmAzmH3BzPUv4A8C2BSeyM6bb88SQcA
HOpeHvofW4x/bFF/W/Q/9hj/2Bkeaqze2rOj0AGAQ18v8RnkRP9vi/kHW9TfHuu/tqi/Hfofe7R/W9TfDv2PLe6/bDH/Zo/5N3tZ
PwNqXw7mP21x/bXF9bc/0P/3h6QH0D592g6boe7lYfxph/kHW4x/bDH+sUX7t0X7t8X11x7rX/2D+6960f/bov62qL8txj+2WP+y
RfvvL4w/AdTJ9TnBcej5Szc02VrpmX+QpA+3b4/9mXPL7VDFy09b9FVan2eW1Ami9IMn3fyzlH3+Jyx88u7CI83ceahP5u9tmNqb
vdHjzZHVicONzt+nri3o4uSbktqDHPcB3L90RO+c/UzB126kIvcjJkBtUX9b1N8W9bdF/e0wAWSP9m+HCWhbLID1Bw4A2KD/scX4
xxb1t0X/Y4vxjy0OANii/7fH/IMt6m+L9V9b1N8W/Y8t2r8t6m+L/scO91+2mH+zxfybPQKY7DD/aYvrry2uv/bo//sDD6CtH+NP
e8w/2GH8Y4vxjy3avy3avz2uv7ZY/+oP3H/Vj/7fFvW3Rf3tMf6xw/qXPdp/f2D8CaBu/hrYV9O3ur43s9TSZGtFkjrzD7OLK3rw
9Z3En7tvzwH6qDXHmyOrs4vtOrogSkmd2o7tHezM62Sd/zl9rNnzv7cRAyiftfgfDU6+SdLE4YZe+L/+H+1+4Ye6f+mIpPVB0Dd/
+Q/98//5H12vlbS6kQrdb/zGL0nvnP2sU/fgQDT4C6BrC/pkvqY3uklRf1vU3xb1t0X97Xz7ZOEZNwH002PvS0o/ATS2d1CzizwN
oyjavy33JAA3Ae0/GSCKm3hO81rE+2r6VqEFMBST5wDAjqHntfRkWcNDjVX6/2Lof+ww/rFF/e3R/9hi/GPrt08fS3pOf7zyrqT0
BwAmT053/i3yof+3x/yDLepvh/VfW9TfHv2PHdq/Lepvj/7HDvdf9ph/s8X8m52eAKb9b2T+Gbs/mGENsgDmP+1w/bXH9dcO/X9/
yLIHiL0/5WL8aYv5BzuMf+wx/rFD+7dH+7fF9ddO1PrXO2c/08XJN7vWv3pqL9a/ysL9lx36f1vU3xb1t8X4xxbrX7Zo//YYfwKo
W1z4pCSN7xiQltpBiW7/7e4Xflj329wUoq6p81880NS1hc7Xsu5/PndlPjSEcqMxCaD0ffnvT/STHw1Jkn76N/819DV+8f3XIx8O
ANii/raovy3qb4v622MCyA7t3x4T0LZYALPDAQB79D+2GP/Yov626H9sMf6xwwEAe/T/dph/sEX9+wfrv7aof/3of/oH7d8W9a8f
/Y897r9sMf9mi/k3WwQw2WH+0x7XX1tcf23R/9viAbS2GH/aYf7BHuMfW1nHP/5nMtlaqe6NbRG0f1uM/+0QgNg//PWs2cV24IOr
v/va7IV7unpqpOf1yI/7L1v0/7YYf9qi/dth/GOL9S9btH97jD8B1C0YPvniuVPSrS97gij9EMp//j//Q1dPjWjfngP6cPv20J87
t8yaWBx/Tse31fc/mwRQrg1cVicONzrFnLq2oIuTb3ZeM//FAzVf2dczCPrJj4Y0dW1BDH7KsdV/AaxRf1vU3xb1t0X968cEUP+g
/dePCWh7LIDZ4gCAHfofW2xAt0X9bdH/2GP8Y4sDAHbo//sH8w+2qH/9WP+1Rf37B/1P/Wj/tqh//6D/qR/3X7aYf7PH/JstAphs
Mf9ph+uvLa6/9uj/7fAAWnuMP/sD8w/1Y/xjy41/JGn3ofck9Y53gn/3rxfnL90gBKgA2r8txv/9gwDE+kWtf/l1D65/Oax/Fcf9
ly36f1uMP23R/vsH4x8brH/1B9p//Rh/ArDkAie/On0h8bVT1xY6118XNDn6/EDn++5rl5+2NLZ3kGtzBnn3P58+1jR5v2UzCaCU
1gc2vheaI52F4OYr+zofwsXJN7sm4Zh8K4YDALaovy3qb4v626L+/YMJoPrR/u0xAW2HBTB7HACwRf/TH9iAbov626D/scP4xxYH
APoH/X/9mH+wRf3tsf5ri/rbof+xR/u3Rf3t0P/0D+6/bDD/Zof5N3sEMNlh/rN/cP21wfXXFv2/LR5Aa4fxpy3mH+wdDcy9XT01
Ejn+2f3CD3tei/yGhxqrH27f3vn73HKra9+/3+9I6+E/7tDw+I4BaUmaVIMQgoIY/9tg/G+HAER77jNwf784+SbrXzXi/ssW/b8d
xp/2aP92GP/Yilr/eufsZ7o4+WbX+ldP2xfrX0XR/u0x/gSwEbj5h7G9g7q8uBY8v9z9mstPWzr31kuaufOw/je4ATVf2acJta+7
Urb5n80SPilJJoOI4A2w1L4Jvvy01TUIcua/eCBJDHxK5J6A4fvm1pmujSjuF0ASE6Alo/62gvW/f+lI1wVAov5Vov623AYsJzgA
kqh/lYKTcFEbsCT1TMIxDiqO66+dsAloSfpv//f/13UAQ1LoAQyJ34Gi4voftxjp/pP+p1zDQ43VZ5/9Tz19+py+uXVGUvoDAPtP
Tsv9WxZ/86H/sRd2/Q1bAJMY/1SB8aedqP4n+BlIvbX3X8tnkB/jHzt+7f0N/VPXFjS7uNJz/fUPvLjX8xkUQ/9vi/kHW9TfDuu/
tqi/PfofO7R/W9TfHv2PLe6/7DD/b4/5N1th+3/SBDBJ7fBo1h7zY/7THtdfO1x/7dH/2xkeaqy6h8m6B9CmNdla6TyIls8gP8af
9o43RyIDmCTmH6oSFkATnHub/+JBJ6TSBdBI0vlLNzTZah9Cpf/JLmzuU1r/DKT1fXD7T073hP/4ZpZaXAdyYvxvh/F/f+D6a8/9
Lrg6h2H9q1zcf9li/7OdpPFnz7WX8WfpaP/9gfGPjaj1LzffEOyDpPWHXrD+VR7avw3GnwAsDA81Vr/51XjoeD7Ije/dtdeFJZ4+
1tT41O3u104c1N2FR5q585Drw5rjzZHV4Hg+aP6LB6Hj/uBrpHb9o8In7y60LyIbrf61v9GoG2CpexHG8Rv/RipsP+MAgC3qbyvN
AryP+peL+tvy6//R8/8pFsDqRwCoHa6/tjiAYYsNQPY4AGCH/sdW2usv459qpVmAdIvCztjeQepfEAvwttgAZI8DAPbYgGKD+Qdb
1N8O67+2itRfou8vA/2PHfofW9TfHv2PPQJA7TD/b4v1R3sEMNli/tMW1187XH/t0f/b4QG0thh/9g8CmOqVNoDGD5+RegNoCJ/J
Lm7uU+r+DILhPy+eOyXd+pLPoUTsf7DB+N+e3/YlpT4AT83LEay/Pwby9/2z/l4+7r9ssf/ZBuPP/kD7t8f4xxbrX7Zo/3YYf/an
sDVhiQftYPNIG0A5s9Teh+sCKN38g6TYEMSNFoBYpTRrW1J3CKVbb3R2v/DDrvpvttrX+maTboCl3pvgIA7AF5P1AEAQF+NiOIBh
K80CfNQCAPUvjvrbCqt/MISS+leLAFA7XH/7AxPQdtgAZI8DALbof2ykuf4GD8Ez/qlO1CSpuwcIe1CAxDxQUfQ/dtgA1B84AGCP
A2D1Yv7BFutfdlj/tUX97dH/2KH926L+9gggtkcAqD3m3+yw/miLB/DY4wG0drJcf8PGoNyDFcf11w4BfPZ4AK0dxp/23Nrv7OJK
19ej5n0c2n1+aQNoJHWFz0QhfCa9NHOfUu9nkOagMJ9BdgRw2GL8b+d4c2TVP8juDq+nOQDvUP/8jjdHVoPjHqm91uLvw/L7HR+1
L477L1v0//Vi/NlfaP924sY/EgHQdQi7/2L9qx60f3uMP/uHC5489vpoz/emZz/X06fPSWLuGRvf8FBj9cHXd/To4Buxr3Pj+jTh
h85GDUGs0vHmyGrc3LITDKF0/PpPHG5o6tpCz+dwd+GRJG3I2tf2ZtPeAEvrN8H+E9gk6fylG5psrbAJPacsBwAkRdafC3E+HMCw
leUJMBILAGWj/rbi6h8WhEj9y5cUABq3AEzdi8k6/glyk0B8DsWFPW3km1tnmICuCQtgdjgAZo/+p35Fr78SiwBlcwvBwQD6NPdp
fBbFpAngc6GIDvM/5WD80x/iAhA5/Fud4AagqAeQBHEPnB/z/7ZY/7LD+q+tLPV/+/FjSdHtX6IfyoP+x07Z7Z/PIBv6f3uMP+0R
ANofmP+3xfybHR7AY4sH0NrJev3lHqwaWa6/rAOUK2sAXxjuA4rhAbS2sow/g78DtP38gsGTUQ84dfzrL/Nv+WUNoHHhMy+eOyXd
+jI0iIbwmfQIAOofBHD0Bx5AW79g23eCIZSOfwDe/X64w/ISn0VWLnwy6gEYfti5JGpfEe6/bBFAVi/Gn/2H8U/90ox/nKjz7xKf
QRH+Z3DuyjzrXzWi/fcHxp/9YXioseoHT85++UXo65aeLOvp0+cY52DDcnMPD76+k/jajxqjnb22UnL4pEQAZZi4841Bbm4n2Ne7
4En39WAI5Uaue18GUL79+HHkE9jcDS+LwNlQf1scgLGVdQIuuPAYXACg7WdTdv0lboKzSFN/txnaF7Yxi/afT9oA0KgFYIfaZ5d3
/OO4ay9hoMWFfRbB8GEfE9Dl4wCeHQ6A2aL/qV+eAAKJDehVCW4AktohZEcv3IsNn3QIoSxH1AS16/ejDmhQ9+IIALUXFYArKXKT
rkT7z8vV2y1g3V14pNOf/in0tQSQlYf5f1usf9mi/rbS1j849xl38JTPID3av60q2j/X4PRo/7YIILaXNQCUB0BWg/l/e6w/2iIA
1EbSA2il6AAUal5M3gcARI1BGf/nk+X6u//kNCGgFUjb/4c9jJC132KyPoDWhfX5uP8qLmn9lzX4crnD7+NTt2P3mCTNwTEHlF2e
+c+k8BmJsVBaBAD1B78PChrbO0gAR03CAsiiMP9WjmD4TPB34NxbL2nmzsOeuZ6oz4azYNlEhU86ru93oQ9S9O8Ftc8v6/1X1Gup
fT5JAdBB9P/FMf7sL4x/6hcVvue4fig4/pHEGfiShH0GwRDKuAcAONQ+uzLaP/kbxTH+7A9++GRU8KSPEEpsZG7+4ezAoMZ3DIS+
ZmappRMLc9q350Cm8ElpYwchVul4c2Q1anzvrzn611bn4uSbna+7/y51h1Bu5Lo/a/0GgpIWwMZ3DEhL0uTiio43R1Y3YtH7GfW3
Fbf4Pr5jQOMaaE/6qLHKQKg6/oXAv3g0X9mnifZ/pe1XKGziR2rX/+Ir+9yFmM+gRCeWnwsdAPlo//kkLQC42k+oPenmgk/8ABTv
UBK1r0jU+MeNe45euOcmRfkMcoj6PRh9fkBa7n3aeHACmjFncVEHAHYfeq/rAIBbEJj/4kHnKQzUvri1Gq5OHG50wienri101d4d
AHBPQHIInyymaP+D6l1+2gq9B+b+txzBCVE3wZmnjXM9zsffgOLG/X74fFQfNaqB9iahIdp/UZ/M33vGXwxOdfhocUXD1L6w4AYs
9zsQF4BL+y8magO6X+/U88/M/1eC+X9brH/Zov520h4+9T8DlIv2bydz++caXDravy3G/9VIewDMn4f2Hz7oHwCQtCpxACAP1h/t
sf5ob3ZxRQrscfM3QzfX9lg1X9mni5NvEgBagqi+x9/749Z8pd4AFDdnSv2zy3L9vfy4lW4Myvg/s6zX37i9WNQ/P7cHxf09rP8P
C5+U1j8r1mCK8x9AO7u4ov0np7vGQGGBNW4dEsUkrf+yBl++LOGTUXNwzAFVL034JLCRxAXgumtq2MMWpN4ADvqd/MICyN45+1mn
xnEBNNwDFxe272duubX+INqYfaDBkG6kFxc+KXn3VYsrun/piPafnO65Hw57QBLyS3P/Nbt+5qvr9cguLgDaXQPo/7GZMf7pb5yB
r0ZUAOLpY812CKWi179CHgxA7SsSlX0ikb9RNsafNrKGT0rSjqHntfRkmfNfFQl7KK3Eg77K4J/53X9yWuMKD6CUpH17DnRyB9KG
TyKe/0BfX9hcWthDkBy3L2vicEPnrsxr/MCu8t9sjfoqgDK4+PjiuVPSrS97FsNYgKwGB5BscQCmf/gTof6E0P1LR5iAqEFw0zPq
cWL5Oc0tt7QwvC3yqTy0/2qcWH6uEzgZ9tR3Nzkx0f4StS9Z2sOPhFDmk3QIoLMA/7Tlh612TUAz8VkMB/D6g5tY9nEArFpF+h+H
BeBqZdqAzv1vZmFP43Hj+alrC7Eb5Hz+ZjlkExUAOrH296TPgANgxREAasdv/67t//HKu9p96L1U/Q/tv7iwQxh55v+5HygP8/+2
WP+yxfpvf3D1jqq/j/qXh/6nP9D+bTD+tEX/01+CBy8kDgAUwfqjvSLrj9S8HJ3PYFn66Pn/VFgAk0QAaJmyPIDWx+E7O3FzEMgu
y/VXCg+fdJgDLS5PAJ/DGkx+aR9AG/UwNmpfXNT6r5Tc9iU+g6xc+MBsSPBMGK69AMoWFYDbtZ+NAI7KhIXQvNzYKWk9gIwAmvLF
ha9Kgb1tawGIfiiW498jcA4svTwPoIo7A0bt8ws+fOHGvz+SpJ77LxeG5Z+9+MmPhpgHzSltALT7HPafnO6ch3S8dRnafUZzy612
/xLzfd/5Szfa82woDeOf/udqHTb+cWf0uP6Wyw+h9EXtgVh7HbWvgN/+g4IB9Oy/yi7t/D/jz2oMDzVWu+6t9r+R+Wfs/mCGef+S
uOBJFwjqm579vPN96l2emaX2WN+N793f87q78Kjwe9qsOv29FBpCGSVq/O+HULpsgo16PeibAMqwzc9fnb4Q+Xo2QZcrrP5xC8Bs
AKoOB2DssQBgK27yR2ISokoLw9s6T2PwfXPrDPWvkH8NlsKf+k4IZTWyHr4jhDKbPAvwV0+NhN58TbT/K3XPKM8BvLAnAGtt8Z76
5xP2Ocwtt7T70Htdk9D+ATAfY/7sivQ/Ek/Arhsb0MsXFj4ZXFCfuragE8vPZf65/C6kExcA6jZbvf34saTkIEr386h9NgSA2gnW
3rX93Yfek7Te9iXaf5n8jW9Rm9CdLPPPa4dX+QxKxPx//Vj/ssX6b/Vem/9cN5qvh34vOPcsUf860f/Yov3byt3+qX/pGH/2h7A1
eH99AOmx/miv6APAePhXccHPwA8+dA/g+eYv/9H5/u4Xftj5PaDu1XKfhY/Dd/Xq2YMVcQ/A/Vc2Wa6/lx+3Ut0L8BnkVzSAT2Id
rIhgCMrFyTe79jdHhU861D6/uPXfpLr7+AyySVp3THvtlXgISRWCATRJih5a3Wri1l+kfAFAJxbmNLnnQCnvb7ObXVxJd031Avji
zsBIzH9mERa+5PghTC4QXSKApkxJ11+pe/5zbO9gPW8MXS4/7b3/lXrPgCGfYD90d+GRZu487Dlf6kKALk6+GRrGhOzSBEC7hy/E
nb+eaH+J/j+lsb2Dury4olHFjycvP2115vsnF1c0nvB6xp/pMf6xE1f7oOB5O1/wIW0oz/iBXYnrXwSA5pOl/Uvh+RuSevIfgp8X
0psKPOgi7fiT9l7cV9O3dOjrpc7fb+3Zkfhv3OvTvBbpDA81Vv3gydkvv+j6/o6h5yVJS0+WNcw6SynuXzqyPq+5/iugyVZ7L+3V
UyOxY6AgFz45c+chfVMEt957MSKA0q+3/9/Dxv+bSa0BlEkLMFJ8+A+KyVr/uAVglIsDMNVL0/4dFgDKl3UBPojJn+q9/fix9Fih
k//BgCyUx/X/3515T48Ohj+RgRDKauQ9/Hj0wj0W6SsUdfPF5HN2eQ7gje0d5AnAJYv6HPy6+8IOQVL7ekQt/tL+q5FrAzqHj1IJ
Cz6Uwp9onSeEEsmiPgPX5/tt//ylG7FBlP6GLTZBpxcXAJpnMZ3apxfV/qM2G779+HHkhmnaf7nyzj9zD1wO5v+rx/qXLdZ/7b02
/3nX34OfB/WvDv2PLfofW7R/WwQQbwz+AVQfD0CtF+uP5SkrAJR1l/yiPgM/hPL+pSPa/cIPO9/zH8JGAGj1Tiw/p7nllhaGt0Vu
PKf/qR73Afa4Fyif68ODD9QMhlCiep/M33vmeHNk1QUOuLV4AkCrU/b6L8rHtbcaac+/pAk+lNrhM/v2HNDY3kF9Ml/GO9z8gusv
Xd+TOvWU2nNrJ27P1fPGNrk88w9S754s96BUd/6Ca0Y+41O3e7527q2XJFHTfsEDkOoXdhbJ558Bu3pqpO63t+GFBTG58LefHnu/
52FTkjrhP/49s9YeHsD8W3ppA6D9/aBx568n2l9mDjSDpPHn5T0Huq6/O29fr/5NoUvc+IcAvmq4ECUp/fiTzyC9LAGI7jobFvpM
BkT10oaP0f6zc+sv7nfBhZ+3Az+7X+vGn/NfPNDE4UbXOjz1LsY9PGds76Bee5TuYTpnBwY12VrhwTsl8cMng8GTQTuGnieEskRu
Hsef33F7ffzxz92FR5374zCET2bjrq3+OnvwQcvBYOKon+Fs5LrXGkApxdwA8xSFWlB/OxyAsRd3AG9uuRX59CmHBYBisizAo1xJ
/U9PABDhq7Xwwyel9qR/mhBK+p9skto/G577x9jewdANEO4JtEx+YqNJ2gTX2VD+tKX7l450DgfwBLz+4T+lSmIxIIu0G6C5B+5/
r81/rrm/ftX6bWwYceGTYfdc4zsGNK4BzSy1YoP4kF7UZyB519RrC9Jy8s8iADGbNO0/bL6Btl+uqCeQO1x7q8P8vz3Wv2xRfzvB
vue1+c/XP4+M9d95+7rUGE1+IbrQ/m2VVX/afz60f1sEENtJM/6PO4DKGnx9wh6+5s/9swZTPda+ypO09uiHUPr7SggArd/C8Lae
vQ/3Lx2h/+lTzP9jI4gK33MP1HT9P6rnDqJK6gr/DO53Q3nKXP8FNqI0ATSTrRVpST0hlITR5De2d1D79hyIXXuP+myizgJI6Q7O
I5vgA2DC9mRx/iIbP4AmbA/K3HJLpz/9U9e8WzuUI3wOjvvfbJLC33yjzw/o8uPehyD5D0BCPmkfAha3DsPDf/OJC8FyIRvvnP1M
f/y3f+18/ad/819D56DdPbPof1JJGwCd5fw1IZTZvffXr7b3LgfMLbd05s83Q/9N1PiTsWd6wb4nLoA7bvxDAF91Zu487Kp3WAAi
quEHgBKAWL+wANb5Lx7wQKoSRYWfv9zYqbsLjzr9fVgonEQAepl++/SxpOf0xyvvSkp/XZ08Od35t8gvS/ikQwhl+dxcTlTWgBsD
BUMo/esF4ZPprNVoVVLPOnvUw66D0o6NNopaAyijbn7z4ABAdtTfHgdg7ATbf9cBPElv7znAAkBFsizAX5x8U++c/Sx0MxaLX8VE
9T/71tr+d2feSxV+yOeQXdIBpEcH39DO29f1g+tX9IMjhyL7IPqf/ELbP9fevjG33F7Uml1cCd0AsfvQe/Q9NQg7gCexASivPE9g
ZoObnagA3PuX2v/p2j9Pa84mbgM0IQR2gu18ViuS1Llfi/3ckEtU+J7vxMKc1BgliK+gqMNHbjzjt/9g20c1ktp/XAglAbi2uAfO
h/l/O6x/2aL+tuaWW131D85Fn790o+fQqcPh0+LSPHwhLdp/dkn9T1z7l/gdKIr2byt2/wPjz1rEBYCmOYDKAwir5dYfw3D4qz5R
648SB4+q4kIofQSA1uvtx4+lx+ra++CCHyT2XRWRtP8qru8HNrOjF9pjm9m1/2S9sTrBtUg//PP+pSOEUFYgaf1X6t7Tc2KZA6ZV
SPsQ2iTMP2STdP7CD6BxfdCJ23M9r3NnAwifySe4BuN/3e1ncP3U/pPT+qgxGjknzWdQvixzcJy/yC7qAaj+A33jDln7c3DMRVQj
6neA81/FzC239JrC1wDCav7iuVPSrS9j98ZNLq5U/bY3hbDwn2AInAuA2/3CD7u+3nsG4EjZbw/KHsDKGlg2MxMH221+WV1jUDfv
uW/Pga62/c7Zz7RvzwHd2rMj8mdOtlY0tndQn8xX9rY3naQAbgL4sBXN3HkoiTN1VsICWC8SQFm7pFA4AtCL+fbJwjPDQ43Vsb2D
+umx9yWpJ/gzuA7j5nna54LbP6PO97yZDA81VruyHfZHP2Anyu4PZgihrIHLYpLWQyhd+KS7XtP/pOfVatX/ep7wyalrCxu+9rUF
UI7tHdTlxZWem18fB2Cq4+o/qnwHMKh/MWkC+DgAU52w9p+0+Z8FgPKlWYCXogPIWPzKJ67/cW3/uzPvSUrX7pn8zye4+LjPC72V
1jb43L4uvXFMO8/EP/0U2RQ5AM+1t7i0mw+jnoLHBgh7HMKrT9jkMwGg+blNtmkOITH+LFea+98s2ICeXdQT7fwgON/5Szf09uPH
evD1nZ7fmbnlli4/bencWy91JqKRXprwSTfmjAqhPPPnm7pMaGshLnwyrK9/+/FjSQRRViFN+5e6QygffH2nrre3qUXdhzH/XB3m
/22x/mWL9V9bfv2l9c/A3e/+4tkBTbZWNK6B0FoH56E5/Jhd1NqXQ/uvTpb27wvWnQPY+dH+7STtf5Cof9XiAkD3pXz4qcQB+Lyy
rD+OibpaWRjeFvvwO4nDd1U5sfyc5pZbkZ+BRO3zSup//D2I0vp1YHzHgMY1oJmlFuuPBcU9SO01KdN6yomFOU2y/pJamuuvux9L
mgtFNnEBfLsPvRe5/sXaV7nCPgc/+HDC4k1tYf5+tuBDCJPaPg/ByyfuIQxR/T7zD+Vw19ekAJr7l46kCp+5emqEwIiUkgKALj9t
dY3tx/YOts8XLbX/7n4v/Lnn9c9gkHuxBFnCb5Pm4JyJww2J++BUosInHRdCGZzXJACuPFnmIDj/VZ7O+kug9p01gLV5BL/mX52+
EPqzdt6+zrmwAlzwpN8XuQA4Sbp6aqTzQIaoMwBSux+aaH+Z/r+gvOevWQPLxh+D+i4/bUXW0Y03w8afyCZNALe4n6qVC1Ry/KCf
qDMzqEYwABHFhYVv+4LtH+VL+gxcuNs7Zz9zcwqh/D0QyG9s72BXnd85+1lnXiEYRNnzmVxbIHC7oK+mb+nQ10udv8fNMzvu9Wle
i15RY5ngeMfXfGVfVwilM3Pn4YYPP7Q2cbiR+Hm472/G8EmppgBKd/E9LUUuwLgDAFpaO3Ad4E+4uRtgnr6QXdQCZJb6S+3PgPpn
l1T/LAdgqH92cQvwEgsAVUq7AB8VTkAAWXFxh8AeHXxDO29f13dvHEsVgLhZBkF1iQtA9Nu5+xyk5L6G+qeTJoAgKOrai/ziDgBI
0tsJB/HYAFFM0gYUfyyE/sPkcz6u/z+j7j7I/13wx6GMP6sRF0AvsQG9KmvjxNXgE+3iguDGdwzoxO25nuAsrhH5hC0ARG228tu7
P+5MGj8hm7i5BnfoN+ogHgGg+QRrvvP2df3g+pXEzYZlBhhvdcEx0Ifbt+vtx48JYKoY8/+2WP+qH+u/tnrqL3VtQL/8dL0vn1lq
6YTi5zqpf3ZpAxDpf8qXuf0H6h/1u0D906P994c048+0AcTUP724ANCsh+8kHoCaV9L8mR8ow8H3cqUOIHt+W+j3WPuqBwGg1Ynq
f6ICiN21+NHBN1h/LMA9AOYXzw5Erj+e+fNNSe01yLAxKIqLCx/z1xXdvUBSCCUhoMX44ZNhex2SQihZA0svKgRU6g6hRL3cON8P
mwl7ACFr78WF7YF2dX2g9jjoxO308z8EICZLmv+UugNo/MOOhM8U54cPpAkA8uvvh2Fp/bx2e3yk9pxE8HAqosWNP4MPACAAqzyz
i8mBzlIgiEm9D8cOBsAhvbnlll5T9O9AUvikO4sUbPvM/6QX3P+cNhBXYg90GeIC4EY1oLnllo5euBf6IBip92EwnEHKJmkNIM35
a2QTDL/qjEE95956STN3HnaNJScON6RrC+trjPHjT9YBEqQN4L68uNIJvpJYhywqKfxNagcqTRxudJ3RmFB7Pi54ZgbZFAlAJAC0
HjN3HnbWfAlgteXPZwbXC/w9EKzB53O8ObIaDPmcONzQO2c/08XJN7sewhMWCMpDR4pz88hjewf12qN088pnBwY12VphDjoHd/53
Qurqz11fP3VtodPOw74fDKGk7ZfP1doPnQy7/m6m3KVaAih9SQswk4srsQdg/MMvLD6mk2UBMqn+EouQWaWtv5TuAAz1z6dr4m05
/rVhWAAoLqn/jwtE2Xn7usYPvkEAWU5hAaDBRXfX18QFIHL4JbusAYhZQiiRXvAAXjD4Kk3oJNfffOICWKXeDRBRG4DY/JNP2AaU
qAC+MQ32LHxJLH5hYwtufvB/F15T9EEwhwDc/JIC6KX2vE7SBvTeOSCe/p5H3L2WtH4P8ODrOz3hb5eftjQzcZCn56XkLwAEN7hJ
3ZutwsIngyF8hIAWl9T+pbUwlMao3n78WA++vlPn29v0XPikJH33xjE9yrDhkPafnz8Gem3+8/Ux0J4DmeafWYNJh/l/W6x/9Q/W
f23NTByUpK4N6G7z+eziSntjeWM0MviB+meXNgCR/qd6ce3/4uSb2n9ymvqXjPZvK/P4U9S/KmEBoE7aw3esB+eTtP742vznnd+D
2cUVDr5XIEsAKOpHAGh1ovqfpOAHH+uP2aV5AIbUXltxD8BmDFQuFwDqryF2zT1rff3dXV/3n5wOXQtGOZLWv/wQSta+iokKnwwN
db62oLlvox8U7yMAtJhgwJX7PQg+gNC1/+B+OTdvzUMYkkXt/3E19dd0ufZWI2z+U2pfn4MBHGPpw2eQQVIAUDAAxR8POcxBZBe8
/wqOP7V2HXXXAAKwbCVdl7kHTq9z/ihk//Nr85+H7nv2z18EzyJxBiy7NPufw0Q9jBzZJAXASe11sDRzcZxByi8uBDqtnbevS43R
st7SluPuA6R2AJwL4JO6A1AkMf40Mru4QgB3jZqv7Ou6n22+sk9K2N9GCFw5wgIQJw43EgNAqX95ggFYEyKA1YK7DrO3tnpf/vsT
/eRHQ5LWr7f+dXV2cUWzF+515hn81yO/3z59LOk5/fHKu5LS7y2ZPDnd+bfIxj+D6pu6thD6wFmpO4ySfqk87rPwr63BoMmw4OfN
FD4pGQRQSuELMGN7BzW7lvy/b88BnR0Y7DkE4x9+YfErn7gFyKT6SxxAKiqu/mkOwFD/7IJPIJR66x+HBYBi0jyBx/U/UQFk/gKY
C6Fk8j+dNE/gDC62EIBYHlf/2anboQeQXPhhUNRnwAasbNIcwJtsrUhLStx47r+e6296bgNEcPHdCTuEEbcBiA0Q2cRtQOn8d3Uf
wgiGZLnFLxa+8plbbunMn2/GLrgTrFStqCfQus3kBOCWL8sT4CcON2LnHxzmgPJxG5yDh4/C7rWcRwff0NmBQb39+LF+8Wy6AHX0
cpPO7u9hD1jwRY1D/aBot3EdyfzN/WnDV6X1EMrgAUqu1cXlmWeg/Rfjj4H8sagLGk5zD8z1Nx/m/22x/mWP9V97wQ3okrSt+a6+
n3+/MxdK/csXFYAotTfh0v/UI6z9u7nNpP5Hov55JQXg0v6rlTT+IYC4OjwA1U7S+uPccqsTfpjm4DtrYNklHTR1AaBjYk2lCq/N
f87aoxG//5F6H4AqhQc/oFxJ64/zXzxIHIM6jIGyi5p7dnsjwiTNhUrtNebNdDCjamkevib1PvjO5/dd1D+fqIN3l5+2QseqSQHe
SC/qd8DdZ/lBS6z9liNNCBP7f6oXFkBz9MK9rvvai5Nv6p2zn3XWJR3/NQRA5BNW/9nFFfUcSPXGlsw55OP2H45P3daoevd+Stn7
cwKw8kmag5DShcCxBzefqP3PTthDkDj/WEya/c9S7zmwuLpzBqxazMWVb265JUUE4CrFQxRY/6pWcPzP+LM8s4sr+nD79sTxz+jz
A9JyugdjEMBdnNv7I4l1XWPBAETmdqrnt/+k/j8M8z/l8D8H1hOrN3VtQROHG50wSf9BL9L6WbH7l47onbOfdb7+kx8NbboQuLp9
+2ThmeGhxurY3kH99Nj7khQ6x+z/3c3xtPcptn9Gne95swieQZXWg1el3jG+/xk4zLeVw6+7s9XGnyYBlNL6Aoy78M7ceahtzXe1
/+T7653PUu+/cwuPKCZsASys/v6EKAeQyhNW/7QHYKh/ccH6n/70TywA1Cis/lEBZGGfAwFk+YUdAA4TDIdwX0M+YQeQfvHsgCZb
KxpX+GarqICOydYKN2E5xB2AnFyMP3wn0e8XkWbzYdqFXjYA5RMXwOcOAERtzHXXXBZqsnMHkM4ofhP5a1oPAfUnPlFcXP8Ttukt
LACXJwAXFxVAMzd0SrMXkucfkI+bfJ69cC/TvZbk3W+12u3dv39Dep/M33tmeKixGvx61k2el5+2NDNxsGvhEtH8p3/5T5aKe9q7
lBwCivT8AFBflhBKP3yS9p+du/aOhsw33Gi+rg+3b08VwIRimP+3xfqXLdZ/+0Pw+hkMoQyi/uUI63/mhk7R/9TMb/+u/5EU2/4l
Uf+CogJwaf/1iBr/EEBcPh6A2h+S1h/D1gCC+x78NTAOf2UTXHsMfs8FgEq9G58Zc5YjzdojAaDVCNv/4/c5TnAtJtjnE75RTNwD
MFwAEGuQ5el5AHDE9XffngO6emqkM668empE+/Yc0K09OyJ/NiGg2QX39+y8fV0/uH4lMmjD9TdvP37cE0LJQ8Cq0dkvNN8byhoW
nEUAaLIsDyD0RbX/7jVI6p9WXAi0G+f78//u+su1t3xh859h91rcf1Uvqv5R+yaQnbteRu0/j0MAVj7HmyOrs94+WTcHkRRESehb
uYLX3ai5OB9zz+WLmn+YXGyvu5xYmOt8Pazm/jrM2N5BfTJf7fvdDFwAXJy3Hz+OnIsLwxmA9KIeAOZfA4Lnr6Xeay59ULmi9j84
7qE8jD/LkzT+IYC7Xm7v1bamuP+qWZoAROpfraT2j3rM3Hmoi5Nvdv7O+d/yHW+OrP7xyruS1Ak/lNoBiC80RzoPBGu+sq/T77gH
8aA8Y3sHNXG40fn7O2c/6577X+POwfuv1bUF7nkLcGdQj0y1i3hE0qcXP5TU3f/vPzkt9xp5r5md775HQHZ+/aXw+rf/Pl3zO6uX
WQClb+bOQ90/9LE0P9d7CCCAwVG5wg4gxR3C4ABSufIcgKH+5XH1ZwHARrD/CU64sQBWDf8gTNjEv+Nq7gdEfETwW25RB5Bmllqx
n4EL5mATVjmiDkBOzr8fe/hOWt/0jHTSPgEyDTYB5Zd0AG/f2lMI4xa/OIBXzHt//WrsITwXAsrh3vJk6X+iFnz9ficpJAvJwg7A
S+nmHyTmgfLyAxDz3msRPlmcf8+Vpu7++NMdfEE2YQGszlenL2jn7evaeWb9a2EBrG8/fqxfPNv+3Dh8l56r/cWIjST+PEPSwy5o
/8WFHcRwX3cPxUgKYEJxzP/bYv3LHuu/1bu78EgvN3b2fE1ar3/nu81RvTq6X5MTzZ6fQ/3LRf9Tj9Ttf63tS6L914D2b4sAYhv+
/WvUGjwPQC1Hmvn/NIe+HA5/ZecfQJXW5x388IfLT9v/fXZxpWt+7vylG52NuPQ9+aVde5Q4dFemNAHEhG3UK+kBJFL3nlAfIfT5
xV1/x/YO9vY5F+51xjoEkRUT7NP9h61998YxPYoJ2/Dx8LV8slxTL06+2RnzRAUV8DmkF7X+GPYAwjjUvBxRIUz+gbvO/L93/WX9
sXxR6y8SATRVi5v/lKQjU/Oa+v1BRe2bQHphDwBw3NxD1nk4pDe33JLWxjKvzX/e9TAMN8YJC4ELXpt5CHx+cb8DcWj35Qp7AOeu
Y1c1eeWoTih5HygPXsjntfnPCb6tWZoHkPh7Dv3z11L8GWwUF7X/wWH8WZ4bgfFPXF8UdxaJ63Fx/r3XzuaoHoXc/3L/Vb24AMTZ
xRXp2gL1r1hU+2f+B5uFHz75l/l7nWBJF27owicd1+bfOftZVzDo2prvqtRZV0AGx5sjq12BkpImDjc6dXb9f2j45NprJfHAr5z8
8MObc/clhff/ca8Znn9/9dsnC9Q/h7T1lxQaALqZal9bAGXcAQBJ+pd//LGkH6/97X9Lkn76N/9VE4cboYMfNv5kk+cA0tLvD/ZM
7ruLA/XPhgMwttLUf9v8nCbn32cBoAJJ9U/ChFs1zr31kk5/+ieNK/5peH4IotRu/5tlEGQhuAH69Kd/Cg0+dPzwSWpfnuAktJqj
mrxyNDZ8wwXvTV1bYAIih7DNh0nYBJRf2gN4Unf4ZNLGHw7gZeNqPxpyrfVDQDtj/GsLPU/AYPxfXNb+h76nOj3XXynV/APKk/cp
s8HN00jn2ycLz0yqsTqugUx9ixt/Er6XX1QAa9Y+3oUg8juQT9RDL9w8g6TQhy4QPllc0iZ0dy9AAFx5mP+3xfqXLdZ/7bTnKEdW
JXU+A7/t//Hf/jX03y39fpD6l4T+xw7t3x7t3xYBxP3p7sKjzhq8W/9NmovgAajFxM3/BwNpvqvzjW1SPQdQpa55BzffIKkrfMB9
FuM7BjSuAc0stbT/5DR9UA5pAkD37Tmgsb3tMc/RC/ekC90HMqh7eaKCKLNi/0kxSQFAnRBKD78HxUSFj82GBMl01T8iiIx7gWRR
AXxh6y1x3PXCXbNZA0sn6QFswX0+bpyzb88Bfbh9e+TP5SF42e0/OR36AMI4nbArb02MdchiokKY/ACU4BwQ1958ktZfpN79Vw4B
HMXlmX/zEQJRjqj7rrG9g7p/6GNNXjmq4L4siQfAFOXvOx99fqAreKkrjHLPAUnde7P8a3OWsSq6uT4o6ncguCcr+Dvgo/1nk9T/
d9Yg//E/tPuFH+rswGDP/jh/3p/73vzCgm/z2Hn7utQYLeMtbRlJ548mWyux568lzmDnkW7/Vbif/p7xZxHHmyOrs4srmltuddZd
/CBK/+9JAdz++Gf84BsEcBfUefiCou9/Jdp/FdIGgC79Pn6erfnKPk20/yuhZAH+2d8g5n/6T3BMT79TPj9oshNCqfXASX8tZmzv
YFf4pNZed/GVfZ0gSvqc/L789yf6yY+GJLXDhoP7e2YXVzR74V4nc8N/PbJz4Yfnf/lX7S/80h/3d5+/6Ah5zX/5b5srCLEuueq/
5vwv/3fn+7tf+OGmqH0tAZR5DwD88d/+tX0ISeq6CLuLNAFA6eStv375r6GHwKh/NhyAsZW+/j/WWufOAkCJ0tR/9ws/7Pl3cQtg
yCZpAnpmqRUZfugEwyBQnPsMOhtt1zbZ+p+FX/PJ1goJ9DmkXgCWOovAQX7wpMTm/yKCmw9Pf/qn2A0QbAAqT9QBPD98Uorf+MPT
Z/PzFyLd36Xug3huEtRfjDx/6Ubn62zELSY0ADogbzAfemW6/joR8w8O91/ZufA9J2+4qv/ZMQ7Kxn0GM0stjQeC/cP4Yx0OvZQr
Tx9PCGIx9y8daY9jIh64EDwUqcaoJlsr1LxEcQfgv/nLf3T+O9ff4pj/t8X6ly3Wf+35n4ET2/aVrv5hoRHoRv9jj/Zvh/Zvi/Gn
vaT5z13HrnYefMcDUKvnrz+e/vRPkYE0O8+E/3vWv/IJm3dwAazf/Gpc3515L7Ltu5rvPzndWYtHelEPHnHrji4EbvbCvZ7fh+Da
I/1/eaIexhOFvQ/Z5Q0AWvr9QdbaKxBcf5+587Dn8KnU7pOunhpR85V9XQfD+EzKkyWE0g+eRDnCAhH9663bHxQWGo38/JCrLGj7
+eTZA/TT36vT/wcxBk0n9/zbmrgAGj6DZEXr35kHlXo+A+qfTrDv8YOz/c9g95X2/RVzcOULhlA6N5qva265pTN/vhn5b9mLW0yw
D3IPPupq+y/8MNVDkHgAUjZZ+/9v/vIfnc8iiLOn2bkAOEmRwbfu60lzcZxJLS7qASR+PxR3/lri9yCLouPPqH0QEuPPtFybH1V3
m77RfD11AHfesxpbWVwAnxMXviqpc/9FCF92SfXvzd+QggFMBOBWp+j8D8rn6nzxlX165+xn9DslON5sj3/++fJ0aDueurbQGd+4
tcV3zn7WEz75QnOkK8AS2Rxvjqz+8cq7+umx9zVxuNEJk5y6ttC1puv6m/uXjuids591vv6THw2x7zMnF35YFnJosimz/pul9rUE
UErRBwDuH/pYP/6f/xL9Dw99rKlrP3cJ5x1T1xY0N3RKw0Mb/0OoQ54DGFL35IOP+mdT1QEYLsTpZKk/CwDlS1N/f/I/abKNTbjp
JU1A++09bvHFX3jcLAOguqTdfNUJPgz0Pe7Jyy4cggT69PIswARDOKT14Mk//tu/6r/8t/+XsU9Jgn3QiYW5zvfi+n42QOQXFcAX
timXha9i/EWYuCdAbmu+K0naf/L9zmE8vXem85mM7xjQuAY0s9TqPClmov3PeQpPTn4IN+PPahTZAME9cHncBOj0RLPT1h+lCECU
utu7/9kRwJGN/wSkzj1Xyqf9Bg++BJ9giGQu/LNI++cAUn7+wmKaEMqPYsInaf/ZhM1BRB3EcLj+loP5f1usf9li/ddee6z+sPP3
xNpLifWX3g/5Rwii/7FH+7dD+7dFAKud1POf7sF3jdHQe+LgwXeUK28gDbLz53PGp26vr3cpPgTLhVAevXBvbe2X+98kwfVHqTsA
1M0BBYNY/d+H4NqjC96g/umEzb1J6+Gr44GDqW79Mer3gL0P6RVZf+TwXbX8OfydzdGu8E9n6vcHddE7GBbUfGUf+yAKShtCGbYO
s96vjVD/BMG+xA+fjLreur2fYaHR/voNkqXdt88+t3LxECpbeeffJD6DMhSpvxT+GVD/dLL0PZ196I1RSb17U/w5OM6Bpefuf6P2
P0vSvrXwpaA0+8+PNxl7JgmufwXX391DkE7cjj5/ETx7wfx/Oln3P3QeSBXg9zmsv2Qzt9zqCb6V1oMoH6jdB0XNxTnud8LdmzEP
lywsANp9XWr/LjhJ568lHkCSVe79V463D4LxZ3aunQf7IKm7H4qSNAZi/IPNyt37EsRng/oXkxTC6s/fs85YveAazMXJN/XO2c86
IZRSe0wTDJ+U1BU+ybpjfq7m/t/9cM/mK/s6n1PwtROHGxI1z+3m3H39eC75dahGWfXfDBlMtQVQSuEHANK4v3bz62tv/kcWuQ5g
SJ3JBx/1z66KAzAcwEgvS/1ZAChfXP079SaArBJJE9B+/aXuhffgk6d2HbuqR/Nzm2IAVIesGyAkL4gy8HUf9U+v0AJMYJzqXk/9
04sLYHXcwiNPn61P0uZlwifLF/kEyH/+39r9wg+7DuN9d+Y9abq77u4QnjsIhmRJAdCdvud298wQ489yFL3+Rt0Dc/+VnT/WdyF8
cYLt3W0WIoAjm+ATkIIbreLuuc699VLXz/L7LhZi0vHrPznR7Gw0TDuuCQYhcvArm9nFFSnwpMGoEMqZpZa0Fj45tnew5/pN+88m
bA5C6q5j5LWY628pmP+3xfqXLdZ/7e34u9u6OXc/07+h/uWg/7FH+7dD+7dFAKudtAEEcYfvpO7wSe6/0kuz/hiUFAKH4vzPwIVg
/eD6Ff3gyCF9d+Y9al+RsAcQPvj6TtcD78IEA0CRLGnuTWrPd8Y9/Nd/nUPfn14ZAejBw2GEz6SX9gHMYQgBLZ//sE0nKoSSh22W
Y22danVC7b4kKnzSN75jQCduz2nfngOd0EmJh+Dl4eof95pg2AzKE5x/kIo/hIoxUHq559+k2M+A9fd0CtVfCv0MqH86WfYfdp39
igjBInwyveD9b9j+Z2l97tONTaOC3xzGpdnt+Lvbmvl9e+wYtv6+69hV7dtzQA++vpMYPsn8fzZZ9z/sOna189/33/q5Jg43us6e
Uv/0/ODbqAC4zmuXWl1nUCX6niLy7D2MO3+NfPLuv/Jfz/gzO9f+3cOmwvqgueWW5v761dB/zxm8aqW5B9uf+ArkRf1tUX97M3ce
am7olPaffD/TGIcQxPROH2vq3JX5zn1UVAglqnG8ObL6xyvvdv7uar4WKNkV7il1B51PHG50hYJOtF9Cmwc2sFoDKKV8BwCkkJvl
eSJc86D+tjgAYytL/d0CgJv8l8QCQEFx9e9MOjdGdWJhLlX4DxtQ0kuagI5beHdPnvIXxZBenifg+TJtVEGoogswyCcpgDUYRLxv
zwGdHRiMffoswXvZJB0ACMPCV3XingAptev94rlT0q0vRcxVMWn7n7jNVw4BuPkVuf5G3wNz/5VHMIQyit/edx27Knfn9oj5n9z8
JyClveeaudXd9qV238X9b3Zu/iHPod+e7xGAmMmOv7utqd8f7Gxiu3pqREcv3Ivc6N/pc2j/hYUdAJPWx0BxuP6Wg/l/W6x/2aL+
GxP1Lwftf2Oi/uWg/dti/GknbQBB1OE7SV3hk9x/pZM0/y+FBzLF4QBqNlHrj6c//VMnhElqr3s9kkKDsBwXgjjJ3E8p3GfwndoP
vNt5pv31pDVf5j3TC9v/I7X7nzxrMdua7YMcPAA1vaIB6BPqPhQjcQA7jSwPYA7jQkAvEkBZirgHfwVDKD9qjErqffga8nEhiLMX
7iWGT/r7r84ODEZ+BuvjqhEO5MUYHmqs7vi729JEs7TxPg8hzMYPwJLKeAgV979Z5J1/k8I/A9bfsylSf6n3M6D+6WXZf+jOX0SF
YDH+zyZ4/3vurZd69p24PbiTV452PQg+bh6CfbjZpQk+dGcwgrrDJ5FVkfUvv9+n/tnFhVDOLbfH9794dkCTrRWdUHS/wxmA7OLm
P6P6o13HrnbOXoc9fIQA6OwYf9oIC6EMcg8Y8ecm4s7gsQaZXjDwnLnMjYeHUOVH+98YtjXf1f6T63OaY3sHafcl8kMog1wgokPd
y3O82R77//Pl6dDgzwmtr63vPznd+b6/382FT0oErwKbQe0BlACy4wCGHQ5g1McPoYwLIOMJbPkkTUBHLbwTPFkcAYj2ii7AIJ+4
ANYg/0BGkB8+yROw00kTwKcrR1MvfEksfmWVFAB6/9DH2v3CD7sO4333xjHpjWPaeab3M3CH8I5euKexvb0bhdAtbf9DAG61im6A
dghALC7p4GMwfBLVSHPPdf/Qxz0hfNz/5pfn0K+/aM/Bo/yC82ljewdDwwRo/+ULHgCTsh0Cc7j+1ov5fwAAANSJ8Wc50s5/Bufb
9q/d+7rDjuw/ySZu/n+X2nNv40ofSCOtPyAG8eLWH51gCFMwCCvqMPDwUIMAvhTC1h/d1x1XY/fgO3lrwP73OwGgovZZhD0Axl1X
g3sexr327q+1u7UY5t/yKRoAMeF9jf0n6WV9AHPQfkUfCCOIID1Xw7QhlCcW5rRvzwGN7R1MdQ1BvOGhxurs4kpP+KS75n535r3O
a3nobzXctTbPeD9sDZiHEGaTd98z64/23GewXn/W3+t2/9DH1D+nrON/Nw/ngrCk7vB5xv/pZTn/8lFjVCcW5hJD4FCNqIcgdR4I
zPW3dl2/L9Q/E3fv6odQBrkAuLRnAPwgYiSLm/+M4s+7+XM/BEDbYfyZj2v/Y3sHdTlmv7Obm0g6gyetn4XndyDa+NRtfbh9e+fv
c8stjU/d1rm3Xsr0c9zcqR+QJYmzYCkUDUB01wEeQpVdWe3f8dv//UtHCr03rNvZbD/sS81RvTq6v/P1qd8fpN0XcLw5snr6WLPz
904IpdSznuiHHL5z9jPqXoNgCKXrU/wxvvtcXmiO6C/z9yQRQglsdARQAkACDmDUJymAjCewVY/AmWoQgIitKusTaMM2QPjhkwTQ
pJcUwOdfc08sxD99NhgE/cl8le9840sVAOpxm9LTHsJDOmn7HwJwsVXEtXWJ8Mk6JdWZAxjl6jn06202DB76dQfwfDN3HtL/59QT
/Jzx39D+8+PBFwAAAADQv9h/UlzS/P/MUiv2YST+65BN1PpjnOD6l/sasglbf5Taa5CnP/1T10PvJOmr0xfa/2V6vdY7b1/vOhCp
RvuwDAGg2cTt/+na8xBYj3Fht6zF2Ak+OIn9J9kUeQAzQQTFzS6uSNcWug56RYVQugCgfXsOrIfOrIWgB68hEiF8aQwPNVaPTM1r
eqJ9GNIP3XYPm5XCxzgu9Hl86nbmw9sIl2e8H7YGTLsHgM0rOPaXGP/nkeb8S+c+eG2OIW5f1tVTI4z9K8JcAzaD4PxnJ4QywG/v
SWcACF7KJ8/5x7CHv0icv8DG49p/0n7nmaWWxtfWv+LO4Eli7BNjdnGlK3xPkkafH5CWpdOf/kljewdT/RzXB81euNe1Xnb+0g0d
vXAv9c/ZisoOQER6ZbV/aT140rX/85dudL5G+0/PH3v6c/n/8o8/Dn39T39f+VtCToQgppcU/OlCKH1++KSkTvgkgI2PAEoAQF/h
CWwAsLlkWYD0F4T3r21+nrq2IEkEEOeQdADA3/gT9fTZYPgkC8DpJAWARiGEslxp+x8CcLFVRLV19z1gs0p76Nc/gOfQ/wMAAAAA
APSfqPl//8BpXCiNv/61rfmuvp9n/iet0PXHK0d1/tKNyJq79S5/DeyjtWACpBe2/ujzw7DC+OuOXUGUKJVbbwmux7AO0x/cej0P
QMqnyAOY44IIOPyVzo6/u62p3x/s1PDqqREdvXAvNGjDhU869w993LMGJhHCl5d/HS2yrycYiohkecb7u45d1Uyg/bP/DQA2Px6A
Wp80+7IInwSQRnD+89xbLyWev4jaF+3CJ93DL1A9AqCxVXSF3zZGYwO4EW14qLEaDN9zXAjf5cWVxDBQZ3ZxpRO+59bL3INhJpkH
ClVmAKLPBR867lwe1pXZ/v22L7Xb//iOAY1rQDNLLdp/AvewR0md3wcXxCoR4Fk3F4Z4MRCEGBzTz3/xoCcsEcWF1dWFUAa/BmBz
IoASANB32HQLAOhZKGYDUC5JBwD8EMrgxtxg+CQLwNkkBYBG8UMow7ABqxrB8ef+Wz8nABebEvda2KrSHvplAzoAANiMHs3PaWdz
tPOfUa8BAADYDLoOfkka90KBgge/tjXfrfvtbQrB9UdX83FFhwBJ62tgLqiJANDsguuPefEQvOqxHgP0CgsiYP9DNsEaju0dDD1A
GtYHhYVQUv/8il5LXfgkIaDZ9Yz3dwx0Po/geN/9LvQGEDP+BACgTFH7slxYx9S1BQKgAaSS5/yF64P23/q5Jg43OqEpLqiGANz6
sP8WW0WaAG7Wv5K9Nv959PckXd5zIPPPDD6srRNCqcbqt08WuBasKTsA1Nl/crorDPH8pRs6euEeIX4hym7/SQ8qRK9P5u89M7vY
+7sw+vyARjWgueWWLi+u6Mf/819C//1+959e6Coh6MXNLq6EBtm6Mf6E2uP7YEglsjneHFk9fawpaT34c+JwIzKE0gmGUQLYXGoP
oPz04oepD7ZwAKZ+HEACAAAAtpbgxlxfd/gkskoKAD1/6UZP8KfPHcLzN0ijHl0bVrgHrgTzD7aoP7YqDv0CwNbF+KdarP/aSlN/
/z+Dr6X22Mjof/ob119b1B9bWZqDX7uOXeV3oGQzS63YdS9JrHuVoGf98crRxDXHID4DAFbuH/q4c/3lAHY+wfCNLIeAqX9x5y/d
0Ph0+vBJ/5rrQic73yN8Mre0433Ug/kHW9TfFvUHuvU8CFgEQFeF/qdarD/aSjp/EcU9tGHC+xoBuOWj/6kW/c/GERXAzfpjdaL6
n4dXjurB13f0naSdZ3r/3Ym1P/v2HCCE0lN2AKIfPunCEDsBoFyLCwtr/w+vHO0K/AwigLVaLijRfQbnL93oBCdePTVCCHoO41O3
dWRqvvP3Ty9+KEk6euF96cK9ztcJtS2fC6GcXVzpqrXUHQCK+nH/VS3uv7pts/gfDStgka8hPXehDRN2ACnqNcgnqf7+n7jXIR/q
39/i+p7ga5Ad7d8W9bdF/fsb/b8tV9ttzXc12Vrp+bPr2FXCJyuy69jVzqbnoEcH3+j6T0mRr0V+9D/VYv6h/1F/O/Q/tqi/Lepv
i/pXi/kHW4w/7bH+aytNXV2wgP/1sNewQSsb+n979D92uP7aov79jfsve7uOXe2sxQTXvgijKZ+rdVKwofv+ZGtF25rv1vHWNr24
Ncc4fAbVoP+3Rf1tUX9sdkWuubuOXdXMnYddfzh8Wgzj/fow/2CL+tui/rZYf+lvjP+rRf9jj/XH/hXX9tshlAudP5yDyY7+xx79
T/8Ka/tuHsL94TNI70bz9cg/7/31q12vTdP/oFpxtZ9dXOkJn3TGdwzo7MCghocaq9W/y42jrPb/3Zn39N2Z97Tz9vXQPycW+F2J
MjzUWP1w+/bI748+P6BfPDugh4GgYWk9/NNv9+M7BnRrzw6dHRjU0UCAH7odb46snj7W7PqaHz55c+6+bs7d187mqHY2R7Xr2FUd
mZrv/JGk+S8exP5vNF/Zp4nDDR1vjtD3pDS7uNJV523Nd7Wt+a6OXrin/SenOwGr1L5c3H/Z4/5rXa0BlN8+WXgm7cGWtK8jcTu7
Mg8gUf/s6IBsUX87DIDs0f5tUX9b1N8O/X//czXe1nyXxS8DUQfxXPhk0kE9RKP/scf8g5007V8igKYq9D/9j/pXh/Zvi/rbY/7B
FuNPG6z/2spS/7G9g12fQdhrrp4aqfgdb070/zbof/oD119b1N8O91/9za99cO0r+BqUxw+hDK5v+V8j+LAaadcUWXsshv7fFvXv
f9TfTlztg69BMXmvufcPfay5oVOaGzql2UUeQluWXceudva8xY0xaf/FlDn/wP6T7Ki/Lepvi/UXO9x/2aP/sVHF+iP1z6Zo/+Pu
uwifzI/+x0ZwT49D/1Mfxj/1SAp9C0rT//zgvTN6dPCNyD8fNUZLee+bSdkBoHFBiIQgrkvT/v3gwzTtPwkBoNFem/889s+ZP9/U
g6/vhIZQSu3gyWDoKrJz4ZPnf/lXOv/Lv9K//OOPe/64753/5V/pj//2r5q6tmD9tjeVtAGgO/7uNrWvAPdfNrj/6lVrAKXU+yGE
FfXcWy+lPgBD8m16VRxAov7pMQFti/r3BwZANjiAZ4v626L+/YEDkHYIIOtv25rvpj6IJ4n658D40wbzD/0h7caGNPN0yI7+xw7j
H3u0f1vU3wbzz7YYf9pj/ddW2vpL0v1LRzqvDb6G8MnsmH+2l6b9j+0d1NVTI6leh/SytP809af/z4b69wfWv+xwAKx/uRBKf/3L
X+8ifLIafvhnHEJAy0H/b4v5Tzusv/Q/xj/Vy3PNdSHofAbVov1XI8sBPB6AVD7qb4v622L9vT9w/2WD/sfW8ebI6szEwVL3PyA7
+h8b9D/26H/s0f/0Bz+Azxfsfx5eOapvfjVu8RY3rLIDQB9eOaoHX99J/DkPvr5DCGJBwfYvJYevPjr4huE73nwezc8ltvnxHQM6
OzDIQ6hS8oMPs5r/4kHJ72ZryhoAivJw/2WP+69utQdQSt0fgs8Vf+bOQ0nxB2DuXzpS9dvclMo6gET98yn7AB6yof52qjgAjGzS
HsBL+zpkQ/1tldn/U/9sCIDoD2k31nL9LV+aAxguhDLuIJ4k6p8R4097zD/YyToBHTdPNzNxsNo3uwmVvQBAAGg+ZY1/qH82tH9b
LEDaY/7ZFuNPe6z/2jjeHFk9fayZuv7S+mfg/3G1n7q2oE/m7xGAkgEBrPaS2r/UbttJ/c/E4Qb1zyht+09Tf2RH/e2UPf/M+mM+
ZR4AIwAum6T1r23Nd7vWv9yfXceu9oQeUv/sourvB2IlPfiO8Ml8yg6Apv/PhvnP/sD+k/6X5fcE+WS55hI+WQ4CcG2lOYDnasr8
Q/movy3qb4cAOFvcf9mj/7HH/gcb9D/20l5/Jdp/Veh/bND/9L+48c9X07ckSS+eO6UXjxzq+bcuEI4AxHTSBoC6tp8mBPGjxmjt
/z82k7D2HwxfjWr/6OWCWG80X0/1x/0++HX/7sx72nn7euifEwtzhK5mdHPuvn78P/8l9Z/7hz7W1LUF67e9Ibk951L+AFDCP8vj
j2mY/7HB/de6WgMoXWc0PnVbM3M3eg62hIk7AINs/ItBGQeQkB8dkC3qb4MDwP0h6QCeFF9/Jj+Lof62ivb/1D8f+n87WQ9AUv9q
pD2Acf/SkZ6DeO7wF/XPzoUF0P/YON4cWZ1dXOnM/QS5rzH/UK0sBxvdZKn/h/DJYtJuLCEAtFwEsPaHtP0P9S8fG9D7A/PP9WP9
yxbrv/0hS/2l9mfg/0E+WQNA6f/LRf/TH8oKwEU+1N9OWetfrD9mRwBof0i7/uXCKLc136X+JYqqf5oH3/nhk9/PEwCaVVkB0PT/
+TD/aSfr+gv1L1/aAD4p/T4J5OdCKOOuuVHhk4yB8uEBhPbS7H+WmH+oCvW3Rf1tsf5igwCy/kD/Y4f1Rzv0P/2B9Uc79D92mH/u
X1Hjn6CvTl/ohFGiXGnaP6oRN6fpt3faf32SAlcfHXzD+i0CmWQJAE0T/tl8ZR8Pg88o7b4Sxv/l4/5r3bN1/w+64kvq/Kczd/Ou
Tv/mb3sW1cMKTipuPn79x0df6/re3//uD9S/Qn4Ah5Su/vcvHdH+k92d0/1LR6h/DtTfll//8dHXujYzS9EBNNS/PLR/W9TfFvW3
Rf9vx11/v59/P/RQl9S7qZn6l2ds76BmvdrvbLaf1pW0CLn/5HTX96h/MfQ/tm69Ma6zA4OaDEy6nR0Y1GRrpef1zD+Ua+HbeTWG
m5HtP4iwt3Ld2rNDh9auAz5Xf3/BZWbioManuj8XPo9isox/qH/5ktq/j/qXy83/x41/fFHjH2TH/LM91r9ssf5rK0/9US7/GpyE
62+56H/s+AHQUu94c2bioO4uPOr5d9S/HMEA1jT9j0T9y8T6l72k+R93CNLVPuxzunpqJHFjNLp9+2ThmeH591fTrn/NhswRue9T
/+zS1H9b8119P/9+zzpM2O/A2N5BfTJf/fvejL6PmP8MO4BN/1+esuY/qX9+aa+/Eve/VfD7fv9rQW7tJez3JOpeDfE+vfhhT+1d
wOTklaM9r0/7e4JkWfdfte+Vaf9lKmv9Bfmw/mWL+tvKWn/G/+VKc/+V5v4X+dD/2GL90Rb9jy36H1v0P7aYf67P3HJLo88PxH7f
+X7+/cj+B/VI2/4l6cVzp6RbXxKEWBLaf3/55lfjXX+Pa+8fNUZ7vgZsJvNfPFDzlX3Wb2PD239yWgvftjftNIabXd/7h4//SUd/
/jPWXypU1v3XZlF7AKXUDiAIk/XNTF1b0Cfz93gCc0au/mcHAgPNs6cz/Rzqn0/W+kd1QNQ/H+pvq4wAGon651VW+0c+1N8W9bfh
Ajjo/2252qcNIKP+5coSgCVR/7LR/9g6dH1GkjQT+PrczbvSb/429c+h/tnMLq50Jp9dCKXv5Vdf192bn6f6WRy+yG/XnTktKHwB
4Nc//1nP6wncKxcBrLZo/7bKGv8gH+afbbH+ZYv1X1t56u8/BIPrQX4cALBH/2PL/x1w5m7e1fhv/lbn3nop9c+h/tmVGUBM/fPh
/ssWAaC20q5/RR0+ov7FpK3/xck3tf/kNAGsJcr6ABKJ/r9srP/aStp/EgzV4/63HHkegBr1ADDWf/OLCgD1fx9cyCEBiOXjAYS2
ylh/of/Pj/UvW9TfFuvv9sIegPT3v/uDfhuy/5Pxf7nof2yx/miP/scO/Y8t+h9bzD9X79snC89cHmqsalmhIZQufPLy09Z6P5Sx
/0F5vp9/P7b9+/sPJemr0xdqemcbV5YA1rMDg7T/PuOHTdLeixmful34ZxCCaOP+oY81de3nukjtS/HwQHvt8daeHd3f+M2vUv8M
7n/zK+P+a7PUv9YAyk/m7z0zPNRYdQEEQVkDCJAP9bdF/W1Rf1tlBdAgH9q/Lepvi/rbov+3dej6jGbUewAmSwAZsnOHj269MZ4p
ABTl8A9/Sd39z9zNu5qenpZo/5UJ1t83d/Ourk1P1/p+tjoXRilJM9fv6tc//1mmg6Uzdx6yASIDPwBU6q3/xQ8upv5ZHD7KjgBW
W7T//lDG/ddmWQCzwPyDLepvg/VfW3nr7z81deb6Xe1fu09APhwAsJFq/oH5n0qFhU9K0uirL0cGMKFcZfU/yIf1L1sEgNrK8gA8
al++rPUngLVcZR3ARjZx678S19+q+fUvY/8J97/ZuPUX9/C1tA9AjQrcY/03u+8JADXjrz8WfQAh9c+vrPl/+v98WH+xRf1tUX9b
BJDZov3bov626H9s0f5tUX9brP/WIyqE0g+f9NcD4up//tINje+IDvOTpJmlVuz3t5osAYgzczdo/yXKEsDqfgei6k/bLybp98B/
Hco3PnVbH27frrcfP071erc246/REIKIjc7t/991p3fdV2rv7dfPf6ZP5u89c7w5spr087j/zabs8y+bof617jkeHmqspgkgCPsF
8BPQ2ZSYT9oACOpfjSIBHNS/OOpvi/rbKnL9RXHU3xb1t0X/b6vnAEZg8eW3v/lbnXvrJc3cedjzb6l/efIEgFL/6t29+Tnt39Dd
m59rbO8g8w81yxr+hmrcvfk5AaA1IoC1v9D+q1V2APRmWACrE/e/tlj/ssX6r6089ffDJyVp/I2X9Q8f/5OO/vxnBMVlRABrf4ub
f0Bxrv0TgGiL/sdG2utvGMY/xQXrzwOo6uXXnwfg1S9v/elvypGq/6f9m+D6Wz/2n9jwQyh938+/n2n9BdkRANofwh5AKIn1xwoV
WX9Bcax/2aL+tlh/t1XkAWDUvzj6H1vU3xb9jy2uv7bof2zR/uvnB/H5wsIno9p/+yFs09KSIoP4XADfZGtF3z5Z2PJzQlkDEPPs
P0e8LAGsUe2ftl9M0u+B438mKM/s4oo+3L499evdmkzwP4P867HUXjdAOcICQFHc8FBj1d/L70s6A8z4szjOv/Tqiz3frvh3b34e
OoDxD8HMXL+r/WsHhVEO6m/Lr3/YARjqXy3qb4v694eo/l/avAOgfhJXf1SP9m+D/t9WmsUv6l++4OR/VAAi9a8W7d8W9bfnh7+F
TYCOT93u/PeoAzHIx5/8p/71I4DVFu2/PxAAbYP7X1usf9mi/v0hWP9g+KTjQih//fOf1fr+NjoegNSfgrUPew3jn/IkBSAy/qwG
B5D6E+N/W0nrLxLtvwoEkNnKUn9Uj/k3G1x/bbH+W7+oAL4orL+UhwDQ/uD3KRc/uBgbfk77r9769bf3e4x/qsP6iy3qb4vxvy32
P9ui/7FF/W3R/9ji+muL/scW7b9anRA4T1j4ZNT8g6t/Y7gZGsRHAF+4tAGIadq/JJ2/dCMyBFFa/xywLk0Aa1L7l9ptm7afT/Az
CPtdkLrDJ5PaukObjzY81FjNEj4Z9P38+z1rNFK7P/rmV+sP0T5/6YaOXrjX8+AwrPPXT+LEBYDOf/FAzVf2lf/mtjh//Yvxf/22
8v3XNus34KQpvrR++OXohXu1vr/Njvrb8m++/K9T/3LEHf6SqH/VqL+ttIcfw7jPYOHbef3Dx//Uk/6PZEXqL7U/A/cH2dH+baXp
/8+99VLP1+n/y5G2/sGnulP/ckTVP7j5IYj6l4P2b4vxv624px85Lvwt+PXxqduambuhmbkb+vvf/SH1YgLScwGgYah/9YIBrMHv
j0/d7vxBdkn9T1T/L9H+q5YUwMT9b/UY/9hi/csW9bcTNv/p+qGHB0ZD/xz8za8s3uqmlLQBRWL+v6g0829xtWf8U1zeNRjqX620
G+Cof3UY/9uKmv+XaP9lSNv3U/9qsP/EVpbw+eD3af/Fsf5oi/V3W2HrL36fIon1xxotfDuv7+ff7/oTF6zH+mO1WH+3w/jHHusv
tqi/Lcb/thj/VyvN/Rf9jx3qb4v+xxbX32rR/9vKc/5x/osH1L9Ebg4n7HNI0/8sfDuvydaKZpZaXX8kAviifPtk4ZnLT1uaW17/
I3UHIErJ9fdrH4bPIZr7DPw/wd+BLPWn7WfnfwZhvwuXn7b08quvS5LG9g7GtnWH+id7bf7zzh9J+vTih5Gv9cMO3XqMvz4jdYdP
fjV9S19N39L4jgGdHRjU7OJKhf9PNq7xqdvKEwTqai5Jc0OneDBbhRj/29qq9a8tgDLpAECYYPEd9yHQ4adH/W2lqX/S5JtD/fM5
/ZvJnq9R//pQf1tx9d+qA6A65am/xAasstD+bSX1/0mLvw79fz5J9Q+i/uUK1j8sfNL/HaD+5aL/scX4v/+4px9J4Zv/3eELZ/TV
l/X3v/uDTn/6p7re4qaQNwCU+peDANb+F6z93YVHtP+S5AlgYgNceZj/t8X6ly3qbytvAN+uO3Ohf27/7oM63vamkfcAgMT8f1ni
5t+Sau8w/qlO2OdA/evB+L9ajP9t5Rl/0v7LlbT+zgPYqpWm/gSAVof9J7ZYf7TF/pP+46//St1rYKy/lCdNAOj8Fw9C/y3rj8Wl
Wf+VeteAaf/lYP3RFusvtqi/LebfbKWpP/tvq8X9lx36f1v0P7a4/tqj/7eV5fzRJ/P3njl64R71L1EZ8/8uiC/4hwC4aHEBiFnq
HxVCSRBfOi+/+npPAGue+tP2s3Pjn5m5Gwr+Lvz97/6gl199vWsPhB9CGdbeafP5+UGTcV+T1Hko2MK385pdXOkKn/S5EMrhocZq
ue92Y5tdXOkKnywaAOr4D0RlP0qyqPWv4Pqvj/F/eZj/CVfbhWt4qLH68quv69zvzna+lrT5aniosXprz47In3no6yUuvilRf1vU
317wM6D+9aL+trLU/3hzZHV2cSV0ACS1B66//vnPqH8GWet/cfLN0EGoq33YE0sQjfZvK0/96f/LE1f/sb2Dkronobn+lsuvf9jB
L4n6V4nxpy3qb8fVfvrqP3S+5iaf466/UaEpczfv6re/+Vvqn1LSAkDwM6D+5cpT//EDu3T60z/1fAau9tx/pRfW/0jxfVBcaBPt
P5u888/c/5aD+X9b1N8W9bdF/28rrP5S9GfA/H/5oubfwtow8//lyxJCQP3LlScAgv6/PIx/bCXVPyx8j/Zfrrj5/2D96f/Ll7X+
jD/Lxf4TW6w/2mL/iZ2k9d+rp0YkdQfwsf5SnjTrj1dPjXTqz/pjudKsP/r1ZP29XMw/22L+wRb1t0X9bVF/e9z/2qH926L+tqi/
Pfp/W9TfFvW3VVb9D329pLMDg11fI4gvGe3fTtz4R1JX+KRbh/fDDMPauyTqH2F4qLHqBx86bz9+rG3NdyVJO5ujknrDJ7+ff19j
ewc1cbghPwS6MdzUg6/vxP7v7ttzgM9kTfAzCKu9E/YZSOra//CLgwfl9qS4IFBJOn/phiZbK6yHxch6/tf9G/r/cnD/G+7Zuv6H
vn2y8IxuavX0b5TqAICz6054MvHM9bvSz39W2fvdbKi/Lepvz/8MHOpfH+pvK0v93Q3wwwOjwW9Jkg5W9i43r6ztPykB/de0/0xo
/7by1J/+vzxR9Y+buKH+5QnW39U+ePDRR/3Lw/jTFvW342p/5OivNX31HxInn93199Yb42E/rr6Jw03E1d6J+wyof/my1n92MfwA
3uirL+vvf/cH/fY3f1v5e94sgv2PlLwAJkm0/3LknX/m/rcczP/bov62qL+tvPVHOYL1l5I3oDD/X66w+beots/8f7myBiBS//Kd
/s1kpg1wEuP/sjD+sRVX/7g1GNp/eeLWH6l/9bLWn/FnufKsf9H+y8P6oy32n9iJW/91wYeSej4H1l/KE7f+6AJAHdYfy5Vm/fET
b6jD+nu5WH+0xfyDLepvi/rbov72uP+1Q/u3Rf1tUX979P+2qL8t6m+rrPovqB0G1/OzEYv2bydu/COpJ3zS/TsXQHbo66Wun3dr
z46eryHZh9u36+3597Wt+W5P6KG0Hj7ZXn9ZWc0SPilJD76+o317DqzSH7W9Nv95578/UDug09U+KQB0dnGle/5/m7rCJ7+aviVJ
Gt8xIC1Jk4sr1f6f2cCynv916P/Lwf1vuFrXUbMcAED5qL8t6m/PfQZdf0dtqL+trPXf7AOguqWtPwfwqkH7t0X/byus/p/0njFC
Rfz6U/v60f/Yov52/EloKd38w6HrM6Ffn7t5V+IATGp5FwCofzny1p8DSOUJ9j9Sch9E+y9Pnvln7n/Lw/y/Lepvi/rbov62eACS
veD8W9LrGf+UJ08AIvUvBxvg7HH9tRVV/7g1GNp/udKuP/IAwmpkrT/jz3Jl3f9D+y8X64+22H9iJ2z9d2zvoKauLUQGgLL+Ug4C
QO2x/miL9UdbzD/Yov62qL8t6m+P+187tH9b1N8W9bdH/2+L+tui/rbKqr97AB6fXza0fzth4x8/eFLqnf93858LgZ/F/Gd+fgil
7/v593XurZc6n4XU/QCkH7x3phN6GGVmqVXum91k1gI6UwWABvc/zA43e8InnU4IpRqEf0bIc/4X5eH+t1ft69hZDwCgXNTfFvW3
R91tUX9b1N9WlvqzAat8tH9b1N8W9bdF/W1Rf1vU3w7zD3ZYALBFAKs9NkDYov+3Rf1tUX9b1N8W9bfFA5Ds0e7rlzcAEeVhA5w9
rr+2qL896m6L/Se2aP+2qL8t6m8nOP4h/LM+BIDaY/3RFvdftqi/Lepvi/rbov72qLsd2r8t6m+L+tuj7raovy3qb4v626L+dvzx
z9jewcjgSVTLhVD6ZiYO6u7Co66vdfY/DDfremubyo3m6z1fyxIAGvTdmfckSTvP9H7vhKTJPQcKvd/NjvsvW9S/m8mDFCm8Lepv
i/oDAAAAAICqMf9ghwloW9TfHnW3Rf1tUX9b1N8W9bdF/W1Rf2xFBCDa4/7XHnW3Rf0BAMBWw/jHDgGg9mj/tqi/Lepvi/rbov62
qD+2Mtq/Lepvi/oDAICtxo1/mPu39eH27Zpbbuny05ZmJg5m+rcvnjsl3fpSX03fqujdbWzDQ43VD7dvj/x+2gBQlI/7L1vUf51J
ACUAAAAAAAAAbFZMQNui/gAAAABQPQIQ7VF3AAAAAKgH918AAAAAAAAAAAD5zC23NPr8QOz3fVnCD786fSH3+0JblgDQxnBT3/xq
XHrvTGzo59mBQU2qscoaG9D/tlm/AQAAwhw5+mvrtwAAMED/b4v626L+tqg/AAAAAGAr4P4XQJm+fbLwDBsEAQAAAAAAAAAAAAAA
UAf2v9mi/raoPzaib58sPHP5aasnZNJxX7/8tKVzb73UCZ+cufNQn8zfY2+igTQBoHHhkwA2lr4PoAwbAM1cv6uLH1w0eDdbD/W3
Rf1tUX873z5ZeObuzc97PgPqXx8mILCV0f7t0P/bov62qL8t6m+P+y9bp38zaf0WAGxR9D+2uP+1xfjHFvW3Rf3tcP+LrY7xjy3q
b4v622L8Y4v626L/wVZG+7dF/2+L+tti/QVbGe3fFuMfW1x/bVF/W9TfFvW3Rf1tUX9b1N8W9bdF/W1Rfzvsf7NF/W1Rf3vMf+YX
FUIZDJ+U2sGThE/ayRoA+uK5U3rxyKHK39dWx/jTFvU3NjzUWH3zv7+9urLSWl1Zaa1e+fSL1Tf/+9urw0ONVev3thVQf1vU3xb1
t+d/BtS/XsH2z2dQn7Da+58B9a8e7d8e/b8t6m+L+tui/na4/7Ll6n/n7p87f/5w4RqfQQ3Cak/96xNVf/cZUP/q0f/Y4v7XFuMf
W9TfFvW3x/2vDeb/7TH+sUX9bVF/W4x/bFF/W/Q/dhh/2qP926L/t0X9bbH+Yof1X3u0f1uMf2xx/bVF/W1Rf1vU3xb1t0X9bVF/
W9TfFvW3Rf3tsf/NFvW3Rf3tMP9Z3PBQY/X0jmbXn+Ghxurx5kjnT9S/c7UfHmqsfrBrZPVP+w9G/vlg18jqB7tG+Fy0XvNrf30g
8k/YZxH8GX79V0//Orb+7jOg/uVh/Glrs9d/Q6T9Dg81Vl9+9fXO3+/e/FzfPlnYEO99M6D+tqi/Lepvz/8MqH+9XO2nr/5DJ32b
z6Aefu0dPoN60f7t0f/bov62qL8t6m+H+y9brv7nfndWczfv6tr0NJ9BTfzaS6L+NQvWX+IzqBv9jy3uf20x/rFF/W1Rf3vc/9pg
/t8e4x9b1N8W9bfF+McW9bdF/2OH8ac92r8t+n9b1N8W6y92WP+1R/u3xfjHFtdfW9TfFvW3Rf1tUX9b1N8W9bdF/W1Rf1vU3x77
32xRf1vU3w7zn8UFA9vS1s6vfWO4qbMDgxrfMdDzupmlliRpsrXC57JmeKix+otnBzT6fG+95pbb9br8tKWxvYP6ZP5eaM1c/e/e
/Fzf/GpcX03fiv3fnFlq8RmUjPGnrc1c/w3zf8K/gGyW4m8k1N8W9bdF/e25z4D6148JCDtMQNij/duj/7dF/W1Rf1vU3w73X7YY
/9jZzBPQGwEHkOzR/9ii/rYY/9ii/raovz3uf20w/2+P8Y8t6m+L+tti/GOL+tui/7HD+NMe7d8W/b8t6m+L/scO67/2aP+2qL8t
rr+2qL8t6m+L+tui/raovy3qb4v626L+tqi/Pfa/2aL+tqi/HeY/7QRrHwyhJHwyWlgIpR8+maZert8hgNIO409bm7X+m+b/CAAA
qAYTEHaYgLBH+wcAAFsN4x87m3UCeqPg/sse/Y8t6g8AQL0Yf9pj/GOL+tui/gCs0P/YYfxpj/YPwAr9jx3Wf+3R/m1RfwAAAAAA
AACbFfOfdvz1F0k6OzDY9X1CD6O5EEpf2vBJ/2cEgz+DCAIFNhZ+SQEAAPoYExAAAAAAUA/uvwAAAFAnxp8AAACoE+NPAAAAAAAA
AAAAAACwmQQDKdkTEa+MesWFUBI+CWw8/KICAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEKFhVASPglsTPyyAgAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAiuRBKH+GTwMbz/wNiwhW+gfDrfgAAAABJRU5ErkJggg==
"""
VIEW_B_B64 = """
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
+v+trNHuBBsAbLEBxh4bMOzMLbd6ai+FTuDsxgbg8kKTv2U2YFD/4johfOv/fWfhkSRx/zXkOvMztx/qo8lXtP/ktM4NDpE4XwOu
f1tFTsBjE1h10iZg/D9L3QvTBwa+1+rqTiZgSvrt6ne9131LPQPQbrOLW/TjwrgZgM7P9UF/v+v74AY6N/GV5Z7LBpjiOgvQ1xec
x004+lgA3YzQGFBcANzUaotFuDm48Te/Xx8N4Iv61bk/bMmTjywc3TukycXuk7xc/fftOUj9axatv3/tu3YnFAC6/+R0Z84gOl79
2Xxjb3/TSxv/jwsA5Z5bHcb/7TD/ZYv5X3vRA3ikjWv/08/fliT9df4u4881of62kur/1/m7nf4n9a9eUvs/tdqi/a8Z/R9brD+x
FV2DUnj9CYcflbYxB7yyPqcVHz4Q3IDNAbSlUP/mzS23OqGTPj/82Z8LW3q8rIGBjU2PLrhMov2vQlL7Hw1/kMT6w4qFNkAmhdCw
AbUaVQQgory4AERfXO2P7BqUlqUp1sCVdmPPSOcz8O+3G2utNkKXomvYkU/c/NfZv1yXFF5/wvhDdUL1d3OPecYfUMyx+as6Junk
C0dKrX8mhKw8N+7mDAx8r6XH3/fcA6JjPxNqr12h71/MZ/N3d7TXoBe//ll7nl/vASTh+vtBTF2hk34YDQeQ5ObG/6PtjtT+HHaP
7Eo9+IXxh3KyBrCGMP5QLX/8zeeCl/wwOMkbf9vD/beMuANgfNG9YB1eAA1tUDnTs1fl5l384GH35+jaE9qfasW1/3Hh2wRwV8P1
//0+pOvvhA6hkuj/Vynr81foHkz9y+uEUMYIHQrpW13dyb67gtwhbCHuYLZo8HNSEDSK88Mn/eDJh0vteRf/+h8Z3kUIZU5ZAhB9
/v6v2cWVnn3Z0dwUVMMPAv3087f11/m7ne/N37yvC1cWUvegugybzabxPGs2ANhiA4wdNmDYefB4YcfU8Nja2fnrXWEaDhuA7RTZ
gCExAFqG34F04Yc/ff197r81u7PwyEuOj3fv0nHtPzndNfiD6oQeoOh/1svfgJcnhJJNYNVJm4BPOoU5en9mMKiYB48Xdvifg+/b
tyY6A6HnBoc6k2GdRW+tjX+jsTe8BYQC0Kdnr2p1dWfXCUddC60imAAuL7oA2p94dwtApZ1dg58sgK5GkQBEaSMAzje12tL5V5/T
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
31l4lBiAkrT+GdlEA1ij4ZNc/81x94Cu9p8DOE0krf/P2v6cbr/E+H8GBLDaiQtAp/7N6YRvL7f/PLXa0szpQ4nt0MxSqxN+67/m
rI/d0f4EpIW/pe3/krj+y6ii/qhXWgA91391/IMX3DNw3O8A60+qUyQENBQ+6Q6Moe7VS9pX6n8OHDhSjTL7v1BelvmXUP23EpMA
Sn/x+fW5e5KkZ8aP6NH8nJ4af3tjEwAbAGrDBhhbbMCwlyWAjAmAakUHQWcXVzbaGOrfGDag2inS/5E2+kA++j7FVHH90//ML2/7
LzEAaokAvur4k49xJ+DFbYbsLILw/ozsipyATd+zXlUEQKMYAvhsZel/Jj0jjM6/v/bg8QL32wLinr8kSeNH9OKR/V0/T/2rl6X9
4fqvD+2/Lcb/bTH/ZYf5X1t5+z9O9DOg/sWUHf+n/uUU6v8f/kQXrvyc+ZcK0P7bo/9jL8/6k9PiAMgqhDZA/nX+LgFwxkI1znLt
M/9YjaLXP/UvjvWHzYsNACKAqVZphz9y/60XAYh2/PDD0NhN1vBP9/PcZ4txn4P7c5a6swGvHknzj8HxB2d9HMLh96EYxn9sUX8b
ofXns14QbrT/P7u4Il1Z4PnLGOufy4te+zO3H3L9G6lq/Q/KSwtgkmh/qkQAq52845/MP1avsw9s/b/TAsgmF1ekJXVCKF34pAvB
5RmgHNcP2n9yulD7wxxYOUn1lxj/r0o0/NBvd9xhMFz/9Zm4cEsfP/20JGluuaWJC7c6IZRJe399ofHoy6cOVPk2keCv8xuZEFz3
+SSFgLq54ejvQSgElLqXx/4vW1nzZ0I/s5X2PjYeQBlafO7EbQJgA0C12ABjiw0Y9tgAbOez+bs7XP2Pr7+WVn9Uhw2odgr3f6RO
H8hH3fMre/13vca1n1ue9p8FENVJ2wQQxeRj9UIn4J1/9bnYn/f7naHJGQbjsos7AfujyVcS+/FMgFWPBbh2COCzlaf+oWcEPoPi
XO0//MXftV/4xY/T/1LXz7T/++//cWtNBDSJ698W7b8txv9tMf9lh/lfW4X6P84v/qyf/q//zQbgEqoY/z/t/R3qn0+5/n/7+vdR
+3xo/+3R/7HH+Ked4AZIiQC4hhHAZ4v622H9oS3uv81JO/wxaf6dNSjlVRmAiGL8z8C5cGWhE4AeJ7ThFMX5z6mziytrnUPGAwEc
+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
+c2t7OGTnk//68+6cGVB8zfvM/mITYn23x59HFtx/U//C9U7undIT+bbG6ajNab+zeH6t8Xzry1qbIv626L9sRPtA/n3W2rfDK5/
W/Q/bXH926LGtqi/HcafbVF/W9TfHu2/Ha5/ANieaP/t0f+xRf1tUX9b1N9O2ftvOwRuofMVDS1AMvo/tqi/LdofW1z/tqi/rZHf
3OrsocvLtT3s/7KVFMCH7K6Nv6Q3Bwb18PPXMv8dP3zy6+kb+nr6hiZGBnVucIh7ccSDxws7plaTgwmnVlva/frlzP/m386+q2du
fRn8Qpj7HPzAz/jwyW7f/vW/NdlaSQyYdN+bbK2I8Nvs7iw86vy3C4V7avxt7T85bfSOtjdq3wzW39qixhsaDaCM2wDMxd+MtA3Y
oddRHerfH7gB26LGNh48XtjB/dcO9bdF/fsDdbbDBKS963P3SgWAsgCiOK5/ezx/2SCAz1ba+Cfqd/nUgdgAJtSL699W1vkXPo96
MP5vi/rbYv63P8ycPtT5HKKezL/P51AT7r+26H/a4vq3Rf/HVtz8o/9n6l8/amyL+tui/jZo//sD8492mH+3Rf1tUX97tPE2WH9i
i/EfW9TfFvXvD2VrfO/wJ5obPqW54VMVvaPthedfW9TfFu2PLa5/W9TYDgG4zfED34p8P4QAPjuziytd4ZO+iZFB3f/mtkaHx9Ys
3ls/m1vuDT+MXvtp99+Hn7/Wqf2jQy/Hfp0bHOIzCPBDKP3wyd2vX07d87v79cuxIZSET5Yzc/thJwzaD6F87eJdSeoEIrrA55Dx
F/bp9E/G9Mb4Aa77nPwQUCkcQplUe2TH+ltbjD/3ajSAUpLOv/pczwZgHxtg6hWqPw1Qc7LUH/VgA6QtbsD2op9B6P6L+lB/W9Tf
Dhsw+gM1tlPFAnQWQJTD9W+D5y97BPDZ+Wz+7o4s/c+0MVA+r2I+m7+748KVBd27dDwxgIn61yfU/vhc/VEPP3yM59/mMf5vi/kv
W8z/9g93r/W/UK8s1z/qk6X+9P/rk/X6p/71oP9jKzT+Q92bwfyjLepvi/rbo/23w/xjf6DOtqi/LepvI63/w3qI+iWNP6B+jP/Y
ov62mH+3w/4vWwQQ2KL+tmh/bDH+Zovrvz+Eapyn/uz/SucHvoVEQ+DS6k8AX355AkCzXv9/O/tubAgoernfg1D4YdZr3/fo0MuS
pGfPn9Kzxw/X98a3KFd3V/us/BBK/0sifDLJG+MH1s68Pp75510I5e7XL2v/yWkdvzCvkd/c0oUrC3W9xW3PhYCGAkBnF1eofYX8
vY+sP28e4//dGg2g/Gz+7o6Z2w+7NkH6uPjrlVZ/ic+gTlnrv50aoCZlDYCg/vWIq/92vPFaSrv/8jnUi/rbov52aP/tsAGpP1Bj
G1z/tnj+skUAX3+Iq/+T+fd1+dSBzp+TFqqgHPcZRL+of33S2h+//rQ/9biz8Cjx+de/P6NajP/bYv7LFvO//WHiwi3NzF3r+vrX
9/5d0sYCCe6/1cty/VP/+mStv0P/v1p5rn+J+lctT/+H9qc+9P/tMP9oi/rbov72GH+wwfyjLebfbRHAZ4v620vq/6BeWccf6APV
g/kvW9TfFvPvtrLu/6L+9eEAWjtZxx9QHwKI7TD+Zo8AFDsEsDYrLoTSD+F7avztXNc/AXzZ5AkAfWr8bUnZr/+48M/fjx2p5s1v
MQ8eL+zwgyhdzf1r38l6//36zEV9PX2jrre8ZT01/rZ2v345V/ik40Ioo1+ET2YzceFW58v3p//3466v/+8//1l/+n8/1rd//W99
+Iu/04e/+DtJ0vzN+xZve8u6s/Co57VQACiqM3/zfur+O9af14Px/16NBlD63Ifgf82cPsQGjIaE6s8GmObE1d+h/vVhA6QtJoDt
xd1/HdqfelF/W9TfDu2/HTYg2WEDhj2uf3s8f9kjgM9WqP73Lh2XlL5QxXGBcchv/8lpLTyY18KDef3uk/+QJOrfoKTr36H9qZab
AJPin38nDu6WxPNv3Rj/t8X8ly3mf23MLq5oZu5az+tHXnxe//rev+vMF191XuP+W5+08WeJ+tcpqf70/+tXVf1ZfFtMWv9Hov2p
U1r/H/Vh/tEWC3BtUX97Se0/7U+9mH+0QwCNLQL4bFF/e1kO4ES9ksYfJOa/6sb8ly3qb4vxNzuMP9jJegAt7U99OIDQBgHE/YHx
NxsEoNgigLV5fhCi+5K6gw99Wa9/AvjSZQ0A9cVd/w8/f03fvjWh//Hu2dj/vYmRQZ0bHNLo8NhaBW9/y3nweGHH0b1D3H+NlWnf
XXilCxBFNhMXbunjp5/Wx08/rTcHBntCKNN8+l9/1oUrCzW9u+1r5vZDffpff04MAJWSwz/HX9in0z8Z0xvjB2j3E3w2f3eHu4bZ
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
W9TfFvW35+7DecInJepfVp7xZ+6/1Ssy/o9qZWn/Xf//4cEjwa9D77zV2Pvdauj/26L/Y4v1P3aYf7dVpP7MN1aH699eVfdf1p8U
k/f+K7H+pEr+3ItTKIDvi69qeodbV9Xz77Q/+eStP/OP1eP51xb1t0X9bVF/W6z/t8X1b4v626L9scX1b4v5L1u0P7a4/m1VUf/L
pw7o6N4hPXi8sIM1W/lw/dvKWn+39zeKPcDZzC3HB0L63/vX9/5dz7/4kqT2/MCT+feDoZ9pJkYGdW5wSKPDY2v53+3WdG38pdiv
d3/0oiR17W3PIi4A9MRC/s9sO8o6/yvx/FUHnn83NH6Q4oPHCzt0XWtn3lHnFOCiGzB+/fOfNffGtwjqb4v628pTfynhBvDzn+no
3qFm3/wWQP3t+Z+Bk7b42aH+5VF/W9TfDu2/vTPvTHZq7+R+AF6vPxNg+eWpv7NVT8BoWtXtD9d/Pjz/2nOfgT8QHa39Z/N3dzCR
Uo8s9Ud9qL+tPPU//OVM8N+Yu35Heudf6nuTW1Te/s/Dg70nEUrSofrf6pZE/8cW9bdF/ftHWn+H+tcjz/gz99/q5an/8dd+renL
v+v5N7zfAU5cziFv/3P37fCiwpkv70i0P7nR/7dF/8cW84/2mH+3laf+UvdnwPxjeVz/drj/2mL+3ZY/9+Kea9MC+ELcxhHqnx/z
77by1J/5x2px/7VF/W1Rf1vU3xbjb7a4/m1Rf1u0P7a4/m1x/dui/raovy3qb4v628pb/3uXjmv/ye5gPsIn0z14vLBjanhs7YgG
Y39marWl5198Kbb2j+bn9Mx4e/3bw89f07dvbcyFPXv+lHTjj7FhiMju+Rdf6qr/6Pz7a4+kTu19fzv7rp452/Q73DryzP/y/FU9
nn+7NR5AKbEBwxr1t0X9bWWt/3a4AVig/vbcZ9D15wjqXx/qb4v626H9t8MDsC02YNij/bHF86+9LP0f1Cdr/UNhxZJ05MXn9a/v
/bt++86/EIBSAPW3RftjJ8v9123AIwCoevR/bFF/W9S//7n2n/rXI63/w/23Xln6n6HFWj5CKIvJG4CFatH/t0X/xxbj//aYf7eV
dfyNDUj14Pq3w/3XFvdfWwTw2WP+0Rbzj3byjD9w/60e/R9bXP+2uP5t0f+3xfVvi/rbov2xxfVvi+vfFvW3Rf1tUX9b1N9WkfVv
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
"""
VIEW_FQ_B64 = """
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
2z13reXhw295x52stbSDOp8H56unC0kQu0X9nz4kPn80+PbRSszv49Fn2pHX545u+/Z+ohv2O9bS1fWJfnk47ynpz/+z9J1v/7Eu
vPKslm982fWv2rhsCSjN4SPbyp1N+TaOH3njynCgunJnU5L/AIy98dzOMD3/9F7pvtiA7rAPgEnS24s/HAz4nQNI9ktCUfwlNv+n
4ABeXk0fPEKcmEN3xL1b9rMweQA10y/VIyxM5tdUH2yYyQt3kWdRg4/3sT9m808ebPrJi43+eVH/p0fRWMdX/29fOhmdeIkN6OmK
yuPn534z/G+7j7bLI7QZnc3n6ZpaLOY5aEbdzRIkAkrTxHtwUT8gEX8XB8HyYP4/L9a/8mH9Nz+3/v9h7dZEGdjxt5+DmOSTlEE5
tw/4zgvno54BEoDW58ZeUlT8jbL2n/pfLCb+vtgX1X/iHy8Uf3f8k5KAmDWvOKz35sMa5HRgTWY6kAQ0D9qhfNqe82S+s1zdpKvE
vL4m2v4DrKs0pol9Qgd4Biqr0yaZtoh2KF7ZIcg/rN0a24Mi+ftq35qjxB6UEHf8E7P2IkkLXf2CPfDb//lA0miuzMxXmrnK73z7
j8e+nqTzzWH+bTpw8UI3nLn67QUVXzTl9rloju/8o68sYsY9qI4zGdOBhGTt8621hMadZo6HM9jtoc53i/F+XiRBzIv6P11IfD7d
zJrWay8dn/jclZWPWPPCrmCfw/jxa28O5yKOvHFFn/3uhnT+bOnPsJPp3ly/19Jv2h9rn342Nh90+9LJsbWA5YXnd02csySgNJNv
5uCLe/DCu3H8zubgBezquqTJzf+hjecTP4cN6JL8m8+PvHHFuwi5eGdTty+dHAxGA/GX2Pyfwhf/2EXg0AEM4h/HPfwYe/DLYPBf
T9mhO/smHncRhtg3y1cW7qbOUFlIlEfTihKB1k3Mym0Ok9xD2LF9sBF7CNhe5JnXXi3f3+ptf8xkaF5s+ukeh7ymB/U/v1AS+lDf
WzbuYQN6PaY8hmOhnXmeM6/NSRpMLJvxv71o/OrFW97kkwbxT9fG+IhyiNfUZgkS8VUTOpQ0mn+YbIeMomS4x7WX+AeUbYo278dG
6JA8/XAc5v/zYv0rH9Z/8zLxlxSs/+6mdPsZWLq6rtfnjk5sgqMM4tjxl+RdB4t5Bnxog8qF6n9M/O1nwEX9j5MSf1/sQ/Wf+Mer
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
wjsSgLarKAnl2H6UH82WngVD2Otzg/GkieWf/acZSYN1XzdRqDR6X5YG5TC3kzgU5Q7MzG7biYZdH6/elpz3AAX2niNNWeyl8TGo
VLz3fzfoLAFlTPIfybf5X5K+p//45/9X0QEMlIiJv92I/8t/+571GeLfhCqHj6S0QwCUx6TUum8LTMJNbPxcurrOhKdHauxDk0CF
SSgl7y2GEslOXGWTCb5b3JsaBBH/0SD0fiDBjLG88PzYpuY+ZENvm0l4UiT1ADDq8y3Anzi0b7ggdm9tdZCA9epF72RQ0SYKO4mf
RBvks3x/a6zfXL6/NYxZyuZ/9xbUvosZ+7g3P0rjBxhPra+OHSKVBgvtJvFkGZJQlvMdPrKTPuvBxYlnwN6E5Tu0Z7ABZSQ2AVDZ
AfjQRgjefeOEJkLdyU+7/5Wkb9aKE9Avana7LNke72MjheXgLAKYMnBvoorZjG5/PZcAjCsrg6IkrHZ74yYCHb1Hf6nFO5vDZ8Id
a5mPGX15LooWY0y7s3T1J0kHwoaHr633gMPO2Emizruxv/8Pz0f3zWuffqb3Tx8dS3RoNoUa9MN+zP/nw/pXXqz/5hUz9ymF4j/C
HGh1PAN5rdzZLEy2HbOJjfrfnqL+V/InAJWo/zHaGP8Q9zRl4397U7OZiSuY/5xIPi8N5q0plzSh+f/bL/yqcP+J4VvDkUQipkip
CfhMEkrJPzfkS2jgKweMhNazzu8kAT37bx9L0vCwhTv3sLDzb7s83HLYf/1DPfHhe9Inv9XkLqN+JKEMraWHLp612yD3AtTQJRjm
glpz+ZGksflnqZ8XTzWRgJsL8NpRtAbvS/6D5hQldS4SGvf4sO4bp2pZSOHkk2X60O+GmOST5uJBc+lgSvxTngOjr+8AB2Zmt//5
f/x3/fhP/rT00jt7rdHsxZqcfyABYqxql+9IzD13a3zuTfLFnwSg8WISoEuTyW79l8BMJqG8uX5veCG80bd+tCq37yxKYm6PIWP2
P7P3No7v3Wvx4DH9/g//qu/91b/o3tqqlm+MX95y4ZVnJ+r8ZWevFTEfiF17MWMdt//93l+p8CIM2v3mmPemsssUQuz9/7Q/48qS
sPrOcNlJoN35N/cCmAuvPMscnCN2z4nkG3eOtz2hBOjEuzrfxXVNrRv2Pfl2zPvu7//wr6M//OXke5c02HfiS0JJArj6lq6u6+m/
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
jRKxmiSsEntRqrDnJMx/u/2HL/kke6DjvD53dPvtxR9Gf71vvdFmkk/OH3tmLEE3gOmXLQGl697a6nBwaW9UL8MkXF7EvxomobvT
5OEXF/FP0/RGB+JfHZtO8quaCJTFgPrcOFcdgyIeB/DyaGLxVwpvgJaY8AwJxd6wJ9lC32/3ERdeeVZnPvhc2hj8uSgRpVkMuPxw
q/fl0/QtkIw9q2lyAzRlkBfxnw6UQ/cYh04P6n+zUvpjYp+O+f/dgfg3g/Xf/NzEkr5ycL/GYAMWpp27Dgz0FWu/+ZAAIh/WH/Mx
SciaTMAXSkIpjRIgugeKpUGiQ/M1lf+HHkF2GYQSUJYlAo2NvzSI7+GDx7bP7R2sE5MMtPmLZ3kHTsP6Yz6+vRB1EkAT/3Qfr94u
/yIVj5UkDS/ipAzSVE6CuMN9Bi688uxEEhQz7iH5s1/sM2BzL7+TRP1vSJ33X+Kfrqm9z8S+GtZ/86ibhM9F/OM8/bfXtfQPzwfH
krx/dYN5ZvRZUUKytU8/0/unj+rVi7fGPu4mhFtdW5VuXBz+mfYnHmcwunP3wfqeA2tvbqvk7Dtj//bYybdd9tjnmQo/m/gX8yXf
sxPvSRo7v5jKTrpnkAQxnxfXPtKLks5KOnzwGPG3mHGPqf+//+t5SdJbl64NxzsxbdDqzGlJo8SfPANxDuwkhSwy9/3DenunjL7z
7T8efvz3f/hXSZOXF84vXR8mnjSOP7lXZ9c+ljR4BqT+7XGoa+nqulbubGrFvAc47wOSdKbj36mvzBjJJK10z8pPJgNlTNQmd/8/
Y9C8HvX4T00CSmlUuYtehN0HYP7YM6LRqS/m8JHv64h/c2Imgoh/O2In4Yh/O4h/flX7gEd9EJSbe7Ojdv7NYkD3qoxBiX2apg/g
Ef84TS/+SvS/seomAHUPLZ04tE+Xza15G9KLnu8h+aQ/+XxTbQ91v7qqG6BDCVDQDd6/pgPlMH0Yh3aHfiBdUwmYaHvawfx/Pqx/
5cf6b3uqtP33nHloN/bfrL2p5YXnm/kFIalaH8C4s1vEP405CHNPaWtaIcQ/XZPJV4l/fXXWu4h/Paw/5tVEAr7kJJSej1f53XeT
m+v3JpJQxiYCTU1COSyDniYD9V6CXeHiWR/egdM1tf5I7NP59qFU3YNC/NsVGivZzwFlUE2VJIiG3f+e+WCQhNIuA9PnLh48pnN7
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
AAAASUVORK5CYII=
"""
VIEW_BQ_B64 = """
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
jzZ1XMUJKKt8/sWnOnzwKHFviPMXtoh/S6Ymp7d+8t9/ubWxsVn668oHH29lMxOjOeJvi/jbIv62piang2N/ZmaW+CcWE3/rz7ob
EX9bIfGnDNoTW//TBqQT2/f56J9/uvXRP/+Uckgk5tl3sacM0ol9/l3MiXs6jL9GS1l5UAbdoRxsVdVLlEE7iLuNkHaY2KdH/8cW
8bdF/O2FlgHl0B7eg9EzNTm95X795L//cqB8rnzw8dZP/vsvKYuW8D50j5h3j5jbqrsGYP25d4vY9XfWvtKqswZJ/NOJff6Je1q0
v7ZYgx8deeNc6iEbrP/aYP2xe7TBdoi9LeJvi/jbqtP/t/7MuwnPvy3ib4v6xxbPvy3On9ri/KMt8g/YIv62iL+tbPz/fOT5wl9T
k9Nb31x5tf/LX4+3/v/xuKt6D9w7cPDYv/d/TU1Ob22d/6fSMnO/3jowSx+qRFH8pyant87vn9k6v39m69rfHt269rdHt87vn+nH
vir+xL0c4y9bxH8EUAi2iL8t4m+L+Nsh9raIvy3ib4vD17Z4/m2xAG+Hwxf2qH/sUQajpWwxhjLoDuVgi0NgNjgEZoMklDbo/9gi
/raIvz3mQe3xHoyubCJKkk+2ryohCklA06MO6h4xt0X87dDvtMX6ry2ef3vU/7aI/+hw41zKwB7lYIP1x+7RBtgh9raIvy3ib4v4
2yL+toi/LeJvi/jbIfa2iL8t4m+L+Nsi/rZCEoBmy8AlniT5ZBqhZeDi7/8iAWVzVfF3sXaJKP0ElMS9OdoAW8R/BFRtNqcQ2kX8
bRF/Wxy+tkMDbIv42yL+toi/LeJvi/jbIfb2KAN7IeNf4t8NEu+NhqJyIPFGd/LKgPi3j2ffRlk7TOzbw/y/LeJvi/jbCx2D0Qa0
h6R7o83ffGj9WcZBNvEn70H7qIO6R//HFvG3w/qLLeJvi/jbY/3RFvEfHay9jAbKwU5RfUTs20MbYIfxry3ib4v42yL+tjj/aIs5
IFvUP7aIvx3qHlvE3xbxt0X8bRF/O6Gxz5bBmZlZkk8mkE1+WJbM0I//N1de3ZqanN5668BsUBJEEiHmi0nAWpb8c2vx3dyElMQ9
DOMvW8R/2J4u/2NfPVh7Qh9pS5JePvVPkqTFq/8+8DNLH97SO2+90+XHGhvE3xbxt+XiT+y7l429RPy7VPXsS8S/TX7882IvEf82
Uf/YIv62qP/tEHt7lIG97PiX+t9OUX+UMuhWXjm4Mrj10fXe99GqbBkQ/27w7NsoaoeJfbuY/7dF/G0Rf3tVZUAb0L6yMiD+9oh7
t/rxzrwTkngPWkId1D36P7aIvx3Wf22x/8QWz7+90LEv2sH67+hg7WU0UA528uojYt8u2mA7jH9tEX9bxN8W8bfF+Udb7EG3Rf1j
i/jbYf7ZFvG3RfxtEX9bxN9OyNq745fB+6u3mX9uwYFPVwq/l30H7lx+WUdeWZTWpbn9E/l/Z31TkrSwucGaQYCvjx4v/N6///4/
++svWXfPX2rzY+16jL9sEf9hZpWly/D5/R+dlCQWfztG/G0RfzvE3o6f2fn7PzrJpquO5T37EvHvytTk9JaLvUT8u5atfyTq/y5R
/9ui/rdD7O1RBqPB9YOIvy2/HCgDO9lxAWXQPb8MiH93ePbtEHsbzEHbIv62iL+9bBk4xL87eWVA/DHO/DUC3oP2UQd1j/6PLeJv
g/V3W+w/scXzPxr8+p/4d4/139HA/P9ooBxssfbbPdpgO4x/bRF/W8TfFvG3Q+xt5a23UAbd4h2wRfxtcP7OFvG3RfxtEX9bxN9O
do5f4vL3LmTXGov48b9z+WVJ0urHn0uSTl26rQsTe4eSUJJ8slrd+B95ZVFf/npOdxdvlv+99U3iH4nxly3i32P+fzJbEOMU/FFA
/G0RfzvE3habruxw6MhO3iZ0ifh3jfrfFvW/Hep/O8TeHmVgj/p/NHD4YjSQeMOeKwPi3y2efTvE3g5zELaIvy3ib8+v/yXaAAu0
wQAsUQd1j/6PLeJvh9jbYP/JaOD5t8falx3Wf0cD/f7RQDnYYu3XBm2wHfqgtoi/LeJvi/jbIfa28ubhKINu8Q7YIv52mH+zRfxt
EX9bxN8W8e9edq8tl793Iy8Jokv45rv10XVdPTc78LWL19b0/urtJ6Ymp7cuTOwd+rdJflitLAmlXw5+8s8jryzmJv0c+LskAG2E
8ZetcY//yPwfZfHXFvG3RfztEHs7bLqyRfxtEX971P92eP5tEX87xN4eZWCL+I8G+kAAAHSP9tcW8bdF/AEAwLih/2OL+Nsh9nZY
f7HH82+L+Nuh/gGA8UYbbIv42yL+toi/LeJvh9jbowxsEX9bxN8G82+2iL8t4m+L+Nsi/ra4/L072YSrUi/hm+/EoeEEk++v3u6X
Sba8JMosVF78HVcO2eSfpy7dLkxCSfLJdBh/2RrX+I/V/1kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3SLhp628BJ5SfuJP
Z/nexlASSpJPAo8/XlwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwICpyemtCxODSSpJPgk83v5/h4hTe34jP2IAAAAASUVO
RK5CYII=
"""


if __name__ == "__main__":
    main()