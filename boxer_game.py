#!/usr/bin/env python3
"""
BOXER - a tiny retro boxing game.

Starts in BAG mode (free practice on a heavy bag). Next to the BOXING GYM sign:
    SPAR      (or TAB)  three rounds against a sparring partner (a different fighting style each time)
    CAMPAIGN  (or C)    a boxing career, different every time: pick your fights from the offers on
                        the table, choose what to work on in camp, climb from club shows to a world
                        title - and make the calls the story puts in front of you
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
    Z                  lead hook - short and heavy; it comes ROUND, so a side-step won't beat it
    V                  rear uppercut - shortest of all; splits a high guard, catches a man slipping
                       (miss with a hook or an uppercut and you're off balance for a moment)
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

Rounds, the corner, the cards (v11)
    * Fights go rounds (3 to 6, by how big the fight is). Between rounds you sit on the stool: wind
      back, head cleared, cuts worked on - and your corner tells you what they saw. ENTER: seconds out.
    * Three judges score every round 10-9 (10-8 with a knockdown; 10-10 if they can't split it). Go
      the distance and it's their cards: unanimous, split or majority. Some judges can be bought...
    * Big clean shots can open a CUT. It bleeds, it gets worse, and the ringside doctor will stop it.
    * Every opponent has a STYLE - out-boxer, pressure fighter, slugger, counter-puncher, volume
      puncher, peek-a-boo, spoiler, body snatcher, brawler, boxer-puncher - and fights like it.
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
ROUND_TIME = 60               # seconds in a round (campaign); sparring rounds are shorter
SPAR_ROUND_TIME = 45
SPAR_ROUNDS = 3
CORNER_TIME = 14.0           # the minute between rounds (press ENTER to get on with it)
CORNER_HEAL = 0.08           # share of max health a good corner gets back for you
CORNER_WIND = 34             # wind back on the stool
CORNER_DAZE = 40             # smelling salts
KD_POINTS = 30               # a knockdown outweighs a round's worth of jabs on the cards
JUDGE_NOISE = 2.6            # judges are human
JUDGE_EVEN = 1.6             # this close and a judge scores it 10-10
CUT_OPEN = 0.025             # chance a big clean head shot opens a cut...
CUT_OPEN_CRIT = 0.07         # ...or a critical one
CUT_GROW = 0.3               # cut severity added per point of damage once it's open
CUT_STOP = 100               # the ringside doctor stops it here...
CUT_CHECK = 84               # ...or at the end of a round if the corner can't get it under this
DMG_SCALE = 0.42             # rounds are long: punches do less, fights go the distance more often
HURT = {"head": 12, "body": 11}   # how far in front of the hips the head / body can be hit
TARGET_Y = {"head": 30, "body": 46}

# ============================================================ knockdowns / knockouts
# A clean punch's IMPACT starts from its power and is multiplied by everything that made it land
# hard (see Game.impact). Divided by the victim's chin, it's compared with these thresholds.
POWER = {"jab": 1.0, "cross": 2.0, "body_jab": 0.9, "body_cross": 2.0, "hook": 2.25, "uppercut": 2.4}
KD_IMPACT = 5.0              # from here a clean head shot can drop him (flash knockdown)
KO_IMPACT = 7.0              # from here it can switch the lights off (out cold, no count)
DAZE_HURT = 60               # daze meter: HURT (wobbling) from here...
DAZE_DROP = 100              # ...and down he goes from here
DAZE_DECAY = 13.0            # daze lost per second once he's had a breather...
DAZE_SCALE = 0.5             # (rounds are long: the head takes a little longer to scramble)
CUTS_IN_SPAR = True
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
GUARD_WALK = 0.45            # you can walk behind a high / low guard - slowly
ROPE_ZONE = 16               # within this of the ring edge you are ON THE ROPES
ROPE_IMPACT = 1.3            # punches land this much harder on a man pinned there
ROPE_SHOVE = 2.2             # extra push into the ropes

# ============================================================ stamina
# Every punch costs wind. Stand off and it comes back; throw non-stop and you GAS OUT:
# slower hands, weaker punches, a softer chin and a guard that drains faster.
STAM_MAX = 100
STAM_COST = {"jab": 5.0, "cross": 11.0, "body_jab": 5.5, "body_cross": 12.0, "hook": 12.5, "uppercut": 13.0,
             "slip": 3.5, "feint": 2.0}
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
    # the lead hook: short, slow, heavy - and it comes round, so stepping off the line won't beat it
    "hook": dict(frames=[55, 56, 57, 58, 59], ms=[100, 60, 140, 90, 100], active={57}, cancel=4,
                 lunge=[0, 2, 4, 5, 2], reach=7, dmg=24, kick=1.7, shake=3, stop=0.09,
                 target="head", spar_dmg=11, guard=28, stun=0.36, wide=True),
    # the rear uppercut: shortest of all, splits a high guard and catches a man slipping
    "uppercut": dict(frames=[60, 61, 62, 63, 64, 65], ms=[70, 90, 50, 130, 90, 100], active={63}, cancel=5,
                     lunge=[0, -1, 3, 7, 6, 2], reach=1, dmg=26, kick=1.8, shake=4, stop=0.1,
                     target="head", spar_dmg=12, guard=34, stun=0.42, splits=True),
    "slip": dict(frames=[8, 9, 10, 10, 9, 8], ms=[60, 60, 150, 100, 60, 70], active=set(),
                 cancel=3, lunge=[0, 0, -1, -1, 0, 0]),
}
PUNCHES = ("jab", "cross", "body_jab", "body_cross", "hook", "uppercut")
BIG_SHOTS = ("hook", "uppercut")   # miss with one of these and you're off balance
OFF_BALANCE = 0.3            # ...for this long
WIDE_LAT = 2.3               # a hook's arc catches a man this many times further off the line

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
    # (their 'gloves' colour the headband, so it matches the hair and reads as a hairline)
    "mia": dict(name="MIA", short="MIA", title="YOUR LITTLE SISTER", color=(255, 170, 200),
                look=dict(glove=(96, 54, 40), shorts=(200, 80, 130), skin=(240, 182, 136), hair=(96, 54, 40),
                          boots=(200, 80, 130))),
    "vince": dict(name="VINCE MARLOW", short="MARLOW", title="PROMOTER", color=(236, 206, 120),
                  look=dict(glove=(208, 208, 214), shorts=(30, 30, 40), skin=(236, 196, 160), hair=(208, 208, 214),
                            boots=(30, 30, 40))),
    "cutman": dict(name='GUS "THE CUTMAN" FERRO', short="GUS", title="MARLOW'S CUTMAN", color=(190, 200, 214),
                   look=dict(glove=(40, 40, 46), shorts=(60, 60, 70), skin=(214, 160, 120), hair="bald",
                             boots=(60, 60, 70))),
}
# a couple of the originals were written as come-back opponents; as regular opponents they say this
FIGHTERS["rios"].update(intro="They say you're on your way up. Good. I eat men who are on their way up.",
                        win="El Toro doesn't lose to tourists.",
                        lose="You had more than I thought... a lot more...")
FIGHTERS["joe"].update(intro="Took this on three days' notice. No hard feelings - I just need the purse.")

# ============================================================ the road to the title
# Every career is different: most rungs of the ladder are FIGHT OFFERS - pick one of the men on the card
# (drawn at random from that level of the sport), then pick what to work on in camp. A few rungs are
# the story's own fights. The story branches on the choices you make in its scenes.
#
#   kind   : debut / offer / story / belt / stay_busy / title
#   tiers  : which level(s) the offers come from        rounds : scheduled rounds
#   intro  : a STORY scene played before the opponent is decided (choices live here)
#   pre    : a STORY scene played right before the fight (default: your corner talks about the man)
#   won / lost : STORY scenes after it (default: generic lines)
#   skip_if: after the intro, skip this rung if the condition holds
#   hostile: condition under which the judges are bought (and by how much)
LADDER = [
    dict(kind="debut", tiers=(1,), act=1, rounds=3, bill="PRO DEBUT", pre="debut", won="debut_won"),
    dict(kind="offer", tiers=(1,), act=1, rounds=3, bill="CLUB SHOW"),
    dict(kind="offer", tiers=(1,), act=1, rounds=3, bill="CLUB SHOW", intro="marlow", skip_if="promoter=marlow"),
    dict(kind="story", opp="cruz", tiers=(2,), act=1, rounds=4, bill="MAIN EVENT", intro="press",
         pre="cruz_pre", won="cruz_won", lost="cruz_lost", hostile=("promoter=doc", -4.0), rival=True),
    dict(kind="offer", tiers=(2,), act=2, rounds=4, bill="RANKED BOUT", intro="act2"),
    dict(kind="offer", tiers=(2,), act=2, rounds=4, bill="RANKED BOUT", skip_if="promoter=marlow"),
    dict(kind="belt", tiers=(2,), act=2, rounds=5, bill="FOR THE STATE TITLE", intro="belt_intro",
         pre="belt_pre", won="belt_won", lost="belt_lost", hostile=("dive=refuse", -7.0)),
    dict(kind="offer", tiers=(3,), act=2, rounds=5, bill="NATIONAL RANKINGS"),
    dict(kind="story", opp="preacher", tiers=(3,), act=2, rounds=5, bill="RANKED BOUT",
         pre="preacher_pre", won="preacher_won", lost="preacher_lost"),
    dict(kind="offer", tiers=(3, 4), act=3, rounds=5, bill="TOP-TEN BOUT", intro="act3"),
    dict(kind="offer", tiers=(4,), act=3, rounds=6, bill="TITLE ELIMINATOR"),
    dict(kind="story", opp="cruz2", tiers=(4,), act=3, rounds=6, bill="FINAL ELIMINATOR", pre="cruz2_pre",
         won="cruz2_won", lost="cruz2_lost", rival=True),
    dict(kind="title", opp="reyes", tiers=(5,), act=3, rounds=6, bill="FOR THE WORLD TITLE", intro="doc_heart",
         pre="title_pre", title_fight=True),
]
STAY_BUSY = dict(kind="stay_busy", tiers=(4,), act=3, rounds=5, bill="STAY-BUSY FIGHT", pre="stay_busy_pre")
STORY_ONLY = ("cruz", "cruz2", "preacher", "reyes")
RANK_AFTER = {3: 30, 4: 24, 5: 20, 6: 15, 7: 11, 8: 8, 9: 5, 10: 3, 11: 1}
PURSE = {1: 600, 2: 2500, 3: 9000, 4: 30000, 5: 400000}
MAX_LOSSES = 3                  # three on the record and the commission pulls your licence
CAMP = (("ROADWORK", "wind", "WIND: tire slower, get your breath back faster"),
        ("HEAVY BAG", "power", "POWER: every punch lands heavier"),
        ("MITTS & SPEED BAG", "speed", "HAND SPEED: quicker hands, quicker feet"),
        ("HARD SPARRING", "chin", "CHIN: take the big one and stay standing"))
CAMP_MAX = 5
CAMP_GAIN = dict(power=0.035, speed=0.022, wind=0.07, chin=0.05)

GENERIC_PRE = [("corner", "{opp_name}. Out of {home}. {record_words}."),
               ("corner", "{blurb}"),
               ("corner", "{tip}")]
GENERIC_REPLY = ["Then that's what we do.", "Got it, Doc.", "Let's go to work.", "Heard you.",
                 "Jab, breathe, listen. I know."]
GENERIC_WON = [[("corner", "That's how you do it. Clean work."), ("you", "He hit harder than he looked.")],
               [("corner", "Won ugly, won pretty - it all goes on the record the same."), ("you", "I'll take ugly.")],
               [("corner", "{opp} won't forget that one in a hurry."), ("you", "Neither will my ribs.")],
               [("corner", "People are starting to call about you, kid. Real people."), ("you", "Tell 'em to call back.")],
               [("mia", "I made a sign this time. It said HIT HIM. Very sophisticated."),
                ("you", "I saw it. It helped.")]]
GENERIC_LOST = [[("corner", "He was better tonight. That's all that was."), ("you", "...Yeah.")],
                [("corner", "Shake it off. We learn, and we go again."), ("you", "I didn't see half of what he threw.")],
                [("corner", "Every fighter's got a night like this. The good ones only have a couple.")]]

STORY = dict(
    open=[("doc", "IRON JAW GYM. 5:40 AM. Same as every morning for four years."),
          ("doc", "You've beaten every sparring partner I can find in this city."),
          ("mia", "He means you're broke, you're twenty-four, and you hit things for free."),
          ("you", "Morning, Mia. Shouldn't you be at the diner?"),
          ("mia", "Double shift at seven. Came to see if my brother's finally turning pro or just turning grey."),
          ("doc", "Club show Friday. Four rounds of a minute - hardly a fight. Purse is six hundred dollars."),
          ("mia", "That's... actually a month of my tuition."),
          ("you", "...Where do I sign?")],
    debut=[("doc", "Your man Friday: {opp_name}. Out of {home}. {record_words}."),
           ("doc", "{blurb}"),
           ("doc", "Short rounds. Between them you SIT, you BREATHE, and you LISTEN to me."),
           ("you", "Sit. Breathe. Listen."),
           ("doc", "And for God's sake, jab.")],
    debut_won=[("doc", "That's a pro record now, kid. One and oh."),
               ("mia", "I screamed so loud the guy next to me changed seats."),
               ("you", "Felt like it took an hour."),
               ("doc", "It didn't. You'll learn the difference.")],
    marlow=[("doc", "We've got company. Don't sign anything. Don't say anything."),
            ("vince", "Vince Marlow. Marlow Promotions. You've seen my posters - you're standing under one."),
            ("vince", "I'm building a card around a kid called Dante Cruz. Seventeen and oh. The golden boy."),
            ("vince", "Golden boys need dance partners. Sign with me and you skip the church basements."),
            ("doc", "And if he doesn't?"),
            ("vince", "Then he fights in church basements till he's thirty, Doc. Like you did."),
            ("choice", "promoter", "Marlow's contract is on the table.",
             [("SIGN WITH MARLOW", "marlow", "Bigger fights, sooner. His rules."),
              ("STAY WITH DOC", "doc", "The long way round. Your own man.")]),
            ("?", "promoter=marlow", [
                ("you", "Where do I sign?"),
                ("vince", "Smart kid. Doc - you can still carry the bucket."),
                ("doc", "...I'll carry it."),
                ("mia", "Did my brother just get a manager AND a promoter in one afternoon?"),
                ("doc", "He got a promoter. I'm still the manager. Whatever that man says.")]),
            ("?", "promoter=doc", [
                ("you", "I've got a manager, Mr. Marlow. He's standing right there."),
                ("vince", "Loyalty. Cute. I'll remember it."),
                ("doc", "That man just put us on a list, kid. Good. I've been on worse lists."),
                ("mia", "Is it bad that I kind of want to egg his car?")])],
    press=[("doc", "Well. It happened. They offered us Dante 'Sugar' Cruz. Seventeen and oh."),
           ("?", "promoter=marlow", [
               ("vince", "Main event. My golden boy versus my other boy. Everybody wins. Mostly me."),
               ("doc", "He's selling you as the opponent, kid. The name on Cruz's record.")]),
           ("?", "promoter=doc", [
               ("doc", "Marlow's show. Marlow's fighter. Marlow's judges."),
               ("doc", "We do NOT win a close decision in that building. You hear me? You win it clear, or you win it early.")]),
           ("doc", "Press conference is tomorrow. Cameras, microphones, Cruz at the next table."),
           ("cruz", "So you're the guy. Nice to meet you. Shame about Friday."),
           ("choice", "press", "The microphones are on.",
            [("SHOW HIM RESPECT", "respect", "Keep it classy. He'll stay cool and sharp."),
             ("GET UNDER HIS SKIN", "trash", "He'll come out angry - harder, but reckless.")]),
           ("?", "press=respect", [
               ("you", "He's earned his record. I'm here to earn mine. See you Friday."),
               ("cruz", "...Classy. Doesn't change anything."),
               ("doc", "Good. Let him underestimate you in peace.")]),
           ("?", "press=trash", [
               ("you", "Seventeen and oh against cab drivers and accountants. Friday you meet a fighter."),
               ("cruz", "You're DEAD Friday. You hear me? DEAD."),
               ("mia", "Okay, that was kind of amazing."),
               ("doc", "That was stupid. ...Effective. But stupid. He's going to come out swinging.")])],
    cruz_pre=[("doc", "{rounds} rounds. Main event. People are actually paying to see this."),
              ("?", "press=trash", [("doc", "He's angry. Angry men reach. Make him miss and make him pay.")]),
              ("?", "press=respect", [("doc", "He's fast and he's smart. Don't chase - make him come to you.")]),
              ("you", "Doc... what if he's just better?"),
              ("doc", "Then he'll have to prove it for {rounds} rounds. Nobody's ever made him do that.")],
    cruz_won=[("doc", "You just took an unbeaten man's zero. Do you understand what you did?"),
              ("you", "I think I'm going to be sick."),
              ("?", "promoter=marlow", [("vince", "Well, well. Plans change. I'm a flexible man.")]),
              ("?", "promoter=doc", [("doc", "On Marlow's show. With Marlow's judges. Ha!")]),
              ("doc", "Be sick in the car. There's promoters outside and they ALL want you now.")],
    cruz_lost=[("doc", "He was better tonight. That's all that was."),
               ("you", "He didn't even look tired, Doc."),
               ("doc", "He will. Guys like that burn bright. We'll see him again - and we'll be ready.")],
    act2=[("doc", "Act two, kid. The rankings. Every man from here on can fight."),
          ("mia", "So the scary part was the EASY part?"),
          ("doc", "The scary part was the cheap part. Now it gets expensive.")],
    belt_intro=[("?", "promoter=marlow", [
                    ("vince", "Sit down, kid. I've got a business proposition."),
                    ("vince", "The state title. The champion's my fighter now, too. And he's going places."),
                    ("vince", "Bigger places than you. So: round four, you go down, you stay down. Twenty grand, cash."),
                    ("you", "And if I say no?"),
                    ("vince", "Then you'd better knock him out. Because you won't win a single round on my judges' cards."),
                    ("choice", "dive", "Twenty thousand dollars. Mia's tuition, all of it.",
                     [("TAKE THE MONEY", "take", "Nobody ever has to know."),
                      ("TELL HIM NO", "refuse", "The judges will be his. Win it early.")]),
                    ("?", "dive=take", [("you", "...Round four."),
                                        ("vince", "Attaboy. Pleasure doing business."),
                                        ("doc", "Somebody's been talking to you. I can see it on your face."),
                                        ("you", "It's handled, Doc.")]),
                    ("?", "dive=refuse", [("you", "Find another dance partner, Vince. I'm done with you."),
                                          ("vince", "Then good luck with the judges, kid. Wear something nice."),
                                          ("doc", "...I heard. All of it. I've never been prouder of a fighter in my life."),
                                          ("doc", "Now we have to knock this man out.")])]),
                ("?", "promoter=doc", [
                    ("mia", "So the school called. If the tuition's not paid by the first, I'm out."),
                    ("doc", "There's a short-notice offer. A ranked guy lost his opponent. Real money, no camp."),
                    ("doc", "Ten days isn't a camp, kid. It's a prayer. And it's a much better fighter."),
                    ("choice", "notice", "The state title can wait - or you can take the money fight.",
                     [("TAKE THE SHORT-NOTICE FIGHT", "take", "A tougher man and no camp. Purse covers the tuition."),
                      ("STAY ON SCHEDULE", "wait", "Mia finds the money somehow. You fight for the belt.")]),
                    ("?", "notice=take", [("you", "Call them back. Tell them yes."),
                                          ("mia", "...You absolute idiot. Thank you."),
                                          ("doc", "Ten days. Roadwork twice a day. God help us.")]),
                    ("?", "notice=wait", [("mia", "I'll pick up more shifts. Don't you DARE take a fight for me."),
                                          ("you", "Mia..."),
                                          ("mia", "I mean it. Go win your belt.")])])],
    belt_pre=[("?", "notice=take", [("doc", "Short notice, so no title tonight - just a ranked man and a big check."),
                                    ("doc", "{opp_name}. {record_words}. {blurb}")]),
              ("?", "!notice=take", [("doc", "The state title. {opp_name}, {record_words}. He's the champion for a reason."),
                                     ("doc", "{blurb}")]),
              ("doc", "{tip}"),
              ("?", "dive=take", [("vince", "Round four, kid. Don't forget."),
                                  ("you", "...")]),
              ("?", "dive=refuse", [("doc", "Three judges. All of them Marlow's. You don't leave it to them.")])],
    belt_won=[("?", "dive=take", [("?", "!doc_gone", [
                  ("vince", "You just cost me a LOT of money, kid."),
                  ("you", "Keep your twenty grand, Vince. I was never going down."),
                  ("vince", "You'll never fight in this state again. Every man I put in front of you from now on - you'll see."),
                  ("doc", "Then we'll fight in another state. Come on, kid. We're leaving."),
                  ("set", "blacklisted")]),
                                    ("?", "doc_gone", [
                  ("vince", "Rematch money. Everybody gets paid twice. You're learning how this works, kid."),
                  ("you", "I'm not your kid, Vince.")])]),
              ("?", "dive=refuse", [
                  ("vince", "...Get out of my sight."),
                  ("doc", "Free agents, kid. Best night of my year."),
                  ("set", "free")]),
              ("?", "notice=take", [
                  ("mia", "The tuition's paid. All of it. I'm going to cry in this cheap hot dog."),
                  ("doc", "That man was ranked and you took him on ten days' notice. People will notice that.")]),
              ("?", "!notice=take", [
                  ("?", "!dive=take", [("doc", "State champion. Say it out loud. Go on."),
                                       ("you", "State champion."),
                                       ("doc", "Sounds good on you, kid.")])])],
    belt_lost=[("?", "dive=take", [("?", "!doc_gone", [
                   ("vince", "Pleasure doing business. Your envelope's in the car."),
                   ("doc", "I saw it. Round four. I've seen a hundred men lie down - I know what it looks like."),
                   ("you", "Doc, it's Mia's tuition, I didn't have a choice -"),
                   ("doc", "Everybody's got a choice. That's the whole point of them. Find yourself another trainer."),
                   ("set", "doc_gone")])]),
               ("?", "doc_gone", [("cutman", "He's the champ for a reason. Let's go, I got another fight tomorrow.")]),
               ("?", "!dive=take", [("doc", "He was the champion for a reason. We go back to work.")])],
    preacher_pre=[("?", "doc_gone", [
                      ("cutman", "Gus Ferro. Marlow sends me. I close cuts, I don't do speeches."),
                      ("you", "...Great."),
                      ("preacher", "Where's Doc Hayes? Forty years I've never seen him miss a fight.")]),
                  ("?", "!doc_gone", [
                      ("doc", "Eli Boone. We came up together. He's forty-one and he's still here."),
                      ("you", "You don't sound happy about this one."),
                      ("doc", "He's the best man I ever knew in a ring. And he never got a title shot."),
                      ("doc", "Beat him. He'd be insulted by anything less.")]),
                  ("doc", "{tip}")],
    preacher_won=[("?", "doc_gone", [
                      ("preacher", "You fight like Doc Hayes taught you. Every bit of it."),
                      ("preacher", "Go see him. Tell him Eli says he's a stubborn old fool."),
                      ("doc", "...Eli called me. Said you fought like somebody I'd be proud of."),
                      ("you", "I'm sorry, Doc. About all of it."),
                      ("doc", "I know you are. Gym's open at 5:40. Don't be late."),
                      ("unset", "doc_gone")]),
                  ("?", "!doc_gone", [
                      ("doc", "He hugged you at the end. You know he's never done that?"),
                      ("you", "He told me to go get the thing he never got."),
                      ("doc", "...Yeah. That's Eli.")])],
    preacher_lost=[("preacher", "Patience, son. You'll learn it. Everybody does, eventually."),
                   ("?", "doc_gone", [
                       ("preacher", "And go make it right with Doc. Whatever you did, he'll take you back. He always does."),
                       ("doc", "...Eli called. Gym's open at 5:40, kid. Don't make me regret it."),
                       ("unset", "doc_gone")])],
    act3=[("doc", "Top ten, kid. From here on in, everybody you fight has fought for a belt or is about to."),
          ("?", "blacklisted", [("doc", "And Marlow's matchmaker is putting the meanest man he can find in every slot. Expect it.")]),
          ("mia", "I graduated, by the way. In case anybody in this gym reads the paper."),
          ("you", "MIA."),
          ("mia", "Nurse. Real one. So when you get hurt now, I'm legally allowed to say I told you so.")],
    cruz2_pre=[("doc", "Guess who the sanctioning body put in front of us. One last time."),
               ("cruz", "I've thought about you every day since. Every single one."),
               ("?", "press=trash", [("cruz", "Cab drivers and accountants, right? Let's see what you say now.")]),
               ("?", "press=respect", [("cruz", "You were decent to me when you didn't have to be. Doesn't mean I'll go easy.")]),
               ("doc", "He's not a golden boy any more, kid. He's dangerous now. Winner fights for the world title.")],
    cruz2_won=[("cruz", "Go get him, man. Go take that belt. You earned it twice."),
               ("doc", "He meant that. Every word."),
               ("you", "Four years ago he wouldn't look at me at a weigh-in."),
               ("doc", "Four years ago you were nobody. Look at you now.")],
    cruz2_lost=[("cruz", "Told you. The first one wasn't the fluke - YOU were."),
                ("doc", "He wanted it more tonight. That's an ugly sentence and it's the true one."),
                ("doc", "Gym. Tomorrow. 5:40.")],
    doc_heart=[("mia", "Pick up. PICK UP. ...It's Doc. He collapsed at the gym. I'm at St. Vincent's."),
               ("doc", "Don't look at me like that. I've been hit harder by a bus."),
               ("mia", "It's his heart. They want him in this bed for six weeks. The title fight's in three."),
               ("doc", "Victor Reyes doesn't wait for anybody, kid. If you pull out, the shot goes to someone else."),
               ("choice", "heart", "The title shot, or Doc in your corner.",
                [("FIGHT ON SCHEDULE", "fight", "Eli Boone works your corner. Doc listens on the radio."),
                 ("POSTPONE THE TITLE", "wait", "One more fight to stay sharp. Doc gets back on his feet.")]),
               ("?", "heart=fight", [("doc", "Eli's going to work your corner. Listen to him like you'd listen to me."),
                                     ("doc", "More, maybe. He's smarter than me. Don't tell him I said that."),
                                     ("preacher", "I've waited my whole life to be in a title fight. Never thought it'd be on the stool.")]),
               ("?", "heart=wait", [("you", "There'll be other title shots, Doc. There's only one of you."),
                                    ("doc", "...You sentimental idiot. Fine. Stay busy. Don't get hurt."),
                                    ("do", "postpone")])],
    stay_busy_pre=[("doc", "Look at me. Upright. Walking. The doctors hate it."),
                   ("doc", "Reyes' people are telling every reporter you ducked him. This one shuts them up."),
                   ("doc", "{opp_name}. {record_words}. {blurb}"),
                   ("doc", "{tip}")],
    title_pre=[("?", "heart=fight", [
                   ("preacher", "Doc's on the radio in his hospital bed. The nurses say he's driving them crazy."),
                   ("preacher", "Victor Reyes. Forty fights, forty knockouts. Never heard a final bell."),
                   ("preacher", "I fought men like him for twenty years. Make him think. Make him reach. He hates both.")]),
               ("?", "!heart=fight", [
                   ("doc", "Forty fights. Forty knockouts. Victor Reyes has never heard a final bell."),
                   ("doc", "Kid... whatever happens tonight, I want you to know something."),
                   ("you", "Doc, don't do a speech."),
                   ("doc", "I waited thirty years for a fighter like you. Go on. Go get it.")]),
               ("mia", "I'm ringside. With a first aid kit. Just so you know.")],
    rebuilt=[("corner", "That's the one. Looked like you again out there."),
             ("you", "Can we get the big one back?"),
             ("corner", "Already made the call. They're giving you the rematch.")],
    setback=[("corner", "Sit down. Ice on that. Listen to me."),
             ("corner", "You're not the first good fighter to get beat, and you won't be the last."),
             ("corner", "But a loss on the record means we go the long way round now. Tune-up fight, then the rematch.")],
    last_chance=[("corner", "Two losses, kid. Two."),
                 ("corner", "One more and the commission pulls your licence for the year."),
                 ("you", "Then I don't lose again."),
                 ("corner", "No. You don't.")],
    title_lost=[("doc", "Nobody has ever taken Victor Reyes that far. Nobody."),
                ("you", "I didn't come for a moral victory, Doc."),
                ("doc", "I know. But the whole world just watched you MAKE him work."),
                ("doc", "They want it again. Win your tune-up and you get the rematch.")],
    retire=[("doc", "Commission pulled the licence this morning. Twelve months minimum."),
            ("you", "Twelve months."),
            ("?", "dive=take", [("you", "I took his money, Doc. Once. I think about it every day."),
                                ("doc", "I know. So do I. But you came back and you fought honest after. That counts.")]),
            ("doc", "You had it, kid. On your night, you had it as much as any of them."),
            ("mia", "Hey. You paid for half a nursing degree with your face. That's not nothing."),
            ("doc", "Come work the corner with me. Teach some other punk what it cost you."),
            ("you", "...Yeah. Yeah, okay, Doc."),
            ("doc", "Lights off when you leave. You know where the key goes.")],
    yacht=[("?", "losses=0", [
               ("doc", "Forty-one fights I worked corners. Never once been on a boat."),
               ("you", "You've never even been in the ocean, Doc."),
               ("doc", "I've been in the ocean. There was a bucket of ice involved and you were bleeding."),
               ("doc", "Not one loss. You went through that entire division and not ONE man beat you."),
               ("you", "Somebody would have, eventually. Everybody gets got."),
               ("doc", "Maybe. But not yet, champ.")]),
           ("?", "losses>0", [
               ("doc", "You know what I keep thinking about? Not the belt."),
               ("you", "No?"),
               ("doc", "The night you lost and you sat on that bench and you couldn't look at me."),
               ("doc", "Everybody remembers the wins, kid. I remember you coming back at 5:40 the next morning."),
               ("you", "Where else was I gonna go?"),
               ("doc", "A thousand guys would've gone anywhere else. That's the whole story. That right there.")]),
           ("?", "heart=fight", [("doc", "And Eli. Eli Boone in a world title corner. He called me crying, you know."),
                                 ("you", "He told me you'd say that. He said to tell you it was allergies.")]),
           ("?", "dive=take", [("you", "Doc... the envelope. The fourth round."),
                               ("doc", "Kid. You came back. Champions aren't the ones who never fell. Leave it in the water.")]),
           ("?", "blacklisted", [("doc", "Heard Marlow sold his company. Nobody would fight his guys after what you did to 'em.")]),
           ("?", "press=trash", [("doc", "Dante called. Says congratulations - and that you still talk too much.")]),
           ("?", "press=respect", [("doc", "Dante called. Says congratulations, and he wants the first defence.")]),
           ("mia", "Okay, champ. The nurse says sunscreen. Both of you. NOW."),
           ("you", "...Hey, Doc?"),
           ("doc", "Mm."),
           ("you", "Thanks for the 5:40s."),
           ("doc", "Thanks for showing up to 'em.")],
)

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


# ============================================================ fighting styles
# Every boxer has a style. It shapes how he moves (how close he wants to be, whether he circles or
# walks you down and cuts off the ring), what he throws (and in what combinations), how he defends,
# whether he leans on you in clinches - and his build. Your corner knows each one's weakness.
STYLES = {
    "outboxer": dict(name="OUT-BOXER", blurb="Long jab, quick feet. Wants you on the end of his punches.",
                     tip="Cut the ring off. Step where he's GOING, not where he is.",
                     ai=dict(react=0.06, slip=0.05, step=0.12, parry=0.03, combo=-0.05, punish=0.05,
                             guard_up=-0.05, feint=0.05, atk_x=1.0, range=6, circle=1.8, cut=0.15, retreat=0.6),
                     stats=dict(speed=0.05, walk=0.18, power=-0.06, wind=0.15, chin=-0.04),
                     weights=dict(jab=3.2, cross=1.4, body_jab=1.0, body_cross=0.5, hook=0.4, uppercut=0.15),
                     combos=[["jab", "jab"], ["jab", "cross"], ["jab", "jab", "cross"], ["jab", "body_jab"],
                             ["jab", "cross", "jab"]],
                     reply="Run all you like. The ring's only so big.",
                     win=["You never laid a glove on me. Not really.", "Footwork, kid. Look it up."],
                     lose=["I ran out of ring...", "How did you keep FINDING me?"]),
    "swarmer": dict(name="PRESSURE FIGHTER", blurb="Walks you down, smothers you, lives on the inside.",
                    tip="He wants a phone booth. Pivot off and keep him on the end of the jab.",
                    ai=dict(react=-0.06, slip=-0.05, step=-0.05, combo=0.2, flurry=0.2, guard_up=-0.05,
                            atk_x=0.72, range=-16, circle=0.4, cut=1.0, retreat=0.05, pin=2.2),
                    stats=dict(wind=0.3, walk=0.05, chin=0.08, power=-0.02),
                    weights=dict(jab=1.0, cross=1.0, body_jab=1.8, body_cross=1.6, hook=2.2, uppercut=1.2),
                    combos=[["body_jab", "hook"], ["jab", "hook", "cross"], ["hook", "body_cross", "hook"],
                            ["body_jab", "body_cross", "hook"], ["uppercut", "hook"],
                            ["jab", "cross", "hook", "body_cross"]],
                    reply="Come forward, then. I'll have something waiting.",
                    win=["Told you. No room to breathe in there.", "Everywhere you went, I was already there."],
                    lose=["I kept coming... why wouldn't you STOP?", "Never... got inside..."]),
    "slugger": dict(name="SLUGGER", blurb="Slow feet, heavy hands. One clean shot is all he needs.",
                    tip="He loads up on every shot. See it coming, slip it, make him pay.",
                    ai=dict(react=-0.12, slip=-0.1, parry=-0.12, step=-0.08, combo=-0.1, punish=0.1,
                            atk_x=1.3, range=-6, circle=0.25, cut=0.6, retreat=0.15),
                    stats=dict(power=0.16, speed=-0.07, walk=-0.15, chin=0.12, wind=-0.15, hp=14),
                    weights=dict(jab=0.7, cross=2.6, body_jab=0.5, body_cross=1.6, hook=2.4, uppercut=1.4),
                    combos=[["cross", "hook"], ["hook", "hook"], ["jab", "cross", "hook"], ["body_cross", "uppercut"]],
                    reply="You've got to hit me first.",
                    win=["One clean shot. That's all it ever takes.", "Lights out. Sweet dreams, kid."],
                    lose=["Couldn't... land the big one...", "Heavy hands don't count... if they don't land..."]),
    "counter": dict(name="COUNTER-PUNCHER", blurb="Rarely leads. Every punch you miss, he answers sharper.",
                    tip="He's waiting on you. Feint - make him bite - THEN throw.",
                    ai=dict(react=0.08, slip=0.12, parry=0.12, punish=0.3, combo=-0.05, feint=0.08,
                            atk_x=1.7, range=2, circle=1.0, cut=0.3, retreat=0.4),
                    stats=dict(speed=0.05, power=0.02, chin=-0.02),
                    weights=dict(jab=1.6, cross=2.2, body_jab=0.8, body_cross=1.0, hook=1.4, uppercut=1.0),
                    combos=[["cross", "hook"], ["jab", "cross"], ["uppercut", "cross"], ["hook", "cross"]],
                    reply="Then I'll make you lead for once.",
                    win=["Every mistake you made, I was waiting for it.", "You kept giving me openings. I only needed one."],
                    lose=["You stopped making mistakes. Nobody stops...", "You never... gave me anything..."]),
    "volume": dict(name="VOLUME PUNCHER", blurb="Never stops throwing. Not much on each one - but so many.",
                   tip="Pick your spots. He throws a lot, but none of it's heavy. Make every one cost him.",
                   ai=dict(react=-0.02, combo=0.3, flurry=0.15, atk_x=0.55, range=-6, circle=1.0, cut=0.6,
                           retreat=0.2),
                   stats=dict(wind=0.4, power=-0.12, speed=0.06),
                   weights=dict(jab=2.6, cross=1.2, body_jab=2.0, body_cross=1.0, hook=1.2, uppercut=0.5),
                   combos=[["jab", "jab", "cross", "hook"], ["body_jab", "body_jab", "hook"], ["jab", "cross", "jab", "cross"],
                           ["jab", "body_jab", "jab", "cross", "hook"]],
                   reply="Quantity isn't quality, pal.",
                   win=["A hundred punches a round. You can't block 'em all.", "Busy hands win fights."],
                   lose=["Arms... like lead...", "Threw everything... and you just... stood there..."]),
    "peekaboo": dict(name="PEEK-A-BOO", blurb="Gloves glued to his face, bobbing in - then hooks and uppercuts.",
                     tip="He's hiding behind the gloves. Go downstairs, and go AROUND them with the hook.",
                     ai=dict(react=0.04, slip=0.2, guard_up=0.45, combo=0.15, atk_x=0.9, range=-14, circle=0.9,
                             cut=0.8, retreat=0.05, shell=1),
                     stats=dict(power=0.08, chin=0.06, walk=0.05),
                     weights=dict(jab=0.7, cross=1.0, body_jab=1.0, body_cross=1.4, hook=2.6, uppercut=2.2),
                     combos=[["hook", "uppercut"], ["body_cross", "hook"], ["uppercut", "hook", "cross"],
                             ["hook", "body_cross", "hook"]],
                     reply="I'll find a way round the gloves.",
                     win=["Couldn't find me behind the gloves, could you?", "Peek-a-boo. I see you."],
                     lose=["You went around the guard... smart...", "Nowhere left to hide..."]),
    "spoiler": dict(name="SPOILER", blurb="Jab, grab, hold. Ugly, awkward, kills your rhythm.",
                    tip="He's holding to kill your rhythm. Punch your way out of the clinch, don't wait for the ref.",
                    ai=dict(react=0.04, combo=-0.1, atk_x=1.15, range=0, circle=1.2, cut=0.3, retreat=0.5,
                            clinchy=0.9),
                    stats=dict(wind=0.1, power=-0.05, hp=6),
                    weights=dict(jab=3.0, cross=1.2, body_jab=1.0, body_cross=0.6, hook=0.6, uppercut=0.3),
                    combos=[["jab", "jab"], ["jab", "cross"]],
                    reply="Hold on all you want. I'll punch my way out.",
                    win=["Ugly? Sure. Ugly wins.", "Pretty boxing don't pay the rent."],
                    lose=["Ref wouldn't let me hold... not fair...", "Couldn't... tie you up..."]),
    "body": dict(name="BODY SNATCHER", blurb="Goes downstairs all night. Breaks you down from the ribs up.",
                 tip="Elbows in, kid. He lives on your ribs - make him pay every time he dips.",
                 ai=dict(combo=0.1, flurry=0.1, atk_x=0.9, range=-8, cut=0.7, circle=0.7, retreat=0.2),
                 stats=dict(power=0.05, wind=0.12),
                 weights=dict(jab=0.8, cross=0.8, body_jab=3.0, body_cross=2.8, hook=1.2, uppercut=1.0),
                 combos=[["body_jab", "body_cross"], ["jab", "body_cross", "hook"], ["body_jab", "body_jab", "uppercut"],
                         ["hook", "body_cross"]],
                 reply="Elbows in. Come on then.",
                 win=["Breathe in. Hurts, don't it?", "Kill the body and the head dies. Every time."],
                 lose=["Never got to the ribs... you kept me off...", "Couldn't... find the body..."]),
    "brawler": dict(name="BRAWLER", blurb="Wild, brave, reckless. Swings from the floor and takes three to give one.",
                    tip="He's wild. Stay compact, stay calm - catch him with the uppercut when he lunges in.",
                    ai=dict(react=-0.15, slip=-0.1, parry=-0.15, combo=0.15, flurry=0.3, guard_up=-0.1,
                            atk_x=0.75, range=-10, circle=0.3, cut=0.8, retreat=0.05),
                    stats=dict(power=0.1, chin=0.15, wind=-0.1, hp=8, speed=-0.02),
                    weights=dict(jab=0.8, cross=2.2, body_jab=0.8, body_cross=1.6, hook=2.4, uppercut=1.8),
                    combos=[["hook", "cross", "hook"], ["cross", "uppercut"], ["hook", "hook", "cross"],
                            ["uppercut", "hook", "cross"]],
                    reply="I'm a boxer. Watch and learn.",
                    win=["THAT'S what a fight looks like!", "Ha! Somebody get this guy a stretcher!"],
                    lose=["Ha... good scrap. Good scrap.", "Whoo... I'll feel that tomorrow..."]),
    "boxer_puncher": dict(name="BOXER-PUNCHER", blurb="Does everything well. No obvious hole to aim at.",
                          tip="He's good at everything. Win the jab and the rest will follow.",
                          ai=dict(react=0.04, parry=0.04, combo=0.05, feint=0.04, atk_x=0.95, range=0, circle=1.0,
                                  cut=0.6, retreat=0.3),
                          stats=dict(power=0.04, speed=0.03, wind=0.08),
                          weights=dict(jab=2.0, cross=1.8, body_jab=1.2, body_cross=1.2, hook=1.4, uppercut=0.8),
                          combos=[["jab", "cross", "hook"], ["jab", "body_cross"], ["jab", "jab", "cross"],
                                  ["cross", "hook", "cross"], ["jab", "uppercut", "cross"]],
                          reply="Then let's see who's better.",
                          win=["Did everything right. You just ran into better.", "Good fight. Wrong night for you."],
                          lose=["Well fought. You earned that.", "Better man tonight. No excuses."]),
}
STURDY = dict(swarmer=0.55, peekaboo=0.55, brawler=0.45, slugger=0.5, body=0.4, volume=0.25)
FORCE_SPAR_STYLE = None      # (tests) always spar this style
SPAR_STYLE_STATS = True      # sparring partners get their style's build (not its health: 100 for everyone)
STYLE_ORDER = ("outboxer", "swarmer", "slugger", "counter", "volume", "peekaboo", "spoiler", "body", "brawler",
               "boxer_puncher")
TIER_NAMES = {1: "CLUB FIGHTER", 2: "REGIONAL", 3: "NATIONALLY RANKED", 4: "WORLD CONTENDER", 5: "WORLD CHAMPION"}
TIER_SKILL = {1: 0.08, 2: 0.33, 3: 0.58, 4: 0.82, 5: 1.0}

# hair / skin shorthands for the roster
_PALE, _FAIR, _OLIVE, _TAN, _BROWN, _DARK, _DEEP = ((250, 206, 166), (240, 186, 140), (220, 160, 112),
                                                     (196, 132, 90), (164, 104, 70), (128, 82, 56), (100, 64, 46))
_BLACK, _BRN, _BLOND, _RED, _GREY, _DBRN = ((30, 24, 32), (90, 60, 40), (230, 196, 100), (190, 80, 40),
                                            (200, 200, 206), (60, 42, 34))

#  key, name, short, style, tier, from, (won, lost, ko), (glove, shorts, skin, hair, boots), taunt, intro
ROSTER = [
    # ---- tier 1: the club circuit
    ("kowalski", 'STAN "THE PLUMBER" KOWALSKI', "THE PLUMBER", "body", 1, "CLEVELAND", (9, 7, 4),
     ((90, 110, 150), (60, 64, 72), _PALE, _BRN, None), "roar",
     "Twenty years fixing pipes. You know what pipes and ribs got in common? They both crack."),
    ("ito", 'HIRO "LITTLE HAWK" ITO', "LITTLE HAWK", "outboxer", 1, "OSAKA", (6, 2, 1),
     ((240, 240, 246), (200, 40, 60), _FAIR, _BLACK, None), "weave",
     "I am small. I am fast. You will spend all night hitting where I was."),
    ("dawson", '"DYNAMITE" DEE DAWSON', "DYNAMITE DEE", "brawler", 1, "MEMPHIS", (8, 6, 7),
     ((250, 200, 40), (40, 40, 48), _DARK, "bald", (250, 200, 40)), "roar",
     "My mama named me Dee. The ring named me Dynamite. Guess which one's showing up tonight."),
    ("moreno", 'LUIS "EL GALLO" MORENO', "EL GALLO", "swarmer", 1, "TIJUANA", (7, 3, 5),
     ((200, 30, 40), (30, 120, 70), _TAN, _BLACK, (200, 30, 40)), "shadowbox",
     "The rooster crows at dawn. Tonight he crows over you."),
    ("becker", 'FINN "THE STUDENT" BECKER', "THE STUDENT", "counter", 1, "MUNICH", (5, 0, 1),
     ((40, 40, 50), (230, 230, 236), _PALE, _BLOND, None), "shadowbox",
     "Ninety amateur fights. I have studied men like you. I know what you will do."),
    ("sully", 'PATRICK "SULLY" O\'SULLIVAN', "SULLY", "volume", 1, "BOSTON", (10, 5, 3),
     ((40, 150, 70), (240, 240, 246), _PALE, _RED, (40, 150, 70)), "shadowbox",
     "I throw a hundred a round, pal. You're gonna get tired of blocking long before I get tired of punching."),
    ("grimes", 'EARL "GRAVEDIGGER" GRIMES', "GRAVEDIGGER", "spoiler", 1, "NEW ORLEANS", (14, 16, 5),
     ((60, 60, 60), (100, 40, 120), _DEEP, _GREY, (60, 60, 60)), "belt",
     "Thirty fights, son. I've buried better prospects than you. Ugly is a skill too."),
    ("nkosi", 'THABO "THE TOWER" NKOSI', "THE TOWER", "outboxer", 1, "JOHANNESBURG", (6, 1, 3),
     ((40, 90, 200), (250, 196, 40), _DEEP, "bald", (40, 90, 200)), "shadowbox",
     "Look up. Further. That is how far my jab has to come."),
    # the original first-night opponents
    ("rusty", None, None, "brawler", 1, "PITTSBURGH", (8, 11, 6), None, None, None),
    ("pike", None, None, "slugger", 1, "SCRANTON", (11, 6, 9), None, None, None),
    ("joe", None, None, "spoiler", 1, "BALTIMORE", (9, 9, 3), None, None, None),

    # ---- tier 2: regional
    ("vance", 'TYRELL "SILK" VANCE', "SILK VANCE", "outboxer", 2, "PHILADELPHIA", (13, 1, 5),
     ((250, 250, 250), (120, 60, 160), _BROWN, _BLACK, (250, 250, 250)), "weave",
     "They call me Silk 'cause nothing sticks. Not punches, not losses. Nothing."),
    ("petrov", 'IVAN "THE ANVIL" PETROV', "THE ANVIL", "spoiler", 2, "MURMANSK", (15, 4, 6),
     ((120, 124, 136), (180, 30, 40), _PALE, _BLOND, (120, 124, 136)), "roar",
     "Hit me. Go on. Anvils do not mind being hit."),
    ("okoye", 'SAMUEL "BIG SAM" OKOYE', "BIG SAM", "body", 2, "LAGOS", (14, 3, 10),
     ((40, 160, 80), (250, 250, 250), _DEEP, _BLACK, (40, 160, 80)), "roar",
     "I will take your breath away. And I will not give it back."),
    ("flores", 'MANNY "PEEKABOO" FLORES', "PEEKABOO", "peekaboo", 2, "SAN ANTONIO", (16, 2, 11),
     ((230, 90, 30), (40, 40, 50), _TAN, _BLACK, (230, 90, 30)), "weave",
     "You won't see me coming. You'll just feel it."),
    ("harlan", 'JESSE "THE COWBOY" HARLAN', "THE COWBOY", "brawler", 2, "AMARILLO", (17, 5, 14),
     ((150, 90, 50), (60, 90, 160), _FAIR, _BRN, (150, 90, 50)), "roar",
     "Back home we settle things with our hands. Ain't nothin' fancy about it."),
    ("chen", 'WEI "JADE" CHEN', "JADE CHEN", "volume", 2, "TAIPEI", (12, 2, 4),
     ((40, 170, 130), (240, 240, 246), _FAIR, _BLACK, (40, 170, 130)), "shadowbox",
     "Water wears down stone. One punch at a time. A thousand times."),
    ("lambert", 'ANDRE "THE PROFESSOR" LAMBERT', "THE PROFESSOR", "boxer_puncher", 2, "MONTREAL", (18, 3, 9),
     ((30, 50, 110), (220, 220, 230), _BROWN, _GREY, (30, 50, 110)), "belt",
     "Class is in session. Today's lesson is humility. There will be a test."),
    ("rios", None, None, "swarmer", 2, "SAN JUAN", (13, 8, 9), None, None, None),
    ("dunne", None, None, "counter", 2, "CHICAGO", (15, 3, 7), None, None, None),
    ("bulldozer", None, None, "slugger", 2, "TALLINN", (14, 4, 12), None, None, None),

    # ---- tier 3: nationally ranked
    ("duarte", 'RAFAEL "FURACAO" DUARTE', "FURACAO", "swarmer", 3, "RIO DE JANEIRO", (21, 2, 16),
     ((250, 210, 30), (30, 140, 60), _BROWN, _BLACK, (250, 210, 30)), "roar",
     "Furacao means hurricane. You don't fight a hurricane. You survive it. Or not."),
    ("mcbride", 'DECLAN "THE BUTCHER" McBRIDE', "THE BUTCHER", "brawler", 3, "BELFAST", (19, 4, 15),
     ((120, 20, 30), (240, 240, 246), _PALE, _RED, (120, 20, 30)), "roar",
     "My da was a butcher. Taught me where all the cuts are."),
    ("asante", 'KWAME "SPIDER" ASANTE', "SPIDER", "outboxer", 3, "ACCRA", (20, 2, 8),
     ((30, 30, 36), (250, 200, 40), _DEEP, "bald", (30, 30, 36)), "weave",
     "Long arms. Long reach. Long night - for you."),
    ("haas", 'DIETER "THE ENGINEER" HAAS', "THE ENGINEER", "spoiler", 3, "HAMBURG", (22, 4, 7),
     ((220, 220, 230), (30, 30, 36), _PALE, _GREY, (220, 220, 230)), "shadowbox",
     "I do not care about entertaining. I care about winning. These are different things."),
    ("santos", 'MIGUEL "MAGIC" SANTOS', "MAGIC SANTOS", "boxer_puncher", 3, "MANILA", (23, 2, 15),
     ((30, 70, 200), (220, 30, 40), _TAN, _BLACK, (30, 70, 200)), "weave",
     "Watch closely. You won't believe what happens next."),
    ("brooks", 'DARNELL "DOOMSDAY" BROOKS', "DOOMSDAY", "slugger", 3, "DETROIT", (18, 3, 17),
     ((20, 20, 24), (140, 20, 30), _DARK, "bald", (20, 20, 24)), "roar",
     "Seventeen wins by knockout. One left standing. He's still in a wheelchair."),
    ("yilmaz", 'EMRE "THE WOLF" YILMAZ', "THE WOLF", "peekaboo", 3, "ISTANBUL", (20, 1, 13),
     ((200, 30, 40), (240, 240, 246), _OLIVE, _BLACK, (200, 30, 40)), "weave",
     "The wolf stays low. The wolf waits. Then the wolf bites."),
    ("razor", None, None, "counter", 3, "YOKOHAMA", (20, 2, 9), None, None, None),
    ("lee", None, None, "volume", 3, "SEOUL", (19, 2, 7), None, None, None),
    ("sal", None, None, "body", 3, "NEWARK", (26, 5, 18), None, None, None),

    # ---- tier 4: world contenders
    ("kingston", 'ROMAN "THE KING" KINGSTON', "THE KING", "slugger", 4, "LONDON", (27, 1, 24),
     ((200, 160, 40), (100, 20, 40), _DARK, _BLACK, (200, 160, 40)), "belt",
     "Kneel. Everybody kneels eventually. I'm just saving you the wait."),
    ("takeda", 'RYO "SHADOW" TAKEDA', "SHADOW", "counter", 4, "TOKYO", (25, 1, 12),
     ((40, 40, 46), (40, 40, 46), _FAIR, _BLACK, (40, 40, 46)), "shadowbox",
     "You will throw. I will already be gone. And then I will not be."),
    ("odhiambo", 'JOMO "THE STORM" ODHIAMBO', "THE STORM", "swarmer", 4, "NAIROBI", (24, 2, 19),
     ((60, 130, 220), (250, 250, 250), _DEEP, "bald", (60, 130, 220)), "roar",
     "You can see a storm coming for miles. It doesn't help."),
    ("delarosa", 'ISAAC "EL ARTISTA" DE LA ROSA', "EL ARTISTA", "outboxer", 4, "MEXICO CITY", (28, 1, 13),
     ((250, 250, 250), (30, 130, 70), _TAN, _BLACK, (250, 250, 250)), "weave",
     "Some men fight. I paint. Tonight the canvas is you."),
    ("maddox", 'CLAY "MAD DOG" MADDOX', "MAD DOG", "brawler", 4, "TULSA", (26, 3, 23),
     ((230, 60, 30), (40, 40, 50), _FAIR, _BLOND, (230, 60, 30)), "roar",
     "They had to sedate me after my last fight. Not 'cause I was hurt. 'Cause I wasn't DONE."),
    ("novak", 'LUKA "THE WALL" NOVAK', "THE WALL", "peekaboo", 4, "ZAGREB", (26, 2, 14),
     ((200, 30, 40), (240, 240, 246), _PALE, _BRN, (200, 30, 40)), "belt",
     "Twenty-eight fights. Nobody has knocked me down. Nobody has even made me take a step back."),
    ("price", 'JULIAN "SHOWTIME" PRICE', "SHOWTIME", "volume", 4, "LAS VEGAS", (29, 2, 15),
     ((250, 200, 60), (20, 20, 30), _BROWN, _BLACK, (250, 200, 60)), "weave",
     "Lights. Cameras. Me. You're just here so the cameras have something to point at."),
    ("baptiste", 'FREDDIE "THE SURGEON" BAPTISTE', "THE SURGEON", "body", 4, "MIAMI", (27, 2, 18),
     ((240, 240, 246), (40, 120, 200), _DARK, _BLACK, (240, 240, 246)), "shadowbox",
     "Liver. Spleen. Floating rib. I know exactly where everything is. Hold still."),
    ("volkov", None, None, "boxer_puncher", 4, "NOVOSIBIRSK", (29, 1, 20), None, None, None),
    # the story's own fighters (never offered: they come to you)
    ("cruz", None, None, "boxer_puncher", 2, "LOS ANGELES", (17, 0, 12), None, None, None),
    ("cruz2", None, None, "boxer_puncher", 4, "LOS ANGELES", (24, 1, 17), None, None, None),
    ("preacher", None, None, "counter", 3, "ATLANTA", (38, 12, 22), None, None, None),
    ("reyes", None, None, "boxer_puncher", 5, "SAN DIEGO", (40, 0, 40), None, None, None),
]


def _style_lines(key, style):
    st = STYLES[style]
    k = sum(map(ord, key))
    return dict(reply=st["reply"], win=st["win"][k % len(st["win"])], lose=st["lose"][k % len(st["lose"])])


def build_roster():
    """Turn ROSTER into FIGHTERS entries (originals keep their hand-written lines and looks)."""
    for key, name, short, style, tier, home, rec, look, taunt, intro in ROSTER:
        f = FIGHTERS.setdefault(key, {})
        w, l, ko = rec
        f.setdefault("name", name)
        f.setdefault("short", short)
        f["fstyle"], f["tier"], f["home"], f["record"] = style, tier, home, (w, l, ko)
        if look is not None:
            glove, shorts, skin, hair, boots = look
            f["look"] = dict(glove=glove, shorts=shorts, skin=skin, hair=hair, boots=boots or shorts)
        f.setdefault("color", lighten(f["look"]["glove"], 0.35) if f.get("look") else (220, 220, 230))
        f.setdefault("taunt", taunt or "shadowbox")
        if intro:
            f.setdefault("intro", intro)
        for k, v in _style_lines(key, style).items():
            f.setdefault(k, v)
        if not f.get("champ"):
            f["title"] = "%s   -   %s   -   %d-%d (%d KO)" % (STYLES[style]["name"], home, w, l, ko)
        st = STYLES[style]["stats"]
        base = dict(hp=84 + 8 * tier, power=0.92 + 0.035 * tier, speed=0.95 + 0.025 * tier,
                    walk=0.95 + 0.04 * tier, chin=0.86 + 0.06 * tier, heart=0.82 + 0.12 * tier,
                    wind=0.74 + 0.1 * tier)
        for k in base:
            base[k] = base[k] + st.get(k, 0)
        if "hp" not in f or name is not None:     # new fighters get the generated build
            f.update(hp=int(base["hp"]), power=round(base["power"], 3), speed=round(base["speed"], 3),
                     walk=round(base["walk"], 3), chin=round(base["chin"], 3), heart=round(base["heart"], 3),
                     wind=round(base["wind"], 3))


def ai_profile(tier, style, extra=None, skill=0.0):
    """The computer's settings for a fighter: his tier sets how GOOD he is (EASY..HARD), his style
    sets how he fights. `extra` overrides anything (the story's special opponents)."""
    t = clamp(TIER_SKILL.get(int(round(tier)), 0.5) + skill, 0.0, 1.05)
    if not isinstance(tier, int):
        lo, hi = int(tier), int(tier) + 1
        t = clamp(TIER_SKILL.get(lo, 0.0) + (TIER_SKILL.get(hi, 1.0) - TIER_SKILL.get(lo, 0.0)) * (tier - lo) + skill,
                  0.0, 1.05)
    e, h = LEVELS["EASY"], LEVELS["HARD"]
    p = {}
    for k in h:
        a, b = e[k], h[k]
        if isinstance(a, tuple):
            p[k] = tuple(x + (y - x) * t for x, y in zip(a, b))
        else:
            p[k] = a + (b - a) * t
    st = STYLES[style]
    for k, v in st["ai"].items():
        if k == "atk_x":
            p["atk"] = (p["atk"][0] * v, p["atk"][1] * v)
        elif k in p and k not in ("atk", "delay"):
            p[k] = clamp(p[k] + v, 0.0, 0.95)
        else:
            p[k] = v
    p.setdefault("step", 0.05 + 0.12 * t)
    if extra:
        p.update(extra)
    return p


build_roster()


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
        return d if isinstance(d, dict) and d.get("v") == 2 and "idx" in d else None   # (old saves: start over)
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
    """A conversation: portrait, name, and typed-out dialogue - plus the story's little script language:
        ("?", condition, [entries])                 only if the condition holds (checked when reached)
        ("choice", key, prompt, [(label, value, note), ...])   you decide; stored in game.choices[key]
        ("set", flag) / ("unset", flag) / ("do", name)         story effects"""
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
        self.pick = 0
        self.settle()
        self.wrapped = self.wrap(0)

    def settle(self):
        """Expand conditions and run story actions until we reach something to show."""
        g = self.game
        while self.i < len(self.lines):
            e = self.lines[self.i]
            kind = e[0]
            if kind == "?":
                self.lines[self.i:self.i + 1] = list(e[2]) if g.cond(e[1]) else []
            elif kind == "set":
                g.flags.add(e[1])
                del self.lines[self.i]
            elif kind == "unset":
                g.flags.discard(e[1])
                del self.lines[self.i]
            elif kind == "do":
                getattr(g, "story_" + e[1])()
                del self.lines[self.i]
            else:
                break

    def choosing(self):
        return not self.done() and self.lines[self.i][0] == "choice"

    def options(self):
        return self.lines[self.i][3] if self.choosing() else []

    def move(self, d):
        if self.choosing():
            self.pick = (self.pick + d) % len(self.options())

    def wrap(self, i):
        if i >= len(self.lines):
            return []
        width = self.CARD.w - PORTRAIT_W - 22 if not self.choosing() else self.CARD.w - 20
        return wrap(self.game.font_s, self.text(i), width)

    def who(self):
        w = self.lines[self.i][0] if self.i < len(self.lines) else "doc"
        if w == "corner":                       # whoever is working your corner right now
            w = "cutman" if "doc_gone" in self.game.flags else "doc"
        return w

    def text(self, i=None):
        i = self.i if i is None else i
        if i >= len(self.lines):
            return ""
        e = self.lines[i]
        return self.game.fmt(e[2] if e[0] == "choice" else e[1])

    def shown(self):
        return min(len(self.text()), int(self.t * self.CPS))

    def typed(self):
        return self.shown() >= len(self.text())

    def done(self):
        return self.i >= len(self.lines)

    def advance(self):
        """Enter: finish typing this line, make the choice, or move to the next line."""
        if self.done():
            return
        if not self.typed():
            self.t = len(self.text()) / self.CPS
            return
        if self.choosing():
            e = self.lines[self.i]
            label, value = e[3][self.pick][0], e[3][self.pick][1]
            self.game.choices[e[1]] = value
            self.game.flags.add("%s=%s" % (e[1], value))
            self.game.snd("bell")
            self.pick = 0
        self.i += 1
        self.t = 0.0
        self.last = 0
        self.settle()
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
        if self.choosing():
            self.draw_choice(c)
            return
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

    def draw_choice(self, c):
        """YOUR CALL: the prompt, then the options (UP / DOWN, ENTER)."""
        g = self.game
        opts = self.options()
        h = 22 + 11 * len(opts) + 4
        r = pygame.Rect(self.CARD.x, self.CARD.bottom - h, self.CARD.w, h)
        plate = pygame.Surface(r.size, pygame.SRCALPHA)
        plate.fill((18, 12, 30, 245))
        c.blit(plate, r.topleft)
        gold = (255, 214, 90)
        pygame.draw.rect(c, gold, r, 1)
        draw_text(c, g.font_s, "YOUR CALL", r.x + 6, r.y + 4, gold)
        draw_text(c, g.font_s, self.text()[:self.shown()], r.x + 14 + g.font_s.size("YOUR CALL")[0], r.y + 4,
                  (232, 236, 250))
        if not self.typed():
            return
        for k, (label, value, note) in enumerate(opts):
            y = r.y + 18 + k * 11
            on = k == self.pick
            if on:
                c.fill((60, 46, 90), (r.x + 3, y - 1, r.w - 6, 11))
                if int(g.clock * 3) % 2 == 0:
                    draw_text(c, g.font_s, ">", r.x + 6, y, gold)
            draw_text(c, g.font_s, label, r.x + 14, y, gold if on else (232, 236, 250))
            draw_text(c, g.font_s, note, r.x + 14 + g.font_s.size(label)[0] + 8, y, (170, 180, 215))

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
MOVE_ROWS = (("ARROWS", "MOVE / CIRCLE"), ("A / S", "JAB / CROSS"), ("D / F", "BODY SHOTS"),
             ("Z / V", "HOOK / UPPERCUT"),
             ("W (+DIR)", "SLIP / STEP"), ("E / R HOLD", "BLOCK HI / LOW"), ("SHIFT+A..F", "FEINT"),
             ("Q", "CLINCH"), ("X", "PIVOT"))
FIGHT_TIPS = ("Slip then punch = COUNTER", "Block late = PARRY", "Step off his line: W + ARROW",
              "Hooks catch side-steps", "Uppercut splits the guard", "Feint him, then land big",
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
        self.sturdy = 0.0              # 0..1: how little ground he gives when he's hit
        self.hold_x = 1.0              # what holding his guard costs him (a peek-a-boo man lives there)
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
        self.cut = 0.0                       # 0 none .. CUT_STOP the doctor stops it
        self.face = 0.0                      # damage taken to the head (cuts open on a marked-up face)
        self.thrown = self.landed = self.power_landed = 0
        self.round_mark = (0.0, 0, 0, 0, 0)  # dealt / kds / thrown / landed / power at the start of the round
        self.pressure = 0.0                  # seconds spent walking him down this round
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
        o = self.foe() if self.game.mode != "bag" else None
        if o is not None and o.action in PUNCHES and not o.hit_done:
            o.track_left = min(o.track_left, 0.08)  # it was thrown at where you WERE
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
        if name in PUNCHES:
            self.thrown += 1
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
        """Knocked straight back (away from where he faces), stopped by the ropes.
        Pressure fighters lean into punches and give up less ground."""
        if px > 0:
            px *= 1.0 - self.sturdy
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
                rate *= STAM_GUARD_REGEN if self.pro_regen else 0.5
            elif self.moving:
                rate *= STAM_MOVE_REGEN if self.pro_regen else 1.0
            elif not self.action:
                rate *= STAM_REGEN_IDLE
            self.stam = min(float(STAM_MAX), self.stam + rate * dt)
        if not self.pro_regen:                     # the computer still burns wind holding on
            if self.block:
                self.spend(STAM_HOLD * self.hold_x * dt)
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
            self.update_locomotion(dt, move, min_x, max_x, zmove, slow=GUARD_WALK)   # inch forward behind it
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

    def update_locomotion(self, dt, move, min_x, max_x, zmove=0, slow=1.0):
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
        speed = (WALK_FWD if fwd else WALK_BACK) * self.walk * (0.6 if self.hurt else 1.0) * slow
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
            if self.moving == 1 and o is not None:
                self.pressure += dt                      # the judges like a man coming forward
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
        self.style = dict(style or {}) if isinstance(style, dict) else {}
        self.combos = None
        self.style_key = ""
        self.me.sturdy = 0.0
        self.learn_rate = self.params.get("learn", 1.0)

    def set_profile(self, level_name, params, style_key):
        """A full profile: params from ai_profile(), weights and combinations from the style."""
        self.level = level_name
        self.params = dict(params)
        st = STYLES[style_key]
        self.style = dict(st["weights"])
        self.combos = [list(c) for c in st["combos"]]
        self.style_key = style_key
        self.me.sturdy = STURDY.get(style_key, 0.0)
        self.me.hold_x = 0.35 if self.params.get("shell") else 1.0
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
        self.wait_t = 0.0                        # stepping in for a short punch
        self.smother_t = 0.0                     # rushing in to tie you up
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
        R = self.game.ranges
        dist = self.game.dist()
        if self.me.stam < 45 * pace:              # low on wind: pick your shots, mostly jabs
            if self.me.stam < 26 * pace:
                return ["jab"]
            return random.choice([["jab"], ["jab"], ["jab", "jab"], ["body_jab"], ["jab", "cross"]])
        combos = self.combos or [["jab", "cross"], ["jab", "jab", "cross"], ["jab", "body_cross"],
                                 ["body_jab", "cross"], ["jab", "body_jab", "cross"], ["cross", "body_jab"],
                                 ["jab", "cross", "hook"]]
        if foe.hurt:                              # smells blood: power shots to finish him
            heavy = [c for c in combos if sum(POWER[n] for n in c) >= 4.0] or [["jab", "cross", "cross"]]
            return list(random.choice(heavy + [["cross", "hook", "cross"], ["hook", "uppercut"]]))
        if foe.block and foe.block_t > 0.3 and random.random() < L["flurry"]:
            seq = [random.choice(["jab", "jab", "body_jab"]) for _ in range(random.randint(2, 4))]
            if foe.block == "high":                # go round it, under it, or through the middle
                seq.append(random.choice(["body_cross", "hook", "uppercut"] if dist < R["hook"] else ["body_cross"]))
            else:
                seq.append("cross")
            return seq
        if random.random() < L["combo"]:
            return list(random.choice(combos))
        if foe.block == "high":
            w = dict(jab=1, cross=0.5, body_jab=3, body_cross=3, hook=1.4, uppercut=1.6)
        elif foe.block == "low":
            w = dict(jab=3, cross=3, body_jab=0.5, body_cross=0.3, hook=2, uppercut=1)
        else:
            w = dict(jab=4, cross=2, body_jab=2, body_cross=1.5, hook=1.2, uppercut=0.6)
        w = {n: v * self.style.get(n, 1.0) for n, v in w.items()}
        for n in ("hook", "uppercut"):             # don't throw the short ones from out there
            if dist > R[n] + 4:
                w[n] *= 0.1
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
        if self.pin_t > PIN_PATIENCE * L.get("pin", 1.0) and self.reset_t <= 0:
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
                slip_ok = {"hook": 0.35, "uppercut": 0.05}.get(real, 1.0)
                if random.random() < L.get("step", 0.1) and me.side_cd <= 0 and real != "hook":
                    kind = "step"
                elif target == "head" and random.random() < (L["slip"] + 0.5 * self.read_bonus(real)) * slip_ok:
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
        if (L.get("clinchy") and dist <= MIN_SEP + CLINCH_RANGE - 2 and me.clinch_cd <= 0 and not foe.clinch
                and not foe.busy() and random.random() < L["clinchy"] * dt * (2.5 if foe.action in PUNCHES else 1.0)):
            self.game.try_clinch(me)              # tie him up and kill his rhythm
            return
        if (L.get("shell") and blocking is None and not me.action and dist < R["jab"] and not self.plan
                and random.random() < 0.9 * dt):
            me.press("slip")                      # bob and weave on the way in
            return
        if blocking is None and self.guard_t > 0:
            self.guard_t -= dt
            if foe.busy() or self.punish:
                self.guard_t = 0.0
            else:
                blocking = self.guard_level
        me.want_block = blocking
        if blocking:
            if L.get("range", 0) < 0 and dist > R["jab"] - 6 + L["range"] + 3:
                self.go(1, 0)                     # walking him down behind the gloves
            return
        if L.get("clinchy") and foe.action in PUNCHES and dist < R["jab"] + 6 and self.smother_t <= 0 \
                and random.random() < L["clinchy"] * 0.2:
            self.smother_t = 0.7                  # step inside his punches and tie him up
        if self.smother_t > 0:
            self.smother_t -= dt
            if dist <= MIN_SEP + CLINCH_RANGE - 3 and me.clinch_cd <= 0 and not foe.clinch:
                self.smother_t = 0.0
                self.game.try_clinch(me)
                return
            self.go(1, 0)
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
        if self.plan and not me.action and dist > R.get(self.plan[0], 99) + 2:
            self.wait_t += dt                     # too far for that one: step in for it first
            if self.wait_t < 0.5:
                self.go(1, 0)
                return
            self.plan.clear()                     # (he kept away - start again)
        self.wait_t = 0.0
        if self.plan and me.can_start(self.plan[0]):
            nxt = self.plan[0]
            if (nxt in PUNCHES and me.stam > 35 and foe.block is None and not foe.busy()
                    and random.random() < L.get("feint", 0.0)):
                me.press("feint_" + nxt)          # sell it first, then throw it
                return
            me.press(self.plan.pop(0))
            if not self.plan and random.random() < L.get("retreat", 0.3):
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
        desired = R["jab"] - 6 + L.get("range", 0) if not foe.hurt else R["cross"] - 10
        desired = max(MIN_SEP + 3, desired)
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
        elif dist < desired - 8 and L.get("range", 0) > 0:
            radial = -1                           # an out-boxer keeps you at the end of his jab
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
        self.fist = {i: fist_point(frames[i]) for i in (6, 14, 15, 29, 34, 57, 63)}
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
        self.choices = {}
        self.career_reset()
        self.rebuild = None
        self.scene = None
        self.scene_after = (None, None)
        self.ending = None
        self.save_data = None
        self.saved_t = 0.0
        self.menu_i = 0
        self.yacht = None
        self.card_t = 0.0
        self.start_rounds(SPAR_ROUNDS)
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
        self.player.configure(chin=PLAYER_CHIN)
        self.cpu.configure()
        level = self.ai.level if self.ai.level in LEVELS else "NORMAL"
        self.spar_style = FORCE_SPAR_STYLE or random.choice(STYLE_ORDER)
        st = STYLES[self.spar_style]["stats"] if SPAR_STYLE_STATS else {}
        self.cpu.configure(MAX_HP, 1.0 + st.get("power", 0), 1.0 + st.get("speed", 0) * 0.5,
                           1.0 + st.get("walk", 0), 1.0 + st.get("chin", 0), 1.0, 1.0 + st.get("wind", 0))
        self.ai.set_profile(level, ai_profile({"EASY": 1.4, "NORMAL": 3.0, "HARD": 4.4}[level], self.spar_style),
                            self.spar_style)
        self.player.reset(96)
        self.cpu.reset(224)
        self.face_off()
        self.ai.reset()
        self.phase, self.phase_t = "intro", 0.0
        self.start_rounds(SPAR_ROUNDS)
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

    def fighter_ai(self, key):
        o = FIGHTERS[key]
        tier = o.get("tier", 2) + getattr(self, "tier_bump", 0.0)
        return ai_profile(tier, o["fstyle"], o.get("ai"))

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
            self.choices = {}
            self.boosts = dict(power=0, speed=0, wind=0, chin=0)
            self.fought = []
            self.money = 0
            self.ladder = [dict(r) for r in LADDER]
            self.rank = None
        self.rebuild = None
        self.scene = None
        self.ending = None
        self.offers = []
        self.offer_i = 0
        self.camp_i = 0
        self.judge_bias = 0.0
        self.tier_bump = 0.0
        self.corner = "doc"
        self.last_purse = 0

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
        self.play_scene(STORY["open"], "rung")

    def continue_career(self):
        d = self.save_data or {}
        self.mode = "campaign"
        self.career_reset()
        try:
            self.ladder = [dict(r) for r in d["ladder"]]
            self.idx = clamp(int(d.get("idx", 0)), 0, len(self.ladder) - 1)
            self.wins, self.losses, self.kos = int(d["wins"]), int(d["losses"]), int(d.get("kos", 0))
            self.flags = set(d.get("flags", []))
            self.choices = dict(d.get("choices", {}))
            self.boosts.update({k: int(v) for k, v in d.get("boosts", {}).items() if k in self.boosts})
            self.fought = [k for k in d.get("fought", []) if k in FIGHTERS]
            self.money = int(d.get("money", 0))
            self.rank = d.get("rank")
            self.rebuild = d.get("rebuild") if d.get("rebuild") in FIGHTERS else None
            for r in self.ladder:
                if r.get("opp") and r["opp"] not in FIGHTERS:
                    r.pop("opp")
        except (KeyError, TypeError, ValueError):
            self.career_reset()
        self.start_rung()

    def save_career(self):
        ok = save_career(dict(v=2, idx=self.idx, wins=self.wins, losses=self.losses, kos=self.kos,
                              flags=sorted(self.flags), choices=self.choices, boosts=self.boosts,
                              fought=self.fought, money=self.money, rank=self.rank, rebuild=self.rebuild,
                              ladder=self.ladder))
        self.saved_t = 2.2 if ok else -2.2
        self.snd("bell" if ok else "block")
        return ok

    def record(self):
        return "%d-%d" % (self.wins, self.losses)

    def bout(self):
        return self.ladder[min(self.idx, len(self.ladder) - 1)] if getattr(self, "ladder", None) else LADDER[0]

    def bout_rounds(self):
        if self.rebuild:
            return 3
        return self.bout().get("rounds", 3)

    # ------------------------------------------------------------ the story's little language
    def cond(self, c):
        """'key=value', '!key=value', 'flag', '!flag', 'losses=0', 'losses>0'."""
        if not c:
            return False
        neg = c.startswith("!")
        c = c.lstrip("!")
        if c.startswith("losses"):
            n = int(c[7:])
            ok = (self.losses == n) if c[6] == "=" else (self.losses > n)
        elif "=" in c:
            k, v = c.split("=", 1)
            ok = self.choices.get(k) == v
        else:
            ok = c in self.flags
        return ok != neg

    def fmt(self, text):
        key = self.rebuild or self.bout().get("opp") or self.opp_key
        o = FIGHTERS.get(key, FIGHTERS["rusty"])
        st = STYLES.get(o.get("fstyle", "brawler"))
        w, l, ko = o.get("record", (0, 0, 0))
        words = "%d wins, %d losses, %d by knockout" % (w, l, ko) if l else "Unbeaten, %d and oh, %d by knockout" % (w, ko)
        rep = dict(opp=o.get("short", "HIM"), opp_name=o.get("name", "HIM"), home=o.get("home", "OUT OF TOWN").title(),
                   record_words=words, blurb=st["blurb"] if st else "", tip=st["tip"] if st else "",
                   style=st["name"] if st else "", rounds=self.bout_rounds(), rank=self.rank or "-")
        try:
            return text.format(**rep)
        except (KeyError, IndexError, ValueError):
            return text

    def story_postpone(self):
        """Doc's in hospital and you wait for him: one more fight before the title."""
        if not any(r.get("kind") == "stay_busy" for r in self.ladder):
            self.ladder.insert(self.idx, dict(STAY_BUSY))
            self.ladder[self.idx + 1]["intro_done"] = True

    # ------------------------------------------------------------ the ladder
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
        if what == "intro_done":
            self.bout()["intro_done"] = True
            self.start_rung()
        elif what == "fight":
            self.begin_fight()
        elif what == "yacht":
            self.start_yacht()
        else:
            self.start_rung()

    def start_rung(self):
        """Where we are on the ladder: story first, then who you fight, then camp, then the fight."""
        r = self.bout()
        if r.get("intro") and not r.get("intro_done") and not self.rebuild:
            self.play_scene(STORY[r["intro"]], "intro_done")
            return
        if r.get("skip_if") and self.cond(r["skip_if"]) and not self.rebuild:
            self.advance_rung(won=False)
            self.start_rung()
            return
        if self.rebuild:
            lines = [("corner", "Tune-up. {opp_name}, out of {home}. {record_words}."),
                     ("corner", "{blurb}"), ("corner", "{tip}")]
            self.play_scene(lines, "fight")
            return
        if r["kind"] == "offer" and not r.get("opp"):
            self.make_offers()
            return
        if not r.get("opp"):
            r["opp"] = self.pick_opponent(r)
        self.after_opponent()

    def after_opponent(self):
        r = self.bout()
        if r["kind"] in ("debut",) or self.cond("notice=take") and r["kind"] == "belt" or self.camp_full():
            self.play_pre()
        else:
            self.phase, self.phase_t = "camp", 0.0
            self.camp_i = 0
            self.clear_fx()

    def play_pre(self):
        r = self.bout()
        if r.get("pre"):
            lines = list(STORY[r["pre"]])
        else:
            lines = list(GENERIC_PRE) + [("you", random.choice(GENERIC_REPLY))]
        self.play_scene(lines, "fight")

    def pool(self, tiers, exclude=()):
        keys = [k for k, f in FIGHTERS.items() if f.get("tier") in tiers and f.get("fstyle")
                and k not in STORY_ONLY and k not in self.fought and k not in exclude
                and not any(r.get("opp") == k for r in self.ladder)]
        if not keys:                                  # (only if you've beaten the whole level)
            keys = [k for k, f in FIGHTERS.items() if f.get("tier") in tiers and f.get("fstyle")
                    and k not in STORY_ONLY and k not in exclude]
        return keys

    def pick_opponent(self, r):
        tiers = r["tiers"]
        if r["kind"] == "belt" and self.cond("notice=take"):
            tiers = (3,)
        if r["kind"] == "debut":                       # nobody too clever on your first night
            keys = [k for k in self.pool(tiers) if FIGHTERS[k]["fstyle"] not in ("counter", "peekaboo")]
        else:
            keys = self.pool(tiers)
        if r["kind"] == "belt" and not self.cond("notice=take"):
            keys.sort(key=lambda k: -FIGHTERS[k]["record"][0])   # the champion: the most wins at that level
            keys = keys[:3]
        return random.choice(keys)

    def make_offers(self):
        r = self.bout()
        keys = self.pool(r["tiers"])
        random.shuffle(keys)
        styles = set()
        offers = []
        for k in keys:                                 # three men, three different styles if possible
            if FIGHTERS[k]["fstyle"] in styles and len(keys) > 4:
                continue
            styles.add(FIGHTERS[k]["fstyle"])
            offers.append(k)
            if len(offers) == 3:
                break
        offers.sort(key=lambda k: (FIGHTERS[k]["tier"], FIGHTERS[k]["record"][0]))
        self.offers = offers
        self.offer_i = 0
        self.phase, self.phase_t = "offers", 0.0
        self.clear_fx()

    def purse(self, key):
        o = FIGHTERS[key]
        w = o.get("record", (10, 0, 0))[0]
        base = PURSE.get(o.get("tier", 1), 1000)
        return int(round(base * (0.8 + 0.02 * w) / 50.0)) * 50

    def opp_rank(self, key):
        t = FIGHTERS[key].get("tier", 1)
        h = sum(map(ord, key))
        if t >= 5:
            return "C"
        if t == 4:
            return "#%d" % (2 + h % 7)
        if t == 3:
            return "#%d" % (9 + h % 16)
        return None

    def take_offer(self):
        if not self.offers:
            return
        self.bout()["opp"] = self.offers[self.offer_i]
        self.offers = []
        self.snd("bell")
        self.after_opponent()

    def camp_full(self):
        return all(v >= CAMP_MAX for v in self.boosts.values())

    def take_camp(self):
        name, stat, _ = CAMP[self.camp_i]
        if self.boosts[stat] < CAMP_MAX:          # (maxed out: you still go to camp - you just keep sharp)
            self.boosts[stat] += 1
        self.snd("bell")
        self.play_pre()

    def advance_rung(self, won=True):
        if won and not self.rebuild:
            self.rank = RANK_AFTER.get(self.idx, self.rank)
        self.idx = min(self.idx + 1, len(self.ladder) - 1)

    def begin_fight(self):
        r = self.bout()
        key = self.rebuild or r.get("opp")
        if not key:
            key = r["opp"] = self.pick_opponent(r)
        o = self.opp = dict(FIGHTERS[key])
        self.opp_key = key
        if r["kind"] == "belt" and not self.rebuild and not self.cond("notice=take"):
            o["title"] = "STATE CHAMPION   -   " + o["title"]
        p, c = self.player, self.cpu
        c.set_views(self.fighter_views(key))
        c.configure(o["hp"], o["power"], o["speed"], o["walk"], o.get("chin", 1.0), o.get("heart", 1.0),
                    o.get("wind", 1.0))
        b = self.boosts
        p.configure(MAX_HP, 1.0 + CAMP_GAIN["power"] * b["power"], 1.0 + CAMP_GAIN["speed"] * b["speed"],
                    1.0 + CAMP_GAIN["speed"] * b["speed"], PLAYER_CHIN + CAMP_GAIN["chin"] * b["chin"], 1.0,
                    1.0 + CAMP_GAIN["wind"] * b["wind"])
        p.reset(96)
        c.reset(372)                       # off screen - walks in
        self.face_off()
        # story effects: bought judges, a blacklisted fighter, an angry rival, who's on your stool
        hostile = r.get("hostile")
        self.judge_bias = hostile[1] if (hostile and not self.rebuild and self.cond(hostile[0])) else 0.0
        self.tier_bump = 0.35 if ("blacklisted" in self.flags and not o.get("champ")) else 0.0
        extra = None
        if key in ("cruz", "cruz2") and self.cond("press=trash"):
            extra = dict(range=-8, combo=0.6, react=0.55, flurry=0.8, atk=(0.4, 0.9))
        if r["kind"] == "title" and self.cond("heart=fight"):
            self.corner = "preacher"
        elif "doc_gone" in self.flags:
            self.corner = "cutman"
        else:
            self.corner = "doc"
        prof = self.fighter_ai(key)
        if extra:
            prof.update(extra)
        self.ai.set_profile(o.get("level", "NORMAL"), prof, o["fstyle"])
        self.ai.reset()
        self.phase, self.phase_t = "walkin", 0.0
        self.start_rounds(self.bout_rounds())
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
        self.last_purse = self.purse(self.opp_key) if won else self.purse(self.opp_key) // 2
        self.money += self.last_purse
        if won:
            self.wins += 1
            if self.method in ("KO", "OUT COLD", "TKO", "STOPPAGE", "CUT", "RTD"):
                self.kos += 1
            if self.opp_key not in self.fought:
                self.fought.append(self.opp_key)
            if not self.rebuild:
                self.flags.add("beat_" + self.opp_key)
                if self.bout()["kind"] == "belt" and not self.cond("notice=take"):
                    self.flags.add("state_champ")
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
        r = self.bout()
        if self.result == "YOU WIN!":
            if self.rebuild:
                self.rebuild = None
                self.play_scene(STORY["rebuilt"], "rung")
                return
            if r.get("won"):
                lines = list(STORY[r["won"]])
            else:
                lines = list(random.choice(GENERIC_WON))
            old = self.rank
            self.advance_rung(won=True)
            if self.rank and self.rank != old:
                lines.append(("corner", "Rankings came out. You're number %d in the world now." % self.rank
                              if self.rank > 1 else "You're the mandatory challenger now. Number one."))
            self.play_scene(lines, "rung")
            return
        if self.losses >= MAX_LOSSES:
            self.start_retire()
            return
        if r.get("title_fight"):
            lines = list(STORY["title_lost"])
        elif self.rebuild:
            lines = list(STORY["setback"])[:1] + [("corner", "One more tune-up. Then the rematch.")]
        else:
            lines = (list(STORY[r["lost"]]) if r.get("lost") else list(random.choice(GENERIC_LOST))) + list(STORY["setback"])
        if self.losses == MAX_LOSSES - 1:
            lines += list(STORY["last_chance"])
        tiers = (max(1, min(r["tiers"]) - 1),)
        self.rebuild = random.choice(self.pool(tiers, exclude=(r.get("opp"), self.opp_key)))
        self.play_scene(lines, "rung")

    def start_retire(self):
        self.ending = "retire"
        self.scene = Scene(self, STORY["retire"])
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
        self.scene = Scene(self, STORY["yacht"], top=True)
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
        elif self.phase == "offers" and self.offers:
            self.offer_i = (self.offer_i + d) % len(self.offers)
            self.snd("blip")
        elif self.phase == "camp":
            self.camp_i = (self.camp_i + d) % len(CAMP)
            self.snd("blip")
        elif self.phase in ("scene", "retire", "yacht") and self.scene and self.scene.choosing():
            self.scene.move(d)
            self.snd("blip")

    def next_label(self):
        """What the victory screen says is coming up."""
        if self.rebuild:
            return "BACK TO: " + FIGHTERS[self.bout().get("opp") or "rusty"]["short"]
        if self.bout().get("title_fight"):
            return "THE TITLE"
        nxt = self.ladder[min(self.idx + 1, len(self.ladder) - 1)]
        if nxt.get("opp"):
            return "NEXT UP: " + FIGHTERS[nxt["opp"]]["short"]
        return "NEXT: " + nxt.get("bill", "THE NEXT FIGHT")

    def taunt_frame(self, kind, t):
        seq, ms = TAUNTS[kind]
        i = int(t * 1000 / ms) % len(seq)
        return seq[i], i

    def update_campaign(self, dt, move, want):
        p, c, o = self.player, self.cpu, self.opp
        if self.bubble:
            self.bubble.update(dt)
        if self.phase in ("intro", "fight", "ko", "down", "bell", "corner"):
            self.update_spar(dt, move, want)
            if self.phase == "result":
                self.after_fight()
            return
        self.phase_t += dt
        self.saved_t -= dt if self.saved_t > 0 else -dt if self.saved_t < 0 else 0
        if self.phase in ("scene", "menu", "retire", "yacht", "offers", "camp"):
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
        if self.phase == "corner" and self.mode != "bag":
            if self.scene and not self.scene.done():
                self.scene.advance()
                if not self.scene.done():
                    return
            self.next_round()
            return
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
            elif ph == "offers":
                self.take_offer()
            elif ph == "camp":
                self.take_camp()
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
        if f.action in BIG_SHOTS and self.mode != "bag":
            f.spend(STAM_MISS * 2)
            name = f.action
            f.stagger(OFF_BALANCE)                   # swung through nothing: wide open for a moment
            wx, wy = f.tip(frame)
            self.say("OFF BALANCE", wx - 26, wy - 18, (255, 170, 120), self.font_s, vy=-14, life=0.6)
            if f is self.player:
                self.ai.punish = True
            f.action = None
            return
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
                if self.round_no >= self.rounds_total:
                    self.end_fight(by_time=True)
                else:
                    self.end_round()
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
            elif self.phase == "bell" and self.phase_t > 1.3:
                self.start_corner()
            elif self.phase == "corner":
                if self.scene:
                    self.scene.update(dt)
                if self.phase_t > CORNER_TIME:
                    self.next_round()
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

    # ------------------------------------------------------------ rounds
    def round_secs(self):
        return float(ROUND_TIME if self.mode == "campaign" else SPAR_ROUND_TIME)

    def start_rounds(self, total):
        """A fresh fight: round 1 of `total`, clean scorecards."""
        self.rounds_total = max(1, int(total))
        self.round_no = 1
        self.round_time = self.round_secs()
        self.cards = [[] for _ in range(3)]          # per judge: [(you, him), ...] one per round
        self.round_stats = []
        self.decision_kind = ""
        self.judge_bias = getattr(self, "judge_bias", 0.0) if self.mode == "campaign" else 0.0
        for f in (self.player, self.cpu):
            f.round_mark = (f.dealt, f.kds, f.thrown, f.landed, f.power_landed)
            f.pressure = 0.0

    def card_totals(self):
        return [(sum(a for a, _ in j), sum(b for _, b in j)) for j in self.cards]

    def score_round(self):
        """Each judge scores the round just finished: 10 to the man who won it, 9 (or less, for every
        knockdown) to the other. Close rounds can go 10-10. Judges see damage, clean punches,
        knockdowns and who was coming forward - and they don't all see it the same way."""
        p, c = self.player, self.cpu
        def took(f):
            d0, k0, t0, l0, w0 = f.round_mark
            return dict(dealt=f.dealt - d0, kds=f.kds - k0, thrown=f.thrown - t0, landed=f.landed - l0,
                        power=f.power_landed - w0, pressure=f.pressure)
        a, b = took(p), took(c)
        pts = lambda r: r["dealt"] + 0.5 * r["landed"] + 0.6 * r["power"] + 0.25 * r["pressure"] + KD_POINTS * r["kds"]
        diff = pts(a) - pts(b)
        for k, judge in enumerate(self.cards):
            d = diff + random.gauss(0, JUDGE_NOISE) + self.judge_bias + (k - 1) * 0.6
            if abs(d) < JUDGE_EVEN and not (a["kds"] or b["kds"]):
                sp = sc = 10
            elif d > 0:
                sp, sc = 10, 9
            else:
                sp, sc = 9, 10
            sp -= b["kds"]                     # a point off for every time he put you down...
            sc -= a["kds"]                     # ...and for every time you put him down
            judge.append((sp, sc))
        self.round_stats.append((a, b))
        for f in (p, c):
            f.round_mark = (f.dealt, f.kds, f.thrown, f.landed, f.power_landed)
            f.pressure = 0.0

    def verdict(self):
        """(+1 you / -1 him / 0 draw, 'UNANIMOUS' / 'SPLIT' / 'MAJORITY' / '')"""
        votes = [(1 if a > b else (-1 if b > a else 0)) for a, b in self.card_totals()]
        you, him = votes.count(1), votes.count(-1)
        if you >= 2 and him == 0:
            return 1, "UNANIMOUS" if you == 3 else "MAJORITY"
        if him >= 2 and you == 0:
            return -1, "UNANIMOUS" if him == 3 else "MAJORITY"
        if you == 2:
            return 1, "SPLIT"
        if him == 2:
            return -1, "SPLIT"
        return 0, "SPLIT" if you == him == 1 else ("MAJORITY" if you or him else "")

    def end_round(self):
        """The bell: score it, send them to their corners."""
        self.score_round()
        self.phase, self.phase_t = "bell", 0.0
        self.snd("bell3")
        p, c = self.player, self.cpu
        for f in (p, c):
            f.finish_action()
            f.want_block = f.block = None
            f.buffer = None
            f.clinch = False
        self.ref.hide()
        self.say("END OF ROUND %d" % self.round_no, VW // 2 - 50, 60, (255, 232, 130), self.font_l, vy=-4, life=1.2)

    def start_corner(self):
        """On the stool: wind back, head cleared, the cut worked on - and your corner talks to you."""
        p, c = self.player, self.cpu
        self.phase, self.phase_t = "corner", 0.0
        voice = self.corner_voice()
        heal = CORNER_HEAL * (1.0 if voice in ("doc", "preacher") else 0.65)
        for f, h, fix in ((p, heal, 30 if voice == "doc" else 22), (c, CORNER_HEAL * 0.8, 22)):
            f.stam = min(float(STAM_MAX), max(f.stam, 50.0) + CORNER_WIND)
            f.gassed = f.stam < GAS_LINE
            f.hp = min(f.max_hp, f.hp + f.max_hp * h)
            f.hp_lag = f.hp
            f.daze = max(0.0, f.daze - CORNER_DAZE)
            if f.hurt and f.daze < HURT_EXIT:
                f.hurt = False
            f.body_dmg *= 0.7
            f.guard = float(GUARD_MAX)
            f.cut = max(0.0, f.cut - fix) if f.cut > 0 else 0.0
            f.stun_t = f.hitstun = 0.0
            f.unanswered = 0
        p.x, p.z, c.x, c.z = MIN_X + 22, Z_START, STAGE_MAX_X - 22, Z_START
        self.face_off()
        lines = self.corner_advice()
        self.scene = Scene(self, lines)
        self.snd("bell")
        for f in (c, p):                           # the doctor takes a look between rounds
            if f.cut >= CUT_CHECK:
                self.scene = None
                self.say("THE DOCTOR HAS SEEN ENOUGH", VW // 2 - 80, 60, (255, 120, 110), self.font_m, vy=-4, life=1.6)
                self.end_fight(loser=f, method="CUT")
                return
        if self.mode == "campaign" and c.hp < c.max_hp * 0.18 and c.downs >= 2 and random.random() < 0.5:
            self.scene = None                      # his corner throws in the towel
            self.say("HIS CORNER PULLS HIM OUT", VW // 2 - 76, 60, (255, 232, 130), self.font_m, vy=-4, life=1.6)
            self.end_fight(loser=c, method="RTD")

    def next_round(self):
        self.round_no += 1
        self.round_time = self.round_secs()
        self.scene = None
        p, c = self.player, self.cpu
        p.x, p.z, c.x, c.z = 96.0, float(Z_START), 224.0, float(Z_START)
        self.face_off()
        self.ai.plan.clear()
        self.ai.def_plan = None
        self.phase, self.phase_t = "intro", 0.0
        self.snd("bell")

    def corner_voice(self):
        """Who is in your corner (the story can change it)."""
        if self.mode != "campaign":
            return "doc"
        return getattr(self, "corner", "doc") or "doc"

    def corner_advice(self):
        """What your corner tells you on the stool, from what actually happened in the round."""
        p, c = self.player, self.cpu
        a, b = self.round_stats[-1] if self.round_stats else (dict(landed=0, thrown=0, power=0), dict(landed=0, thrown=0, power=0))
        who = self.corner_voice()
        tips = []
        style = STYLES.get(self.opp_style(), {})
        you, him = self.card_totals()[1] if self.cards and self.cards[1] else (0, 0)
        if p.cut > 0:
            tips.append("Hold still... there. The cut'll hold if you keep that glove up on that side.")
        if p.stam < 45 or p.gassed:
            tips.append("You're blowing hard. Jab and move this round - let the tank fill back up.")
        if c.cut > 0:
            tips.append("He's cut. Go straight down the pipe - doubles on the jab, then the right hand.")
        if c.body_dmg > LIVER_BODY * 0.7:
            tips.append("He's sagging every time you go downstairs. Keep digging - that liver's ready.")
        elif c.stam < 40:
            tips.append("He's tired. Make him work - go to the body, his hands will come down.")
        if b["landed"] > a["landed"] + 4:
            tips.append("He's beating you to the punch. Feint first - make him show you something.")
        if self.rounds_total - self.round_no <= 1 and you < him:
            tips.append("You're behind on my card. Nice won't cut it - you need to take this man out.")
        elif you > him + 1 and self.rounds_total - self.round_no <= 1:
            tips.append("You're up. Box smart, stay off the ropes, don't give him anything stupid.")
        if style.get("tip"):
            tips.append(style["tip"])
        if not tips:
            tips.append("Good round. Same again - jab, move, make him pay when he reaches.")
        stat = "Round %d: you landed %d of %d, he landed %d of %d." % (
            self.round_no, a["landed"], a["thrown"], b["landed"], b["thrown"])
        out = [(who, stat)] + [(who, t) for t in tips[:2]]
        if self.mode == "campaign" and self.cards and self.round_no >= 2 and who == "doc" and random.random() < 0.5:
            out.append((who, "I've got it %d-%d %s." % (max(you, him), min(you, him),
                                                        "you" if you > him else ("him" if him > you else "even"))))
        return out

    def opp_style(self):
        return self.opp.get("fstyle", "") if self.mode == "campaign" else getattr(self, "spar_style", "")

    def end_fight(self, by_time=False, loser=None, method="KO"):
        p, c = self.player, self.cpu
        if by_time:
            # the three judges' 10-point-must scorecards decide it
            self.score_round()
            verdict, kind = self.verdict()
            if verdict == 0:
                self.result = "DRAW"
            else:
                self.result = "YOU WIN!" if verdict > 0 else "YOU LOSE"
                winner = p if verdict > 0 else c
                winner.won, winner.end_t = True, 0.0
                loser = c if winner is p else p
            self.decision_kind = kind
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
                   "CUT": "T.K.O.!", "RTD": "T.K.O.!", "DECISION": "DECISION", "DRAW": "DRAW"}
    METHOD_SUB = {"KO": "COUNTED OUT", "OUT COLD": "KNOCKED OUT COLD", "TKO": "THREE KNOCKDOWNS",
                  "STOPPAGE": "THE REFEREE STOPS IT", "CUT": "THE DOCTOR STOPS IT ON A CUT",
                  "RTD": "RETIRED ON HIS STOOL",
                  "DECISION": "THE JUDGES' DECISION", "DRAW": "THE JUDGES CALL IT A DRAW"}

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
        wide = spec.get("wide", False)
        if self.off_line(att, d) > LAT_HIT * (WIDE_LAT if wide else 1.0) or (d.side_t > 0 and not wide):
            return                                    # off his line / stepping off it - it sails past
        hx, hy = self.hit_point(d, target)
        caught = None
        if target == "head" and d.slipping():
            if spec.get("splits"):
                caught = "CAUGHT HIM SLIPPING!"       # dipped straight onto the uppercut
            elif wide and random.random() < 0.55:
                caught = "SLIPPED INTO IT!"           # slipped toward the hook
            else:
                att.hit_done = True
                d.counter_t = COUNTER_WINDOW
                self.say("SLIP!", hx - 12, hy - 18, (120, 220, 255), self.font_m, vy=-18, life=0.7)
                return
        att.hit_done = True
        blocked = d.block is not None and ((d.block == "high") == (target == "head")) and not caught
        if blocked:
            self.blocked(att, d, spec, hx, hy)
        else:
            # how far into the punch it landed: 1 = at the end of his reach (flush), 0 = smothered
            ext = clamp((dist - MIN_SEP) / max(1.0, self.ranges[att.action] - MIN_SEP), 0.0, 1.0)
            if spec.get("splits") or spec.get("wide"):
                ext = max(ext, 0.75)                  # short punches are meant to land short
            if caught:
                att.is_counter = True
                self.say(caught, hx - 34, hy - 40, (255, 200, 120), self.font_m, vy=-16, life=0.9)
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
        split = spec.get("splits") and d.block == "high"
        d.guard -= spec["guard"] * (1 + FLURRY_RAMP * d.block_chain) * (1 + 0.6 * d.gas()) * (1.8 if split else 1.0)
        if split:                                  # straight up the middle of the gloves
            chip = max(1, int(round(spec["spar_dmg"] * 0.3 * DMG_SCALE * att.punch_power())))
            d.hp = max(1.0, d.hp - chip)
            d.since_damage = 0.0
            att.dealt += chip
            self.say("SPLIT THE GUARD", hx - 36, hy - 28, (255, 190, 120), self.font_s, vy=-14, life=0.7)
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
        dmg = max(1, int(round(spec["spar_dmg"] * mult * att.punch_power() * self.dmg_scale()
                                * random.uniform(1 - DMG_VARIANCE, 1 + DMG_VARIANCE))))
        att.landed += 1
        if POWER[name] >= 2:
            att.power_landed += 1
        d.hp = max(0.0, d.hp - dmg)
        d.spend(STAM_HIT)
        if d.pro_regen:
            d.stam_t = min(d.stam_t, STAM_REGEN_DELAY - STAM_HIT_PAUSE)   # caught clean: no breather
        d.since_damage = 0.0
        att.dealt += dmg
        att.unanswered = 0
        d.unanswered += 1
        if target == "head":
            d.daze += (dmg / self.dmg_scale()) * (0.8 + 0.45 * imp) / d.chin * (1.15 if d.hurt else 1.0) \
                * (1.0 + d.cut / 250.0) * DAZE_SCALE
            d.daze_t = 0.0
            d.face += dmg
            self.cut_check(att, d, name, dmg, crit, hx, hy)
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

    def dmg_scale(self):
        return 1.0 if self.mode == "bag" else DMG_SCALE

    def cut_check(self, att, d, name, dmg, crit, hx, hy):
        """Big shots open cuts; open cuts get worse, bleed, and the doctor is watching."""
        if self.mode == "bag" or (self.mode == "spar" and not CUTS_IN_SPAR):
            return
        if d.cut <= 0:
            chance = (CUT_OPEN_CRIT if crit else CUT_OPEN) * (1.0 + d.face / 60.0) * (POWER[name] / 2.0)
            if POWER[name] >= 2 and random.random() < chance:
                d.cut = 22.0
                self.say("CUT!", hx - 12, hy - 34, (255, 80, 80), self.font_l, vy=-14, life=1.0)
                self.excite(0.2)
        else:
            d.cut += dmg * CUT_GROW * (1.3 if crit else 1.0)
        if d.cut > 0:
            for _ in range(5 + int(d.cut / 20)):
                a = random.uniform(-1.0, 1.0) + (0 if d.facing < 0 else math.pi)
                sp = random.uniform(30, 90)
                self.parts.append([hx, hy - 6, math.cos(a) * sp, math.sin(a) * sp - 40, random.uniform(0.25, 0.5),
                                   random.choice([(200, 20, 30), (150, 10, 20), (230, 50, 60)])])
        if d.cut >= CUT_STOP and self.phase == "fight":
            self.say("THE DOCTOR STOPS IT", VW // 2 - 60, 66, (255, 120, 110), self.font_m, vy=-6, life=1.6)
            self.end_fight(loser=d, method="CUT")

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
    STORY_PHASES = ("scene", "menu", "retire", "yacht", "offers", "camp")

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
                self.draw_cut(c, f)
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
            c.blit(self.arena_bg if (self.bout().get("act", 1) > 1 or ph in ("menu", "offers", "camp")) else self.bg,
                   (0, 0))
            if ph != "menu":
                self.crowd.draw(c, self.clock * 0.25, 0.0) if False else None
            dim = pygame.Surface((VW, VH), pygame.SRCALPHA)
            dim.fill((8, 6, 18, 222 if ph == "retire" else 206))
            c.blit(dim, (0, 0))
        gold, white, label = (255, 214, 90), (232, 236, 250), (170, 180, 215)
        if ph == "menu":
            self.draw_menu(c)
            return
        if ph == "offers":
            self.draw_offers(c)
            return
        if ph == "camp":
            self.draw_camp(c)
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
                draw_text(c, self.font_s, self.bill_line(), VW // 2, 20, white, center=True)
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
        lad = d.get("ladder") or LADDER
        i = clamp(int(d.get("idx", 0)), 0, len(lad) - 1)
        key = d.get("rebuild") or lad[i].get("opp")
        opp = FIGHTERS[key]["short"] if key in FIGHTERS else lad[i].get("bill", "")
        rows = [("CONTINUE CAREER", "ACT %s   %s   RECORD %d-%d" % (
            "I" * lad[i].get("act", 1), opp, int(d.get("wins", 0)), int(d.get("losses", 0)))),
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

    def career_strip(self, c, title):
        gold, label = (255, 214, 90), (170, 180, 215)
        band = pygame.Surface((VW, 26), pygame.SRCALPHA)
        band.fill((10, 8, 20, 200))
        c.blit(band, (0, 8))
        c.fill((92, 80, 120), (0, 8, VW, 1))
        c.fill((92, 80, 120), (0, 33, VW, 1))
        draw_text(c, self.font_m, title, 8, 11, gold)
        rank = ("RANKED #%d" % self.rank) if self.rank else "UNRANKED"
        draw_text(c, self.font_s, "%s   %s   EARNED $%s" % (self.record(), rank, "{:,}".format(self.money)),
                  VW - 8, 13, label, right=True)
        draw_text(c, self.font_s, "ACT %s   -   %s" % ("I" * self.bout().get("act", 1), self.bout().get("bill", "")),
                  VW - 8, 23, (232, 236, 250), right=True)

    def draw_offers(self, c):
        """Three men on the card - pick the one you want."""
        gold, white, label = (255, 214, 90), (232, 236, 250), (170, 180, 215)
        self.career_strip(c, "FIGHT OFFERS")
        n = max(1, len(self.offers))
        w = 100 if n == 3 else 120
        x0 = (VW - (w * n + 6 * (n - 1))) // 2
        for k, key in enumerate(self.offers):
            o = FIGHTERS[key]
            r = pygame.Rect(x0 + k * (w + 6), 40, w, 96)
            on = k == self.offer_i
            plate = pygame.Surface(r.size, pygame.SRCALPHA)
            plate.fill((30, 24, 50, 245) if on else (14, 12, 26, 220))
            c.blit(plate, r.topleft)
            pygame.draw.rect(c, gold if on else (74, 66, 96), r, 1)
            c.blit(self.portrait(key), (r.centerx - PORTRAIT_W // 2, r.y + 5))
            rk = self.opp_rank(key)
            if rk:
                draw_text(c, self.font_s, rk, r.right - 4, r.y + 4, gold, right=True)
            draw_text(c, self.font_s, o["short"], r.centerx, r.y + 36, o["color"], center=True)
            st = STYLES[o["fstyle"]]["name"]
            draw_text(c, self.font_s, st, r.centerx, r.y + 47, white, center=True)
            w_, l_, ko = o["record"]
            draw_text(c, self.font_s, "%d-%d  (%d KO)" % (w_, l_, ko), r.centerx, r.y + 58, label, center=True)
            draw_text(c, self.font_s, o.get("home", ""), r.centerx, r.y + 69, label, center=True)
            draw_text(c, self.font_s, "PURSE $%s" % "{:,}".format(self.purse(key)), r.centerx, r.y + 81,
                      (150, 240, 160), center=True)
        if self.offers:
            o = FIGHTERS[self.offers[self.offer_i]]
            st = STYLES[o["fstyle"]]
            lines = wrap(self.font_s, "DOC:  " + st["blurb"], VW - 20)
            for k, line in enumerate(lines[:2]):
                draw_text(c, self.font_s, line, VW // 2, 140 + k * 10, white, center=True)
        draw_text(c, self.font_s, "ENTER  TAKE THE FIGHT      S  SAVE",
                  VW // 2 + 30, VH - 14, gold, center=True)

    def draw_camp(self, c):
        """Training camp: what you work on for this one. It stays with you for the rest of your career."""
        gold, white, label = (255, 214, 90), (232, 236, 250), (170, 180, 215)
        key = self.bout().get("opp")
        self.career_strip(c, "TRAINING CAMP")
        if key in FIGHTERS:
            o = FIGHTERS[key]
            draw_text(c, self.font_s, "NEXT: %s  -  %s" % (o["short"], STYLES[o["fstyle"]]["name"]), VW // 2, 37,
                      o["color"], center=True)
        for k, (name, stat, note) in enumerate(CAMP):
            r = pygame.Rect(26, 47 + k * 23, VW - 52, 21)
            on = k == self.camp_i
            lvl = self.boosts[stat]
            plate = pygame.Surface(r.size, pygame.SRCALPHA)
            plate.fill((30, 24, 50, 245) if on else (14, 12, 26, 215))
            c.blit(plate, r.topleft)
            pygame.draw.rect(c, gold if on else (74, 66, 96), r, 1)
            draw_text(c, self.font_s, name, r.x + 8, r.y + 2, gold if on else white)
            draw_text(c, self.font_s, note, r.x + 8, r.y + 11, label)
            for p in range(CAMP_MAX):
                col = (150, 240, 160) if p < lvl else (50, 46, 70)
                c.fill(col, (r.right - 8 - (CAMP_MAX - p) * 7, r.y + 6, 5, 7))
            if lvl >= CAMP_MAX:
                draw_text(c, self.font_s, "MAXED", r.right - 50, r.y + 2, (120, 130, 160), right=True)
        if key in FIGHTERS:
            tip = STYLES[FIGHTERS[key]["fstyle"]]["tip"]
            for k, line in enumerate(wrap(self.font_s, "DOC:  " + tip, VW - 20)[:2]):
                draw_text(c, self.font_s, line, VW // 2, 140 + k * 10, white, center=True)
        draw_text(c, self.font_s, "ENTER  START CAMP      S  SAVE",
                  VW // 2 + 30, VH - 12, gold, center=True)

    def draw_sweep(self, c):
        """Two search lights sweeping the crowd before the fight and during the celebrations."""
        if self.phase not in ("walkin", "talk", "reply", "intro", "champion"):
            return
        for k, sp in ((0, 0.7), (1, -0.55)):
            x = VW / 2 + math.sin(self.clock * sp + k * 2.1) * VW * 0.45
            glow = self.sweep_glow
            c.blit(glow, (int(x) - glow.get_width() // 2, 18), special_flags=pygame.BLEND_RGB_ADD)

    def draw_cut(self, c, f):
        """A red gash over the eye (and the occasional drip) on a cut fighter."""
        if f.cut <= 0 or f.out_cold:
            return
        hx, hy = f.head_pos()
        x = int(hx + 2 * f.facing)
        y = int(hy + 1)
        c.fill((200, 20, 30), (x, y, 2, 1))
        if f.cut > 40:
            c.fill((160, 10, 20), (x, y + 1, 1, 2))
        if f.cut > 60 and random.random() < 0.05:
            self.parts.append([x, y + 2, random.uniform(-6, 6), 10.0, 0.4, (180, 20, 30)])

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
        name = self.opp["short"] if camp else "%s  %s" % (STYLES[self.spar_style]["name"], self.ai.level)
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
        draw_text(c, self.font_s, "R%d/%d" % (self.round_no, self.rounds_total), VW // 2 + 14, 36, label)
        for f, fx, rt in ((self.player, 88, False), (self.cpu, VW - 88, True)):
            if f.cut > 0:                       # a little blood drop: how bad the cut is
                col = (255, 90, 90) if f.cut < CUT_CHECK else ((255, 40, 40) if int(self.clock * 6) % 2 else (140, 10, 20))
                x = fx - 6 if rt else fx + 2
                c.fill((20, 10, 16), (x - 1, 23, 6, 9))
                c.fill(col, (x + 1, 24, 2, 2))
                c.fill(col, (x, 26, 4, 4))
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
        if self.phase == "corner":
            self.draw_corner(c)
        elif self.phase == "intro":
            self.banner(c, 50, 44)
            last = self.round_no == self.rounds_total and self.rounds_total > 1
            msg = (("FINAL ROUND" if last else "ROUND %d" % self.round_no) if self.phase_t < 0.9 else
                   ("BOX!" if self.round_no > 1 else "FIGHT!"))
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

    def draw_corner(self, c):
        """Between rounds: the numbers from the round, and your corner in your ear."""
        dim = pygame.Surface((VW, VH), pygame.SRCALPHA)
        dim.fill((8, 6, 18, 150))
        c.blit(dim, (0, 0))
        gold, white, label = (255, 214, 90), (232, 236, 250), (170, 180, 215)
        self.banner(c, 50, 50)
        draw_text(c, self.font_m, "END OF ROUND %d  OF  %d" % (self.round_no, self.rounds_total), VW // 2, 53, gold,
                  center=True)
        a, b = self.round_stats[-1] if self.round_stats else (None, None)
        if a:
            p, cc = self.player, self.cpu
            rows = (("PUNCHES LANDED", "%d / %d" % (a["landed"], a["thrown"]), "%d / %d" % (b["landed"], b["thrown"])),
                    ("POWER SHOTS", str(a["power"]), str(b["power"])),
                    ("FIGHT TOTAL", "%d / %d" % (p.landed, p.thrown), "%d / %d" % (cc.landed, cc.thrown)))
            for k, (name, x, y) in enumerate(rows):
                yy = 67 + k * 10
                draw_text(c, self.font_s, x, VW // 2 - 50, yy, (130, 200, 255), right=True)
                draw_text(c, self.font_s, name, VW // 2, yy, label, center=True)
                draw_text(c, self.font_s, y, VW // 2 + 50, yy, self.opp["color"] if self.mode == "campaign" else white)
        if self.scene and not self.scene.done():
            self.scene.draw(c)
        elif int(self.clock * 2.5) % 2 == 0:
            draw_text(c, self.font_s, "ENTER  SECONDS OUT", VW // 2, 120, gold, center=True)

    def bill_line(self):
        if self.rebuild:
            return "TUNE-UP   -   %d ROUNDS" % self.bout_rounds()
        return self.bout_line().split("   -   ", 1)[-1]

    def bout_line(self):
        """How tonight's fight is billed."""
        if self.rebuild:
            return "TUNE-UP BOUT   -   %d ROUNDS   -   RECORD %s" % (self.bout_rounds(), self.record())
        b = self.bout()
        bill = b.get("bill", "LIGHTWEIGHT")
        if b.get("kind") == "belt" and self.cond("notice=take"):
            bill = "SHORT NOTICE   -   RANKED BOUT"
        return "ACT %s   -   %s   -   %d ROUNDS" % ("I" * b.get("act", 1), bill, self.bout_rounds())

    def method_line(self):
        m = self.method or "DECISION"
        if m in ("DECISION", "DRAW"):
            kind = getattr(self, "decision_kind", "") or ""
            cards = "   ".join("%d-%d" % (a, b) for a, b in self.card_totals())
            if m == "DRAW":
                return ("%s DRAW   %s" % (kind, cards)).strip()
            word = "WON" if self.result == "YOU WIN!" else "LOST"
            return "%s - %s DECISION   %s" % (word, kind, cards)
        tail = ""
        if self.rounds_total > 1:
            tail = "   R%d %d:%02d" % (self.round_no, int(self.round_secs() - self.round_time) // 60,
                                     int(self.round_secs() - self.round_time) % 60)
        return "BY %s  -  %s%s" % (self.METHOD_TEXT[m].rstrip("!"), self.METHOD_SUB[m], tail)

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
              pygame.K_z: "hook", pygame.K_v: "uppercut",
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
    story = game.mode == "campaign" and game.phase in ("victory", "defeat", "scene", "menu", "offers", "camp",
                                                       "retire", "yacht")
    if key == pygame.K_s and game.mode == "campaign" and game.phase in ("victory", "defeat", "scene", "offers", "camp"):
        game.save_and_quit()
        return True
    if game.mode == "campaign" and key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
        choosing = game.scene is not None and game.scene.choosing()
        if game.phase in ("menu", "camp") or choosing or (game.phase == "offers" and key in (pygame.K_LEFT, pygame.K_RIGHT)):
            game.menu_move(1 if key in (pygame.K_DOWN, pygame.K_RIGHT) else -1)
            return True
    if key in PUNCH_KEYS and not story:
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
L5rwzIu/NNwGxD9MaOyl3ouv6+qDj/UnQF0LN1Z4AfD4zeKlDaafCenz3bhfffCx/qTDM0sLJBtuyMnZxzV38TNJcf3Q+7/6e73/
q7/Xx48/oo8ff0SHDjykJ/Zs3fCbxUsbzLO47KOT/8F1pGpbGOZ5ILEwE4qYpxW62OsuvDy2f7L/+5DiFzyLi3kTEPQ2H+rzI8f6
C7/TWyb0/vGTQ3/eTQC0/64JPbtxQts2DyfWHld5h9ft8WgRt/jF/S8d0v1P7Ot/Dc0xE0FfOnZkaMGd4hfVxL4DGL53MCn77OXd
txmLFy7X2oC1eOGy3ji0O3fOwocENsV8bWI+Z3/NLFgeP7uk+Ss3Mx9l9wfvZ/lMX1V0b5S1h90u5h15dqXXLju379Xsys3cj3Fu
i9j+yB1LuWsHhhnPEucB+zqP4b4b2+9qZq6OPiWL+f/RwPpXWqz/joayPt/XBtJg4zPxry70XTivDbgHmhH6HC6KPfGvpmr/w7Vf
jRl/xj5/bYw/41WZAy3aC2GKAEu9QwE21r7KNb3+aNa+7OIXaIZvLUbbvtzfi/L+r/5eUnExGHt/FmuU5XxrlvZ6sCTverA0KMRQ
Zlzb4devv6i5i5/p8FNTUclm7P5f6t0LbvGLIuP6XGhq/THv+Ytivz19ptKf+9KxI/1fu89eg/n7OPZhyDxu33/3t3+uu7/9c/3+
v/yFfvvvvqXnHtqvX9z1B/3irj9o3zvzOjF/Qd/61b8fSpTrPh/Yt1JNSPGLvL1EpiCDj/tOLfX2eR2d2DR2z2Sp3QQ09r1g3wfS
eN8LoTH3zUXkrTc2/kPeJqrO/fjm3RAvZO03b87NXnfhGq8vpN9xx5+SgotfjNs7VltM0S4jk2gepezrvOyatw/Bu/MMeXM97IMO
E3P2VMrOPRTN+Ziiy/Q79YW8Z/mK8bjnM8w7FAbsObgYvmdw2TkkSdwDlrundhfu8Swbc/JeVV3VuU+jrL8Z5/maIrFz/ubcI8n/
m+X2+yR57k7VdS+0J+YsMInmu3FmPrt/yi268P7/vJ75/d3f/nkvGZzoz6p69dS5/juuGbOb81j3brkz8723bt059CGp3waIZ54H
9vnG0A+JPqkuX/ylwdlRk4MD9fjmHWJzv/lykPE+XM8HS1dLvyck9xLFL+qb3nuv990gZP8/yf+bUXVejvhXV/UMsHsGkviXM++9
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
RQGG9YU+qDl1+3/WvqqpOv7k2m9GbPx9hy/QnpD1R7TDdwDg1/8juxZ597d/Lkn6+rd73/P1v5Z+LbHhvwK3L8pPAC1950/8SSFY
F4sX+gzw9UU24t0+Dj82LygBgUQi4hbF9P3SA73DX2u/mz7eK3yadwCSwhfV2e1gH4DMK4TRK0DLodRYIc9gf1v02sOs+RLrapj/
Xz+Ye2tGU2u/xL+60Dbwjfs5g9SevASs9vzCwuZDFOHpgDnzKGmt3xf9fgOqzP1LtEFTQuJflAhaGk5IT1u050OS7jWmat8jZfsf
3ruaV7SuIg3WHOcp/tgqtx3cxP8Hdmwi+X+LQpLOb9tMIsO2+MY+bsLJV0+d087te3X544v9s6cLN1Z0mnaJ8s2Dz+vdhWwSSkk6
/rMHM4V4fElApx7aqfkTl/rt8vmRXiGNLx070v8eEn9Wd3L2cR08+lZuQSSMHt4J4rD+khbxH32+IrScN62H84/rF0WZ07LvgS8W
X6Yv6hCxb453/6enCG1R8YuPzpzX1iOZL2tueaX/6+ktE9lf8y6ckd3f2StAYrPnHUwB4JdeX9T03nslsc+wC0OFwCT9bu08TN/Z
QfEL9t2Gq5J/RmIvXFPqxJ8cZM0Y5zmIO1L+42+efK0/mIxhbpQ7pl7Uts2TqyXfjoYR/+ZUSX7ixv/pqd20QQV1Y28mQpv+uZD1
4b5f9j+kbOyJfz1vnnyt0p/jGdCcmIG//WfMCwD9UHVc/2lUSwC01P9Y2HyI2LfkgR/+rv9h4r544XL/QyIBUB0/+tt/ycTYfEiD
ZD8m5i47/pOfftH//MKNlaEPieIXdbnXvzS49nnm1lNl4k1i/N8Ue/I5FuOfZrjFF0LZzwyJdqjj0+tLG75YfDn6ULXdBv3FGNqg
M7wD19Nk/0/sq2H+f/1h7NMM1n/Tqhr/PF+b3KrpvffyHI5QpQ24/ptDH5SOiX2d659xfz2MP9OKib/ZA7Gw+ZAWNh9iDrRDvvVH
4t8N31rkb//dt/Tbf/ctfedP/rT/wYb/evL6InuN0rc2SfGLemKfwb5nQEs/2m2pzuFrO/aMfbrjPn9Zg29WSN8v9fan/PNvf6x/
/u2PdcfUizr85j9KyrbD6poNa9r/6de3sv7Ijb/5sN/DDr/5j5q7+Fn/g+dwnNBnsHs/sBele8w/pMPcW3M4f5ReSBvY5498Z5Da
/hlvN2XjnaI953b8Td9PG7SPfqd5Tex/buPnGhdl8bf7IZvdHzHn2Q3f+gtj/+qaWPdt+mcaB3ljH19f4/YzZu6Z+LfHbQeTbM98
HJ3YpPkrN7Vz+169ds89/Y9nN07QJg0w8bfteu5M/+PJE4NkiNs2T66aj65/ztud3Q5uwsmPzpzX9JYJHZ3YpJ3b9+r5a9f0/LVr
On1rhfsg0qs/+CP97j8/oFd/8EeZD5ebBFTKtospfnH1wcf6bfTRmfOS1G8r2qXY01O7V3/9+oupf4yxRht0h73PaRH/NKrs/7H3
/rDm2xz2n6dl5x+I4d4P9EPxmjp/zVpAPGI/2ny5r1zm/db2/vGTmt4y0f+YW17pfyDLl4fM5Su6OfONyf4+Q4k9uFVV3Ycu9fYh
2mcA7OIX7LvtBs+BtHgPrm/c5yCSFsBoCh1PNU0lQGEiqJqm4k/SmW6RiDUdN/Zc+6OBNohnEq9+9vqTlf48L2Cjg9hXUyUB0If7
fskiWEVVF3/d5AP2s5fYNyOv8IjhFmA4fWtFO7fv1c7te3X61or3g+IXWU1c/2bSmbFndU1MvNEGo4M2qKZq8QXDXbTkeVzNp9eX
Npi2iEUbVFf3+ucdeDTwHI7H/H9arH/dHoh99/LuG4pgdON22YAyKposBINu0d9Uw/gzLeZA06lzCNJNgkj8q2EtZv1x1ybtNUnW
g7vDHsT6qhy+loh9XU0VIKHf75bvoKQ9BqLwRT1l/VFeMRIp2w4Sc6Ih6hyClzRUBIPxT5w68w+s+9ZX9bon9vVx7afX5PVPG8Qr
Gu/49pybeTfmP+tpat6ZmFdHG6Rhj/lD4l9UjIcCtNVUfe8qKkJFG4Rrct9bAz/OWPKNffLWVexrnnOP7TPtkJf4//z2LTo6samf
+F+S9t81QfL/BpUVIDEoPtIu9x4wtr73tp5ZWtDljy/q8scX+21z+haJJmP4klCaeeWiJKB57ZKHIhjlTL/iKzYSgnFoc+q0QcM/
CkoQ87SIfzVNFCBn7rm6ptfAaIfqqu6FsxH/brEWkA6xb09e4XGfre+9LalX+FGS9swczHzdLoaBMGVxn3pop+av3Mx8cP1X18Q+
9G2bJ/t7b5v82W53dfPP2HgXiNdk/HkHSGe9xn1jqn/40+tLG7YtvtwL2lpHXlVv0//uVVMFCd06/NSUPli6Ktogja9Nbl37FfEP
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
S8S+SWXPAPvDRhu0j7g3y0zCxxS0IP7tCKl6yvXfPt690nh6avfq01O7V83v82LOe1i7TDuUtQXt0B7uhbSYi0uPuKdD7NNg/Sst
4p+e2wZ577wHdmzSp9eXNhzYsUkfLF3NfH36+Hv9j69NbtX03ntlj6eQr2jswzOgO09P7V713Qu2LxZf1heLL+uNQ7uH/jzXfT15
94GvDYh/c2L7H/qe5jH+H12sP6YX0wbu2BT1sQ7fnrJ1SOLeDjPuKZprYPyTHv3+aKAPGg20Qzt4DqfFO3D3WH8ZDVz7aRH/dMre
v3jmtou9hmmErnfZaIPm0f+kx/M3jSb2ObPuXh19Txqh+83vf2Jfpz/XuCmac/vF5P5MYn9T/MJFUv96Qp69r54619FPMx5M/2P6
oFC+ttq5fa/mlleG7oOPDp/wFr8gGShGxbbNk6tPHF/0fu2BH/5uqBiJJN09Ndj7uXjhsvfPshYchvn/tIh/OlX2/xD7dpB/KT3a
IC3i370qazASsa/LvH8+vL+8vGDoHOjczIN66Ztf0ezKzaEP3nezYvKQfbjvl/pw3y/7v9/63tv9X79//KSkQRFU2/SWCR2d2KRt
mydZFyjB3sM07NxLse9ixL4ZxD+tcd6HsjHlP24WzD889YR2PfeyTPUXl7tIcDsEfpQQ/3QO7Nik+cVB7E0FHt9AxyD+zSH+6dlx
tz9nM/En9s2p+vyV8tuB6r/hnp7avXpy9nFJKoy/RBu0wVz/sf2/ROybFvIMsN0uL2CpmIqbV6WoyuPEvTvEv32+fsf+mov4N4d3
r265C1HzV25KGh7/2/dD7HsY459yRe0gydsWvA83q4t7AeXsQ3MnZx+PuvYlYl9X1Xdg4t4MxkDpsf6VBuu/6fnmoF0m4fzxs0uS
pN64fveqGetPH39PcwvnJEkL736g6Z/8uV765lc6+flvB75nsE/IM4D3rzj2e8D8lZtD72C2LxZf7n9dkmYkvfT6og4/NdXBTzoe
3PGQy26DGRH/ppj1gJD+58COTV3+aLc1N+6M/7v35snXotYAJNYBmtZ0G8xd/EyMf8JVib/EfdCUvHVI+p9usAcxjaJ+R4pfg6ff
r6bJdiD5TDHfgdADOzZp/srN0nbwoR2aw3O4W6w/psf6Szqs/6ZF/EdDzP5/xjvNiL32WXNsVsi6L8/e9uStvRiM+dvH8zeNomuf
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
"""
VIEW_F_B64 = """
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
95XcP+O538yyBlkC8592uP/a4/5rh/5/OOTZA8Ten2ox/rTF/IMdxj/2GP/Yof3bo/3b4v5rJ2n9663TH+vC9Kt9618DsRfrX1Xh
+csO/b8t4m+L+Nti/GOL9S9btH97jD8BNC2t+IUkTe4YkZa7yc7d/tvnnvlh0x9zU0i6py58dk/nri72Xsu7//ns5YXYIhjIxvy/
LeJvj+cvO7R/ezz/2mH/oT3yj9li/t9O3P13bmlV72/f3ve++ZVO717A/bc6SfFPQ/yrxfiny6QAhu/3//mN/vLPxiRJP/nzv4h9
jz/5478fxZCAwBbxt0X8bRF/W8TfHgNQO7R/eyzA2GICzg4LAPbof2wx/rFF/G3R/9hi/GOHDUD26P/tMP9gi/gPD9Z/bRH/5tH/
DA/avy3i3zz6H3s8f9li/s0W82+2SABth/lPe9x/bXH/tUX/b4sDqLYYf9ph/sEe4x9becc//jWZ7qQfFkY22r8txv92KMAwPPz1
rLmlbsJJF3/32tz5O7pyYmLg/SiO5y9b9P+2GH/aov3bYfxji/UvW7R/e4w/ATQtWvziB2dPSDd+P1AIwy+C8a//6//QlRMT2rNr
30CSUGd+hTWxNP6cjo/9zzaY/7dF/O3w/GWP9m+H/Sf22H9oh/xj9pj/t+Xff4+cvxP7XHvw6RFpRbr0qMP9t2JZ8Z9f6ejSow7j
nxow/tlgUgBjPXBrU6+1epM5564u6sL0q733LHx2T+0X9gz8Avzln43p3NVFbYbgDwMm4GwRf1vE3xbxt0X8m8cGlOFB+28eCzD2
mICzxQKAHfofW0zA2SL+tuh/7DH+scUGIDv0/8OD+QdbxL95rP/aIv7Dg/6nebR/W8R/eND/NI/nL1vMv9lj/s0WCaBtMf9ph/uv
Le6/9uj/7XAA1R7jz+HA/EPzGP/YcuMfSXruwBlJg+Od6Nf+/eK9i9dIQlwC7d8W4//hQQGG5iWtf/lxj65/Oax/lcfzly36f1uM
P23R/ocH4x8brH8NB9p/8xh/ArDkCl58cfJ85nvPXV3s3X9doYuDT4/0vu9eu/Soo0O7R7k351B0//PJo22Tz7sZMP9vi/jbiz5/
+c9cPp6/qkf7Hx7sP7HB/kNb5B+zw/y/Lf/+m1T8wnFFMI54c6Dcf8sJib+LO+Ofev3+P7/R9Kd/6H5x/oex79nM4x+TAhjSxsKK
75n2RG8jevuFPb1JoAvTr/ZtAqLhl0MCAlvE3xbxt0X8bRH/4cEGlObR/u2xAc4OE3D2WACwRf8zHFiAtEX8bdD/2GH8Y4sNQMOD
/r95zD/YIv72WP+1Rfzt0P/Yo/3bIv526H+GB89fNph/s8P8mz0SQNth/nN4cP+1wf3XFv2/LQ6g2mH8aYv5B3tHInNvV05MJI5/
nnvmhwPvRXHjY601/9Dv/Eqnb99/NBmNS5bokpZN7hiRlqVptUiCWBLjfxuM/+1QgMGeuwbu6wvTr7L+1SCev2zR/9th/GmP9m+H
8Y+tpPWvt05/rAvTr/atfw20fbH+VRbt3x7jTwCPAzf/cGj3qC4trRe+W+l/z6VHHZ19/XnN3rrf/Ad8DLVf2KMpde+7Ur75H4pf
VIf5f1vEv3nRBMTSYIFTNwfB81e94tp/dP6N9l8t9p/YY/+hLfKP2WL+315W8QvHL4Jx+uXvc/+tSGjxkeee+SH5byvkj3+mP/2D
4taCr5yY2BLjH5P/iegCvNQN/KVHnb5FGGfhs3uStKkCb218rLUWfe2rG6f6BqLuIUASG7AqRvxtReN/9+LhvgloifjXifjbcgfA
nOgCjET86xTdBJQ0AScNTkIzDiqP+6+duA1wkvRX//f/25cAQoqvACnxO1BWWv/jNkO7f9L/VGt8rLX25JP/rUePntJXN05JCl8A
2Ht8Ru7vsvm8GPofe3H337gNuBLjnzow/rST1P9Er4EUvwHFvZdrUBzjHzt+7P0FrXNXFzW3tDpw//UTbrj3cw3Kof+3xfyDLeJv
h/VfW8TfHv2PHdq/LeJvj/7HFs9fdpj/t8f8m624/T8hCaClbvEq1h6LY/7THvdfO9x/7dH/2xkfa625w6TuAGqo6c5q7yAq16A4
xp/23mhPJCaAlph/qEtcAtzo3NvCZ/cSk6NMd7pJsOh/8oub+5Q2roGkvoPw0eTDvtnlDveBghj/22H8Pxy4/9pzvwsuznFY/6oW
z1+22P9sJ2v8OXDvZfxZOdr/cGD8YyNp/cvNN0T7IEkDCbBo/+XR/m0w/gRgYXystfbVLydjx/NRbnzv7r2uWMPJo21NnrvZ/96p
/bq9+ECzt+5zf1j3RntiLTqej1r47F7suD/6Hqkb/6TiF7cXuzcR4h8muv/50O7RXPP/c64QzDruxfmErr9EiwFI3WtFGy/Oxf7I
+Tt9a7vRe4Lr/yWev6oWbf9Za+3+HlBiX46bA/3t0//de43n32ax/9AO+cdssf/B3hvtibW5pdWgAhjSxvrYlRMTxL4CSeuQcfzY
S7T9qmStBbsiGNLmHf80/j+S1vD9TaAOjb56JCCwRfxthRwA8BH/ahF/W378f/v0f4sNuM2jAIkd7r+2SABhiwk4eywA2KH/sRV6
/2X8U6+QDdBuYd5h80l5HACwxQEkeyQgsMcBGBvMP9gi/nZY/7VVJv4SfX8V6H/s0P/YIv726H/sUYDEDvP/tlh/tEcCaFvMf9ri
/muH+689+n87HEC1xfhzeJAAulmhCXD95LdScnIU+qBwWYd+/WsQTT78g7MnpBu/5zpUiP0PNhj/2/PbvqTgBHzEvBrR+PtjIH/f
P+vv1eP5yxb7n20w/hwOtH97jH9ssf5li/Zvh/HncIpbE5ZIbo7NI7QAxuxydx+uK4Dh5h8kpRZhoADDhpC1Lam/CIZbb3See+aH
ffEn9uUl5R8L3f8zt7Qam6ie+0SY0AT00TVIiVhXwY1z0oqbOtEiSBLPAWVF23+0P0maY3M5gIh9cdG+PyT/YVwRHvqfcth/aIv8
Y3bY/zAcihRhIP9VNYrGXmL8U4U8a8Gbef6/0f+ZkEYfXYSPogMqJ28CgigGPuWQAMJWyAGApA2IxL884m8rLv7RSSDiXy8KkNjh
/jsc2ABnhwk4eywA2KL/sRFy/40m4WP8U5+kTVruGSBuo5DEPFBZ9D92OIA0HEhAYI8ENM1i/sEW6192WP+1Rfzt0f/Yof3bIv72
KIBkjwIk9ph/s8P6oy0KANuLO4DE/Gcz8tx/OfxYD+6/digAYI8DqHYYf9pza79zS6t9ryfN+zi0++JCDz1K+ZKjcE2yhR74jV6D
kERlXIP8SABqi/G/nTfaE2t+Ij2XPC8kAZ9D/It7oz2xFh33SN21Fn8flt/v+Ih9eTx/2aL/bxbjz+FC+7eTNv6RKEDVhLjnL9a/
mkH7t8f4c3i4hNBHXz448L2ZuU/16NFTkph7xuNvfKy1du/LW3qw/5XU9/mJz7OKLzgUYRj0RntiLW1u2YkWwXD8+E+91tK5q4sD
1+H24gNJIvYBQgvA+/x5OD9Zvf9szHNwmNAE9NECnD5iXZyL/5sPHwbN70gUYKhStP276yCx1l63pL4/Lf+hpMQiPBLPBEWw/9Ae
+cdsMf9vL2tN7M2HDwdeo7+vRsh6JPGvR+ha8FaIf2P/M0UqviQNPDkEX0yeBARS8sB/s/0SNIUEELbyVD2S2IBYNeJvKy3+cRPR
xL96WQVI0jagE/dy8o5/olgAqI7bdOL76sYpNsA1hAk4OySgsUf/07yy919p803AWXMb0aMLwCHPaVyLckIKALiiDA7zP9Vg/DMc
0gowkHysPtEDSGkbgHw8AxfH/L8t1r/ssP5rK0/83caHtI2fXIP86H/sVN3+uQb50P/bY/xpjwIkw4H5f1vMv9mhALAt/x6QdADY
RwLW6uS9//IMVo8891/WAaqVtwBAHJ4DyuEAqq0848/o7wBtv7ho4Qv/Xpx1/2X+rbi8CXBdcpQfnD0h3fh9bHIOknKEIwHx8CAB
6HAI2f/G/Fu1om3fiRbBcPwEfO73wyXrk7gWebniF0kFOP1ia5KIfU14/rJFAvRmMf4cPox/mhcy/nGSzr9LXIMy/Gtw9vIC618N
ov0PB8afw2F8rLXmF76Y+/1nse9b/mZFjx49xTgHjy0393Dvy1uZ7/1t62Bf0vOs4hcSBTDipJ1vjHJzO9G+3hW+cK9Hi2AQ9zB5
CsA7/vx/UvELh2fhdHkS0GcVBSDW+UWLX0gb8Q1Z52XfQzlx7d8vRMJae32y+v60Pkiiv69S3v2H/poY+8/LowDJcGD+34a/BzHp
nuCPkRz2/lcjaQ+Ej/jXIyT2Unr8N9NzwFAWwEirisfDWDHE3xYJOGzl3QAU3fgc3YBI28+n6vhLPAjkERJ/NwnkizsYRvsvJrQA
SdIGdIfY51d0/OO4ey/FSMqLuxbR4kc+NsBVjwRAdkhAY4v+p3lFEiBKHICvS/QAktRNgn7k/J3MyVGJIhhVSdog5/r9pAQRxL08
CpDYSyrAIynxkLBE+y/KxdttoL29+EAnP/o89r0kQK8O8/+2WP+yRfxthcY/OvfJhuhq0P5t1dH+uQeHo/3bogCSvbwFSJISEBD3
cpj/t8f6oy0KkNiI63viDt85/j44Yl5O0QKESWNQxv/F5Ln/Rg+iShyEqUJo/7/3+EziOgzxLybpAGr0Gkjde68rFuDj+au8rPVf
1uCr5ZLvTZ67mevwI3NA5RWZ/8xKfisxFgpFAuLh4PdBUYd2j5IAtCFxCdCTMP9WjWjy2+jvwNnXn9fsrfsDcz1J14azYPlkJR9w
fb9LOikl/14Q++LyPn8lvZfYF5NVgCqK/r88xp/DhfFP85KS/zuuH4qOfyRxBr4icdcgWgQjrQChQ+zzq6L9k3+jPMafw8EvfpFU
+MJHEQw8ztz8w+mRUU3uGIl9z+xyR8cW57Vn175cxS8kCjEkeaM9sZY0vvfXHP17q3Nh+tXe6+7fpf4iGMQ9W97nX7f/1l2PaPGL
pGT1PA/HC01Af+T8neD1R2Idzo+/X3QhFGvu5aQVv5BYa69bnvyH9EH1y7P/0Ef+vfIoQDI8sgrkRds//Uw5/hxo0j7EkPOnXIdi
QvaAEv96hBR+kbbW+esnrT9AVNZDweSOEWlZml5a1RvtibXNcBGGCfG3lbb5f3LHiCY10u2E1FrjJlAffyLafzBrv7BHU91/pe3X
KG7jidSN/4UX9riFAK5BhY6tPBW7AOOj/ReTNQHnYj+l7iSPS7zqJ2D1kqIQ+5okjX/cuOfI+TtuQohrUEDS78HBp0eklcEJn+gG
OMac5SUlIHjuwJm+yU83Kbfw2T1NvdZi0rMi6zFcm3qt1Tf57MfeLQDcvXi4L/kPk8/llO1/UL9Ljzqxz8A8/1YjuiHLbfQp0sa5
HxfjH4Bx435/wTepjzqoke4mrTHaf1kfLtx5wl8MDkp+srSqcWJfWvQAmPsdSCvAQ/svJ+kAvB/v4Pln5v9rwfy/Lda/bBF/O6Eb
cv1rgGrR/u3kbv/cgytH+7fF+L8eoQfw/Hlot9lf6k9AIGlNIgFBEaw/2mP90d7c0qoU2ePmH8Zur++xar+wRxemX6UASQWS+h5/
749b85UGE7C6OVPin1+e+++lh52wMSjj/9zy3n/T9mIR/+LcHhT3dVz/H1f8Qtq4VqzBlOcfQJ1bWtXe4zN9Y6C4w0puHRLlZK3/
sgZfvTzFL5Lm4JgDql+e5CjA4yDt8LW7p8YVe5QGE4DS7xQXlwD9rdMf92KclgCXZ+Dy4vb9zK90dPKjz7tfpOwDjRYJQ7isxAO9
56r1JDR7j88MPA/HFWhGcSHPX3MbZ7763o/80gpQuXsA/T82M8Y/w40z8PVIKsBw8mi7WwRDyetfMYUJiX1NknKfSOTfqBrjTxt5
i19I0o6xp7X8zQrnv2oyPtZai3udWJfnn/nde3xGk4ovgCFJe3bt6+UdCC1+gXRuL1VU3FxaXBFmx+3LmnqtpbOXFzS579nqPyz6
io5IG89kbl3si5PnrT7apnRs5anYxPNJhUYk9gE1YefNT/Rg/yu9r9fXxhj3VyjvWjtrj/WI5j8M6YNQTNb+wyPn70je/UCS3rt4
rS8fIopJyj8WV4DEPQe4PRHkH6tGUv4fqX/+P9r+p9V9Rma8k18054wkvbTwqa61X+59HXz+lDFnbtH5/2jsJeJft5NH25qLWXt3
ttr566EqgBENftLAc7NdhGFBAhRbJOAYHv5GLH9AevfiYTZANCB66BrNOLbylOZXOloc3zaw+cGh/dfDLQJI/Q++Uvfh122OmOq+
ROwrFjr4pwhGMVlJCHoHAB51/GIvfZNzbLwqhwRAw8FtbPORgKZeZfofhw3o9cp1AJ7n39yixS+kjfH8uauLqQf0fP5hPeSTVIBk
av3rrGtAApryKEBix2//ru3/7vLbeu7AmaD+h/ZfXlwSiCLz/zwPVIf5f1usf9li/Xc45Nn4SfyrQ/8zHGj/Nhh/2qL/GS7RTekS
CQjKYP3RXpn1R2Jejd41WJF++/R/Ky4BtEQBkipl9T1+EQwfyX/spM1BIL88918pvviFwxxoeUUKADiswRSXdADVT3y18Nm9xGLw
xL68rAOorMFXyx1+TDt85+PeC6BqSQV4+vazkQC0NnFJcH/U2ilpIwE6CXCrl1b8RYrsbVsvwOAn5Xb8ZwTOgYUrUgA77QwYsS8u
mnzp2n8+kKSB5y8/AZBDAqDiQgtQueuw9/jMQMIrb12Gdp/T/Eqn27+kfN/33sVr3Xk2VIbxz/BzsY4b/7gzetx/q+UXwfAl7YFY
fx+xr4Hf/qOiBfDYf5Vf6Pw/4896jI+11vqerfa+kvzmBM/9ZpZ5/4q4wheuIIlvZu7T3veJd3Vml7tjfTe+d18XdXvxQenPtFn1
+nsptghGkqTxv18Ew+Um4H5QrWgRPDTHX++l0IidnTc/2fhnq3tv5tnLhn8NKEJSn7ml1YF1l7Q+iH2Ixfj7r6L7D6NrX+5+MLlj
RJMa0exyh3hXIFroNC7/mFt/cbnKDu0eZaxZgmv3bg3g9uIDzd66P7AHMaT9cy3yiyvo+NLCp5K6hR/Jv9EsF3uJ+Fsrkn/jcTc0
BTDiDl8HDTw3wUUYBnHxp/qmDRJw2GMDoq20zScSE3F1Whzfprml1YFkBF/dOEX8a+Tfg6X+hwB3v6UIRj3yJv+hCEY+RQ4AXDkx
Ebv4O9X9V+KeU5EEQG6SNJoASGLRvai46zC/0tFzB870bYLzE9D4GPPnV6b/kfrb/7mri1yDmnEAvnpxxS+iG/rPXV3UsZWncv9c
fhfCpBUgcYuNbz58KCm7EIb7ecQ+HwqQ2InG3rX95w6ckbTR9iXaf5X8g3dJh+CdPPPPbMaqHvP/zWP9yxbrv/V7aeFTXWu/HPu9
6NyzRPybRP9ji/Zvq3D7J/6VY/w5HOLW4P31AYRj/dFe2QLkFB8vL3oN/MILrgDwV3/8r973n3vmh73fA+JeL3ctfCT/adbAHqyE
ZwCev/LJc/+99LAT9CzANSiubAEAiXWwMqJJWKMHUJOKXzjEvri09d+suPu4BvlkrTuG3nsliqDWIZoAN0vZpFlbTdr6i1QsAfGx
xXlN79pXyefb7OaWVsPuqV4BgLQzMBLzn3nEJX92/CTQLiGKRALcKmXdf6X++c9Du0eb+WDoc+nR4POvNHgGDMVE+yGXhCYuAVD7
hT26MP1qbDJo5BdSgMolXko7fz3VfYn+P9Ch3aO6tLSqg0ofT1561OnN908vrWoy4/2MP8Mx/rGTFvuo6Hk7X7RIPKozue/ZzPUv
CpAUk6f9S/H5NyQN5H8gUXRxIQko48aftPfyvpi5oQNfLve+vrFrR+bfce8PeS/CjI+11vzCF3O//6zv+zvGnpYkLX+zonHWWSpx
9+LhjXnNjV8BTXe6e2mvnJhIHQNFueIXs7fu0zclcOu9FxIKYPjx9v89bvyPZhD34eYXBUA+aWuLrvCF82B/f4Ewnr2a41+LY4vz
UusguccaQM6ZesQVADh3dVFaH+f4eVeTrgH7Psvx54LOXl4YKEAiqfd84K/BvHfxmqaXVnkOKyip+PXJjz6XtF5kxFv3ymz/7H0r
7cz3X9TBp0c4f23A3wtH/JsV3YtYOP/GYx7/RgtgZG0AlRh41ilv/Km+2RwScNQvpP07bECsXt4DAFFsPqnfmw8fSg8Vu/kwmqAb
1XH9/7enzgxMODsUwahH0YevI+fvcEigRkmLvyzA5FckAdCh3aOxm28vrG/OEvHPLek6+HH3xSVhIvbNSNp8TvuvR6ED8I/5BFxT
4govSP3PVGWKYCBb0jVIWmxMK4ThHxhjESxcWgGSIpv5iX24pPafdNjxzYcPEw9s0/6rVXT+mWfgajD/Xz/Wv2yx/mvvpYVP+76O
Xg/iXx/6H1v0P7Zo/7YogPR48BNg+fwEQKyB1Y/1x+pUVYCEdZfikq6BXwTj7sXDeu6ZH/a+5xeBpwBJ/Y6tPKX5lY4Wx7clHsCm
/6kfzwH2eBaonuvDXd/ikv9Hi2Cgfh8u3HnijfbEWvQAKgVI6lP1+i+qx723HqHnX0IKL0jdhBx7du3Tod2j+nChik+4+UXXX/q+
J/XiKXXn1o7dnG/mg21yReYfpME9Wc8dOCNJvfMX3DOKmTx3c+C1s68/L4mYDgsKMDcv7iySzz8Dtp4ECzkkJaGRpJ8cfXeg2LWk
XvJh/5lZ68ULmX8LF1qA6khCEiDOP5aXNf68tGtf3/03mgwR9Usb/1AAoB4uibMUPv7kGoTLU4DB3Wfjik6RA6J+ocnPaf/5xSUA
nb11f73gSP973fhz4bN7mnqt1bcOT7zLccV7D+0e1UsPwor5nh4Z1XRnlcK/FfGLX0QLX0TtGHuaIhgVcvM4/vyO2+vjj39uLz7o
PR/HofhFPu7e6q+zu9dc3KOFkZJ+hkPcsZUwJ1HO+9u3682HD2OLm/qxTcpDJjH2r0poIRKKkJRXNv9kHIrwhEtae/lRa6duLz7o
m+8J3QPEs3A+0Wtw8mi7WwRDG2NSvwiJtHEtJneMaFIjml3ukHcpJzfvExUtCO9y/nwxcyM1ByXKm53ar8lzN/uKwhfZc04fVMz8
Sqe75ush/s3pWwvetU/S1tt722gBDCllAX79AqBexN8OCTjspSUAml/p9CUfYANi9fIcAEC1svqfgQTEFH9phF/8QupOqoUUwaD/
ySer/XPgengc2j0aewDjqxun2ACKx1LWIbzegfZHHd29eLiXnCDpwLZo+41zG9AdJt/ChR7A5hl4+L208Knmv/+i9cd4bKQVv8ha
bEwrBIBwSddA8u6pVxelleyfRQGGfELaf9x8A22/WtEF9yjuvfVh/t8e61+2iL+daN/z0sKnG9cjZ/zZ+FkM7d9WVfGn/RdD+7dF
ASQ7IeP/tARYrME3J674uz/3zxpM/Vj7qk7W2qNfBMPfV0IBkuYtjm8b2Ptw9+Jh+p8hxfw/HgdJyf8vvLCnt9dkyuajbTn+gUi/
+Eh0vxuqU+X6L/A4CkmAO91ZlZY1kJiDxDPFHdo9qj279qWuvSddm7RENCTjq160AG3cnizOX+TjJ96I24Myv9LRyY8+75t36yYF
jZ+D4/k3n6zk876DT4/o0sPBIsx+AWYUE1qEPG0dxq0DHDl/h7OSOaQl4XZJPt86/bF+9x//3nv9J3/+F7Fz0O6ZWfQ/QUILUOU5
f00RjPzOfP/FgaQzUvf+e+oP12P/TtL4k7FnuGjfk1YALG38QwGA+szeut8X77gCDKiHX4CEAgzNiysAs/DZPQpiVygkAeiF6Vdj
k9JLFGCr0j88eijpKf3u8tuSwu+r08dnen8XxeUpfuFQBKN6bi4nKdeAGwNFi2D49wuKX4RZj9GapIF19rjYxwkdG2FQ3gTojH+q
FbL/uWhBAGSLxn92udOLdXRt149v0jwPz1/5ROOfVIgk7Vr4iH9+Ifsf0vogiX0QRWQVQP1Ra6dOfvT5wJpjUhEAtw4wvbRay+fd
SvwiGEnFx3292FMEI5do+48rftG37yQlB6Xf/tl/Xk6RwkcoJ674CJoTkodvK2i0AEbS4nsRJCDIj/jbIwGHnWj770sAJOnNXfvY
gFiTPAcALky/qrdOfxx7GIzNt+Uk9T971tv+t6fOBBVf4Drkl7UA8GD/K9p58xN975PL+t7hA5kTEPQ/+cW2f+69Q8NNRswtrcYe
wHjuwBn6ngbEJQCSOIBUVOgBAJdYmwN2tpIK8Ny92P2na/9ucyLCpC1AkgTRTrSdz6m7sOj6rNTrhkKSkv/7ji3OS62DFAIoKSn5
iRvP+O0/2vZRj6z2n1YEgwI8tngGLob5fzusf9ki/rbmVzp98Y/ORYduPkcxVW46of3nl9X/sPG5XrR/W6n7Hxh/NiKtAElIAix/
DZ71geqlbYYm+UxzktYfJQ5+1cUVwfBRgKRZbz58KD1U394Hl3hSYt9VGXkPwANbxZHz3bHN3Po/WW+sT3Qt0i8+cvfiYYpg1CBr
/Vfq39NzbIUEV3UISYISgvmHfLLOX/gJcF0fdOzm/MD73NkAkt8WE12D8V93+xlcP7X3+Ix+2zqYOCfNNahenjk4zl/kF1f8QtrY
93xpaTU1yZs/B8dcRD2Sfgc4/1XO/EpHLyl+DSAu5knJfyQSAOUVl4ApmoTeJaB/7pkf9r0+eAbgcNUfD8pfAIY1sHxc0hmtqG8M
6uY99+za19e23zr9sfbs2qcbu3Yk/szpzqoO7R7Vhwu1fexNJ6sAGAUAsBXN3roviTN1VuIKwFwgAXTjspLSU4CtnK+/WXxifKy1
dmj3qH5y9F1JGig8El2HcfM83XPB3Z/R5GfeTMbHWmt9uR325k9m/txvZkm+2gCXi0naKILhil+4+zX9TzgvVmv+60WKX5y7ukjs
c8pKgO4/A0fHP9+eOqOdp9J//jFJ0+QxSJQW/3vqxl/L6lvzovBFdVz8/VgfW9xY502K73RnlXnPCgy0/137EguRRK8F673lZJ3/
ctdmurMaXJRkdrnDHGjF/Ln/tCIADgUAwqQVIXFFMJy09ReUl7QPQiL2TeqticFE0TMX7P8sJ2kfYqjNEv/GCmAc2j2qS0urA4vv
PhJw1MfFP63iDvGvT0gBABJw1Ceu/WclH2ADYvVCDgBIyQnQ2XxbTFr/49r+t6fOSApr92w+LCY6AbrHK7ojrU+s3fxEeuWodp5i
wr9KZRLwce8tL/Tw46VHHQ5gDCmSADUnbvMbBUiKc4d8Q5KgMP6sVsjzbx6bZQKuSQuf3VM7ZkOzn4je997Fa3rz4UPd+/LWwO/M
/EpHlx51dPb153sb4RAupPiFG3MmFcE49YfrusRmq1Jc8Yu4vv7Nhw8lUQijDiHtX+ovgnHvy1tNfbxNLek5jPnn+jD/b4v1L1us
/9ry4y9tXAP3vPvzJ0d6Gz/jYs1m3PKyNp3Q/uuTp/370jY+Ix/av52s/Q8S8a9bWgESfx04awM0CfiKybP+eEjE1cri+LbYA8Fx
yYrF+leljq08pfmVTuI1kIh9UVn9j78HUdq4D0zuGNGkRjS73GH9saSsA/B51lOOLc5z2D2HkPuvex7LmgtFPmkFAJ47cCZx/Yu1
r2rFXQe/8MKUxYfawvz9bH7CqzmtZrb9lxY+7duzjjBpRSCT+n3mH6rh7q9ZCXDvXjwclPz2yokJElYGykpAfOlRp29sf2j3aPd8
0XL3a/d74c89b1yDUZ7FMuQpvhOahGDqtZbEc3CQtKQP0kYRjOi8Jgnoq5NnDoLzX9Xprb9EYt9bA1ifRwhJ/rPz5iecCyvBJTzx
+yKXgF6SrpyY6BWETDoDIHX7oanuy/T/JRU9f80aWD7+GNR36VEnMY5uvBk3/kQ+IQXAxPNUo1xCZ8dPNJx0Zgb1iBZgQHlpiQ+l
wfaP6mVdA5dc/q3TH7s5hVj+HggUd2j3aF+c3zr9cW9eIVoIY+CaXF0k2W1JX8zc0IEvl3tfp80zO+79Ie/FoKSxTHS842u/sKev
CIYze+s+xRdKmnqtlXk93PcpflFeaAJ0n/udcethWWdQ9+zaR3GkBHkS0IcUZvDnIUiCni0a//e3b9ebDx9qer1dc8arXnHt312D
Yzfn+15PuhbRQiTsxQ2Tdf40mn9ydrnT1/9I5OLD5haX8yppDaaX/1YtChHmlLUPAs1ya2J59pyTf6y8aPER8p80I2kf4lY8/9tI
AQw3+X9SStwA6hIQRB98HX/w6T8MUHktn6QN0HniL1H5rqis+FN5sF5pBwAkNiDWKfQAQFJyRBKgl5eWhObB/le08+Yn+vaVo0EF
GFiEySdtAcBv5+46SNl9DfEPE5IAMSrp3ovi0hIQSNKbGYmAOIBRTtYBmKIVOdEMNr8V4/r/U+rvg/zfBX8cyvizHmkF8CQOwNdl
fZy4diGy4SotEf3kjhEduzk/kLibe0QxcRsQkw57+e3dH3dmjZ+QT9pcg0s6lpQIiAIkxURjvvPmJ/reJ5czDztWWUBpq4uOgdxG
LBJA14v5f1usfzWP9V9bA/GX+g7AX3q00ZfPLnd0TOlzncQ/v9ACDPQ/1cvd/gM3PhP/cLT/4RAy/gwtgET8w6UVIMmb/EfyNqAv
rdb8yTeXrPkz/xAMifeqFZwA/eltsd9j7asZFCCpT1L/k1QAyd2LH+x/hfXHElwB2p8/OZK4/njqD9clddcg48agKC8t+bm/ruie
BbIOJFGEpBy/+EXcXoesIhisgYVLKkIi9RfBQLPcON8//OsKwEgbiXJZey8vbg+0i+s9dcdB0WQQUvL8AwUYsmXNf0r9CXD9ZEsk
vy3PT34YkoDYj7+fjNsVwpDWx0fqzklEk2MhWdr4M1qAkATc1Zlbyi4oJUUSQat/r5A0mIAe4eZXOnpJyb8DWcUv3FmkaNtn/idc
dP9zaEEeiT3QVUhLQH9QI5pf6ejI+TuxhWilwWK0nEHKJ2sNIOT8NfKJJt+OJp6RpLOvP6/ZW/f7xpJTr7Wkq4sba4zp40/WATKE
FgC7tLTaS7wtsQ5ZVlbyeamb0HnqtVbfGY0pdefjomdmkE+ZAgwUIGnG7K37vTVfCsDY8uczo+sF/h4I1uCLeaM9sRYtMjL1Wktv
nf5YF6Zf7SsCHFeQhKKn5bl55EO7R/XSg7B55dMjo5rurDIHXYA7/zsl9fXnrq8/d3Wx187jvh8tgkHbr56LtV/0Iu7+S96lfNz4
M+7skeMnQHfXYeq11sD4/7etg7F7UuiT0uVJQO9ywKWdQ4oWBGAOIl1S/N18xJ5d+3R6ZHAdy5/nicMYNExa+39/+3btWd9DdXpk
dKB/SSp+gXxC808ufHZPR87fCT4HKfFMUJabA8qThB71YA2mPllrAKHtnwIM1XL3hmj+DYe193rMTu2X1P29yJP/BOVE9yFu1fPX
jRTA8GVtAJ1eWg1+8GXzc5g8G6Cz4i8x2ZNXaPylsAQcxL+Yvo0/K+nvjcMgqLys/j8tIevOm59ocv8rJEAvKG4CKLrp3/U1aQUY
SL6RX94CDHmKYCBcNAFQNPF2yAMX999isirARw9gZFWf5fBRPnEHYJIKABzS6MDGW4nNt3i8RQ9f+L8LLyk5EY1DAZ7ishYgpe68
TtYB+ME5oFEWHgtIe9aSNp4B7n15ayD5/KVHHc1O7U/dvI4N/gbE6AE7qX+hMa74RbQIAEVIystq/9L6YkDroN58+FD3vrzV5Mfb
9FzxC0n69pWjepBjsZ32X5w/Bnpp4dONMdCufbnmn1mDCcP8vy3Wv4YH67+2/A0njjv8Pre02t0EkbDJXyL+RYQWYKD/qV9a+78w
/WrmwQuJ+OdF+7eVe/wp4l+XuAIkTujGc9aDi8laf3xp4dPe78Hc0iqJ92qQpwAJmkcBkvok9T9ZiSd9rD/mF1KAU+qurYQcvpYY
A+XlCpD4a4h9c8/aWH9399e9x2di14JRjaz1L78IBmtf5SQVv4gtKnV1UfNfd1LHqg4FSMqJJth2vwd+olu//Uf3y7l568f5EFhT
kvb/uJj6a7rce+sRN/8pde/P0QSgh8KT3yKHrATE0QSs/njIYQ4iv+jzV3T8qfX7qLsHkPzBVtZ9mWfgcL3zRzH7n19a+DR237N/
/iJ6FokzYPmF7H+OE7cfFPllJZ+RuutgIXNxnEEqLq0IVSgSAJXjngOkbvIxVwBA6k/AKonxp5G5pVUKgDWo/cKevufZ9gt7pIz9
bSQArUZcAYa4BMRRxL860QTcU6IAjAV3H2Zvbf1+/5/f6C//bEzSxv3Wv6/OLa1q7vyd3jyD/34U9w+PHkp6Sr+7/Lak8L0l08dn
en8X+fhnUH3nri4OFNpx/OIL9EvVcdfCv7dGC13EFZ6i+EVxIQnQr5yYGHj+dWsybm+QltV3PsY/E8NacLI8CeivnJjoFWWgIEA1
0uLfS4AbQXyrkxX/S486vSTEUbT14vwCnFnnT3t9/Qt7EvsfKbEAD0pw57+SktBHHVuc1zR734KEFAGGrfe3b9ebDx/Gtn9yDzcj
Lv+GRA6Ourn7ckj+E4n4VyFuH+J0Z2udv268AIYUH/hDu0c1t9QdTIY++DLozC9tA3RW/CUSoJSVFv+QBBzEP7/oA7A0GP80bEAs
J/rwldb/JyVA9zfguiIYbD4MEzIBFN3sSQGG6rj4z527GZsAJanqY9I12EwD0CaEJADqVb9TWB/P/TefrArwcUkg0g4gcQAjn7QD
ML1/V38SiGiSbrf5loWYYuZXOjr1h+upG/5J7Fyv+ZVO4uHr6OEXCvBUI88C5NRrrdT5B4c5oGLcAm80+Uncs5bzYP8rOj0yqjcf
PtTPnwxbnMQgt+nNfR1X4NGXNA71Nwy5g/PI5icXCC3+Im0UwYgmcOJeXV6ReQbafzn+GMgfi7pCRyHPwNx/i2H+3xbrX/ZY/7UX
PQAvSdvab+u7hXd7c6HEv3pJBRik7iFg+p9mxLV/N7eZ1f9IxL+orAI8tP96ZY1/KIBUn75xz0r6e+OwCbq4rPXH+ZVOr/hCSOI9
1sDyy0p05QqQHBJrKnV4aeFT1h6N+P2PtNEH+TGPSzyJaoUcgMwagzqMgfJLmnt2eyPiZM2FSt01ZhJDhAsp/i5t7HWIrn1J/X0X
8S8mKfHPpUed2LFqVgExhEv6HXDPWX6iZ9Z+qxGSBJr9P/WLS4B75PydvufaC9Ov6q3TH/fWJR3/PSSgLCYu/nNLqxpIiOWNLZlz
KMbtP5w8d1MHveQC0fFnHiTgLiZrDkIKS0LPHtxikvY/O3FFmDn/WE7I/mdp8BxYWtw5A1Yv5uKqN7/SkRIK8CggkRXrX/WKjv8Z
f1ZnbmlV72/fnjn+Ofj0iLQSVpiTAmDlub0/kljXNRYtwMDcTv389p/V/8dh/qca/nVgPbF+564uauq1Vq+YhV9oVupPev7W6Y97
r//ln42RhL6kr79ZfGJ8rLV2aPeofnL0XUmKnWP2v3ZzPN19it2f0eRn3iyiZ1CljcIv0uAY378GDvNt1fDj7jD+rFfa/p9o7Nsv
7NGFF/Z018DWx6R+EQwfe4GSFUlAL0lX1B2TUhCgOiH5N6SN8RHKy5v/5Mj5wT1BtPXqxJ0/dWeQ/KJTIQWPuC7VS0pCj/ol5aJM
w97P/NLWAUKKMLD+Wz13XwgtAMCYv1pnX39eJz/6nPg3KG4f4lY6f21SAEPaCLyb+J+9dV/b2m9r7/F3EycZJAadVYlr+HHxTxv4
s0BZXFz8QxNwEP/yovE/+dHnbEBsUFz8kxKgx10HEqAXFzcBFCeanNK9hmLiEqC4ystJVU+TEoROd1ZZBC4gLQHT9FJ68h+Jfr+M
kMOPoRvNOYBUTFoBAJeAIOlgsLvnslE0P5cA5ZTSD7G/pI0iJP7GK5SX1v/EHbqLK8Dj7sGMP4tLSoA7P3ZCc+ez5x9QjNv8Nnf+
Tq5nLcl73up027v//IZwHy7ceWJ8rLUWfT3vIdNLjzqandrft3EayVzbn5L6NjnEHXQMuRYkQMnP39zmy1MEwy9+QfvPz917D8bM
N1xrv6z3t28PSgCNcpj/t8X6ly3Wf4dD9P4ZLYIRRfyrEdf/zI+doP9pmN/+Xf8jKbX9SyL+JSUV4KH9NyNp/EMBpOpFD8BIgwVI
0pCArBpZ649xawDRfQ/+GhjJZ/KJrj1Gv+cKkEiDB68Zc1YjZO2RAiT1iNv/4/c5TnQtJtrnk/yznLQCnHEH3VmDLMeNf05Kqfff
Pbv26cqJid648sqJCe3ZtU83du1I/Nmb5SBGk6L7e3be/ETf++RyYqJP19+8+fDhQBEMipDXo7dfaGGwKExc4m4OoWbz1x9DC8BI
ye2/fw2S+IcKSULjz/+7+y/33urFzX/GPWvx/FW/pPgn7ZtAfu5+mbT/PA0JuIt5oz2xNuftk3VzEFmFMEg6X63ofTdpLs7H3HP1
kuYfppe66y5+8pO4mPvrMId2j+rDhXo/72bgEtCnefPhw8S5uDicAQiXVIDcvwfEJV+K3nPpg6qVtP/BiSalRHlZ4x8KgDXL7b3a
1hbPXw0LKcBA/OuV1f7RjNlb93Vh+tXe15z/rd4b7Ym1311+W5J6xRekbgGGZ9oTvYLk7Rf29PodVwgY1fGTbUvdtt4397/OnYPv
S8Z9dZFn3hLcGdTD57pBPCzpowvvS+rv//cen5F7j7z3zC30PyMgPz/+Unz8u1/PNPzJNr+k+be0vCb+GDRanMe9xn7oMKEJ6Nsv
7NHdF/bE/g4wRg3n7z+X0uMv9Rd+mVr/ftLzF20+v6z2f9eL9cDYJ4L4F5N1/s4XdxaMc5D1cPfWtCTomy0J9zC4vfigl4A+KRdl
1LHFeU0HFC5HPP8shlsLeH/7dr358CHtvya3Fx/oR62did87+/rzvfwbEmcgm3Zo92hi/P39n8S/Plvp/LVZAQzf7K37unvgA2lh
fjAJQQSDzmrFJUBJSwLBwL9aRRJwEP/quPizAdFGtP+JbvhhA249/EQcaVUfXcz9BJW/JfF8YUkJUGaXO6nXwCUG5RBYNZISME0v
vJua/EfamHhAmJAK2KE4hFRcVgKgPeuTmWmbb0kAVM6Z77+YmgTIFSHZDJMLwyJP/5O04dzvd7KSdCNb3AKkFDb/IDEPVJRfgKHo
sxbFL8rzn7lC4u6PP13iDeQTVwDG+eLkee28+Yl2ntp4La4AzJsPH+rnT3avG8l/wrnYX0jYSOXPM2QV26T9lxeXCMK97opyZiWA
RnnM/9ti/cse67/1i9v44xcfuXvgA/W+2z6oFw/u1fRUW1HEv1r0P80Ibv/rbV8S7b8BtH9bFECy4T+/Jq3Bp80LsQ4cLmT+PyTp
jEPymfz8BFjSxryDn3zy0qPuv88trfbNz7138VrvECR9T3Gha48SSX+qFFIAiWSfzcoqgCr17wn1UQSvuLT776Hdo4N9zvk7vbEO
idDLifbpfrH3b185qgcpyT59FH8vJs899cL0q70xT1KiRK5DuKT1R3ff/cHZE4kFYHzEvBppSWic3vy/d/9l/bF6SesvEglw65Y2
/ylJh88t6Nw7+5W0bwLh4goQOm7uIe88HMLNr3Sk9bHMSwufxiaAiEtCH703u/23JKDPL+13IA3tvlpu/sFfg3z26BVNXz5C8pMa
vbTwKYV3GhZSANXfc+ifv5bSz2CjvKT9Dw7jz+pci4x/0vqitLNI3I/L85+9drYP6kHM8y/PX/VLK8Awt7QqXV0k/jVLav/M/2Cz
8Itf/HHhTq+whUsw7IpfOK7Nv3X6477CJOtrvmtSb10BObzRnliLJnWeeq3Vi7Pr/2OLX6y/VxIFxwvyiy9cn78rKb7/T3vP+MK7
a19/s0j8CwiNv6TYAiTEvry4+be4AuS99cjIGJT1x3JCE9C7+LuCSXHjUPZg5ReX/0paL0K4HmO/8NeU+otg+DE/d3WRcVBOoe3f
Pf9OrX8ddw2If3Eh6+/S4Fkw/xrR/1Rn4bN7unJiopcEPSkn4mZKwj0sXB6T2eXOwBoMyvP7Gn/e398Lca39st7fvj2x/W/GJPRN
6d4jJ9YkpZ4Flvr3Hkb3nXMGsrikAiTR+3Dc3k//deJfLT/+7plrK5y/bqwARloCAkn6t3/+saQfr3/115Kkn/z5X/DQW5EiCVCW
39k/sLnQNX7inw8JOGyFxH/bwrymF95lA2INsuKfhQ0/9Qit+ugXYZC67Z9FmOKiE6AnP/o8tvCC4xe/IPbViW6CU/ugpi8fSU3+
6RL/M/FcTNzhxywcQiouNAGQ1F/8IuvgEQmA8nGxPxhzr/WLkPTG+FcX+w4ES4z/q5C3/6Hvqc/A/VcKmn9AdaJFpULbeHTSGmG+
/mbxiWm11iY1kqtvceNPkv8Xl1QAJm8f74ow8DtQTFLRTTfPICm26CPFL8rLOgTvngVIQF8d5v9tsf5li/VfO3Ebf/y2/7v/+PfY
v7f8DpvOq0L/Y4f2b4/2b4sCSMPp9uKD3hq8W//Nmovw14EP7R7VhwsDb0GKtPn/aELcb5v8YJvUQAIsqW/ewc03SOpLfuiuxeSO
EU1qRLPLHe09PkMfVEBIAZI9u/b1DpoeOX9HOt+fEIK4VyepEEZe7D8pJ+sAZK8Ihoffg3KSkp/PxSSy7Yt/QiJ0ngWyJRUAiFtv
SePuF+6ezRpYmKwC8NF9Pm6cs2fXPr2/fXviz730qKOzrz8ftIcaXXuPzwwk2f4io/hLL9m2tybGOmQ5SUmg/QSs0Tkg7r3FZK2/
SIP7rxwSgJZXZP7NRxLKaiQ9dx3aPaq7Bz7Q9OUjiu7LkihAW5a/7/zg0yOJCSC0a5+k/r1Z/r05z1gV/VwflPQ7EN2TFf0d8NH+
88nq/3trkP/8X3rumR+S/KRGcYV3ith58xOpdbCKj7RlZJ0/mu6spp6/ljiDXUTY/qt4P3mH8WcZb7Qn1uaWVjW/0umtu/iFMPyv
swqA+eOfyf2vUACspF7xRyU//0q0/zqEFiBZfid9nq39wh6XIJSk6BH+2d8o5n+GT3RMT79TPb/QRa8IhjaSC/trMYd2j/YVv9D6
+y68sKdXCIM+p7jf/+c3+ss/G5PUTfYc3d8zt7SqufN3ejk3/PcjP1d84b1f/En3hV/44/7+8xc9Me/507+iEEMRheK/7r1f/HXv
+88980NiX5G0AvAuAfryO/u5F9cgNAG91B2HTokiAHWIFiF0XPxd7H1u3o24Vyep/Z9bfwaeiryfdh+mzPr79fm7vX3REv1P1fx7
gIvt3Rf2dJ/DIjkRWXfML20OSOqP/5UTEzpy/k7wGgzC+GdQ/XUAabAotiTdU/c8RlIeSvbBFZN1FvjugQ90eL3v7+09jOw7J/bF
JBUgyYy/h9iXEzIOelbaMvn3GimAUTQBwe/+49+7SVDEoLOMovHXL/49NgkN8c+HBBy2wuP/Y61PLrMBsUIh8X/umR8O/L20DbjI
J2sD3OxyJ7H4ghNNRony3DXoHfRdf9hKmvSZ7qxqW/ttFh9zCt6ALvU2oUf5hS8kJv7LiB5+PPnR56kHMDiAVJ2kBEB+8Qsp/eBR
70Awm29zi06ARpMKSBubsPzN0O9dvNZ7fbNNRDQttgBVRNHCABiU6/7rJMw/ODx/5eeS/ztFi7v4145xUD7uGswudzQZKSwYxx/r
kHSjWkX6eIowlHP34uHYzQ1ONCmTWgc13Vkl5hVKS8D31R//q/fv3H/LY/7fFutftlj/tedfAye17Sss/nFJK9GP/sce7d8O7d8W
4097WfOfzx69ounLR6RlpW4+J/lPNfz1x5MffZ6YEHfnqfi/z/pXMXHzDq4AzFe/nNS3p84ktn0X873HZ3pr8QiXVPjUrTu6JPRz
5+8M/D5E1x7p/6uTVAw4CXsf8it6AHL5nf2stdcguv4+e+v+wOFfqdsnXTkxobY7ELmOa1KdPEUw/MIXqEZcQQb/fuv2B8UVrUJx
fpLtPGj7xRTZA/STd9Tr/6MYg4YpPP+2Li0BLtcgW9n49+ZBpYFrQPzDRPsev3CXfw2eu9x9vmIOrnrRIhjOtfbLml/p6NQfrif+
XfbilhPtg1zh5b62/8wPg4owU4A5n7z9/1d//K/etYji7Gl+LgG9pMTCO+71rLk4zqSWl1QA1e+H0s5fS/we5FF2/Jm0D0Ji/BnK
tfmD6m/T19ovBxcAK3pWYyvLSv4mpRd/kdR7/qIIQH5Z8R/MvyFFE0BTgKc+Zed/UD0X5wsv7NFbpz+m36nAG+3u+OdfL83EtuNz
Vxd74xu3tvjW6Y8Hil88057oK6CBfN5oT6z97vLb+snRdzX1WqtXzOLc1cW+NV3X39y9eFhvnf649/pf/tkY+z4LcsUXqkIemnyq
jD+xzyesAGRKARKeAUopm4BeknTgA527+jOKAFQoWoRQUnz812PvI+bl5Ym/JK5BAeXX338sqdv/SxQhqYMrwLP3+Lu95wA/T4SP
JPTVm711X3NLq5pSN+57du3TjV074t/L/ofCkvZASINrkz9/ckTTncHzRbT94sbHWms7/u6mZiNFlePuA27v4ZHzG/M9xL6c7jr8
/YHX0+KfNO/M2mM+fuxDxkFbYe9tIwUwpOQEBHcPfKAf/89/S/6LKQ+982MnND7GJFCIIgkgpP7NDz7in09dCTh48AqTJ/5sQKxe
SPz9zYdZm304BBwuawLIb+9pmz/9B18WYPIJPfzVK7wQM+kjbSSn/NO/EvEPVGQCNJoEVNoofPG7//h3/elf/W/GPhWJ9kHHFud7
30vr+zmAUVxSAYC4Q8FsvC3H3wTqT4D6Lj3qaFv7bUnS3uPv9pIB6cyp3jWZ3DGiSY1odrmjvcdndPfiYfdctsZzQDH+AiTjz3qU
WYDkGbg6bgPWzFS719YfBBRgkPrbu3/tSACaj7sG7/3iTzaeuQKKX8QVAPD7LoRxxUfKtH8SoBTnb2wOKYLx25TiF7T/fOLmIJIS
QTjcf6vB/L8t1r9ssf5rL7r5JDP2Umb8pXdj/hKi6H/s0f7t0P5tUQDGTvD85z+vr4G1DsY+E0c3nqNaRRPiIj9/Pmfy3M2N9S6l
J+F2RTCOnL+zvvbL82+W6Pqj1F+AxM0BRQvB+L8P0bVHd/CF+IeJm3uTNoq/TEYSY7n1x6TfA/Y+hCuz/kjyn3oNHACOHP6VpHPv
7NcFLzFNVPuFPeyDKCm0CEbcOsxGvzZB/DNE+xK/+EXS/bZ3CDKmaJW/foNsofv22edWLYpg2yo6/yZxDapQJv5S/DUg/mHy9D29
feitbjKapCTcnAPLxz3/Ju1/lqQ968mfo0L2n7/RZuyZJbr+FV1/d0WYj91MPn8RPXvB/H+YvPsfegWxI/w+h/WXfOZXOgOFd6SN
Qhj31O2DkubiHPc74Z7NmIfLFleAyr0udX8XnKzz1xKJaPIqvP/K8fZBMP7Mz7XzaB8k9fdDSbLGQIx/sFm5Z1+SD9sg/uVkFYHx
5+9ZZ6xfdA3mwvSreuv0x70iGFJ3TBMtfiGpr/gF647FuZj7X/vFRdov7Oldp+h7p15rScS8sOvzd/Xj+ez3oR5VxZ8cTGFKJ0D3
sBcov2oS0Dsbiej7fz7ShOYfi9WL/8Z7yH+VTzXxl9w1+NO/+t/6boGzR6HKrr9L6r2X/qc+29pva+/xjXZ9aPeopiNrXMz9V8ef
e9jWfltHzr8rrSf8d2u9/h4I9j+UF90DEV0PmF/paP77L+rSo44O7R6NnYdAfn4BQjen6cTdB9x7NnsRgKb48Y8WIEmL/5QG50VZ
eywmtPiLtDXO/zZWAEOKT0AQ4m5M9cFu8gHkUSgBhBRb/ZH451dHAg4mIcLliT8bEKuXFv9evEmAXousDXB+/KX4h16pG/Nnj17R
g4V5FmAC5T2AIXmFMCKv+4h/uFIbQCPjVPd+4h8ubQHAcRufjyn5oAvVZ6uVdXia4hfV602Aeg7tHtXv/vWv9dwzP+xLBvTtqTPS
TH/cXRIgl4gG2bIWIHt9z83+nSmMP6tR9v6b9AzM81d+/ljfFQFIE23v7rASCUDz8RcApMGDXmnPXGdff77vZ/l9FwsAYfz4T0+1
ewcdQ8c10UIMJJ7JZ25pVVrfZJ5VBGN2uSOtF784tHt04P5N+88nbg5C6o9j4r2Y+28lmP+3xfqXLdZ/7e34u5u6Pn83198h/tWg
/7FH+7dD+7dFARg7oQcw0pL/SP3FL3j+Chey/hiVlYQe5fnXwCXh/t4nl/W9wwf07akzxL4m0XnMkx99rntf3pLOnEotBBMtQIJs
WXNvUne+M67oUZS/LkDfH66KAmxJhzCQrcwBYIqQVM8VgPclFcHw+xwUt75OtTalbl+SVPzCN7ljRMduzmvPrn29ohdSfCESpHPx
T3tPNNktqhOdf5DKF8FmDBSu8PyblHoNWH8PUyr+Uuw1IP5h8uw/7Dv7lZCEm+QP4aLPv3H7n6WNuU83Nk1KPO8wLs3PPwAft/7+
7NEr2rNrn+59eSuz+AXz//nk3f/w7NErvX/fe+Nnmnqt1Xf2lPiH85POJCWg7713udN3BlWi7ymjyN7DtPPXKKbo/iv//Yw/83Pt
3xW7juuDXNKrOJzBq1fIM9jezHegKOJvi/jbm711X/NjJ7T3+Lu5xjgUYQh38mhbZy8v9J6jkopgoB5vtCfWfnf57d7XLubrBS36
iotI/YXWpl5r9RUlmeq+hTYPIFPpApBSbBFIh7WAdFUkoHd+9x//rj/9q/8tSRQBCFBlARgf+a/CEP/hUHr93TnwgR4sdNcH6H+q
8//961+v/9tf915LS0CParhx0E5Jah/Uiwe7sz3TU+tFOyN7INz+BxTXtwdiZfD7lx519NUf/0s/+fO/SNz7zJizmF4BQm/9K/E+
kDDmpwBDcdfn7ybmVB2QsO9QYv9nUXcPfCDd+Fnf13njv1n2nzRaAEMqloBAilmsX6CEbRHE3xYJOGzlib/bgOg2H0piA2JJafHv
bXprHdSxxfmg5MMMgMJlbYBL2/g/3VntvQf55V2Aica50EQd+pTdAIpishYAooWQ9uzap9Mjo/FJcdWfBAhhshIQxGHjbX3cAfak
a/Bg/yv6wdkT0o3fizTb5YT2P2mHvxwK8BRX5v6b/AzM81cR0SIYSfz2/uzRK3JPbg+Y/ymstwCj8Geu2Rv9bV/q9l08/+bn5h+K
JB0b+B4FGHLZ8Xc3de6d/b0FlSsnJnTk/J3ERAO9Pof2X1pcAhppYwyUhvtvNZj/t8X6ly3i/3gi/tWg/T+eiH81aP+2GH/aCT2A
kZT8R1Jf8Quev8Jkzf9L8Qmh05AAK5+k9ceTH33eSwItdde9HkixibgdV4RhmrmfSrhr8K2kb0+d0c5T3dez1nyZ9wwXt/9H6vY/
RdZitrW7iSQ4ABmubAG2KfUn5ZA4ABOi7AFgV4TkAocgK5FWeDxaBOO3rYOSBou/oxhXhGHu/J3M4hf+/qvTI6OJ12BjXDVBQqAU
42OttR1/d1Oaalc23s8qood+fgJuqYoi2Dz/5lF0/k2Kvwasv+dTJv7S4DUg/uHy7D905y+SknAz/s8n+vx79vXnB/aduD2405eP
6NjNjfn9tHkI9uHmF1J4wZ3BiOovfoG8yqx/+f0+8c8vrQjG/Ep3fP/zJ0c03VnVMSX3O5wByC9t/jOpP3r26JXe2WsSAFWD8aeN
uCIYUa7AqT83kXYGjzXIcNGCa8xlPn4ogl0c7f/xsK39tvYe35jTPLR7lHZfIb8IRpQryOAQ9+q80e6O/f/10kxs4ZEpbayt7z0+
0/u+v9/NFb+QKPwCIJ8q8v/cZS9QYZUloEdulRSAQWHEfziUnf9ENaLzEYd2D641Sht7P6dE0ak6/ds//3jgteV3RjX1Wqubn8ND
8Yvi/HMwbg4u+rsgSV/98b8kJbd/xpzNiSv8LlGAoSlx+w4l9n+WUU3uvcdf4wUwAORHAgg7m/kGMGz8IhhpCdA3NuEyAMojawIo
aeM/hS/KowCDPSZAbaQtAET5CSGi/OIXTECECSkAoMtHgjfeSmy+zSurAMndAx/ouWd+2JcM6NtXjkqvHNXOU4PXwCUBOnL+TuLi
ATaE9j8U4KlX2QPYDgUYystKvBQtfoF6hDxzRas2SywAlFEk6Zh/aIDEJ8VF59MO7R6NTWZI+69eNAGNlC8JjcP9t1nM/wMAAKBJ
jD+rETr/GZ1v27v+7OuSLbH/JJ+0+f9n1Z17m1R4Qlxpo0At0qWtPzrRJNDRRNxJycjGx1oUAAgQt/7oXndcjH9w9oR04/eStwbs
f79XgETEPo+4ArTuvhrd8zDptXd/rd2txTD/VkzZBJRT3mvsPwlX9gDwXiUnpOEgZDgXw9AiGMcW57Vn1z4d2j0adA9BuvGx1trc
0upA8Qt3z/321Jnee7MKUKEYd68tMt6PWwOevXWfQ6g5FN33zPqjPXcNNuLP+nvT7h74gPgXlHf87+bhXCJuqT/5AOP/cHnOv/y2
dVDHFuczk9CjHklFmJ89ekV3Jeb/DfT9vhD/XNyzq18EI8oloA89A+AXQkK2tPnPJHEJJyUSAFli/FmMa/+Hdo/qUsp+Zzc3kXUG
T9o4C8/vQLLJczf1/vbtva/nVzqaPHdTZ19/PtfPcXOnfoJuSZwFC1C2AIO7D1AEO7+q2r/jt3+SIVZnZ7tbbFztg3rx4N7e6+fe
2U+7L+GN9sTayaPt3te9IhgaTKrqF1l46/THxL0B0SIYrk/xx/juujzTntAfF7oJWSmCASCPKvL/JO0Fog/KRv4lO+Qfs0X8sdW5
eaDofMSlpdXkfaAUnTLhii8wx1MNv//399G6eTg/H1nf7wIFGMwl54Bm/asJ0bES+z+btVnP/1IAAwAybNYbwDDKSoC+UfwCdSHh
bT1YAMBWlWcBIOkAhl/8ggmIcFkFAPx77rHFjbFNWvGLjc23dX7yx19QARKPOxQfmgQIYUL7HwrwYKtIa+sSxS+alBVnEkBUayDp
mHfYMZp0zCUA8s3euk//X9BA4amcf4f2XxwbrwAAAABgeLH/pLys+f/Z5U5qMVT/fcgnaf0xTXT9y72GfOLWH6XuGuTJjz7vJeN2
vjh5vvsvMxux3nnzk76ETGp1k3VQgCSftP0/fXseIusxrtgOazF2oodg2H+ST5kDwCRCLG9uaVW6utiXaCapCIZLQLxn176NpLfr
Rdii9xCJIgAhxsdaa4fPLWhmqpuMyS/69e0rR6VXjkqKH+O4olOT527mTh6HeEXG+3FrwLR7ANi8OABfjZDzL73n4PU5hrR9WVdO
TDD2rwlzDdgMovOfvSIYEX57zzoDQFKgYoqcf4xLOClx/gKPH9f+s/Y7zy53NLm+/pV2Bk8SY58Uc0urfcn2JOng0yPSinTyo891
aPdo0M9xfdDc+Tt962XvXbymI+fvBP+crajqAgwIV1X7lzYKX7j2/97Fa73XaP/h/LGnP5f/b//849j3/+Sd2j8SCqIIQ7iswiOu
CIbPL34hqVf8AgCszI+dkK6e731N34/HAfnHbBF/bFXReSDHzUdcunwkcc0xqegU8//F+XvZkoqP7NVG4d8oir/nt+Pvbmr2ncH9
m3F54HzsP7FH/hlgc6EABgBgqCQlQO8dxmMACgCPlTwLAP5k6N71w9fnri5KEgWQCshKQOAfPDq2OB9U/IIJ6DBZBUiSUASjWqH9
DwV4sFUktXX3PWCzCk065icAcuj/AQAAAAAAhk/S/L+f8CotKa6//rWt/ba+W2D+J1Ts+uPlI3rv4rXEmLv1Ln8N7LfriRERLm79
0ecn447jrzv2FcJApdx6S3Q9hnWY4eDW6zkAU0yZA8BpiRBJQBBmx9/d1Ll39vdieOXEhI6cvxOb6NMVv3DuHvhgYA1MoghAUf59
tMy+nmhRBmQrMt5/9ugVzUbaP/vfAGDz4wB8c0L2ZVH8AkCI6Pzn2defzzx/kbQv2hW/IAFQc0gAhK2ir/hO62BqATAkGx9rrcUl
3JO8pHtLq5nFSJy5pdVe8n+3XuYK004zDxSrygIMPld4wXHn8rChyvbvt32p2/4nd4xoUiOaXe7Q/jPcXnygkx99Lkm93wdXCEai
gEjTXDGGC5HEntExfVLyT5QTF1dXBCP6GgAMm/mxE/pu4V19/c0i888AAMSImwfyHXx6RKcWrg/sOfRF1wCY/8/2Rnti7eTRduL3
QwsvTKm/aKF7Tmb9Pb+4fbRZeeCi72H/CQCUQwEMAMDQ4dAvAGBggogJoEKyEhD4RTCiB4OjxS+YgM4nqwBJEr8IRhwmoOsRHX/u
vfEzCvBgU+JZC1tVaNIxFiABAMBm9GBhXjvbB3v/THoPAADAZtCXeEbSpJeUOJp4Zlv77aY/3qYQXX90MZ9UchJiaWMNzCWKpgBJ
ftH1x6LKJOtGGNZjgEFxiRDZ/5BPNIaHdo/GJrCK64PiDu8R/+LK3ktd8QuKkOQ3MN7fMdK7HtHxvvtdGCyAxPgTAIAqJe3LcslC
z11dpAAVgCBFzl+4PmjvjZ9p6rVWLwkQCYCax/5bbBUhBcBY/8r20sKnyd+TdGnXvtw/M1osvlcEQ601kuFuqLoAibP3+ExfMYb3
Ll7TkfN3KCIQo+r2H237yPbhwp0n5pYGfxcOPj2igxrR/EpHl5ZW9eP/+W+xf3+v+6dX9IUibOXNLa3GFtJxY/wpdcf30SIZyMdP
wuoKj0y91kosguFEi2EAAAAAeHzFzU38/MkRXbp8JLUIhsT8f16u0KYzO7U/+O/6RTB8rL8XF5r7DQBQj8YLYHx04f3gxBok4Gge
CVAAAACArSV6MNjXX/wCeWUVIHnv4rWBwiM+lwTIP6CNZvRNWvMMXAvmH2wRf2xVJB0DgK2L8U+9WP+1FRJ//5/R9xJ7PM7of4Yb
919bxB9bWUjimWePXuF3oGKzy53UdS9JrHtVYGD98fKRzDXHKK4BACt3D3zQu/+SAK6Y6AG8PEnIiH957128psmZ8OIX/j3XFb3o
fY/iF4WFjvfRDOYfbBF/W8Qf6Be9/94VBajqQv9TL9YfbWWdv0gSlwSIBEDVo/+pF/3P4yOpABjrj/VJ6n/uXz6ie1/e0reSdp4a
/HvH1v/s2bWPIhieqgsw+MUvXDGGXgES7sWlxbX/+5eP9BUciaIATL1coQZ3Dd67eK1XuOHKiQmKsBUwee6mDp9b6H390YX3JUlH
zr8rnb/Te52iOtVzRTDmllb7Yi31FyBB83j+qhfPXwAADB/GP9VzhVDj5oKutV82+ERby+S5m/KLb86vdDR57qbOvv588M9w61++
bg441t8BYDPYauOfbRb/0bgAlnkN4dxEf5y4BChJ70ExWfH3/6S9D8UQ/+GW1vdE34P8aP+2iL8t4j/c6P9tudhua7+t6c7qwJ9n
j16h+EVNnj16pXfoOurB/lf6/ikp8b0ojv6nXsw/DD/ib4f+xxbxt0X8bRH/ejH/YIvxpz3Wf22FxNUlNvRfj3sPB8Tyof+3R/9j
h/uvLeI/3Hj+svfs0Su9tZjo2hfJcKvnYp1VWMF9f7qzqm3tt5v4aJte2ppjGq5BPej/bRF/W8Qfm12Ze+6zR69o9tb9vj8kvyqH
8X5zmH+wRfxtEX9brL8MN8b/9aL/scf64/BKa/vdJECLvT+cg8mP/sce/c/wimv7bh7C/eEahLvWfjnxz5nvv9j33pD+B/VKi/3c
0upA8QtncseITo+ManystVb/p3x8VNX+vz11Rt+eOqOdNz+J/XNskd+VJC4BaJKDT4/o50+O6H6k0JG0UXzEb/eTO0Z0Y9cOnR4Z
1ZFIAQH0e6M9sXbyaLvvNb/4xfX5u7o+f1c72we1s31Qzx69osPnFnp/JGnhs3up/432C3s09VpLb7Qn6HsCzS2t9sV5W/ttbWu/
rSPn72jv8ZlegRdiXy2ev+zx/DW8mH+uF+svtoi/LeJvi/GPregcRFTaszDym1taVXTuwcX45Eef5/pZdw980PvD2lc9GH/Wi/uv
LeJvi/FPv0YLYHz9zeIToYk1Qt9HxfH8Qho28a8PE6C2iL8dbsD2aP+2iL8t4m+H/n/4uRhva7/N5lsDSYmAXPGLrERBSEb/Y4/5
Bzsh7V8iAW5d6H+GH/GvD+3fFvG3x/yDLcafNlj/tZUn/od2j/Zdg7j3XDkxUfMn3pzo/23Q/wwH7r+2iL8dnr+Gmx/76NpX9D2o
jl8EI7q+5b9G4YV6hK4psvZYDv2/LeI//Ii/nbTYR9+Dcorec90B1PmxE5pbyl9IA/GePXqlt+ctbYxJ+y+nyvkH9p/kR/xtEX9b
rL/Y4fnLHv2PjTrWH4l/PmX7H/fcRQKg4uh/bET39Dj0P81h/NOMrKTzUSH9z/fOnNKD/a8k/vlt62Aln30zqboASVohBoowbAhp
/36yyZD2n4UCJMleWvg09c+pP1zXvS9vJSb+/GLmxkDRF+Tnil+894s/0Xu/+BP92z//eOCP+957v/gT/e4//l3nri5af+xNJbQA
yY6/u0nsa8Dzlw2ev+zx/GWP9RdbxN8W8bfF+RcbcQUviuB3IEzaHJCb+ymyf5D414vxZ724/9oi/rYY/2xotACGNDgJFBfUs68/
H5yAg8q/4epIgEL8w7EBzhbxHw4swNggAZAt4m+L+A8HHsDskAB9uG1rvx2cCEgS8S+A8acN5h+GQ+jEcsg8HfKj/7HD+Mce7d8W
8bfB/LMtxp/2WP+1FRp/Sbp78XDvvdH3UPwiP+af7YW0/0O7R3XlxETQ+xAuT/sPiT/9fz7Efziw/mWHA5DDyxXB8Ne//PUuil/U
wy8+koYiJNWg/7fF/Kcd1l+GH+Of+hW557oibFyDetH+65EnARAFmKtH/G0Rf1usvw8Hnr9s0P/YeqM9sTY7tb/S/Q/Ij/7HBv2P
Pfofe/Q/w8EvAOCL9j/3Lx/RV7+ctPiIj62qC5Dcv3xE9768lflz7n15iyIMJUXbv5Rd/OXB/lcMP/Hm82BhPrPNT+4Y0emRUYpg
B/ILL+S18Nm9ij/N1pS3AAmqw/OXPZ6/7PH8ZYPzL7aIvy3ib6vq8y/0/fVi/1V5WUU3o1xbj2vz7vsojv3Pdtj/Y4v42yL/yaDG
C2BI/ZNAPjf5M3vrvqT0BBx3Lx6u+2NuSlUlQCH+xVSdAAj5EH87ddyAkU9oAqDQ9yEf4m+ryv6f+OfDA9hwCJ3Y5P5bvZAJUFcE
Iy0RkCTinxPjT3vMP9jJuwEubZ5udmp/vR92E6p6AyIFSIqpavxD/POh/dtiA7Q95p9tMf60x/qvjTfaE2snj7aD4y9tXAP/j4v9
uauL+nDhDhtwc6AAjL2s9i9123ZW/zP1Wov45xTa/kPij/yIv52q559ZfyymygOQHEDKJ2v9a1v77b71L/fn2aNXBoouEP/8kuLv
J+SOJuWOrj9S/KIYDuDZYv5zOLD/ZPhxAKl+ee65FL+oBgdQbYUkAHIxZf6hesTfFvG3QwJ6Wzx/2aP/scf+Bxv0P/ZC778S7b8u
9D826H+GX9r454uZG5KkH5w9oR8cPjDwd11CegowhAktQOLafkgRht+2Djb+/7GZxLX/aPGXpPaPQa4QzLX2y0F/3O+DH/dvT53R
zpufxP45tjhP0Zecrs/f1Y//578F/7l74AOdu7po/bEfS27PuVS8AAnFR6rjj2mY/7HB85cNnr/scf7FFvG3RfxtVXn+hfNf4eZX
Otlvinkf+6/qde/LW735t6x9ucS/Gux/tsX+H1vE306ec6VbYf6h0QIYbjJ08txNzc5f03cL/Yk14qQl4EA+/mR0yAScRPzrwgSo
LeJvgwRkwyGt/Ttp8WfwWQ7xt1W2/yf+xdD/28mbgIn41yN0AvTuxcMDiYBc8hnin59brKL/sfFGe2Jtbmm1N/cT5V5j/qFeoROg
0sZmLf8PxS/KCZ3YpwBJtSgAMxxC+x/iXz0OwA8H5p+bx/qXLdZ/h0Oe+Evda+D/QTF5C5DQ/1eL/mc4VFWAB8UQfztVrX+x/pgf
BUiGQ+j6lyuGsa39NvGvUFL8/cIjLgG3n4Q7WvziuwUKkORV1QE8+v9imP+0k3f9hfhXL7QAgBS+TwLFuSIYaffcpOIXjIGKqeoA
Ku2/uJD9zxLzD3Uh/raIvy3WX2yQAH040P/YYf3RDv3PcGD90Q79jx3mn4dX0vgn6ouT53vFMFCtkPaPeqTNafrtnfbfnKyCLw/2
v2L9EYFc8hQgCSk+0n5hD8mIcwrdV8L4v3o8f9nh+cse519scP7IFvG3xflfG19/s/jEpUdhBTAkyb036z7NHuhkoYU3z3z/RUnx
ewuJf7XY/2zLzQ+E5h8j/tUi/rZCxz++zT7+ebLp/6Cb/JHU+6czf/22Tv7qbwc29ccFnKrAxfjxnzz4Ut/3/v7X/0j8a+QnAJXC
4n/34mHtPd7fWd29eJj4F0D8bfnxnzz4Ut9hamlwACQR/6rR/m0Rf1vE3xb9vx13//1u4d3YpDLS4KFq4l+dQ7tHNefFfmf7oKT0
g+3d+M/0fY/4l0P/Y+vGK5M6PTKq6cgk3OmRUU13Vgfez/xDtRa/XlBrvJ3Y/qNINl+tG7t26MD6fcDn4u9v+Jyd2q/Jc/3XhetR
Tp7xD/GvXlb79xH/arn5/7Txjy9p/IP8mH+2x/qXLdZ/bRWJP6rl34OzcP+tFv2PHX8DljQ43pyd2q/biw8G/h7xr0a0AExI/yMR
/yqx/mUva/7HHYJxsY+7TldOTGQezEa/r79ZfGJ84d210PWvuZg5Ivd94p9fSPy3td/WdwvvDqzDxP0OHNo9qg8X6v/cm9F3CfOf
cQfw6P+rU9X8J/EvLvT+K/H8Wwe/7/dfi3JrL3G/J0nPakj30YX3B2LvClxMXz4y8P7Q3xNky7v/qvusTPuvUlXrLyiG9S9bxN9W
3vgz/q9WyPNXyPMviqH/scX6oy36H1v0P7bof2wx/9yc+ZWODj49kvp957uFdxP7HzQjtP1L0g/OnpBu/J5CDBWh/Q+Xr3452fd1
Wnv/bevgwGvAZrLw2T21X9hj/TEee3uPz2jx6+6mndZ4u+97//TBv+jIz37K+kuNqnr+QjE8f9kpsv+c+FeP80e2iL8d5p/t5JmP
O7R7VBemX008f8E9oD5u/1ta/Cl+UVwV+fdQXJ78Y8S/elXEn76/GMY//RovgCF1fwHi5P0w564u6sOFO0+U/0Rbi4v/6ZHIQtfp
k7l+DvEvJm/8k264xL8Y4m+rigS4EvEvqqr2j2KIvy3ib8MlAKX/t+ViH5oAnfhXK88EqET8q0b/Y+vAJ7OSpNnI6/PXb0u/+tvg
n0P885lbWu1tfnNFMHw/evFl3b7+adDPIvlDcc/emtei4jcg/s3PfjrwfhL+V4sCMLZo/7aqGv+gGOafbbH+ZYv1X1tF4u8X4eR+
UBwJCOzR/9jyfwec+eu3Nfmrv9XZ158P/jnEP78qCyAR/2J4/rJFARJboetfSclPiH85ofHvHoCZoQBMhfIWQJXo/6vG+q+trP0n
0aT+PP9WI28BACm5ADnrv8UlFSDxfx9ckQUKMFQvz/6rpPaP4qpYf6H/L471L1vE3xbr7/biEgD9/a//Uf8Qs/+T8X+16H9ssf5o
j/7HDv2PLfofW8w/1+/rbxafuDTWWtOKYpPuuWR7lx51NvqhnP0PqvPdwrup7d/ffyhJX5w839Ane3zlSTh5emSU9j9k/GIXtPdy
Js/dLP0zKMJg4+6BD3Tu6s90gdhX4v6+7trjjV07+r/xq18G/wyef4ur4vmL+BfH85edKgvAEP/8OH9ki/jbY/65ef58nNQ/J+fP
Q1x61AkqAED7r8d3C+/q7OvP9/bgpsWf9l9MngJsEvv/q5Y3/xj332rFxX/++m3NzMxIMfnHGP9Xi/HPhkYLYHy4cOeJ8bHWmvsF
iMqbABHFEH9bxN8W8bdVVQJcFEP7t0X8bRF/W/T/tg58MqtZDSbgyJMAHfm55Cc3XpnMVYAE1fCTz0jhE3CoRjT+vvnrt3V1ZqbR
z7PVuWIYkjT7yW39zc9+miux1eyt+4/9BGiT/AIk0mD8L/zmQvDPIvlJfhSAsUX7Hw5VPH+xAFwc8w+2iL8N1n9tFY3/3uMzvXv1
7Ce3tXf9OQHFkIDARtD8A/M/tYorfiFJB1/8UWICaFSrqv4HxbD+ZYsCJLayEqD7iH318safA0jVqmoDOvJJW/+VuP/WzY9/FftP
eP7Nx62/uOLvIQUApOSE/6z/5vcdBUjM+OuP7nfAl7T/Kq79E//iqpr/p/8vhvUXW8TfFvG3xQFsW7R/W8TfFv2PLdq/LeJvi/Xf
ZiQVwfCLX/jrAWnxf+/iNU3uSC4mIEmzy53U7281eQowzM5fo/1XKE8BGPc7kBR/2n45Wb8H/vtQvclzN/X+9u168+HDoPe7tRl/
jYYiDHjcuf3/z94aXPeVunv79bOf6sOFO0+80Z5Yy/p5PP/mU/X5F+JfDM9ftth/bovzR7aIvy3mP+1cerT+jLuS8HoMEqA3w+1/
c8UvHM5gVKNv//N6EYwov/hIGs5f5Fd1/jH6n3zS4i9Jt69/Gtz+URzjnw2NPnOOj7XWQjqguAk4vwI8N+RiQm8AxL8eZW7AxL88
4m+L+Nsqc/9FecTfFvG3Rf9vayABRGTz5z/86m8TJyCIf3WKFCAh/vVLm4Aj/vW7ff1THdo9yvxDw/Imn0c9bl//lAIkDaIAzHCh
/deLBWBbPP/aYv3LFuu/torE3y9+IUmTr/xI//TBv+jIz35KovqcKAAz3NLmH1Cea/8cgLFF/2Mj9P4bh/FPedH4UwC7WX78q0iA
jnyKxp/+phpB/T/t3wT33+ax/8SGXwTD993Cu7nWX5AfBUiGg7sOUaw/1qfM+gvKY/3LFvG3xfq7rTIFyIl/efQ/toi/LfofW9x/
bdH/2KL9N88vBOCLK36R1P67ReBnpGUlFgJwBQCmO6v6+pvFLT8nlLcAQ5H950iXpwBMUvun7ZeT9Xvg+NcE1ZlbWtX727cHv9+t
yUT/GeXfj6XuugGqEVeABOWNj7XW/L38vqwzwIw/y+P8iy2ev2yVmX9DeVkJiNn/Xy/ib4v9J/Zc/OOS/0vJBQC4/9bLFb8gAX1z
4vY/50H+jWpRgAGbGeOfQUNx5twF//b1T2MXUPwkHLOf3Nbe9URlqAbxt+XHPy4BB/GvF/G3RfyHQ1L/LzEB0YS0+KN+tH8b9P+2
QhZ/iX/1opsPkybgiH+9aP+2iL89P/l83ATo5LmbvX9PSsiBYvzNh8S/eRSAsUX7Hw4UoLLB868t1r9sEf/hEI1/tPiF44pg/M3P
ftro53vcUYB5OEVjH/cexj/VySrAwPizHiRAGU6M/21lrb9ItP86kADdVp74o37Mv9ng/muL9d/mJRUASML6S3UoQDIc/D7lwm8u
pBZfo/3Xb+P+O/g9xj/1Yf3FFvG3xfjfFvufbdH/2CL+tuh/bHH/tUX/Y4v2X69eEnpPXPGLpPkHF//WeDu2EAAFAOKFFmAIaf+S
9N7Fa4lFGKSN64ANIQVgstq/1G3btP1iotcg7ndB6i9+kdXWHdp8svGx1lqe4hdR3y28O7BGI3X7o69+Odn7+r2L13Tk/J2BwuXY
4K+fpEkrQLLw2T21X9hT/Yfb4vz1L8b/zeP5yxbPX8OB/W922P9vi/jbI/9bc5Lm3+Jw/y1mfqUTVHRTkn704sup+99o//UJKf5L
/Ovjx3/21n3uvw0j/ray5h+kzRv/bdYfwAmZ/JE2km8cOX+n0c+32RF/W/7kj/868a9GWvIZifjXjfjbCk2+FMddg8WvF/RPH/xL
32AIYcrEX+peA/cH+dH+bYX0/2dff37gdfr/aoTG301AuNeJfzWS4h89fBFF/KtB+7fF+N/W+FhrLS6ZrS+povjkuZuanb+m2flr
+vtf/2PwZkaEcwVI4hD/+kULwES/P3nuZu8P8svqf5L6f4n2X7esBNA8/9aP8Y8t1r9sEX87cfOfrh+6v+9g7J/9v/qlxUfdlEI3
oDD/X1zI/Fta7Bn/lFd0DYb41yv0AB7xrw/jf1tJ8/8S7b8KoX0/8a8H+09s5Sl+F/0+7b881h9tsf5uK279xe9TJLH+2KDFrxf0
3cK7fX/SDhax/lgv1t/tMP6xx/qLLeJvi/G/Lcb/9Qp5/qL/sUP8bdH/2OL+Wy/6f1tFzj8ufHaP+FfIzeHEXYeQ/mfx6wVNd1Y1
u9zp+yNRACDJ198sPnHpUUfzKxt/pP4CDFJ2/P3Yx+E6JHPXwP8T/R3IE3/afn7+NYj7Xbj0qKMfvfiyJOnQ7tHUtu4Q/2wvLXza
+yNJH114P/G9frEFtx7jr89I/cUvvpi5oS9mbmhyx4hOj4xqbmm1xv+Tx9fkuZsqUojExVyS5sdOUBi+Roz/bRF/W8w/1Iv9b8OL
/f+2iL8t8r/Vj/xvzfLn3eL4cw9//+t/1O3rn2p2an/se2n/5RXd/ywR/yak5Z8h/vUj/ra26vn3xgpgZCUgiBMd/DhuEMSEczji
bysk/lmTbw7xL+bkr6YHXiP+zSH+ttLizwJM/YrEX9rcA9Am0f5tZfX/WZvPHfr/YrLiH0X8qxWNf1zxC/93gPhXi/7HFuP/4TP7
yW1d+M0FSfGbT1zyB+fgiz/S3//6H3Xyo8+b+oibQtECJMS/GhSAGX7R2N9efED7r0iRBNAcwKsO8/+2WP+yRfxtFS0A8Oyt+dg/
N3/9myY+9qZRNAGBxPx/VdLm37Ji7zD+qU/cdSD+zWD8Xy/G/7aKjD9p/9XKWn/nAEy9QuLPAYz6sP/EFuuPtth/Mnz89V+pfw2M
9ZfqhBQgWfjsXuzfZf2xvJD1X2lwDZj2Xw3WH22x/mKL+Nti/s1WSPzZf1svnr/s0P/bov+xxf3XHv2/rTznjz5cuPPEkfN3iH+F
qpj/d4UAon9IQJ8srQBDnvgnFcGgEECYH7348kABmCLxp+3n58Y/s/PXFP1d+Ptf/6N+9OLLfXsg/CIYce2dNl+cX+gi7TVJvaLk
i18vaG5pta/4hc8VwRgfa61V+2kfb3NLq33FL8oWIHH2Hp/p+4N0Setf0fVfH+P/6jD/Y4v5B3t597+x/ludoue/iH81iL8t4m8v
ZP6Z/FfVSSqCES1+4eJ/e/FB3/u4/9Yvbf2R+Fcn6/y1lF58zSH+xRB/W0XmH6TNH//GJs7Hx1prP3rxZZ399enea1mDz/Gx1tqN
XTsSf+aBL5eZ/A9E/G0Rf3vRa0D8m0X8beWJ/xvtibW5pdXYCQipu3D2Nz/7KfHPIW/8L0y/GjsJ5GKfVDEP8Wj/torEn/6/Omnx
P7R7VFL/JAT332r58Y9LPCMR/zox/rRF/O242M9c+afea27zW9r9N2nSev76bf3Dr/6W+AfK2oAYvQbEv1pF4j+571md/OjzgWvg
Ys/zV7i4/kdK74PSFs1o//kUnX/m+bcazP/bIv62iL8t+n9bcfGXkq8B8//VS5p/i2vDzP9XL88mdOJfrSIHAOj/q8P4x1ZW/OOS
/9P+q5U2/x+NP/1/9fLGn/Fntdh/Yov1R1vsP7GTtf575cSEpP4CAKy/VCdk/fHKiYle/Fl/rFbI+qMfT9bfq8X8sy3mH2wRf1vE
3xbxt8fzrx3avy3ib4v426P/t0X8bRF/W1XF/8CXyzo9Mtr3GoUAstH+7aSNfyT1Fb9w6/B+MYW49i6J+CcYH2ut+YUXnDcfPtS2
9tuSpJ3tg5IGi198t/CuDu0e1dRrLflFqFrjbd378lbqf3fPrn1ck3XRaxAXeyfuGkjq2//w8/375fakuEIkkvTexWua7qyyHpYi
7/lf93fo/6vB868t4m+vyPiT9d9q5G3/7D+sFvG3Rfztsf/TxvhYa+3nT470veYXv4ibe3B/j/Zfjaz+J+7ZlfhXp8j5a/r/6hB/
W4x/4jX64fMkIHDv3+wXoEnE3xbxt+eugUP8m0X8beWNPxMQ1QqN/1YZgDaN9m+L/t9WXPyTNo4Q/+r58U+a+PffS/yrRf9ji/jb
8TfBZW1+c++Pbrz1sek8XNENiMS/GkXjTwKU6kSvAe2/WUXmn3n+rQ7z/7aIvy3ib4v42yIBrr3o/Fta/Bj/VKdoAQbiXw0OgNnj
/msrKf5JazC0/+olrT9K/fF34x/iX6288af/qVbe/T+0/2qx/miL/Sd2ktZ/XeEFafAAKusv1aAAiT3WH22x/miL+QdbxN8W8bdF
/O3x/GuH9m+L+Nsi/vbo/20Rf1vE31ZV8W+Nt/u+5jqEof3bSRr/SEpMQOnmPw98udz3s27s2sH8Z4qkAhhSfyGGKFf8whUgyVP8
wqEIRtf4WGstGrM9u/YFFyCJ7n/41baO5pZWe8Uvvpi50fve7HKH9ZgMRc7/0v9Xh+dfW8TfHvmX7LD+bov42yL+9tj/aWN8bKOY
piT5ZyDPvv68Zm/dl0QBkjrR/9jKc/7avZ/4V4f426L/GfRkk/+xr79ZfELXtXbyV92vsxIQoFrE3xbxt+euQd/XaAzxt5U3/s/e
mo99ffaT29LPflrxp9v8QuPvFuDv7zsY+3P21/T5Njvavy36f1tx8f8wfo4ZNfDjT+ybR/9ji/jbcbE/fORvJIXNPxz4ZDb29fnr
t6Vf/W31H3KT8mMfugFRIv5VKRr/G69Mxr7e6MT5JhHtf6TsPoj2X50i8888/1aH+X9bxN8W8bdF/G1F4y8lXwPm/+sRnX/Lej/j
n+qc/NV0rgIMEvGvit/3hG6Ak4h/lbj/2kqKf9oaDO2/WqHrj278Q/yrlTf+jD+rlXf/D+2/Wqw/2mL/iZ249d9Du0f7ii5Esf5S
jbT1x6QCJBLrj1Vi/dEW64+2mH+wRfxtEX9bxN8ez792aP+2iL8t4m+P/t8W8bdF/G1VFf9/+uBfSIBYAO3fTtz4xy98IQ3O/7v5
z8XIz2L+s7j3t2/XmwvvDhTB+G7h3b5koJLk73/43plTfUUX4swud6r9sJvMvS9v9YpgRAtfSIMFSPz5/7nxdmzxC0ma3DEiLUvT
aq3Rp8Urcv4X1eH51xbxt0f+JTusv9si/raIvz32f9rw2/n4WGvNFd48tHu0r+hmFO2/OvQ/tvKcv3aIf3WIvy36n0GN76PPm4AA
1SL+toi/PeJui/jbIv628sR/sw9ALdD+bRF/W8TfFvG3RfxtEX87zD/YYQOiLQrA2OMAhi36f1vE3xbxt0X8bRF/WxwAsEe7b17R
AgyoDgfA7HH/tUX87RF3W+w/sUX7t0X8bRF/O9HxD4dPm0MBEnusP9ri+csW8bdF/G0Rf1vE3x5xt0P7t0X8bRF/e8TdFvG3Rfxt
EX9bxN+OP/5xySelwcIXqJcrguGbndqv24sP+l7r7X8Ybzf10TaVa+2XB17LU4Ak6ttTZyRJO08Nfu+YpOld+0p93s2O5y9bxN8W
8bdH3O3Q/m0Rf1vE3x5xt+XHn/2fzaL/scX+T1vE3xb9T7/GC2BIBN4a8bdF/AEAAAAAQN2Yf7DDBLQt4m+PuNsi/raIvy3ib4v4
2yL+tog/tiIKMNjj+dcecbdF/AEAwFbD+McOBUjs0f5tEX9bxN8W8bdF/G0Rf2xltH9bxN8W8QcAAFuNG/8w92/r/e3bNb/S0aVH
Hc1O7c/1d39w9oR04/f6YuZGTZ/u8TY+1lp7f/v2xO+HFiBB9Xj+skX8bRF/bGW0f1vE3xbxB2CF/scW8bdF/G0R/w0mBTAAAAAA
AAAAYLNiAtoW8QcAAACA+lGAwR5xBwAAAIBm8PwFAAAAAAAAAABQzPxKRwefHkn9vi9P8YUvTp4v/LnQlacASWu8ra9+OSmdOZVa
dOT0yKim1VpjjQ0AAAAAAADANusPAABAnMNH/sb6IwAADND/2yL+toi/LeIPAAAAANgKeP4FUKWvv1l8ggOKAAAAAAAAAAAAAAAA
aAL732wRf1vEH4+jr79ZfOLSo85AkQvHvX7pUUdnX3++V/xi9tZ9fbhwh72JBkIKkKQVvwAAAAAAAAAA39AXwIhbgJn95LYu/OaC
wafZeoi/LeJvi/jb+fqbxSduX/904BoQ/+awAQJbGe3fDv2/LeJvi/jbIv72eP6ydfJX09YfAcAWRf9ji+dfW4x/bBF/W8TfDs+/
2OoY/9gi/raIvy3GP7aIvy36H2xltH9b9P+2iL8t1l+wldH+bTH+scX91xbxt0X8bRF/W8TfFvG3RfxtEX9bxN8W8bfD/jdbxN8W
8bfH/GdxSUUwosUvpG7hC4pf2MlbgOQHZ0/oB4cP1P65tjrGn7aIvy3ib4v4A7DC85ct+n9bxN8W8bdF/2+L+Nsi/sbGx1prr/6P
N9dWVztrq6udtcsffbb26v94c218rLVm/dm2AuJvi/jbIv72/GtA/JsVbf9cg+bExd6/BsS/frR/e/T/toi/LeJvi/jb4fnLlov/
rdt/6P35x/NXuQYNiIs98W9OUvzdNSD+9aP/scXzry3GP7aIvy3ib4/nXxvM/9tj/GOL+Nsi/rYY/9gi/rbof+ww/rRH+7dF/2+L
+Nti/cUO67/2aP+2GP/Y4v5ri/jbIv62iL8t4m+L+Nsi/raIvy3ib4v422P/my3ib4v422H+s7zxsdbayR3tvj/jY621N9oTvT9J
f8/FfnystfabZyfWPt+7P/HPb56dWPvNsxNcF23E/Or39yX+ibsW0Z/hx3/t5N+kxt9dA+JfHcaftoi/LeJvi/jbSdr/yTVoBvG3
x/OXLfp/W8TfFvG3Rf9vi/jb2uzxfyyqHY+PtdZ+9OLLva9vX/9UX3+z+Fh89s2A+Nsi/raIvz3/GhD/ZrnYz1z5p171Qa5BM/zY
O1yDZtH+7dH/2yL+toi/LeJvh+cvWy7+Z399WvPXb+vqzAzXoCF+7CUR/4ZF4y9xDZpG/2OL519bjH9sEX9bxN8ez782mP+3x/jH
FvG3RfxtMf6xRfxt0f/YYfxpj/Zvi/7fFvG3xfqLHdZ/7dH+bTH+scX91xbxt0X8bRF/W8TfFvG3RfxtEX9bxN8W8bfH/jdbxN8W
8bfD/Gd50WRtobHzY98ab+v0yKgmd4wMvG92uSNJmu6scl3WjY+11n7+5IgOPj0Yr/mVbrwuPero0O5RfbhwJzZmLv63r3+qr345
qS9mbqT+N2eXO1yDijH+tEX8bRF/W8TfTnT/J+PPZhF/ezx/2aL/t0X8bRF/W/T/toi/rc0c/8fmf8CfwN4MgX/cEH9bxN8W8bfn
rgHxbx4bIOxs5gHo44L2b4/+3xbxt0X8bRF/Ozx/2WL8Y4cFMFskQLFH/2OL+Nti/GOL+Nsi/vZ4/rXB/L89xj+2iL8t4m+L8Y8t
4m+L/scO4097tH9b9P+2iL8t+h87rP/ao/3bIv62uP/aIv62iL8t4m+L+Nsi/raIvy3ib4v42yL+9tj/Zov42yL+dpj/tBONfbQI
BsUvksUVwfCLX4TEy/U7FMCww/jTFvG3RfxtEX877D+xRfzt8fxli/7fFvG3Rfxt0f/bIv62Nmv8N8X/BAAAqA8bIOxs1gHo44T2
DwAAthrGP3ZYALPF85c9+h9bxB8AgGYx/rTH+McW8bdF/AFYof+xw/jTHu0fgBX6Hzus/9qj/dsi/gAAAAAAAAA2K+Y/7fjrL5J0
emS07/sUXUjmimD4Qotf+D8jWngkikIkAABUi/0ntoi/PZ6/AGBrov+3Rfxtbcb4b5r/EQAAgM1oMw5AAQAAAGAY8fwFAACAJjH+
BAAAQJMYfwIAAAAAAAAAAAAAgM0kWhCDPRHpqohXWhEMil8AAAAAAAAAiGKiEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ
K64IBsUvAAAAAAAAAMRhshAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkMgVwfBR/AIAAAAAAABA1P8PnCsgkG9P4fwAAAAA
SUVORK5CYII=
"""
VIEW_B_B64 = """
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
vzmMXVOs+LMAVN6Dxws77ty41vMZuNinFcLi+o+H+Nsi/vYY/58+yfiz+NmOe1dO6sn8+z2/2ACoJ8b4w/VfHc+/dtz85+Rrv+y+
5oo/hOY/Rz+fCf5am7zY+nvfCorGn3lNM8pe/4ir7PV/85WJ4K+hC+eM/h88/Yref/M24GcXV5p6i1sa8x9bxN8W8bfn7sNlml9I
xL+uMuvP3H/jq7L+j7iKjP9u/v/w8LHgryPvvNXa+91qmP/bYv5ji/wfO+y/26oSf/Yb4+H6txfr/kv+STVl778S+Scx+XsvTqUG
AJ/+paF3uHXF3n9n/CmnbPzZf4yP519bxN8W8bdF/G2R/2+L698W8bfF+GOL698W+1+2GH9scf3bihH/q2cO6fj+ET14vLCDnK1y
uP5tFY2/O/ubxBngYuaW0xtS+F/7l/f+Td9/6WVJnf2BJ/PvB5uO5JnYPawLwyPaOzq2Xv7dbk3Xx19O/fXud1+SpJ6z7UWkNSA5
tVD+M9uOiu7/Sjx/NYHnX1vMf2wRfzvkH9oi/va4/9qKkf+J6srGP1l/jM+gnjLx5/xjXEXvv25fZc/tueCvW+/9zuj/wdOvzPlf
4h8f5383DbX9H3zweGGHbmj93DvqduGpWgDilz/9SXtvfIsg/raIv60y8Ze2fgekthF/e/5n4OQtvjnEvz7ib4v422H8t1emA2pe
/EnALa9KB3g6kMcRe/zh+i+H51977jPwE+GSsf94/u4OEjmbUST+aA7xt1Um/kc/nwn+G3M37kjv/Kq5N7lFlZ3/PDx8LPjvHGn+
rW5JzH9sEX9bxH9w5M13iH8zyqw/c/+Nr0z8T772S01f/W3fv+H9DKzz3FBc2fnnntvhQ40zn9+RGH9KY/5vi/mPLfYf7bH/bqtM
/KXez4D9x/q4/u1w/7XF/rstf+/FPdfmNQAIcQdHiH957L/bKhN/9h/j4v5ri/jbIv62iL8t1t9scf3bIv62GH9scf3b4vq3Rfxt
EX9bxN8W8bdVNv73rpzUwdO9jQFofpHvweOFHVOjY+vHNJz6PVNrq/r+Sy+nxv7R/JyeG+/kvz385DV9/dbmXtgLF89IN/+c2owB
xX3/pZd74r93/v31R1I39r6/n39Xz51v+x1uHWX2f3n+io/nX1vMf2wRf3vkH9oi/na4/9qKNf6Tg15NjOtfEmNQRUXj7/IPOf8Y
X9nzL4in7PiPuMqOP1v9/K/ZxbZ3dGzddV2W+gegN8YPrc8urujmvt2p/8bRr5b4gamI+Nsi/raKxj/tAWDm8zv65U9/QvwrIv72
/AN2yTgS/+YRf1vE3w7jvx0X+6wHYOLfnKLx/3DyR8FFaBd7CkBUx/hji+dfe1nzH/f1mbnrwb87d+OOfvPOr4h/DUXi798nkvgM
6iH+thh/7OTdf933MP9pBvMfW8TfFvEffHtHx9aJf3OKzH+4/zYnL/7ue77/0svBJhgSn0NVzD9tEX9bzH9ssf5vj/13W3nxZ/+x
WVz/drj/2uL+a6vo/J/9l+aw/2iL/Uc7Rccf7r/NYP5ji+vfFte/Leb/trj+bRF/W4w/trj+bXH92yL+toi/LeJvi/jbKhL/Dyd/
JKm3EKWLuyv+eemzBfbgU+wdHVt/c6jTAOPYrs7/zi2vdr8+tbb5+9C1/8z425I6jRhcA4y8hhczS6uaXF3h50Kd+P/+2WdTvz63
vNr9DPx47R0dW/dj7zz85DXd/+q2Hh15JfjvEfviWH+2RfxtMf+xRfztkX9oi/jbYf3ZFuO/La5/W5y/s1c0/5azv/HVvf4l4l8H
40/HkNV/+MHjhR26odQBiA5IzSL+toi/raLx3+odkKzkxd8h/s0pMnkh/s0h/raIvx3Gfzsu9kU6oBL/+IrGnw7kzWH8scXzr70i
859z70wGC3Ace+n7+pf3/k2/eedX60/7IqiVvLht/oyEC6CgnqLx97tlIx7GHztF5z9oBvMfW8TfFvF/OhD/5nDPtVUk/m6cOvna
L/sS4WY+v6MPf/dhY+9vK6s7//TWQJn/V8D83xbzH1us/9tj/91WXvzZf2wW178d7r+2uP/aKhp/9l+aw/6vLfYf7RQdf7j/NoP5
jy2uf1tc/7Y4f2eL698W8bfF+GOL698W178t4m+L+Nsi/raIv62i6z/JPXi39/7aT3+i4/tHaH6R4cHjhR1Trsjh8ubroaYLvo/n
7+54Y/zQ+uz8+3pm/G09mg/PQZEur/mFL/k5HN8/Ij/2fhOM//rueT2K+k63J9afbRF/W8x/bJH/Yy8rb4Hrv3nE3w7rz7YY/20x
/7RVNP6hc6cS5x9jKJ5/i9jqXv+oh/O/HWYNMKTtG/RBQfxtEX9bReLPA0BziiwAEX8bxN8W8bdF/JvH+G+HDQBbbADYY/yxxfPv
YKMAx2BIK8KB5vEzYIfYN6vO/ZcN+PqImy3ib4v4P70Y/20R//b4TTAkafrqb7vNL9IaByNfkbhlJcDxM1AP839bxM0W6/+Di/gP
BvYfbXD9N4/7ry3uv7ZowPB0YP/XBtd/s7j/2iL+toi/LeJvi/N3trj+bRF/W4w/trj+bXH92yL+toi/LeJvi/jbyot/svmF4+Ve
NfbetgoX424jDBWfd967clIHT3caMUjSB1eua2L3cOr3zyyt1nuzkBRuQPJk/n19/dZE93teuHhGuvlnfTl9s/vaxO5haUma1Bg5
iQUQI1vE3xbzH1vk/ww+4m+L+DeH+68txn9bReJPA4bm0IDh6UAThmYUvf6JfzPqnL/eKuP/M9ZvoCr3Aez1FrbRHuJvi/jbIv62
iL8t4m+L+Nsi/raIf30PHi/scL/K/l3iX19W/D+ev7tD6myAhX7deu937b9hdHH9t8MVnUwi/u05986k9VvYth48Xthx58a14Gdw
7KXv61/e+zd+BlpA/O2kjT/Ev3lp91/YYv5ji/jbIv7tYPy3lRV/fgba457D7ty4ppOv/ZLmFy1wMU/7GXBNSNAcxp/BROxtEX9b
xL9ZefuPe27PEX9DXP+2iH872P+1x/6vHfZ/7bH/aIfxfzARf1vE3xbxt0X8bRF/W8TfFvG3RfxtEX9bxN8W8bdF/G0R/3Y8PHws
+OvIO28R/xLqnHV/Mv++JGlydSW1yYV7fXJ1hZzQDXPL6Q1Bsr7m3Ltysht7xzW8+PLc5Z7mF2gX478t4m+L+Nsi/raIvy3ib4v4
t4P8Hzsu9xC2OINtJ+tngDGoecTfTt75661g4BtgcADbFvG3RfxtEX9bxN8W8R9cxL95XP+2iL8t4m+LDQBbXP928hbgiH/zKMBh
L+0zmLtxR59NT9u8qW2E+NvJGn+If7O4/9pj/mmL+Nsi/nYY/23RAGCwuAOUrhEGBx2b5/8M+D8H7trnc2gO44895j+2iL8t4j+4
iH/zuP5tEX87rD/YY//XHvuPdth/tMP4b4/5jy3ib4v42yL+toi/LeJvi/jbIv62iL8t4m+L+Nsi/raIv42P5+/ukKQ9t+dSfxH/
Zh08Pa2FB/M9v0JNMGh+0e/B44UdU2vZTS6m1lYLxSvZBAPtYfy3RfxtEX9bxH9wEf/mcf3bIv52yP8ZDMTfTtbPAPFvTyj+nH9s
D/G3wfhjbO/o2PqP/t+fr6+srPb9+uTTL9Z/9P/+fJ0PoDnE3xbxt0X8bRF/W8TfTlbsiX87uP5tEX9bxN9WkXsA8W8O17+9tM+A
+LfHfQa37/y1++vfLn9G/FvkfwbEvn3E305y/CH+7XGxT96Duf82j/mnLeJvi/jb4/nLVij+xB7byd7RsXV/Hsq1357Q/J/xpx3M
f2wRf1vE3w75J/a4/m0Rf3usP9hj/9ce+4922H+0w/hvh/mPLeJvi/jbIv62iL8t4m+L+Nsi/raIvy3ib4v42yL+toi/Hfbf7bwx
fmh97+jY+l8OHun7tXd0bP13ew71/OIz6Ld3dGz93O7x9XO7x9c/++7h9c++e7j753O7xzNj5uLvrnUX89Dn4X7xWcTH+G+L+Nsi
/raIvx3mn/a4/m0Rf3vk/9gi/vY4A2wrGX9i3y7ib4vxxxAHsG0Rf1vE3xbxt8XN1xbxt8Pigz2uf1vE3xbxt8U9wBbzf3ssgNqj
AIc9fywi9u0j/nYogGvHL0DM/bddzD9tEX9bxN9e8jMg/u1Kzn2IPbYjNw/l2m+XP/9n/GkX8x9bxN8W+4922Hu0x/Vvi/HfHvu/
9tj/tcf+ox2ef+2w/myH+Y8t4m+L+Nsi/raIvy3ib4v42yL+tlh/tkX8bRF/W8TfFvG3w/67jWQDhuQvPw+RzyCdi0+y8UVezEIN
SPaOpjfBoPlFc3j+skX8bRF/W8w/7TD/tMf1b4vx3x75n7aIvz3qb9gi/9MW8be1FcefHdZvoCgX6O+/9HL3tTs3runB44Wn5v/D
04z42yL+toi/rb2jY+t+7CXi3ybibycUe4n4t4nr3xbxt0X8bfnxn776W818fkcf/u5DPoOWMP+3lxyDiH/7/M+A+NtwYxGxt0H8
7fgbLsS/fYz/Nph/2iL+toi/veRnQPzblUw2IfYA2sTzlw3mP7aIvy32H+2Qf2KP698W47899n/tsf5vj/1HOzz/2mH92Q7zH1vE
3xbxt0X8bRF/W8TfFvG3Rfxtsf5si/jbIv62iL8t4m+H/XcbLu7TV3/b8zpnr8sru2/yxvih9dnFFSXjP7Z3XBeGRzSxe7j72szS
qiRpcnWFz6MhPH/ZIv62iL8t5p92mH/a4/q3xfhvj/xPW8TfHvm3tsj/tEX8bW218eepe/P8ANgi/raIvy3ib4cCQLaIv51QpzXi
3y6uf1vE3xbxt8UBYHvM/20Rf3sU4ACA7Ynx3w7zH1vE3xbxt8f4DwBAu5j/2CL+dth/tEP+iT2uf3uM/7aIvz3WfwBYYfyxw/3X
FvG3RfxtEX9bxN8W8bdF/G0RfzusP9si/raIvy3ib4v422H/3UayCQbNL9oTaoIx8/kd/fKnP9GF4ZGe76X5RTt4/rJF/G0RfzvM
P+0w/7TH9W+P8d8W8bdF/O2R/wbAylYaf576/wMAAAAAAGxVW2kBAgAAAAAAAAAAAAAAAAAAAAAAAAAAAADKcE0wHJpftMdvguHc
uXGt7/v4PAAAAAAAAAAksWgIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYODsHR1bd7+n2UK7XBMMh/gDAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIDB9v8Dgxjc
3GssnDwAAAAASUVORK5CYII=
"""
VIEW_FQ_B64 = """
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
9EFl3OtfGsS/7PqXJu+BxcGHuf4TtNn/2Iri33dNjD996/CseaWpUoDExnp7M0iIkg9rMtOl7ECS2ZBOYqx22HP9biEk1oOb5Ttw
8bPXfqsbVnI4afL56x6+Llp7ZL7Tr621FYmYV1X3MCpxr6+pfUK0Rbqmk/PRBnHs+Qg3CdPF7TXfhYs3/YXJVb7maNAeA+78T+y8
58LFm1pePDrcA3Tj7qed/c47iYm/m4S4aL3KzHuSeKA5vvk3X/EdabwYgNnzz/xbPSTD7ZZ7Nsi3r9Dd5yON7/uUOHtXR6jwuz3m
edmZf5AGY52z7366nWCyuA1IBhSHMxn5xT4D7HVKSRPJQVHOxNod75eNOym+0CzGPd0L5X3wnasw7ORLofPWSMe53zx8Y0+u/zxI
Pjm97OIXbuEL157ZJymCgUeS+zwwe67MXIQ0yBFj3gv23nxPe2++J2lUCIPiF+2w28D9uOn/yUNWXVHxC+/e582NYQGS36ze3uWb
Y0M8X84ryb8H3d5/vrx4dHse+vPhz/H1NS+svq/r899v/f9jpwgVv5BG6+ZmDOrrl6RBoSRdnSyQhHJNxF+iDWJV3QNh+iCJwvBV
kfQ/v5S1r2/+5f+pb33zu8M9/3/8079JH/1vXf66O1pT6wGhfejseysWOg+ZOg+9tLkxsc5elIsAA6E9EYdevTqxD8KnrPgI57D9
fLmC7Ws+tZBabA4Oabpi31kBDF8F1PnnDo4dOIpJXhJKQGB/v0QFPJ/YBDRu/N3Yzz93cCz+JKCJUzcBUCgBBPEv11TsFwcfZhNi
giqx9/U5ZYlPUM60hb2pf/nW596CC5L0yyf/3Ts5YdpDGi7KD695X4Ji3+/S53tCGrSF3Q5FxS8kaW3fYxOFGMqYjSzuy4T9bF/Q
jJYfbPbiuZDaF/3isc3g9b84+M9gX8QLb5i7COlP/DBA8p9msPk2P5LM5BNz/fuqzr7T5i/VM76Jt9h3sKXt5DP2omNZ8QuDhYBi
dsL5GKYPQzvc9vAl6JM0WpSU9Bd/KX3rm98lCX1DTB9zav7wVpMJEmmDeCbGvoPZA5/LHCaIeQ5IxN/lPpPtRDRu4RFpEPuz737q
Paj90y++oP8JYP4/L9a/8mH9N69Q/N987uDYZpPYZEz2PWBvIDWbcIn/pNh7oGzjiO8eoA8q5ou91Fz8zdekbhzqi6b7H5d9/Uvh
+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
"""
VIEW_BQ_B64 = """
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
1wVIiH+1HAkIig6aMgCtlrP4COIVJb0tmvRskujzwtl5LV78eGQAVFUMAOWTBe7rR2bnduuqL4fPYWnwoqW7GhbBcBPR4fOAF7I9
fqJbd2/4lR/d5h//eRzG/vIX65KoRh7LjfkPH3pEX28NFrz85FdO0RiIw6btsfnWBpve7BUdPJXYgNunsoNg7rmL/Lp8B6hK9u8U
bSSd5v6s6v+7/73Ud4Fzdx8ZG+/7xS8k6fGPPxgWwUA5t6GwSRtIxfNwYSGSJ18/L93443AR1G1EndaiDFXvY/7CcNn7WHj9hwvN
T75+Xk9KxNszshB2XxjzcFxUdL27whf+4nJRsU90U3jEYf6/GuuPtoi/Lb8vdvNoR2bndt07btk7mB/7P/z0Wb15+frY5gfmO+u5
uLy7sbf+fuDAd8O5npT196oCDLRBOb8NpGbXv6Sxe4DYxynaf3Jo9tHaOSD6//bYf2InjP3Z505r7Y8fFa5/xWAfSjPhIbAvf704
mBNISL7EGmS6qoRw/gGAmLUA2qEZ2mDyuPmeMCHBiZdWog9kFz0LJJ4HoRfnF3aXfjKntUs3h18b24uYGHvEIfmtHQouTIaidnDP
YbcP2k9MH5sgl2dxM2EhKqndcxj1/PWv0DAJU0ncw/kHt+4oSb84wDmCOu56b5L4IcRcTxq/AIM/3nHvXRLJKLtSdv4oTMAUuwcx
3NNGm9SrKkDLPdCt4d5naS+JScV8J7FuJyy2I+0lffP399TtLSz6d5nzr3dkdm7XJVCqSurDeZj+FT2L2xa+4x6IExYBCBMvhc9e
5t3y4gySHcZA/Qr7+c9XbozNNfvnrYvQBvm4eeUUzCs3U1Y8wXH3xfAMytZ2dBK+J367yhinQ67tzj53eux7K2vXSPyJB5p/zu7J
508N34+r1r38vbeXP1of+ffC86TLO9vcGwVWl57S4sWPJZWffYlJ+PnW8o9Hvn7x/c3OPvN+c/X8gl64dHO491aS6vb+o7myeVBJ
w2TnvpSiCy7HlSu4sP6DZzh7UcHff+7HyP96kxwQa7e3NXfg+2Husdd+8Myw+AVtUSw8CyA1S/5M7Jsruu7953FR/IvGQdfnn+Ps
V4Kzz53W8rX1sf2fq1s7kvc8+P/9dm+cE86B8g7WXtu1r7cfe4zC4y2E+z7RrbKzL05qIcKL72/qn76f0apG7xmeBWmKcl4dOBB3
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
NP6ZDHf9u/G9NDjzUvTOVZQQjmdwHAqv9a/o/MtIMSoN1lru3StP9Ewy+jxc7Fx7uLiH4yGJmHel6+K+KBaOSY7Mzu26eWWKX/Tn
xfmF3aWfzGnt0k2d+duntfbHj6w/0lQ4MjtI/ilV72V+8/J1LR6aGdnPWbW389WZg+z9zMhfo3rz8nUtb9UXiqEIRryyPZ/uHWxQ
/GKPX8wiXCuTyp8daCblTCmxbs5f/1q7+PFw/rKoeEvM3lv2MjRTtg5ctv+c/A/dqDuLx/7/7tQl35aIf1fqrnvk13Ye+tzdwfsA
e5vTuLnor77dfOji+weHc6CuCKqbD21SiJlCJPXC4heSV/hdLpeStHZblfuw3PUfrsezzzavcD1+2FZBAe3lne1h25GjL58w/r+b
Oz1SfEQanZvjGm+m6gz2fmdaAKNIWQKOKkxA59Mk/mgmJgEEyU+6Ufbi677WNPkYL2NxUoqPMOnZL78d/A2H6IeLv1sI2/jos5E2
qeqPGAu1xxioXy7pRmURpPuLkFXJH1wSGibjirWdeC4rALC8s61fHJhh838Jt+nNJR93G3qWt8Y33tZxG4Qc4l0sTMLgV1z2v1a1
+bzq2ndIgFWv7Bo9c+xgWvI3tBaXdFgjyf6bFFxwG0l9fpJ0v3I2fVi5MBF9atEFabQfI9bN5GoHvwiJxPM7VVHc71/fI+Oitdvb
Y32QX4iHfide+EweFsHQYKP6n195TVJxEQzmI8ox/z95mPuxxfqvjbo5Z3SvTRtwD7QXji1T7wHGlO348U9Z80I+jH/6wx4Ue+7w
UWwC0Jj1R4mEWE387OwbUe3wh98sjbWB4xL/h2iPeu5e+PLGK3ri1GtR6/GOvxZch7YY1dUhYA6IlSuK+erSU/p0807hIXiSv+XV
NPlt3TOYw17xihKaxBY/iil+QdKCeEWFGJ449Zo+++ITHT96svJZXJekzCVcdGs1f5ZG1mnCImLTcv+E71+fbt7Rz86+MTIHdO7u
I4XPg5TiF39+5TVppbw4/LSqml9wxS/KsAe6vTD+q0tP6fUrG0njH2KdLjz7snjx40bFN4l9c3XFfz/dvKPVT76Wv283HNc44bvv
tDw/23Jt4BKfx9wD5+4+onOPPTIsoikR7xSDsxaj+579vecxxS/8/f9u3Ejy+XixSZdc38P7VDdyJWJCGr8ogNv371TNwRUVv3Ao
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
ra4CYUwRAOLfXGz8y/p+H+2QLjX+LvHYkdm53R8+89zI3/n0w8ELAm0QL6X/qSpAInH9N5Ha/0vj7UDcm0kd+zjEP4+y4gv/MJz4
Xxn5XtgXEf92uP5tpb77Soz/c3JjyJWr/1r6M64NXMJJXzgOoh2aadIObuFFEm3QUtP7wLWB3w9JvH+liFkEjpmDlrj2m/DjX5b8
R5JOfbE1tgYjiWdwS8z/22L9yxbrv/Zi34MLi1+gtab3AHPQ+cSMQ6W9tjhz7OBY/Il9Oylj0avnF3gGZ1RXhFDai7tD/NtrOv6X
mH/Ooc0aAPHPo24drAjvwfkUHb6rir00ev07zH82k3L9V43/uf7TNd3/KfH8bavJ+q/j3wdrt0l41URs8n9pb/7fxz6IPGLXH9/6
7Vv69MNrle3AvZAmdv2xKPZc/+3lWH+RGPs01XTuWWLtNwfWH22x/m6ryfwbz918UuLP+nt+7H+wRf9ji+evLfp/W03PP3L950H+
AVtN4//CpZt6debg2N+j+EUarv/JcGR2NHGktHfet+wcMM+B7hyZndt9eP5lfb/xhn5xYFAA4/Sjg//95Tff6LMvPtGdp35U+vdX
t3boixo6Mju3W1UA43ePfqe129vD4hefr9wYfo+4p2H+3xbzP7Zy5CAg/s2FxS8cxp/9aZKDrOjskURbNJEr/sQ+Xa6zd8Q+XZv9
n9Le+y973tKlnnesmocm/s202X/Lns98Yvshci/ll5L/pyr3kkT8m0g9cy3t/9gf6Os/FBP8p+7/bzj4dBVHJA7cNdU0/pKGEz8S
8W+qSfyl0Yk3ifg3VZf04angz0UTnxLxbyql8pRE/HOLjX848Fm7vS3dvjb2d2iHNE3i7xKPffXt5kP6UFTbbKFJ5Ts34cD1315q
/y+NT/zo9v558epT3cRDVeVZicXftsriXxd3icq/OTS9/ul/8kh595V4/+1C0Riyij/xL42/B9AOzbh2eP6Ff6hMgiIF72AObdBK
k/hLXhvcph/qyrD6u8bnoOl/2gnHQIc/WR/7mWH8v7g2PvaRuPZbYP7fFutftlj/tRe7Bkbxi240vQeYg84vZvzv5oX+4ed/NxZ/
Yp9P0VhUGoxH9fO/G7sHiH1zfh9U9w4gFb9/Ef90TedAw/gT+2bargFIrL+01WQdrGwcRDukK4p/3RpkeP07xD9dyvVfN/4n/mna
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
"""


if __name__ == "__main__":
    main()