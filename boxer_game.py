#!/usr/bin/env python3
"""
BOXER - a tiny retro boxing game.

Starts in BAG mode (free practice on a heavy bag). Click the signs next to the BOXING GYM sign,
or press P for the same menu from the keyboard:
    SPAR                three rounds against a sparring partner (a different fighting style each time)
    CAMPAIGN            a boxing career, different every time: pick your fights from the offers on
                        the table, choose what to work on in camp, climb from club shows to a world
                        title - and make the calls the story puts in front of you
    BAG                 back to the heavy bag

    P                   the menu, wherever you are. At the gym it is where you pick SPARRING or
                        CAMPAIGN; in a fight it is RESUME / QUIT TO THE GYM, and in a career
                        RESUME / SAVE AND QUIT TO THE GYM. Leaving a fight always takes two
                        presses, so nothing gets thrown away by a mistyped key.

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
                       (swing and miss with either and your weight goes with it - see BALANCE)
    W                  slip  (dodges head shots; punch right after for a COUNTER)
    E  (hold)          high block   - stops head shots, body shots still land
    R  (hold)          low block    - stops body shots, head is open
                       Tap block just before a punch lands to PARRY it (attacker is stunned).
    P                  pause: where to next / leave this fight (see the top of this list)
    BACKSPACE          reset bag / restart fight
    1 / 2 / 3          sparring difficulty (easy / normal / hard)
    ENTER              rematch after a fight
    M  mute     F11  fullscreen     ESC  quit

Wind (stamina)
    * Every punch costs wind - a cross costs twice a jab. Blocking and walking cost a little too.
      Stop punching and it comes back; stand still and breathe and it comes back faster. You get
      almost none back while a punch is still running, so a wild spell you keep missing with empties
      the tank twice as fast: once for the punches, once for the long recoveries.
    * Empty the tank and you are GASSED: slower hands, weaker punches, a guard that caves in and
      a chin that will not hold up. Pace yourself. Rushing in is how you lose a fight you were winning.

Balance and weight (v12)
    A punch is not a move that either works or doesn't - it is a commitment, and you pay for it.
    * BALANCE is the blue bar under your wind. Throwing takes your weight off your feet. What it
      costs depends on the punch (a hook costs four times a jab), on how far you had to reach, and
      above all on what stopped it:
          landed flush  - cheapest. His head took the momentum, you stay square over your feet.
          caught on the gloves - dearer.
          hit thin air  - dearest by far. Nothing took your weight but the floor.
    * Low balance is not a penalty box, it's a slope: your punches lose the power that comes up off
      your legs, your hands slow down, your recovery drags, he shoves you around more easily, and
      you can no longer roll with a shot - so everything he throws hurts more. Spend past what you
      have and your feet go completely (OFF BALANCE) - you are wide open, and it is your own fault
      rather than a timer attached to one punch.
    * It comes back fastest standing still, slower on the move, barely at all mid-punch. A clinch is
      a rest for the legs. An empty wind tank costs you most of your recovery.
    * WEIGHT TRANSFER is the white pip on the balance bar: your feet have been planted long enough
      that the next punch will carry its full weight. It is a sliding scale, not a switch:
          feet planted  - the whole punch.
          on the move   - about two thirds of it. You can box on the move, you just give up power.
          side-step, pivot, mid-punch - nothing. Your weight is in the air.
      Walking also bleeds off weight you had already set, so you cannot plant once and then circle
      all night at full power. Chaining spends it too: the second shot of a combo is an arm punch
      and the third is barely a punch at all. Mashing one button is the worst thing you can do -
      give yourself a beat on your feet and the next one lands like a different punch.
    * Your opponents know this, to different degrees. A club fighter barely sets his feet and
      arm-punches his way through a fight; a world champion sits down on everything. Out-boxers and
      counter-punchers are never caught punching off the back foot, while swarmers and brawlers
      throw from wherever they happen to be standing - which is what makes them catchable coming in.
      When a good opponent stops dead in front of you, he is loading one up. That is your moment.
    * The same goes for him. Catch him with his hands still out - on the way back from a punch, not
      just on the way out - and there is nothing between your glove and his chin.

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
DMG_SCALE = 0.36             # rounds are long: punches do less, fights go the distance more often
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
STAM_REGEN_PUNCH = 0.15      # a man still reeling his hand in is not catching his breath. Without
                             # this, stretching a punch's recovery (REC_WHIFF) would hand out wind
                             # as a reward for throwing wildly.
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
# v4: the canvas. F_KO above is the old crouch, kept for anything that still wants a stumble-down.
F_FALL = (66, 67, 68)        # legs buckle -> hips drop -> he lands on the canvas
F_DOWN = (69, 70)            # lying there for the count, chest going (alternated: he is breathing)
F_RISE = (71, 72, 73)        # onto a knee -> pushing up -> standing, unsteady
# Out cold. The frames are authored standing and the game tilts them over as he falls, so a pose
# that will be shown on its side keeps its limbs on one side of the spine - otherwise a boot ends
# up under his back and holds him off the canvas. See the notes in build_strip_v5/v6.py.
F_LIMP = (74, 75)            # flat on his back, where a stiff fall ends
F_CRUMPLE = (76, 77)         # a heap on his side, where a crumple ends
F_BODY = (78, 79)            # curled round his ribs, where a body shot ends
F_FACEDOWN = (92, 93)        # face down, where a hook puts him

# A fall, as a little timeline: (how far through the fall, which frame, how far over he is by then).
# The pose does the collapsing; the angle only says where the floor is. The last entry is the
# landing - same frame, final angle - so the body keeps turning after it has run out of poses.
KO_SEQ = {
    "stiff":   ((0.00, 80, 0.0), (0.22, 81, 8.0), (0.46, 82, 32.0), (0.72, F_LIMP[0], 66.0),
                (1.00, F_LIMP[0], 90.0)),
    "crumple": ((0.00, 83, 0.0), (0.22, 84, 4.0), (0.44, 85, 13.0), (0.64, 94, 34.0),
                (0.82, F_CRUMPLE[0], 58.0), (1.00, F_CRUMPLE[0], 84.0)),
    "body":    ((0.00, 86, 0.0), (0.24, 87, 4.0), (0.48, 88, 14.0), (0.68, 95, 36.0),
                (0.84, F_BODY[0], 62.0), (1.00, F_BODY[0], 88.0)),
    "spin":    ((0.00, 89, 0.0), (0.20, 90, 9.0), (0.44, 91, 30.0), (0.70, F_FACEDOWN[0], 64.0),
                (1.00, F_FACEDOWN[0], 90.0)),
}
KO_SETTLE = {"stiff": F_LIMP[1], "crumple": F_CRUMPLE[1], "body": F_BODY[1], "spin": F_FACEDOWN[1]}
KO_SETTLE_T = 0.15           # how long after he lands before he settles into the last pose
KO_FALL_T = 0.48             # how long a stiff fall takes, start to canvas
KO_SPEED = {"stiff": 1.0, "crumple": 0.76, "body": 0.66, "spin": 0.92}   # ...the rest, against that
KO_BOUNCE = {"stiff": 9.0, "crumple": 3.0, "body": 1.5, "spin": 2.0}     # how hard he lands
KO_DIR = {"stiff": 1, "crumple": 1, "body": 1, "spin": -1}               # backwards, or onto his face
KO_PUNCH = {"hook": "spin", "uppercut": "crumple",                       # what each punch does to him
            "body_jab": "body", "body_cross": "body"}
COMBO_KO = 4                 # clean shots taken in a row that count as "worn down" rather than one shot
FRAME_COUNT = 96             # drawings in the strip, every view the same
FALL_T = (0.10, 0.24, 0.40)  # how long each stage of the fall holds
BREATH = 1.9                 # seconds per breath while he is down

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
BIG_SHOTS = ("hook", "uppercut")   # the two you really have to commit your weight to
OFF_BALANCE = 0.3            # (kept for the old tests: stumbles are timed by STUMBLE_TIME now)
WIDE_LAT = 2.3               # a hook's arc catches a man this many times further off the line

# ============================================================ balance, weight transfer, exposure
# A punch is not a move that resolves - it is a commitment. Throwing one takes your weight off your
# feet, leaves your hand out of position, and takes a beat to come back from. How big a beat depends
# on how far you reached, on what (if anything) stopped it, and on whether you were set when you
# threw it. None of this is a flag: it is all a matter of degree, which is what makes overcommitting
# feel dangerous instead of merely unlucky.
BAL_MAX = 1.0
BAL_COST = {"jab": 0.07, "cross": 0.19, "body_jab": 0.09, "body_cross": 0.21,
            "hook": 0.30, "uppercut": 0.26}
BAL_WHIFF = 1.5              # swung through thin air: nothing took your weight but the floor
BAL_LAND = 0.55              # it landed: his head or his ribs absorbed it and you stay squarer
BAL_BLOCK = 0.80             # he caught it on the gloves
BAL_REACH = 0.55             # extra share of the cost for a punch thrown at full stretch
BAL_REGEN = 0.78             # /s with your feet planted and nothing else going on
BAL_REGEN_MOVE = 0.42        # /s on the move
BAL_REGEN_PUNCH = 0.16       # /s while the punch is still going out
BAL_REGEN_REC = 0.34         # /s while you are getting the hand back and the weight over your feet
BAL_GAS = 0.55               # share of your recovery a dead tank costs you
BAL_HIT = 0.14               # taking one clean rocks you back...
BAL_HIT_MOVE = 0.26          # ...and more if you walked onto it
BAL_PUSH = 0.016             # balance lost per pixel of knockback
BAL_MOVED = 1.6              # how much easier a man off balance is to shove around
BAL_STUMBLE = 0.10           # spend past this and your feet go
STUMBLE_MIN, STUMBLE_MAX = 0.26, 0.52    # how long for, by how far past the line you went
BAL_POWER = 0.42             # share of a punch's power that comes up off your legs
BAL_SPEED = 0.20             # share of your hand speed that needs your weight under you
BAL_ROLL = 0.30              # how much harder a punch lands on a man who cannot roll with it
BAL_PARRY = 0.34             # getting parried takes your weight with it

# Weight transfer: seconds with your feet under you, up to SET_TIME, is what you have to drive a
# punch with. Chaining spends most of it, so the second shot of a combo is an arm punch - mix in a
# beat on your feet and the next one carries. SET_FLOOR is a punch with nothing behind it at all.
SET_TIME = 0.40
SET_FLOOR = 0.55
SET_KEEP = 0.45              # share of your set-ness still there for the next punch
SET_REPLANT = 0.5            # how fast your feet come back under you through a punch's recovery
SET_WALK = 0.45              # ...and how fast while you are walking, up to:
SET_WALK_CAP = 0.25          # the most weight you can get behind a punch without planting your feet
SET_SHED = 1.0               # ...and how fast walking bleeds off weight you had already set. Without
                             # this you could plant once and then circle all night at full power.

# Exposure: how far out of position the hand you threw is, 0..1 scaled by the size of the punch.
EXPOSE = {"jab": 0.40, "cross": 0.75, "body_jab": 0.50, "body_cross": 0.85,
          "hook": 1.00, "uppercut": 0.90}
EXPOSE_RISE = 7.0            # /s as the punch goes out
EXPOSE_FALL = 2.6            # /s as you bring it back
EXPOSE_GUARD = 0.50          # a hand that is out is not blocking: the guard drains faster
EXPOSE_IMPACT = 0.75         # how much harder a punch lands on a man whose hands are out

# Recovery: the back half of a punch stretches with what happened to the front half.
REC_WHIFF = 1.75             # it hit nothing...
REC_BLOCK = 1.20             # ...or got caught on the gloves
REC_LAND = 0.85              # landing flush gets you back on balance quickest
REC_BAL = 1.10               # being off balance drags it out
REC_GAS = 0.45               # so does a dead tank
REC_MAX = 3.20

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
SET_UP_MULT = 1.35           # ...and on the heavy bag, where nothing bites, for landing in time
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
                 combo=0.20, flurry=0.25, punish=0.20, guard_up=0.10, learn=0.3, feint=0.0, pace=0.45,
                 plant=0.38),
    "NORMAL": dict(react=0.63, delay=(0.12, 0.22), slip=0.25, wrong=0.18, parry=0.30, atk=(0.6, 1.4),
                   combo=0.35, flurry=0.50, punish=0.55, guard_up=0.20, learn=1.0, feint=0.18, pace=0.8,
                   plant=0.72),
    "HARD": dict(react=0.76, delay=(0.09, 0.17), slip=0.30, wrong=0.12, parry=0.45, atk=(0.45, 1.1),
                 combo=0.50, flurry=0.70, punish=0.70, guard_up=0.25, learn=1.5, feint=0.3, pace=1.0,
                 plant=1.00),
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
    band=(226, 44, 48), band_l=(254, 126, 112), band_s=(148, 24, 46),   # the headband, on its own now
    stripe=(222, 46, 56), stripe_far=(146, 20, 48),                     # ...and the stripe on his boot
)

# Which pixels are which garment, and which shade of the trim each of them becomes when a design
# is painted on: 0 the trim itself, 1 its shadow, 2 its highlight. The boot stripe is deliberately
# NOT part of the boot: it follows his gloves, the way a fighter's kit usually does.
GARMENT_PARTS = dict(
    shorts=(("shorts", 0), ("shorts_s", 1), ("shorts_l", 2)),
    boots=(("boot", 0), ("boot_s", 1), ("boot_far", 1), ("boot_far_s", 1)),
    band=(("band", 0), ("band_s", 1), ("band_l", 2)),
    glove=(("glove", 0), ("glove_d", 1), ("glove_l", 2),
           ("glove_far", 1), ("glove_far_d", 1), ("glove_hl", 2)),
)
GARMENT_COLS = {slot: tuple(SRC[k] for k, _ in parts) for slot, parts in GARMENT_PARTS.items()}


def _mix(c, target, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c, target))


def lighten(c, t):
    return _mix(c, (255, 255, 255), t)


def darken(c, t):
    return _mix(c, (0, 0, 0), t)


def look_palette(glove=None, shorts=None, skin=None, hair=None, boots=None, band=None):
    """Recolour map (player colour -> new colour) built from a few base colours.
    The headband follows the gloves unless it is given a colour of its own; the boot stripes
    always follow the gloves. hair="bald" shaves the head."""
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
    b = band or glove            # a fighter with no headband of his own wears one to match his gloves
    if b:
        m.update({SRC["band"]: b, SRC["band_l"]: lighten(b, .45), SRC["band_s"]: darken(b, .35)})
    if glove:                    # ...and the stripe on his boots matches them too
        m.update({SRC["stripe"]: glove, SRC["stripe_far"]: darken(glove, .35)})
    return m


SPAR_LOOK = dict(glove=(52, 110, 230), shorts=(196, 40, 52), skin=(170, 108, 70), hair=(232, 196, 92),
                 boots=(64, 66, 90))

# ============================================================ the pro shop: kit, and what it costs
# Four things he wears, and each of them is TWO purchases: the colour of it, and the design on it.
# They are sold apart because they are worth owning apart - a man with four colours and four
# designs has sixteen pairs of trunks, not eight. The slot names are the same words look_palette()
# uses, so the colours he is wearing ARE the recolour map; the designs are painted on afterwards.
WARDROBE_SLOTS = ("shorts", "boots", "band", "glove")
KINDS = ("color", "design")
SLOT_NAME = dict(shorts="TRUNKS", boots="BOOTS", band="HEADBAND", glove="GLOVES")
SLOT_SHORT = dict(shorts="TRUNKS", boots="BOOTS", band="BAND", glove="GLOVES")   # for narrow columns
KIND_NAME = dict(color="COLOUR", design="DESIGN")
SLOT_BLURB = dict(shorts="satin, and a waistband that stays put",
                  boots="ankle support and a sole that bites",
                  band="keeps the sweat out of your eyes",
                  glove="ten ounces, horsehair and leather")


def _col(key, slot, name, price, color, stock=True):
    return dict(kind="color", key=key, slot=slot, name=name, price=price, color=color, stock=stock)


def _des(key, slot, name, price, trim, bands, stock=True):
    """A design is WHERE THE TRIM GOES, as fractions of the garment's own box: (x, y, w, h). The
    rule is in fractions rather than pixels so the same stripe fits him standing, turned away, or
    flat out on the canvas, in every one of the 96 drawings. No bands means plain."""
    return dict(kind="design", key=key, slot=slot, name=name, price=price, color=trim,
                bands=bands, stock=stock)


WHITE_TRIM, GOLD_TRIM, BLACK_TRIM = (242, 242, 246), (230, 184, 60), (34, 32, 44)
# His own kit: THE COLOURS THE SPRITE WAS PAINTED IN, plain. Wearing them means nothing is
# recoloured and nothing is painted on, so the default fighter is the one that was always there.
KIT = [
    _col("trunks_gym", "shorts", "GYM BLUE", 0, (46, 98, 208), False),
    _col("boots_canvas", "boots", "WHITE CANVAS", 0, (246, 246, 248), False),
    _col("band_red", "band", "RED CLOTH", 0, (226, 44, 48), False),
    _col("gloves_red", "glove", "RED LEATHER", 0, (224, 40, 52), False),
    _des("trunks_plain", "shorts", "PLAIN", 0, WHITE_TRIM, (), False),
    _des("boots_plain", "boots", "PLAIN", 0, WHITE_TRIM, (), False),
    _des("band_plain", "band", "PLAIN", 0, WHITE_TRIM, (), False),
    _des("gloves_plain", "glove", "PLAIN", 0, WHITE_TRIM, (), False),
]
# What the shop stocks. A first-fight purse is about $500 and a ranked one a few thousand, so a
# headband is pocket money and anything gold is a reason to keep winning.
STOCK = [
    _col("trunks_crimson", "shorts", "CRIMSON", 450, (196, 36, 48)),
    _col("trunks_emerald", "shorts", "EMERALD", 650, (26, 148, 96)),
    _col("trunks_midnight", "shorts", "MIDNIGHT", 800, (38, 38, 66)),
    _col("trunks_gold", "shorts", "GOLD LEAF", 2200, (226, 176, 52)),
    _col("boots_black", "boots", "BLACK LEATHER", 500, (46, 46, 58)),
    _col("boots_red", "boots", "RED DEVILS", 700, (198, 42, 44)),
    _col("boots_royal", "boots", "ROYAL BLUE", 900, (48, 86, 198)),
    _col("boots_gold", "boots", "GOLD TOPS", 2600, (224, 174, 56)),
    _col("band_white", "band", "WHITE CLOTH", 300, (240, 240, 244)),
    _col("band_black", "band", "BLACK CLOTH", 350, (40, 38, 52)),
    _col("band_green", "band", "GREEN CLOTH", 400, (36, 160, 102)),
    _col("band_gold", "band", "GOLD SILK", 1500, (230, 182, 60)),
    _col("gloves_black", "glove", "BLACK LEATHER", 900, (44, 42, 56)),
    _col("gloves_blue", "glove", "BLUE LEATHER", 1100, (44, 98, 214)),
    _col("gloves_white", "glove", "WHITE LEATHER", 1300, (238, 238, 244)),
    _col("gloves_gold", "glove", "GOLD LEATHER", 3500, (228, 178, 56)),
    _des("trunks_stripe", "shorts", "SIDE STRIPE", 600, WHITE_TRIM, ((0.40, 0.0, 0.24, 1.0),)),
    _des("trunks_waist", "shorts", "WAISTBAND", 850, GOLD_TRIM, ((0.0, 0.0, 1.0, 0.30),)),
    _des("trunks_tone", "shorts", "TWO-TONE", 1200, BLACK_TRIM, ((0.0, 0.52, 1.0, 0.48),)),
    _des("trunks_champ", "shorts", "CHAMPIONSHIP", 3200, GOLD_TRIM,
         ((0.0, 0.0, 1.0, 0.26), (0.40, 0.26, 0.24, 0.74))),
    _des("boots_stripe", "boots", "SIDE STRIPE", 550, WHITE_TRIM, ((0.40, 0.0, 0.26, 1.0),)),
    _des("boots_top", "boots", "TOP BAND", 750, GOLD_TRIM, ((0.0, 0.0, 1.0, 0.34),)),
    _des("band_centre", "band", "CENTRE STRIPE", 400, WHITE_TRIM, ((0.0, 0.32, 1.0, 0.36),)),
    _des("band_edge", "band", "TRIMMED", 550, GOLD_TRIM, ((0.0, 0.0, 1.0, 0.26), (0.0, 0.74, 1.0, 0.26))),
    _des("gloves_cuff", "glove", "WHITE CUFF", 1000, WHITE_TRIM, ((0.0, 0.70, 1.0, 0.30),)),
    _des("gloves_bar", "glove", "KNUCKLE BAR", 1400, GOLD_TRIM, ((0.0, 0.26, 1.0, 0.26),)),
]
ITEMS = {it["key"]: it for it in KIT + STOCK}
DEFAULT_WORN = {slot: {} for slot in WARDROBE_SLOTS}
for _it in KIT:
    DEFAULT_WORN[_it["slot"]][_it["kind"]] = _it["key"]
assert all(set(v) == set(KINDS) for v in DEFAULT_WORN.values()), "every slot starts with both"


def trim_shades(garment, trim):
    """The three shades a design paints with - the trim, its shadow and its highlight - nudged
    first if they would vanish into the cloth. Gold trim on gold trunks is not a design, it is a
    plain pair of trunks you paid extra for, so a trim too close to its cloth goes dark on a light
    garment and light on a dark one."""
    if sum(abs(a - b) for a, b in zip(garment, trim)) < 150:
        trim = darken(trim, 0.45) if sum(garment) > 380 else lighten(trim, 0.6)
    return [trim, darken(trim, .38), lighten(trim, .40)]


def slot_items(slot, kind, stock_only=False):
    """Everything of one kind for one slot, what he came in with first."""
    return [it for it in (STOCK if stock_only else KIT + STOCK)
            if it["slot"] == slot and it["kind"] == kind]

# ============================================================ the shop: the room itself
SHOP_BACK, SHOP_FRONT = 120, 158     # the feet of a man at the racks / at the front of the shop
SHOP_WALK, SHOP_WALK_Z = 88.0, 48.0  # how fast he walks along the shop, and in and out of it
SHOP_MARGIN = 78                     # the door end to the first peg
SHOP_PITCH = 32                      # one peg to the next
SHOP_SECTION_GAP = 26                # one section to the next
SHOP_NEAR_X = 19.0                   # how close you stand to be served
SHOP_NEAR_Y = 20.0                   # ...and how far down the shop you may be while standing there
SHOP_PEG_Y = 50                      # the colours, hanging on the pegboard
SHOP_PEG_TAG = 67                    # ...and their price tickets
SHOP_SHELF_Y = 93                    # the shelf board under them
SHOP_SHELF_ICON = 77                 # the designs, standing on the shelf
SHOP_SHELF_TAG = 98
SHOP_ROW_Y = 13.0                    # step back from the wall by this and you are at the shelf
SHOP_CONFIRM_T = 5.0                 # a confirm nobody answers lapses
SHOP_FLASH_T = 1.7                   # how long "BOUGHT" stays up
SHOP_SIGN = "RUIZ BROS. BOXING SUPPLY"
DESIGN_CLOTH = (108, 112, 138)       # the plain cloth a design is shown on, on its own peg


def shop_layout():
    """Where everything stands. Each section of the shop is a run of positions; the COLOURS hang
    on the pegboard above and the DESIGNS stand on the shelf below, so walking up to the wall and
    stepping back a pace are two different things to be looking at. (stands, signs, room width)."""
    stands, signs = [], []
    x = SHOP_MARGIN
    for slot in WARDROBE_SLOTS:
        cols = slot_items(slot, "color", stock_only=True)
        dess = slot_items(slot, "design", stock_only=True)
        x0 = x
        for i in range(max(len(cols), len(dess))):
            if i < len(cols):
                stands.append(dict(kind="item", row="wall", key=cols[i]["key"], slot=slot, x=float(x)))
            if i < len(dess):
                stands.append(dict(kind="item", row="shelf", key=dess[i]["key"], slot=slot, x=float(x)))
            x += SHOP_PITCH
        signs.append(dict(text=SLOT_NAME[slot], slot=slot,
                          x0=x0 - SHOP_PITCH // 2, x1=x - SHOP_PITCH // 2))
        x += SHOP_SECTION_GAP
    x += 14
    stands.append(dict(kind="mirror", row="wall", key=None, slot=None, x=float(x)))
    return stands, signs, int(x + SHOP_MARGIN)


def mirror_glass(x):
    """The looking-glass part of the mirror standing at x (room coordinates)."""
    return pygame.Rect(int(x) - 17, 44, 34, 70)


def icon_garment(slot, color):
    """A little drawing of the thing itself in its own colour - trunks, a boot, a headband, a
    glove - outlined so it reads against the wall, plus the box its cloth occupies so a design
    can be painted into it. 18 x 16."""
    w, h = 18, 16
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    ol = (22, 14, 30)
    lo, hi = darken(color, 0.34), lighten(color, 0.34)

    def box(x, y, bw, bh, col):
        pygame.draw.rect(s, ol, (x - 1, y - 1, bw + 2, bh + 2))
        pygame.draw.rect(s, col, (x, y, bw, bh))

    if slot == "shorts":
        box(2, 2, 14, 6, color)                                  # the waist
        box(2, 8, 5, 6, color)                                   # ...and the two legs
        box(11, 8, 5, 6, color)
        s.fill(hi, (3, 3, 12, 1))
        s.fill(lo, (3, 12, 4, 1))
        s.fill(lo, (12, 12, 4, 1))
        cloth = pygame.Rect(2, 2, 14, 12)
    elif slot == "boots":
        box(5, 1, 7, 9, color)                                   # the ankle
        box(2, 10, 13, 3, color)                                 # the foot
        pygame.draw.rect(s, ol, (1, 12, 15, 3))
        pygame.draw.rect(s, (236, 236, 240), (2, 13, 13, 1))     # the sole
        s.fill(hi, (6, 3, 5, 1))
        s.fill(lo, (6, 8, 5, 1))
        cloth = pygame.Rect(2, 1, 13, 12)
    elif slot == "band":
        box(1, 5, 16, 4, color)                                  # the band
        s.fill(hi, (2, 6, 14, 1))
        box(12, 9, 3, 5, color)                                  # ...and one tail hanging
        s.fill(lo, (13, 11, 1, 3))
        cloth = pygame.Rect(1, 5, 16, 4)
    else:
        pygame.draw.ellipse(s, ol, (2, 1, 14, 12))               # the mitt
        pygame.draw.ellipse(s, color, (3, 2, 12, 10))
        pygame.draw.ellipse(s, ol, (0, 6, 6, 7))                 # the thumb
        pygame.draw.ellipse(s, color, (1, 7, 4, 5))
        box(4, 11, 10, 3, lo)                                    # the cuff
        pygame.draw.ellipse(s, hi, (5, 3, 7, 4))
        cloth = pygame.Rect(1, 1, 15, 13)
    return s, cloth


def paint_icon(icon, cloth, color, design):
    """Put a design's trim onto an icon, the same way it goes onto the sprite: bands measured as
    fractions of the garment's own box."""
    if not design or not design.get("bands"):
        return icon
    into = trim_shades(color, design["color"])
    pairs = list(zip((color, darken(color, 0.34), lighten(color, 0.34)), into))
    pa = pygame.PixelArray(icon)
    try:
        for bx, by, bw, bh in design["bands"]:
            x0 = cloth.x + int(round(cloth.w * bx))
            y0 = cloth.y + int(round(cloth.h * by))
            x1 = min(cloth.right, x0 + max(1, int(round(cloth.w * bw))))
            y1 = min(cloth.bottom, y0 + max(1, int(round(cloth.h * bh))))
            if x1 <= x0 or y1 <= y0:
                continue
            patch = pa[x0:x1, y0:y1]
            for src_c, dst_c in pairs:
                patch.replace(src_c, dst_c)
    finally:
        pa.close()
    return icon


def make_item_icon(item, color=None, scale=1):
    """The icon for one thing on sale: a colour shown plain, or a design shown on plain cloth."""
    if item["kind"] == "color":
        icon, cloth = icon_garment(item["slot"], item["color"])
    else:
        icon, cloth = icon_garment(item["slot"], color or DESIGN_CLOTH)
        paint_icon(icon, cloth, color or DESIGN_CLOTH, item)
    return pygame.transform.scale(icon, (icon.get_width() * scale, icon.get_height() * scale)) if scale > 1 else icon


