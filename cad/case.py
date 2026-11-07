"""OpenLoom two-piece enclosure, modeled in millimetres with CadQuery.

Run from the repository root with:
    python3 cad/case.py
The STEP file is written next to this script as cad/openloom_case.step.
"""
from pathlib import Path
import cadquery as cq

# Overall assembled size: 70 x 45 x 25 mm. Change these first if the board
# or display module has different measured dimensions.
LENGTH = 70.0
WIDTH = 45.0
TOTAL_HEIGHT = 25.0
WALL = 2.2                    # side-wall thickness; leave room for the PCB
BASE_HEIGHT = 20.0            # bottom shell height, including its floor
LID_TOP = 2.0                  # solid material above the OLED/button openings
LID_SKIRT = 5.0                # lid overlap that slides down over the base
CLEARANCE = 0.30               # fit clearance between the lid and base

# OLED module is about 27 x 27 mm; the visible 128x64 display area is wide
# and short. The opening is intentionally smaller than the module footprint.
OLED_WINDOW_W = 23.0
OLED_WINDOW_H = 13.0
BUTTON_HOLE_D = 6.0             # adjust to the actual button cap/actuator
USB_CABLE_W = 12.0
USB_CABLE_H = 6.0
POST_D = 6.0
SCREW_CLEARANCE_D = 2.4         # for small M2 screws; use 2.7 for M2.5
POST_INSET = 5.0                # post centers from enclosure outer edges

# Base: open-topped tray, with four screw posts tied to the floor.
base = (
    cq.Workplane("XY")
    .box(LENGTH, WIDTH, BASE_HEIGHT, centered=(True, True, False))
    .faces(">Z").workplane()
    .rect(LENGTH - 2 * WALL, WIDTH - 2 * WALL)
    .cutBlind(-(BASE_HEIGHT - WALL))
)
post_xy = [
    (-LENGTH/2 + POST_INSET, -WIDTH/2 + POST_INSET),
    (-LENGTH/2 + POST_INSET,  WIDTH/2 - POST_INSET),
    ( LENGTH/2 - POST_INSET, -WIDTH/2 + POST_INSET),
    ( LENGTH/2 - POST_INSET,  WIDTH/2 - POST_INSET),
]
# Posts rise from the floor into the cavity; bores start above the floor and
# extend past the post tops so each screw hole is open from the cavity side.
# Change post positions to match PCB holes.
for x, y in post_xy:
    post = (cq.Workplane("XY").workplane(offset=WALL)
            .center(x, y).circle(POST_D/2).extrude(BASE_HEIGHT - WALL - 1.0))
    bore = (cq.Workplane("XY").workplane(offset=WALL)
            .center(x, y).circle(SCREW_CLEARANCE_D/2)
            .extrude(BASE_HEIGHT - WALL + 1.0))
    base = base.union(post).cut(bore)

# USB cable access centered in one short end wall; the opening begins at the
# floor so a cable can exit without requiring a connector-sized hole.
usb_cut = (cq.Workplane("YZ").workplane(offset=LENGTH/2 - WALL/2)
           .center(0, BASE_HEIGHT/2).rect(USB_CABLE_W, USB_CABLE_H)
           .extrude(WALL + 2.0))
base = base.cut(usb_cut)

# The lid top ends at TOTAL_HEIGHT. Its skirt starts below the base top and
# has an inner opening wider than the base, leaving CLEARANCE on every side.
lid_bottom = TOTAL_HEIGHT - LID_TOP - LID_SKIRT
skirt_outer_l = LENGTH + 2 * (WALL + CLEARANCE)
skirt_outer_w = WIDTH + 2 * (WALL + CLEARANCE)
skirt_inner_l = LENGTH + 2 * CLEARANCE
skirt_inner_w = WIDTH + 2 * CLEARANCE
lid = (cq.Workplane("XY").workplane(offset=lid_bottom)
       .box(skirt_outer_l, skirt_outer_w, LID_SKIRT + LID_TOP,
            centered=(True, True, False)))
lid_cavity = (cq.Workplane("XY").workplane(offset=lid_bottom)
              .box(skirt_inner_l, skirt_inner_w, LID_SKIRT,
                   centered=(True, True, False)))
lid = lid.cut(lid_cavity)

# OLED window and button holes go through the top panel. Their positions
# are measured from the enclosure center; change them to suit your panel.
lid = (lid.faces(">Z").workplane()
       .center(0, 0).rect(OLED_WINDOW_W, OLED_WINDOW_H)
       .cutThruAll())
button_y = -WIDTH / 2 + 11.0
button_spacing = 18.0
for x in (-button_spacing/2, button_spacing/2):
    hole = (cq.Workplane("XY").workplane(offset=TOTAL_HEIGHT - LID_TOP - 1)
            .center(x, button_y).circle(BUTTON_HOLE_D/2)
            .extrude(LID_TOP + 2))
    lid = lid.cut(hole)

# Export the two independently printable solids as one STEP assembly compound.
assembly = cq.Compound.makeCompound([base.val(), lid.val()])
out = Path(__file__).resolve().with_name("openloom_case.step")
cq.exporters.export(assembly, str(out), exportType="STEP")
print(f"Wrote {out}")
