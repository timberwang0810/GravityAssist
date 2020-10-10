from visual import*
from visual.graph import *

scene.title = 'Base'
scene.width= 600
scene.height= 600
#
# Setup the graphics display.
gdisplay(title='Project', xtitle='Distance', ytitle='Velocity'\
         ,xmax=778.5e9+(778.5e9-1.5e11)/2,xmin=5e11, ymax=60000, ymin=0, width=500, height=500)
#
# Gravitational Constant
#
massArray=[1.898e27,3.796e27,5.694e27,7.592e27,9.49e27]
velocityArray=[]
plotArray=[]
i=0
aPlot = gcurve(color=color.cyan)
bPlot = gcurve(color=color.green)
cPlot = gcurve(color=color.yellow)
dPlot = gcurve(color=color.magenta)
ePlot = gcurve(color=color.blue)
plotArray.append(aPlot)
plotArray.append(bPlot)
plotArray.append(cPlot)
plotArray.append(dPlot)
plotArray.append(ePlot)
while (i<len(massArray)):
    vAdd=0
    
    pi=3.14159
    G =6.67e-11
    dt = 5000
    timeDelay=1.008e8
    distanceCap=778.5e9+(778.5e9-1.5e11)/2
    capped=False
    #
    # Set up the Earth and the Sun:
    #
    sun = sphere(pos=(0,0,0), radius=7e9, color=color.yellow)
    sun.mass = 1.9891e30
    #
    earth = sphere(pos=(1.5e11,0,0), radius=3.2e9, color=color.cyan)
    earth.mass = 5.97636e24
    jupiter = sphere(pos=(778.5e9,0,0), radius=3.2e9, color=color.green)
    jupiter.mass = massArray[i]
    #
    # Set up a circular orbit - one orbit per year.
    #
    year = 2*pi*(((mag(earth.pos-sun.pos))**3)/(G*sun.mass))**0.5
    earthspeed = (6.28)*(earth.pos.x)/year
    earth.momentum = vector(0.,earth.mass*earthspeed,0.)
    #
    jupYear=2*pi*(((mag(jupiter.pos-sun.pos))**3)/(G*sun.mass))**0.5
    jupiterspeed = (6.28)*(jupiter.pos.x)/jupYear
    jupiter.momentum = vector(0.,jupiter.mass*jupiterspeed,0.)
    #
    spaceship= sphere(pos=earth.pos,radius=3.2e9,color=color.red)
    spaceship.mass=800
    spaceshipspeed=25000
    spaceship.momentum=None
    #
    # Have the Earth Leave a Trail
    #
    trailE= curve(color=earth.color)
    trailJ= curve(color=jupiter.color)
    trailS= curve(color=spaceship.color)
    #
    # Lets do two years -- wont work for elliptical orbits.
    #
    #scene.autoscale=0
    #
    
    t=0
    origM=(jupiter.momentum)
    # (Re)initialize
    while not capped:
        
        rate(10000)
        #
        # Get the force on the Earth:
        #
        earth.force = -(G * earth.mass * sun.mass) *\
                       norm(earth.pos-sun.pos)/((mag(earth.pos-sun.pos))**2)
        jupiter.force = -(G * jupiter.mass * sun.mass) *\
                      norm(jupiter.pos-sun.pos)/((mag(jupiter.pos-sun.pos))**2)
        spaceship.force= -(G * jupiter.mass * spaceship.mass) *\
                     norm(spaceship.pos-jupiter.pos)/((mag(spaceship.pos-jupiter.pos))**2)\
                     -(G * sun.mass * spaceship.mass) *\
                      norm(spaceship.pos-sun.pos)/((mag(spaceship.pos-sun.pos))**2)\
                     -(G * earth.mass * spaceship.mass) *\
                     norm(spaceship.pos-earth.pos)/((mag(spaceship.pos-earth.pos))**2)
     #   
        # Update the Earth's momentum and position:
        #
        # Launch
        earth.momentum += earth.force*dt
        earth.pos += (earth.momentum/earth.mass)*dt
     #
        jupiter.momentum += jupiter.force*dt
        jupiter.pos += (jupiter.momentum/jupiter.mass)*dt
        #
        if t>=timeDelay and spaceship.momentum==None:
            spaceship.momentum=spaceship.mass*spaceshipspeed*\
                                cross(norm(earth.momentum),vector(0,0,1))\
                                +(earth.momentum/earth.mass)*spaceship.mass
        elif spaceship.momentum!=None:
            spaceship.momentum += spaceship.force*dt
            spaceship.pos+= (spaceship.momentum/spaceship.mass)*dt
            d=mag(spaceship.pos-sun.pos)
            s=mag(spaceship.momentum)/spaceship.mass
            if (d<=7.8e11 and d>=7.786e11) and (vAdd==0):
                velocityArray.append(s)
                vAdd = 1
            currPlot=plotArray[i]
            currPlot.plot(pos=(d,s))
        else:
            spaceship.pos=earth.pos
    
        if mag(spaceship.pos-jupiter.pos)<=1000:
            print(mag(spaceship.momentum)/spaceship.mass)
    
        trailE.append(pos=earth.pos)
        #
        trailJ.append(pos=jupiter.pos)
        #
        trailS.append(pos=spaceship.pos)
        #
        if mag(spaceship.pos-sun.pos)>=distanceCap:
            capped=True
        #
        # Increment the time:
        #
        t+=dt
    
    i+=1
#
print("Done with Orbits")
print(mag(spaceship.momentum)/spaceship.mass)
print massArray
print velocityArray
#
