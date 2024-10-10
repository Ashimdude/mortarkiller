import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_paste_button import paste_image_button as pbutton
from streamlit_image_coordinates import streamlit_image_coordinates
import math
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
def closest(k, lst):
    return min(range(len(lst)), key = lambda i: abs(lst[i]-k))


option1 = st.selectbox(
    "Map?",
    ("None", "Sanhok", "Erangel", "Miramar", "Taego", "Vikendi", "Rondo", "Deston", "Karakin", "Paramo"),
)
bullseye0 = 0
bullseye1 = 127
es = st.text_input("How high above terrain are you?", "0.0", key="shooter")
et = st.text_input("How high above terrain is target?", "0.0")
sea = st.text_input("OPTIONAL your alt from sea level. For skyscraper, mountain", "")
seatarget = st.text_input("OPTIONAL target sea level", "")
es = es.replace(",", ".")
et = et.replace(",", ".")
es2 = 0.0
sea = sea.replace(",", ".")
seatarget = seatarget.replace(",", ".")
if (es == ""):
    es = "0"
if (et == ""):
    et = "0"
st.write("Use a 2048x2048 map to get coordinates")
mp = str(option1).lower()
rawstr = "121 133 145 157 169 181 193 204 216 228 239 250 262 273 284 295 307 317 328 339 350 360 371 381 391"
rawstr = rawstr + " 401 411 421 431 440 450 459 468 477 486 495 503 512 520 528 536 544 551 559 566 573 "
rawstr = rawstr + "580 587 593 600 606 612 618 624 629 634 639 644 649 653 658 662 666 669 673"
distances = (rawstr + " 676 679 682 685 687 689 691 693 695 696 697 698 699 699 700 700").split()
angles = []
vv = 85.5
while vv > 45:
    angles.append(vv)
    vv-=0.5
x1 = 0
x2 = 0
y1 = 0
y2 = 0

tune = -11
tunealt = 2
g = 32
v0 = 151
elevationbullshm = 0.0
elevationbullsea = 0.0
elevationbullshm2 = 0.0
elevationbullsea2 = 0.0
work = False
if (mp != "none"):
    work = True
else:
    work = False
if work:
    mountain = 0
    mountain2 = 0
    paste_result = pbutton("📋 Paste screenshot for reference")
    if paste_result.image_data is not None:
        st.image(paste_result.image_data)
    value = streamlit_image_coordinates(
        mp + "2048.png",
        #mp + "2048.png",
        key="local4",
        use_column_width="never",
        click_and_drag=True,
    )
    try:
        x1 = int(value["x1"]) * 4
        y1 = int(value["y1"]) * 4
        x2 = int(value["x2"]) * 4
        y2 = int(value["y2"]) * 4
    except:
        pass

    #im = Image.open(mp + "_hm.png")
    im = Image.open(mp + "_hm.png")
    pix = im.load()
    trg = pix[x2, y2]
    shtr = pix[x1, y1]
    elevation = (shtr[0] - trg[0]) * 2.08
    if (sea != ""):
        elevationbullshm = (shtr[0] - bullseye1) * 2.08
        elevationbullsea = int(float(sea)) - bullseye0
        mountain = abs(elevationbullsea - elevationbullshm) + tunealt
    if (seatarget != ""):
        elevationbullshm2 = (trg[0] - bullseye1) * 2.08
        elevationbullsea2 = int(float(seatarget)) - bullseye0
        mountain2 = abs(elevationbullsea2 - elevationbullshm2) + tunealt
    es2 = float(str(float(es) + mountain))
    et2 = float(str(float(et) + mountain2))
    distance1 = ((x1 - x2) ** 2)
    distance2 = ((y1 - y2) ** 2)
    distance = (((distance1 + distance2) ** 0.5) / 102.4) * 100
    #использовать ли табличную дистанцию или расчетную?
    #elevation += tune
    vv = 45.5
    st.write("Distance on map: " + str(distance))
    st.write("Elevation without adjustment: " + str(elevation))
    elevation += (float(es2) - float(et2))
    st.write("Elevation with adjustment: " + str(elevation))
    while vv <= 85.5:
        v0x = v0 * (math.cos(math.radians(vv)))
        hmax = (((v0 ** 2) * ((math.sin(math.radians(vv))) ** 2)) / (2 * g))
        hmax += elevation
        hmax += tune
        x = int(distances[angles.index(vv)]) / 2
        y = hmax
        t = 0
        while y >= 0:
            vy = g * t
            t+=0.001
            x+= (v0x * 0.001)
            y-= (vy * 0.001)
        if (abs(x - distance) <= 10):
            st.write("For hit distance: " + str(x) + "   " + "Aim mortar: " + distances[angles.index(vv)])
        vv+=0.5
