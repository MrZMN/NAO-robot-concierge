import motion
import almath
from naoqi import ALProxy
from naoqi import ALModule


# this file enables some movement examples by NAOQi

class MoveModule(ALModule):

    def __init__(self, name, ip, port):
        ALModule.__init__(self, name)

        self.motion = ALProxy("ALMotion", ip, port)
        self.posture = ALProxy("ALRobotPosture", ip, port)

        # Init
        self.motion.setStiffnesses("Body", 0.9)	    # set so that robot can move
        #self.motion.moveInit()

    def standUp(self):
        self.posture.goToPosture("Stand", 1.0)
        
    def sitDown(self):
        self.posture.goToPosture("Sit", 1.0)

    def walkTo(self, x, y, z):
        wald_id = self.motion.post.moveTo(x, y, z)
        self.motion.wait(wald_id, 0)	# whether in parallel
        
        
    def hulaHoop(self):
        self.posture.goToPosture("StandInit", 0.5)
        
        # end go to Stand Init, begin define control point
        effector        = "Torso"
        frame           = motion.FRAME_ROBOT
        axisMask        = almath.AXIS_MASK_ALL
        isAbsolute      = True
        useSensorValues = False

        currentTf = almath.Transform(self.motion.getTransform(effector, frame, useSensorValues))

        # end define control point, begin define target

        # Define the changes relative to the current position
        dx         = 0.03                    # translation axis X (meter)
        dy         = 0.03                    # translation axis Y (meter)
        dwx        = 8.0*almath.TO_RAD       # rotation axis X (rad)
        dwy        = 8.0*almath.TO_RAD       # rotation axis Y (rad)

        # point 01 : forward  / bend backward
        target1Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
        target1Tf *= almath.Transform(dx, 0.0, 0.0)
        target1Tf *= almath.Transform().fromRotY(-dwy)

        # point 02 : right    / bend left
        target2Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
        target2Tf *= almath.Transform(0.0, -dy, 0.0)
        target2Tf *= almath.Transform().fromRotX(-dwx)

        # point 03 : backward / bend forward
        target3Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
        target3Tf *= almath.Transform(-dx, 0.0, 0.0)
        target3Tf *= almath.Transform().fromRotY(dwy)

        # point 04 : left     / bend right
        target4Tf = almath.Transform(currentTf.r1_c4, currentTf.r2_c4, currentTf.r3_c4)
        target4Tf *= almath.Transform(0.0, dy, 0.0)
        target4Tf *= almath.Transform().fromRotX(dwx)

        path = []
        path.append(list(target1Tf.toVector()))
        path.append(list(target2Tf.toVector()))
        path.append(list(target3Tf.toVector()))
        path.append(list(target4Tf.toVector()))

        path.append(list(target1Tf.toVector()))
        path.append(list(target2Tf.toVector()))
        path.append(list(target3Tf.toVector()))
        path.append(list(target4Tf.toVector()))

        path.append(list(target1Tf.toVector()))
        path.append(list(currentTf.toVector()))

        timeOneMove  = 0.5 #seconds
        times = []
        for i in range(len(path)):
            times.append((i+1)*timeOneMove)

        # end define target, begin call motion api

        # call the cartesian control API

        self.motion.transformInterpolations(effector, frame, path, axisMask, times)

        # Go to rest position
        # self.motion.rest()
        
        self.posture.goToPosture("Stand", 1.0)

        


#http://doc.aldebaran.com/2-1/dev/python/making_nao_move.html
#http://doc.aldebaran.com/2-1/naoqi/motion/alrobotposture.html#alrobotposture
