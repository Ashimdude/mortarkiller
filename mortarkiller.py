import pandas as pd
from PIL import Image
import streamlit as st
from st_img_pastebutton import paste
from io import BytesIO
import base64
from streamlit_image_coordinates import streamlit_image_coordinates
import math
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
def closest(k, lst):
    return min(range(len(lst)), key = lambda i: abs(lst[i]-k))


option1 = st.selectbox(
    "Map?",
    ("None", "Sanhok", "Erangel", "Miramar", "Taego", "Vikendi", "Rondo", "Deston", "Karakin", "Paramo"),
)
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
#es = "0.0"
#et = "0.0"
#sea = "0.0"
#seatarget = "0.0"

tune = -12
tunealt = 2
g = 32
v0 = 151
elevationbullshm = 0.0
elevationbullsea = 0.0
elevationbullshm2 = 0.0
elevationbullsea2 = 0.0
bullseye0 = 0
bullseye1 = 127
work = False
image_data = paste(key="image_clipboard", label="📋 Paste screenshot for targeting")
if (mp != "none"):
    work = True
else:
    work = False
if image_data is None:
    work = False
else:
    header, encoded = image_data.split(",", 1)
    binary_data = base64.b64decode(encoded)
    bytes_data = BytesIO(binary_data)
    im = Image.open(bytes_data)
    width, height = im.size
    im = im.crop(((width - height) / 2, 0, height + ((width - height) / 2), height))
    im = im.resize((2048, 2048))
if work:
    es = st.text_input("OPTIONAL How high above terrain are you?", "0.0", key="shooter")
    et = st.text_input("OPTIONAL How high above terrain is target?", "0.0")
    sea = st.text_input("OPTIONAL your alt. from sea level. For skyscraper, mountain", "0.0")
    seatarget = st.text_input("OPTIONAL target sea level alt.", "0.0")
    es = es.replace(",", ".")
    et = et.replace(",", ".")
    es2 = 0.0
    sea = sea.replace(",", ".")
    seatarget = seatarget.replace(",", ".")
    mountain = 0
    mountain2 = 0
    
    #st.image(paste_result.image_data)
    #im = Image.open(paste_result.image_data)
    value = streamlit_image_coordinates(
        im,
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
    im = Image.open("C:/heightmaps/umaps/mortarkiller/" + mp + "_hm.png")
    if (height == 1200):
        x1 = x1 + 3
        y1 = y1 + 5
        x2 = x2 + 3
        y2 = y2 + 5
        st.write(1200)
    if (height == 1080):
        x1 = x1 + 24
        y1 = y1 + 5
        x2 = x2 + 24
        y2 = y2 + 5
        st.write(1080)
    else:
        st.write("RESOLUTION UNSUPPORTED/UNOPTIMIZED. Results will be slightly innacture.")
        st.write("Text @ashimshim in Telegram to fully implement your resolution")
    pix = im.load()
    #st.write(x1, y1, x2, y2)
    try:
        trg = pix[x2, y2]
        shtr = pix[x1, y1]
    except:
        st.write("Stay INSIDE the image")
    elevation = (shtr[0] - trg[0]) * 2.08
    if (sea != "0.0") and (sea != "0") and (sea != ""):
        elevationbullshm = (shtr[0] - bullseye1) * 2.08
        elevationbullsea = int(float(sea)) - bullseye0
        mountain = abs(elevationbullsea - elevationbullshm) + tunealt
    if (seatarget != "0.0") and (seatarget != "0") and (seatarget != ""):
        elevationbullshm2 = (trg[0] - bullseye1) * 2.08
        elevationbullsea2 = int(float(seatarget)) - bullseye0
        mountain2 = abs(elevationbullsea2 - elevationbullshm2) + tunealt
        st.write(trg[0], bullseye1, elevationbullshm2, int(float(seatarget)), elevationbullsea2, mountain2)
    es2 = float(str(float(es) + mountain))
    et2 = float(str(float(et) + mountain2))
    distance1 = ((x1 - x2) ** 2)
    distance2 = ((y1 - y2) ** 2)
    distance = (((distance1 + distance2) ** 0.5) / 102.4) * 100
    #использовать ли табличную дистанцию или расчетную?
    #elevation += tune
    vv = 45.5
    elevation += (float(es2) - float(et2))
    st.write("Distance on map: " + str(distance))
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
            st.write("For hit distance: " + str(x) + " " + " Aim mortar: " + distances[angles.index(vv)])
        vv+=0.5
    st.write("Elevation without adjustment: " + str(elevation - (float(es2) - float(et2))))
    st.write("Elevation with adjustment: " + str(elevation))


    
