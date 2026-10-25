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
# Out cold, by how it happened. All drawn ROTATED, so they are authored in standing space with
# nothing behind the spine - see the note at the top of build_strip_v5.py.
F_LIMP = (74, 75)            # "stiff": one clean shot, straight back like a felled tree
F_CRUMPLE = (76, 77)         # worn down: folds up in a heap on his side
F_BODY = (78, 79)            # a body shot: folded around his ribs, knees up
KO_FALLS = {"stiff": F_LIMP, "crumple": F_CRUMPLE, "body": F_BODY}
KO_TILT = {"stiff": 90.0, "crumple": 84.0, "body": 88.0}    # how far over each one ends up
KO_SPEED = {"stiff": 1.0, "crumple": 0.74, "body": 0.62}    # ...and how fast it gets there
KO_BOUNCE = {"stiff": 9.0, "crumple": 3.0, "body": 1.5}     # ...and how hard he lands
COMBO_KO = 4                 # clean shots taken in a row that count as "worn down" rather than one shot
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
             ("Q", "CLINCH"), ("X", "PIVOT"), ("P", "PAUSE / MENU"))
FIGHT_TIPS = ("Slip then punch = COUNTER", "Block late = PARRY", "Step off his line: W + ARROW",
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
        return 0.42 / max(0.3, KO_SPEED.get(getattr(self, "ko_fall", "stiff"), 1.0))

    def fall_angle(self):
        """Out cold: how far over he has gone. A man dropped by one shot goes over fast and bounces;
        a man who was already finished folds slowly and just settles."""
        style = getattr(self, "ko_fall", "stiff")
        end = KO_TILT.get(style, 90.0)
        dur = self.fall_dur()
        bounce = KO_BOUNCE.get(style, 9.0)
        t = self.fall_t
        if t < dur:
            k = t / dur
            return end * k * k
        if t < dur + 0.2:
            return end - bounce * math.sin((t - dur) / 0.2 * math.pi)
        return end

    def lying(self):
        """(image, x, y) of the out-cold fighter, kept on screen and resting on the canvas."""
        ang = int(round(self.fall_angle() / 6)) * 6
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

    def limp_frame(self):
        """Out cold: he settles once as he lands and then does not move again. Which pair of frames
        depends on what put him down."""
        pair = KO_FALLS.get(getattr(self, "ko_fall", "stiff"), F_LIMP)
        return pair[0] if getattr(self, "fall_t", 0.0) < 0.55 else pair[1]

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
        if self.pause_open:                       # the menu is modal: use the keyboard
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
        if not click:
            return
        if self.hover == "info":
            self.toggle_info()
        elif self.hover == "main":
            self.toggle_mode()
        elif self.hover == "campaign":
            self.start_campaign()

    def pause_rows(self):
        """(label, what it does, action). What leaving means depends on where you are."""
        if self.mode == "bag":
            return [("SPARRING", "three rounds, a new style every time", "spar"),
                    ("CAMPAIGN", "your career: pick your fights, climb to the title", "campaign"),
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
        """What just happened to him, in one word. The order matters: a body shot is a body shot
        however worn down he already was."""
        name = getattr(att, "action", None) or ""
        if name in ("body_jab", "body_cross") or d.liver_t > 0:
            return "body"
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
        draw_text(c, self.font_m, "THE GYM" if self.mode == "bag" else "PAUSED",
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
        if game.pause_open:
            game.toggle_pause()                   # ...same for the menu
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
CxTxA1QDY6B3cO8CT16Yk6wmfO5dYEnRfWDTnAzyk7Y+bhgaXjrwwmhi4/qk5nz4JR8+IWa7v4CJN9txtFwxtfXl3+OjTNHa8yRo
xJ2PvPa3xH+hJN2su+XslZ+k3kuu+K8kfec3/zmKS7g5X1v81/hhaWlpadWqVfgkEOOLJHxjQeoU/0J8thih9je4gsAmH4z9s/Hd
QQrFV3di4qISseY0QvMu41JHzkXLr5292m40//DM21rt1DeT90rH5wOfCLNPsFCyBJil1J6r/VhbXpTQmkOpFZP75l/9d21c87Te
Xrs2uvdo1gdqbctRxZnYhnxZOEVtnyS+jO3DCalHicSWnd5V9jn41dUD3P+1sO/XmT8jzBq7HN9ZiYIivQKx++5iizrabHxzSp/+
eKxVg7Dc+zrJD67A4+rVf6RPcJcxeS2D7RsjvokYc3fBB81g5qyNb06RV6wJe5146+xlSfG9op0r6UcBtl4lLd6AnZuHWix4FAjJ
ASRhYtJT1z+PXvvs/tyqLZt2LCX9jv1zud/sI4rb96GI+O/RAyOSpLHJazq49vHgf5u8QBtvbMiq+/f5ZeOap6PPd28erOV9Piq4
c8Bn9+dWmT2o1Np73jq7L1bTFqtL8WjErDQaFwA2hDYgTgo6S3HxF4lkSx5oftsMNEBvjrLFz2mNhy+PvBD7WQpR0inS/MRgz/u+
hrcQhtl0ju14UpMX5nLNQ8Y3N37zD9Jv/kGbJJ2W9Hff2xMJwmTBuGhThS9ixbnDo0m/Cst0y+Y81+nkuYhhmm18ufx1SONbd00g
6NAmqQlB2uHWCKD6SGp+ReOTNnkbzhw+/n5bKNCBAs/yhDb+t5u/mQbEknLNPZBMUYFHe+018QeEj8pRdeGzT3jTxbd2cJmyTR6f
uBex7QZCknT26kzq+HAv5Uv9uY9Naoqed65Kuhg/eWEuEmHWfOvymJRejNSPY6KK+cjNHdhxa6nT5v1oZ5fQ59xuOL/10PlYo+gk
gVSpP+cUG+L/vQH5r2Yh/9sbhMxBPh+Yxg/m+Zewf17yiDAnjQPGQHmyxkCo7c89XNQ57B+EefaLzj8Sz34RfPvPcaXvf6RsAWb2
n8WoUoAZ8d8wup1/fHV1S9jUbpCC6GwnaaKzZl9kGsFtPXTeK0ZSNBeDP9qk+cEV5pSTkwwR5PTVxxn63Q9JTRCTcONrL0oyreNC
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
gDXXT94+ZEm9EOO9UKzfJyaUSp46OEPWOOAuajhl60+ovS1GyHOfVXModZ59qXcLo0j9bUi9ocHEgXyxOTs2upIbpJelaO2hS966
Q2I/4eTtg0X9Z3WE3rs2cA8vP745yLZ7SC2KWwfEvjMf5x4u6ty9xcTvv3X2cmqOKwnm/WRs8V8Ts7dFAp/M+H1fDgbRuzjTdxZi
MfmkvuWu8K+ULv774d88q2d/+KH3e2OT7b+jX+YaW3D2y2MnJElfHjuhuztfjJ5pV3w2TXRW8gvP2vhEgMfVEqCdtkQ2Xx7pr5qT
DUPDS7c/uS5J+lJtEVKfH3xjQGqNg7TnX0oXYbbHQL/ZvygbhoaX9k3mL1C4OzujP/1m5/708sgL0eczDxZbwr/LIAKcjrHJhtlT
S1quecjCFv6V2uPOJlrfhd1tzPoxnSKOXOT+O2euavjs/tyqcx6tJMkfp3bXFeb/avDpVSWdjxH/7R5ZwrMS4rPdxhYBTgPx5WLk
EaFNgv1OfpJElw2u3R9l4eXHuv0PBCUhnaJOg7vA/m725io38GwwG9G0DW4/Usb+BnuDM31nAfvnoKz93cMX9g8nr+1N8Zv9kdX8
zYD9O8ksvHKee9f2Ljz7+UhL/IbO/UnFb/ginbS5x/ggD74gw+9mb66auv65d06y/WBfNusn0p5/qdj6a2AdyCbv/C+xBlRJHvvf
OrtPX82ein249s+y/dH3/pVA6DKhe09jdxfX/iG2hzZ59v6+Z7/I88/c0yb40lHK+cv7e6y7lbF9/LDen57VmTfP6KMPLmVeOgo5
C7Pv9JM2HvbuHpGkYF/YfmBOqoYyYwEfFKPMOZj9UBhF1uEkQm3P896G+H+zkP9qFvK/zVPUB7NXbyfGP7Mw/jCFp/1O1ePANOPz
XUA9PjDI/qcgvkvAZhzYfpi8MNexFrD3DKfIeHDtb8R/DawB6VS1F2IPFE5SDnLnz38cfO7KE2tg7olTNg/giwOlxT2xf5si802o
DyT8kEUZ+7u0mzB15nfJyfgput6G5MGk7PxLv1Ok/ier/pO9Txi5Gl9ZdRDk4Ovj/enZjsZL1KN0h9D8rx1/wA/dxzcGpGrq4ZiL
ulODy34znKrzX9g+H1Xnf7F/PorUoLtQ61OcsnfAXPFf7J8P1/55116pPf+n5Ryp+fRTxv6+BjPM//lg/mkW1t/mYO/ZLFXPPRI5
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
H/D4TTRaj7N/VHomzZz+jVbWVmudP2uALfK3Rf52OP88WDgfYafKe6HwWkjGuLdT1fWGjPnsote7Scl1IP9q+J81rfq6Q/JP578u
imINKKZf910i+7Z+3A/aR/bFri+Pnv+X2nsAjPdua79s6/Qbox3f+/j5c21uNTQxPtn6XvR8/cz+0a4GqqHmv7fmprR4ezP2+V3T
O5e9a3r3x0u/3x2WRjF+898fl+9Ly/e7fidLE1Sp3URzz+RnetpY04HJ+N+Vumty8f0JLd7ufn5pOGvxv9dXO8ao1G5y6X8/riFm
nGj2eRoy37nX0Nnp9mvL7d34ey7DVIdQDZzoHJIV+fdXXDNUt078xxefN+e2GPcP7tfKs23Nb79sfe/wwQO6dvNbHT54oNmA+ZfO
v0Pz33Rnpyd1Z3FJZyPff3R9Nvj7jb/9oFtzUzp37WFznzcwB85vv9TK2qrW1jcq+le/Ptj7en1kaQK8sX5Xf/jyT7W8j15Vsp6P
cM1/XQ3+eOn3ffxXAhhmWy82R24Emor7x5z+7/blH1UToTzn1V2LYcx9b5UPHj3xLIVPPrvFNau0RpBOXW867JC/LfK3E8pe6s4/
T/buMS9fEvknIHt7WS/+yTv3+LLOQ1J96xG9+EfqrEMv+TvUISzL+tuP8V+nzB2OfexUsf5KzDNZMfbtVTX3U4NsQsefUu/HPnne
B9S9BiGhDa+ix0CsB8XFbTyyJvdPWa8FapBN0g24WYurk3YuiOyrwfsAW+Rvi/ztVVWD4PNI8j9Y6TcDlpIbqg6zKmvAsWdvQuO2
62cxmIeKKeP1QPb5lDkHMedkw/GPLfK3NSj771I9a5HlGiCuP6kO498We8C2qpp/yL8Y9l8GB/u/NpJuxkf25atiDSD3bHj/a6uK
/Bn72TH+bTH+7VT1GQCJ8Z8V5x9sMf/bIn871tlL5E/+dqzzr3P2EvlbI39baTeWfCvS/FdS183mkxrysA4ki7vps9RsHntncanj
Rtq+0A2Ij55fTrwZuJR8I/a61aBo/nENmJNu0O2QfyfWAFvkb4v87QzCZ17qnH9UUhMwrkGsVhWfv3Z4LSSz3oORyF7i+k8r0c83
ct2nnX5f80n+ybj+00a/77tE9lz73095zv372Yeazfp7AGTe1mqY84u6mgC7Y82i5+t3Ggt6dH221ZCZpnfx59+jTVBn9o9Kz5oN
dLZebI645tU7jQW5/YCJ8cnUJsB5mqI6w1SLrRebI/Oa2PUbXYYazvqNL0P3K9l6sTky3ljouLeJyz7Eb9IccnZ6sqsJbdSw1CFU
Aydai7i5hPwHQ2gt/vlEeO55sLik4xcvdNS4Na/99FL6cEaXv1lp5byyttpsAuyp432uQpL2gaXmXrAC10LEWby92c77WefP/Oa/
w378kyZrY1Opms9fUIPstl5sjoyPTexurN9N/L1jp87o9vJybe+jV5W4z8pE0YAZQFWY0wdHXWrRl//Jca+z9bFTZ4K/k+egZnxs
YvfYqTNdB6Khg04OlsjfGvnb8bOXwvnnzcjln0Wd8yf7weDqUMbcE33crPNQL88zLOLq0GsucXWQWBOk9PW3H+O/bpk7HPvYKXv9
ZZ7Jh7Fvr+y5369B2iYXNWhKqkGva28aahAWza9IThz/9y40jlmT+6vX1wI1yK/Xce8/BsdD2ZV1DoLss+N9gC3yt0X+9squQd7n
lOpzUUWcKmrAsacd5qHe9PJ6IPtiypiDmHPy4fjHFvnbGoT9916eZxgkXQPE9SfVYvzbqnIP2MdYj1fm/EP+vWP/ZTCw/2unquxZ
f8PKWgMY8/nw/tdWmfkz9vNj/Nti/Nup8jN4jP9sOP9gi/nfFvnb6Vf2EvmHkL8t5h5b5G+L/G1FzzHHNUDius9yuXxCN7/9+cTp
YBOGjfW7wea/rhHAuWsPdWV0X7CpgH8j9ribENepBmXlf/T8sp58MqMfl+/r7atz0v0HHc0I/Jt0rzzbJv8A1gBb5G+L/O308zMv
5J+u7HuQcRyaT7/yJ/tOlnswRR5/2HD952Dguk97/bzukPzjce2traruu0T2yVgD+qPsexSSebfxsYndj/aOdjQB/vj5cx07dUYb
63czna+PenL/c/2r8VCNv/2gxduben74ZK6md8OU/fjYxK47/x6VtSHt+Fh3E0jXBFhSVxPgaHNU15BZUqsml79ZSfx3D0stxscm
dqNjONpsNq75b9JjhhrM7jQWdO3mt5r74LeSpKTGna1/i7d3E2qUPQx1iNbAjfuidUjK/4fH3+vIwROSyL9Mof3IifFJPflkRlK4
wXmoyfP89ktNH9rXNf+Qc1jSPrDU3gv2x/GtuSlJ0uS7R1q/5/bg/bk/2nTZb85JHZo4Bn19xNVqY72zMTCZViP6WZkoVxvGNQDg
ddf3RSxukS3afCSKg6Vk5G+L/G2F8i964VWW3yP/NrK3VdbcE33MLPNQr88zTKpojJB0oo81oa2sOch/PNbhbDj2sVXG2GeeKYax
b6/M409/MyAONehW5rFPlvcB1CCen1/RnDj+712vrwnW5N71+lqgBvmVsRZwPFQM2dvgfYAt8rdF/vaq2AdAPmXWgGNPO8xD5Sjy
eiD73vQyBzHnFMPxjy3yt2W1/97r8wyLsvP3H5f1IB3j31YVe8A+xnoy8h8c7AEMBvZ/7VSVPetvPK5DtMP7X1tl5M/YL47xb4vx
b4v3X7bI3xbzvy3yt1N19hL5JyF/W8w9tsjfFvnbKLv5lP+4rAPxQjcfXvluQ+9c+kQX/vt4x++mNf9dvL2pm42HI0k3ZJ/fftlR
37rXoIz8/QbAIaEGwHGfza5b/iGsAbbI3xb52+nHZ17IP5uy78PBcWg+/cif7MP6vQdT9PGHEftf9rju016/rjsk/2Rce2urqvsu
kX0y1oD+KPsehWTebXys2QTYd+PVdmwT4Gjz39B5Z6ndbPbeT81zyq7pXajZnTNszcFC+x1OqEGm1N0INbQPIHU2AY7jmv/+5+RU
R1Nm1wSyDrVwNfD5javL6qHw9ZtvSmo30I5r2un4TTv95ptRw1CHUA2k4nUI5f/D4++1OnmG/CsSXTs31u/m2luU1GoA/Pzwya7f
J+ewuH3gpT8vdfzexvpdTR9qv8Yuvj/R8XN/LY7jjoOoQxvHoK+Pqu7PgezSXi/UAwDwunutFzIOlmyRvy3yB2CNeWgw0NjBBuO/
/8jcDvOMLca+PVcDckfdMR/ZY022Rw1sMP/YIXs7ZG+L/G2RP9DEsacd5iE7ZG+HOccWY98W+Q8G6jAYWA9sMP5tkLst8h8M1MEe
a68dxr8Nxrwtxr0dxr49xr8dxr89xr8t8rdF/rbI3w7rry3yt8XcY4v8bZF/MWXnxjqQLHSz2lCDrltzU7GP4Zr/+o+ZdEN2hxrk
y3/y3SNd3z96frmrgYPP3aQ72tRBIv+qsQbYIn9b5G+L/AcHx6G2eC3YIHc7ZG+L/G2R/2Dg2McWrwM7ZN9/ZN4trWlX3Pn6pOa/
Uvvcf6h5ZMgw1iHUBDjUHFPqbv7r/r6kVlNT1/xx6R8PdPLxs9gmwK75r881APYbcNahFmU0bI97XNd41uc3oQ0163Q21u+2GnIO
ex2qnHejdSD/akRr6BoAv311Trr/oKMZcHSOm99+qVtzU61GtFHkHC/LPnA0vw8mpzpq5fbgk9Z6atAfHIMCAAC8njhgAwAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAFCqLDdPj95s2Oc3/83zmGiKyyqa+cX3J4J//9y1h7FNgNOaDwAAAAAAAAAAhlv0HPT0oX0d
55sn3z3S+u9o89/QY9TtPHOoCbDUPv/uGirH5eI3AZbim5X6Qs1/JXU14KxbLco0Pjax+9HeUZ1+o3tvxTWhlbLVizr0xtVCkk6/
MUr+FRsfm9h1DYBDQg2Apw/tC+4HIx175gAAAIAtDsABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoIbimjC7m/1fGd0X+3dp
/gsAAAAAAAAAcPzzzX4zYKm7+S/aTYCjspx7d81Nb7xqNgx2jU6dzfE9krrrEEVdyuc3no0K1evGq232WirimqS6vONeL9Sgd3Hz
WRwaAAMAAAB4nf0bP5P425Eb3OkAAAAASUVORK5CYII=
"""
VIEW_F_B64 = """
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
yf/Y6Djxb1Dq9d+Jv1ZYAEpXtAHRxf6o1E2uS+o58Di3+t+57tsRzn9i915/3sP1X07R38D+50ekx/kHgFetEPdqXJIxVtRz+2sn
++Y5Ume8d83HUd/c3aXuWC5Jl/+yk2AJ77ETr+7qadApicW3ityG2+2vnYwuQMfGHql//OFvoH0XnyxH1yDC9QfmQeX4CQCpM8bs
Pjwjlxz7yaHTpf/NU+++pGOf8Bycyt/kM3d3Sd9cP945BCD1HHjJGqP2a6R7SNX9W8S+HjevTCr+fHeJuNfgYjd3d6lnvumefYsa
kLv79MUny4w9JcQKALnmv36884pvs/7fLtb/bZH/skf+107ewS+f/x7EmpOgmrLjz9zdJb03sYe10Aaljj/cg9vB+G+H8ac9ZfK/
vlgBVvLv1cTeAz/uKQWIRe6xFv89eP/xcz1Fl8LDMbH8I7FvxtzdJcnLZYUN8CZe3dXNQZ6ffpsGzA3IugeEY5A/zktrxR8Yf6pL
af4rddaXLz5cTpuDapx7cAlZe0+k7Px77l4skf+tavWazWyAmtX8V/JyMOTfa/ML8M3dXerbaxsbt1weEs3Iyv8W5uC5/pP4DfDq
FB9zWANqXrj3v0xxaOTzr/9Q0foD6itq/iuVW3+TWIMrK6sB2LFDE50GYEpbf3PnviT2X9UR+zuYf7zc14Tk6DvjPXvVUV3q+oMe
qzu/9/8Wss+h8v6U4Z+/OPHmDwufv+ZWc71S7/Ma0hXdg+cfL/cUPnH88d/NoRj/m8P8czCy5j+vjG/TqXd7x3bmP3bC812xub/U
e+9lD0S+ogbM4TNALP/l7sPhHgiJv4MieesPoZT6DxLXf1NS1v+ZfzavbPFnSdo6+rwePHrMudOWUAC9eeGZX/d8NaneBsCu4Kfb
2xnWWgrHfz9XjGz3Hi1umjqnlduRBl+x+IUN4N0cyOee046ufn7q0oIm975Y+3ddr8rMfxx/7umvgbq82FfHzjX7S25wWbWX8pqi
sg+ofdtufNpTDHqKGmSNKzumuObk7HtoVtb566wxiPGnGtf07kzO/vOpc7ek4CzS2QtXyXU1wO39PPrOeE/z31gD5rAAPfXH6nFz
Ub/+yc9P/C4z/5J1/ZMDKCdW/8RxzUckadeOvcnnH5kDpYvF/42Fz6LNl1PP/xL/5qXGn/Pv1bn5j6TMplROuNYjzn81wjW9c35+
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
Z+4JYv5ZTWwO5J6/aICKjYgGtMMhbEDImmh9KQ2Q/CbAfpNfKb4Ppff8L/nfMu49Wtw0Njq+cmDn5m4RuPPTb/ed8/U/P7Bzc/c/
5+6KZqc1UAB9+GTtdZPW/hbCJsA0/y3HbwLsK/sMGz4jnLmyuK6KUrYl9/yd1hpA+nMg/x7w3fGT2nY8/3/jfUnT1DHIlFdHwDVE
1QP1rTmkNqdFPhd/P9ZhnjeMb7jOQ/6lmtj4I/U2Ys67zllvq6co7+XeD85B2vLX/vOaoDqXj+zhGbimyb0vdmqNeU2Yi84g0QS4
uqx9EBJNaAepmxPDwNWJPfs/q3Nx36/qZ7GJfzm/vzhTWIMvS2yfg3/+0a1Noxy3Hnf0nXH9/MTvFDZp/v3FGUnqNulhna05NOC0
9dXMdb329YPu59d3bC38Gff6lNciH/G3Q/7X3pkrizr6zni3me+ZK4s9eRdXs9jtCXJN8v7qL0e5D7ckbHSH5rgmtJK613IoFv+U
2t1oBtf/YOWt/7jc17Ybn3bzLVl5X+qglNOd23h59m03PtWuHXt15+sv9J174Ux2nt1vlop0Ycz8xuMTr+7q1ET/8x+739/+wsvd
PjBH3xnX1Llb3XpyXOvpmmrAPHd3aV3Ff2ANgMOO7+4Akl90KS/xTtK9PgpA26IAsa28Ahyx5r8pB7ApQJkm6/CpFD+A6jeHcdYa
QB4cxK+87mSNP+7g9XfHT0rqjDM0AW5ebAOof+jd+erYue5YH3svKP5QTd0C9Nx/q3EPTEXFZ9x9IHYvlhh7qvIL0JdRVABdYvEt
RdXiqFnNf/3FN+Kfbv7xso7/6VrSGCTlNSA/2NavuG7NHt2nXTv2Zm56Llt8mw2Iae49Wtw0dU4r4eFdX+xZS+pc7x88fKg7X38h
KV4wdPboPt1cvN/K776epTT/df+Z1QT4+J+u6SKHTSvx76FZaw2uECKNgJtXdP07fhNgNw6hnqznsKrr/xQtS8P6vy3yX3bI/9oq
iv9Pnx3R9PKSJoNDYWHc3Vo0xQjKY/yxU3X84fpvRt3xX+L6r4vxx1ZeAbJdO/YmPQ9L5H/LqpJ/7Bz0oqndoPn3g7ymbRK5rzaU
b8BM7MtIbQAv0XiqaeH+n6wCoKneX5yn2GcJKc2n3PhfNBdFulgD1PA+qnO3eg68h7lG1BNr/iv1FvJxTYCroBBfeXUPML6x8Jnm
f/h6Q7/NxpE3ByIH0I6i5l8+d0D4fdF8tilF8XfNl323LxzUrh17dWKkU3zG/V34sZ9e7txTaARTLLX5aWoBXJ7FyskreiutNQEO
ixqGTaiIeT2xBrRO1hqExDpEHd2iqxlNALS6jlBU/DzvbB7SuKIz/ljk1jxdTsWd6/X/FmINsFkHbQYNsAcjzMM7WfNPVyhIyp5/
+n8vyJc1B8qa+6Bd4dkV9jLbogHtYHF2a3iciaz/n7myaPGrrHsHdm7uKcT68xO/66k944QFiCVJVxb18cKAftF1igLog5VVSDic
74Sfu5/xmwD7aP5bnnteTXk/KP7cnLzzd279J7amufD5nW4upugM6q4de/l7yJBXf8nV5pA6awpVGtMiXxj/j7Zs0QcPH+r91c9j
68ouxi7PiOpi40/3PbiRdq3zPlSXd/5l/vFydy+PG3/8fSh558CmlzkngKeff94lJQcj0Xy5iqJ9ECmof1XezcX7emV8W9/XXU6s
7J5z9v+XE4v/7NF9kpQUf/Z/NiucDxH/4RPbZ+XObvhnB96b2LNCU7w0703s6amHe+bKYrQR7cSru3qav6AZNOC059YTDuzcrDfu
p62lnRjZrOnlJdbdGkD8bZH/teE3YnNjv9QZ/8MzqS5nGTbmZJ7Tntj+K5rQNsO7blfOZ8QzFv/bBbFnD3oxvwFzVuyl3vinXvvE
v7q8JsBSJ8+S1wsJ1YRNgLv1x04e13fHT+ovPr2kvzj4Wt+6vzt3sf21k5yBSRQ2n41xez9vXzio7S+83P26a/47d3dJc14/Hnfe
V+JZuIw6DZj9+h3r5bz1wBoAS8Fg7x1AcsXGsjb+SPENERw+SkcBaFsUILaVWgCFA9jtib0HYQGUzo31Fg0gG5Yy/riHrazJf4jD
kuXkbUAPY+0/+KK+lOs/i/8+MPbXExZ/6/meiguhcw+orkwBVtg7+s645iLPtnULV25Ebvw/ruwCWDQgb5+LcdYzWNYmROZC1bkm
wLFEYl4jzsmtI3r/xnxf42buEeXkJRFjBy3y5pt58yekizX/jRU73Hbj08zG5TRgThNe/2HM3ZpDUbG3rPeBIjblhXMgdxC16vo/
hSDysf5vi/yXPfK/toriL3XiWlR4wyH+6Rh/7FUdf7j+m5Ea/zKFN4h/GsYfe3n5Xye18AaqSck/xg6Cob4yDZizkPtqFw2Ym+ca
kFdpAO/uv/f3vUX+sYZuAx7F779+AUpykO3Ja/7ojz2xuWgMRZiq8e+jfj7GOXvhalITYHJgaWLNf52wCTAGzzXBljrNqCT1Xfux
Z4eLT5Z16t2XdOyTL1v+DdeH2PzfxfWOOvOgvDUI1h+qy2v+Jal7/kLqHDzdtWNvbrMFv/ksihXFX4qfqegWGH7Q/zWeA8pJnX9+
NXOdNbgGpRa9dY3wLnrFiIuacCKdf7376w9XJ94sbH7tzj6yDlFdSg4gxp8DhWdQ2XuVLq8B536NaP7xcs/5U2ntb4EG2PUV5QCK
zl+jvryiS+H8sye/njP/JA9QrGgO5M99/BxkmIdk3Ek3Njq+4orMZzn2yZe6fGRP/JzGuVsUQGxRyt594t+uY5982VPYKkT8ByNW
aD4rb9DfBIB7b6r3Jvas9BR0Vif2Pz/xO52ffrsb72jx59XXSqLhQg0UQB8cd/73snobyrqxfurcre78RxmvmXh1V3SvLWNOM/z7
blb8Q+5ewThULLX+Wzj/cYVy3dn534zvj+4NYkzKl3L+Mdx7+76yz16EDVHXS0HWtmTF/6fPdoo/S537q39t03S2OXnXf957IPE+
NCFl/Ln4ZFmXj+yR1JkTpTZllmiE2pQyTTjZ+9m8cB9oVg7G5YDdswPXfpo6zX/Zf17dvUeLm459opXZo/0NgKW1+0PWnnNiX0/V
+GedP0U94XzInf+tev6asT/b3N0labXBixRfy3H883VZOANZjWv8m9WMJxZX914dXfsS6/4NoAGnrX968lDSc9HG13mmD890fxbV
EX875H9t+I3w/rxwa6352mp8w78Bd+9d+PxOd28EsR+sMP+FZpTZU8X+q2Z8vHBr03sTe1ZSnrGktWs/3DeB8m4u3tcr4/1rP27/
Z966f9gE+Dfj+3u+z/nTatz1Pf31Uu+5r5m3pBufSm8d0rbjndf6626c/yrv9xdncseQ3176UD85dFpHpW4OUlJf41ln4tVduv3q
LvY9JGiqAbP/HqyXfbcDbQAsdRaeJfUcQHIFNNyAlLfxR2KzVVUUgLZFAWJbKQU4suQdwEa62Hvg4p/X/FfqxH1y31tMPiuKjT9+
sztpdazxJv+x69zf/CNxCCBFrABlqrzxhuR7uqz7r9S/AJHXhI35ZzUnf/h6z+EL3/zj5czGmyF/AcJ/WEaxlAJYF58sd5/FiooP
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
W8TfDud/nw6p99/rO7aS+yoQNoCRyq//5+UDXB4GvcZGx1fufP2F3lj4rPvhTJ27FW1AO/Hqru6He02RiVd36fKRPeTAImLPXdtf
O5ncgFbSU9vcaBj4DeCvTrypubtLPbF3wvfAb4CN5rjmv2d/9gOd/dkP9B//+uPux//5/d/p//z+7/TNn//Y/Tj7sx9Y/8rrwuSZ
G7X/jW03Pm3gN9lY7j1a3HTxyXLu+pv73sUny3pm4sPuM0Dq2VTW39JUqf+A5lWt/+OjEXN113ds7V7j/sf1HVs1d3dJHy/c2vTx
wq1Nc3eXus1q/Y/Fe8XPBOg3Njq+4mIXi+u//Nu/d5svu49XXn+T+Ffknn9jXBNa/+Mff/XPufGX1prPSp396F/NXO/uO0evsvF/
5fU3e2IfO/+y3uJv0gB48swNzc5f7XsDfOEGRP+Dxef6Ug6AEf/2sAHUFgcgbaQmIIl/uxh/bBF/W8TfBgUg7JRZgL73aJH7b0tS
FqAldZMw/ocrvk38q2P+acdf+wn5X2P9oR1F177z8cKtTbNffNu9X4cfs0f3DfT3ftpVacB5c/F+qWZtyEYDbHtlDrWE40+I+JdH
AYjhwfqDLfJfdsj/2kqJv+/2hYM9H6iHAkC2Uq//hc/vMP60IPX6J/7tIP52yH/ZoQDccEjNf0nqHg4m/s3Jir/feNkd8vIPeoXN
f/2xCmkoQGaL/Yc2yjbgydt/4l7D9V9O2QaoNCBpn2sCnHfPzWr+S/zLK1OAz8//cv03o2oDQtYgmkX+yxbxt5USf+b/zeP5azjE
7qlZGIOaVSb/TuybU3b/Ifvf2sP8xw7jj40y+28dxp/ByYp/iOJv7UmZ/6Mdsevfcdc71/5gFTW8vr/vLetfccOgCW1zyjRbePHQ
ZYrQNyRv72cWngGaxfkXO6w/2+P8iy3ib4v42yP+g+OakKS6+GS5b/8n+6/KGRsdX/loy5a+BlThx8kfvi4pvi+O/efNKVt/pmj9
k/hXl1J/TGL8bwvxt5cy/+H8r62i++/1HVstfq2nRtiAtm13vv6CJrQFLnw+39PYN9aA1n2EjVLJv5QTe+4q04DWfw+IfX0fPHwY
jb3jvwdT5271/J0Q//pc818M1uSZG/poy5bKP+/vcaAJcHl5TYCzmv+69Yeis6msv5VTpf4DmlGn/g/qcw19X/xiXov3Fvo+bvzq
130/c3Dq7/teh2b4Mf2Xf/t3nf/1+Z4GzB8v3Np089pnxL8mt/4QfrjmtLPzV/WPv/pnXZmZicb/ldff7Mbdbz7rc01oWX/oVxT/
f/zVP+uV19/UzWuf9cT+44Vbm1zext0L1lv8nx30/6Db/Cap+5/O/LWbOvbLf9C9R4ub/K+z4NwcP/6T+9/o+d4//uqfdeyX/9A3
qSf+zUmN/8cLtzZJWrl94aB2H+59EOD9qK7s9U/8m+XiP7n/jZ5iklI8KUn8m8X4Yysl/t78h/g3jOvfVur4T/zb8/3C6WhRbfe9
zvXf+Zz4N+fAzs2a82LvEr5ZBXClPavX/0zP94h/Pcw/bczdXdLs/FVdf2tSJ0Y2azqI94mRTsIxRLybs3hvQeNjE9Fr3y2Chmj2
25yie6/Tmf/sWXllfJtmj+7T5Jnev5XZo/t0c/F+67/velM2/rHYS8S/DvcexL4ew/XfrFj8v184nbv+H5sDsSmxPNYfbJH/skX+
11aV+KNZ/hpoFsb/dqRc//799/yru4h3S8L5vn/4lPi3p8z4Q/ybRf7LXlr+69am9yb2rMxlPCvz/Fte2fwX8W9WSvzdIbAwDxN7
Dy4f2aMzVxbb/8XXoaw1uFPvvqTZL75l/GkJ+w9t5d173feL9p+4r3P9l+eP+/7XfP7+E5d7yRurkO6T8x/1xd81+J2+NNX3+rx5
KvFPd+/R4qaxhdMrKXPPtfUfrv+m5a09RPY/S+J+2yTyX7ZK7v+XRPybxPkvWzx/2fKv/1Be/peYNyM1/+gj9s0qu/+Q/W/NYf5p
i/1X9th/Oxjzj5e1//mR3O87efHHYKTO/yXpR6eOSNf/QDPaHFz/Ty9XaMzJu95/M76/72uoxuUGwjxZpwntlG6/usvwt0OWiVd3
6bKkqXNaYf96tqz8y+z8VdZ/BoDnL1usP9vj/Ist4m+L+Nvh/LWdMusRjos/+88Hh/MX7UmtP+Ow/7k5ZeqPMf43j/jbKzv/4fxv
NWOj4yuxpnex/f9OeE/wz+v5vl84rW9+8499+YDJrSPSA2la46yBrro68Wap12et/4ev6fl8tUGha46HNWH8s5qgdmM9sV+v79/d
/bp7jcu/XFZnrR/p/CaPRQ1o7y/Md2PtXkvuq5qs591Y7H3bJvbr24XTyfEn91XOtfnb+jE9HQcmtfnv2QtXO3OYiPv73uo2/912
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
7yR9d/ykth3P/t94X9L0jr01f9ONxeXhQ24fhMP8sxnsPx9O1OGzVRR/rn8AVTXVgNb9W7EmtE9r89lBieW/qsRpPcZ/oHUsqmwA
QnOIvy3ib8+9B93/joEi/rbKxp8H4GaVjT8LoM3i+rfF+G8rjH9e8QE0j/jbYvyxRfzt+EVwpbT1h9c+nY1+ff7aTemX/8D8J1Fe
AeK896Ao/khTNf4UgG4O448tCgDZYv3fFvG3RfxtEX9bFECxx/q/nSoNaCkA0QwKYNnj/murjQLcKKds/ov7b7PKxp/5Z7OYf9pq
Ov9I/Mtpev8D8U8Xy78c2Lk5s/mvRP6lKXn5RxowD0ZW/jFvDOL6bw75R1usP9gi/raIvy3ib4/9t3a4/m21EX/mn+mIvz3Gf1vE
3xbxt9VU/P/l3/5df08B9NK4/u3E5j9FDXjc+udi8PXZT2/q71n/rMRvAuz7fuF0ZgHi175+0Cm6ffJ4X/F5nysGh7jVBsnVGjCM
TdAAoAaev2wRf1vE317T+9+Qjvy7LeJvq434oxz2f9rwr/Ox0fEVv/mylB1Hrv/mMP7bIv62iL8t5j/2/PnPqXdfym3+i2bce9Tf
AOb7xPX/LOQfqynTgPPAzs2aC96n746flKRoQ04acaaZnb+qyf1vRK//y0f2dD/3m9D6whxMN/eyvNTyb74+pMQ/bALsI/71+E2V
/a9FX7vvLUnSj04dka7/IZr73Xbj0+Z/yXVg/vGy9j8/kvn9nz7b+d7FJ52cudsL4WP+2Rz2n9uqUv/KnRdGfVXiDwB1xNYfqo43
9x6tNaH1PY3NZwepqdist/gPvI4IG9BtEX9bxN8ecbdF/G0Rf1tl4s8CaPO4/m0Rf1vE3xbxt0X8bRF/O6w/2KnSALUIm0bT0YDW
HuOPLeJvi/jbIv62iL+tsvFnA2KzKIBij3Fn8Ko2oEVzOABgj/mPLeJvj7jbYv+JLa5/W8TfFvG303QBPqSjAbM95v+2iL8t4m+L
+Nsi/raIvz3ibofr3xbxt0X87RF3W8TfFvG3RfxtEX87/vwnpQEP2uGaAPtyCxCPTUjqbzyLuLHR8ZWPtmzR1Yk3+75XpgFziAYA
9fD8ZYv42yL+9oi7Ha5/W8TfFvG3R9xtufiz93PwGH9sEX9bxN8W8bd379Hipvcm9qz465ys/7fLxfzYoYnu1ybPFK//oxn3Hi1u
GlttgpTagHPu7pIW7y1ofGyi73sob2x0fGV2/qqktSa0vn/81T/rzD8f634eNmD+fuF0X/NZp9uEVuMr3FfiiL8tP+/oj0Hh2PN9
kBeWpK+Oncv8d+/ve0snRjYTe0+36d1jRZsAzz/uNP11zX9nj+7TzcX7mv3iW+ZCLWL+b6NK/Sv/vUI9VeuPUf8QQF1N3mu7TWhb
+veRbz3Ff+ANgKWnN1jrBfG3RfwBAAAwrFgAtUX8ATSJ9Qc7JOBtEX97xN0W8bdF/G0Rf1vE31Zq/NmA2A6uf2xENKC1x/OvPeJu
i/gDAICNhvmPHRow2+P6t0X8bRF/W8TfFvG3RfyxkXH92yL+tog/AADYaGjAMxw+2rJF84+XdfHJMgWIByy1AXNZd77+Qrt27KUQ
dw5iY4v42yL+2Mi4/m0Rf1vEH4AVxh9bxN8W8bdF/O2lrjFT/7M9s0f39XzO+n+7/IamRQ04/YbBi/c6ibLxsQn9xcnjfc1PndkH
y23++k81v/msE34+f+2m5u4ude8PY6PjK2ED5u+On5QkbTve/7/xvqTpHXsb/b3XC+I/HMImwKHvF053xqm7Swa/3fqS1QTYb/7r
7sE3F++b/I4bEfN/G1XrX4XPALOf3tT5X59v7fdcr8rGn/qHAIYR93Bb6yX+z1j/AkUOTv299a+woRF/W8TfFvG3RfwBYGNi/Ldz
79HippvXPrP+NTYs4m+P8ccW8cd6c+/R4qb1soD8NCL+QBruv7aIvy3ib4v4A8D64NY0y2x+RrPKPP8Sf1vE3xbxB4CNifHfFvG3
deyX09a/wrpD/hFIw/hvi/jbIv62iL8t4m+L+Nsi/raIvy3ib4v42yL+toi/LeJvi/jbIv7VuULDKd8vW4D4R6eO6EcHX6v0e6Hj
oy1b9NNnO4WhXSHorAYM42MT+uYXk/qLk8d1f99bmR+/Gd8/2P8T6xzjjy3ib4v42yL+AKww/tgi/raIvy3ij42M698W8bdD/U97
XP/Nmj26T98vnJbUafwba/57YOdmi19tQ5u/dlNXZmai31u8t9Btwox2NBX/EyOb5RpnI+6jLVu6Y5Dv+4XTOvXuS4P/hdaxe48W
N118sqz5x2sfUrz5byz3y/3XFvFvVtn6V+717n1wzX9Tfx69ysZf6v8boAEzAOBpN9QNgFkAtUX8bRF/W8TfFvG3xwKQLeJvi/jb
YfwHYIXxxxbxt0cBaFvE3xbxt0X87XD/tUX8bRF/W8QfGx3rz7aIf/NSGyAx/tsi/raIvy3ib4/7ry3ib4v422H8t0X8bRF/e+S/
bBF/O4w/toi/LeJvi/jbIv62iL8t4m+L+Nsi/raIvy3ib4v42yL+toi/LeJfnV94OMYvROyKPpcpQPzVsXP6auZ6g7/xxpbVgDmM
PzEfHMYfW8TfFvG3Rfztsf/QFvG3w/hji/jbIv62iL897r92uP5tEf/hQAOq5mStM8e+HjZfc4h/PX4TYF+sAWfW/fdHp47oRwdf
6/na5NYRGqDmyDrL4prPxprihfH/i5PHdX/fW5kfxD9bnfiPj03om19MFsYfvbLyvz99dkTfL5zu+QjHnrMXrib9b8w+iP9voMPl
4v2PU+++pJuL93Ob/3L/tcX8vx2p9a/817u/A5r/1lcm/jRgBgCsR0PdANjhAcAW8bdF/G0Rf1vE3wYLQLaIvy3iPxwY/20Rf1vE
3xbxt0X8bTD/sUX8bRF/W8QfYP5jjfjbIv62iL8N5j+2iD8Aa9x/bRF/G9x/bRF/W8R/ODD+2yL+2IgY/20Rf4D7rzXib4v42yL+
toi/LeJvi/jbIv62iL8t4m+L+Nsi/raIP55GWU2AU5v/sv4/WOF7kBf/WAMAtIPx3xbxt0X8bRF/G8x/bBF/gPHfGvG3RfxtcP8F
YIkGVM35eOHWptkvvu1r9lumCSHxb4ZrApzXgDOrAaQkfXXsnL6auT6g3/bp52LpmtDOX7upY7+c1rFfTmc2n/XnP64BLaqpG3/H
XfPkv4q5/G+e2aP7uh/S2j3g3qPFTdPLS8n/W9PLS9wPcrimm+5j9otv5X+E913/57j/2mL9wZ77O+C6HzwaMAMA1puhbwDMA4At
4m+L+Nsi/raIvz0WgLCRcf3bYfy3RfxtEX9bxN8W8bfnNq0489du6srMjM0vswERf2xkXP+2eP61w/zHFvG3RfxtEX9sdMx/bBF/
W8TfDvdfW8TfHuMPNjKufzuM/7aIvz3yL7aIvy3ib4v5jx3uv7aIvy3ib4v42yL+toi/LeJvi/jbIv62iL8t4m+L+Nsi/vZY/6zO
bwLsPqRO898DOzcXFiCW1uJ/9sLV3P+t2Qf5xaY3mrDxct73894DGgDYYfy3RfxtEX9bxN8e809bxN8W8bfD+G+L+Nsi/vYY/20R
f1vE3xYNqJrjNwF2H1L++jPxb4fffDNswOlek9cEGOX4TWhd09mUpoJ+7GlAW10T8XfIf6UL85CxvGTYFN4pyumS863m44Vbm/yP
vNdy/7XD+sPwcM2zrX+PjYgGzACA9eSpuZGNjY6vvPL6m5LETdgA8bdF/G0Rf1vE346L/czlf2EBaMD82Du8B4PF9W+P8d8W8bdF
/G0Rf1vE346L/alfnegWv+U9GBzib8ePvcN7MFhc/7Z4/rXH/McW8bdF/G0Rfxus/9tj/mOL+Nsi/va4/9oi/nYYf+ww/7TH9W+P
8d8W8bdD/sUW8bdF/G0x/7HH/dcW8bdF/G0Rf1vE3xbxt0X8bRF/W8TfFvG3RfxtEX9bxN8O65/1jY2Or/ifl4mdi//Na5/pxMhm
TW4d6XuNKwQ9vbzE+7JqbHR85afPjmj/8/3xChsx5xWBdu/dN7+YLCx6PvtgmfegBYz/toi/LeJvi/jbYf5pi/jbIv72GP9tEX9b
xN8O478t4m+L+A8Htw5K3Ot7b2JPTz6gqAmhRPzrem9iz8rk3hf1yvi2vu8VNWJ2sc/Kv0jkYFKVvY7JvzSL+A+Wy0P6Lj5Z7jYd
zxt7xkbHV06MbJaknnHHb/xLvAeD+68d1h8AAADWh6dqEscDgC3ib4v42yL+toi/HRaA7JCAt8f1b4/x3xbxt0X8bRF/W8TfDvMf
W8TfDgWg7XH92yL+9pj/2CL+toi/LeJvg/V/e8x/bBF/W8TfHvdfW8TfDuOPHeaf9rj+7TH+2yL+dhh/bBF/W8TfFvG3x/3XFvG3
RfxtEX9bxN8W8bdF/G0Rf1vE3xbxt0X8bRF/W8TfDuuftvKaAFN4PlusCbDf/LdMEXQKoNti/LdF/G0Rf1vE3w7zT1vE3xbxt8f4
b4v42yL+dhj/bRF/W8QfQF2xJsBFzX8dN/+5vmNr9Pus/beH/Ist14g2q/m1RB4yjxs7nFPvvtTz/byxx28+7pteXpLE8xg2BtYf
AAAAnn5M5AAAQC4WgOyQgLfH9Q8AADYa5j+2iL8dnr/scf3bIv4AAAwW8097zH9sEX9bxB+AFcYfO8w/7XH9A7DC+GOL+Nsi/raI
PwAAAAAAAID1ivVPW34R6VgxaN6XONcE2Fem+a/7NyiADgDA4DH/tEX8bRF/ANiYGP9tEX9bxB9AXa4JsK+o+a/j8gCSurkAt+4v
sfbfFvIv9vLeA2JfznsTe3oaAqeOPf7nxBkAAADA04QHGAAAgCFGAh4AAAAABoPnLwAAAAwS808AAAAMEvNPAAAAAAAAAAAAAACw
nlAMupwm4kUBdAAAAAAAAAAAhluVBpyOyyW4RsBSZ91fIg/TJvIv9mLvAbEHAAAAABThYREAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAEEUBdAAAAAAAAAAA1jfXCFii8e+gkH+x594DH7EHAAAAAOThgREAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkIkC
6AAAAAAAAAAAAM0i/2LPb34t0QAbAAAAAJDv/wczZUU+OA4ujgAAAABJRU5ErkJggg==
"""
VIEW_B_B64 = """
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
P8n9FJV1/kIDznJCc/wih3/9OSfNZ7OLxt+PfZ4DAMS/mKT4p137cc/Ax/YN8B5kFM0/523+y2agcsj/22H9yxbrv/aKHoAk/1yd
uPcgKZZc/9WJxj/t+ndxf8j1Xwrjvy3mP72N/SfNiDYg9HP/cQ1gWH+sXrQg3/SZt9q/A8S/Xi4PES1E7BD/erh9P9EmwFUUQGT/
Wzlx999289MMBeBogBTPP4CatP8zdNju8tVb7ea0Uez/zMZvgJrUgDa6Dy7aAJUmtMX4DajinmWjz1Fu/HF7IELrB6FxC9lkXXPM
Gn/G/vyyrkF25IA2kH8rL2v8k/Zfuf0Q5N+KSZr/u3txlvgjXrQBUlL+wclz/og9iHgZZMl/Ou76v3z1Vtezb/vfW1zVyflZTew9
RA66hCzz+OdvvdvxOXv/s3Pj/9ile10NsKXWGYBzf7ktqXufW5a9/+QfkqU1IExa/8qS/+H+W44ff3f+pTWnf6BHT77pGnt8bhzi
dyBeXGHPJNHmv29cPC3d+WPHeEQT4Ool5T+dUAE+VIP428pSANGPPw1Isok2/5XUUXg1mt/0Hds3oJnHKx3vhcu5SRSILiJPE2AK
EFfLXw+TFGzym9b4l/X27BaW5vvGr2j9uoo1n3VjU9LfZwxK5t4DqbVf2ZcW/7izY+57CIvuO8kjrhGb4+ffyD9k4+ou5WkCxv7z
6sTVv0oae9rxZf23tDriz/WfnTsHE/16Uv03rv/qRdffpc3fgaRC89FcBHHPLrgHd4O/9hsXf5cLcv8WMa9edO3R7fvxP3fXP/nP
/KLjv59LixNX94Rn3/xC9193/yxaW4b4Z1O0ATP7bKvnrwfPPF7ZyO8rUwMYSeQ9KxC3f8rtd/O/f2fvkN44caT9/SNPFoN/F8W4
34f33zna9b2pmZvt7zPO14sGtDa4/psXHf9dA9rQ+M9e22oND46su71t0Wa/zsTqinYP7WTtvUJjl+7pi9dea38+u7yqsUv3OtbG
suz/kTb3ALH/pxy3fjvzeEXaaALsizb/leJzPzwLFxO3/zxuXT6pATPKCeWf4/bFoVo0YK7PB6MH1//72sfac+RCV+2lLPs/P5/4
mebuPiIHVFBS/M/e+LbdBDgk2oB5K+09bKQBsFSsADEFWKtTdAGAAqzlUQDXVujwhUMDhuaFNqAkCR1AJSlXTFwD2iQ0QK3eHyan
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
corcf33Ev5ys+X+faxoz/fV9HfjlL3gPCsoz/jvEujp54u8OwDP+VIf8py3WH+1k3f9A/OuRd/8J61/1yBJ/xv96cP+1Veb+6zAG
lZNl/SV6/SfdgzkIlk+R+Ee9mPtUF9/7saa/eVbTq9y6sq6/X3zvxzp7I/k9YP6ZT9H8A+uP1WD9xRbrv7aY/9si/2arivFH4vov
ivuvraLjP8+/1eD+a4v422L8sVU0/q+MfqyJuU+lRWlsqL/r79MAI5sy48/lq7eCsXdowJyu7Pjv/x74uO6zu/Nuq2nsRKS42Pn+
gfb9NOn8L6qXpfnv7veva/zKeEcBYmnjfrDY+h1At7FL9/TFa6+1P59dXu1qNiJt7jcJrfmiGlnH/6T955LIPxRE/scWz7+2iL89
6l/ZIv52uP/aYv+nrazXfyj/sPv965q4Nt6VAyX3mV3R9Xf2H1Ynz/nrzw/v33gfppp4adsC59/tcP63GcODI+tfvPaabo2+k/hz
H+7o1+TGc657ph2/0t1g89m1cT168k3q/+6jJ99o/95D69yHq/P0r3/Wnh/9ox4e3m/9UrYkv47b7ODpxN8D5JOlAa0f/wOnphjf
G0b86zO7vCol3INnlzv3jLSfeUeP6u2jB9pfn7v7SKOM/5WIW9/Nsv4bXXt3xob6dfLeLHOfFOw/7A3++zB7+77Gfvt/dfG9H7e/
z/Nv/cYu3Wv/OTpH+nLuQd8HowfX3e+Aj/x/NdLGjYWl+T7d1vqJ8X/V1PXfSVK78a9EE9qyssZuYWm+b3hwZD3v39vOXP6nCi7e
w4Mj639/4VzX3Md3vn9AExrZ9nOgPPH3Y7Vx3+38t+Y+XY9+batovAGwxAKANeJvK+sGIBZg6pE1/mwAqgcb4Gy4AqBHvp4Ofn/2
9n0pUoCb8ad6WePP+F+tvNc/8a8HBXBtUYDbFgW4bXH92+L5yxYNUG0UaUAbXbB3C/XRBWPUg/hXp0wD5o6fS9nQiLAi+R8pPgfE
/bcY8v+2WP+yRfx7z+zt+/pqair4PeJdjTL3X5RXJP4HTk21m/9K0ti7b+p3//lfOvDLX+j66YO1vt6tJm8DQp9/AJvfh3KKHIBH
dch/2sgz/rD+WJ8s91/iX5+0+LP+VY+880/2v9WD/Ye2itx/OYBaXt71l+kzb2nsEgXIqpI3/n4DWt+LuU81featjsIRSJcn/q3n
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
"""
VIEW_FQ_B64 = """
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
Q5snX5/VwsUVPXj4KPh1pu1ImtsOige0IzWZre/7kcbMAV2VP2+MienCxZWkwjAU/40Tc83H5h6w956b8ecpKbj2RT8Ur5UCnJI0
eiwMzzAtcv5iQkz+N0mlucfKYg+/2PiX9Weh+Ev9boOUPRBFZ49ix1B28cIxs0d6dfbFSFl7SVGWs4+9oPF5yAyz9nXz4krhvPNo
DuKLdn7xbeituUObN++O98Oh/D6+eeii4r/Dr/EUAe77PnRblfdg+7ka8/1l57Al9fJZkBp733M0Nf6+2PftHLBU7bo1zDnU0DxG
6Pv7ev469Mx1i62heUWFBd09PXZR4KvvHNp2xV1yocjmdNi7e3b8DOjB9P3Nz//jddYYKyL+0+fvH3+tZ3d/X5KG67yPH/9Z6TP5
LwbPBQquNYQCbPn45hvcmLL/px5TiNYeY4b4xqamLkCVujvm6/uaDyWlALPkj7+Zeyh75/Xpc+xDUov/mrokvjloe6/55ccb0iOV
FgFmDnSgSn7z1U8+19V3Dg3bxMzHHfd8rf3uZxf/xYDZA3rz7rqef/mMju7fpd9eeVeS9PNj5yaKAEtb58S++TdJ0l/+lfT80z+2
96MwJk1kcp7Y+27NWPSk0oowP+l25v4FzKSxL/mqNNr4U/QwthcKQhPQJF8tVpb8VqqWALrP8Y8tQivFJR8OiYn/ntsf9nLRsYgv
6bn98bLrXgoX3EktktEnMclPYmIvjSeM+LatX3gbszdPuYmsbGbw7x5WjX05LtrkiwE7iaTvIHuoGHNoQnT40uaMi8r07RlRFPfl
Rxt6e+fMxPVfdRwkTb4k9ynWLjvxTJGiRWU7kahJ5NT3wl9lyZckf7KlJv5d92PbOc5V2JuBJI1v6izZ2Dl//rY3MQfK+SZzYvsf
H/sg9udffSrJvxmdJEBhRUkoY4v/Lj/aGFsAsBNhvSr1bt6ha27x3zJ9eQY3oeoEtK8dePcq1lQRZqn8nvjh2XekW7+vVXxmO/MV
FjGHluxCwHaiLHssy/ybX+ohjJt314dxdeeTU5JVnv7Dx717DjP//+Rg/SsP1n/bV9Tn+w5tSYN2MDG7c+nNYbKyog1x5n4xP2/4
HJg90tv4130GSNwDdZTFv6hw7J7bH+q4BvMH9ga4snvA/nnXH2z0+vqPFVOAPNT/uAeF7fj/Ziv29s+hDSa1Pf7p4/gzpu8vKv5u
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
H7aFJdQG7H2IY8f/T4f9CaNv7XtWL6+eG/tY0Vy03SZvzR3avHl3vYHfdPspS7Rq8xX/NY6vLWtx3+HSn/Hyh9elI6/G/nrbXlmi
VcMk5jYJzS9cujGRrFuKG5eWJd7uE85f5EX882L+Ib/Yvf6cPW1HlQLkVWLPGRi/ruJftv9kb08Kjdhy7n9Avf2fsXOgRWdOEc8U
AdYDBYteuYXHfrc6eMfr8Nfsjab3A6Gc6ftPej5eNfdP3/d/ljEFdxb+03/U0f2DYo4nrc/H5r5q+/fc7lLPvKfo49jTtXZvVbN7
54LPV/vZWrUwocHcQ3tu3l33F3/chvbunt20i7z6iuZcf7AhRRRCTS28bPgKn37+1aeSpNOSDuw7PNEeZr7hSe93TJ9g+gu7ONG0
FP8162bH15Z1XIP2eG9mV3NFhDJpughz2fV/f3VZe+aODP/rfs7mi780KsT9+Vef6kDEemWfHDyxNFGw+uCJpeHaS5HvnLX5UP9v
zpueXv14+LEbcz+t9gtvI7514OF4SMWFf+efnZEeDO6zWJz9HYmdf/btf2beoX2hPUEvbv3XnQcKFf9lzB/H7ovKYm/EzEXT5zSL
4rPTgdhPJ9Mul525T9qrvrJ3Ol/st1PcG393L9sE1NaiO4Oigdj4S822AfEfSIm/EdsOJN0u12b8i/Q9/kUbgHwLvzY2QNeXGv82
Jnv63g6hvseNf5sTbX1tA3P95xr/SP2NvRTX/xz8T//RuwhDAchmpCYgaCrhJ/Gvh+u/GWV9fyjxpFTvWUD8i7U9/pdoA1vZfbAV
703Px2qhDeL55iEkDiN1qU4bcBipurauffqfgRxzoMR+gPn/vFj/yov13/xi2qBO/M1c36lfif7IUWUdLKUtRj+fuDeB2LcnNik6
c3DNii3E445FiX99jP/zik2CO/fSAUmsgTUldv3d1WTRwb63QWrspeYPgPW1DWKv/zaL3/U19jaev9PH3f9jnr1SWv9P/ONUeQ4Y
DRVi7n0b1EEh5vbZ7wDm73Vx/YdxBqAbrH/llTr+bKoNiP8A57/ySilCZTD/3xzW3/Mi/nnR/+TF8zeP3Od/iX++848S8U+5/t29
V78rqRtJAexyKfFfdIqY1o0Z8a+277CpXATEfzL+z326PPE1JgmrvgoXQypCP1Tft6fPaM/p7v69I9+fkR4NEsjRJhpLzP3l0i3N
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
SUVORK5CYII=
"""
VIEW_BQ_B64 = """
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
6ddn+n62sHSz+3PiXs7E2OSW2W9r9py7SYjdc3HuGlfP3JHzd9iDW17I3n+K/8ZTe+8t64ulZMXKfN+sRVbZf27eL2iPOELPIr32
qHNeY/HcMd1dfSRJmvv0W9qhIvssUkgOvsWR/vhL3AdVlS082HP+hXN3Qex56BN/9YqW/vRl6o80NNw8TFLn2Xn70HipPBhuEWaE
yVoH8M3N5fGtgf3mhx+ifMbdLmtdXursSwk9C2xyzkjS25LmD73ck4OJ50A5Weew764+6vQ1Dvcc8PzGut7ZO6KLPIcrqXMG26Dw
cr/uWrs1z9/N6emsD/y/73fmd5jnb4Z7DtHgegUAoD32ertknd1a8+9X8Tn4/iLrMDWZfOhlzwGgmJlvePvOsrSdH0zqzTv/4snj
fe8CEsVnyzKxziuobOZtjhx6udTZC+Jfnd0/xzhz8eH8rzu50K39J3ZO87dXl5mH8HDnn7t7ELWzH7FMEWabm1PeIL/2Dne8c/vQ
uI4/WItShBnVDXNNnqQFgH3Jh81mhqxJfzcBK8lX6/G1Qe6iy/G/6iniYmPhpTwSoKdlil1UTXzrO3xtCjHAr+rmW7vwxbz6C0CS
gKOeoMKzvz/nff7aRYAl6bXtP28n6qNNivmKMcydnpLUeTbYia/yktGzQT1c2SIAWWMg0+8z+ZCvbvIxs1GX5CfhzMZbk3TJTMCV
TbyK6r7/7awOvr/YtxkoK+GwxIRPXW7iTbPhOWvRJeTfM7/2JcGSGOfYfPF/+Hh1jx3HoiLMfe8A29wCJLz7hgspOCtlFzs1suYc
uu1+8XynAKf6C0Oiwz6QLXXm3w4ev9jzPDALL5MPn3bec7eZpP9ZhX/N99wFM2P/nc+lyZmhT+TqzsOZNpDkbYd39o70tIPUaYvf
bM9DZ42lfIWY99/5XI+OvbFrFhXKyJp/tq//vOLXdhI4Xz9k+h4TYxuFr/19z9yn30qSzr056V0HMDG/NfV6T/Ff35oA8jH/nxbr
X+mw/pueb75Z6sw5m2fB97+d7ca7aAxP/Mtx7wHzv961l+3iv9wDcWTN+0v9ay5c/81wx595139IAWbiX07Z8Wfe+q/E9V9FmT0o
5hlQtAcF+WKtQRoUxQjjxmOnHdb7it5lKTqYYea2aQ+/2G3g3gtS8ToZ7bDDTga0ufn8TkEGKbPgYM9euO1n762p17vrAT7sS+xl
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
0k4iGgrBxxGa9NlNvGHagQ2H4XyHf7MO/OrqPX3z4Cvp4vnMf89exKT4bxxu4g36n+aUevflHawRbtHNrKKz5vskdm6G2++EjOlN
cVrJbI6I/rGGgluEWVLPofis4r8G7VBfyAKv/X0Tc9/7l10UmIPzYdz+R9p59oYcgrER83DM/6dF/AcD67/tmxib3Fq6v66Dxy9K
KtcGxD8OM/Y8ePwi90DL3Os/pAizQezjCT186saf5288rH2lExR75j+TYP4/vaI2YA2yHdwLzeEZkA7JltLISyhmz0fT78QTmojP
bpuQQ6ouc5iMtYBiZeKblxwrq+ivxDp9FhNP3/3g9k/2elhIezFHFMYkojdC7gfmguIqPIvhfI9rOw4z91mYAN3C3Fs8RXPP7thT
2il+ytxDdfbh96y+5+i7C/r+t7Od4r/qFJ+1CzEbFGUoz1z3ebKufXMW4G1xFq+qj1fu7dHpy1sScz+p2O/CWShE3o6iMb/pi+z+
f/+dz/X26jJ9UA1u3HvGm/Q5UYUWPzV9jhn/IA67+GmVOU3ERzukExJ7is+2x3cW2CQ/pB2acWZqemvp/k4CYsMUAS6TjBj1nTg8
qqX7nYINdhHgLBRjjs8992W4c870Q3H8x/UFb9EpaSfmxDq+Tl+zHpSHzMZ7cFxFazCsgbXLdz/QBu0osw5P/OMi9s1y11vs/VZ5
774S8xCx+YrPhpj79FvGopGZXCZ2fqWis6iSv19CeaZQmzkLfOPsdF++K/dd2DwnzPwD+5yrcWMvqRt/s89Zyt5vyz7EetzcV6zH
xDMxNrnlziv/x/UFb3zt65jCm9VtzwFvSdLC0s2eOeTNzee9+W4N+pLq7EKbB99flNRbcNP3e9vxB2u6fWi8uQ84hChAOzi4F9pn
90mm2Ky9n3l+Y1179/6U4qMNFbf4r9SZC5pXp3+yx0jm15c+6U+iaq/vmr7NLv4rUZA2hK/wYJGd+bd7fTFHNSG5J+35hW8efCVJ
Oi/pyKGXub5rCom/xHtBLG4RYMPMQR99d6GwHonBfFs5WbGXeuMv+WvCuEWYJdqgDlOQOaQWzNfbuejN2teZqekt83P2vMVTFH/T
P029ckTnOj9+5osAJy0AbBKwSgp6ECMuN/4UHWyXvfhSlACX+DeH5LftK3r5YvNtO6o+A+h/4vBtgJBYiG9LmTEoz+BmUAh+cGUl
3jAJgOYPvZzuwz2j8hZg3Im2H89f1H6rBrCbAGt+Y10f7dun5Scbur65wf0QEf1P80KKv/AO1jzzDPaNacz3Vr78prtZnQPX9bkF
qCR1J5izxkR2+1z5bFWSdO7NyeY/7C6V1QahTBtItENZWbEvmxDd7YtOXVV3gYznczY3/vZBJMN+zrI+Exfz/2mx/pUW67/pTIxN
bp28srPJ9tMPP9Kpq5cLD50iLrcALfdAO3zX/9OVy6XGnmyAq6dsAXLExfgnPbMPgvnPdFh/HFy0QXtCC5HQDnHxDEinqACbQbKl
uEKLMdDvxBdaBHju029LFz1FOUX7oH3vWVkJuiWK/pb1v9452T3Ybt8PpvivuQekTlvkxV4iMVwo377nr6/ttAX9TbPcube88WeZ
/RAox07+Hxp/5t7iy016ztgzKrsQnim0k/fua4rOStlFgCn+W85/XF+QVH7uU5L+ODkjiZjXUXbtxTf3QOzrM4k48lCIvFlmHrOw
AIzVFy2ubUiTM8S6hqy4m/Gm2+eYvbkUYWieXfyXouNxhYw50TzaIR1in5Z7BtiXfEzqTX5IEaR2mXtE1hkvg7OPcdmFmOfUuR/W
Hj/J/TsU/62m79zd1Xvdsb3h21tCnxOPvf61dPWetB1rd66HmDcreO7B83cQV9E+IPfPoj7fOnzW/UAbxGfHXyq3Dk/86yH27bP3
ffoKAdt8if8RX0jh5dkrd3TprV+2/tmGwf9652R3PX5njeVe0HlIe28iew3Ls88Bf/rhR5KkU1cvd3OhmP91x/v2/k/iXo3vDLa0
E38394zBHts4fPmXQoouo5q501O69MmKzqk3tvY85ofzv2aNvSZT7GjpvrT2+ElPEeAszCXHYQqbmrzB9t6E4w/WdGFk1Pv3LoyM
so+hQRSgTcd3L+Rd69wL9fmK/85vrGtWI32xpTB8c+xCv77xjF38V+rMMxiX3vql5j79VicOj/YV/80rQksR4Gz22Qukl5d/wC3+
e2vq9e7P3tk7wvUdQVH+B7sNUJ9diNYwc0AL56YK/z7P4up8sZc68Tdzb09XLnv/rr0WQxu0w1d0+czU9NaH87+W1G2HLYn9iKHO
TE1vzZ2e6hlnhjDrYFlFyp9VyQoAk4A4LXfhq2zyW9RH0cd0SH6bXlHxLzbfNotnQFruGEhyNkGIRfgmZW3+YQzanqLktxSCTycr
CRAJgKqzF2B8h37tCZ+fXTzfs1BvCi8bpgDz8hMWi6sqGu/Q/zSjbPEX3sHi8W38lBQ07rny2SqFTiPI2vx89N3LPZv6fRtFbdsT
/1ssAJQX0gZuMWa3ALMTd9ohUF7sb5ydzr32i4ouMyYtVnTwRdqJuX0IJm9OgmdyOcz/p8PcZ1qs/6Zjx/6L5a8lSfunZvRn7oFW
1bkHeNZWl3X9PxLrLm3JuvaJfTvc+C+cm6Lvb5m9B4X5zzRYfxwMoUUgbbRBPKWK0HragTm3angGpFeUBNSw428SLqG6E4dHtXR/
vXBemf4/PlP4yFcE2BQ/Ncz9USYxEH1TuKxDqPbhU3c9kqJg8ewUVrjXTUop9Rb/NVa+/CZ3DzqJ4YoVrf1SdLxZvviz/tUuM+63
k/8T//aEFsBm7DkY3CLA5nskyiqv2+8of09P1rUvMedTR5W9J8w9NK+oDUzRX/schvkexX/L6SuApPJrADyDq+kZeyq/CDyaVdTn
UHQ8PjO/yfvWs4HCp/FxD6RDEtbBZxLEuQV2JNZYYrOL/xqm+PLevT95/w4FG6rJW3uRes8A22fBOnFu6UPucnl5f8wamETM20Tx
2faFrsGgGVnPgqwk0IiLdfh0iH06Jw6P6tybk933KXvPFdLLKrw89+m3vPtGdGZqeuvfPnmv+3szrpx65Yi+fuUIe+Aa5p4D3j81
o0cry3pu6r2+c9huEapTVzuFFyTmg6rIPINtxd8UAb7y2WrPfgf22NZXlHtYCssHB7+Jscktt7id1NnvoM9Wdc75vin+K7HeFYPp
qyfGJrfWHj/J/bPMJcdhCm1eGBnt7M3Z3qszv7He/d78xrp3X8nRdxesuf7nW/m8u5XZW/X9b2d18P1FCtAmZNrAvhck6febP2QW
nuVeqCer+O/tQ+N68eRx6dotzW+s68D481p77F9fNHg21BcyhslbbzdMv/bRvn16beVmT0FU1FN13pPc89X41r5ueP7cqav39NG+
fVzrDbLPt2edv/7mwVeSpCOHXuadrCZTiHbp/rrcOaC8fshuD9qgmqzYm7k3KexZcOrqve25uVEK0FZgcv4YRbVg7BwF9vc+3M4H
IXLPB5u9ckcnr6z0FBz3xV/yF2GWOrE/1/nlMx33JAWASUCclnfhSyS/bRMJ0NMh+W16ocW/2HzbjLxnAH1Q83xjIKl/E0RRW3A/
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
1msXnJWkD67d0vzGetMfe1cKScKXl5zMLf5r/OzzT/Szk8cpAlyCKcq8cG4q9UcZWm4BZjSDuf/0aIP0KD6bTowcEKyB1cc6ZFpV
478Te5I9V8UelLTq7j/84NqtzrttgMW1jVr/LSA2+pzBwHMgLeKfDrFvzsPHq3vmPtXW4rmdAsB2kZdLb/1Sp67ey13rtfeXzF65
01MYBv0mxia3QmL04fyv9XcX/r3vez4UXY5j8dwxzV65oxOHR737pq58tipJOjNFnJti1lgoQJuG3T+F3Ato1t3VR5r79Nu+4r8/
n5rWX1buSdo9Bb4GkVl3N06dmyrc+2bwnKiubN4Tdx8Wc2/V1X3nMvP/9EX1hN4DpgiwjeK/1cXKPyBl10Ni7No8X+yJe3kHf/4/
JUkf7dsnqVNgfPbKHV1665fdOaKsGjyIw1d8+e7qo6A5ut3iuRT/0YePV/eEHmg0D+vnpt7T0n02ncdA/NOxYx9S2JH4x1M29gdO
39BzU+91N7+hnjLxP3D6BvFvUJlnAOKrE/8zU9McmqmJ6799VZ6/p67e6/k6cXi06Y+5a4UWEjdxdxcpScJUzacffiSps/k57ysr
7gaJZ+oJvf6l3nvAfElc+3WU7f9djHvqceNfpQ1Qn68daIt2ueN/2qE9XP/pEPu0mP9Pj/WvtIh/esx/pkX806rzHCZpWT1c+2kR
/3TK9jv2/gfWvuph/XFwlF2LpA3iYi0snSrPX54B9VVdf7Rjz/VeXZV55k4B5t7+nzaohnn+wUA7tK/u3hPEUWUPCnNv8ZQde7L+
Ehfrv+mU6Xt88w6oLuS6Z995c6rMfXL+Li7GoGlUnff3nbegL6quytjfnf8h5tVU6Xvsvp+4Vxcae859NaeoDXx9vim2ab4ujHTW
XpiDKC8v/gdO39D1zQ19tG+f9z3r6LsL3S9UE/rsde8Dt+Dsdwu3NTs+ogsjo9wHDSrq8+3iv5L04xun+75HO2VzkxDfXX2U8NMM
J7cN0KysM49oD3tv06iz94e9V/EwBzoY6IfSqhr/2ZcPkAelJnLvtc/kwArle//9+tpJzW+sBxUXMX9mfmOduetteXnIQpi5uYmx
yS3mFMph3DN4GAOlVTUPBH1PfVz77Zi9ckcf7dunj/bt0zt7RzT36bdBf+/U1XvsuwoQWvzX+HD+1z1feV6a3M/7VkV2u5w4PKp/
++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
"""


if __name__ == "__main__":
    main()