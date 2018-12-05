# Design Document

Sam Aronson

### Intro

For this project, the goal is to reach the exit tile before running out of fuel. To reach this goal, managing  fuel consumption is crucial and the primary goal of the AI. In this document, first we will discuss the approach the AI will take to optimize fuel consumption, and then the specific techniques and approaches that will be used for each individual task.

### Fuel Management and Optimization

First, we must understand the factors that affect fuel throughout the game for the AI. These are described in Figure 1 below.

![img](/Users/local/QUAKER/saronson/Documents/cs107-p8/imgs_design/fuelconsumption.png)

The ways that fuel can be gained is quite simple. An allotment of 30 is given at the beginning of the game, and then 3 fuel is earned for each half second spent in the game. Additionally, healthpacks can be used to increase fuel, but I do not believe that it is cost-effective to seek them.

However, considering that the overall goal of this project is to maximize my grade, we will still be seeking for healthpacks.

Instead, to conserve fuel the following goals will be set for the AI

* Try to move to the exit tile as efficiently as possible using a known location of the exit tile
* Avoid stones and ferrets
* Eliminated ferrets through shooting them
* Seek out healthpacks
* Try to minimize the number of times information about ferret and exit tile locations are quered

#### AI Design

![img](/Users/local/QUAKER/saronson/Documents/cs107-p8/imgs_design/overview.png)

The AI wll be designed to execute actions using three components shown in Figure 2: a path manager, fuel manager, and shooting manager (if I have time). Additionally, a stone tracker will be implemented to aid the decision making components.

The fuel manager will ensure that enough fuel has been accumulated for whatever the next task is (be it moving to another part of the map, or waiting to move). The fuel manager will first "save up" fuel to find the healthpacks and approach the nearest one.

The path manager will determine the path the squirrel should take when it is time to mvoe to either a healthpack or the exit tile

The shooting manager will attempt to track the ferrets and shoot at them.

The shooting manager and path manager will be informed by the stone/ferret tracker, which will attempt to track the stones to find the ferrets and avoid more dangerous regions of the map.

##### Fuel Manager

The fuel manager will alternate between two stages.

###### Fuel Collection:

 In this stage, the squirrel will be mostly stationary, only moving to avoid stones and gain the information needed to determine the next segement of the squirrel's path. The goal is to stockpile fuel until it is ready for the advancement stage.

###### Advancement:

In this stage, the path manager is enabled to go to it's next waypoint (either a healthpack or the exit tile.

##### Path Manager:

The path manager will attempt to generate paths for the AI to execute. It will use the methods built in project 6 to find an acceptable path. It will be informed by the stone/ferret tracker, to try to avoid "hotspots" of activity. If this is impossible, we will use additional caution in these areas, attempting to track the ferrets.

##### Shooting Manager:

The shooting manager will use the getFerret() method and predictions made by the stone/ferret tracker to try to accurately assess where the squirrels will be to shoot the stones in the correct direction.

##### Stone/ferret tracker:

The stone/ferret tracker will attempt to use getStone() to find stones and ferrets. As shown in Figure 3, the stones locations may change every clocktick, but they should be trackable to their original position, which will be very close to the ferret. By tracking the path of the stone, we will be able to predict it's future path (helpful for avoidance), and the location of the shooter

![img](/Users/local/QUAKER/saronson/Documents/cs107-p8/imgs_design/stone_backprop.png)

Furthermore, if the shooter is moving, we will at the very least be able to create a heatmap of tiles to attempt to avoid. By using these methods, we can get "close" to the dangerous regions, and then use getFerret() to more accurately shoot at the ferrets. We can also attempt to avoid these more dangerous areas by trying to generate a path around them. 

![img](/Users/local/QUAKER/saronson/Documents/cs107-p8/imgs_design/ferret_heatmap.png)

### Conclusion

Through tracking stones, I will create an AI that is informed as to where its opponents lie on the map, while still creating an efficient solution to play HaverQuest.