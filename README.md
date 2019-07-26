# Raspberry Pi Machine Learning Vision for FRC

## Inspiration 
Vision tracking for FRC (FIRST Robotics Competition) is often a huge hassle for teams to complete, especially since they are only given 6 weeks to program it to detect that year's field objects. And that doesn't take into account how little time the programmers have time with the robot during that 6-week period!

## What does it do?
This project uses CustomVision.AI to detect FRC field objects (in the case of this model, a prototype of the 2019 hatch).
CustomVision.AI exports to a .onnx file that is used within my program to detect the object itself, then the Python program runs vision math on the supplied co-ordinates of the detected object (if it is detected)
to find out where it is in space.

## Current State, and where to go next
This project is for the [BOS Raspberry Pi Contest](https://bosinnovations.ca/first/).


Currently, the program detects the hatch quite well (see google doc), and vision math finds distance to the object reasonably well. It also has foundation code for sending the vision results back over to the roboRIO to use to control the robot.

Next, I need to fine-tune the distance math and find angles to the target to port into solvePnP() to detect where the robots are in 3D space, and after that, port this program to a Raspberry Pi.

### Want to learn more?
[Google Doc](https://docs.google.com/document/d/1wLhM5ahvdox7a_Fom5_leUtu3d5cdZXE6BZQBcUypsc/edit?usp=sharing)