def make_shop_room(stands, signs, room_w):
    """The shop, one surface as wide as the room: wall, floor, the pegboards and their shelves,
    the signs over them, the door you came in by, and the long mirror at the far end."""
    s = pygame.Surface((room_w, VH))
    wall, wall_d, wall_l = (66, 54, 80), (46, 36, 58), (84, 70, 100)
    board, board_d = (92, 76, 104), (60, 48, 74)
    floor, floor_d = (112, 80, 56), (86, 58, 40)
    wood, wood_l, wood_d = (136, 98, 62), (172, 130, 86), (92, 62, 38)
    brass = (214, 172, 72)
    s.fill(wall)
    s.fill(wall_d, (0, 0, room_w, 15))                                  # the ceiling
    for x in range(0, room_w, 16):                                      # the wallpaper
        s.fill(wall_l, (x, 15, 2, SHOP_BACK - 26))
    s.fill(wood_d, (0, SHOP_BACK - 13, room_w, 3))                      # the chair rail
    s.fill((54, 42, 66), (0, SHOP_BACK - 10, room_w, 10))               # the skirting
    s.fill(floor, (0, SHOP_BACK, room_w, VH - SHOP_BACK))
    for k in range(0, VH - SHOP_BACK, 7):                               # the floorboards
        s.fill(floor_d, (0, SHOP_BACK + k, room_w, 1))
    for x in range(0, room_w, 28):
        s.fill(floor_d, (x, SHOP_BACK, 1, VH - SHOP_BACK))
    shade = pygame.Surface((room_w, 9), pygame.SRCALPHA)                # the wall's shadow
    shade.fill((18, 10, 26, 95))
    s.blit(shade, (0, SHOP_BACK))

    f = pygame.font.Font(None, 14)
    f_big = pygame.font.Font(None, 18)
    for sg in signs:                                                    # a section: pegboard,
        x0, x1 = sg["x0"], sg["x1"]
        pygame.draw.rect(s, board_d, (x0 - 2, 44, x1 - x0 + 4, 51))
        pygame.draw.rect(s, board, (x0, 46, x1 - x0, 47))
        for py in range(50, 92, 5):                                     # ...with its peg holes,
            for px in range(x0 + 3, x1 - 2, 5):
                s.fill(board_d, (px, py, 1, 1))
        pygame.draw.rect(s, wood_d, (x0 - 3, SHOP_SHELF_Y, x1 - x0 + 6, 4))   # ...a shelf under them,
        s.fill(wood_l, (x0 - 3, SHOP_SHELF_Y, x1 - x0 + 6, 1))
        for bx in (x0 + 2, x1 - 6):
            s.fill(wood_d, (bx, SHOP_SHELF_Y + 4, 4, 5))
        mid = (x0 + x1) // 2                                            # ...and its sign
        label = f.render(sg["text"], False, (40, 28, 20))
        pw = label.get_width() + 12
        pygame.draw.rect(s, (28, 20, 34), (mid - pw // 2 - 1, 26, pw + 2, 15))
        pygame.draw.rect(s, brass, (mid - pw // 2, 27, pw, 13))
        s.fill(lighten(brass, 0.4), (mid - pw // 2, 27, pw, 1))
        s.blit(label, (mid - label.get_width() // 2, 29))
        for txt, yy in (("COLOURS", 40), ("DESIGNS", SHOP_SHELF_TAG + 11)):
            lab = f.render(txt, False, (156, 142, 176))
            s.blit(lab, (mid - lab.get_width() // 2, yy))

    pygame.draw.rect(s, (34, 24, 40), (10, 44, 42, SHOP_BACK - 44))     # the door you came in by
    pygame.draw.rect(s, wood, (12, 46, 38, SHOP_BACK - 46))
    pygame.draw.rect(s, wood_d, (16, 50, 30, 34))
    s.fill(wood_l, (16, 50, 30, 1))
    pygame.draw.circle(s, brass, (44, 92), 2)
    pygame.draw.rect(s, (24, 16, 30), (6, 26, 54, 15))                  # ...and the shop's name
    name = f.render("RUIZ BROS.", False, (255, 222, 140))
    s.blit(name, (33 - name.get_width() // 2, 29))
    s.fill((120, 90, 60), (10, SHOP_BACK + 2, 44, 6))                   # the mat
    s.fill((150, 114, 76), (10, SHOP_BACK + 2, 44, 1))

    for st in stands:                                                   # the mirror
        if st["kind"] != "mirror":
            continue
        g = mirror_glass(st["x"])
        pygame.draw.rect(s, wood_d, g.inflate(10, 10))
        pygame.draw.rect(s, wood, g.inflate(6, 6))
        s.fill(wood_l, (g.x - 3, g.y - 3, g.w + 6, 1))
        pygame.draw.rect(s, (36, 40, 56), g)
        for k in range(g.h):                                            # ...and its cold glass
            t = k / max(1, g.h - 1)
            s.fill((int(40 + 26 * t), int(46 + 28 * t), int(64 + 30 * t)), (g.x, g.y + k, g.w, 1))
        pygame.draw.line(s, (120, 136, 168), (g.x + 4, g.bottom - 8), (g.right - 8, g.y + 6))
        pygame.draw.line(s, (90, 104, 136), (g.x + 10, g.bottom - 6), (g.right - 5, g.y + 14))
        lab = f.render("TRY IT ON", False, (255, 236, 170))
        s.blit(lab, (g.centerx - lab.get_width() // 2, g.bottom + 8))

    big = f_big.render(SHOP_SIGN, False, (255, 206, 120))               # the sign along the ceiling
    for dx in range(0, room_w + big.get_width(), big.get_width() + 90):
        s.blit(big, (dx + 70, 2))
    return s


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
# How much a man of each style bothers to set his feet before he lets a power shot go, on top of
# whatever his tier gives him. Technicians sit down on their punches; come-forward fighters throw
# from wherever they happen to be standing, which is why they are easier to catch coming in.
# Short forms of the style names, for when the full one will not fit beside the gym sign.
STYLE_SHORT = {"outboxer": "OUT-BOXER", "swarmer": "PRESSURE", "slugger": "SLUGGER",
               "counter": "COUNTER", "volume": "VOLUME", "peekaboo": "PEEK-A-BOO",
               "spoiler": "SPOILER", "body": "BODY", "brawler": "BRAWLER",
               "boxer_puncher": "BOXER-P."}
SPAR_LABEL_X = 214           # the opponent's label must not start left of this (the gym sign)
PLANT_STYLE = {"outboxer": 0.22, "counter": 0.26, "boxer_puncher": 0.20, "peekaboo": 0.12,
               "slugger": 0.10, "body": 0.06, "volume": -0.14, "spoiler": -0.10,
               "swarmer": -0.20, "brawler": -0.24}
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
    p["plant"] = clamp(p["plant"] + PLANT_STYLE.get(style, 0.0), 0.04, 1.0)
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


def view_sector(d):
    """Which drawing of him suits facing d degrees: 0 is to the right, +90 is toward the camera,
    -90 is away from it. Used by the fighters in the ring and by him walking round the shop."""
    a = abs(d)
    if a <= 22.5 or a >= 157.5:
        return "side"
    if 67.5 <= a <= 112.5:
        return "f" if d > 0 else "b"
    return "fq" if d > 0 else "bq"


def make_views(strips, mapping=None, painter=None):
    """{"side": (right, left), "fq": (right, left), "bq": (right, left), "f": set, "b": set},
    recoloured, and then painted on if he is wearing a design. The painting happens to the STRIP,
    before it is cut into frames, so both the right- and left-facing sets get it and the flipped
    one comes out mirrored for free."""
    out = {}
    for key, strip in strips.items():
        base = strip if not mapping else recolor(strip, mapping)
        if painter is not None:
            base = painter(key, base if base is not strip else strip.copy())
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
LOCKER_NAME = ".boxer_locker.json"     # the wallet and the wardrobe: they outlive any one career


def data_path(name):
    for base in (os.path.expanduser("~"), os.path.dirname(os.path.abspath(__file__)), tempfile.gettempdir()):
        try:
            if os.path.isdir(base) and os.access(base, os.W_OK):
                return os.path.join(base, name)
        except OSError:
            continue
    return os.path.join(tempfile.gettempdir(), name)


def save_path():
    return data_path(SAVE_NAME)


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


def load_locker():
    """The wallet and wardrobe, or None. A broken file is simply ignored."""
    try:
        with open(data_path(LOCKER_NAME)) as fh:
            d = json.load(fh)
        return d if isinstance(d, dict) else None
    except (OSError, ValueError):
        return None


def save_locker(data):
    try:
        with open(data_path(LOCKER_NAME), "w") as fh:
            json.dump(data, fh)
        return True
    except OSError:
        return False


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
             ("Q", "CLINCH"), ("X", "PIVOT"), ("P", "PAUSE / MENU"))
FIGHT_TIPS = ("Slip then punch = COUNTER", "Block late = PARRY", "Feint, then land: SET UP",
              "Step off his line: W + ARROW",
              "Hooks catch side-steps", "Uppercut splits the guard", "Feint him, then land big",
              "X pivots you off the ropes", "3 knockdowns = T.K.O.", "Mash A S D F to get up",
              "Power comes off the floor", "Feet set = the white pip", "Whiffing costs you balance",
              "Catch him coming back", "Off balance? Jab and reset", "Stand still to get set",
              "Mashing = arm punches", "Hooks cost the most balance", "A planted punch hurts more")


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
        # --- balance / weight transfer / exposure (see the notes by BAL_COST)
        self.bal = BAL_MAX             # 1 = weight square over your feet, 0 = falling over
        self.set_t = SET_TIME          # seconds planted: what you have to drive a punch with
        self.drive = 1.0               # how much weight went into the punch in flight
        self.expose = 0.0              # how far out of position your hands are
        self.rec_x = 1.0               # how much longer this punch's recovery is running
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
        self.ko_fall = "stiff"         # ...and, if he is out cold, WHICH way he goes down
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
        self.feinted_t = 0.0           # >0: a feint is still hanging in the air (see BAIT_WINDOW)
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
            sector = view_sector
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
        """Animation speed right now: hurt, gassed and off-balance fighters punch slower."""
        return (self.speed * (0.82 if self.hurt else 1.0) * (0.78 if self.gassed else 1.0)
                * (1.0 - BAL_SPEED + BAL_SPEED * self.bal))

    def set_x(self):
        """How much weight transfer you have available: SET_FLOOR with your feet still moving,
        1.0 once they have been planted for SET_TIME."""
        return SET_FLOOR + (1.0 - SET_FLOOR) * min(1.0, self.set_t / SET_TIME)

    def footing(self):
        """What a punch thrown right now would carry: your legs (balance) times your feet (set)."""
        return (1.0 - BAL_POWER + BAL_POWER * self.bal) * self.set_x()

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
        """Damage multiplier for the punch in flight: tired arms don't carry the same snap, and
        neither do arms swung with no weight behind them (self.drive, fixed when you threw it)."""
        return self.power * (1.0 - 0.3 * self.gas()) * self.drive

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
            # what you are driving this one with is decided NOW, by where your weight is. Chaining
            # straight off the last punch spends most of what you had left.
            self.drive = self.footing()
            self.set_t *= SET_KEEP
            self.rec_x = 1.0
        self.track_left = TRACK_MAX if name in PUNCHES or name in FEINTS else 0.0
        if self.game.mode != "bag":
            o = self.foe()
            # you throw it at where he is NOW (you were already facing him, near enough)
            self.track_left -= self.turn_to(self.angle_to(o), TRACK_SNAP, 1.0)
            self.track_left = max(0.0, self.track_left)
        if name in FEINTS:
            self.attack_id += 1        # it looks exactly like the real thing coming
            self.feinted_t = BAIT_WINDOW    # ...and for this long, the next one is a punch you set up
            self.game.snd("swish")
            if self.game.mode == "bag":
                self.game.bag_feint(self)
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

    def commit(self, outcome, ext=1.0):
        """The punch is spent. Pay for it: the balance it took off your feet, and how long it now
        takes to get your hand back and your weight over them. `outcome` is what stopped it -
        "land" (his head took the momentum), "block" (his gloves did) or "whiff" (nothing did) -
        and `ext` is how far you had reached when that happened."""
        name = self.action
        if name not in PUNCHES:
            return
        out = {"land": BAL_LAND, "block": BAL_BLOCK, "whiff": BAL_WHIFF}[outcome]
        cost = BAL_COST.get(name, 0.12) * (1.0 + BAL_REACH * clamp(ext, 0.0, 1.0)) * out
        cost *= 1.0 + 0.5 * self.gas()                 # nothing to hold you up on an empty tank
        self.bal = max(0.0, self.bal - cost)
        rec = {"land": REC_LAND, "block": REC_BLOCK, "whiff": REC_WHIFF}[outcome]
        rec *= 1.0 + REC_BAL * (1.0 - self.bal) + REC_GAS * self.gas()
        self.rec_x = min(REC_MAX, rec)
        if self.bal <= BAL_STUMBLE:
            self.stumble()

    def stumble(self):
        """Your feet have gone. Not a flag that fires on a missed hook - what happens when you have
        spent more balance than you had, whatever you spent it on."""
        over = clamp((BAL_STUMBLE - self.bal) / max(1e-6, BAL_STUMBLE), 0.0, 1.0)
        self.bal = BAL_STUMBLE + 0.08
        self.set_t = 0.0
        self.expose = max(self.expose, 0.8)
        self.stagger(STUMBLE_MIN + (STUMBLE_MAX - STUMBLE_MIN) * over)
        self.game.on_stumble(self)

    def get_hit(self, target, stun):
        self.finish_action()
        self.set_t = 0.0               # rocked: your feet are not under you any more
        self.block = None
        self.buffer = None
        self.stun_t = 0.0
        self.hitstun = stun
        pair = F_HIT_HEAD if target == "head" else F_HIT_BODY
        self.react = pair if random.random() < 0.6 else (pair[1], pair[0])
        self.react_t, self.react_total = 0.0, stun

    def stagger(self, dur):
        self.finish_action()
        self.set_t = 0.0
        self.block = None
        self.buffer = None
        self.hitstun = 0.0
        self.stun_t, self.stun_el = dur, 0.0

    def push(self, px):
        """Knocked straight back (away from where he faces), stopped by the ropes.
        Pressure fighters lean into punches and give up less ground."""
        if px > 0:
            px *= 1.0 - self.sturdy
            px *= 1.0 + (BAL_MOVED - 1.0) * (1.0 - self.bal)   # a man off balance gets moved
            self.bal = max(0.0, self.bal - BAL_PUSH * px)
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
            return self.limp_frame()             # drawn rotated, flat on his back
        if self.down:
            if self.rising_t >= 0:               # pushing up off the canvas
                r = self.rising_t
                if r < 0.18:
                    return F_DOWN[0]
                return F_RISE[0] if r < 0.40 else (F_RISE[1] if r < 0.64 else F_RISE[2])
            return self.fall_frame(self.down_t)
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
            return self.fall_frame(self.end_t)
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
            if self.action in PUNCHES:
                rate *= STAM_REGEN_PUNCH         # still throwing, or still getting the hand back
            elif self.block:
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

        # --- balance, weight transfer, exposure. Your feet come back under you when you give
        # them a beat to; your hands come back down as you reset from whatever you threw.
        if not (self.down or self.out_cold):
            # `rate` is balance back per second; `gain` is how fast your weight gets over your
            # feet in this state (0 = it doesn't, and whatever you had is gone), `cap` the most it
            # can reach without planting.
            cap = SET_TIME
            if self.clinch:
                rate, gain = BAL_REGEN * 1.4, 0.0            # leaning on him is a rest for the legs
            elif self.side_t > 0 or self.pivot_t > 0:
                rate, gain = BAL_REGEN_MOVE * 0.6, 0.0       # explosive: your weight is in the air
            elif self.action in PUNCHES:
                # going out, or coming back: either way your weight is not settled, though you do
                # start re-planting as you bring the hand back in.
                rate, gain = ((BAL_REGEN_REC, SET_REPLANT) if self.hit_done
                              else (BAL_REGEN_PUNCH, 0.0))
            elif self.moving:
                rate, gain = BAL_REGEN_MOVE, SET_WALK        # footwork builds some of it, to a point
                cap = SET_TIME * SET_WALK_CAP
            else:
                rate, gain = BAL_REGEN, 1.0
            self.bal = min(BAL_MAX, self.bal + rate * dt * (1.0 - BAL_GAS * self.gas()))
            if gain <= 0.0:
                self.set_t = 0.0
            elif self.set_t > cap:
                self.set_t = max(cap, self.set_t - dt * SET_SHED)  # walking the weight back off
            else:
                self.set_t = min(cap, self.set_t + dt * gain)
            if self.action in PUNCHES and not self.hit_done:
                self.expose = min(EXPOSE.get(self.action, 0.5),
                                  self.expose + EXPOSE_RISE * dt)
            else:
                self.expose = max(0.0, self.expose - EXPOSE_FALL * dt)

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
        # the back half of a punch runs long or short depending on what the front half ran into
        while self.action and self.t >= spec["ms"][self.idx] * (self.rec_x if self.hit_done else 1.0):
            self.t -= spec["ms"][self.idx] * (self.rec_x if self.hit_done else 1.0)
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
    def fall_dur(self):
        """How long this man's fall takes, start to canvas."""
        return KO_FALL_T / max(0.3, KO_SPEED.get(getattr(self, "ko_fall", "stiff"), 1.0))

    def fall_dir(self):
        """Which way he goes over: backwards, or forwards onto his face."""
        return KO_DIR.get(getattr(self, "ko_fall", "stiff"), 1)

    def fall_angle(self):
        """Out cold: how far over he has gone, read off this fall's timeline. A man dropped by one
        shot goes over fast and bounces; a man whose legs went just sinks and settles."""
        seq = self.ko_seq()
        end = seq[-1][2]
        t, dur = self.fall_t, self.fall_dur()
        if t >= dur:
            bounce = KO_BOUNCE.get(getattr(self, "ko_fall", "stiff"), 9.0)
            if t < dur + 0.2:
                return end - bounce * math.sin((t - dur) / 0.2 * math.pi)
            return end
        p = self.fall_p()
        for (p0, _, a0), (p1, _, a1) in zip(seq, seq[1:]):
            if p <= p1:
                k = 0.0 if p1 <= p0 else (p - p0) / (p1 - p0)
                return a0 + (a1 - a0) * k
        return end

    def lying(self):
        """(image, x, y) of the out-cold fighter, kept on screen and resting on the canvas."""
        ang = int(round(self.fall_angle() / 6)) * 6 * self.fall_dir()
        r = self.game.rotated(self.side_frames(), self.limp_frame(), ang * self.facing, self.facing)
        x = int(self.x) - r["px"]
        # Rest his BODY on the canvas, not his bounding box - but never let a trailing limb sink
        # more than a few pixels under the floor.
        y = min(self.gy() - r["py"], self.gy() + 1 - r.get("body", r["bottom"]),
                self.gy() + 4 - r["bottom"])
        x = int(clamp(x, 2 - r["left"], VW - 2 - r["right"]))
        return r["img"], x, y

    def fall_frame(self, t):
        """Going down: three stages of the fall, then lying on the canvas breathing."""
        if t < FALL_T[0]:
            return F_FALL[0]
        if t < FALL_T[1]:
            return F_FALL[1]
        if t < FALL_T[2]:
            return F_FALL[2]
        return F_DOWN[int((t - FALL_T[2]) / (BREATH * 0.5)) % 2]

    def ko_seq(self):
        return KO_SEQ.get(getattr(self, "ko_fall", "stiff"), KO_SEQ["stiff"])

    def fall_p(self):
        """How far through the fall he is, 0 standing to 1 on the canvas."""
        return clamp(getattr(self, "fall_t", 0.0) / self.fall_dur(), 0.0, 1.0)

    def limp_frame(self):
        """Out cold: which drawing of him belongs to this moment of the fall. He settles into the
        last one a breath after he lands and then does not move again."""
        if self.fall_t >= self.fall_dur() + KO_SETTLE_T:
            return KO_SETTLE.get(getattr(self, "ko_fall", "stiff"), F_LIMP[1])
        p, frame = self.fall_p(), self.ko_seq()[0][1]
        for p0, f0, _ in self.ko_seq():
            if p >= p0:
                frame = f0
        return frame

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
        self.plant_t = 0.0
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
        if self.me.bal < 0.45:                    # no legs under him: nothing he can lean on
            return random.choice([["jab"], ["jab"], ["body_jab"], ["jab", "jab"]])
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
        if (foe.expose > 0.5 and not self.plan and not me.action and me.bal > 0.5
                and dist <= R["cross"] and random.random() < L.get("punish", 0.4) * dt * 7.0):
            short = dist < R["hook"]             # his hand is still out there: go through the gap
            self.plan = [random.choice(["hook", "uppercut", "cross"] if short else ["cross", "jab"])]
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
        if (self.plan and me.can_start(self.plan[0]) and POWER.get(self.plan[0], 0.0) >= 2.0
                and me.set_t < SET_TIME * 0.95 and me.bal > 0.45
                and self.plant_t < (SET_TIME + 0.12) * L.get("plant", 0.6)):
            self.plant_t += dt                   # set his feet first: a power shot off the back foot
            self.move = self.zmove = 0           # is an arm punch, and he knows it. Stand still -
            return                               # set_t only grows while the feet are planted. How
                                                 # long he is prepared to wait is his skill: a club
                                                 # fighter hardly bothers, a champion always does.
        self.plant_t = 0.0
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
        self.read_locker()                        # the wallet and what he is wearing, before his sprites
        self._boxes = {}                          # where each garment sits in each drawing
        self.player_views = make_views(self.strips, self.look_map(), self.paint_designs)
        self.spar_views = make_views(self.strips, look_palette(**SPAR_LOOK))
        frames = self.player_views["side"][0]
        self.frames = frames
        self.player_sets = self.player_views["side"]
        self.spar_sets = self.spar_views["side"]
        self.spar_frames = self.spar_sets[1]
        self._fset, self._fviews, self._port = {}, {}, {}
        self._icons = {}
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
        self.shop_button = pygame.Rect(self.campaign_button.right + 3, self.button.y,
                                       self.font_s.size("SHOP")[0] + 8, 13)
        self.arena_bg = make_arena_background(self.button.x)
        self.hover = None
        self.info_icon = make_info_icon(INFO_D, (14, 12, 26, 120), (186, 194, 220, 175), (216, 222, 242, 195))
        self.info_icon_hi = make_info_icon(INFO_D_HOVER, (9, 7, 18, 220), (255, 232, 130, 255),
                                           (255, 244, 200, 255), ring_w=2)
        self.info_rect = pygame.Rect(0, 0, INFO_D_HOVER + 4, INFO_D_HOVER + 4)
        self.info_rect.center = INFO_CENTER
        self.info_open = False
        self.pause_open = False    # the P menu: where to next / leave this fight
        self.pause_i = 0
        self.pause_t = 0.0
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
        self.shop = None           # the pro shop, built the first time he walks into it
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

    @staticmethod
    def _body_bottom_impl(img, u):
        """The lowest row that is still HIM rather than a few stray pixels trailing off him: the
        row below which only 3% of his pixels lie. Resting a body on the floor by its bounding box
        means one dangling glove or a headband tail holds the whole man up in the air."""
        try:
            a = pygame.surfarray.array_alpha(img)
        except Exception:
            return u.bottom
        wide = (a > 0).sum(axis=0)
        total = int(wide.sum())
        if total <= 0:
            return u.bottom
        acc = 0
        for r in range(len(wide) - 1, -1, -1):
            acc += int(wide[r])
            if acc >= 0.03 * total:          # 3% of him may hang below: a glove, a headband tail
                return r + 1
        return u.bottom

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
                                  left=u.left, right=u.right, body=Game._body_bottom_impl(img, u))
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

    # ------------------------------------------------------------ the wallet and the wardrobe
    def read_locker(self):
        """Load the wallet and the kit. Anything unrecognised falls back to his own kit. A locker
        written before designs existed (v1) listed one key per slot; those keys are still colours,
        so an old locker opens with everything it had and plain designs."""
        d = load_locker() or {}
        try:
            self.money = max(0, int(d.get("money", 0)))
        except (TypeError, ValueError):
            self.money = 0
        owned = d.get("owned")
        self.owned = {k for k in owned if k in ITEMS} if isinstance(owned, list) else set()
        self.owned |= {it["key"] for it in KIT}   # his own kit is never taken off him
        self.worn = {slot: dict(kit) for slot, kit in DEFAULT_WORN.items()}
        worn = d.get("worn")
        if isinstance(worn, dict):
            for slot, chosen in worn.items():
                if slot not in WARDROBE_SLOTS:
                    continue
                if isinstance(chosen, str):       # an old locker: one key, and it was the colour
                    chosen = {"color": chosen}
                if not isinstance(chosen, dict):
                    continue
                for kind, key in chosen.items():
                    it = ITEMS.get(key)
                    if (kind in KINDS and it and it["slot"] == slot and it["kind"] == kind
                            and key in self.owned):
                        self.worn[slot][kind] = key

    def write_locker(self):
        return save_locker(dict(v=2, money=int(self.money), owned=sorted(self.owned),
                                worn={s: dict(k) for s, k in self.worn.items()}))

    def wallet_add(self, n):
        """Bank (or spend) money and put it beyond the reach of this career ending."""
        self.money = max(0, int(self.money + n))
        self.write_locker()

    # ------------------------------------------------------------ what he is wearing
    def worn_item(self, slot, kind="color"):
        """The thing he has on in one slot - its colour, or its design."""
        return ITEMS.get(self.worn.get(slot, {}).get(kind)) or ITEMS[DEFAULT_WORN[slot][kind]]

    def wearing(self, key):
        it = ITEMS.get(key)
        return bool(it) and self.worn.get(it["slot"], {}).get(it["kind"]) == key

    def inventory(self, slot=None, kind=None):
        """What he owns, in shop order. This is the inventory: everything bought is in here for
        good, and the wardrobe is just a way of looking at it."""
        return [it for it in KIT + STOCK if it["key"] in self.owned
                and (slot is None or it["slot"] == slot) and (kind is None or it["kind"] == kind)]

    def look_map(self):
        """The recolour map for the colours he is wearing - None while every slot is still his own,
        so the default sprite keeps the exact colours it was painted in."""
        look = {}
        for slot in WARDROBE_SLOTS:
            key = self.worn.get(slot, {}).get("color")
            if key and key != DEFAULT_WORN[slot]["color"] and key in ITEMS:
                look[slot] = ITEMS[key]["color"]
        return look_palette(**look) if look else None

    def design_plan(self):
        """[(slot, design), ...] for every slot with something other than plain on it."""
        out = []
        for slot in WARDROBE_SLOTS:
            it = self.worn_item(slot, "design")
            if it.get("bands"):
                out.append((slot, it))
        return out

    # ------------------------------------------------------------ painting the designs on
    def garment_boxes(self, view, slot):
        """Where one garment sits inside each of the 96 drawings of one view - worked out once
        from the colours the sprite was painted in, and then true for every recolour of it, since
        a recolour moves nothing."""
        key = (view, slot)
        if key not in self._boxes:
            strip = self.strips[view]
            cols = GARMENT_COLS[slot]
            boxes = []
            for i in range(strip.get_width() // FW):
                frame = strip.subsurface((i * FW, 0, FW, FH))
                rect = None
                for col in cols:
                    try:
                        m = pygame.mask.from_threshold(frame, col, (1, 1, 1, 255))
                    except (ValueError, pygame.error):
                        continue
                    if not m.count():
                        continue
                    rs = m.get_bounding_rects()
                    r = rs[0].unionall(rs[1:]) if len(rs) > 1 else rs[0]
                    rect = r if rect is None else rect.union(r)
                boxes.append(rect)
            self._boxes[key] = boxes
        return self._boxes[key]

    def paint_designs(self, view, strip):
        """Paint the trim onto a recoloured strip, in place. Each band is a slice of the garment's
        own box, so a stripe stays a stripe whichever way he is facing or lying."""
        plan = self.design_plan()
        if not plan:
            return strip
        look = self.look_map() or {}
        pa = pygame.PixelArray(strip)
        try:
            for slot, design in plan:
                into = trim_shades(self.worn_item(slot, "color")["color"], design["color"])
                # what each of this garment's colours looks like NOW, and what it becomes
                pairs = [(look.get(SRC[k], SRC[k]), into[w]) for k, w in GARMENT_PARTS[slot]]
                for i, box in enumerate(self.garment_boxes(view, slot)):
                    if box is None:
                        continue
                    for bx, by, bw, bh in design["bands"]:
                        x0 = i * FW + box.x + int(round(box.w * bx))
                        y0 = box.y + int(round(box.h * by))
                        x1 = min(i * FW + box.right, x0 + max(1, int(round(box.w * bw))))
                        y1 = min(box.bottom, y0 + max(1, int(round(box.h * bh))))
                        if x1 <= x0 or y1 <= y0:
                            continue
                        patch = pa[x0:x1, y0:y1]
                        for src_c, dst_c in pairs:
                            patch.replace(src_c, dst_c)
        finally:
            pa.close()
        return strip

    def apply_look(self):
        """Repaint his sprites in the kit he is wearing - colours first, then the designs on top."""
        self.player_views = make_views(self.strips, self.look_map(), self.paint_designs)
        self.player_sets = self.player_views["side"]
        self.frames = self.player_sets[0]
        self._tops.clear()                        # these are keyed by sprite-set identity
        self._rot.clear()
        self._port.pop("you", None)
        self.player.set_views(self.player_views)

    def wear_item(self, key):
        """Put on something he owns. False if he does not own it, or has it on already."""
        it = ITEMS.get(key)
        if not it or key not in self.owned or self.wearing(key):
            return False
        self.worn[it["slot"]][it["kind"]] = key
        self.apply_look()
        self.write_locker()
        return True

    def buy_item(self, key):
        """Buy it. It goes into the inventory for good, and he walks out wearing it."""
        it = ITEMS.get(key)
        if not it or key in self.owned or self.money < it["price"]:
            return False
        self.money -= it["price"]
        self.owned.add(key)
        self.worn[it["slot"]][it["kind"]] = key
        self.apply_look()
        self.write_locker()
        return True

    # ------------------------------------------------------------ the pro shop
    def enter_shop(self):
        """Walk into the shop, at the door, facing up the room."""
        if self.shop is None:
            stands, signs, room_w = shop_layout()
            self.shop = dict(stands=stands, signs=signs, w=room_w,
                             room=make_shop_room(stands, signs, room_w))
        sh = self.shop
        sh.update(x=34.0, fy=float(SHOP_FRONT - 4), ang=0.0, view="fq", step=0.0, moving=False,
                  cam=0.0, near=None, confirm=None, confirm_t=0.0,
                  flash="", flash_t=0.0, flash_col=(255, 255, 255), wardrobe=False, w_row=0, w_item=0)
        sh["cam"] = clamp(sh["x"] - VW / 2, 0, sh["w"] - VW)
        self.mode = "shop"
        self.phase, self.phase_t = "shop", 0.0
        self.pause_open = False
        self.clear_fx()
        self.snd("blip")

    def leave_shop(self):
        self.reset_bag()

    def shop_flash(self, msg, col):
        self.shop["flash"], self.shop["flash_t"], self.shop["flash_col"] = msg, SHOP_FLASH_T, col

    def shop_row_at(self):
        """Which row he is looking at: up at the pegboard, or a pace back at the shelf."""
        return "wall" if self.shop["fy"] <= SHOP_BACK + SHOP_ROW_Y else "shelf"

    def shop_stand_at(self):
        """The thing he is standing at, or None. You have to be up at the racks, not out on the
        shop floor, and which of the two rows you get depends on where you are standing."""
        sh = self.shop
        if sh["fy"] > SHOP_BACK + SHOP_NEAR_Y:
            return None
        row = self.shop_row_at()
        best = None
        for st in sh["stands"]:
            if st["row"] != row and st["kind"] != "mirror":
                continue
            d = abs(st["x"] - sh["x"])
            if d <= SHOP_NEAR_X and (best is None or d < best[0]):
                best = (d, st)
        return best[1] if best else None

    def shop_cancel(self, spoken=True):
        """Back out of a confirm."""
        sh = self.shop
        if not sh["confirm"]:
            return False
        sh["confirm"], sh["confirm_t"] = None, 0.0
        if spoken:
            self.shop_flash("CANCELLED", (220, 200, 210))
            self.snd("block")
        return True

    def shop_buy_key(self):
        """A, at whatever he is standing at: buy it, confirm the buy, or put it on."""
        sh = self.shop
        st = sh["near"]
        if st is None:
            return
        if st["kind"] == "mirror":
            self.shop_wardrobe(True)
            return
        key = st["key"]
        it = ITEMS[key]
        if key in self.owned:
            if self.wearing(key):
                self.shop_flash("ALREADY WEARING THEM", (210, 206, 220))
                self.snd("blip")
            else:
                self.wear_item(key)
                self.shop_flash("NOW WEARING  " + it["name"], (130, 232, 170))
                self.snd("swish")
            return
        if self.money < it["price"]:
            self.shop_flash("YOU'RE $%s SHORT" % "{:,}".format(it["price"] - self.money), (255, 112, 112))
            self.snd("block")
            return
        if sh["confirm"] == key:
            self.buy_item(key)
            self.shop_flash("BOUGHT  " + it["name"], (255, 216, 124))
            self.snd("bell")
            sh["confirm"], sh["confirm_t"] = None, 0.0
            self.firework(st["x"] - sh["cam"], SHOP_PEG_Y + 4)
        else:
            sh["confirm"], sh["confirm_t"] = key, SHOP_CONFIRM_T
            self.snd("blip")

    def update_shop(self, dt, left, right, far, near):
        sh = self.shop
        sh["flash_t"] = max(0.0, sh["flash_t"] - dt)
        if sh["wardrobe"]:                             # the mirror is modal: he stands still
            sh["moving"] = False
            return
        mx = (1 if right else 0) - (1 if left else 0)
        my = (1 if near else 0) - (1 if far else 0)    # down the shop is toward the camera
        sh["moving"] = bool(mx or my)
        if sh["moving"]:
            l = math.hypot(mx, my)
            sh["x"] = clamp(sh["x"] + mx / l * SHOP_WALK * dt, 26.0, sh["w"] - 26.0)
            sh["fy"] = clamp(sh["fy"] + my / l * SHOP_WALK_Z * dt, float(SHOP_BACK), float(SHOP_FRONT))
            sh["ang"] = math.atan2(my, mx)
            sh["step"] += dt * 9.5
        want = clamp(sh["x"] - VW / 2, 0, max(0, sh["w"] - VW))
        sh["cam"] += (want - sh["cam"]) * min(1.0, dt * 7.0)
        was = sh["near"]
        sh["near"] = self.shop_stand_at()
        if sh["near"] is not was:
            self.shop_cancel(False)                    # walking away from a till is a no
            if sh["near"] is not None:
                self.snd("blip")
        if sh["confirm"]:
            sh["confirm_t"] -= dt
            if sh["confirm_t"] <= 0:
                self.shop_cancel(False)

    # ------------------------------------------------------------ the shop, drawn
    def shop_item_icon(self, key):
        """The little drawing of one item, made once."""
        cache = self._icons
        if key not in cache:
            it = ITEMS[key]
            cache[key] = (make_item_icon(it), make_item_icon(it, None, 2))
        return cache[key]

    def shop_frames(self):
        """The drawing of him for the way he is walking, with his back to you going up the shop."""
        sh = self.shop
        deg = math.degrees(sh["ang"])
        key = view_sector(deg) if sh["moving"] else sh["view"]
        sh["view"] = key
        v = self.player_views.get(key) or self.player_views["side"]
        if isinstance(v, tuple):
            return v[0] if math.cos(sh["ang"]) >= 0 else v[1]
        return v

    def shop_frame_i(self):
        sh = self.shop
        if sh["moving"]:
            return WALK_BASE + int(sh["step"]) % WALK_FRAMES
        return IDLE_SEQ[int(self.clock * 1000 / IDLE_MS) % len(IDLE_SEQ)]

    def draw_shop_man(self, c, cam):
        """Him, on the shop floor - and his reflection if he is standing at the mirror."""
        sh = self.shop
        frames = self.shop_frames()
        i = self.shop_frame_i()
        feet = getattr(frames, "feet", SPRITE_FEET)
        x = int(sh["x"] - cam) - FW // 2
        y = int(sh["fy"]) - feet
        st = sh["near"]
        if st is not None and st["kind"] == "mirror":
            g = mirror_glass(st["x"]).move(-cam, 0)
            clip = c.get_clip()
            c.set_clip(g)
            refl = self.player_views["f"]
            ri = self.shop_frame_i()
            c.blit(refl[ri], (g.centerx - FW // 2, g.bottom - 4 - getattr(refl, "feet", SPRITE_FEET)))
            tint = pygame.Surface((g.w, g.h), pygame.SRCALPHA)
            tint.fill((70, 86, 120, 70))
            c.blit(tint, g.topleft)
            c.set_clip(clip)
        shadow = pygame.transform.scale(self.shadow, (40, 7))
        c.blit(shadow, (int(sh["x"] - cam) - 20, int(sh["fy"]) - 3))
        c.blit(frames[i], (x, y))

    def draw_shop_pegs(self, c, cam):
        """Everything on sale: the colours on their pegs, the designs on the shelf underneath,
        each with its price, and a marker over whichever one he is standing at."""
        sh = self.shop
        active = sh["near"]
        for st in sh["stands"]:
            sx = int(st["x"] - cam)
            if sx < -24 or sx > VW + 24:
                continue
            on = st is active
            if st["kind"] == "mirror":
                if on:
                    self.draw_shop_marker(c, sx, mirror_glass(st["x"]).y - 10)
                continue
            it = ITEMS[st["key"]]
            wall = st["row"] == "wall"
            iy = SHOP_PEG_Y if wall else SHOP_SHELF_ICON
            ty = SHOP_PEG_TAG if wall else SHOP_SHELF_TAG
            owned = st["key"] in self.owned
            worn = self.wearing(st["key"])
            if wall:
                c.fill((52, 42, 66), (sx - 1, iy - 4, 2, 4))               # the peg it hangs from
            if on:
                glow = pygame.Surface((26, 22), pygame.SRCALPHA)
                glow.fill((255, 228, 140, 46))
                c.blit(glow, (sx - 13, iy - 2))
            c.blit(self.shop_item_icon(st["key"])[0], (sx - 9, iy))
            tag = "WORN" if worn else ("OWNED" if owned else "$" + "{:,}".format(it["price"]))
            col = (140, 240, 180) if worn else ((190, 230, 255) if owned else
                                                ((255, 226, 130) if self.money >= it["price"] else (230, 120, 120)))
            w = self.font_s.size(tag)[0] + 5
            pygame.draw.rect(c, (24, 18, 32), (sx - w // 2, ty, w, 10))
            draw_text(c, self.font_s, tag, sx, ty + 1, col, center=True)
            if on:
                self.draw_shop_marker(c, sx, iy - (12 if wall else 10))

    def draw_shop_marker(self, c, x, y):
        y += int(math.sin(self.clock * 6.0) * 1.6)
        pygame.draw.polygon(c, (20, 14, 28), [(x - 5, y - 1), (x + 5, y - 1), (x, y + 6)])
        pygame.draw.polygon(c, (255, 228, 130), [(x - 4, y), (x + 4, y), (x, y + 4)])

    def shop_counter(self, st):
        """What the bar along the bottom says: (icon, name, price, [(words, colour), ...]).
        It lives down there on purpose - the goods are on the wall, and a panel in front of them
        would hide the one thing you are trying to look at."""
        sh = self.shop
        if sh["wardrobe"]:                        # the mirror borrows the bar for its own keys
            if sh["flash_t"] > 0:
                return None, "WARDROBE", None, [(sh["flash"], sh["flash_col"])]
            return None, "WARDROBE", None, [("UP/DOWN  KIT", (206, 200, 218)),
                                            ("LEFT/RIGHT  PICK", (206, 200, 218)),
                                            ("A  WEAR IT", (255, 230, 140))]
        if st is None:
            row = "AT THE SHELF - DESIGNS" if self.shop_row_at() == "shelf" else "AT THE PEGS - COLOURS"
            return None, SHOP_SIGN, None, [("LEFT/RIGHT  WALK", (206, 200, 218)),
                                           ("UP/DOWN  " + row, (255, 230, 140))]
        if st["kind"] == "mirror":
            return None, "THE MIRROR", None, [("everything he owns", (206, 200, 216)),
                                              ("PRESS A TO CHANGE", (255, 230, 140))]
        it = ITEMS[st["key"]]
        icon, price = self.shop_item_icon(st["key"])[1], it["price"]
        name = "%s %s" % (SLOT_SHORT[it["slot"]], it["name"]) if it["kind"] == "design" else it["name"]
        if self.wearing(st["key"]):
            lines = [("YOURS - AND ON HIM", (150, 240, 185))]
        elif st["key"] in self.owned:
            lines = [("YOURS ALREADY", (190, 230, 255)), ("PRESS A TO PUT THEM ON", (255, 230, 140))]
        elif sh["confirm"] == st["key"]:
            lines = [("A AGAIN CONFIRMS", (255, 236, 150)), ("ANYTHING ELSE CANCELS", (240, 160, 160))]
        elif self.money < price:
            lines = [("$%s SHORT" % "{:,}".format(price - self.money), (255, 120, 120)),
                     ("COME BACK WITH A PURSE", (214, 196, 206))]
        else:
            lines = [(KIND_NAME[it["kind"]], (206, 200, 216)), ("PRESS A TO BUY", (255, 230, 140))]
        return icon, name, price, lines

    def draw_shop_counter(self, c, st):
        """The bar along the bottom: what he is standing at, and what A will do about it."""
        icon, name, price, lines = self.shop_counter(st)
        x, y, w, h = 30, VH - 34, VW - 34, 30        # clear of the little "i" in the corner
        box = pygame.Surface((w, h), pygame.SRCALPHA)
        box.fill((12, 9, 22, 232))
        c.blit(box, (x, y))
        gold = self.shop["confirm"] is not None
        pygame.draw.rect(c, (255, 228, 140) if gold else (104, 92, 124), (x, y, w, h), 1)
        tx = x + 8
        if icon:
            c.blit(icon, (x + 3, y - 2))
            tx = x + 38
        draw_text(c, self.font_m, name, tx, y + 3, (255, 255, 255))
        if price is not None:
            draw_text(c, self.font_m, "$" + "{:,}".format(price), tx + self.font_m.size(name)[0] + 10, y + 3,
                      (255, 226, 130))
        draw_text(c, self.font_s, "P  DONE" if self.shop["wardrobe"] else "P  MENU", x + w - 7, y + 5,
                  (176, 170, 196), right=True)
        lx = tx
        for k, (t, col) in enumerate(lines):
            if k:
                draw_text(c, self.font_s, "-", lx + 3, y + 17, (120, 110, 140))
                lx += 11
            draw_text(c, self.font_s, t, lx, y + 17, col)
            lx += self.font_s.size(t)[0]

    def draw_shop_money(self, c):
        """What he has on him, in the corner, the whole time he is in here."""
        st = self.shop["near"]
        short = (st is not None and st["kind"] == "item" and st["key"] not in self.owned
                 and self.money < ITEMS[st["key"]]["price"])
        txt = "$" + "{:,}".format(self.money)
        w = self.font_m.size(txt)[0] + 26
        pygame.draw.rect(c, (12, 9, 22), (VW - w - 4, 4, w, 16))
        pygame.draw.rect(c, (230, 120, 120) if short else (110, 98, 130), (VW - w - 4, 4, w, 16), 1)
        pygame.draw.circle(c, (198, 158, 56), (VW - w + 4, 12), 5)
        pygame.draw.circle(c, (255, 222, 120), (VW - w + 4, 12), 4)
        pygame.draw.circle(c, (198, 158, 56), (VW - w + 4, 12), 2)
        draw_text(c, self.font_m, txt, VW - 8, 5, (255, 120, 120) if short else (255, 236, 160), right=True)

    def draw_shop(self, c):
        sh = self.shop
        cam = int(round(sh["cam"]))
        c.blit(sh["room"], (-cam, 0))
        self.draw_shop_pegs(c, cam)
        self.draw_shop_man(c, cam)
        for s_ in self.stars:
            self.draw_star(c, s_)
        for x, y, _, _, life, col in self.parts:
            c.fill(col, (int(x), int(y), 2 if life > 0.2 else 1, 2 if life > 0.2 else 1))
        if sh["flash_t"] > 0 and not sh["wardrobe"]:
            k = min(1.0, sh["flash_t"] / 0.3)
            w = self.font_m.size(sh["flash"])[0] + 16
            box = pygame.Surface((w, 17), pygame.SRCALPHA)
            box.fill((12, 9, 22, int(230 * k)))
            c.blit(box, (VW // 2 - w // 2, VH - 54))
            draw_text(c, self.font_m, sh["flash"], VW // 2, VH - 51, sh["flash_col"], center=True)
        self.draw_wardrobe(c)
        self.draw_shop_counter(c, sh["near"])
        self.draw_shop_money(c)

    # ------------------------------------------------------------ the mirror
    def wardrobe_rows(self):
        """The eight lines of his kit: a colour and a design for each of the four garments."""
        return [(slot, kind) for slot in WARDROBE_SLOTS for kind in KINDS]

    def wardrobe_items(self, row=None):
        """What he owns for one line of the wardrobe, what he came in with first."""
        slot, kind = self.wardrobe_rows()[self.shop["w_row"] if row is None else row]
        return self.inventory(slot, kind)

    def shop_wardrobe(self, open_it):
        self.shop["wardrobe"] = bool(open_it)
        if open_it:
            self.shop["w_row"] = 0
            self.wardrobe_sync()
        self.snd("blip")

    def wardrobe_sync(self):
        """Put the cursor on what he actually has on."""
        sh = self.shop
        slot, kind = self.wardrobe_rows()[sh["w_row"]]
        worn = self.worn.get(slot, {}).get(kind)
        items = self.wardrobe_items()
        sh["w_item"] = next((i for i, it in enumerate(items) if it["key"] == worn), 0)

    def wardrobe_move(self, d, rows=False):
        sh = self.shop
        if rows:
            sh["w_row"] = (sh["w_row"] + d) % len(self.wardrobe_rows())
            self.wardrobe_sync()
            self.snd("blip")
            return
        items = self.wardrobe_items()
        if len(items) > 1:
            sh["w_item"] = (sh["w_item"] + d) % len(items)
            self.snd("blip")

    def wardrobe_wear(self):
        items = self.wardrobe_items()
        if not items:
            return
        it = items[min(self.shop["w_item"], len(items) - 1)]
        if self.wear_item(it["key"]):
            self.shop_flash("NOW WEARING  " + it["name"], (130, 232, 170))
            self.snd("swish")
        else:
            self.shop_flash("ALREADY ON HIM", (210, 206, 220))
            self.snd("blip")

    def draw_wardrobe(self, c):
        """His inventory: eight lines of kit down the left, everything he owns for the chosen one
        down the right, and him in the glass behind it wearing whatever he picks."""
        sh = self.shop
        if not sh or not sh.get("wardrobe"):
            return
        r = pygame.Rect(8, 10, 224, 132)
        box = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        box.fill((12, 9, 22, 240))
        c.blit(box, r.topleft)
        pygame.draw.rect(c, (124, 112, 146), r, 1)
        draw_text(c, self.font_m, "WARDROBE", r.x + 8, r.y + 3, (255, 236, 160))
        bought = len([k for k in self.owned if ITEMS[k]["stock"]])
        draw_text(c, self.font_s, "%d bought  -  %d to find" % (bought, len(STOCK) - bought),
                  r.right - 7, r.y + 7, (184, 178, 200), right=True)
        c.fill((70, 60, 92), (r.x + 6, r.y + 21, r.w - 12, 1))
        rows = self.wardrobe_rows()
        for i, (slot, kind) in enumerate(rows):
            y = r.y + 26 + i * 13
            on = i == sh["w_row"]
            if on:
                c.fill((48, 40, 68), (r.x + 5, y - 2, 94, 13))
                c.fill((255, 228, 140), (r.x + 5, y - 2, 2, 13))
            if kind == KINDS[0]:
                draw_text(c, self.font_s, SLOT_SHORT[slot], r.x + 11, y, (226, 222, 238))
            draw_text(c, self.font_s, KIND_NAME[kind], r.x + 56, y,
                      (255, 230, 140) if on else (168, 162, 186))
            c.blit(self.shop_item_icon(self.worn_item(slot, kind)["key"])[0], (r.x + 100, y - 4))
        x0 = r.x + 122
        c.fill((28, 22, 42), (x0, r.y + 24, r.w - 130, 13 * 5 + 4))
        items = self.wardrobe_items()
        sel = min(sh["w_item"], len(items) - 1) if items else 0
        for k, it in enumerate(items[:5]):
            y = r.y + 28 + k * 13
            on = k == sel
            if on:
                c.fill((60, 50, 82), (x0 + 2, y - 2, r.w - 134, 13))
            c.blit(self.shop_item_icon(it["key"])[0], (x0 + 4, y - 4))
            draw_text(c, self.font_s, it["name"], x0 + 24, y, (255, 255, 255) if on else (196, 190, 210))
            if self.wearing(it["key"]):
                draw_text(c, self.font_s, "ON", r.right - 9, y, (140, 240, 180), right=True)


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
        self.wallet_add(self.last_purse)          # straight into the wallet, and onto disk
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
        if self.pause_open:                       # the menu is modal: use the keyboard
            return
        if self.mode == "shop":                   # the shop is walked round, not clicked on, and
            self.hover = None                     # the gym's buttons are not even drawn in here
            if self.info_rect.collidepoint(x, y):
                self.hover = "info"
                if click:
                    self.toggle_info()
            elif click and self.info_open:
                self.toggle_info()
            return
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
        elif self.mode == "bag" and self.shop_button.collidepoint(x, y):
            self.hover = "shop"
        if not click:
            return
        if self.hover == "info":
            self.toggle_info()
        elif self.hover == "main":
            self.toggle_mode()
        elif self.hover == "campaign":
            self.start_campaign()
        elif self.hover == "shop":
            self.enter_shop()

    def pause_rows(self):
        """(label, what it does, action). What leaving means depends on where you are."""
        if self.mode == "shop":
            return [("BACK TO SHOPPING", "there is more on the walls", "close"),
                    ("LEAVE THE SHOP", "back to the gym", "quit")]
        if self.mode == "bag":
            return [("SPARRING", "three rounds, a new style every time", "spar"),
                    ("CAMPAIGN", "your career: pick your fights, climb to the title", "campaign"),
                    ("THE PRO SHOP", "spend what you have won on new kit", "shop"),
                    ("BACK TO THE BAG", "carry on working the heavy bag", "close")]
        if self.mode == "campaign":
            return [("RESUME", "back to it", "close"),
                    ("SAVE AND QUIT TO THE GYM", "your career is kept where it stands", "savequit")]
        return [("RESUME", "back to it", "close"),
                ("QUIT TO THE GYM", "end this sparring session", "quit")]

    def toggle_pause(self):
        self.pause_open = not self.pause_open
        self.pause_i = 0
        if self.pause_open:                       # drop your hands, nothing is buffered through it
            self.player.want_block = self.cpu.want_block = None
            self.player.buffer = self.cpu.buffer = None
        self.snd("blip")

    def pause_move(self, d):
        self.pause_i = (self.pause_i + d) % len(self.pause_rows())
        self.snd("blip")

    def pause_pick(self):
        act = self.pause_rows()[self.pause_i][2]
        self.pause_open = False
        self.snd("blip")
        if act == "spar":
            self.start_spar()
        elif act == "campaign":
            self.start_campaign()
        elif act == "shop":
            self.enter_shop()
        elif act == "savequit":
            self.save_and_quit()
        elif act == "quit":
            self.reset_bag()

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

    def bag_feint(self, f):
        """A feint on the heavy bag. There is nothing in front of him to flinch, so the move has
        to announce itself - and it leaves the set-up window open behind it."""
        hx, hy = f.head_pos()
        self.say("FEINT", hx + 4, hy - 20, (150, 195, 255), self.font_s, vy=-16, life=0.45)

    def on_miss(self, f, frame):
        """Swung through thin air. Nothing took your weight, so you pay the full balance cost of
        however far you reached - which is why a missed hook will put you on your heels and a
        missed jab will not, without either being a special case."""
        f.spend(STAM_MISS * (3.0 if f.action in BIG_SHOTS else 1.0))
        wx, wy = f.tip(frame)
        if self.mode != "bag":
            f.commit("whiff", 1.0)
        o = f.foe() if self.mode != "bag" else None
        if f.stun_t > 0:                             # the cost was more than he had: his feet went
            self.say("OFF BALANCE", wx - 26, wy - 18, (255, 170, 120), self.font_s, vy=-14, life=0.6)
        else:
            off = o is not None and self.off_line(f, o) > LAT_HIT
            lab = "off line" if off else ("miss" if f.bal > 0.45 else "no legs in it")
            self.say(lab, wx - 12, wy - 8, (150, 156, 182), self.font_s, vy=-14, life=0.6)
        if f is self.player and self.mode != "bag":
            self.ai.punish = True

    def on_stumble(self, f):
        """His feet have gone from under him. Worth seeing and worth hearing."""
        if self.mode == "bag":
            return
        self.snd("swish")
        self.shake, self.shake_t = 2, 0.12
        if f is self.player:
            self.ai.punish = True

    # ------------------------------------------------------------ update
    def update(self, dt, left=False, right=False, down=False, block=False, far=False, near=False):
        if self.saved_t:
            self.saved_t = max(0.0, self.saved_t - dt) if self.saved_t > 0 else min(0.0, self.saved_t + dt)
        self.info_t = clamp(self.info_t + (dt * 6.5 if self.info_open else -dt * 7.5), 0.0, 1.0)
        if self.info_open:                        # reading the controls pauses the fight
            self.clock += dt
            return
        self.pause_t = clamp(self.pause_t + (dt * 7.0 if self.pause_open else -dt * 8.0), 0.0, 1.0)
        if self.pause_open:                       # ...and so does the menu
            self.clock += dt
            return
        if self.slowmo > 0:                       # slow motion on the big moments
            self.slowmo -= dt
            dt *= 0.35
        self.clock += dt
        self.update_audio(dt)
        self.update_fx(dt)
        if self.mode == "shop":                   # the shop is its own little world
            self.update_shop(dt, left, right, far, near)
            return
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
                if t is not None and t.fall_t >= t.fall_dur():
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
        # how far into the punch it landed: 1 = at the end of his reach (flush), 0 = smothered
        ext = clamp((dist - MIN_SEP) / max(1.0, self.ranges[att.action] - MIN_SEP), 0.0, 1.0)
        blocked = d.block is not None and ((d.block == "high") == (target == "head")) and not caught
        if blocked:
            self.blocked(att, d, spec, hx, hy, ext)
        else:
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

    def blocked(self, att, d, spec, hx, hy, ext=0.8):
        if d.parry_ready and d.block_t <= PARRY_WINDOW:
            d.parry_ready = False
            att.bal = max(0.0, att.bal - BAL_PARRY)   # turned aside: your weight goes with it
            att.stagger(PARRY_STUN)
            if att.bal <= BAL_STUMBLE:                # turned aside hard enough to take his feet
                att.stumble()                         # (never shorter than the parry stun itself)
                att.stun_t = max(att.stun_t, PARRY_STUN)
            d.counter_t = COUNTER_WINDOW
            self.stars.append(dict(x=hx, y=hy, t=0.0, life=0.28, big=True, kind="parry"))
            self.say("PARRY!", hx - 20, hy - 26, (130, 240, 255), self.font_l, vy=-20, life=0.9)
            self.hitstop = 0.09
            self.snd("parry")
            self.excite(0.12)
            return
        att.commit("block", ext)                   # his gloves took it: you are half-way set again
        d.unanswered = max(0, d.unanswered - 1)    # covering up shows the referee he's still in it
        d.spend(STAM_BLOCK)
        split = spec.get("splits") and d.block == "high"
        d.guard -= (spec["guard"] * (1 + FLURRY_RAMP * d.block_chain) * (1 + 0.6 * d.gas())
                    * (1.8 if split else 1.0) * (1 + EXPOSE_GUARD * d.expose))
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
        k *= 1.0 + EXPOSE_IMPACT * d.expose       # his hands were out: nothing in the way of it
        k *= 1.0 + BAL_ROLL * (1.0 - d.bal)       # and his feet were gone: he cannot roll with it
        if counter_hit:
            k *= 1.18                             # caught him mid-punch: he never saw it coming
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
        att.commit("land", ext)                   # his head took your weight: you stay squarer
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
        if not glancing:                          # rocked back on his heels: whatever he throws
            cost = (BAL_HIT_MOVE if walking_in else BAL_HIT) * POWER[name] / 2.0    # next has no
            d.bal = max(0.0, d.bal - cost)                                          # weight in it
            d.set_t = 0.0
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

    def ko_fall_style(self, d, att):
        """What just happened to him, in one word. The punch comes first: a hook turns a man
        whatever shape he was in, and downstairs is downstairs however worn down he already was.
        Only a straight shot asks how much he had already taken."""
        name = (getattr(att, "action", None) or "").replace("feint_", "")
        if d.liver_t > 0:
            return "body"
        if name in KO_PUNCH:
            return KO_PUNCH[name]
        if d.hurt or d.downs > 0 or d.unanswered >= COMBO_KO:
            return "crumple"
        return "stiff"

    def knock_out_cold(self, d, att):
        d.ko_fall = self.ko_fall_style(d, att)
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
        set_up = p.feinted_t > 0                  # it followed a feint, and followed it quickly
        p.feinted_t = 0.0                         # one punch per feint, not a whole flurry
        self.combo += 1
        self.combo_t = 1.4
        self.best = max(self.best, self.combo)
        mult = (COUNTER_MULT if counter else 1.0) * (SET_UP_MULT if set_up else 1.0)
        dmg = int(spec["dmg"] * mult * (1 + 0.08 * min(self.combo - 1, 10)))
        self.damage += dmg

        self.bag.kick(spec["kick"] * (1.35 if counter else 1.0) * (1.2 if set_up else 1.0))
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
        elif set_up:
            self.say("SET UP!", px - 16, py - 28, (160, 255, 190), self.font_m, vy=-18, life=0.9)
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
        if self.mode == "shop":
            self.draw_shop(c)
            self.draw_info(c)
            self.draw_pause(c)
            out.fill((20, 16, 28))
            out.blit(c, (0, 0))
            return
        if self.mode == "campaign" and self.phase in self.STORY_PHASES:
            self.draw_story(c)
            self.draw_info(c)
            self.draw_pause(c)
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
        self.draw_pause(c)

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
        draw_text(c, self.font_s, "UP / DOWN  CHOOSE        ENTER  START        P  MENU",
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
        draw_text(c, self.font_s, "%s   %s   MONEY $%s" % (self.record(), rank, "{:,}".format(self.money)),
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
            button(self.shop_button, "SHOP", self.hover == "shop",
                   (54, 142, 112), (82, 196, 152), (164, 246, 206), (24, 84, 64), (20, 70, 54))

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
        draw_text(s, self.font_s, "P  MENU        BKSP  RESET",
                  w // 2, h - 22, label, center=True)
        draw_text(s, self.font_s, "ENTER CONTINUE   S SAVE CAREER   M MUTE   ESC CLOSE",
                  w // 2, h - 12, label, center=True)
        self._panel[mode] = s
        return s

    def draw_pause(self, c):
        t = self.pause_t
        if t <= 0.01:
            return
        dim = pygame.Surface((VW, VH), pygame.SRCALPHA)
        dim.fill((8, 6, 20, int(175 * t)))
        c.blit(dim, (0, 0))
        rows = self.pause_rows()
        h = 24 + len(rows) * 30
        top = int((VH - h) // 2 + (1.0 - t) * 10)
        x, w = 30, VW - 60
        panel = pygame.Rect(x, top, w, h)
        pygame.draw.rect(c, (16, 11, 26), panel.inflate(4, 4))
        pygame.draw.rect(c, (36, 30, 52), panel)
        pygame.draw.rect(c, (96, 84, 128), panel, 1)
        draw_text(c, self.font_m, "THE GYM" if self.mode == "bag" else
                  ("THE PRO SHOP" if self.mode == "shop" else "PAUSED"),
                  VW // 2, top + 5, (255, 214, 90), center=True)
        for i, (name, sub, _) in enumerate(rows):
            r = pygame.Rect(x + 5, top + 20 + i * 30, w - 10, 27)
            on = i == self.pause_i
            c.fill((74, 58, 116) if on else (46, 40, 64), r)
            c.fill((132, 110, 196) if on else (60, 52, 82), (r.x, r.y, r.w, 1))
            draw_text(c, self.font_s, name, r.x + 14, r.y + 4,
                      (255, 255, 255) if on else (206, 202, 230))
            draw_text(c, self.font_s, sub, r.x + 14, r.y + 15,
                      (196, 204, 240) if on else (138, 144, 178))
            if on:
                draw_text(c, self.font_s, ">", r.x + 5, r.y + 9, (255, 214, 90))
        draw_text(c, self.font_s, "UP / DOWN    ENTER    P CLOSES", VW // 2, top + h + 4,
                  (150, 156, 182), center=True)

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
        if not self.info_seen and t <= 0 and self.clock < 30 and self.mode != "shop":
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
        money = "$" + "{:,}".format(self.money)               # what the SHOP button is for
        draw_text(c, self.font_m, money, VW - 8, VH - 15, gold, right=True)
        draw_text(c, self.font_s, "MONEY", VW - 12 - self.font_m.size(money)[0], VH - 13, label, right=True)
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
        by = sy + 4                                      # balance: how far your weight is off centre
        pygame.draw.rect(c, (20, 14, 30), (x - 1, by - 1, w + 2, 4))
        c.fill((38, 34, 52), (x, by, w, 2))
        if f.bal <= BAL_STUMBLE * 2.2:                   # violet, so it is never mistaken for the
            bcol = (255, 120, 200) if int(self.clock * 7) % 2 else (160, 60, 130)   # blue guard bar
        elif f.bal < 0.45:
            bcol = (234, 150, 232)
        else:
            bcol = (176, 150, 255)
        seg(0, f.bal, bcol, by, 2)
        seg(0, f.bal, tuple(min(255, v + 46) for v in bcol), by, 1)
        if f.set_t >= SET_TIME and not f.action:         # feet planted: a punch now carries. In the
            px = x + (w - 5 if mirror else 0)            # clear gap below the bar, not on the wind
            c.fill((255, 255, 255), (px, by + 3, 5, 2))

    def spar_label(self):
        """Who you are sparring, in the longest form that still clears the gym sign."""
        st = STYLES[self.spar_style]
        short = STYLE_SHORT.get(self.spar_style, st["name"])
        budget = VW - 8 - SPAR_LABEL_X
        for cand in ("%s  %s" % (st["name"], self.ai.level), st["name"],
                     "%s  %s" % (short, self.ai.level), short):
            if self.font_s.size(cand)[0] <= budget:
                return cand
        return short

    def draw_spar_hud(self, c):
        label = (170, 180, 215)
        camp = self.mode == "campaign"
        draw_text(c, self.font_s, "YOU", 8, 13, label)
        name = self.opp["short"] if camp else self.spar_label()
        draw_text(c, self.font_s, name, VW - 8, 13, self.opp["color"] if camp else label, right=True)
        if camp and self.opp.get("champ"):
            c.blit(self.belt_small, (VW - 8 - self.font_s.size(name)[0] - 21, 13))
        self.draw_bar(c, 8, 24, 76, self.player, False)
        self.draw_bar(c, VW - 8 - 76, 24, 76, self.cpu, True)
        self.draw_kd_pips(c, self.player, 8, 47, False)
        self.draw_kd_pips(c, self.cpu, VW - 8, 47, True)
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
                if f.stun_t > 0 and f.bal <= BAL_STUMBLE + 0.1:
                    warn, wcol = "OFF BALANCE", (255, 140, 220)
                elif f.bal < 0.42:
                    warn, wcol = "NO LEGS UNDER HIM" if f is self.cpu else "GET YOUR FEET SET", (235, 150, 235)
                elif f.gassed:
                    warn, wcol = "GASSED", (255, 190, 70)
                elif f.on_ropes() and not f.clinch:
                    warn, wcol = "ON THE ROPES", (255, 130, 120)
                if warn and int(self.clock * 3) % 2:
                    self.chip(c, warn, fx, 54, wcol, right=rt)
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
            draw_text(c, self.font_m, "ENTER  REMATCH        P  MENU", VW // 2, 80, (230, 232, 250), center=True)
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
BUY_KEY = pygame.K_a                              # in the shop: buy it, confirm it, put it on
FEINT_KEYS = (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_g)   # hold + a punch = feint it
CLINCH_KEY = pygame.K_q
PIVOT_KEY = pygame.K_x                            # roll round him and off the ropes
INFO_KEYS = (pygame.K_i, pygame.K_F1)             # open the controls panel


def shop_key(game, key):
    """A key press in the shop. A buys, A again confirms, and ANYTHING else cancels - which is
    what walking away from a till means, so walking away cancels too (see update_shop)."""
    sh = game.shop
    if sh["wardrobe"]:                            # the mirror is modal
        if key in (pygame.K_p, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            game.shop_wardrobe(False)
        elif key in (pygame.K_UP, pygame.K_DOWN):
            game.wardrobe_move(1 if key == pygame.K_DOWN else -1, rows=True)
        elif key in (pygame.K_LEFT, pygame.K_RIGHT):
            game.wardrobe_move(1 if key == pygame.K_RIGHT else -1)
        elif key == BUY_KEY:
            game.wardrobe_wear()
        elif key == pygame.K_m:
            game.toggle_mute()
        elif key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
        return True
    if key == BUY_KEY:
        game.shop_buy_key()
        return True
    if game.shop_cancel():                        # any other key, and the sale is off
        return True
    if key == pygame.K_p:
        game.toggle_pause()
    elif key == pygame.K_m:
        game.toggle_mute()
    elif key == pygame.K_F11:
        pygame.display.toggle_fullscreen()
    elif key == pygame.K_BACKSPACE:
        game.enter_shop()                         # start the walk again at the door
    return True


def handle_key(game, key):
    """One key press. Returns False if the game should quit."""
    if key in INFO_KEYS:
        game.toggle_info()
        return True
    if key == pygame.K_ESCAPE:
        if game.info_open:
            game.toggle_info()                    # shut the panel first, quit on the next press
            return True
        if game.pause_open:
            game.toggle_pause()                   # ...same for the menu
            return True
        if game.mode == "shop":                   # in the shop: back out, then out of the shop
            if game.shop["wardrobe"]:
                game.shop_wardrobe(False)
            elif not game.shop_cancel():
                game.leave_shop()
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
    if game.mode == "shop" and not game.pause_open:
        return shop_key(game, key)
    if key == pygame.K_p:                     # P is the menu, wherever you are
        game.toggle_pause()
        return True
    if game.pause_open:
        if key in (pygame.K_UP, pygame.K_DOWN):
            game.pause_move(1 if key == pygame.K_DOWN else -1)
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            game.pause_pick()
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
mduXT41uL+eswSinz99rCICSJgi6HRiCvqDOLv93j571LvaY+th5fCp10G3Ea+XAsx343HgwdZPgDgnMAlDchrvN3pAxl1+k+jvQ
rO3xob1Jlibxly3LHIzk7/kUGQzU7jdc9BvpFVknWZI8GN2e3C1Lorykvx9nYe/BcE3bXs+WGse03bbGlOXZN5uWujqnX+u7+hce
B7+ZcjbceRvBXANpAwGZ+cI7g7vCBGFG3P6A0e1tio31/2qw/1Ut9n+fPi+MjwZJl6Uw8NuC8z2Uf3pZ3gGzF2nqwPcOSNGxC3VQ
PHsc6b4DcesPEpfzXFnbf0mpn33Wf1oTN8fKsvfL+LO5LImAp1MEoJe6e+6aVln7j/Z5FPYB/OyLAVLzAOhS9n3IuEuw1EeUXRf2
/rDRaj1IjXXRzXXgPvtpfDs6Lk0F/a+vzH2JkEiS0SjN/qO9pjw2v6xhWXvtMeh/m/MlvXADUJq2ZiTFv+fre5FemiQk7pkIKRoQ
9NhScFnmf37wf+p/+x/+LPweX52Yd2R4cy/nVhKY+UFDXxxzMW//9vUaeWsgUh9p0CfXpUkM6RuTHlt6XtogrU5eUM/JE5GvnXj8
OPxzs/ehG9+FtElfRlRPeGT2w8xejOQ/i8teY3Zu2Zt1HylY+4k774z00tw/kqLn3uLW25BP1vU3F2egs8uShHlEQXs/Yn3edxba
OHfxRtf1nVnEnWVLOt/jk2Wth7pIL25N4sja+R9zBiJpzYc+IRt7De6rm8Eg592jZ8M5Vlygpq0bXwn/vH/7eknRcb4kvd/Ty7q/
R1wfkMRuj1jnyS9pzPPFxeDcvrvO6ZtXMZ/KzvfcZ1n7JABfa7KM900dUN7Fadbu++5TEHyyWHneARSPBEjViEv+QmD68qQJBi1J
h7Y8Jy1s0Pj1GcV9v+/vMy5tLs/5W5vbHhGsOJss5U/ZFituHdTXx9rnrZqteTInzubdo2f1wdFBnfl4NnYfbOPbH+qb3/1SUrAX
9un9Ve3+d/9Wuzf3xu73bvvkhrR/n3Zs20N9pJRUFyZuQLN1Idae8zt5+hNv+X8zey9z+Y+tLOvMoR/o2p2vmTMnyHIHWGo8BxG3
LmruHu3YtkdSd5+niuOeNbf3XCT/vosbBJ1zza1x48DZe+1x74UvED31kE/We0gTV+ca1uQu3prRjm17Gu4nSf59+m49Y9huYWwl
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
L6Tte6XmZxEl1uDaZXDfDmlt3d7X95o2H8WIexdMwNVvfvfL8HOD+3Zoct8O3djx15KkA/f/vXYen9KPfzYcfk/ceSHOrbSPb/9r
5/EpfbVWLw+mbmrLaPTrvnMV4ecXpTF1T5+cdU7QjOmjfe+CeQ+k7n4Xsu45etci2G/MLc/eC+uercty/8jWjW1EO2Rp65POf7rn
nzl37mevvaU1PV9f2zSuLa40rIUinTzjG3ud4eDQgNyUzXHPP+JlPfdjnnffms/9h3c0/tLr4b1TiXNtZTHPPu1RNlnW4Ay3Dz4o
Rdoi7gSkk9T2NN/nLednhF9Se9ON6zVp2e0NqrNxcJcmx5rftUbxeAc6S9a7wGifR0/m1vX3DdQWnyxpc98GAtOX4NGTuXXjqgfQ
NXVw9I2h2ISpdsBEm1mfJllednb8k6x43lvnK//JsTdJ8NIGZgzUUuy3tRhkzLFaY9/vzXv+fNsnN3R495Yw9hgxx/JpVhec/28v
U/4TV+dyrstR/q3iDnB7ZYk/5s59TRIUSeHZ/gOz18PfZ9b2v+iT00taf7DL300Ef2PwjUjZm89x7iGfZmPRjW9/GDl7K0nv/cMN
ndq/Tz/+2XBkT1hSYnw+6iUde042sva5uLaLNdViUfbVyHIO16x7zt66H/YNjIEa2c+n3dfaezGs87eGtftymLHDuAZqhxSU50eT
13Voy3NhQllJkT83tbnYn7EbuEkHH44ckiRtm7gS/vnQluekhQ0avz4Tfq6ZbRNXGB+2wNQLdVCN/r6Bminn+cs3JCmS6Jp9xfZy
93NvvdSn7UcOSJPXNb68FHmuTczPd4+e1Vc3gwuJ7x49K62NgeISEG7d+Er4Z+4gpZfn7gXKZ99t2bFtD+1Om9l3ow3fXS8T6wGt
M/Nes/5s3y01d71eGB/VuYs3tPP4VENCTrTum9l73vX/NGdEfWsXkmrMn9Ox452bcvSNd0yMjdlb98O9edMfsF7RGl8dSI31YJf9
5NiblH9J7FhX9v5WUsw99h/jtWP8b69DUd7Z2fstUr78FrRD2cSNe5rdu+jvG6jZMZRc3L1Lz96vkYJ9mi8uHo6cd7bfBe4ttcZd
l5OC9VBJenHz85HvXV2NfmwwDytOq3k4URx7HXp6Pvjc/u3rI2N+1zez98KYiLr147J+1GeG3T9y3yvZoydz6y71DdS0VI9fbeY5
5uOekyci5zBtHxwd1JmPo0Eb3HGnMXF1Lnzeu/HuUX/fQC1tDPehDb0anf1MkrRj256afQb8ncFdNVPupq1PE+/HLv9u5J5rkLLN
K025Z+U+6yNvDUisZ7ZNXC7NCWvvtxvbnzKZ8jX9qlvelH/72GPOiatzDWsNafoA9l2KYepi62vjkuLHm8bTPvbvqfoH8MmSgFCq
N04sfhaD5HfVay0Baht/sC6Q9+Lv+z29Gn/pdY1++VkkACsbAM21EvzcDgjdc/KE9++zGZxP2nboq2/+GH7uL4PfapJEAI5s7IMo
rryJGRgT5UeZlyPLpm6exHe0/60zCdhMwkdJTZNfoHVmcWf6fP39MAmk7k5MRgI82OX/fk9vVybQzCpLEgxf2yPVLwcckzS2bU/D
36P9aS7Lug+JkMqRORjo1QMNn7LHQr5NPR/qMV5cnTTbrL9252vGpQUyG5NxgTrWNo4l1Td0THJn6qI533zAFwxISndYWqq/G8zR
0suakNO4fGqXjlhj1jGScabG+n912P+qFvu/1Us7J7YvalD+xckafI86yK/VPRfzfQQ+LFaaRJC+8kdrsrT97H0VK2siYJdZ9zdG
v/xMO6z1aOZffu3Yf1ydvBB7HgWNzCFoc1mmWfvz8M0DDYlPF5S8F2MuSSGZWafMm4zZ/pwUvx9MfUTZl2Hikr9I8Qmp7GAoUrDv
OLN2JvHA7HWNv/S6JEWSw0v0C1Ix+48SZZmGLwBN2rYmKRjQMQWBEqmD1iSNQ93kI5J0Y8dfS5IO3P/3kc+bunKTkrhIStJc2vcj
LV/gGvc8kS+xfDfKUvZxcwl33hCHdyH7nqNvLYL9xuzYe6leqvtHFvZ8y5U2GOX7Pb2c+0wh7drbkfP39NXPhvXt2sfmDLTbp758
5pR0864eTN0M+1LU5Z17xT33hl3WZr2H5z+bXImvB4bCdWdJ4e+Udz5px/rT82t3T8eDhCV2sgbkk3bvMakPXth7MDKHkngX0oh7
7jnrVqy8wbePnL9He9MGRa+rAU8b3oHq5AkAPfLWAOfd2sgOBGcC07/ev0lSsNZp7nYRmL5YecfpbvtlB6cfCX4jMGJG5n7j4FrS
KRvr/e1H+Zcvb+w31heK4d7vzXIH8vz0Lf3DewckSbVarUbssdbYdeFbq+D8f3uZtdCs63KUf+tauQNM+bdXOPd9tBI5P25ir7L/
lV4ryadmlurlbxLNmMQzB2ava2YtBi71kI/b7ptA8/b526/fu6j33qufu3XPGJr9MIOzha2JS1YS9w6ROKM4vrJnzbq98sb+YQwU
r1nCWbSOpLLlurLwvUbXbwgSyS5skBQklX1x8/Oa1HfhHorL1IuxJ6gf1upTMLE0H44cavja/OUb3j/7Po5z66U+/dX3u6iLHPr7
BmoPRw5p28QVSdRB2Uz5S41lbZJdp8G+YmvMHLO/b6B2ZeF7afJ6w/e48ZfePXpWUjSebTjuf2sgUh8mQRv7YfkUOe5xYzuzvtAa
+3zn8OZeaTE4A/qsJ7kuk73+OT2/rK9+Niyp8W703YlJ7Xbi/Pji/CMbt/x3Hp8K60CStJZr5MHUzfAd2Hl8KtIPG6y1FS9N38C8
uRhx5ej20YP7dmhy7UwQZ0BbZ48/7XL2JV62y/7k6U/CvUjGnu3ji3XVLOcX907TyTP+9z3v/X0DNdNvn7t4Q2Mi71QeWfcXDcY+
5UmaJ5j99eHNveF4lXehObNfI9XXdOKeecabrbOfx/6+gdrRN4Y0ffeW93vj6sOcfWM9olwmH+TE1Tm9M8jeQFHcdWhzx923Du3O
DbZufKXh76F9unlf5tGTuXWX+gZqQwrmQuYMpjmPac5gxvHF17bHncbIWwPcO8ppeM+LknbVpKC845jyNc+ybxzfjWP7/r6Bmi+H
9yVP/lAzlnlncFfka83KPWlONXF1Lrx/h+K5sc19OU3NXi91UCw3/kzcmoNZW+Y9aB9f7inT9qRhr9+ZeYGe4bFPO9l1sX/7+jAf
iaw9Fl+9PM1j/56qf4C45GtpA8EZDEzzIfldtXzlnycIN+VfjLwXf88c+oE+uPLfJEmXuICaW57g5zcG39CB2es6MHs9vIhqYzM4
n2bvgrmQ+tXbH+r3/+uPJdEPF8Xd5MrbJ1AX+VHm1UgbhCku8d39h3ckKUx2Z9D+17WcgG2qnvDR/G7XgS/ZI/yyBF99Ye1AtBSU
+UEFSU9tkfJfki71cQAljSzJF9zA20nPPuPP9FpPPt7GH66LNdsEmLg6pw+ODoaJg6/d+do7DuL5L457GVKKbha7dYL28G0K+OrB
iHs30HiJNI4bAH3E+pqvD3frg/LPptlcOO4iAQERk7H+Xy32v6rF/m+1mvW3vnfA19ZT/sXjHSjH9HyQJDDtnov7/NtjS8q/GFkC
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
XZT2pTVr5VfL0s9Ozy/rq58N61vF3/V9+cwp6ebdcPzEXCGefcbfPP/uWf7BfTs0uZZjxz73I/EOFOnRk7l1/X0DNbNXs7r6fEO7
k/demD3Ps527eIN+IUaWOIgon3sWkbaoOKZfMGeh929fH9mf99336tZ9mUdP5taZPQ7Tju7Ytieyrnnm0A+8f3d6frlhvOmLv2ef
/Xlu8Bfqnz3bFW12WLZLCuNVm99NjGo3jrX5fDNx6wsmn6A73nfjLaEYbluSZ90H6b0zuKv2wdHB8GN3HBlpj9bWJew1Zu4+FmfC
E1feiMtrSvl3Js7gtpcv7sOzMPbvqfoHaJZ8TZI3ARsPfDFIflct3+WLz2a+kCRtGRzSzKxIgNoGeZIv2yj7/IpIfGcnfGdA2poi
EgGgGF9988fwz3/5n/575GtmQS4uKSd9cj7/8vufS/p55HOv/vRzSUEfvDA7I8m/OESZ55c16IlE4ruixB1+znIA0Q6+ffFW8I7c
GHwj/Lq9GE4ihubSBjw3STBsO7bt0YVNm9r2sz1r7M2UNIkfpeS2xz6QyHPeXJrEX9OzZ2PrQmLsWSR7DBQ37mwSfAMt6u8bqJnx
/7mfBHVhz8vsgKC+S8H2Ablrd76WRP3k9Zf/6b/rs5kv9PnfvRq+G3/5n/57pA7iAhb46kGiLpoxZS5Jn//dq/r874J16Vd/+nk4
D3tu8BcN7RBzr9b59gHccrfbHavMa1I0+Sn1kR7r/9Vi/6ta7P9Wy+5zXab/DfxfevfP/rwhyTXl37qkd8D0wbwD7RP3DthjUJ7/
9om2M3U8++3n2/syGP+0X1LwVakxGWcc6iCfLElgpOQ9gDOHfqAPrvw3SdHABC72B6KaBWJKsy9m18OXRz7SJknn/yr6PUmXc9if
jJf2MqqdPNvXL0QuplkxYe1LVKaOuqU+zJr/1o2vxO+Fec77+C5f0xen16zcpfq5NxLvtEfchcak9sYXeIDnvnWmLpKeb3NZ0lzG
Hln7fNze/NfvXZQk/cN7B6ifDPr7BiLJT112X2D+nHUvwNSHe1ncPVdkPOvJ5NMkI5SCy6h2eZvkPEnJHXj2k8Wdv90yGKz/mxRf
vvNArEO0Jm7tTYpf/6HMi5G09vbqTz+XXvt779qbxN5vUeLW3xZ/tTfycVwwSt6BfOL627jA8oZ7/vnY2uePzc1oh7Xm9n5Pb9es
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
9lbS4d1bwrrgvG06ac4hSgrXrU29kBCjNeli0Ej2Hv3C7Ez971P+Lcm3BvHzSMJm2v72YXyZn51Q8N2jZxOTzLp/jzLP59GTuXX9
fQO1xSfBxc7V1ef1xcXDkXUC311e5PPoydy68bV7O75+cGr6ujb3bQg/NvVi3P3nJ9r9p33hxxvf/lBbN77SUGeIZ9eBJG0/ckCa
vK7x5aCsqYNymOe/v2+gdmXhe0nS+PJSw3th9wtS0DdI9WSzJtGs/TmJfcVOZdYyLmzaFPs9Qxt6paUg9gDzBf/+18Sv9kbOnsT1
y0fO3wvX2r4dDe6qvjA+Kqme6N0keD/x+HFivXQr3xk4SY1zsUHWG9rBLf+xkcHwPL9xbXFFw5t7G87ZUv7lMOUvSb9eO/NsvDO4
K7J+TX+cz9bXxiP7Ji+fOSXdvBu243cnJrXbc79Fit5/D+INMG/OwrcHMz2/LDmxNTiXXp6dx6fCHEhSurK31zAG9+0w9ca7kBGx
lsrj3gHIcgfG9AULew9KWusjRk6GX7fHUPBLyj8r1c96ut+zdeMrjP/bIOvZhy23P9XC3oOR594w84WxlWW939Mb5sFDeuwJlMOs
hb579Ky+uhms4bx79Gw4BnX3zAwTI9Ssibr6+wZq9rzCFc7tFtWV57PSxt1Lin+L4qW9g2fG+SYOIlpj78mYZ9tte0yZnzz9Cfsy
KQXlUV8r++HAFknxd4DjzqDXx6Pd5dGTuXWX+gZqWlrbQ1pjch0fsL730uqKzhz6Qey/9Ye5BQ3veVETTiztncenIrHnXVcmL+hf
fv9z7n1J6nHyHLs5p32axUL1xju3PDf4C/ZdCjQ8cTv2eTf7XyYPsL3/xTtQjOn55cT2xofyL97vL00Fd1qajDlN+2TmU5J07uIN
7Tw+FTv/QjnW4qE/lWv9PVX/AHEakq9JDQnYnsYCf1qQ/K4cSUG4I6yABAaT3daQ/K46zRLf+QJwcOG6PUjC2Xnc/rdeD/VLqPQH
7eErezcQhEGZtyZP0BOJvqBVcYfPjYlf7U2VfG3i6pym55c1LemSJxkDC6ZRTTd9PUk2fewNr2NLz0vOorgtzQJ5t3EvvzQsOick
fpSiBxJpf/JJG/DBDgBno+1vnQm+YbPHP/U6IfhJ2Uw9RN+L4J0w25lHzgebMdRBsdz5sF0XwcFd6U9+FHzN1AHJ3/PxtUGG2xbZ
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
Zq9H4qAnJQ9FsmZnn6Vg3c2wkxKa9TY32Xu49rZCzoa8mPOW48WjlzX28ZGGz5EAtXiHJ2Y1NjIoLQZthL1eb5i2ZGxlWS8evSxJ
4XswPHE2kgugPu9jP7KZfieZuY/bjkvSjm17wvWJ6dmz+uLiYUnB/Jm4WNlFYzsEa/1ff3ykft52fDQ82/nt6LiGpw5Ki8E+mF32
EnHJ8ghiyAdx5H17kl+89vf6+uMjmj5/TzpfnxuYsrcRB6t1vjvXZt+dtef2azXW5IMPzod/tvtu6qo1PPvFMXlHtr42Hn7OzSnl
25v54uLh4D7YoqSBIR2bm4k848b7PcF4idxr6RR116K/b6Bmnw0a3tyrYfXq5cOv6dzFG5z98Yhba3af/8F9OzS5b0fDOP+dwV2R
ecT0/LLuP7yjb1VfG7q2uOKd2yHKF2vMzA/e/bMqfqJnm68fMON67n+VL+++F3Ot9ExZ9c+erSllzjWj28egaf9/o89jvX/87ey9
df19A7XUsW/XdEu5P3oyt+5S30BNS/F7eCav8Y5te8K/89uUV4lMe3/o5Inwc+d+8q+CP/ykcR3O6IayR3fJknMT7WPPs8xZlJOn
P5EUzKW++tlwuAew5fankqJ77mjN9Hx93Wbn8SkdnpjV4q/2popDIwX1N6jwbONTte/YU+V//MrkBUnK3Ah1y2CoU1H+xcmT/JGD
QK3JG3xAouxblafs7SCUWiv76dmz4cIz5d8a2qDO0OoFVOogH57/8rWaAHWm7xTBiNukWfJTiYOGrYhb/K9v9kaTndrsA4YDj74P
P28WxV0cQMmmIdhGQvJfgl6Vyx7vMP6vlq8uqId8zKZklg0Zu536/O9e5Z1okamDrOwkndRBuWiDWpOn3TGY/xaDtYenD/tfxWD/
t1p5yz/ODwe2rP2JfjitPHXA818c2qDqmLKX8j//jPtbw/izWq0En/+etYbS+PYfKf/2i92LvPVjSdF9SOogn7i9eN9l1N/818a9
SYLP5NNKEiSJBDB5Ue5Pn7igNIz9i+GOQ5MCEUjm959r68ZXtH/7+kg9kICkWO5er6mHV3/6eWQu9sGVejBE3on28e29Mw8uD+sP
1WHtrTitrr1R/q1LUweR+0dSwx0kyj+bZvOvLxLOnH/x2t+H5W/afonxTrvR7hSvlcRr1EHrmpV/XCIMd72TOmg/3/4L62/5FbHv
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
"""
VIEW_F_B64 = """
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
0jDJ3z/s/ovGPqoEi81hanceSGIBuiwm/n/Y/Zfgc+4GCGnzEKQkJqAlMwvQBvHvLuLvD+OPf1z/frmbcKMKEEjtRTiYBxXH9e9P
2AZ0Sfrb//7/WjagSwrdgC7xO1BU3PhjFkHNfxl/yjXQX2ns3PkXvXjxqh7fnpCUvgDKkdE5me/dygsTncT441/YYltYAWKJ+U8n
MP/0J2r8cd8DKbwAn3kt70F+zH/8sWNvJ9Snri1rYWW97f5rNxw0r+c9KIbx3y/WH/xh/dkv8r/+fFIdbCysrCtv/CWu/6IYf/xi
/PGL+PvH/NMvnr/8Yf3fP9bf/Aob/9McgJeah2LIPebH+qd/3H/94f7rH+O/PwP9lYYp5mAKQKR1bn0tKATBe5Af80//PqkOBnuA
WH/oHjP2J81/oppDTtbXJW3tg5GdEhZ7I3L+sxF/UzxOkuZX65qscx/Oi/m/P8z//bLvuwb33+5x9z6bZmtRyL+Xi+cvv9j/7E/c
/NONf9Tc02AOmg/Xv1/Mf/yKyn+Z9QZ3/i+prQAf139xrL/5wfwTgA8D/ZXG498Nh87nXWZ+b+699v4UOzcsbd6zTd5gu49NA/2V
htu8zmVilXX9Z/xUNfR195afavzqw20f+zTcNbgTh3ZlWv9fWFlv+fuIeTZp8y/uOCM13yvmoPmZ2I9ML7Xkdt17ghn/JZ6/yuZe
/0m5dnsPKLEvhvN3/rH/0B/qj/nF/gf/3HPwSRbX6pp5UdfsmUFiXwL7DHASO/YS134Z4q5/O97Mf8pH/tevgf5K49HYx4X+joNT
V5n/AACQQ5YGeJK0+nyNdYcSUH+gewb6K435sWOhX7u3/DRowEn9q84g/r3HXvt5r3ZDknSz+n7b68w6hMT6f5nC1v8PvHOu7XVh
+1dY/y9uoL/SuPN6v45//zz43J3Xk5uKm9eb7yX++bD+45e79ypNDpJ7cPk+qQ42TNP3pPwv8S8mz77b+5dPEvcOof5Pb7DXgKTo
dSDWfrBVsP+qt5j5qD0OGXMLN/TixauS2OOPl0eW80dZn79Or70arM3xOxEuKf4m9qYWx9S1ZZlnMePrmTlJzZib1zDvTCdt/O09
hXGY/+cTl3+RpPNXapKkqHUIal/lN9BfaZz/+E29Xdkf+nWT/5KIf7dl3ftg8Bxcvu08/9/Z7X/Q3fh/eu3V5gRHCpLw9sEv+wa9
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
x3x7HDIH5BEurAGYFH7/tdenyUGWLy7/LjXHHrsQ5eyZQR0+eFS3D+6L/DuZh+Zj7/H5aeKc3njnSpD/spmx5tNnz0ILp5g8DE1k
yjN1bVknDu3SzMq6Jmq32r7u7tuSTPMMDoJFCcs/hu1z2z/R+n1x1z/XfnZhcyDD3vcWtgbBvbdzXql+riOjFzR7ZrDt98RtSsiz
WPmi4k8B4nK56z/259Jwz4QhGzN3MWsP7pqEzZ2Lopik5y8pPOZc8+UKa0L+SvVzTdYuBOsNcWv+dh6SpuPpmMKfcWPOp8+eta3F
2ftCW/4+1uBycXMA9nvhnr+2kQPrLDP/jML8sxw3q+8HORfzX3c8CjuL5GL8KYe994Hnr+6y183CGl1ImwXQiX/57PgnrT/EoQBc
eewGMBIFoMtmiryZ4m/GpckP2xq7mDHHfu1WKwDnCwWg/TDX7EB/pXFyqhnEq5e+kBQ+/zkyOif3dQu1CxvvAQ0A8lpYWW+La9T9
113fcX93kE1Y/be4PZ1mL5ApQBy2P449KNmE1X8LewaI2otIDrIY93dAat/XfGR0LvG5i2s+n7D4m+vfjDPmuo9b3yH+8bKefzHn
T21hZyE5A9YZZrw/fXex5fNROTCUI6oGbpzTy4uaNLUiECusgaN99sLkAL7Yu1efPnsWW4eSGhD5xTXSvLf8VOc/fjPYeyi1NyPn
DHDnEf/us3MBnL/uDNNw0F5nTmLmQ1H1y5Dsk+pg449XPi/895j4j21+qiGJddCMTBOqsY8q+tUv+iVtnnmR1JKXcRsx/+oX/Zpi
7bkQGgD7Rfz9Ms1PTQNHKX3+V2K8z+vrmbnIOYxpsDam1vXOsJwAze/KF9fcUewvL92XtaUdCyvrDSWcq6MBark61YCWPXDxnjxf
3jF+VY3zH7d+fvzqw5b5TljNDan9zItZ86T/TnomZmFNx+PYvcDC1qR5D4oLmtH6/kG2oIWVdWljbiltXv9t+0quLbc9ay2EzH3S
rt2hXdjZR0lB3dU4nAHrnKSahjSAzyeq/4g9f5Hi42/mRfNj4XlLpGPOAMcZ2t0nrUkzK+vUQSxR2D6styv7df7jjb0nG/fn6vHD
we+B+R0x63Tu7wjrP8V9+6/PgxzMwsp6W4wXVta1ML0UrMnZrwdeBlF7QKXNnPyYmmPPkdE5Pf7xz8HXD+x5S1L72hxr0PmR//Iv
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
bV1VqT3+cWp3HpT8E28tWeJv2K8xZ79YhyiG9efue/J8ecdMf6WhtebHQ7s35/X2GYCZF/Xgd8Ow5zvfjU93/ofdwope+z9cGYk8
RxDsm+hn/b8M86v1VLUopeY6KzFPb3jqbuh1PLS7T0Pq0+JaPVgbPTlV09xYtbs/4BZkn6E4MjrXdo7ur69fSVxr+/TZs+b7ttZ8
D+fHjklq7iPi+m9n8i9hiuxzs98/qblWZ9ZBeR/Kl2buv5mHEfeCBF/PzGlkeinIw1+99IUk6cjoBc2eGWz5mpR8/ovYp8f+q97G
+SNsZUnjT9K1H5eDIffSeUl1INA5nIMvzy///k++f4Se8Eo3/7ETh3YFyS17EhOWAEv7uhOHdnXqx92yoooN2Ih/56SJf5bPIRvi
749Z7AkTlgSLeg3y4/r3i/j7Rfz9YfzvfSbGr1Q/12unZlv+EP/Oi1vI3H/3OgudBTD++Mf6gx9prn0jLP5RryPpXg47tlHxj/oc
iksz/sd9HvHixh+J67/Tyhj/oz6H9Fh/8Iv5px/kf/3KEn/3tWGvoehVPoz/fjD+9Abuv34Rf39Yf+5tcbkvt/g5yvPaqVlN1tc1
v1pvy2/Zn5usr+uV6uc+fsQtLW1OkdxjMUnjv/0n7nXIh/uvX3ENsA3yL51TRvyTvoZ0uOd2X9z1/9qpWb1S/Tz4w/VfvrRjOvtP
Oof1H7+Iv1/kX/zh+cuPJ8+Xd2S5p2bJlXH/TYf8o19l7D90nxGQHfMfPxh//GL/bffEFV8NkyX+SO9m9f3IP+def7fltWnm/z9N
nNNPE+e0/+71tj+nl3mvjDTX/9DuPv1mZ59+uDJSyvX/4NE3GuivNDL/sNvAe7UbsX8kBe+F1B737+ZuRxY+HJle4hksheGpu0Fh
4Yu//Sv96fe/DP1z8bd/1fLn8Y9/ptFgSRZW1iMbMO+vDum1U7M6OVVr+UPsy5P22Yv1n/Lx/OUf68/+kX/xi/j7Rfz9Iv5+3Ky+
n+n17L8qJqkB1W92tje4Y++nP2nmn3GfRzqM/34Rf7/Iv3eXvcafJM/9l/xXMtMAPs/6v/3af/v6H/RvX/+DXql+rgP/e17D+/p0
tm8Xa9QxTMPf02uvSpL2VLPXjandeVD2j7WtXL6zqKlry5q6thx87sjoXMsfSbo0+WHLH+Q30F9pPHj0jd6r3WiL/5HRuSC/ZfYS
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
g/t8/FgvDdMA3m0u2ykPHn1D86MEl+8samR6KWgEeWvxvvZXhyQ1z/oeGZ0L/tivkci/ZBX23LWwst4WV0lt70HtzoOW94DYF/fp
s2ehsTfs92Bkeqnl94T4F1ekAS3yi2v8noa9x2H/3esl/ETbS1QTQqm1EeEr1c/b1h+Szqay/pZNnvoPKEeR+j8obmFlXctPahq4
fVPLT2ptf745989t33Ny5B/bXody2DH9l//zf3Xpf1/Swsq6vqwt7TB/7t26QfwLMusP7p8Hj76R1FwP/af/8c+6NjcXGv+3330/
iPvj3w1LUtseXJovR0uK/z/9j3/W2+++r3u3brTE/sva0g6TtzH3AuJfDs5/dV+W80dPni/vMPP+OPbzwJPnyzvK/6m3liz9LKLy
X+gOE/tXqp/rtVOzeu3UbEv9Q/Marvti7NyM2Zfy6bNnwf056bzRyPQS70EK9hryxcs3Q19j1trsdba4ewBxD2f2X6WVdv/VTxPn
9NPEOe2/e73tz+ll1inCmPVn8+c3O/s0PHU38vUm1lnWfcjPpHdr8T7nvzxL8/zF+Zdy0X+5N6StP8/+585I8wyctFaBfNLmH91x
6ocrI8HapyS9cf6M3jj5Tpd+6pebnX83f6Rmzj2qtnPU55Ce+wz2xd69qe+/2yX3u7Pb/6A5/C4p+K+xeOuexv/Lf25bVGCyUx47
/sND77V87Z/+xz9r/L/857ZNPcS/PGnj/2VtaYekxv3LJ3VktHWyxPuRX9brn/iXy8R/eOi90GSKi/iXi/HHrzTxt+Y/xL9kXP9+
pR3/iX/n/Fy7ENpU03ytef03Pyb+5TlxaJcWrNibA19RCQBpcOP6n2v5GvEvhvmnHwsr65pfvKnF9z/WP73ar//mxPufXu3Xf/vL
87bvI97lWX5SU2WgGnrtm03QrvmxY9368ba8pHuv0Zz/DDberuzX/NgxDU+1/q7Mjx3TveWnHf95t5qs8Q+LvUT8izDvQdjnw3D9
lyss/j/XLsSu/4fNgdj0lh3rD36R//KL/K9feeKPctlroFEY/zsjzfVv338vHT9MvDvEne/bByCJf+dkGX+If7nIf/mXLv+1tOOT
6mBjIeJZmeff7LLmv4h/udLE3xSBm6yvt3xv2Hswe2ZQU9eWO/+Db0FRa3DnP35T89/8wPjTIew/9Cvu3mu+nrT/xHye6z87e9y3
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
XZpUpcH7kyyIf0LuUWo+O9vxf+P8Gen2t23vBfGPxv43v+LOP8btSWmZ/1hmzwxq6toyz18ZUP/WjyfPl3cM1C40wvb0p8m/hNVA
ZM9/diYndrP6vt6r3dDN6vuhrzP31e/Gp5ufmPtAkrT/7nXtv3t984WV5LMZ2PTaqVmNTI9oVs3xe2R6KXa9bbK+ri/27pUknXv9
XUnN+dLjH/+sv/nb/9Wln3p7iNt/Ze695vciav6JVi3rz+7XJM1Ya9LufeDEoV1acOrkmhy8tPleDO/rk1abvysINzx1N/jfYWfq
wupRcv6rXOx/7g1Z689Lrc9e7Mctxqz9p6l/bvc+Cr5/owfS7JnBjv6cW1HY86959jX5rzDmPagMVINci5mzUnsgm6T8oxTkgBv2
s+9kfT32WcG8hrXPeHH93+0xpfl8xvwzj4H+SuOLvXsj1xfMXlzbP/2Pf9bUP4+3fK5ZE7r1dfZ7IDXro4xML5X0k3fXTt8/gC0u
scgEqPOIv19xB2CIf+cRf7+Ivz9BAh5eEH+/iL9/jP/d5Rb/jDsAT/zLYwpAuxvQTQMq4t9dXP+dN9BfaSRu/lT04SPiX8xAf6Xh
JrJs927dCDZ0ovPs98I+jIHuIP69g/j71T7/8f0TbU88//pF/ssv4u9P1PqnuwFu+IO39S//5/+yAa4ACvD1Fnv+w+a1zqMAuh8c
wO5tzP+7w9x/oxrAUACrs5LyX+isrPFnvClX0vyf8ae70qx/cv8txs3/2v+b/Hv3LD+pqTJQjTz8SA64s+z4hx16/7l2oW0Mmh87
1sWfcOsz74HNzH1oAOMP629+kX/xi/j7xfy/O/Lkv4h/5zH++EX8u4Px5/9v7/5Co7r6f49/I3IIackJIjJH5FeZ04syBA+I/CgS
RKRX4SASRHpRSul5LqRIkV5IKOLFIA/BiyCltCIi4cfv4oc8hFBkrkSChCDlITwnyNALz/AI0g4Swu8EG8JBMucirsmePfv/7D2f
SfJ+wdBmEnX4zMraa9Zae30HE9dfLfofLdp//tpF2AIKjvv3QoS1/6gCPA4FYLp5s/cWQl16u5OV/z1g/3n+em3/tP3ehP0O+Hl/
J5Avd4B5Wt4iwH5BxTCm7r2g/efEX4DZHVz/GwdAF4bxvxb5a/H5qz+4/0WD/f9a5D+4OP+tWP79n2F7z9n/qeH2f85cPGm1lTfi
V7P/Be1/hgb5a5H/YGD/bX7cvP+Edc75u8Ijafb/m+2Of35+uBi7DoN8RM3/b9dn7fnxIxTgjOEK/vr9j//1vwWvBln98X//j/23
//rfWX9JyV1P50bLLe/zads/61+98Ragzcq/5ss8RHq/3H/QVfzXWasv2aHKd1atz4buN/HuNeFe1XR6mX9m/i0fQcU3zXaLoP41
oACzO4OvXKqYrXf/ney7Ss6bf1AR1KD8zXbbf1ARVPa/xWtuNIZs2VqXpq7ZwvyPZtZ57nPU3IP3z8b9LMIF5dh+PuGfTfrzKIab
b/ho5qrZ838w/9BnLu9X0/fEr2T/Yf9bf+R1/2P915cFvLr9L+35ty77sLnU9t/7lvn/OFFz+u77cfcg0f9kc+lu3eauV8ytiS1W
LqT+O9bOfNb+/6N/f5LbazsI3Nybm0t23GfaDuUJq25ttu+duf0vZ81s5/6kY5fn2/PXhyrfWak+2+IzQbc0/fV2fda+/y+j9tf/
t5Ho/DHGn/kKux7s3P842/76j28mzcy6PndNHhk2WzerWpnfBZ/Ju39v9yN/8d3XZdadvduLyP1f/RO3B4vPX/lJe/68twZP7cmq
ffLF57wHKQWdP+zfg25mHfvPn73etKCaqa4G0tQXn9u5EyOFveb9Jmr9MWz9y19/quPsVs+Ytbq1aWbMTcdJu/7oz9+tQQatfyGZ
sPoL39/5we7+MN3xXNBZxWaMP/PwYGzMlt5u2dy7Lfv+zg87Z9C/7lzDLb3ebJ06e8EW5n+0cqlin3y90PUZoJ39+z5oLzncr38o
aQH4IAyAekf+WknzD7v5kfx7Q/5a5K+VJH8W4IvTa/7oDe1fi/5fKyp/s53NV2GHP5B/74Lyd1/HFSAk/97R/gdb3OF75F8M700Y
dx83QjefeG+gpCBheqXRcitoMdGJKz5I/r1Jkj83lBaH9j/Y4vLn829v+PyrxfqXFvkPrrD5TzbA9Rfz/8VJMv8TlT3jn95xAM1g
Y/2rOIz/tZKu/1IAphjp1r8oAJC3XvNHb9h/opVk/B/V93D9LRbr78Xyrr+E3VTk1r+CfgdYf+lNUP6HKt91/Mx2fZY1yIL41x+9
/197smrXvvg8Mnvaf3GSFIBh/NMb1l+0yF+L+TetXubfyL939D9a5K9F/6PF9VeL/keL9q/jinF6n0tTgNlfgMdfmIoCMOHa2b/t
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
1Oa3qD6I/Psj9Q0A5J8Lxj9amQ+gp/2nlnb9y4z885QlfzPGn3lh/KnF+qMW+08G0+ryU5u/Om53Hze6+n/WX4rjrqdm0QeYs/5Y
LNq/FuMfHeYftMhfi/y1ogqAkX+++Pw7mMhfh/5Hi+tv/9D/a3H/kVYe7b/RrFt1a7PrwYFL8U6dvdCexzRLn7/L3n/Qrfua9yFa
r+2ftt8b1/bn3m11PL6/84OdOnuhfR0w2zl0zLX1oIOdafPZBRX6DSv+6/ivA64QpDN5ZNhuDY9YaZSihX7eQ6B/uf8g9OeiCjD7
izB/8vVCx8OMA6Cz4POXFvlrkX//sP9t8LD/WYv8tci/fzj/qr+aG42huXdbXYVmvQWo3LxDWAEM2n/xos6fIf/iMf7UIn8t8i9O
c6Mx5K7D7uHdy3/q7AU7dfaCmVnXNThu/dG7NsBaTDD/2Mcs+fy/y9/7MOsutMlaTDTX/pNy70XYesAnXy/YH99Mth+3hkf4LJBC
WPv3P4LUf31Z9Mvb96L6n7i2T/7JlUbLrZe/r9j5+lM7X3+a6s+69cY3f5uyP76ZNLPuNV8z1n3TejA21s42qJ9xBZjNrP1f/zWY
8Wd+2P/cP89eb1raM7Can54PfJy++W33X4LMgvKPa/9mO30UY/503GdicsN+Fbb24njXYJL+Hvz8cDHy+0H7RA+yJOtfafog8s8f
+6+0yL8/kpx/G7QO4x/3L588Zq5Pcw+z9H3ZQedfgzGzrj0otP98ub3/xy7Pt9fC/O3YbGcdJSnWXNJLMv987PJ81wPpeceg/v66
trQYeQ+wt/8Ju/fRYQ2yd/57jLz5l0sV++ObSfvg9k1bO/NZ6AOd3NqL//Hy95X2fV3u8f2dH+zu40bH49TZC4nv/0J6jP/1ovbf
Mv+fj+ZGY2h1+Wl7D3rQ2cNh559Hof5Rcv79/15h/RD1p/KTZ/6sf6UTNf9jFpy/67PMdsafL39fKfAV7i9p1l/cz8f9fTm/xIFw
uJ//2PSNqs3cudX+OskNwM1Pzwf+XacLeYX7G/lrkb9Oc6MxZMvWmr5hNnPnVqLszcg/L+SvlSX/2AmgLz5vb9JFtKztP/QGvC8+
jywag060f62o/MNufjej/89LVP5RxR/JPx/kr0X/o8X4X+/S1DVbmP+x/XXtyard/+l+6M+H3bDkiuBN3/iW8U9Ogvof8u+fsP4/
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
j5C9R7voWsICzLXrZ2y1sWa1lTeMhQrE+F8jy/lXFKDNT9bzxzj/EECv8rzWNjcaQ1XLp6At0iP/7Bh/apG/Vpr8Gf/nz5vpzMWT
ttpYMzNj3qEPzp0YsWevN207ZO///NXxrj8TNP/faNat9mTVrnH+ZCrez7JBubrz4Eqj5dYv9x90rdF4Ba3XIF5e198f//0/7NoX
n3MNjxA2B+2de3bzzmbx14CfHy7urLOEqK1v5fXSD5y4OVB3ZiL3f/WG8b8W9Xf2Hv97UHuyavd/ui98RXtb2n7H/zmYfqs35K8R
VH+n/XxKUftR0C3vNrtf8j+s+EfpQLTIX4v8AQAAMKiYgNYifwB5Yv5BhwV4LfLXI3ct8tcify3y1yJ/raT5cwNSMWj/OIiCNsDx
u9BffP7VI3ct8gcAAAcN4x8d/+cvivD0H+1fi/y1yF+L/LXIX4v8cZDR/rXIX4v8AQDAQePGP8z9az0YG7Olt1sdB0FTCKA/XDFO
rzwKML/8fcU+Pn6aQpwRyEaL/LXIHwcZ7V+L/LXIH4AK/Y8W+WuRvxb56yWdY+b8z+LUrp/p+Jr5/2KdOzFiz94X/12rL7ULzPqL
yW7XZ6250RgqjZZbZjvFas3MyqWKfXD7pr1aeB7491OAM1xptNyqLS12POf/eml51Z693mxfH0qj5Za/UDAFOLMh/8Hg1h1dH+S3
XZ9tFypHb5IWYDazdhFmFI/xv0bW868oQJuPtPlz/iGAQcQ1XIv8syM7rTT5M/+cv7Ttn/F/vpobjaErlfFWbeVN+znm/Pvjt4eX
7JOvF2zbt/f/t4eXrP7rS7v7uNHxXlyautae/0d27rOs60tqT1bt1NkLkZ+BvWs0/ueRHeOf/vHOQXvNvduymYsn2/POYeu+7vel
vQ6zbjZ5ZNj/Y+21x+rWJu9vztLMw3H/Vzyy0aL+zt4RNG66/9N9apf0GVlrkX8+qL+DQXJI/QLiXJq6pn4JBxr5a5G/FvlrkT8A
HEz0/zrNjcbQ6vJT9cs4sMhfj/5Hi/yx3zQ3GkNM/uuQP5AM118t8tcify3yB4D9wc1ppjn8BPlK8/mX/LXIX4v8AeBgov/XIn+t
6RtV9UvYd1h/BJKh/9cify3y1yJ/LfLXIn8t8tcify3y1yJ/LfLXIn8t8tcify3yz84VGkzy/bQFCD+auWofXfo00+vCjgdjY/bV
4Z3DtF0hyLCDuMuliv3xzaR9cPumrZ35LPTxb+XuA+uRHf2PFvlrkb8W+QNQof/RIn8t8tcifxxktH8t8tfh/E892n++atfPtIv/
rtWXuorJbtdn7dyJEcVLO9CWllft8cJC4PcazTpFmAuWV/63hkesNFqmaGSEB2NjXQXIzXb6npmLJ/v/gvax5kZjaO7dli293X2Y
7RRgdmu+UUWYuf5qkX++0p5/5X7evQ8UoO1N2vzNun8H3HsAAACKwfhTh/lnPcb/xXhUfzHkfYT9HP1P/n57eKnrEYT+J1/eviSq
D2luNIa8azReQes19EPFof/pnZuD9j7OnRix2sqb9iPoGuDvfxrNulW3Nq223nlfmfu6urXJ74JHmvvvkuD+r/6j/9Fj/lkr6bgJ
AOJw/vPe9PPDxcjv+z8X7AWH1S8gSnOjMWTLxmY2EfLXIn8t8tcif71LU9dsYf5H9cs4sMhfi/x16P8BqND/aJG/3vSNqs3cuaV+
GQcW+WuRvxb563D91SJ/LfLXIn8cdMw/a5F//pJufqP/1yJ/LfLXIn89rr9a5K9F/jr0/1rkr7WbP+svKqx/aZG/Dv2/Fvlrkb8W
+WuRvxb5a5G/Fvlrkb8W+WuRvxb5a5G/FvlrkX92zY3G0NxouWVvzSY+HO76vrcQoSv6GFaAMGj9/dX0vQJe9cHlikD6+fN/tfC8
Xy/pwKP/0SJ/LfLXIn899h9qkb8O/Y8W+WuRvxb563H91aH9a5H/YPD3QRQAy261sWanykcDn/dz7Z/881W7fsYm787aocp3Hc9v
12dt5uJJq628aT8Xdv39aOaq2fN/dKwHTB4ZNls3q1q5RYGlbmH3siwtr9rjhYXAwnb+/D+4fTNyDebW8Aj5h+gl/3KpYn98M2kW
kz86Lb3dClz//erwsM29L3LtuHVg5+eHizt9Soy9WPirn9pr8R4zF092XHOD1t65/mox/i9G2muj9/fAzChA26M02fn7INf38B4A
AFAMxp8A438V+p/81X99aZV//TjweRTP26aj+pBzJ0bsWX1njWatvhT4M9v1WTt3YsQe1Qt6sQcc/U9+/G09TZv1zj83mnUrlypm
650/U93a5Jrskeb+uzS5sfbVP/Q/esw/D4ak4yYAKELcfhT2oRSnudEYqlq5ZesW+B647Pfa54BD6heQhJv4dNgA1F/kr0X+WuSv
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
"""
VIEW_B_B64 = """
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
EYxBIfFHdlnmP+Z3gPhXw91/Yu4DfRMz7D9pA/LPflEAwi/i74dZA2D/oV9Zxv9zP62SkygZBSj9Yvz3y210YTD/bA/uv+2XJv/w
5c3ZncZrqEza69/eC3Ss5xDXf0Fm/s/+Z7/S5t8k6Wbnq+D7uP6LY/+/X8TfP3dOb8Ya5v/tQf7BL9Zf/LH3oXP+xQ/GH7+Ivz/M
P/0i/rtL2gKgxBtAHk9uXQ7+vPDwqYYmH0fWf3s+PNi05ksD+Ox6u2tbJuanrk03fe3iiS7NLa5H/t00+89v3F7QveGzZf/Y+wb7
f/y7+Ktzuj07H8wvTczd86co10f9p7fmFtepP+ZZ1P2X8xftERV/s+ch6QwkiqH+kl/E3x/Wv/ybnpuV2cdjz4EGFV53m/o/5Zqe
m23dg6idM/A/r7wK5qIS8S9L3Pl3M/4Y5vfBrX/L/L981P8EAABAFdj/419V508HejqlFWlM5OnilJF/+3H6AfHOwD3/+8nLl5n3
n59/vqIHfT3t+YH3AXsNQFLLepgZo1ZW13T8y3tB7Lnuy8P+z92B/Fv7sP7lF/V//OL8r3/sfwDgC+MPgHYrJf/fd0ZPn3/flp93
L8uSf/vk5UvZ+dMw82sbpf+M+52bt45z4XCntCb6Eibg+dcv8j8AvBzndzeg243IpZ2bQdPGcxqwlSYq/m7z8bgGbMS/uKgDqKhe
VCProAi0Ggexw65/GjAXRwMGf8z4H1YAIurwo4vxP5ul1fqBk31ntj7u6JR6dw7YuY1/TfI/DAcgyxF3ANJtvmzGo8GjB5sOQXL9
F5MlAWHuxzSGKQ8FcHcPNoC2H9d/+5mFlE9evqQBjwe93bWtF58O6D9n7ksqNv9vFLHk9yAPO94dHa/U031YP6+8ankWsJnrfnPz
kC6e6NKth/Maf+u99v7ge8Tnrzv1hxPS3OJ6MMbY8TbPAPbrxL98YQWA3OcvqfkZzC5Cg3zinn8lNRU+bHr+1U4zSJ5/i3Pz/+ba
dwvg2gWZovLWSI/1R7+I/+4Qdv81c0/3HiyRfy6bKUAZNe93n8OIf7nM9e+OP4ZbDJH4lyNp/hk3BhmM//mlvf/GFUAn/sVEzePt
4v/Behf7T0qXNv/M/pNqcADAL+LffvZBok9evgz9Hnv/oWlE4mL8z8+spafdf2jeA3MPYPwvjgKU/tnjir2ewvjfHmb8cZ+92P9Q
vaXV+oGoYm/u/VcSz18li8r/ROV8whrQkn/Iz+zBCuOef5Fa48/1XxwHsP2JG/8fvtWtcz+tSmrOxdm4/ovj+veL+PvVkn9YF/uf
28SM/bdn51u+Rv6hPTj/64d9BoPzL36Q//SL+PvH/NMv4r87ZCkAyn0XQFETd+upvi/s/JHxh4MbulWf11jfmVJ/tr3oya3LTZ//
9rM/Syp///m7taO6MSiNzIj7hMPN97P/xx+z/nt7dj53DQLWf8tB/bH2+6j/9Nbc4nro19x9V5y/KF/S+SOjpe4A+09KQ/0lv4i/
H1H7z6l/1T5X1w5JJ6S5RYWeezwxdEm6ORu67mjq/zD252fHf2V1Lfg9cOvPh71G/Mvj1n+I2n8bNw9FcdT/BAAA+1XUmQzmPeVj
/48/Wc6fRtV/eNDXU+0PuceVWf9noKdTWpHGRF40rSL7z88/X9GDvh5dZf9Jbm7OwX0PJMXGHuVg/6d/5N/aj/NffkXtr6L+T3uU
cf73445OTXFPyIX9DwB8YfwB4EsZ+f/7/e8Hf55f2yjhp9pf4u4BUnj+7ZOXL2VqSIcZ/ek7new7Q64ih6g1GZSvjOff5bMfNP2b
91YYg9IqI/9D/IE3W4fP/7i7Ad3d7O9uPOcAarns+Ic1IRxf2VmMkYh/WaIasEVe/zRALY1dANFtwGyYRUdTjCDsADDyS7sBbrTr
cOj1TwHuYuYW10MLb0jhhx8Nxv/ipjY39PFSp+YUfs+Vwg9CcgC1uPm1DV043Bl8HtYA2zC/B5JTCAKlyJKAMBuh7cYMyI8CuLsH
G0Dbj+vfr7gGVDTgqR7zf39efDqg41/ekyRdPNEVFEE51tMYayRFxt3M/WtLrzX+1nua2tzg9yCnz1936g8nGr8LHR2v5G4ot98D
N/63HrY2jkF6O7FvLgBks+f/pjCNnYu+unZI82LBsYiw59+wIkBRz7/MR/NJKkBpr3vZsTeFccfX18j/l4D1R7+Ivx9uAT7pUGjO
2b4Hk38ujx3/jo5XwbOXPecM5jzbfyb+5Ulz/YfNOSXiX6ak8V8KH4NQjrD9P0bY9U/8i0uz/8Sg8Go14vaf2Dnnh29tPwOz/6R0
9gEAuwESBdDbg/j7FzX+B+OOFLn/E9mZe6+kyPVHe/w3+0zc/Z+M/8VRgNIvM/67zQcZ/6tn5p927M3zl73/QWpdC5YYf4oyc/+4
++/M8uvY5y/WvoqL2n97YuiSFu/cb2pAG9yDQ/YDIZ+k679p7ZH4F2bnfrLsfz730yp7nitgrn/7Pjyz/Do4d0Thw+q4sTXjCtd/
ezD++GHmnpubO/N6+/yvm39g/3O5Wvb+W8y5U/IP1bOvfykkB634Bhhc//l98vKlOP/iF/lPv4i/X1nm/zyHlY8GAP7lKQBK3rk6
NCDEfhK1/mLuAZJaa2CR/y9s+Nc16W690P7zkSv9bfyJ32z2vh+pUQdoajP8e936YxL7f6qStQYB+8/L8c3C4wO93bUt6o/5FXX/
Ne+Hew6b679ccfXfDOY/5aP+kl/E34+o/ef22hf1r9ojrAZWFOY+5XPPYIfVv7LPwHd0vCL+JXFj786Bkmov8R6Uh/qfAABgPzLr
7vY8yJiemw2+ztynPOz/8Y/6D35kqf8Ttf/8QV9P02sDPZ3SijQmntHCuLnPppoDszv1BTLkn/W02h95T7Kv+6i9h+YskjvmmD2I
55+vtFz/yI79n/6Rf2u/qPvvsZ5D+nnlFfX32sCu/ybtjPtu/R8zHzKxp/5Pce71b6//pj3/+/WRI5pfo/9FHmb/g9nnaWP/A4Aq
sf9qd+L8F/aLMvP/Zh46tcl8NK243E9S/u2Tly/19Pn3bf+Z96qk9cfNzUP65OVL2WfIkF/c82/a/c9R+eexjfUqfuQ9p8z8z72V
nXGf+OfH/NOv/Rj/Dh//0bgGbPZgE3cAfm6RgSavNIcvzJ/tAxgSh2DKFNaALe765wBwMWYTSlIDZltUEwAaMBcXtQHOTDpbDl9v
F+BAPpcWZnWy70xk4Q2TeAjDIchy3Bs+q4GJR/q4ozOIe+Pe2nro0X3oMrG/tCzNsRklk6XV+oGp7trW6MJ3uiTp2rkLkQcgpeZD
wWGHILn+i3ETEJKkdQVNR6TGn80moMGjBzUoqzEJCqEArn9sAPWH69+/sAY80s7GTw4ele/4l/dKmf9fXTukWsdrTTEeZRYsXr2W
1Nep889Xgjycy417banxOzG1uaEbg+9oZEbEP6fPX3c2xT/sOSDsur/f/z6bbwv6/HWn/hBRhMZ9Bl5ZbeR9zDjFQnwxSQWApOQi
QJ+/7tS9Tg48FhFWgDKs8KfdiBPFlbH+SP4nP9Z//bPfg46OnUN3UcX3pObYk4coxo1/2D04Kv9P/IuLuv6l5AKUrL8UEzb/DFv3
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
0Qgp+v7K3qty3Xo4r2vnLhTa/0wT2uJM3s3o6HilldVXLfeApuu/RxoQ+Z8i3AIEea5/9p7nl3T+wpwDaCn8s3yYIqw52edP3XFH
ai3EkVR8nvxDPnbhpaQGGC7yD+Wy8282U/zHjEEG6y/liDr/YnPPggWWd35fGIOKmZ6blVl3cQth2UX4DMafckWN/6bonqSmeU+a
IohI5hY/l8KLjsWtQTL/zy/t81fYPZj4F7e0Wj8wrtYCoIYZX6LWYzY3D1EMN6eW4m8WUxCaBoTtQQOA3eEfC48lNe+/nVtcbzmX
/eTW5cZZvO0/SzRgS7Lw8Kn6z52M/LqJn6m/FFVYdW7ycaozqCMzz7g3pFRbeq05Ne6n1B9rv3vDZ4OC5aYGU9T+8x9HJtv94+0p
bv0r18jMs6bz7+75I+JfTFL8Jc6/tJsZf+xrn/hXL03+OQn1x/ILi7871w/LP9uIfz72/nOpOe9vGsDYQusetu/H3TPs+6/dPMfc
A0zt1bj6THeun9bQ5GOu/Ryi4m/OXru1l5bPftD0uXkfJMaeIpLOv88trlN3oA3C6n8e69xe+7Lqf5omYJKkFHUSAQAAdqtgTuMw
eQf761Hfi3yynL+w98JJ7P8p20f9p7ekxlkMqTUP19HxKngOGF9f02edrfW5peY8BeuR6ZhruLe7tpV1/ffoo29D/03i38rO/QxM
PFL98MHC+f/ffvZnmtDmEFy3fWd08VfnmvZdpenDYLD/Jz+7AfzPK6+CBrNf3pwNxnlJTX+2sf+zODf/Zt6HvomZlvxbWDNy+u/k
Y9chi6u/5K4/mnlocAaDfVeFhDWBD3Os5xBnLyoSN/+MOv97de1QsH5s9w5AelH977L+G/we5Be39//58KC+vDmr8ZU1zgBgz3HH
H/sZwOQ6k3oQMv4U0zcxI/ccGOe/2s++D0jN9wJJwZyIcb88cfn/sNo/7hrAxRNdGrnS7+NH31Pc/Jsx2rXzftj9gF30JMwvy/rj
uZ9Wm94TF89h2bhnsE2OM+xctvv8W/S5DQ1F8j+su+RH/YHdwY3puZ9WI7+2l+Pf4eM/ah8AkEQDtjaKOwDgNiAk/uWjAZ5flxbC
Nzk8lYImPC4aMFcrbQM89/eAIhzlowHt7mCKLQ2Isb8dTBEs5j/VsRugJhWht9H8ojxJBdDDik6GNcNDfvYGUFewCVEKDv8OHj2o
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
n32r/kn3Jvv8dVL9ExP7O87rXPPlSJp/Jv1u8D6kE9eA3BbWbMfOvdmvDU02zvKR/8nn4q/Oae6vD1tedxue2lZW17S5Gf11pNPb
Xdu68v4FSWp6D35eeaXnw4P68uasxleam8/2dB/Wyuoa9W5LEvceSCL2FeL6988d/xfv3JckPXyrWzPLr0ObX6O4L2/Ohr5uP2fZ
TTfNnIj19+x6u2tbXx85Evs9Fw53SmuK3GuSvj4oeaAo9ntg4m32e0bF1372jXo2k3gGy8vUQEnq/5UUf4n3oAxuXWGzNyIsB23y
/8gnLH5R6y9p/z7Cpc39SM3vgflz2H25/9xJPQnWx7jvxskSf5OTloh/VaLO30Xh/Fc57JhLjfch6fxv8Ew2+VgvPh2QpOA85EBP
p7TSeG5IOsOKfEx9PbP3M66GGWNQ+cy1/uPIpOefZO9JcwaAvf/lsnsR2vlP8pz+JNU/dNnPXuTe0mmMM63PAe/WjurGYOP+GbWu
a85/mdy0+R0i3vlkOftlcB/Ix9Q/PHVtumn+/vaN69KDv7bUNvn8dafurWw4tc0f697w0bB/XhJzzzIM/7qmibt1DTuvT9yta+RK
f+Lf5z3Izr6P/mWqkeP57Wd/bvk+894k4T1olWbvuT3/sdd6hyYfp6qNiGJM/OcW1yXnOk/qE0P80wubg/5QX9bx8+OJ9QfsvvDI
Lq7+Q5r4Z+mX9Cbp8PEfpQHb7pF0AID4l8ttwEYDyPYIaz5lF+BOgxtw+eIWIIOxJ+TmzHuRX9gByDiMP+UzSdBf9J+WUh6A5D0o
B9f/7pLUfJMGYMXYSbhg81VjPUVTmxu6MfhO7N9PswGLBchkWQtAm+v+6qP50O+/KlGAviRpm9AajD/ZmWcw+7U0DZBQjqXV+oGh
yZ34c/22n0kmT9ytJxY/icMGiHzs+KeZ+0ch/vmExT/N2G//rpjFeN6D7OzFrKz3XbMZ3eQiOICaHfn/3YX1r/Zj/dc/8x5kuQdH
YRN6Nlnyz1z/1ch6/cd9D9d/NmWP/8Q/P+Y/7ePuQUnaf+LGnnxdNeJy/03Nl8n/Fxa2BhBXPCAp/mxAz8bsO3nxYDQ4ABMXQ+Jf
jb9MTUuKjz3jfzns+64poGEXzkgqXkIDmPySDoBlbkJufY5k5gBwXva1f+ratMzvEIVnypH1/kkDzvKFNZgKs/DwadO9Is2hYOyw
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
VCuNnmDILk39H3O9hz1/Me6kk/QMbJ/BM30uBtQZ+f3I56P+01uS9Kfbv5fUuJ+647vt4omuYJ/o9r7zLZ65imP9q3pl739Ddubc
URo3xz5seS3sXJidF/qo/zTjUQ5mD+7cYmNsCRuLzJhjzoAR5/x+nH4Q1A44+ujblpomYdw9Jm79XIn5Z5yo+p/uXMfM/834Y/IP
p65Nh9YuM7h/xEtTf1VSsKdw2Hl94m5dI1f6E/8+tXCrYfcbtPOhJu9M7r9aaeLfuC97+gHfEEXqD8TVJUAy6j9E6/D5H6cBmz/u
AdQkFKEpV9YD2MS/HGawdovQR6EBTHFpC4BG4dqvjmkEloT3oHxzi+uasw9vhWw2kdhk1Q5FGmAz/scrUgBaogFYFczDcNoEMhuw
iosqAD3603ea2owuKD+2sS6tbG+00k7x+bGN9VRFJBAvbfETrvnyJRVB5PmrXHbxPSn/3JKF+PxM7s18bq77qN8Bd7H44omuan/A
Pc7Ef2jycVNzNXeRyyD+5TLxd4uecP23h5v7N/eApOdf4+KJrmBDEPfbfMj/+8X6l3+s//o1t7iu4+fHd16IyD+bTUDEv1xN8ef6
b6ve7trW5YmdXWszN7+WJJ269kXLe0B+rRqM//4w//FnabV+oMz9J0jmrkFmWX80yP+XL20TJIn4V6Fo/Fl7yY4GSH6Ye4D5/M71
06nnNcx//EiTe2AMKiZNARq7CaHJ/XPwqxjyCtVbWq0fGJrUVtwBxqx7qEzzEfZA5BPWADWOW4SVZiTlSTP3Zw5aDvfs0bCU6vqX
mH8WkbT/PGru44rKPzD/zObe8FkNTDySJN0YfCfx+0/2ndFnnV2R+58lEf8EYUVkshaPIf9WnH0PkLI3H0T54vb/37l+OnH8Yf6Z
zG2AKmW790rcf/OKiz1jT3sEc541BWfA5tca40jc2a+vbt3X1fp802umcJ8ZhySTJ+X6zyNVAXp+RypV5PwX8rHn/8S/GkkFoJNw
/rG97N8DuwhrWAHoJ9vPbsQ9WVQRPlN8b2TmmTY3D4X+XdMAwOwV7e2uvfGF93wqev5LaqyBsf5VnizPYRN366YRBhLE5T2z5h9Q
HncMKnL+kflPfvY9gPpX/hD/9kt7/k4i/lVI2wDYsJsRSo3cKMXR00maB+W57pGNvf/cXnspknujAUZ+ac+/u8++PPeWI2/8yT2U
I835azMG2ftuab5TrpEr/bpxeyHYD2qYOJtzwsYv+k8HTciZe2aXpvGgi0aE5ZpZfh36+pc3ZzV49GDT10e7DuvcT6sa7UrfrBbx
Fu/cb/r83E+rkV9zP0dxWa7/qO9FPt8sPD7Q213bej7c2BD35c1ZSdL4+poG1R0ab8b/9nDX34dCnglYe89mfm1DlyRdWpgN/fr4
W++l+nfc/Ju0k4NjHa1a9rlrY2m1foDz18m+PnKk6fMLhzultca+27T5Tbf/hSTuAxlcPNGlkZlnTQ3EpZ0m4nF5fPMc7L5XnLtI
J80Z+DhhOSD373MPLsb8HqD9sp6DRPnS3oOj/i450Gju/EfaeRZ4+vx7new7k/hv/Dj9IPJrRx99K9Uu5P75kM7Cw6dN501ZB8su
6hl4PuIZ+O3L52Ov/av1eY2l+P3BzhmAucV1SdLx8+NNY/qTW5f128/+3PL3zNqXOYshcQYgq97u2pbJ3Xz+ulN/OCEVWf+6unZI
84o+t4r0kva/JeUomP/ECzt3FCXs/FcUuy4Z0jNjt9R4b148GNXx8+PBGOMyY872mZct5jz5LZ/9oDFfl4L/NfUE4pj8vn2tk//M
zsxf3H3MUWOIyfvfGz4a+nWpcf9g3C9ubnFd2q7tab824unn2Q+Scm9u7U8beefiisafe0Ay89ybRpb5J9IpOv/fy/UfOnz9h2nA
5h8NIP2iAZ4/NMBrr6gilC8ejMptBG+jAFZ15hbXNWcnHhj/2ybt/MfedBg2BjE3yo/5T/vkLQDN3Kd6aQtwUGgjv7gC0GYDVlR8
g83nKzuv2c0vkKxIAwzm/uXK0gDV4D0oj3n2HXLm/neunw6NcdjBFxTzzcLjA3OL61uy3oOw8fzUtWmZ5wTzjDC38EVbfsa9bG5x
vSWuQ5NfSM7vhCTiX5Ghycfi+ven6dlXCm2uKYWP/+TZiiP/7xf5H39Y//UrLv4BZ1Ni1DMY7092ZeX/zetIz479d/NPJElH+y9o
eWFeB/t/v/M7wPVfGa5//5j/+FPm/hP2P6TjrkGmbQBD7rlcWfP/xL9cxN+/rOM/ymHujx/1n96SFNuAwSD/Vg0KL/mV97nJzJkm
nMOSCBe3b3MoZt3dMGOUYeLOwbt07AKINlNcOE2hB5rAlM9d/41afzSxN3kImpEU17L/JCL3g/I17b+y9z8UOAODeFH7z+2Ceihf
b3dtK+zwtXnth/pybB7OXPtjG+vsf87JvvbNHmi3CXaRBszILuv9l/hXKyq+/edOSpOPY8cf1l/SsRugSgrGnTTXNtd/MW7szR5+
4l8te/5jnwEzpjY3dGPwndAGAGbuc1WtRfrurTTOjplxiDlsduSf/SL+7TUw8Sj4sxmT0u6BQDnc94DfgeplKQBnz3Giir/RgDm7
uPfg3dpR3RhsjEVhZ0tvjn3Y8j6YwnsUoMyvyPkvYl5M2PnftPHfHmcohJ4gbd6T518/mvafc/6x7dj/7xfx9yfL+VPiX0xc7aW0
tcfs5uOmIdtAT6e0IhqQJ0gzDwrDfbd8ViOj0H2FYaj7Wb4859/tv0uup5g8538NYl9c1vi7DWDYb1uugTPHNHG3rmHn9Ym79aAB
qmFyz8jP7MFN0wTVbX5K3q24G69WmmO+Lo12Hdb4+pq03Hh9fH1No10733Oz85XVJPJQG3/avWdm+bWkRowl6fnwoPomZvTlzVkN
Hj0YfN3+XpTHvf5/XnkVvAfu9T++vqZjPY3rneu/XF/ebDSEN78HJ4YuSTdnQ2PO+F/MpYVZ3e9/P/Z73PX3qGcwpDe1uSG99V5Q
d952aWE2+J64PFxY/k3aycHRBDta3DX/cUdn6B4Tm8kT2Xm6ibt1fbMQ+VegxjPu0+ffh37tkqRRNXovRK27G2Hxlzj/noV53nL3
OV+eWIhdezFMLpomwPnEnYE/2P97SdHxNzW4h4b7iX+FTO1JzjW238jMM+JfoaT+OybPTOzL09td2/r6yJGW182cX2rMTdPMQV1H
H31bwk+4v9lruGnrz7Dum994yDPw/NqGRn/6LvL596tb9xvPuBau/ewaay3NZwB+qC+3jDvuWpfNXgs2Zx45d5GNyd18/rpTfzgh
5Vn/urpG7rkMac5+sfewvTj/VZ2oe8Dx8+M7PU5D2HvmUJypJWDmMUcffdtSX8Bmzz/dHDTSs9dQpOZ9zFcfzeuPtQuRz2HmXuHu
30Vx9jOVmX+aPbenrk2H5i4M3ofi0tQgMPMgW2MtvsqfbH8oFn/2QiQpu/4AquPGPyzfZs//33QdPv6jNGDzjwZsfhF//ziA3V5u
EUpJqQpAoHxlNQBm7Mkuy/zHfo/MBiyaXxRHA+z2Cxv/m5pg5GxCwiJMsqQNWHEFrih+VY6sBaCNhYdPWxbImCell1QAJa4JWJoi
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
WC7i7xfx96es8Z+xP5+wBmwtsZeCdfe4PYi8B8kS955sxzlqfDF7INiDks/Sav3A0KS23H2b9v9q8nHQkMcVdgAM2Zj3wHx+8USX
5hbXm2IbdfjRPYDNmldx9j3AxNUU3QtY918acJYjev0xPvcgtTSA4X6bQ3T+J038yf8UFbX+m9R88Lv5J03rvzwD5JenATMNaPP7
ob4cFM6wX5MazwF2AcQm7P8vnWn+kvX6l6LPAHD9p5d3/A8b+yXG/7SichCXJxYSG8BLjD9l4v7rV97xP+oMNvEvLq4AlrRTBNSg
WGV6AxOPZDfiuXC4U1rbyUGnyf9PD/e38Sfee+yiz1LzGUjiX62wJlTmd2BqcyN1/Fl/Kd/oT99pqu9M7PeY86duIzZJTQVDgb3C
jDVDITUJftF/uqUJJA0A0uH8l1+568848efsYzZ2nMrc/yPx/JtF3vOP5D/LQf0rv4i/P5w/9cetvWT2Gqa9d7rNMqSdpiVIz1yn
H/Wf3pKS5y7Uvipf1NmLsP2HUvP8E/mVWf+HPaDZEX+/Sjl/Tf6hbbj3luej/tNbYU0I360d1b3vf9aLB6M6fn489O+a8y5mjaW3
u7YlUXcgL/NeFP03yPfn09td23o+PKgvb842vT6+vqZBdWu063DwOcoXdf3b78eJoUtavHM/9t/g+s/GjruJtX2Nu69tbh6S1Bj/
b459qIWHT03jO2Kfw9TmhrS2vfdE0vzahiTp5Pb+hzx72qh9Hs/e93xv+GzLPqy0+59/nH4Q5Nv+KUkfXNHRUeebahfK/eH3maT1
x6YGzCiNOX+UlH+zz18z/mcTt+5r2Ovw5r2Iq5Myt/AFtQgyioq9tBNbs9Ye935xFr64qMazR/sv6OeFL5pq/7D3tjojM8907Epj
VdfsQTGfx/2+IBt3DdjE2Eiqf45sllbrB6a6a1tak9T/vi4tzOp+//vB183z19TmRvBeRJ3/Ghvul2oXGvvNt91b2ajuh99H0u4/
ZP5ZnPsMfGPwndj+a09uXdbJvjP6rLMruPbNdT+2sc45vAxM3M15pPm1jab3wp3j2L3vwvb/GO7ZSESL2jP1VDt5ONfFE126unYo
uHfY9w0UZ67dqHVeu1Yfa8HlinoGs/HsVUyW9V471ubPp65Nt9xnd/L+j1kLS7Dw8Gmwl0QraprDG8tnP9DRR9/qj7ULGttYl7tP
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
r37zL/rqN//i+0feE9j/7FeW87/Uvi3X0mr9gHm2dfe9cf66PfLsgU5TK4L9b8ni1l+KvMbvSrKouaeRts78sSt3NDT5WKeuTevF
pwPBx2edXcxTYyTFX2pd/0q6x5J/y4/1d3/K2v+JdMwZibdvXNfbl883fW2gp1OfdXY1vR9mDfjO9dOpnxWY/6RX5PyFtHMPtj+I
f7wf6suSGmOPfQZparNxBuzYlTs62n9BUmsOTlLw+ZNbl5s+kN7Sav3A0ORjLTx8GnxI0tDk48hYmrMXUiNnd+zKHY3MPGv64H4d
737/+5Ef42+91/L9nP+thn3+y875//K//y31B8o3MvNMx67cCT439wHzmhl3eL4tD89fflw80RWc2b23shF8SApel8ipYX9Jm/8P
+z7Gq2SXFmZDP0Z/+i74niJrAogXtv/T9FqL2gdhf0jSV7fux/43zH0E6ZicxH530Nd/mAMAfhF/v4i/PzwA+0X8/WP88Yv4+0X8
/WH894cGqP6kPQCA6lAAzj/Gf7+e3LrcMvcJa36UdmM6sgmLv70JK2uzVDYg5lNfWlB9aUH/6//836bXiX+1ilz/Ua8hvbBn37AC
BRxCrQ75B7+Iv1/E34+BiUe6N3+/5fUL772r//H5/9Tc4nrwGvfe6lCA0q+4+GcpVEC+Ih/i7xfjj19R8Z+4W/f9o+15SYfgJfL/
VUqKP+uP1SL+/oWN/8xn2oP1Rz8oQOmfWXuR2P/gA/H3y46/yx7/KYBVHdYf/WP9xS/i7xf5N3/inr/cPYgoFw3g/aMBmz9J13/a
8ccuWEkDnmzIv/lF/P0oswEw4096S6v1A0ur9QNu4eGD/b9v+r4s1/+PI5NBcW+EMzGfX2suTmU+n9rcaHoP4uJvGpD/t/FRLZ/9
IPKDBuTRLp7o0r3hs4z/HqQ905I0tz925U7wcbD/94z/KdgF+PI2X0Z14hpAmiaQUnMDbOQXtfckzf7PuNeRHvl/f5j/+Jdm/zmq
w/jjF/H3i/i3X9r9n+w/r07R+m8mz2byn27+DfHi5p72/hP2H7aXvf+Q86ftl3b/J/fecnD+t3pLq/UDIzPPIhuQmyYwRtwagN0E
L6wBPE3I83EbwYQ1oEX1/jI1Hfp6Us6//9xJ3bl+mjWwGL3dta2w+6vxbu2obgy+E3rdn7o2HdkgmNiXz77eFx4+jY2/xHuQhnv/
Nez7sGk4m2f85z1oD9Z/iytr/zPySVt/3nzdxfNXMWnjz9nT6qTZA33n+ulCeWq0ypLXTPt97773flU/7huvt7u29fT596FfM3PP
n28PNb1u5+Ok8Pi/+HRAkvTj9AP9OP1AAz2d+qyTPLSrt7u2lTT3//n2UKZ7gHkmc/NvJjeHdFh/96fo/s+kr6FVmvNCZj1x4m5d
E3frqc6Lsf6YTlnnLyQ1nb1APLMGZtZZ7g2f1Y3Bd4KxxuTdpOYzjUOTj3Xq2rROXZvW5YkFSdH5H/JC6Syt1g8MTT6W/fHk1uXQ
+A1NPg7i/t38k+B19+yR3S8AxaQ5/xt3/vGPtQvt/HHfGPb5L3MGzF17T8v8rpixyXygfPa4IzHOl4nnLz/M+euxjfWmDzOXTFv/
Ael8det+6u+9t7KR/E1IxeTe7ve/H/kx/tZ7LX/PPNNmqZWCaHHxN4rk/8k/JIva/5nWi3/8XWMb65Hjk3l9bGOdXrQZmH0/v/zv
f0v1sRcd9P0DGBwA8Iv4+0X824sHYL+Iv1+mEfC9+fv6H5//z9DvYfypDvH3i/j7RQEgf2iA6k+aDehsbK4WDUj8Y/7vX31pQfWl
Bf2v//N/m16P2ywXNl6RdM7Hjr+7iSRtsSwWYLI7dW1a9aWF4POBD97V//o//7dpEz/xr16W699g/CmP/fxrF0VPu1ka5SH/7xfx
94v4V++bhccHJGn+/cHQD42OSqIAYjvE5Z+Jf/WS8v9sQGwvd/wn/u1FAVy/3Ouf/Ge1og7Bcz23T1z8WX+sHvH3J2z+yfpX+7D+
6EdZBShpgJ3fk1uXExvg0YCkOkXjz/hTjIm/++GOPRTAqk5cQXrWH9uP9Re/iL9f5N/aK+r5yzTAQ3VoAO8fDdj8ibv+acDZHuTf
/CL+ftAA2J+LJ7qCAnxFrn+kt7RaPzC1uaH5tZ0PSZrabPxv1vibIupv37iuty+fr/aH38PyXP9JxRQpoBgvy5kWlMcuwOc2X05b
/G2vFoDzxW28nOTFP/5Ok50SufnONPs/wz7n/F05yP+3F8+/uwvrL+1F/Su/iP/uwv23PdLu/2T/eXWo/+ZX2Nwz7fiT5mtI5t5/
7fonEudPqxYXf86fth/nf8uXpgG5kbYBrWk+LrU2gCc/mo9pBOM2oDVoPFitkSv9mrhbb4mz+Xzibl03xz4MXv9Ff/N9t//cSd25
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
Lc5/W+Rvi/LHFue/Lc5/W+Rvi/xtkb8t8reVNH9JenzrtEbOTnU8x6aQ4eprtcLscKk5qqHQ98y+bujYiVOh2b+sVvROeVSS9OLO
eNviw+9fOyct/8wi0Bk4duJUK//b1a2NU+/euNnK3utfl7cWCX2HtSpT4f7LFvnbov5ji/ztMf7QFvnb4fpri/LfVhbnvyTO/5Sy
nv+I5LKa/4vk0rR/BmHudTrM/82Ha3/W+tZGI37+jZD863++mdfe9Lb9TzY2pFdbm90FcRvAsyHkVhvyk98eabF8KvQ9oweHpHVp
tjqlfeVvJG1vaHpidCR0s9SRs/NtfQHXby1q5Ow89dEe/PLfH4a+dv2//qHf/9u/6/HHR3L8RjtfcbjUXLhwXJI0Nv2w7TX3fByH
z8xpfGac/FNwud88dKj1XGW9obHph23HIOr8139z/mehvlYrFKtTzX3lb9r6dqXtTa3jbjzu3wCVsj++buufhx2n67cWQ+s+0nb9
B+Fof9tZuP+yRf4A0ghrA/K2/cRtp6mv1QqTKjXD2n9o+2mXpP2NvPJD/7st2v93lrD+x6g1mxAu7vnv+l9uvGlzc/0CDvMv0qvV
qyoVy60+F2ezOqVP3zugB882JKmjjc4rbjsdkvHn6s+f3HuTVfvb12/a36bv1VgDPURlvRFY9/e+3vrviP03/WU/4ovqf3f5u3zr
a7XC9L0DTff6p+8d0ANP37wUPf/rT5Im36VmGoX7L3tJ9v/l/gs7XastzmOhshjr3zL+tndx80+ypi3jb7try319+/nZ143W63E/
R0tqBj4PE7tl/Yf9Fr+UDfBskb8t8rcVN39ugPuD/O35K5VBZQ/59w/52yJ/O5T/dugAsMUEDHuUP7a4/7UXp/4jsQFhv8TJf/s9
5J818rcVt/wJM3rimC59972+ZRPOxJJcf1mALHvUf2yRvy3y3znIvz/i1n+4/vZHkvo/gxCzlaT8D8MAxPSyrP8z+Sg56j+2aP+3
R/+7rbj1T/of+4Pz3w7XX1tcf21572udsPN/9P7d0M+5tLRC/0tK9D/aov/RDtdfW+Rvi/xtkb8t6v+2OP9tkb8tyh9bnP+2OP9t
kb8t8rdF/rbI31bS8W/ePviFH1f0NeM+Y3OLDLuFoL2LPktbuUvt7f/1tfCNIt2Cb08nZvr7xXe44nCp6d30NErYuR+2AcDL438M
/Bw2gIyH+y9b5G+L+o8t8rfH+ENb5G+H668tyn9bnP+2Mp7/2I+vuOslG3+LLCU5/5l7nT3m/+ajvtZ9A/iFymLk+p+OqweVimUF
bQLPBvDBTlbvR78uafbNpoGb1SnNnTuq8ZnV0PePnJ3X8/Njkrb7AsbeHpJeKfLfodNK7aX1V9gTxqYfytsXU1lvaGz6oRYuHG89
98t/fxj5Gb+/069vt7sF9YGNHhyS1reOy7XPPsj9O+11m282lQ3bzHqzOiWFbDwutV8DJOn6rUXK/pjirn/u3fz3ZbWifeVvNFmd
Cqz7SNR/kqD9becIu/+SpB8YC9R33P8CSMvbBuQ1+7qRuJ5SX6sVJlVq+utA1H2CxWl/S5LX9VuLgXVPh/GH8dD/aIv2f1tBe+q4
e2CvoPWHF35c0Y2/3pCUvM8YW5Kc//71D6WtY8D6h+mdHv9atXp1qy/L49iJU3rw5jiEzb+QFNpuh+x58/fnvlmdkpR87ay9jva3
/gur+zvee4BL333fdf/TUrFM/b9PvJkH1SeL1am2MVhh878k6crQAU2qxJ4AEbj/shO3/8vh/it7ce+/pOjxh+xBEp/Lpzhcai5U
FuP/m4j9d8g/vjT5S5z/vXK5zA6XUq81nPbfoH92y/oP+61+cdwFuKkA9UdW+SMdzn9bcfPnBrg/yN9enEol+fcP+dsifzuU/3bo
ALBFB7A9yh9b3P/a61b/CeqsRHbiNuoHdVhKbZsQ0gGTAvnbipNZWPboTdzrbxgWIOsN9R9b9H/Z4vzfGci/f7KoM5J/erHa/yMG
IXon4yGZXuufEgMQe5Fh/Z/sU6D+aYv2f3v0v9vqlj/9j/3F+W+H9gdbXH9txc2f/pf+of/RFv2Pdrj+2qL9wRb52yJ/W9T/bXH+
2yJ/W5Q/tjj/bXH+2yJ/W+Rvi/xtkb+tuPn7F6B3fe8sQN9daxFoSd4NeGZfN1qvh/1b/waE6B//cYjaAOB3Vy8rbNtgtxEzC0B3
R/+LLfK3Rf3HFvnbY/yhLfK3w/XXFuW/rV7Pf4kNyHsRN/+oDRjQm7htBGxAkr0453+3DWCQHvN/89Fqgw7YAP7YiVOauDgpKf4G
tK2NU191/i42gG+3WD7V9T0nq/clbW9mOn2vFvn+5+fHJElP55fbnm+1PTc20nzVXW9s+mHbzwsXjkuSJu7+qsNn5vThn3+x+Fq7
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
"""
VIEW_FQ_B64 = """
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
"""
VIEW_BQ_B64 = """
iVBORw0KGgoAAAANSUhEUgAAJAAAAABQCAYAAAABQIiwAAEAAElEQVR4nOz9X2hV177//7+U4CfkSCohSBSxZW0vZCF7b0SknxJE
pPQilFCC9OqL9PgpB+mBH6EXH8KX0IsQPoR9UcKHD62IR+TwvfjuIiGE4sWhBAmhWySUniLBi56gxZ/KJgR3SEMowfW9WBlzjTXX
/P9vrCbPB8jWJNq1x5hzzDHfY4z3+5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALAM9dcaQV9/tbl2qOrPAgAAAAAAAADo
HmHxY9ulU31tf/5m9TGx5RBJ2tMvTaz+4/q5jn+f/ii/3RGPPtg/0vQlfQgAAAAAAAAAAJBd0LoM6y8AAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABwY
h1x/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgKIM9dca5vevNtfIuwgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaMNBdAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBrqrzXM719trpEnMCPTjrePHZMkLW/t6O7ujiTaFQAAAAAAAAAAAAAAAAAAAAAA
AAAAAADQwgF0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAcGOqvNSTp9rFjkqTlrR3d3d2RJL3aXCNfYApD/bWGaUc/0660
KQAAAAAAAAAAAAAAAAAAAAAAAAAAAABAknpcfwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6aof5a4/axY21fGz7aq2H1
anlrR3f7a41Xm2uH3Hw6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD2Lw7zAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABQoaH+
WuP2sWORP7O8taO7uzt6tblG3sAYVbTnUH+tYf+ZfgEAAAAAAAAAAAAAAAAAAAAAAAAAAACA368e1x8AAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAACgWw311xovPxvx/vz1nQeaUq3xanPtkMOPBQAAAAAAAAAAAAAAAAAAAAAAAAAAAADIqMf1BwAAAEC7of5a
I+jrJPoBAAAA9jfeBdyjDwAAwH7EHAcHGdc/AAAAAAAAAAAAAAAAAAAAAKAIQ/21xsvPRiRJz+YfSpJGBnqlDWlKtQb71AEAAAAg
Pc4Cu0X7AwAAAAAAAAAAAAAAAAAAAAAg9bj+AEHY9O8W7Q8ABxfPALdM+1+9MtzxvfmlRe/79Ec5uP4BAMBBxByoO/Au4B594BZj
UfVocxxEXPdu0f5uMMfpDlz/bnD9dweufwAAAAAAAAAAAAAAAAAAACCZT1+/Dvz6Jz291X6QfWB5a0fDR9O1W9ze56H+WuPlZyOS
pGfzD9t+ZmSgV9qQplRrsFcaQF6cxXCHtneHtgeAg4mzwG7R/m4x/wEAAAAAAAAAAAAAAAAAAFGC9hqyz7B69ANwsHTVzR236X93
94gkBqWy0P7dgcMXAFzgGeDeUH+tYbf/0o+PAn9uY3NLu7tH6IsCcf0DAICDiDlQ9+BdwD36wB3GourR5m4R/3eD694t2t8d5jju
cf27w/XvHtd/d2D+CQAAAAAAykb8AQAAAAAAAAAAID/23hZvqL/WuH3sWOj3L68u6szJ83q1uXYoafu//GxEkvRs/qHenrkhPfxR
z+Yftv38/Y0dTe1s01f4XWL91z2eB+7Q9u7Q9gBwcHEW2C3a3x3mPwAAAAAAAAAAAAAAAMD+EXQWg70/AIow1F9rmDONxtd3HnB+
sWL0A3DwdM2NzaZ/t2h/9zh84RaJB3CQ8Qxwzx6Djg8cif15+qI4XP8AAOAgYg7UPXgXcI8+cIexqHq0uTvE/93huneL9neHOY57
XP/ucP27x/XvHvNP99iDAgAHG88BAABwEBB/AOAS710Aqsa4AwAAAAAAysTe23IM9dcat48da/va5dXFtj+fOXleUvuaV1z7Pzw5
EPnfvb+xQ+LWDIjBucX6b3fgeeAObe8ObQ8ABxdngd2i/d1h/gMAAAAA5WLd0S3aHwCA6vDcxUHHPQAAAIBuMdRfa7z8bKTta1/f
ecDZIgC52ePLs/mHbd/jDGN16AfgYOqKm5pN/27R/u5x+MIdEg+4x0KYWzwD3DN98GJ8VF/dWtT09hZ9URGufwAA3OAdwC3mQN2D
dwH36AN3GIuqR5u7Q/zfHa57t2h/d5jjuMf17w7Xv3tc/+4x/3SLPSgAcLDxHHCLNUgAgMTzoCrEH7oD1zsOIt67AFSNcQdoxxwU
AAAAAIrH3tvyDPXXGp/09Gryl+/bvv6gfkWStLy1o7u7O97X07T/w5MDoT9D0tZ0iMG5x/pvdyj6eeCP5dFv4Ypse9o9HeZBALoF
a2DV4yywW7S/O8x/AAAAAKA8rDu6RfsDAFAdnrvdgTVGd7gHAAAA0E2G+muNl5+NSJKezT9s+x7ni8oR9D5GG2M/Cos9SPLONjLO
lCusD/xnS+kHYH9yfkOz6d8t2t89Dl+4Q+IBt1gIc49ngHt2H0jS87kHWlh/o+ntLe9rcU7OLtAXGXD9dwc2pADAwcI7gHvMgboH
7wLu0QfuMBZVjzZ3h/i/O1z3btH+7jDHcY/r3x2uf/e4/t1j/ukWe1C6B2uQ3YF+cI8+qBbPAXdYgwTQrXgWV4vnQXWIP7jH9Y6D
ivcuAFVj3AFamIMCAFAN4soAcPAUtffW/wzh2dEy1F9r/PziBz2oX2n7+vLWju7u7kjK3v7+RK1SM1mrJBK2JkQMzj3Wf7tD0Wcx
hvprjdvHjnl/NmMe/dapyLan3dPhDBKAbsAamBucBXaL9neH+Q8AAAAAlId1R7dofwAAqsNz1z3WGN3iHgAAAECV4s78DvXXGi8/
G5EkPZt/GPhv3N/Y4YxRgew2N76+84A2xr6TNP7w8OQA40wJ0rS/QT8A+0+Py/+4f9P/6OBhaf2opjdSbfpvMChlQ/u713H4YiP+
8MVA/1FtbG5pqL9G2+dg2v7e4jJt7kDcQthA/1FJot1LxDOg+zyfexD5Z9vFXzb16HR/7L9pB/3oqxauf/fiAhLm+7QxAOwfvAO4
xxyoe5XxLoB06IPqMBZVjzZ3h/i/O1z3btH+3YM5TvW4/rsH13/1uP7dY/7pFntQugNrkN2BfnCPPqgezwF3WIME2lEYuDvwLK4e
z4PqEH9wj+u9O/DMrR7vXd2Fe6A6tLU7jDtAC3NQAFVjDuQefVA94soAcDAVtfdWkuzExV/feaAp8X5mvNpcO3Tm5PnGJz29Gj7a
K0la3trR3d0dSbnbvy1Jq0Gi1mSIwblX1Ppv0DsE/ZRc0WcxhvprjdvHjrV9f/hor7Ql3eUealNk29Pu6RQ5D7LRzgDSYA2sO3AW
2C3avzqcwQYAAAAOJvZhlcvfvqw7usG6LwAA1eG56x5rjG5xDwAAAKAqSc/8mvNcz+Yf6u2ZG9LDH/Vs/mHbz48M9Eob4qxXAYb6
aw27zQ3aGPtNmvjDuy829EVvX6Wfb79L2/5B50sB7A89rj+AwaZ/t2j/6nH4wh0Sz7vFQlj34Rng3le3FjU6eFgL62+8r9m/95vs
Oxr5fXOfmaQQy1s7uktyv0BFXf/+jb60czg2pABwiYMvbvAO0H14B3BrqL/WeDE+qpOzC4W/CyA9+sAdxqLq0ebVIf7fPbju3aL9
3WGO4x7Xvztc/+5x/VeP+adb7EHpDqxBdgf6wT36oHo8B9xhDbJ7sA7vHoWBuwfP4urxPKgO8Qf3uN7d45nrBu9d3YN7oDq0tVuM
O0ALc1C3iLu5Rx9UizmQe/SBG8SVAQBSvr23/sTFJC0Odnd3R9oK/l5Re5/vb+xk/HQHDzE494pa/5Va+a0Mk+eKfkov73g01F9r
+PvDGD7aK22JvgmRp+1p93zytL3d7ow92RADxUHFGlh3yHsWmNyf+dD+7nAGGwAAANj/2IdVLruw8omv7kti3dEV1n0BAKgOz133
WGN0i3sAAAAAVUlz5vfEV/f18OSAJOnZxM3qPuQBNNRfa/jP0Nk4T1eOoL3mtG+5ssQfpjjSWJgs7f/uiw3vWQBgf+lx/QEkNv27
RgE89zh8UR0Sz7vFQlj34Rnghn8sOjm7IK03g3HT282MQTO/bWh394ie3Pmo4++fvT6vnp7f9v7Ufg8FJYQYPtqrYfWSpMAn6Pq/
+MumJvuOBv582PXvb3PaORwbUroDiTdwEHHwxR3eAboP7wDu+N8DHp3u18VfNtveBXp6fsv8LoBkynwfQ3JFvY8hOcZ/d4j/u8N1
7xbrv+68GB/NPcdhM10+RYw/3APZFHH9S7R/Hlz/7jH/rBZ7ULoDa5DdgX5wjz6oHs8Bd1iD7A6sw3cHCgN3D57F1eN54A7xh+rl
vd4lnsl58cx1g/eu7sE9UB3a2i3Gne7HeZjq8M7lDnE39+iD6jEHco8+cIO4MgBAyr/39tn8Q709c0Nvq5XAmKTFnWZG39HEwtOO
rxd99mhqZ5t3hRjE4LpPnvVff44rqZnnSlsi91JKRZzFC+oPxOMcqjtFtj1jTzrEQLsHa1/VYw2sOxRxFpjcn9nR/u6QgwMAAADY
/9iHVS67wO+Jr+5LYt3RFdZ9u1cRcWdiEADQXXjuuscao1vcA92NfQ8AXGMcAlCkLGd+332xoYcnByr5fAdF2Ngutc7R6eGP3jk6
g/N0xbLXZIyv7zygfUuUJ/6wu0sdzbzytP+7Lzb0RW9fJZ8TQHV6XH8ANv27VUYBSNo+HQ5fuEPi+WqxENY9hvprDdPm/mdAT89v
qYugIh27/b+6tShJenS6Xxd/2fR+pqfnt9A+kKQndz7S2evzktrH/bhEHCQpaDe9vdV2/U/2HdX09pamt7dSFQH2tzntHIwNKe6R
eAMHFQdf3OEdoHvwDuCe3QdSKwbhfxeQlOldAMnEvY+ZdwL6oHxFvI8hnbA2l5RqHYDrPh3i/+6w/uUW679u2HOdPHMcqTMBN30Q
L+q9S0o//nAPpGO3vz3PyTLHp/2zK+r5S/tnx/zTLfaguMEaZHegH9yjD9zjOVAd1iC7A+vw3YHCwN2DZ3H1eB64U2T8gfZPpqDr
nTXfHHjmdgfeu9zhHqgObd1dGHe6C+dhqsU7lzvE3dyjD6rHHMg9+sAN4soAACPvmS9JejZxs+PnSFrc8mpz7dDEghr3xy94XxuZ
XSlk7zPyIQbnXt713zDkXornj8ExHrlR9DlIpFPEPMjG2JMMMdDuwNqXG6yBuRd2Fl5Kl3+V3J/52c/dR6f7tbD+JjTnj0T7FyXv
/Ifz1wAAAEB3Yx9WuexCs/6ivqw7ViOs6DLt3x2KiDubn7GLOlPQOb2we4U2BFAEnrvVY42xu3APdA/2PQBwjXEIQNHynPl998WG
Hp4cqORz7mdxY/uJr+5Lkh4GnKNDscLWZDivWB7iD24VlesTwP7S4+o/XFQBNjb9Z1NU+0ti838OFEB1p6zEA0iGhTB37PH/+dyD
joOPklIVQQ369/1fY0xqsdv/q1uLkppj/6j6NdnX/iyIM3fjnGa/XdM3q61/++cXP0iSHtSvFPzJ9yfvOSy1xpn1o6F9EFcE2Mac
tB0BIfdIvIGDioMv3SPvOwDFv7Ir8h0A6fnnQeY9YHTwsKRmLMLE444PHNHG5m8h/1KL/10g7r9tO8j3T9T7mJ2IxiQEipK0DxAu
z/sYssnT5ubdl/hzeiRfqh7rX26x/utO0FzHjPdJ17fMHOfaFslv8/jq1mKh449E+6dhxxvMPD8Jc/0vPe+M+9P+8cLG/7RJPyWu
/zzYf+IWe1DcYA2yO9AP7tEH7vEccId9iG6wDt8dKAzcPXgWu8fzoFpFrX8Re8gmz/V++9gx2j0Dnrndgfcud7gHqkNbdxfGne7C
eRi3eOeqDnE39+iD6jEHco8+cIO4cvejAA+AKvnPfJkYQ5K9tySHzmZkdkVFnH0xOX6Ma5KmTp4v62PvO0ExuIu/bHr5l/yIwRXH
3v/v33/e0/Nbqv3nyCbsHJidA8Kcd09zFuPy6mJo3rHlrZ1iPvw+lPccDLJpG4eUfh4UlvcN0YiBdgfWvroDa2DV8+fAktqfvUmY
s8AK+HHOosaz+8BIc23T/vkEzX8kpc79Y9Dm0YjzAwAAoGrsw6qOXWhWYu9/Fcz1bYr9SvIKLdP+3aGIuLNd0Flq3WsUdE4urkC5
+X6SdvTHNmj7dIgNYb/iuesea4xu5b0HeL4Wh30PAFxjHAJQtILO/HLOK4c0Y/u7LzZo6xLZsWL/moxEzLgKxB/cytP+3BPA/tLj
+gOYg6dStgJsbPpPL+jgr9TaDJREWAFI2j4ZCqC6FVT4Lm3ieWTHYrAb/o2f0l5gSPISn6Q9+PjNaud/wz8umSIBEi8SQc/f6e0t
PTrdr1Njl6Vbi5rebm7I3dj8LeJf6vx3peYz4UH9ii6vJnuWH2SXTvVp6fm2pNb8c2H9jUYHD3sB07PX5wOfB2HXP5LzByBOzi6E
Bn0ICBWDxBvdgw2f1eLgS/coYjOcv/iXxL0Tp4x3gNqrN8QcUvAnPbHfA0bVioOa94As/35YX/gPzUjS13ceHNiFz7D3MUk6NXY5
cUw06N9Ne2jmILa/Lep9LA5jUTZFtLlZhyH+nJ4/Cbckki9VJO/6I+tf+bD+645/zlkk+iCcmW/6Y/9S9PuvLWz8MWj/cPZ8325v
s/aSRljyZ9o/Gf/+k6gNiTau/3zYf+Je0B4USRS/qBib0rsD/eAefeDG9PYWzwEHiliDZJ6THuvw3YHCwN2LZ3H12JdevTxFaO34
A7GH9Iq43mn3dHjmdgfib+5wD1SHtu4OUUWvJcYdVzgP4xbvXNUh7uYefVA95kDu0QfdgbhydymyAA8AxPGf+TLicp5I1tmLiFew
+xs7RX7cfSnv2Zf1C+9LarX11M42z4iEovK/TW9vEYMrkR0HfT73QI9O9+viL5ttP5N1/zmSCTvzPqr+zDkgrm0d8XKOXV5d1IP6
lbafW95qjlN3d3cYp/b480BISvW+5W97f5sbpu0R7Pncg7ZzMElEnUFFNGKg3YG1r+7APnS3/Hmwsvj09WvmoznY78NJ88+gGPb8
J2vuHxt7QjsR5wcAAIAL7MMqX1COZYNcD+Xyt71d7JczX92hiLizv6Dz2zM39LZa/U1B53hpCpTHxZj9953JKS8R04hDbKh7UJOn
HP55D/U2q8U5OzeKPPcb9HxlXEqPfQ8AXGMcAlA2zvxWL8vY/u6LDT08OVDJ5ztITF+c+Op+29dp6+oQf3CL9gdg63HxHw0qgCdl
K8CG7PztXxQ2/0cLOnwttQ5DJsHhi/zsxANpE8/TrtlFJd+QWAwuS1TSB3PtT283D2JvbP4W+u/E/TeCDkEOH+3VsHq1vLVzoMcl
/9xHap//2F/f2Ez/XPa3fVhSCBJCSB/XzzXGP6xp6eZj7+VYam1USXoANeyaR7SggMRk31HvmWwS0djfIyCRD4k3ugMbPqvHwZfu
UcRBDH/xL+aX8ap4B0C0sPiPPw5q+kFK/y7wSU9v4H3gPzRjHPTDMv5+mLtxTmN77wXma62xJ5mwPjDM88j0x0E/MGO/j9na3sdi
khNL0fFP+3DHQWxjv6La3Eb8ORl/Eu6F9TckX6qAP+lq0euPtH+0stsf4cLanoR71Yja+xC1KRfFK2v/A6KF3QP2Ggyq4d9/8nzu
QTMmGnNPMP/Mzr7+7X0P5h0grACJxB6UorEpujvQD+7RB260JYcQz4Eq5U1KExfjRyfW4bsTh4TdMu8FJ2cXeBY7QpKy6hRShNYX
fyD2kBznMNzjmVs9ew3MPgNmrv2kxWcZX4rBPVAd2tqNuKLXPT2/Me44wHkYtyjIUB3ibu7RB+4xB3KPPnCDuHJ3KbIADwDECTrz
Zcb4IvffTu1sE6vwGZldUZFnX+5vNPP40NbJ2HE4/95bSZF7n4nB5Rd09n108HDbnrckzPrv5UfB+a0kclyFCcsB8eh0f0fugbQ5
IB7Ur+jyavPftHOPmb64u7vDvRPAPoeR5SxYUJsbtH2wj+vnGmb/ie3U2GWN7p2DSXPuHckQA+0OrH11hyLWwNiHnl7QOVQ7Dxaq
Z+ad0xvNvkB5wuY/5j5AcYjzAwAAoBuwD6tcdo5liVwPZQvLb/3uiw0F5VzizFf1iog723mcTT8/m7jZ8fcOel7zKFkKlIfFJoLu
u5GBXo2oV/c3dmj/CMSGugM1ecrlrXOJeptV45ydG/Y8Je/cM+j5ytwmPfY9AHCNcQhA2co683ttbVlTJ88X8hn3mzxj+7svNvTw
5EAln3O/i4vpvPtiQ5K89uadqlj2WSN//KGn5zfiDxUh/gPAr8f1B5je3tLVK8O6t7js+qMcKPahF9P+X1F8s1IUIHRrYf2NJvuO
en9Ok3j+m9XW1+xFHonFyiTsBLgsBpfLf+A6PulDtvFoqL/W+PnFD5IUmpSDAg2d477Z0GZ/3STfiFoclqTVRz+Hfs9OxmEjIUQn
/6FHUwgmyTPh9rFjgYk3EM1fbMdsLjeHsP2boglI5EPije7Ahk/3OPjiRlHFd24fOxb4M8wvg5X9DkC7p2PH2sLeA/zyvAtInYc0
3p65IT388cBvKH21uXZoWq0YzqvNtUOz3/Y1pFbfFPE+ZrP7Qmr2BwdmWsymFcO8nyV5Hwtixj/T5l/feaApcaAjComAyhOUhFtK
F3dAPqx3uUX7u+Fv956e39picVL4OoyUfI6DYEHrvtwL1bL7wBTftPuA679c/v0nSz8+0vRG+xiEcgQlvkU17PinpLbDwEmxByWf
qE3pEpuiq+CPR9MP1aMPuocpCp9G0HPA8D8PJJ4JQfxJaSQlLgLmrUGy7pUZ6/DumHnQydkFCgM75H8Oe/siOCxZqbDkrBL70otW
VRFaRPOfw5CUfv6DTHjmumXin+a6T9q2Ue9dSId7oDpBbX3xl83Q2DNtXYywotem3dMWvTbjDjGeZILaycZ5GLfynAOQ2vuXvkiG
uJt79EH1mG+6Rx+4QRK47lJkAR4ASMs+Z5f3jB2i/bS27v0+aL+/F39IGA+6v9HM4zO1s13MBzwggtqe2H/5guKgZszJM78Pyr1E
jqtg/r3/Uus94NTY5bavZ80DZ+cdu7y6qOnT70miL/zCzgL4z74n4W9zcz9wHyRjjz9Z2t/PtDui+WOeZu+VpI54JzHQ4pALzr2w
XFiSvDOpqXJhsQ89sbBnr50HK64PpPizwDwHksn6Tma3/6evX3fsSaT94wXNd06NXdbo3APiQAUgzg8AABAtbL8u86FisQ/LjaJz
PaCTyWn99swNnbj2vxQU67HP98ah/bMLGs/zxp2lZi7nXyenpfn3i/y4B0KeAuX+2ERcXnmEIzbUHajJU55Lp/q09Ly5R82e92St
t4nk7HUuc7bO/n3SNUau9/TC9rulmXdKrXtAkvTun/W2dOBrtiQVFktg3wMAV9h/BaAK/jrL9ntAkjO/gyvfVfRJ94eCxnY9PDlQ
3oc8ANLEdN59seG1N+9UxTNrXvYeZym6pinxh/yKiv+gfOx7QNV6XP2H7Q3/80uLkijAVhV/wev5pUUdH2hOUA3av1z+Anj3Fpcp
AlmBsINfXtHlDP+efehoeWuHQ3gJLKy/aUs8zGJwOYIWIaXwpA9GmoOPZuJKQYB49rPXHiPsrzeDb/HJ9kwfzH67pomrdS3Nrmh5
a0fDR3vbfo6EEMG+WX18SJI3D/IvyvuLYtvs6z8o8YaNQ6idzOFqO9lV3KYIAkLFIfmwG2z4dI+DL24EzUUzb4ajZnliVbwDIDl/
/C3sPUBqLk6ahcoo9rvAta0jWlb7nNM+pGEOzTybuJn3/8q+4X++frP6+NDH9XONpefbmd7HgvrA8B+YQZP9Phb07hX1nIgai+z2
lpptPjLQqxH16v7GzoFe6LfbPG0SpqA2//T168I+20FlkuKiPPb6i4lFsP5YHdrfDf/8snk4rxmPS5J43p7jLD3f1rVjwfMiYp7B
7PY3ByOD2p7rvzydfcD1X6Wg/ScD/Ud1fOCItwcl7/VP+0dj/4k7/nb2rvuQtcY47EFJzh8L5VB89cLWAbIWAaYf0qMP3DPxZcPE
2vIWH/E/DySeCX52UhqzD3Fh/U2itvevQQ4f7aX4Qgasw7vhP6DqjfvWIeGent8oDFwyfz9IrX1YHJZ04/ncg7Z96UmwL704rH1V
y5zDmN7eyjz/IdaW3ovx0WaxuxyJOZCevwBqEQVokY4de+AeqE5YIqDp7S3auiRRRa/N748PHNHG5m+h/0bYv0uMJ57/vK+fKTjL
eRh3zBzUm3uuH41dizdz0GtbrXGJ6z+ZoLjbxV82Q997ibsVj9inG3mTISI9f5zTP+eXRKy5InZc2Zy9C5v/S8SVy1JkAR6Uh6R8
2G/85+xG1e/lX4pbA0iy9/b+BusBfq821w5NLLSfsws7+xLFbv+pneb+lbkb5zR283HRH3lfunSqT9PPW7EF88xNmvsQ2UQVQzo1
dlm6tejdD1mQ4yo5u/2l5tg01F9r2F83Mek0OSDs3GMP6le8vFiTv3yvMyfP0xcB8pwF8Le99q7/y6uLXtsvn36P+yDEN6uPA6/7
JO0fNQ9i/EkmKAZqngdf3VrsiEkTAy1HnrUv837MdZ6OPR+y93yaeFwS7EPPJiwfVtLiPIZ9FvjyurTk+z7PgWSCcl7Z+ejD5p+0
fz4mx9X08875Tlw8Ii4OxJ7QJuL8AAAA4cxcyS7aacwvLRJrKJh/L5zEPqwifX3nQbOYrKT/ebj9faioXA9o8ef5laQT1/6XgmI9
krx1R5Qn6PxFEWcuXn420sxjLmlw5TutX3g/8O+xF6VTQQXKG2bd2HzN5DL355WnoHYwYkPdgZo85fm4fq4x/mFNS9b+NOY+1Yha
50q635DcJtmE7XeT1LHfbXc32bvUs/mHUkC9EJ6vwcLO/nLmF0C3YBzqPpz7wn7h5RpTe73NJGd+H54cCIytEVdLJu/YPrjynSTp
2t6vMyfPM8dPIEtM590XG3p4cqCSz3cQBL1/Zd3jTPwhH3/85/ncg1R5lvbODKME7HvoLgdp7t/j4j9aVAE2O/mbjc3n8czF3CxC
0jp0sbG5FRmQpv3zCyqAZx94kSgAWaaiCrAFJWHlEF44/wuBN96vH2UxuET29R6V9KG5uTN+MdJ+BkxcrWtpdkXmPjCJH+yEHGgX
Ni6Yrw/11xobm9FzIX8h2qXZFd0fv6CR2RVpS14ijunT72nyl+/bnskciGwxhyCXnm9794ZZlLcDofbz2D8HspOd+K97DqF2MnP+
4wNH9PeN5oZyu/ivETQHCgoI+V/YaOdoJB92gw2f7gUV3pE4+FKlsEIYaTbDIZ0y3wGubR1JFPPhOd0S9f/d/l7ad4GgvrAPRiU5
NIMms+hVRB8Ypi9MP2j+fb09c0N6+KN3gOYgb+iNeh+z1wei3sfstrev/WfzD/X2zA29LdHWlrZEQHv8be6fFwWtA3z6+rXsA5hf
33mgKbF4GcROwh10GCPqfYv4fz6sP7pF+7tlj8UmjjbUX2uYd9ywdzC77f86ellf33mgT1+/VlAhQomYZxjTJt+sttbfe3p+82I9
Sdffl55v69ox7oEs7D6QuP6rFrT/ZKD/aGwMKMn1T/tHK3v/CWNPOH/bX70yrKUfHwWufyXBHpRs/Ieys22KLvtT7j9RBbHtwwFJ
1gLoh2zog+5j4j3+gmxnr8+nKkgV9DyQeCbYgpLSdOxFzND2iGePPf51eIoxl8uf+E1qLz5iCgMbUcW/KAycXVA/mOew2Qe9sP7G
ux9MMbY4PIuzMeuNtrzPYUSz17/8vCK0Ie1uxx8+ff267Xuf9PQW/VH3HXO9Zyl850esLR0z//nq1mLbfCdtYg6kF3b+KGtCPvaz
peePPeS5B2jvdPyJgCRFxjtp63zssd4wRa/t/T1xewuD/l1iPPGG+msNU0A2KvES52GqF/QsNmcBsuL6T8Zf+MWflMn/7CXuVizO
ILnDHKha/nH++dyDjlizfd46CH1QHBNXToO4cjZhicSMIgrw5P+UCEJSPuxn9jm7U2OXvffjqHUve+/tnUfLbf+e/yzp1M4290YA
L0ePws++hM2D7Pa/NfVBx9eRzNyNcxq7+djbeytJcXv/kV1YHFRqrr34zz9GvQtI7de7ybVkco5J0vLp91iPDGHvP7fbx/561jxw
du6x5a0drx/8/y00+c8CSK08rOYsQJJngb/t7Xxk3AfRgq57+3kc1P5B8yAzDrEfIpmrV4Y1vbjcsf9zYf1NW1Hm/+v/tOaV/hgo
72D55V37un3smJa3dnSXvsjEv+8T5YoqzGl/LY79DLi83vl9ngPpBOW86ulJdhb7L296dV/tZ05p/2T8uX+ae823IuMR/mv/0532
M/C0fZN/nz9xfgAAgJah/lrDXms36zLGQH8zTkQu9OIEFQae3t5iH1YBXm2uHZpSrTGi8POInDEth8nta/jXHa9eGda9xeXEsR7k
5z9/UcSZi/UL73sFsoPymZsi5exFCZenQLmJb3j5zOfJJ58UsaHuQE2e6pgxX2LuU6WgdS5UIyjPJKoVNKfhzG/3CTsvwzMW+xXj
UHfh3Bf2i+b5omZeQztuk+Sdy5z5VcBQQ1wtmaCx/eIvm6Hnr/1ju4ltmrimaXdEyxPTeffFhh6eHNC1tWVNnTxfyefdj+x9tvb7
F3OX6vjP3RH/6T7se+geB3Hu3+PqP5y3AFvQxnOJzedpZS1yvfR8W3deLHsHHw3aP5mgAnjHB9IVgKQAanr+Q9fmxSDu0K/Unngg
LAmrRCLKKP5NV1kTzyMZ//UelvTh1ebaoSzPgImUn4exKZ6dGCiIvxCtJH1954FGZlc0M/qOJhaeSlY3nvEFMhiT2tlzIH+bRx1+
tAvQ2kk3Lq8u6kH9CnOhAHbxtUt/vtj2whuXCDSI/zlskhHQ3sGCkg9TeK18bPh0yw5I2wmIzbVPAuJyBSX8f3S63yu+k9anrztj
PxLzyyBlvgPYMYiweY59UMD4+s4DTYnndJiP6+cakvTXe5/rxLvTid4Frm0d6Zhz2pvqns0/lOZbh2b8WGBul7UPDPt+CLoHjGcT
N4v+6L9rdnJiu83jkvFFXf/mUCBtHSzsHThJm0vN57G5tk1bjwz0akS9ur+xw1gfwJ98SWq9A4e9jxH/L0be9UfWv/Jh/bd7mHlO
0pjzX9706tn8Q40M9Eob7e9itH86Wdff/zp6WV/feRD4HkwfpJdmzYXrvzhFX/+0fzJF7D+x178M2j/eq8017/12fmnR2+SZZP2L
PSj52RuiSQZUnajk20GFYFA8+qB7fLP6uC0+b/dDVCImKbjoV9TzQOKZEMfsAc1biBzxvrq12LbvJG0xZiTn33sidRYeMYWBp7e3
9ooABL8H2ygMnJ5/H4Q/OeWo+r1DkqYv4MbC+hsK85TIP/8xop7B/vhDx56SnWbCA+Y30UwRVCndGZggxHrSsd+7jg8c0d83fkt8
ML71zH1Me2cU9Y6bJv7GvvNs/HOe7PdAWZ9wfzGJgL66tdiWCEiKTwZEW2cTlXzD7Hm237Wyjjt+xHhavL3NEeO9F4OwzsP09Pym
md82QvuE8zDFseOcSeKecbj+o/n3F5qkY6ODh73Yg/9ZQNytGPYzwY59cgapfP5kiAvrbxLHd5gDZRO01ig155wmCWLSpGT0QXZm
r4lh2px1rvL44/x+pvBangI8KAdJ+bDfDfXXGhNX61qaXen4XtC8yL/u8k/Tk22F9uwzpdckkueG+GltXffHL3h/npA0MruiNGdf
bk19UPrn3K/21k0aktr23krpYv9Ixx8HNWdz/WthcftOwvafT59+T5O/fO/luuKZHC6sbeyz6mnOYkxcrUuS7o9f0Mjsipd7jHXh
eP72MW3f05PsWRDW9sun36P9Ewq77uPOvi893/byvpncb7R7MvNLizo+0Mx/ZfhjQf72t2Og9nk7Yv3p2LEJfy44SanXvoaP9mpY
vfRFQkFrw/a+T5TPbvuguWgU/1ng+9rR1M62fn7xQ/Pvn35PEvOfLLLkIrBdXl2k/VMKO4MdN//5y5teaUBtZ+A5/xvMH9c38X/D
jusT5wcAAPudOQN2b3E5caFO1t3zsXOhp8E+rHTub+xoZKBXf3nTq3e13fH9JHsQWXfM7uHJAb37YqPta0GxZ9Z9y+M/b1fkmYv1
C6185oMr33UUy6ZIebigAuVRMWh/gXKpmc/818lpSe3tbyOvfDT2gLpBTZ7y2futzDqXaee4uQ/P3fzIdeiO3fb2GWwbew7LFXSt
c+a3u5jnsH3mwphfWvS+z3MW+0lQLU4p/f4rFINzX9gv7DrLhondpMlpaOLX9p8leXn2ECxojmnyDkxvbyUa2+1YGjG0ZAqK6ehn
SV/09lG3LoOgvA/2mGPet1A+4j/di30P3eOgzv17XH8AqZWgZnf3SPJN/76N5xLFp7L6uH6ukabItSm+Zg5b0/7ZtYpdNweXKBRA
LYZdgG1jc6stCUTYYoz/4G9UElYE8xKy7kmTeD5sIcxfQIBrvlNUm9jfS1ME1TwDRvYSCC1v7TSTr4awi5IzNiWzu3tEl071BV77
pg9MEiZTjHZi4amkZhsbtHUyWa7/T1+/ltScA5lkEFLzICrJIJKLm/sECSp4RwLoeHkKr9Gm+bHhs1pBAWmzGJMUB1+KYQef/Qn/
02yG+6K3j+LvKcS9AzQTb6SLA13bar6/2XN7v6H+WsMu0uafr7LA1snE4wzz/I16F7i2daTt+peabR9VvIEDM+Gy9oHUeT/4++HZ
/ENpvnlwKejQDIv9TWnex/zXP9dwNmna/M6jZUnSg/oV7/vP5h/q7Zkb0sMf2xJEI1gr/r/d1uZxyZeI/xeH9S+3WP91zxSIiYs5
+xPumXn8p69f6+cXPxDzzCht7PnZ/MO2tuceyM4e/7n+q5dl/A+6/rn208u6/8Re/2LsSc/f7vYelDD+PShIz78HRWruQ7GTAaE8
/uLvczfOaezm47aN6hwOKBd90N1MYqYw9nPATt59+9gxXV5dbIvHoZOdlCboMEzUurD9XuBff0Qy/qJff9/4LfFavFmHr716wx6f
BPyFaP1jv114xPRHGZ/B/vNB7zP/mGPvuwrqiyx745DcN6uPD/mvUal1f0RJk6CJ+yC5oOeB//3X7Cvp2FNCcoJI9vynOc9vH/OT
7sH69PVrfdITvucfnS6d6tP08+Z4fvXKsJZ+fET8oQL+eZCdlC+poL1vBvvOk/HH37gHymUnArLnM1mSAdmYy8TzFxmUmu2WNgGH
f96zZBUSIP4QLSjeH8S8g5ki5FF70TkPU5wsRU9JipuN2WMiNc+AGSZR2ejgYS9h1tnr823Xf+v8y2Ou9wyC5p/mXFfa2CdnkNIJ
SoYodSak91/zyM5f5FpqPWPNHNTEODc2WWt04dTYZY3OPeDaL1HU2d4iCvCgWCTl6z5BazMS715F8e83CZoX2fP/of5a4+s7D9oS
Q9vnSK+tLVf+/+H34NXm2qGJBTXujw+2ff3++AWNzK4k2vt8a+qD0j/nfsfe22rZMTh7zPbH5rLuPzdrkGdOnueZkFMzD4QSn0Wa
uFr3vv7T2rpmRt/xcpDRF+mlOQe29HxbE9b37LaXaP800l73f3nTq/u9e3tArbxvnH2JZ8eh7Xesjc2t2BxAZh6qvUcF6+7p+HNh
2bngzO+Trn2Rey+9oHUAqRmL061F7+xFlsKQUXmY0BK0Lm/PRV8+nMx0FtiY/OV75qIZtJ7B6XIR+PMl0f7pZcrB4cP532BBcf5H
p/ubY/7e9y/+sumtyRPnBwAA+5ldsPOrW4ua3og/g8q6e3Zmni8196bkPQeAcK821w5NqdbQhtrWyu25fdwZ06BcDwjn35cgSQ9P
Dni//5+Hd2TWfY8PHPVizmFo/3yizl9kPXMhtffz+oVmLm2pmdP832vNQp7kMu9kx59Pzi60FSiXpJnfNkL7wV+g3PC3vz+fuURf
2EwfnJxdYA9ol6AmT3nsHOd2zZeo8xdRz13Onibjf/bOLy3q+MDRtnPWadcYkYx/z9s3q813L5P7QZK3zhsmbr3FoF5IsLizv5z5
dW+ov9a4emXY+/PSj4/avm/25hLvwX706HS/Lv6yKSn9/ivuheJw7gv7lX2+K+2Z96mdbWmj82tP7nyk1Uc/a+ymuAcCmPwO9tgu
KbLd7bHdjlkb5DVMJ09MJyiGiXhBtZb9eYaNLHuckVyR8R/mOsVi30P3OMhz/x7XH8AsDNwfvyBJGpldSXzoguJrxTnx7rSk+EMX
dvHBEfXq/sYO7V8QCqBWxy6ck7fwHZJ7tbnmLQb7k2+ETUb9ha+X9h6+puiRsby1w+HTjMzhOynZwTu7AOfUzrbu7u5IW81DwA/2
DsRfXl3U9On3vL97d7c5PtE/4fzzIUmaudeZ8dM8h212f9DG6aS5/sPmQLePHdP06fe8A6gS17qfXXxkfmmxbfxPExDyj/02EhGE
8yefJ/lwtdjw6Y4/IG1+H7cRKwwbEZPxJ4MOKngXJ+79l3ff7D6un2v89d7n3p/NQmTUHMgUQIpq96H+WuPnFz/oVzUX1N6euaG3
FVCwTTyn7bHEHND7x2orYb23OPztWsffvfNo2XvPMu9Y/nlU2IEZqbWB9KC/N9iHI8P6QJL+5Yv/6Pi7dx4t60H9Stv9IDX7NUti
9YPWF/5nqT0enXh3OnIsuvOomXDYH38e6q81Xn42ol8np6X54AV9Nk93jj0mQV+S8V9qPoNNMU5JejZxs+3nGeeTIf7vDutfbrD+
61ZQvFkKjjn/5U2v3p65IT38sS32bPqBmGc2dh/EXf/+uD/3QD7m3ffEu9Oxay5c/+XIOv5Lndc/iT+zSzP/tNd/7SIMjD3J5d2D
woGAbOw9KGYNsnkIOD4BfdSmdNYDovk3pL/aXDs0+21fQ0p3GFtKdjiA/uhUdR9I9EMaPT2/eQWZgwTthZOaxRhMEZLLq4t6UL9S
0Sf+fTJJaUxCDrsQrbkP/Nd+XAEqxLt0qk+mza9eGdbSj490fOBI4kNJhllfQTz/np+g9XdTjFmKL8SWhlmDMb6+8+BArwMEJaWx
28J8r/ke1lpj4bCkG+b+mOzrPLSdJjlo2H0gMR/yj09S5zPYX/jOtGXoHugDPMYkkbcIqimAd9D2KRRh7sY5jd183PY1E3dLug9x
vxxArZJ/nDHFrIPGHz/72rf3PtjYd57MpVN9Gv+wlvseQHr+BKxaP5o4GZDBubt4ZRS9tuc9kjiHmlDYdWnWAOKSPgQx52GWnrfH
UnN8zAPLjkfESfIcRqeP6+ca4x/WtHTzsa5eGdb04rL3vbiYs415Z3pBSbGk5rM4ydwT5VlYf0Pxo5L4z3uZ9177zFeRsWYEW3q+
LbvouGEnBg1DXDm7qLHdJHu2C/D09PyWqQAPikFSvu5i+sMuEGDMLy1636fd0xnqrzXMfluz59xfhNB/Ltu/xmUSQ9vF9sxZOvbg
ppdk7/+tqQ8cfLL9KffeW9YXUwlrK/N1sxaZZf+52QdNfxQj6Vmky+vN8xr3xy/op7V1SdLEwlP6ISP7LFKSHHz3ezvbX+I+yMrk
fEjS9lL72aNPOHeXiB2HvvTnix0Fv1Aefx4mqVWoJE2OMbP2JUJ3qYStAwTF5qIErYF9+vp1MR9ynwtbl5ea+1KSngU2OWck6Zqk
qZPn23Iw8RxIJ+wc9k9r682xxsd/DnhqZ1uf9PRqmudwJnnOYBsm7y1t3+KttVtxfi+np2994P/6P80cVcT5y+E/h2hwvQIAUB17
vV1qFUed3thK/E58cnaBdZic0hYFRnKvNtcOTanWuLayLO3lB5Pa886fGrvc8S4gpTtfilZbjyg8H4OJ25w5eT7V2QvaPzt7fC7i
zMWtqQ+audCt/Sd2TvNra8vEIQL448/eHkS19iNG5RmwC5T7+XPKG+TXbvHPd7wC8VZsSBJ7QCtGTZ7ymbPW/q8Hnb+Ieu5y9jQd
//6qjc0tHR846uU6DMPcJz//NWnvOQzb52b49xz685z4kYcjmL9Niph/UgOvGOZ5cG9xmXMWODDs9zCp+R4gUYvTFc59dR/W6vOx
6yz74/txZ97tfT9BMR/WBqI166dta2H9jRdXS5pfw9tbu/coIH6WTVBM5+Ivm5rsC+4DYjr5Be1vNvvLzRqXyTNscm2H8ee9QjZF
xH/MeQ2kEzaHMdj34N5Bn/v3uPyPBxUfNIcZwzb9+wuwUXwtn6A+iDx08e6f24q42zh4kR4FUN0yxa6zFr4LSr5qCjEjWNbkG3bh
6ym1LwRLJODOy/8cCDr4+Nf/NR74/J3a2W4W5dnrzst7P28X6qFP4gUVY564WpfUfDbYhS+iitGSoCa5tEWAw+ZAZtxn82G0vMVH
TECI5OfJmcQbpuiCeclNW3gN2b0YH9XJ2YWOw8BhBQclNnzm5V9s9weks/x75vdBGxEl5jm2oPZ/tbnWthnUPgwTpOMdYI+/ADnv
vsnZ7W+ep/9YbQX5zVj0L1/8R8fftZOfhMUcvIJ305P6dXJakvRs4maB/w/2Dzshq9SMv514d7rteWAW4Wuv3jTfc/eYor/mPSvo
GeIt4vsStkpqHtqoDR/4DaT+OJzpA0mB/fBJT29bP0jNvvh0Lw4dNpf6+s6DjkNLgyvfaf3C+wdysT8s/mxf/971GxCTtovABI1D
ZuwxbWwz7X2Qr/2gsWdi4akkafzDWuA6gGnzB/Ur+vT169BinIhH/N8t1r/cYf3XvaB4s9SMOZtnwcvPRrz2jpvD0/7p+O8B87+B
ay97B8G4B4oRFveXOtdcuP7L4Z9/Rl3/QeO/1H790/7ppJ1/Rq3/Slz/WaTZg2KeAXF7UBCtqDVIg8QEyQQdijdjUPP6j1/jiktO
YGLb9Eewovsg6IBG3DoZ/dBiFwPY3T3SKsis9jhy6F64vWfvg/oVbz0gCPsS29nXvb0PMSh2TwGq4phCwDYz94k6lGR7+dkIhdgS
sAte2F8zvzff84/7UYngpGSFgb01YKnzfeEA91vU/+9Xm2u55qUka8rOX7DZPIfNHq2wZ3HcAdWw+2BEvbq/sXNg7wUT+xmZXWn7
+qVTfRr/sCapfZwxbc0e6GLt7h5JlQzXXwCPdk7OTswxv7TYNr6neeZ+0dtHu6fgnweZdrO/HrYH0V9wzS62RuwtvaLuAcSz21pq
JUYxopL/B7W1P84pce4uTFTRaxN3MPGeIP45Zti7lL0GQIwnmaIK0drtzvWfjP9MgOEfm/z898OSmu9dPIPTM+e/7Hm/iTlL4fuX
mXemE5YUyxZ3/gX52HOgNPMfiflmVkGFlme/7fMSUkryEsEx5y+fP7Z5fOBI8+xvRFJK4srZBa27BElzL9jJWHn+ZkNSvt+Hof5a
4+qVYe/P/vczEzPaL4n4quLfb2vYyW8vnerT9POttj/72WdKbWYvBNKL2vt8a+qDwL/D3Ci7tDE4/95b3oOLYe9BT3P+Uercf47s
gs4ijcyuBJ67tvcfjsyuaGb0HU0sPGVemlHqHGRqXfu0fz5B51Cl6DN4hj3+0PbZxe0/QT5D/bXGZN/RwBi0XZyBOHQ54tYB/PG5
MP69KJLacnBI8vZFS8SJggS1SdRZ4KXn2/r5xQ+J/m1yQKQX1fZ/rA1qYuFpZPtfkzS1d/ad9k8v7RnsMJy/7jS/tKjjA0fb8qz6
13+l9vV24vzFMjF/O55szC8tet+nrQHgYKHYrHvP5x5E/tl28ZdNr2g20vlm9fGhoOv91NjlyDaXWGvM6tXm2qEzJ897+w8NE2cL
iv2w9yq7+xs7HXmupb1c13senhzQuy82Eq370v7FKOrMhRSy/6Q2rGtry8QhAoTFnyf7jnYUyo5iCpTfmvpAZ6/Pt+UzNwZXvtO/
11rv2qyNdZ55MX3w6HS/Lv6y6X3drL+wB7Rcdn/4a/JI0sxvG6H9QE2e7JKcvzBjjP3ctees9nlHzp4mk7XmJnOf4pn6R0nP/QY9
Y5FekfNP5GPG8xfjo/rq1qKmN7a8M6lhBvqPst8f+0ZcvA3FC4v1c+6rO7BWXxw7v60d30+S88fOa0hd4OTsOaZ9tldKV2vZrgVo
zrY8ufORVh/9rLGbYryJEFRn+dHpfi2sv+nI42n4Yzp2+zPfTMceZ6Tm2qK9xpUm/mDuJeSTNf5za+oD1n0zCMtxZZycXZDEvgeX
7BiEdDDn/j2u/sNhh+6k5qb/P9YGUxcg/D13hAthfRDU/lIz8aS//Sm+ll1YAVQpeQE8ij9mlybxQFjhO38BNpOAlYNIySRNvhFW
+JpkxPmFPQcmrta9AqhS8PgvtR+Cv7u7d/0zHqUWlpzJL2kxWsRLUwRYip4DUQgsuawBib+OXva+/vWdBxRAzeDqlWFv80Pawmv2
AprZyGJ/n2s/mikmJakVzFk/GngoWGLDZ1HsALT/sEuaBMTmOeAfe4aP9mpYvRQCCBCW3CRJ0pO2sd/3DiaRgCkL/zzzp7V1nXh3
WlL7wqQZdz7p6W2+V+2xC83633PN88CeLw1ONg8FrF94v6T/R79fQXP+P9YGNTOqjmT0XkK+LXn9YeI+cQvKHQdmasNtSRMP8r0T
9P77x9qg7o83Y6CmH85en/d+Jks/2H0wMtAs/nht73tmwfkgvUNExZ/N9S+12tR+HzNj0vLWjpZPvxc4Dr38bESantSvk82xzR6D
7PY+CG0dJGzsMdf92M3HXrFm+7qv9bxpex5Iansm+9mbKdBC/N8t1r/cYf3Xvbh48x9rg5KeVvZ5Dpqoe8DMdaRW/Jl7oHhBcX9U
I2r88a+9sOZVjrTzz7j1X6STag9KSPL5oDUwCgHHy7MGaSfZljqL0LIPJbms/XB5XVrytW9QgXKJ/ohTxL1g2nWov9YwCbsf1K+0
/V36oZ2/UKT9HBj/sNbxLEi6F+7y6mJb27MvsZN59krJ9yGG7QNl7pOMXYx5fmnRK+QopVuHpxBbclFt82pzbe+QcPNgnt0fYZIk
CPLWXxS9NoB2H9fPec+C3d0jqQ5LpknWFJQI4aDdQ3Zbmz2gQfyHhv2H5KPazX8fhK3fHLQxzI79+PeiTCw8DSw6aJ7VEnug8/LH
nkdmV1Kfw0A2rcQc2Z65dvHNgzZu5BHUTvY4FBd/W3q+rSVth+4BRXJ57wESUyZnJwKa3t7yEqMYQcmfg9razBk/ff3a+zmu/fSC
nr1x407Yu5Qd//mkp/lsJsaTXdZCtMQ10/Pv/w8amwz/O1fYM5h1r2BFxd0O6vtqHvZ1Hlb0N00fID0zB5p+nmz+IzHfzMs/Ptjz
0GasIf7MKX2Qn3+NUWrOc3p6WuORf+yh3fMLez6aeyAu4XmQVnGM3B/vwCEp3++DiTPcW1ymKEAFvHOlkmZG39HEwlPN3TgnqZWE
dTZgPcbOTWCY82II99Pa+t7ZimBLz7dTJd0eu/mYeE9K/n23u7tHMu295T04H38sNO35R4m+KELQWSR/3qsgpu0nFp4yBmUUloOM
9i9f3Bm8jvNH7GXLpag4tEG8PxkTAzL5x+x5epI8TEnQF/Hs4ssmf579tSh2TO7Oo2U9qF/Rp69fdzwjRgZ6NaJmfhnmRMmFnQW+
P35BZ06e1xe9fR2FOO3cJib3LdIr4hw2+x7SizuD7Z//+NnXP23f7tKpPi09b/7ejmNubG7FznWI8xdjqL/WsIsJ+ov+mvknMWQA
ODgoNtsdvrq1qNHBw237sML2ZEnNHOpR30d6pg/CsB8oHxPrMTGehycH9D8P78g7k6HmnN+OcZo1d+alyb3aXDs0pVrD5Fg2Ble+
835vcgA/PDmgd19sRK77onxZz1wE7T+ZIg9rJDvWfPXKsKYXlzWqbPvX/PnM1y+8791n19aWyUm8x9536D8LMKp+Tfa1CpUnQWwo
H39/2DV5zO+j4nPU5MnGrEH6xxv/XN7sOZTU+Gb18SE7h4bEues8zDw0Sa4H5vnlMWsDcXNPM5+9trIc+m9dU3Peg2yyzj+RXFC+
KfMMHh083KyBt7GlqPMZtpOzC7wTFyyojyTmOEWy555m3hMVd0Nxws5/ce6rO7BWXzzz/uT/+sL6m45xxz/3D3seIBm7zrI5bx23
78ew8wmnOQuGJn9MJ44d0/mit09Ssw+e3PlIq49+1thNMd5ECJrX+Nl7npPEH25NfUDek4KlbX+kN9TfPGchRc8h2ffQPQ7q3L/H
9QeIYhffRLGiDj4adgFIDj4WK679sxTAY4KaTprEA1GF78xiJEV2kkuTeNtfdEeKLn6HdOKeA1Ly8Z/rHr83SQ+fJrkHuP7TMRsh
EhVfG70sSR3Fc3gGxCsq8YadeHtK7cU2l7d2SIAewZ9oI2kwhw2f2ZigdFCCjaRt7x9/4sYeCgG08ycfNm1y6VSfpp83+yNJ8euw
dzCkE5Tw4Y+1Qd0fH9RPa+s6e33eWwyz38+0tXdta68AjLXh0F4othfSzL1iHwyw2ckjDqKo5Bt/rA1qZlReW9pxCtMfd3d3Ui0O
+5OzMj7Fx+HsfrB/Jms/2IdmJHmHZIyD0idJ2t0ek4La/u7r+PHj2fxDab554G9w5bvWOFQb1tROdPHO/Sxq7JFa1/3Yzceh130a
B7mtgxD/d4v1r+7H+m/1TCEASbkT8iE/Owk0qmHfA8B+FZf8U+qcf6JYSfegmNizvwBGUByafSjp7e4eSbwG+Wz+YXuSbeuwho21
gOQ+rp9rSEq8FvyXN73SgNoKvwz1t69HIr006/F/edPr3QumHySKwqdlrt2sRZDangH1K7q82lpntosy8DxoCSt4lGUNkgJU6bQK
ATcPRtp7UcJ0jP17aPtivHw4qRPvTscmQ0mSIMhO2BQ1Z6XP2plCYFJzT+LLz0Z04qv7iZ7FSZM1mbV6f0zJ7Oc6KP1hxn/jxLvT
bWu4Z6/Pe0Uhxz+sdTwTZr9dU+3VGy1F/DfMffDr5LSXdJQ9LPH7Hsy678TCU0mt+dCEksXmDvq+kjhBc5+ke7BQDLv4bJpnLn1Q
HP84FPXeZZ4V9ryG/ef5ZL0Hlp5vU5whJTuhj70P2p9E2yQ8kdrnlUHzRjsRK7HOZMKevVL4uBP1LiVZ71N7cWjaP17RhWgl4v1p
2Gcy/DE4qbMYhtQa+8OewZ/0NOdGxDmDFRl3QzJB51/MM8A8h3t6ftPu7pHQf4Ok3MUwbWf6w7S7fz4k0eZlseeTRcSakYx5Hpqx
x97v4J/r0O7l+bh+rjH+YU1LNx/r0p8vdiS5RTlIyvf7YOIM5tz29MZWW/HsIAP9R0kKnUDUusv98Qv6aW3d+3P94hmtPvpZ4x/W
IhNChz07EOzV5tqhiQU17o8P5v63aOtsgmJwn/T0anjrSGDRx7i9twdp3bxIUWfwspx/RHZRZyHZ+1++qBxktH95oq57zt6VI28c
+tpW+/sA8f5kTCz61ebaodlv+7wYqD8OnWXtizNH8ew1r+Y5i+b7mL2nLUlhSHP9f/r6deTaMPPT/Oy+mdrZll1Y3uwztM9/0c7F
sdv+32vDXrvb7L2etL0b5PbpRJzfPROvvLe4TAwZACCJYrOu2QUjT84uSOvN9p7e3lJPz2+a+W0jNBZx9vq8dSYy+rmOYGafgzG9
vaVRBRe1Yz9Qsb7o7Wu+tw42z13/Y/Wx/uWL/+hYezRr7zOj72higQK0Sb3aXDs0pVpDG9K1teW275lzuFIzdvBFb5+mnm9LAeu+
9vlg5FfGmQv7vNLYzcfEISIE1cGQktfCCOLPZ27yakvE42x27ZegOiTT2819bhubwbkeUAx73mnfD5N9Rzv2fUahJk92dhvbdWDM
n+3C7/5cMlJnzkPO3SU31F9rJFljHP+wJkkN5vvF885SW3N/PzP3R3HKmH8inv3MNU7OLkjqPIsRdTbj4i+benQ6OEaB7Mx4ZMdD
jfmlRXJtlMBc50FxN8ahcgWNMZz7cou1+nKFxftHBw9L60d19vq8904rNfsjrqZd/eIZzUkau0ls2ihqjhn2c7R5PDvWdnzgiKY3
trz1xSje9b/e3NNm+oA2jxYWUzN5ze3+SBp/QHlo/3J5OX989d5tk31Hm+sA7HuolH2G/cX4qE7OLhzouX+P6w/gF5TgmQOQ1fG3
Pwcg3eEAannCkqFkLXzHAcjk0iTeDiu6g/JQANWdn9bW9wqPZyvGTPGL/CiCXQ07AVBc8ZG/jl5u/uHdP+tthW8GktqL3qElb+IN
0wdhxS/YiBXMHAYeu/lYkrwFrumNzsTDUfwJ+GjjcP5NJ3ZA2v5aVPLtoMK/NgrAJBN1nSYteor8ohKASs3iazOjzUBzUHEwbTXf
b5OMVV/fedCRsGNw5TvvAI6dPIVxLJgphudn+iNJPxj2vIr2Tqfofpi7cc6bC9AX0YLaPqjNVx/9rLGbatuo6B+D1i+8r8GV7yQx
7iRht73/ndj+86+T09L8+x1/XyIekQfx/+qx/uUW67/V8seb7QJISdcBGOOLxT1QLXMPmHa37wEzT4/C9V8c1rzcov2rk3QPiqRE
BTAury5q+vR7ktiHkpTdB3FrkH9509ux/ojiJF0LttcD7CTnt48d0+XVRT2oXwn891mfjPZx/Zy3Nra7eyRxH0idRcij0A/t0u5F
TLof7vLqopZPv6e7u83nM23dElT4xRTBCzoAwxpksUxBwd3dI0pTCPiv/2u8rciFRKGLLOx9EHaiQ7swsF/aRKAUbUvG9IXph3+s
NmMOv05O6+H8Q737YiPyWZykL7ykQ5+N6NfJaf2q9mSYB+keCio8+NPaus5en29bV7x97Ji0FXwgsvbqTeQ7lklc9uvktKT2vQ+I
14xJP5XUnP+k3YfL+m567MGqhj3fN++7SZ659EFxovbCTVyt66e1dU0sPG1LiuKPxUnte0A/6aF/ksp6D1zbOqJrx5r7dZe3dogh
JOSPc9r7nu05T9Ac3547StFnL5CdiffYY8/S3vpj0ncp7oXkii5Ei2S8BCnqXGOMisEtPd+OfAaTeD6a/7xdmrgbc8/s/Nej3Qdh
cx7D7oOl59skY83JzIPsfQ5Be8klCh6Vxe6DomLNSMaOe8ats6M6cc9i5ENSvu5n5jbm3LZJTjy9sSV/AYEwJ2cXiAflMLHw1LvO
7b3PSRJCI7+050kpepdO0Nqvfb79mprvuctbO7q7u5Np3xUA5EEOPnf8bc9e/+LZa4tp4tD2mgt53tIzc0V77aun57e9ojrJY9FB
a1+cOQpnr3k1CzBsd+S+Muu+UngBSNPu5pyXxD7bIoWdBTbail2rueZo8vlw7ecTlotAarW7nc+HHGLlYO5ZHuL81bBjyV/dWtT0
xhaFBQHggKPYbPd4PvdAj0736+Ivm21fjyqW+uTOR833AbEPLi1775W/8PjC+pu2gsBP7nzEPqwCmfzzZp/yJfV537s19UHHz5u2
N3m5JxYoQJvUq821Q1OqNa7t/dl/9taOHQTle7s/fkETMjE52r0oec9c+O8T8z3ib9GC4s/zS4s6PnA0cR2SoH2i5u+Y57H938v/
qfcHu+2lZvubejDT2822Pz4QnwcFxbELlV+9MqzpxeWO+RCKZ98LLx9OerlOwgSd95I4e5pF25n3e6u6NfWB/uWL/+j4uVtTH4SO
9cjH9MHMvVX97e686hfPRM79jX+vDXfU05HIvZpW3vkn78DZPZ970Pbnr24tanTwsBbW33hfs3/vN9l3NPL7SG+ov9a4emXY+/PS
j4/avm/uD2KgxbKv41NjlzvujSCMQ/l9FXD+i3NfbrFWXy7zzhUU77eZ+Nrqo58lzv9mVnSME8mE1Vk+PnDEi3EmOVtnrwkgGfu5
amotS+3xHrv+son9BMUfwvY+Iz/avxr+mH+Y9vj/b+x7KIk/t4Dh7T05oHP/HtcfgOJr3cNfAHLMl3wS5aP4ozt5Dr5M/vK9zpw8
z4M5h7CCR2lwKDgb+/Apz2A3Lp3q2+uDp5KUuhgzByKzC7v+7SKcKI4/EVNU8ZG/jl6WtDcPCngmBBVhIBlBsKyJN9r6YA+bsNK7
emXYW2Q3QQRTiCGOPQ59fefBgSjWlUfQYm/U123+a//Z/EO9PXMjtPgg90ByQUn4DPMOIOV7D0A2f6wN6v74YOD37u7uJFoY8wLV
VsKO9Qvva3Dlu7Z3Beap7UlPkkqbJJRDMuVI0w/2hl76IbuwNq9fPKMnF8/sxSzUCBqD7m/sSLVhxp0UgtZl7FjEy89G9KuaBU6l
9oOWxCPSI/7vDutf1WP91x0Tb24mF3ja9lytXzyjOSm2Dxjj8+MecMck75Sedswr6xfPSAnaX+L6zyrq2k+zHk/7ZxOWdDXt2hft
X54088+7u81nAX0Rz18EPm4N8tn8w44k28T/80uzFvyXN70d6zB2H/ws6fLqoh7Ur1T2+fcT/7pM0j6QOvsB1Vve2tHy6fe854DE
s8DPP+7bzFxoYuGpVxgsbg2S96/07D5IWgj4L296KXJRAP/1/9Pauk68Oy1J+vnFDzpz8nxkYeCl59uR//bLz0b06+S0NP9+6M+h
yS6sufroZ514d7otDjG48p33LL1+cbjj749/WJOkhr2vK+y/5X+XC5tH7fd9RUF7T0ySVZP4Vmo+S4eP9npFdy6vNvcNnTl5Xkt7
f8+0d1h7mX0PUrMvwxKRoiUqFvTzix+k6cnQv0t75uNf22Xtq3xmnhn1zP3Lm87kbyheUMx56fl2WyLK0OfmXmLv/fzsLELQ+1eS
e8A8hz99/brj36PNk0vS1oaXMCJBIlZz9gLZ+MeeJGu/yMe8C4zMrsQm4I4rgIp0ksTgTLJ6SamewYhmrvmkcTcUw577pOmDpefb
3vri8taO7sbEHdApqO2j5kAkWS1e2j5Accw6uxG1zk4SuHLsjSkNSZpfWmxLDhqV/E0KL8CDZEjK133C1qv8CdGjEqRf/GVTj05T
vCeJsPOmP62te783+85JglueoH7Iep4U+Zm5qPZCQHd3d8j740CWHHys+RbDfxYD1fLnIPMX1UQ5ws4g0f7l8M/5d3ePJIqB3nm0
7O3rN3k+yfOWXdZccHceLUtSR18g2qvNtUNRua9M7qWf1tbbCpEbI7MrqvU0i/YwPy1e1Flgw/9cfnLnI97FcjIFk8JyEUjtOcVs
Uzvbe/0m9gBlFHYGWGrOgX6dnNZgyJbba5KmTp4v/0P+zhDnd8df7GV08LC0flTTG1sdBWDCnJxdYDwBgH2EYrPuDfXXGkGF2BbW
33hr73Hmbpzb26NVxifcn/znLk6NXZZ8hTtNITyJguNlmbtxTvWLZwKLb4Yx51MnFnjPTerV5tqhMyfPNyTpi96+9jzA6iz0a+cQ
Hpld0f3xC7R7CbKeuQgrjE0+7WRMGy09rzWa5yqaBcqPDzTnN1F1SOL6oRU7ZR9cELtN9uYsDalZA4bYULVM/Rf/XHNh/Y2Lj3Mg
XTrVl/hnk9Te4expem/Vz+nWlOtPcTBNXK1r5t6qbl08E/uzrzbXDk2p1rBrWUjk3s4q674H3oGz89dcm+w72hZvmN7eUk/Pb5r5
bSN0DnT2+ry1T4jz13mZWOi9xWVioBXwxz2TxjolxqEixJ3/4txXdfx7QFmrzy7oDF1Qe9jvt5dO9Wn6+Vbbn8Pia0gv6xwTxbDr
LG9sbqmnJ3mdZc49puN/rvrHHvNns/5o5xsIGnOIcZaD9q9W2JzEnAGIe+cKwr6H9PzvXc/nHnhzodHBw3p0ul8Xf9mUdPDm/j2u
/sP2pv+o4mtJEskTAM3OPvzo3wyRpPgdh6/zofijO1HF79K2/ZmT5xmDcigi6QCHgrMxhYApgNodwvohrviFRD+kZc9Do65/CoBV
Y+Jq3fu9nRAlbRFU7oF4SRNv/HX0cvOL7/5Zb0uhm7BuHzum4aO90pZ0l4ViT5GHgQ9asa6swoLS9teTJCA2hX8lJSo+SDKU7Ej+
1p3SJKY0ghJ2XJN0bW1ZZ/YSRhz0ccu8d82MKjApa5Cgvnirfk7/WO18T7PHNA7JRAtLjBsmSz9wQKZTmnZP0ubmEJ8UPAbxftwS
1/ZB7W0fkjTXsylqOrjynVfs1HyN9o5G/N8t1r/cYP23O5iDu0Hz+6T3AO2fDfeAWyYuF5dsO0n7Iz3z/ht27T+5eCY2CTfP3+zs
+IN//Yu1Lzfy7INgD0oxzBqkWX98+dlIqvVHg7WAZMISopt+GJldaeuDJOswQeiPcGGJ6bP2wYP6FV1eXdTl1UWvUACS8T8D0iT6
v7vbvMZ5DmST9fnL+1dy/kSUSdbhKUJeDH/bS3Zyyad6UL+i28eO6fKjRV2/ONzx95eeb+vSqb7IA0i/Tk5Laq4HmHUAG+8MTUP9
tYb/nWtOrcJT/14b9hL+DK585xXekeStoS/tvaOZQ+BhiVPMM+TZ/EOvmEPWedTvWdD1b5j74Oz1+baCkMNHm30wffo93d3d6Wjj
5lpNc3/Xq821Q/4D+esX3vfWxQz7HjiIz46wtceoNUdzX5iCJEFji3Qw2zML//kXKV3xO8bx7IKu/6Xn21JAEoiguQ9tXzz/2GPW
4O1npxT93GTcyc48l+0EBca1reZh+U9fv257H/76zgNN7WyTmCylqLZeer4tqTWntK//qESsPHeT84//YWNPEjwLsrHfBcx8P8l5
GHssspGEuBh2DM4uFiAlewYjGeJu1QqKPSTpg2tbR3TtWCtZ0PDRXg2rV8tbO5yzyyFqDoRqxPUByW7LN3G13rnuRaLh0ph9n6YA
j30eOAwJoItBUr7uEVQI8uTsgr66tajRwcNtCYujivNM9h2leE8CYedNf1pbl9TaA3r2+jxJcEv0anPt0MSCGnY/pDljbZ8nZe5f
HDvOYGTZ94l0ws7g2fsW4hB7zifoLAZrwNWJOocXhfbPJ+oMUhK0fzr+GKg5Y7G7eyQ2BipJl1ebhcSW9/ZiMebnY957k+aCM/0g
Nfti+vR7ksi5V6Q/1gZ1f7x9bdgw+/sNzuYVI+lZYIkCMWV5+XBSJ96dDv1+UN88ufMRBUtyiDoDbNj70G33N3Z0bW254+toIs7v
3vO5B21/Pjm7IEl6dLq/42cv/rIZ+HUAwO+b2c9MsVl37DVf+9nM+m31vrq16P3+/viFtnoLl071eQVpmYcW59Xm2qGxm2qYHLUo
lxmrp1Rr+PMAh8VxzDnskdkV3R+/YJ2PF2N/TlnPXFCcvBgm3j9xta4JNa/xNAXK4woGc38kQ2zIDbv+y6VTfVp6vq35pUUdH2i+
BxhpavIgm7/dnW/mmfSx2zfpeS/WH8vBuepyhdUMMexcMlM72221LLyvIbOk+x543mbnr8Vmm95uPnOPDxzRxuZvkfXw7PVfxqR8
7FjoV7cWNb2xFXv2ZaD/qDY2t3gm5GTH3Yyo+CfjUHH81y3nvqrnP/dl1uT9a/X+P9tYq28a6q81bh871va1sLwA5ll76VRfIfE0
3oPjmXyQSeaY4x/WvDUXpFdknWWkw3wQiPdx/Vxj/MOalm4+1qU/X9TSj49cf6R9zb/fxH7Pmt7e0qj6tbD+RpN9R735URL7Ze7f
4/oDmIOPUezk2WFJn5FOXPFBg+KD5aD4o1tJi9/Foe2zCSt8LWVLPGCKe7EQXC0OmZbvrfo5SfOSWsUvDOZD5eMZXB37sPvM6DuJ
/o49BjH+x7M34cYlH/7r6GVJexuxSIaVWd4Nn38dvdyR7MErvCAW5IMEtYm/0GmSQhhJMQdNx1+AKmsBDJ69yYUVXgsTlJgybtOi
4Y/tTe0VLaSvmuwYkD8paxpBfWEnCZVo8zBF9YEU3w/0QUuZ174tSUKngygoCXEce9w3MdKv7zzwkgOZWMTgyncaXPlO19Qa89GO
+L9brH91B9Z/3flm9fGhpefbjaBr3x7riTmXK+ge8L9jhd0DrL/kF1TwgvavRpLxP2784fmbXVzieeY/5QrbB5E0/mmPP/RBfv4C
MEkLkPixFpCd3Qf+gqlJXV5d1IP6lY6v0x/umXsDLXbyvaBnQNJE/1zbyfjXwYKevx1FUZFbUBFsKXodPmjvA9ILa3vJrAE81fLW
joaP9upB/Yquqb3ozpm9WP7S820vgYQ93gz11xovPxuRpieb7w1qvjcHvS8f9HeGof5aR9ztrfo51SWZ5KBnr89LG819PusX3m9r
Oyl9IRJzD61feL8tnoEWu/iOVxBy71zY3d2dwDavXzyjJxfP7D2vW0Vk7LUxY3DlO/17bVhSqx8P2n2QZe3R+KfpST2bf+itMRrE
pJPzr72HFX4h9lMOfyHmsMKncXMe2j6fqP2HUvs5MOaf1Qh65zIJbj59/dqLx5n+8PZAkwgxVtDez4mr9USx56SJWBEtaN9b1NhD
AexyBL0Lm/l+1HmYO4+aBe/OnDzf1jdf33lwYOfzWSWJwY3dfKyR2ZXM6zDoZLe7944bkHjsL2+Ciz6iWFGxT7vgstScA6E4YeeO
Lp3qc/ehDqCl59uZz38hnzxn75CefQY1bQEeEkAXj6R8btmJnr1EfOvN8/EmKd/MbxuhSVzPXp+3ijikT+R9UPhjDzazBpBkLzTy
s9fAwtZfgnCetBz+2EOWHGRIJ8kZvF8npyPXdumD4rx8OKkT7063fS1oD4Mfsed87MT1WdD++USdQWIPRHGC1lzMfitv/3NAHNrE
QB/Ur3h7EdnHn58/F1bc2lft1RvpaHs/TP7yvc6cPE9flCBqXf7lZyOMTSXg/de9qPZPu+cZ8cLmP2/Vz+nJnfZ96IZ572Lsj2bi
9UP9tQZx/mp9dWtRo4OH24q+PDrdLPhy8ZdNTfa152Cd7DsaWYgT2dmFrG2MHThouBfco9isW6YI9ujgYe9r09tbCiuUimJ5+z4V
nGPD5D5nH1w5zFz/b3fnm3v9Q74vNeNAWfOgoOnV5tqhKbWeu3FxhPrFM5oTbV+krGcuwoqVU7Q5HX+8X2q1f5IC5UH9wH6U7L5Z
fXxoqL/W2N09wh7QCpnr9JtVc080a/IcHziqjc0t7e6G7yGkH4oxcbWumXurGpfa5j9xNY9QnCRzz+bagKgvVZKgPrDb/8mdj7x1
36BaFq3v00dJpd33wDifn31tmvY/PpB+r/7cjXN7fVLoxzsQ/HHnF+PNQwCjg4el9aOa3tjyvhbn5OwC400O09tb3ruXiYVOb28x
DlWIc19u2WsuQWv1UWvxrNU3x3OTG8k2fLRX2pLu9jfrwvrjbjP3VrX66OfYuX8U4j7p7O4eSRTjHJf0L1/8BzHPjPLWWQ5rd+Tj
H4OSxB6AgyIu/o/szPuVYXIKSK055vT2VqZ4xO9dj+sPEFR8yt7wbxI+Gx2Jy/eSaSO7rMXvkF+e4o/Ip4jid0jPJECPKrycxNTO
tn5+8YOmT78niUPBWfmT70npCgBzyLQYQf0gKXIuZD8brkma2ivSg+Tirn+JZ3BZ4gqgpkmALnGIJq2o5MPmEECaTVgUdwyXdcOn
2Qj39swN6eGPbf3hFcBQjQX5HOxCGFnd3W1e+/RDtCQFqEwBDN7BipOn8JotSTIUeyGH+yFcUFLWsL75aW090b/J4nw6afpAoh+K
EpWQOM/45GdvoqYfWuzngRFVEM8/7nsb0n3JgewCp7R3NOL/7hH7cYf13+5kX/92HxBzLl7QPRDW/pI62p8kfMWj/cv3zerjQ0vP
txtBa15hzwDGn2LFPX+lzmcuc6BiRO2DSBP/5D0ru7j1Ryl98XezBsZ+lOTsfrD7IG3xXzs5vY11yWT890MadjGe5a0dXQ74Ge6N
TuY5wDOgGqa9zTpYUKyzfvGMnlw8E1sIjAJUxTJ7TtKgD4rhJQXd2jtErOZ4vXz6PW9vQ2eh4GbhKnvseTb/0Buv7Pc11gWiRa2v
GGafW9p900GF3AZXvmt7lzso95GZ4yRhJ8qNe082zwzzs/ba2PqF97374Nra8oGPGQWtPQbNgcKK79jXbVtMiPWAxKIK3xkd6y0W
Ym/ZRO17MNj3Vi7zDnB/PHj+j+r5+8HE4C6vLurMyfNeHMgfj2MPdLywvZ9x775pYm9IrvXsjZ7zUAC7WlHnYUwh2qCxyBuDdtLH
Lw6iLDE4kkHn4593+tvdjPdx7Uz8phz+2Kc/ud+nr1+3PY+/vvNAUzvbGupn3pNF2JgzJ8W+F6M40f1AYvOimPOn9tdo++rZyefT
FOAhAXS1SMpXPn9yPsNO0tfT85t2d4+ExujswhiMV9HsdwBbVPwzyXlfieStabX2f3YKWvfiPGl+SedAUrI1GN6FixEUA5XmJcXv
P6cPinHi3em2fjDP1RH1hv8lFCIs9xvrwOULOwMTN/6w9pJcUPFf2x9rg14uIPvnRmZXVOtpFXoxexEZ7/MJKwYsBa99efmx9l7L
lsm5mkvcHsSke9LN2OSfEzE2FSfu/Zd4abmSxh+Q3l5MuSF1voOZdg/ahy6x1yENU4iNOH91pre3pPWj3u/9RQP/r//T/sw8e33e
Woc5eMVgymBibVevdO7Ln19a9L7Pc7M6/vinQR+Ui3uhO1Bs1o2h/lrjxfhoW8HrUfV3/FzUWq/EOmNR/PE4sxbpz4HC/sJivdpc
OzR2U40ndz7Sv3zxHxqX2oqh+gvSmjwoM6PvOPm8+4V5B0t61svEdWj7/Ey8OUhU3DmuIDN7IZLzx/sNswcxSYHyIPRBNvaaGHtA
q/dx/Zz3Hpy2Jg/9kM9Pa+uauFrXzL1Vjfu+Z2oepcH4k47d9lFzT0msbZUkqA+C2t+fVwbZpd33YAuKm3JPpPNx/Vxj/MOalm4+
1qU/X9TSj49cf6QDwcTejJOzC5Kk53MP2n7O/2fbxV829eh0Z7wOyfnPu9j5xZKOQygX577KZ98Hk31HO9bqJWnmt43QtYCDvlY/
1F9r+PMD2IaP9kpb0t2AOUuaub+fHR8i7hPPjvHM3FvV7LdrHT8TF+M0OP+VjInNDPXXGmliOnE/g2LkGX+Qjf/8xd/uzre1veG/
1rn2i2Xvt51fWtRA/1Hve+x7KN6rzbVD02qfA73aXDtk4hAmz8/xgeYc8qDN/Xtc/seDDmNL7Rv+/YnL7cN319aWOfxbgqTF7ySR
cDunPMUfJdH+GYUVH0xa/JcDdtmZJDRZir1InW1vipPwHCgOBYC7T9RcSCIRSpF4BperPRFZePE7KTrxs/0s4NrPzkvwUACSQgTL
suHzr6OXvev/2cTN2H+fds/GX3g2aQJoxp/sTBGMuE1tUUWoePamE1R4LSwRzU9r65n+GyxUpvfy4aROvDstSV5RMLtf7L5YffRz
7OINbZ9eXB9I9EPRwhIS+9vftHtYm0dh4SyceR6YP4cVJAwTlRyI6z4e8f/uQ/tXg/Xf3we7D4g5FyvsHrDF3QMoF+1fvbBngH8N
nvbPLsnzN2j+w/pvcVqFgFvYg1KNVgGe6PXHKHYfLG+1fs8aWHJh/ZBlDdh2eXVR03uJ6iX6JE4r/tneD2nWw0xS6Lu7O5rc+5p9
X5jv0Q/Rkj4DkJ6/EHacXyenNTjZ+jMFqMrhL3qRdtyhD/LzEhJY52Du7u4ErtGbxDTNfmquIQS9K5ux69rass6cPE8/pWAXN7W/
ZgsqFhn4b2yorW9sByWeZ+9/iCrAY5sZfSewUGdcYZKOtbHasDc/2s9tnJR/7TGIv43944vUHGNYD0gnqvCL4Y/92Ii95Re2/+3J
nY905uR5/fzih9C/S9wtHxP7DCv++1b9nE68O93sg+nJzn/AQhwuv7CCd3OSzpw8r5efjUhqxoHenrkhPfyxbWwaGeiVNqQpsQc6
TJK5j38u+evkdGy8ges/nbhnr3/OE1bk0WDOUxxzBiboLMC1Y0c6xqK2v8sYlFjaGFwcxqDkzLwzqN39sU4/5p3lCIt9miR/n75+
3THueOMNhThTC5v3SxT0rRL94A5tXz1/Ij4pWQEeCo6Uh6R8bgQl55Oayfj+vvGb9/uNzeBz8ra5G+f27pPiP+d+Y969ikyyypnf
9KLyYIWtLdK+xfhpbT0yBirNS+o878Xeq2ItPd+OjIGy/9y9qPwbtH/5aP/yxJ2BiRp/rknsZyvQH2uDuj/efCbbuchMfk+D9s4v
rBiw1MwFF8QuVmXQF+n4172S7kEMYuai9phk9sJJrAtnlSXHDLCfBe1Dlxj/kxrqrzUunerT0nNFxvlRjJ6e37S7e8QrJiip7fdB
MQf7Gue6zm+ov9a4eqWVH8lf7Ness2xsbpG7tgLmPdfuE2N+adH7Pv1QPO4Ft+wC2CdnF9qKzfb0/Eax2ZL5C5CbZ/GpscsdRbGj
2LnR2RORXti6V9j5C//5Xj/GqexWH/2sW1Mf6F+++A+N+75nF0Ft7cVKdhYe0dLEd2j76oycPy5JmljozMfkx76rdIL2Hdruj1/Q
T2vruQqUIzl/f7AHtFof1881TM2jtDV56Id8WnkfmuP8v3zxH23fX3q+zbnTCkxcrWvm3mrg3POv9z739kBwFqA8QX3gb38Uw+y1
jdr38NPauiYWnmruxjlJrTWZof5awz6LZxCrK8bG5lb8DyG353MPvN9/dWtRo4OHtbD+xvua/Xu/yb6jkd9HtLDzLv7xyH8e4NKp
PuacJeDclxth94G9Pm/W78P64CCv1dtzkTCXVxd1WdJw/YqWt3ba3nOlvTHm27XIuLOffcZLOnjtXoTxD2uhseeoMYXzddns7h5J
FNMZ/7AWuf+Kdi9WlvEHxbBjDvZYZN8Pdh9w7Rerde63+d5rzzvDEH/OLujatef+zedDa1/PQZr797j+AFHCEpebwD+H7/Ipovgg
h4yyo/27T9Livxz+zScs8YNJvpGk6I5EH1SBAsDVCducGDcXoh/KwzO4PEEFUG2/Tk5L89EbgWj/9OyDAP6k51Ly4mthBVARLcmG
z6DEcCiG//r3F541m/4Zf8oTVPxIai9CElWEanDlO9o+A3/hNbsQgLknflpb976W5MCMfwxj0SC9uRvnVL94xtvY4C/QYA7GnL0+
rzkFL96wOJ9PXB9I8jaIjt18TD8UxLS71D739Ld/UJsnwXgU7tKpPo1/WJPUftAx6UHJsORAiEb83y3av7ux/luNqHE+qA+IOVeH
e6AaWdddaP9y0f5uRc1/JJ4BeXyz+vjQ0vPthj8Gyh6U6hS1/vjzix8kNftDIu6TRdim26R98ElPr5a3drR8+r2OogESfRLnxLvT
gX1Qv3hGilkLs9eBTTufOXmepHEJBO2FS/oMkCTVOhO6IppdiCHNGiQFqPILSkIZloAybtxB8fyFXvz9Yt8bUitRqKTgWFFt2Nuv
y9jfkmZ9xb+uaEuSKMh+j5aa45bU/tw+KO9yl071qYgCPEn418YOQvumEbb2GIRYULX8sR+D9s7PPoAa5t9rw6Htf21tuayPdmA0
C/IE77G1n6nmLFJQQkrioPkFzf0N8w4gyXsHezZxs6qPtu+YvZ8zo8GJts11f/b6vF5+NqJfpbbign5c/+UysQd/3MEu9Ihs/HGI
+CIYj/XysxFJzbHo7Zkb0sMf22JzIwO90oY0JRKDxkkTg+McRjHMvNOse8UVWkD5wsYdu/CIPe60/V3Gm9TC5pv2eEPS8/LRD+7Q
9t3FJGedubfa8T3OAVfDFGgmKV91zLjycf1cY/zDmsZuPtalP1/sKJCK4pn1R/t/7a+n+XckztjlEdfm+ynppGtJY6BB+67Y+1Ot
sP3nEutgVWEdshr+Z8CTOx/pzMnz+qK3j/Z3JO78C4rlz0Xmz0PG/LJc9r7PoEJ5M6PvSGrOm+iLbOx1r6A9iEGxOf+e26CcrGZ+
yrmw7F4+nGyeg0mZXwbFSRt/QDWy5AdFq9j7zL1VvXw4qX+sPu4oei0ptggVkjFx/OMDR9q+vrG5FVvcZe7Gub14fskfcp8zeZXu
LS539IPfQP9RbWxuUUy5REP9tcbVK61zov71FbPeRT8Uj3uhezyfe6BHp/t18ZfNtq9TbLY8Q/21xovxZiLPr24tBv7M9PZWaKFO
g/X2fMy61/3xZGce/TEHf9Hh5a0d3WWcyuTV5tqhsZtqPLl4RremPuh4Hwgrgjoz+o4mFtiPlZVp97gcwsH74HjfLYvJNz+x8DTx
32G/SXFM+y8931bSswHsSSlW1B5QFG9kdqVtjStJTR7mncXzz3XMuxbnTovnP/NoisHbbk19kCinDPIza732/J/2d8fMP8duPtal
U31ejQDz7vvp69feWTypuQ7P2bvk7Lwn80uLbecs4tZmmG/mY8feJvuOanp7S1pvtv/09pYkaea3jdB+OHt93orRRcexEcyME0F1
R6LqcLIeUA6zF4tzX9Wyz30tPd8OWKuPXguQWKvPK03cmTNeLUFjd1CbmH0/hnnXGldn7NkeU8L6gLZPzm77uJjOrakPQueWzDnL
EzT+/PXe57z7VmDp+bb07ZrGfV+PGn9QHP+8M4p/vmk/f3geZMfcX+px/QGk5AUIbSahPMpDwm23aH+34or/onhpiu5w7RcnTQFU
e/Edxbl0qq+58Yq5UOUoAOxG0EZD/8Zzf+JzgyQc2dgFkMKSb6cpvmaKb0rS3d0d7oeEitjwad8Dn/T0ciAjhj/5Rtz1LzH+lMEf
yLSFJTqxmcKCyMYUXqtfPNNWoG5mtPUz5t44e31ec3tfs+dI/sUxEjXlY5KwmvHI7heptTHI3ycGC8T5xfWB1OoHcyiMfsjvv3/y
kf52d171i2e8A3dS+5hi90nQeBSEBfx0/In3kibCIjlQ8Yg9uEX7V4P1X3dMzDnqQHxQH9D+xeIecCcu6SftX664hJ9R7c/zN7+s
a1+0f/nYg1KuotYfz+wVguF+SG/p+XbmPrDd3W31B/1QjDT94H8e0AfFiHsG8BwuXlyxBanZ/rR9OnbxNZOIJqwYrY01+GL4EwCF
uT9+QT+trQcm5Is6oBcVK+I+aUmaiFJqP3ydhfn7JrGfFFy48KD0T1wBHptJjChlK0yy+uhnr90PSvvmkScWhGyC2jxJ7AflYe2x
O5hzSP4zSPYclHeA7MLm/ibucPb6fFvCPeRn9v8n4S8uGBR74/rPLm6+Y2IPdrtT6DG/tMUwbOZc6rOJm0V/LFj8cYawhNDEgNKx
k7DaTMHxhycHAv8e7Vy8qNinOYNk5j/P5h/q7Zkb0sMfvTFI2ns/2BCJiHMi8Vg14mLQ9EO57JimH21fvqjrf+JqveOZ0DxPQdGv
snxcP9f4673PdeLdaa8ITNqkfFV8zoMorh9QLBN3jjv3FXT2l/Epm7j95yTfLp6J/0T9TNS+K4m4Z1Gy7j+XiH8Wzd8XrENWIyz3
G+1fjax7IGj75OLiPkGx0PrFM3qyl5ODnALFsvvDX3xq9dHP3tfsIiZSMy8Q130+/j2IRtj9Ycflwsalf9/Lh8W4lJ9550q73xP5
2LmtaPtqZdnfjGj+ImBGUJEdclXl93H9XGP8w5qWbj7WpT9f1NKPj1x/pAPH5PV8MT6qr24tanpjq6PAo99A/1FtbG5R6LQEpj/u
LS7TDxXjXnBvqL/WeDE+2va1R6f7tbD+xit8HYdis9nYbW8KkJs2N/eEsbt7xCow3i5qvd2fR5p7Jp2wPYgm5mDysY7dfKzbx455
3x8+2ittiZzzBUhadDPpuQ2ES3L2mn1w5QhaAzD7Ec21HZcLAtmErb/Y7e/t/0nYB+xJKZ7ZA2pcOtXn8NPsPx/XzzUmrta1ZLWx
EVeT5+P6uYYk9nyWzH/umnOn+YWdeQzKv4dqJZ3/ozz2e7DZbzLUX2uYd95PX79uO4sncfYuC7P3Yel5c3//QP/R2L/DeYt8Xm2u
HZpWZ701O/7Z0/ObdnePhD4LvH0nIsZWBP/+q7A6hK39b5wBK9pQf60xcbWuCYlzXxVjrb4cl1ebayoP6lckteL0I7MrHXs5k8w7
OX/UYs8HjeWtnY41kLB9PxNX65q5t6rxgH979ts19gUVwN/298cvaObeqma/Xev42VtTH8S2L9d9PmH3gtQ5/rDuUp1bUx/oX774
j46voXzN999tL99Akn0PS8+3NdRfa7THKHgnKMLu7pEDOffvcf0Bwg4+2uzAg2EnM0c+FB90i/Z3J2vyAQ5elyuq6A6F74oV9wym
qEv57CRkiZ4HFuZC+WS5/iWewXl9s/r4kH/zvtQeBDIbgQy7CAMJ0LOxkw8ECSv6GJV42xTfpC+iBW3CXXreHEf8m0+SmtrZ1u1j
x7S8RYLuJOzrP67wLONPuZK++5KAqXj//ZOP9Le786Hjjvm6Peec8/0b9s/TF+mZeb9R39vsU794RnM3zgXeG3ZRQRvtXwx/H5iv
2YKKahr0Q3L29W+3u/lz0DuZ3eb+8cj8PYmNK0nY7f+3u/Ptia9uPk6dFIjNKukR/3eL9neH9V/34hLQS519QPsXh3ugO7DuUj1z
7ccl/Axqf+TH2lf3Yg9KuVh/7F5J+0CStJf4nH7ILiwJRJp7Yerk+TI/4oHEM8CtJEWokI6diCbs4Lu9Ds8zuBim3WdGwwuNFCHo
XY3+6WQSUcYV25Saa1imXZOsyQQV6DT/zeyfeP/wF+CJuh8mFp56sZ4shUlYf4xnJxmOux/CYkG0cXpRsf+o2A+xz+IkOYNkI/ZW
rCTPU3vvs0lKKcmLPaBY/kQQv05OS/OdSUAN3sfKZa5/+ywAbZ5P3Lo7hR7LZ85jxMUhxm4+9pJ/onr+hNAG90LxzLjOmYviJUn6
6T+DJLUSDj+buFn6Z9zPTLGLJFoxCZIsFSUsCT2qYdrf9ec4qOKu/6BnAuNQ+U68O+0lx02TlG+/JIJzba8dG5I0v7TYVhQgKim9
xJmjrMz5X3PuzuaPiQa1MWd/i9V29k7tbc4aYrXIPVCNuP3/cWtg9EFxwuLRrEO6RfuXK+oMDG1fjKr2HiKZS6f6ZPa+BeXBsgtP
mcIxaWKniBeUh29mtPm/cXtSosYl5kT5BOW7iuoL4g/FyrPXFtkkyQEB/F7FFXdBfvZZ6hfjzYnM6OBhaf2opje2vK/FOTm7wDpX
QUyfvBgf1Ve3FjW9saXjA0ci/85A/1FtbG5pqJ+i1nnYbS9xL7gw1F9rmLZ+PvfA+/rC+htHn+hg+upWsyjt9PaWXm2uHRrqrzXs
r5m195HZFV061Rf4ThW03u4vyBpUjBXlMcWFafNs0p7l/aSn16u1gOzM2WtiDNUIO29tYsomBh10rte/H5p4W3p2vN9ef/G3f9K2
pQ/yC6oFMzK7Iil7LRjkE9X+9tckNdj7mZ15B4j7Oc6ddgd7D7rEvqsipa2xgOL5z13Y+Wgury7qzMnz3vlfOxeZtLc/dEOaEu/A
SXxcP9eQmnPSpefxazOctyiGuTY/rp9rLD3f7lgH2NgMPu9im7txbq8fWl+zn+Nc/8kk2Q9nv/dyBqx4Q/21hok7S5z76has1Vcj
bt7J+aN2/rUmY/KX7zUp6czJ895z0B5X/Jaeb0vfrnV8/a/3Pu/I+0ANu3T8Y7oxcbWumXurGv+wFniucfbbNd2a+qDt7xDjxH7n
v+ZRjaXn2x35BqL2PQT1E+8E+dn9cBDn/j2uP4CR5MCL/+eRX5ICbBS/Kw/t7w7F79xKkvicokfVSVMAlfGnHKad44oB25gLFYMC
wN3n6zsP2p4BZkPQ/Y0dXVtbdvWx9o2kRR/9ibdNP5BwILmg5J9hCT9187F+fvGDND0Z+u/ZG+GWt9gUVwT/AgzjT3lSvfvyDlYK
k/zTtP/cjXOBfWG+TmHHcoQt/EaZu3HO+71/UxaS+7h+rvHXe5+3fc1Oiuu/H/x9Qz/kl+SAl/110+ZB719z1u/ZOJGMf/yRWs/e
JEmwbLR5csT/3aL9uwPrv9Ub6q81lp5v68S705LS9QHtXwwz9zzx7jT3QMX8139c8XGu/3IkTT7pb3+ev8Vh7cudRG1P/NMJ4v/u
xfUBa5DV4F4oD88Adyi24EZUQRE7Hs24U5ykhXjsvsmSoMYkk2MtIF6a9o0qjuGPSVCgM55pz6D7wT8+2ethSfqLGFEyphCtkeR+
IBZUrNizGL6vcW0Xw8Q+YwugWoi9FScu9uyfe0qtJJTEHrKzk9+GjT1nr8/r5Wcj+nWyuT4zuPKdN/e3UZQ5PXPdRwm79s1ZgGvi
LF5W36w+PqSrXzYkYj+u2O/CYfz74n6dnJbmO8cgg+TE2cTN+c1YZI//gyvf6draMmNQDv52b5tvMuYUKuj8VxAz5pj5D4ph2l8i
6Xa3oB/cSdL2JBmrTtBZYJMEmn4oh0mG7k8amiQp335KBNct7KIAA/1HY39+vybmc8l/7svwx5wZh4rxt7vzbe9d/vOLEm1dhuZY
s50oD5mN9+Bixa3BsAZWraD7gT6oRpp1eNq/WLR9ufzrLfZ+q6h3X4k4RNHsgsxpTCw8ZS5aMJPLxM6vFHcWVQoel5CeKWBnzgLP
3TjXke/K/y5snhMU6MnH3/aSvPY3+5yl8P227EPMx5/7ivWY4gQVo/rb3fnA9rWv46F+CslmtRcDbkjS/NJiWwx5d/dIYL5bg7Ek
u6H+WuPFeHNif3J2QZL0fO5B28/4/2y7+MumHp3uL+vjHUjm2Wr6ZXTwsLR+VNMbW97X4pycXWAsKgD3QvXsMemrW4uS9u6BPdPb
W6EFv1Ac0/bT21veO9KrzbVD02qOT/4izJI0c68ziaq9vmvGNn9B1uGjvdKWdJc5VCj77EVSrfjb4442RzZJck/a8YWfX/wgSV6x
Ya7vfJK0v8R7QVHsmLN95sLEoM9en4+tR2IQb0snrO2l9vaXgmvC2GsxBn2Q3aVTfZpYeKoktWCe7OWiN2tfH9fPeYXm2fNWnLj2
N+NT/eIZjTe/3aD98wmLNwfl/OHcaXf4pKdXd/fev/zok3TMPvO4tV7k983q40NDAddt0Lgvtd55z5w8753Dezb/UG/P3JAe/qhn
8w9b/8ZAr7QhTYm4QxRz3sK2u3skNA7H/v5ifVw/1xj/sKalm4916c8XtfTjo8z/lj8Gt7y1w3MhhdZ51KeJ33tRLs59VYe1+uyW
t3aaax0+l1ebay0P6lci/765zsNin3bcWWL8HuqvNeLWPW4fO9Z8Bu7G54C5NfVBx9fCakASZ0smaL+VbeJqXTP3Vk3sxjP77Zr+
eu9z4swVi9treNDH+LLR/m4EjVNR+x6CnhUG52Ky8/fDQZz797j8j5sCbJISLcSjWP72T1r8TuLhUAT78EVcATzavzwUv6te3OYr
km9UI+szgPGnGEEHICUO4lUlzRyUZ3A5kiRgsjcDmSTbbAIqX1jibbMRa+rkeXcf7ncq6gCGf6Ptr5PTGpxsfd9fAGNqZ7tt4YH7
oTiMP+VLUvydd7DymWdw0JzGfG310c9espr9GAytmpl72vN+s8E8bE5k98/st2uSpPEPa+V/2H0qrA+SMn0g0Q9phbV92oKo/rFo
7Ka8TYg8n8P5299ORGbYz1nWZ4pF/N8t1r/cYv3XnaH+WuOj2dZmk4VbtzV280sOIlXMfv5yD1Qn6Pp/s/plqrknm0Pz8c8/WfOq
FvMf98w+COKf7rD+2L3og+okLUROPxSLZ4A7Zv0x7r2LYgvFSlqMmXGneHYhnqhEoBMLT9uKQfJuVry4fdBB71lhBTql9iKd3Bfx
/vsnH3mJbe374ae1dUmte0Bq9kVU20sUhkkqaN/zkzutvmC8KZc/9hY1/0yzHwLp2MV/k7Y/sbfiRRY9Ze5ZKDP/vD8+mCgBokn+
KTX3nvv3QEvNfdD0RXJ/uzsvKX3sU5L+vTYsiTbPI+3aS1DsgbbPzyTijnL2+rxefjaiXyebc6WwMcg8F7gv0jFxzNgC8NZYdH9j
R6oN09Y5hLW7mW/6xxyzN5dkM+UzY47UPAOm+c7xxjDjDpIh6XZ3oB/coe3d8p8BDktCb58FJtlbtcw9IuuMl8HZx2KZwgD3xy9o
Qs37YWNzK/LvUBwgm45zdzcfe3N7I2hvCWNOcez1r6Wbj6W9tvbHemjzciWOPQT8HRQrbh+Q/2eRX9A6fNj9QB8Uz25/Kd06PO2f
D21fPXvfpylEG7YHkQJI1fBf23YOMhNzGJld0czoO5V/toPgv3/ykbce31pjeZzoPKS9N5G9hunZ54AXbt2WJI3d/NLLhWL+1z/f
t/d/0u7ZBJ3Bllrt7889Y7DHthhB+ZfM3luJ/bdFswtQ2W1rxzFvTX3AGntO36w+PtSMJ0sbm1tthQXDEEsuxvO5B5Kkr24tanTw
sBbW33jfu/jLpib7gvtisu9o28+iWKZfwv5su/jLph6d7i/3Ax0gQfdC1LXOvZDfUH+t8WK8GWD46lazKOr09pZG1d/RthSbLc+r
zbVD02rG2YLmM/5CeCOzK97vZ0bf0cTCU1061df2TI4rxjp8tFfaku7215hD+dhnL+BeVP4B+/325xc/tBV1/qSnl+u7AHH5H/yF
sJGPeTezz1yYGND8eD327/Mszi6o7aVm+5vY25vVLwP/rr0WQx9Uw18LRmrukzMFgff6oSGxHzGpj+vnGhNX623zzCTMOtjZ6/Oc
hy9Q2PmjoLOnnDstT5rcq3d3m+eNzPkk4+s7DzQl5qRZmGdq2jUXnsX5hJ27MM/e+sUz3t7cZ/MPm/87cbPKj7hv2Hv8jZ/W1jWx
8FS7u0d06VRf4PXMmkz54s5a+AXF4IaP9uru685nA8+FYnD+qxqc+6oOa/XpvdpcO3S3v9bQ1t5aR4zlrc78AD+trWtm9J2OXHv2
85d9VemZtaeR2ZWOtS1b3PsWe9uSM/v4o9rbWHq+3TGu35r6oCPOxntVucwzNsm6C9d/PkP9tYb/3qD9u5M5i0SM2Q1zn8zcW+34
3n6ca/a4+g9TgNAt/8GXtMXvkJ//8AXtXx2K37lnNl+RfMMNngFu+edAku8QpDiEV6aww7/MQasTV/zO3gxkm9rZLv/DHXBsxCqe
fQAjaPOJHYj+p+lJb9OJ1Ew8bwphSNI1SVMnzwcu8CCZuPkO40850hZ/5x2sOEGJHyQlmvfMfrum8Q9rZX20AyMs+cnZ61+2JfUJ
ShRh2wtKN/ZjcLpsSfqgfvFMWz/YfRCwAYV+SCiq7edunIu89metBfygsYg5aby4xFdSq83tJFhRMQmeyekQ/3eH2KdbrP+6Y7f9
98tPJEmD9WH9nXugUnnuAZ612YVd/+ti3aUqYdc+bV8Nf/vPj9cZ+ytm70Eh/ukG64/dIa74C31Qrrj7QIruB2Ju2fAMcC+uCJhh
t78puIDsLp3q09Lz7di4MuN/8S6d6tPEwlPNjHYW4Plpbb3tz+b+SFMYgLEpubAklPYhPP96ZNDeaIm1ryxaiTUee0WpJGli4Wng
MzdqDzqFYeLFrf2aa5tYUDmC2p/1r2qZeb9d/Jf2r45/D1xU0VPmnu6tX3jf2/ts/nf9wvu6v8He57S8cUfRe3rCrn2JmE8eWfae
EHsoX1wfrF94X1L7OQzzNTMOcV8kYxdfXkow/wkai3gGZ9M291R4u5OEpnxxY86vk8356eDKd95YY2PcSc/EN3nf+n0g8W3xuAfc
oQhb9zMFYuyzeOadizGoWEGFAUyCyp6e3wL/zkFPAp1V1NqL1H4G2D4L1mznij7kPheV98esgUm0eZXiYg/+n0V+SddgUI6wZ0FY
EUgUi3V4d2h7dy6d6tP4hzXvfcrecwX3/MUwjImFp7z7Fujj+rnGX+997v3ZLgL55OIZ9sCVzH8OeLA+rPXVZR2uf95xDvvSqb62
OMPYzWbhZYl4UBahZ7Ct9p+7cU5zN85p9tu1tv0O7LHNLy73sJQsHxyCBRXdkVoFqMZ9X5/9dk2msDvrXfmZsXqov9aIK25KLLkY
X91alCRN9h3V9PaWtN4s5ji9veV9bXp7K3Bfydnr81as/0hFn3h/MnurXoyP6uTsgr66tajRwcNaWH/j/Yz9e7/JvqOR30dypg/s
e0GSZn7b0O7uEe6FEgz11xovxptBBTMmTW9v6dHpfp0auyzdWtT09paODxzRxmbw+qLBsyG/JHOYqPV2w4xrt48d0+XVRT2oXyn6
ox5YWeOe5J7PJmjtay7g58ZuPtbtY8e41ktkn28PO3/984sfJElnTp7nnSynVtH3bfljQFHjEEVp8wtrexN7k5I9C8ZuPt6LzfU1
zL9b8kffV0zOHyOuFoydo8D+2q29fBAi93xiI7Mr+mh2VfPj9bavBb2LvVU/F7geVr94xsTwaPcMTPzZ7gMbucbK89PaelvOH7PX
Nmm8/+VnI/p1clq/Sm1nkkYGeqUNaUo15kgpmPaXFPgOIAWvATMfKo8Z889en9fLz0Ycf5r9wb/HX2rmHpsZbe4tuTX1gf7li//o
+Hs8X4tj6kVJ0vzSogb6j3rfC4tHG/a+59vHjnV8/9PXr9vuFVO7kOdCOJMDMWn8jbXhYvnnQv44tES+jars7h4Ra/XJvNpcO3S3
v9bQljR8tFmb9/Jqc63LjhWb+Pzd3R3v2WvO/k4sPJXUGXvmnGO7of5aI+h5F2b4aK+01RxL/POdn9bWNTP6TuRZF+b1nczaX5ig
vVZhzD6rOLR/fmH74CR590HUugvtXx4Td6D93Quad6J6Sfah7Cc9Lv6jFCB0K/Dgiyh+VyUKoLpD8Tv37M1vJN+oXtQzgDGofEFz
IKnzEGRcX3A/ZBN2+FciKWJVkha/Cyp2FFWEB/G+WX18aKi/1kiSeJ4CGMXzF1kL8vWdB83F8z1ByeY/6Wl+/+7uDsG6lEzhtSSF
Hym2VhyKv7sTl3xSCk/8YC26s+k5h7jkJ6YfJHnFwYz25KDNPqAv0kvcB6b97QQ0VmJcG/2QTJLkP3ELYVZbMxalFJf4SlbBWWP2
27XQg5ISi8ZpEf93h/Uvt1j/dScs7ixJx6/OaezmGPdABYq4B3jWphd1/bMGVo3Q+b9o+yoEtT9jf7X88/+x8TptXzHWH7vDpVN9
scVf6INqJF4PRm7+QvDEH6rjT8Anse/HBTOGM/5Xz+x/mBmVdwjePhxs1gD8ycfsw8IkpimGub7N+G+3YdBa2OqjnwMKdLIOllTQ
+O8fT6LWIIPW4SUKw8RJtPZ78UzkWiOyi4u90d7lCyu8SeyzGkF74MISUUrs/3TJ3gNt9j8PrnzX+t/aMElBU0i774R4T7HYe+Ke
nUzITsSdtAD5+oX328YgMy4xDiWTdf7jH4uI/6THvsPukSTxtj3nMWNO0Dkwxp3kJhaexibhM0i4Wg478SrrLtUx4//EeJ17oMtw
H1TPnIO3vxZUDKZ+8Yye7K3LcB9Uw8yPLp3qC8xzwppXOmGxf0ky2QjOXm8/ezf77ZrGP6xV+TH3taR5f8LOmKIYZv13aS9+kDT2
g2IExSHecP6rMlHr8BJz0bKxDu8Obd8dntz5KFWCbeIQbtHmxQnafyi155Yx61vkAC1ekvcwOw/TpVN9bX+feyG72DPYdi6aPXZ7
s8c2nyTXftS7GONNtKiiR5ICC50mLUqFdF5trh0a6q81enp+C/w+BQWL8Wpz7dC02tdRpre3On4fdqbC3tvDmJ6evYb1YnzU+/qj
0/26+MumtN4s9Du9vaWent8089tGaMHfs9fn1bpfjpT6uferof5a48X4qL66tajJvqPe9W9+H1VsmXuhGM/nHkhqjT2nxi7rq1uL
3vcpNuveT2vrbWdNjfb19sfe+Hb72DGv0O3l1cW2YrdIzt5/lWQfYhC7uDDjVHJR+5/9wgoPmyLDd/trxEIzCIq/+Qthm6/9/OKH
aj/cAbD0fFthOciixiGTU+Dj+rm2dw2ez8kFtb2ULAefHfupXzyjW61cBeThTsiM//Pj9bbncByz/nX2+jyFgjOyr/0k/rHaWpuk
/Yvhn/+ExZk5e1q8V5trhyYW1LBz/iQ1dvOxXn42EvkzIwO90oY0Jealadwfv6Cf1tZD90L456UGOZbSS/rMPXt93rvef52clubf
D/1ZcxYPwaLWxP5YG9TMaPtz1d4XNMQ7bqG+WX186OP6ucbS82YMdKD/aOzfsWOhdx4194iGxd6ezT/U2zM39Pbe7yWeC3HYf149
Mxe6P958FgSd+5I4+1Wm5ji0LfNsGJldEWv1ybzaXDt0t7/W0N4y1uW9r5u4vHF3d8drXzu/pz//vDF349xeG5f20Q8ku+2l1vVs
v/uSO7XTUH+tYdZBzNqfPfdY3trRyOyKovZcSa32jzvbwv62aoWtu3D9l8/kgKD93Qmbd6JaBzHvQ0/V/8EiChDygM4ucvO/kiUh
pv3zoQCqO3mL33Ht5xdU/C5J8JO2L0bUM4AxqHxRcyApfSIOXtbSYQ7kXtoCqP4XM9o/O/uwWJIiOxTAKNalU33eIkAYr8035BXA
kNqTPkvNxR2JvkjDv/k/yTPWHn/SJK1BO4q/uxM175Hak4AGMUlQWHzPLi75iSSpPqz3hs+2fc8+JHbpVB99kAN94E7S5D9RY5Dd
7vRBOlmfAXvzy8arzbVDYzfVCNqQThwiGeL/7hD7cYv1X3fi4s5SurUwZFPEPYD0klz/PIfLFTf/p+3LxdjjXtQeFPZBVCPtHhR/
/B/FMGsxUvw6DGvAxTNrwaYPkq4HG6yFZRNVCJ5nQLn8Y7/UKoTN3Kd89pizZI0djP/V8O9/aBbEbn3fn5DVtLMpTmKP9ySmyS4u
CeXYzcdc8yVIkoA1qt1nv12TpMDCqFzz4bKs/cbNR7kfkottf1EAr2wU3nQr6h6IanveeYtj5v92Ir6gtg/bA71+4X0NrnwnqbkP
mmduMlH7TqIEXfu0eXpF7D1BPmFz/zcx98DXdx50jEGSNLjynQZXvtM1SVMnzxf/gfeZvPMff4JQxqHk2Hf4+2XPeQZXvvPGH+Y/
ydnX/8RewkOuezdMzDlr8SmkZ1//x6/OaeLemCTuAVfyFGEz79CM/fi9sxNA+5n7QntrLjbOfiWXNOdM4Nk7Em4XIk0fBBWDRDGC
YkBveAeuTFwOCNYfy5V0HZh3snLQ/u7Q9u7tzSUb42oV1Ry7+Tjz89fOZ2bwXlycVh/tvwToLoTtP5f29iD69n2SA7RYSd7DJEnW
uuRSzPowkkl6BltSW/sPrX7pjT1c59mljUH438UoUFWMW1MfuP4IB8JQf61x6VSflp43c4cF7RefDYgtI71Xm2uHTEHH4wNH2r63
sbml3d0jIX+zicKD2Qz11xovxkfbvvbVrWahvNHBw3p0ul8Xf9ls+/7u7pHQolN2vmfG+PT8/TG9vaVHp/slSQvrbxL9G9wL2dht
H9bW09vNiqm7u0coNutQkjzoNlME9EH9ilcINIi/AC5azPx/YryumVF5+0/SMO1rcs+bf9f8nmdGuKj9z4frn+vN6peau3FOYzcf
e9c7ihUbf7PcPnasrdjwJz29uttfIw6aQ1wMwl8Y2//O9nH9XMN+f977foPndLwk8R9zHkAK7gN/XoL6xTMab/6WPogRtAf3/nj6
Z7CN9k8mSewZ5fL3QVzeQ85dF8s//0/q7PV5vfxsRJL0bP6hBiebX3975ob08Ec9m3/o/ezIQK+0IU2JeVIQe99/EJNnyY49jN1U
xx4HiXettF5trh2aWFAjzTP318lmfib73J3NrslGf+RnYs/tZ33FeZcC+PN97u4e0cbmVuTfsWOh17aC13A+ff3aez5I0rOJm4V8
3v3K3w9S8nN47Meqzlv1c/rHKnPOMpi1YvvslznvFbVWzztuy6vNtUN398aSuyH5R0z7/rTWrO41sfBUH82utr0DH7865+21Grv5
pZmDEk8oiN32zf0o2967rD+HKnurWob6aw17HSRo7W/4aK+0JY3MrgSeIzVtb4zdfBwab2B/W/VMDMjW3P/Qx/hTEX9crVln09GH
OQDiYkAol5l7JmW/c5k62NLvPwdBT5X/sSILEPKATi/N4i8HjspBAVR3krR9koO/XPvZhfVB0uAnbZ9P3DOAIpDlSroJhYQo5WAO
5F7eAqjILmjzc1zxU4mNWGWJKzpiCmDYpnaagQvGnvSyXv/Ij+Lv7qRNvPHe8Fnv6+ZwDElQ8rH74Ot//m/SP/8p8d/9+p//de93
/6oTb/2hhE93MBTRByfe4j7IgjHIrSztb9p9aPVLbzH+1ebaoaAN6cxH4xH/d4fYj1us/3aH75ef6D//LWLe82//pRNv/SG0Dxh/
sjP3wNf//N+aXwiaf8a0P/Lh+ncj0bsX135p0jx/iYeWI0nyE/ZBlCvvHhSJ9i+Cfy1mbLyeeNznGZxf0FqYxHpY2aIKwadZA2MM
Si+q7dlvVb645Hu0fbnC2n9iIfm6Sis58ePAdQCJtYA4aZJQhjGJ68c/rBX74faxsASsktoKjnQUQVUrMZPUKmL1ez8AVpU8a49h
zwUOayeXuP3rw7HxH969sonb/2banjlQOYo6/4Xs7D4wSShN0p+gtg/bA63aMAn3Uigq7oxsitp7wrM3u6i5/7oUWgTeHoNGBnq9
r9/f2PHGIYl33jgUX3aniH2HyMck/Uya/OfrOw/axhuTfHhw5TsNrnyna5KmQpL+oV1Q4vm/3xuLTAaH4vnn/3mLXyCZsDPXae+B
IYofFSIsEX3c/L+ViOyxV4zK/HulfuADYmR2paMwqp0EmuTb1RmZXZHkLwTQ7AfaPrk0OWckday/cOYuv7R9YFIWD61+yThToNAY
EGsvlSAG5FbSdWBycZSD9neHtu8OQ/21xtLzbS3dfCxZecTSxiHM7+3CU1IzbkrxwWimD1CtqP3nUmvef/Z6swiPKQbPWdTiJcv/
0/w+OX+KFXsG20P7FyV57ivz9X/1zmLb2G8bbqi/1ggqQoVqmfnh/fELmrm3qpcPJ/WP1cf6ly/+o+Nnxz+seWcpkN3H9XON8Q9r
Wrr5WJf+fFFLPz5y/ZEOlK9utRfGm97e0qj6tbD+RpN9RzW9vaXjA0e0sflb7L/VOuNV1qfdn4b6a40X46OS2vvj1NhlPZ974OhT
HQxBbT+9vaVXm2uHhvprDbs/zDM6rtgsypdsvT043/zl1UU9qF/x/ry8tSNJuru7wxzVx57/H786p4l7Y5oZbX0/zd4TqTPuJhF7
ixK79rW6rMP1z73zv8tbO83itihMZP6HvbO/dsFhFCtp/SmpvTC2Pf7fmvqg7e/UL57RePO3nMeOkHQPij0GBfWBeV7bz2mkk/UM
nnkGn70+3zFvQjJh137a9rfzQSBe0vEnCOtc+QXN/21h1//Z6/PeXP/Z/MO27z2buFnSp91/TPvHnXsJetflfao8ceO+/9yd/TWD
XAT5/LE2qJnR4HlN/eIZPbl4Zm//P+cusvKvTf60tq6Jhafa3T2inp7gNQHz3J39dk3Xto5Ikh7Ur+jy6qIXe/v09Wu9/GxEv05O
d9wX6OTP/TY/XvdyoCTdf845pOKY+yDofcp+v6XNq2HGqJl7nYuPxHc6RV2LQ/21xk9r696fJxae6qPZ1dAcNP4YNJrSxOLNGpRh
2n9i4aleba4dWnremffc7+P6uQMfyxzqrzXCYvH+db/ho73SVnM91z/HkZptL0mXTvVp6fm2N6+xn7Xkk3Tn+NU5b/3lzeqX1Bev
2OH655KabW/FNQ/8GFQGO/dDUL4BKfnaCnHRYqTpB7P+uNf2Den3Oy/tcfEfzVOAjQs+v8j2p/hdaYosgMckNZ2ki48c/C1PWB+Q
fLt6PAPcSnYA8k+yD+ExFypO5AFIrv/SFJGInvbPJqrtmfdUw594Iy7piZd83mKSQiAdrn930hQfJwlfsZInfgj29T//qySScBTl
++UnqfvAdrj+OYlBc8rTB4frn5MUN4fkyX9aGIOKk+YZENbujD3pEf/vDsQ+3WL9t/u9/EdwH7BJrhph7S9xD1SB6788ce9eUde+
xPWfV9zz98S96Hgo7Z9N0uQnxD/LE7cHhbavRlhBwjR9wDM4OwrCu8EzwJ24trcLgbEXsXhJil8kLf7FHDS9yPY3fbB3CO/s9S87
DsSYhLjjH9a8r/H8TS/uPpCVjPLs9fZ1F3M4r5mc2zt0xEG9BJIWAJPkFUGV5BVCHbv5pS6d6vPanTZPL83ar7326C+CRBwumyTt
HxX/od2zSbwHa2/ti/lnsTj/5Z6/D4KS0AcJ2gMtMfdMKmnMIW7M4Z0rvyR7T+L6gWdvekliP1HxB28M2mj/Ook/k6H4sjtpzl4w
7yyH3QcT43XNjDaT3krBc057vBkZaCWeu7+xI9WGNbXTPEPG2BMvas337/fGUhQ+IvFnHkH9YBL00QfliRr/098DjzXUT4GvvEyB
2p/W1r3ngEkCnfQZPHy0V8Pq1fLWju7SJ6WhyFH1ghLyUQggn7Tn7jhzV7zkfWB+5l914q0/cK0XoKg4KLJJtgb2J514ixhQ2ZKe
weNeKAft706e86cS62B5+Isf2eYDCmGEMQUJf52c1q9qL8g2MtArbYhC5CHsPpgfr/OsrUjSNbCgIjz+/W8Se7EApJcm95U5i21j
rEE38xc6tZniLTbm8+Xa2Nxy/RH2va9uLUqSprfb23ph/Y339eMDRyr/XAdVUH+YvkB5TLtLzbY3c5VXm2uHptVcc7efDVHFZiXO
eLkQtt5uF2E1Rcj935eku7s7zFF9wvJtTNwb834mLhe9+Rk79iYRe0si7dnT9dVl3V39UsNKVnQY8ZKcAfg7eZ1Lk/QM3vGrc5Kk
sZutsemj2VXvHHZQbgIkF9X2Uns+CLsPTJFg0/7siytO2r2fNuIX+eVpf6Tj3/tz4l6yv8c6V3Zh839b3N63Z/MPvd+vX3hfgyvf
lfBJ96ewfQ8jsysdXzt+dc7L/0Odl3KlGffta35w5TutX3i/eR4PlTJnZ4xXm2uHgr5W7afqbkFrYn+sDer+ePPs0cjsii6d6guc
S85+u6al59u6dix8/cDEgsx94cd90uR/Dv/93pgXgzZjUdLcn5yJzO/V5tqhiQU14n8SVbLPfzXPez3WpVN9bj/U75D/+v5odjWm
/lfr3JEkzh6p2YZ3+2uNNLH4u7s7mhl9xzvfPrHw1JunRL2HmXn/0uqXB/qc9VB/rXH72LHA7wWt/fmZdpdabS9JS8+b7T+2t9d8
zvf3zDjzTfByMEoUlP+W999qhO07hxv+tRU7/6F/7Yu4aHpLz7cT/ZzdD+Z96+z1eT2585HqF8/o1l4+Av1Oc3D3uP4AYYKKgHHg
pRoUvytXngJ4LPbmU0QCVqQXl/whruggqsUzoHswF6oe13/xikzARPunE5cElKKD5QvaBJQkAYc/4MM7QHpc/90hb/Ilies/qzSJ
H4Icrn/OgkxB/vQ//jPX36cv8svTB7S/G7S7G7R7cYj/dzdiP+4R8yzHwq3bGqwPJ5r72O/FNto/v7Ttzz1QDK7/7hDX/mExOa7/
8iWZf9L+2bEHxQ0KwHSHJGsx9EF5kt4HrIeVJ8kzgPYvTrLiU03sRSxeGQXgmYMmlzT5nn0Q7Oz19oNgzYORjw/pd3rYpRuk6QdJ
Un1Y7w2f9ZIfjt38UnM3zrX9LH0RL83472cKoe4V4yzh0yHK4frnerP6pVcEyWD8LwfrX+VJugcrbA7E+m8+eWNvtH82YfMefxL6
MP5kQIw/6UXNe5K+89L25WPsL1aad66oAgBP7nzUlogD6VH42p24tifuWQ7/+GPmPDOj0szoO6GFd7zxZqP961M72zyDMwi8/hlv
KmHuga//+b81v/DPf/LaXkpWfAr5hI7/3AOVsp8HE+N1zYw2k3FnNXy0V9qS7h7ghKHY396qn6PglCOc/XKL9s8vcP4ZgHfg8uU5
/ygRB60SsWi3aH832ANRvCTrMHHPXrsA+bP5hxqcDP45CpEHC4pFc96ifOn2H7YX4ZGkE2/9oWP/m8Q4lEfS/D9mPzTvYMVIcwZb
ov2LlLXt36x+yTiTk12UCuUIKnSKapizQZI0v7Sogf6j3vd2d4905LG18T6b3avNtUPTahZANmP0x/VzjfEPaxq72VwzOT7QLN67
sbnl6mMeGF/dahYnnN7eCv0a90Lx7PvA/Nn/fX+hcMNfEIxis93n7u6OtLW338FyeXVR06ff836GeWq7uHwbxt9jzmGcvT5P7C2n
2P3Pnj/pxFtfanlrp+N6l6TlrZ3iP9w+lvQMAMqXtP3tsen75ScduQnsOVT94hmNN39LboIAQbVHkrD7QFJg+zNfTcbfB3+/NyZ/
rCLJ3hN/IVpJmv12jTwQBWDvjxu0ezWi5p8n7oX/va/vPGjO630GV77T+oX32752f4O5aRh77jMyu6Lbx455f17e2tHd3Z29/mmt
AZ946w9tsT3k99PaeqIzF/7r3lzrgyvfaXDlO12TdObkefomgbg2n1h42hEXtff9m3nP2M3H3n2zvLWju/21holLSM0+I/bQkmRN
zHx/5l7nO8LE1bqWZlcCYxGfvn7djAlNT+rXyWlJwc8EiXOrUTGIkdkV7/f2Ph/mRNVJ8+41dlOMLyUZmV3piO2YcR/pmXWvj2ZX
U9eA3NsHzbUuhcbi7e/bJhaeer+3+0CKzoErSWanEHvewl1eXdSD+pWOr5t9Vqb9TfvZ7W/immM329e8Dtc/11JEDiBkY89vJLXF
PYPjEe3vv9wD5bNzDq+vLkti/KlC1LzT5Bsz77df33ngfc2fBxrJmOfA/Hjd9Udxrqfq/2DeAmwceMknaftT/K5cWQrgcfi0Ghy6
Lk9YAIKkD9XhGeBW2kN4UjMwMXbzS+ZCBVi4dVvfLw/H/hzXfzniNqGwGahYSQLPFH0sV1QBDNq9XFz/vy8UIC9eljlnEBJx5GP6
Ae7QB+4UMQ4xBuWTte1p9+IQ/3eD2KdbrP+6t766nHj+Y/rARvvnk2b+yT1QPK5/d/Je+xLXfx555z8S7V8F9qCUh/VHd5IkQqcP
ypM0ERaFAdxKsgaG9JIcgGQvYrHSJN9jHb54aZMf2gfB3hs+q4VbtyVJS6tf6uP6ORLsZZSuCEy7r//ZFIP5V5146w+8f2WU9gC8
H2tg2eVZ+zVFSOwkEPRBOnnXXiRiP3lkib1RfLD70P7ZBcbe/q35vkXMxx3eeasTNf4z9pcnSfGFuNizP+k5ScnKEdUHjEXl4BlQ
rrbxZ2/OE+fJnY+8hD8G43/xks49h/pJLFwkM+bAvbh7wE7Eyn2QjX8t5vjVOU3cG9PMaPp/69PXrwP/fYlnRJlIAl0ufwJoSV4R
AIn2zyLvuTvWvfLLu/5F+5ePd+BqsAbmDuuQbtH+7rAHwo00OZjC9pz7C5Db3p65IT38se3rFCJvRxFs9/LsP7x0qq9jvZHrOps0
51DtwuO8gxUjzRls2r9YtP3vx8f1cw1JFHdPIKrQ6d/uzsfGc1jTyu+b1ceHPq6fayw9lzY2tzTQfzT275g+mP12jes8I/91u9eO
DUnq6flN0hHve7u7RzrWV2zEOLN7tbl2aFqtNdjmvbCt6e0tSc2+2N09Evr3uRfyyTJ+2+uNq49+Zk9nl7H3ndzd3ZGat5KWT7/X
/LOF53e4uP3PUXufw2Jv//TdPf3TR+92xOOIveXn7Y3bUlvhYVNo+O7uDtd7SknuARTPjj3nYccjzl7/Ui8fTrbtDUK0vHF/f/ub
eRPz1eTC+uD++AWNzK6Q+8SRpO1vz0cvneqr7PPtF/61d3KNdTfvDNLG3rw+wv2N5tx0amebuWmEkdkV3T52rO1rw0d7pS3pxFt/
0Mt//Jf39cP1zyWJ9ZcCTSw81cyo9MfaYOjPhF339zd2pNqwpna2JRFzSOLV5tqhiQU14trcL2pub86/+OMSxB6ym7hab/vzyOyK
lmZXJDXjDXdfN8f32/Urury66P3cs/mH0vz7Glz5TpI0uPKd1i+87z0PDrqovVf2s2B5a0d3d3e8GDTvAuUw5+QMM/dPMgfl/FF5
gs5+SbR5kdKcP2LvT9OrzbVDd/trDX8s3s+sR/nbKn3uz+b3T7xFztUgD3zzD7MmIjXn9lJ7H0TVX7bZ1/ulU33ENAvgf9dd3trR
yOyKZkbfSfT3GX+KM7I3l5eacx6jc03M/PlfdeKtP5BToAQ/ra1HzjvtNXep+Y41MtCrEfXq/kbrHaE5TlX2sX/XotYhk+QAMvPQ
s9fnvXlq/eIZjTe//bt7Tve4+I+m2YB+uP65xm5+6f2ZQSi/pO1P8bviUfzRnSSHfzl0XZ649qftq8MzwK00cyCDuVBxuP67EwmY
yhObAH0vKTEbsYoVl3gjTdE7rv/skl7/LLqXo4jkSxLvAVllmXOiePSDe/SBO7S9O2nizyge8X/3iP24xfqvG6821w4NrX7ZOFz/
PHUfSNKb1S81M/qO7v/Q97vb6NBtuAeql/X6P351Tuury5Ka9wDySdv2PIOLlWf+I9H+ebAHpbux/liNqETo9EH5iiiGjWzyFIDh
GZBd1vVHnsHFSDLmSIpdh2f8zyZx+/t8/c//Kql5GBX55SkCI3EgMq+sRVAN2j+7vGu/tHk+xN7cSht7o/hgcZLO/8PeeZl3lsfE
fNh7Xo6FW7f1/XL0uMM7b7mS7v1h7HcnzThEf6STt/C1xFiUFUXHu49J8nzirT9E/hzFqfKLu/7Hbj6OHPPtpP/ILmr8Ya2xPElz
b/D+VZ6oJJQT91pxtrj7oH7xjHTzsZcc7tfJaUnSP01PSpK+vvOA5Oc5MA5hP+LcnXv0gVvs/XEr7/lHifYvAuuQbtH+7rAHolpp
il8k2XPuLzYuSc8mbub/oPtYXA4y3nmrk3b/oSlKsrT6JWNPgXgXq17WM9jIj7b//Zm4WtdPa+uSKAIWZai/1rALGtkmrtY1c29V
4wqO58x+u6ZbUx/sra+rYYq6097ZmHYb6q81Nja3In/W7gPau1jfrD4+9HH9XGPpubSxuaWB/qOxf4f+yM+eo9v3Qk/Pb5F/j7av
nr/grL3Ph3et7mSKrErE4oqUZO+zP/b26/tXtU7sLZE0+QeMw/XPdXf1S8k3jbq7u8O1X5LlrZ3AIs92kWEkl774dSf7nhmsD3sx
0RPvTgcWjEdLVNFTVCNpH0QVBLbZhWjnbpwr6FPuX/72//u9MQXFi5K2v8F7WjpR+384d12uJPPPsD54cucjnb0+L21IIwOdcyNJ
ur/RnB9N7WwzNw1gX/u3jx0L/Jnho72aXP1eJ976g45fbe76sec75J3Jx34OTIzXNTPa/HqS697GNZ7eq821QxMLatwfH8z9b336
+rV3/kXqjEuMDPRKG+IcTA7+2KjhnUM9eV5S87yReSasX3hfgyvfSVLzf2vDmtrZlkSsTurMwXfiXvuzYPhor7TVinHGnUtFev53
gfnxuvd79sFVo7kuud32taDx5q36Of1jtXnmurU201qjl3gHSypL7S/mni2vNtcO3e2vNfyx+OXT73njdVz7pM39afZ9flxn/0+Q
y6uLelC/IkmhfZAu/my+96868dYf9HH9XENijMnD/65r5jgTC091/OpcovUwxp/8RmZXvL5Y3trRyOyKZkbfif17pv4X7V8MMx5N
jNdl3oVNjNPMPc9en9fPL36QpicDz7t477c72xr/sCZJPB9S8J+BSRv33y96qvyP5SlA+Gb1S1061advWMfMLEv728Ufaf9iUPzR
nSRtz6Hr8sS1f1TbM/7kxzPArSIO4TEGZcf17xYFULsfi2DFSRx8/jcSz3cDis+WK2/yJYn5T1okfugO9IN79IE7tH13oO3dIv7v
BrEft1j/dY9nsFt57wHG/3y4/t3J2vbHr85pfXVZUvM5jGyytL+/7Rl/8mMPijusP3YP+qC7sRZWnjwFYLj2s8uy/sgzuHphYw/j
vzscRi1O2iIwfhyITC/LAXgUg7ibW3nizhLrX3lljb1RfLBYac4fMe8sVpYE6DbiDfkQd3aPsd+NvGMPipEl7mmewzyD86HouDtx
40/cmTvmPvmFXf/Hr87p7/c6zxmhWFHxt59f/KAzJ89Hnn+0E4AyDqWXZPwPG4fOXp8v6VMdDPY5YH/yMUlesn9JGrs5FnkfnL0+
7yU/fzb/UIOT8n4vkfw8jaH+WsP+80FNBIf9i7UX9+gD99Ks//IOXJ68OSBo/+xYh3Qr6xlU+wyw+XfK+oz7VRF7IGj37JIUv0hS
hBzZ+QtQSUqUe4zYW35Z9x9ShKdYWZ4D9EFxeBd2h7Yv309r6/pjrbPIafNrT1PnV239W5y7yGrp+bb07ZrGfV+f/XZNt6Y+kGTP
cR7vFUaivfPa3T2inp7fAr9n9jTMfrtGgbWSmHYd6q81Nja3In+W/igX90J3CStwzbtu+Yb6a14B4DTzIfojmzT7n5P0hynyvn7h
/UI+30GR9p1rsD6sdUl3V4n/55U098/de2PS1l6h2j3LW83iwnd3d2j7jNIWv06D/dHxAmP/CUXtW0dydh+cuNecgxr3xy94v08z
J+KdITnT/ifuRf9cXPvzjpBd0Bwoyblr8g/kFzX/DOsDqdkPczfOaezmY2mj+bVre9+7v7Hj/dzUzjbzowgml+rl1cVUf8+//ti8
Fxjz0/CfwTh+dU4Te+e+xm4+Dt3/8OTORx3nX7jGswtbH0vCXqORpF8np7V+4X29PXNDevijdwZG4hyMLW2bh8VGpWYf2PfK2evz
0sZee6sZEzLxIZ4H4U689Qf9/OIHPahfafv68NFeaasZa0Cxos7hmbNfYflubcz/81l6vq2PZlc1P16P/Ll/rD4O/LpZs997P2Cd
PiH2/OTzanPt0F3fmVHz9bi/mzYHjXlXkKSR88d10PajLG/ttMXg/R7Ur+jy6qIXm5ei+yFt/NnsRWcvUDZD/bXG7WPHAr/nzXHu
jbWdfQ/Cu29+I7MrsvvCtP/EwlMdvzoXOSax97lcZt4pqeO86a+T015+B4n19rKl3Ztr/s7vVU/V/0E2oLtF+7tDAVR30rZ90KF3
2j+7NO0f1PYojt0XqF7ascgOBCE/rn+3SERfvaTB56hNQNLv+2XXpaTB5ywBCMRLs/hCEZjikXzJLeI+3YF+cM/fB5Loh4pw/btD
27tF/N897gG3aH/3iH+6lfYeYANWsRiD3OHdyy2ufXeK2IPC2J8f649uJU2ETh+Ug7Uwd4ooAEN7p5cn9kbxnfzSHn6UGP+LlKX9
gxyuf64lXzJKJJe1CAyKwTuvO8Qe3CL25lbWub8k1n9zynL+iHln8eLaPmz/M/GG7IqIOyOfrIWXzXP6De9cuaWZc0adw+AMTHp5
Co/bz2HG//Qo+t4dwtretHVc0Wuu/WySXv9BY74/8TPyCWv/6dPvSeL8YxmSXv9ha71nr8/r5Wcj3p+/vvNAUzvbZX/sfSlJEZ6o
4iR2X9jJzv/pu3v6p4/e9b5G8vN4Jhl0XBJilGcoIJkuikfs3z36wL00MSDegYtVRA4I1sDyYx3Srazt32p7kp9nxR4Ut/LuP/z6
zgOv0FQcuzAh0A0Yc7oDzwG3aH93aPvyvNpcOzSxoMb98VaxTbvI+8zoO5HFZqX2/SUjsyttheHRaai/1kjSRremPtC/fPEfHV8L
0iqWSuGvPExxo0un+gL3Tc1+uyZJ+rhOO5fFrLHs7h5RT89vgT9j+mb22zXiCwWzx6ck9wLK9dPauiYWnnYUuH6rfs4rOEuB3/LY
RZglaWy8Hrv3zeA5kV3avCf+fVjE3rLL+85l4v+MRfkkvQfu3huTttq/fnd3h/bPqKj8A1J4PSTmruULanvaPb0Tb/1BkryizMtb
OxqZXdHM6DtejCisBg+KYcflzPvZT2vriWJ0SC9uDhR17pq8M/lkOQPgN3az+W5s9v5PnTwf+N8p7EPvI0E5tx/Ur4T+/Cc9vbp7
b0zHr7Z6ws4DvbT6pT6un2tI4tmbgB1z+Pqf/1urFtu//Zek1vM4jIkVrT762bsPkF7Q+pgtyfmvsZuP9fKzEf06OS1JGlz5Ts8u
vF/4Z90vTJvPjNrrWuFGZlciY6N+T+581DwnuWF9sTasqZ1tngeWsHfgy6uL3u+jngnIx34GfL/8JPBnzHplkncv1giy8cf/0zBt
fvb6vJ7c+Uj1i2c03vwW6wIR2PNTnDz3epq2t+f7EwvNvf8HxavNtUN3+2sNbUnDR4PXnJa3dnRZzbi8+Ttx/26a+PNBbfsiXV5d
LGROE/Tuy3ifnIkz24aP9kpb6ogzBKEGVTH8c5+f1tb1x9qg7P1Bxj9NT7bleBhc+U6DK995f76mZgyOOVAycfPOpHN//xxU+v2u
gR128R99tbl2KGlCQzNZOlz/XEvPSTpTBNrfHbvtwzYy2Gj/4qRt++NX53S4/rnsRRtkl6b9j1+do/1LlOYZgOLlaX+z8IvsuP6r
l+X5O3bzcdsvAnHZJWlzqdXu/kNKFGHIZuHWbUnN4HPUr7B2N0g8n0/S619qvwfML4lrP4+0478f8558/O2fpQ+QX1A/0BfV8s//
6YfqcP27Q9u7RfzfPda/3KL93SP+6Rbt71ae5zBFS/Lh2neL9ncn7bhj739g7Ssf1h+7R9q1SPqgWKyFuZPl+cszIL+s649223O9
Z5clzny4/nnH+E8fZEOcvzvQD9XLu/cExciyB4XYW3HSzj1ZfykW67/upBl7guIOyC7Jdc++8/JkiX1y/q5YzEHdyBr3DzpvwViU
XZa5vz/+Q5tnk2Xsscd+2j27pG3Pua/yxPVB0Jh/9vq8Xn424v36ore59kIMIr2o9j9+dU53d3d0+9ixwPess9fnvV/IJumz138f
mHtAkp7NP9Sz+YcaGejVF7193Aclihvz7cRwkvTr+1c7vkY/hQtKxIdq5UkEjfTCzjyiOuy9dSPP3h/2XhWHGGh3YBxyK2v7j5w/
Th6UnMi9Vz2TAyupoPffJ3c+0tTOdqLi4uZnKELVEpWHLAkTmxvqrzWIKaTDvKf7MAdyK2seCMae/Lj2qzEyu6Lbx47p9rFj+qSn
VxMLTxP9PVP0GtGG+msNUzwniVtTH7T9ivLH2iDvWxnZ/XLpVJ/+eu9zzX671vFr/MOapNZ7LW1dLNMP5tfu7hFdOtXXdpbXvGv9
XosYdTP/+HR//IImrtYj7wWUp1kM+2ng98IKXDMmFcdfhDmsEDOKk2f/s/k1d+McsbecssaAePfNL8s9cHd3p+0X7Z9PEXHPoH+D
/dHxktYgCfslEbfOy+4Dqb0o8/DRXi8+NLHw1HsGJ8E7WzKm/U+89QdJaovLjcyueHtAzfsB40rxkp7DsH8RBy1G2jMAYf3wanPt
UNivyv7P/A7Z7f+gfiXTv+HPBzH+YY34RAp54g08D4oTdN7i/viF2DmPfR5p/cL7pXy2/ejSqT5NLDzVT2vrsb+ChMVGDbM3y/7F
86CTeeb+/d6Ybh87pgf1K94vSbq8uqjLq4ua/OX7jr9rn4PkLGQ6/riz8fd7Y/KvH5txiPG+eGH9gPJR/9Ed9n+m92pz7dDd3R0t
b3WuOZmvnTl5XknePdPuP5c637V4z8rGzGn8v4LmOFHoj/SG+muNn1/8UEgf+Nchaf90/HOf41fnQveDmndc2/qF99t+IZuoeWeS
GMR+ctjVf5gN6G7R/u7Q9u7Q9m7R/t3lveGzrj/CgZX2Xniz+qVmRt8p7wMdQFz/1cpTAJVrP5sswWeKPhYrS7vbaP/s8iR/o/hg
sZj/uxWWBJRFyWoF3Qf0QbVMHzAeVY/ngDu0vVu0v3v0gVu0f3dgzukO94BbbMp1x373ogh89Uz70/bVy5r4lgLw+WVJBEQR7OLk
LUTLGnA+rIV1B+b+bjDnr17eNrcLsDHmpMc13x3oB7eCDsCz/6F6zH3cYt+DW1z/7qRp++NX54j/FChJApqofefIh/mne/SBG2mT
XwWNQ5zByC/t3GewPszztyBpxx7WfYuTNPE5577Kk7QPpPZEw8/mH+rZ/EONDPTq4ckBfdHbx/2QQVz7m6R+5po3iW5ffjail5+N
6IvePt4Dckj67DX3gf8eMAZXvtO1tWX9/OIH7oMUkhbhCXsWBBlc+U4SydDTSJKIj+TP5bL7IAjtXw5i/+7RB24Qe+sOrH91B/rB
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
"""


if __name__ == "__main__":
    main()