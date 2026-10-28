# Lab 4 - Interactive 3D Print
## Inventing Interactive Systems
### Robert Bourque

## Overview

I was more interested in the 3D modeling interactive parts in this project. I wanted to see if I could make sliders with cantilevers that allowed them to be inserted easily without falling out the other side. I figured an easy application without multi-material printing would be capacitive sliders. I put copper tape on some outlined triangles to determine position and then put copper tape on my sliders and inserted them. You can use them to play Pong. My favorite part was modeling something new.

I didn't know how to do proper thresholding for the sliders, so it is a little bit jank. But isn't the most important part that I used Fusion to create working sliders from the 3D printer?? 

## [Demo Video](https://youtube.com/shorts/g7rEPRxMzso?feature=share)

## Included

 - ESP32 script ("sliders" > "slider.ino")
 - Python script ("pong.py")
 - 3D printing files ("components" > "body.stl", "slider.stl")
 - README.md
 - requirements.txt
 - schematic image
 - assembly image

## How to Use

1. Recreate the circuit shown in the diagram.
2. Install copper tape onto the sliders and body as shown in the image.
3. Upload the code ("sliders.ino") to the ESP32.
4. Run python script ("pong.py") with ESP32 connected.
5. Bon appetit.
   
![schematic of electronics used in lab](./schematic.png)

![image of copper tape placement](./assembly.jpg)

## AI Use Summary
3D modeled and wrote ESP32 script without assistance. Used AI to make a Pong game from data being printed to Serial.