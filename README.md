# Raspberry Pi Machine Learning Vision for FRC

## Inspiration 
Vision tracking for FRC (FIRST Robotics Competition) is often a huge hassle for teams to complete, especially since they are only given 6 weeks to program it to detect that year's field objects. And that doesn't take into account how little time the programmers have time with the robot during that 6-week period!

## What does it do?
This project uses CustomVision.AI to detect FRC field objects using machine learning (in the case of this model, a 2016 FRC Stronghold ball).
CustomVision.AI exports to Tensorflow and Onnx, which is used within my program to detect the object itself, then the Python program runs vision math on the supplied co-ordinates of any detected object.
to find out where it is in space. 

## Current State
We switched from ONNX to Tensorflow in order to run this project on non-Windows systems—specifically the Raspberry Pi.
This project is for the [BOS Raspberry Pi Contest](https://bosinnovations.ca/first/).

Currently, the program detects the object, and runs vision calculations to find distance to the object. It sends this information over the robot network using PyNetworkTables for additional processing on the roboRIO (e.g; pathfinding).

## Next Steps
We’d love to optimize our machine learning model by ditching CustomVision.AI and Tensorflow entirely and instead running the model on an OpenCV Dynamic Neural Network, and using all four cores on the Raspberry Pi. With this change, the vision program will be able to run in complete realtime—opening its use for on-the-fly pathfinding in the autonomous period and lining up with targets during the teleoperated period. Additionally, we’d love to extract 3D-world co-ordinates from the detected object using OpenCV, allowing us to go from driving straight with PID loops to generating paths on the fly with Pathfinder to get our robot to swerve directly to its target.

### Want to learn more?
[NEW Google Doc, September 2019, using Tensorflow](https://docs.google.com/document/d/1xEkql4t2k2on5pWODVsJKmNB83CbAXsfhYoOYy8iIx8/edit?usp=sharing)

[Google Doc (June 2019, using ONNX)](https://docs.google.com/document/d/1wLhM5ahvdox7a_Fom5_leUtu3d5cdZXE6BZQBcUypsc/edit?usp=sharing)

Winning Facebook post: https://www.facebook.com/bosInnovations/videos/1325857704252193/
