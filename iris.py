import time
from Tkinter import *
import cwiid
from collections import deque
import os

GESTURE_CHECK_FREQUENCY = 10
MAX_QUEUE_LENGTH = 300
TOLERANCE = 4
STRENGTH = 23

#list of tasks:
#'w' = watchful
#'s' = clear_stack
#'h' = say_hi
#'c' = connect

#Main class
class Iris:
    def __init__(self):
        self.connected = False
        #A long term memory of gestures
        self.memory = []
        #A short term memory of states
        self.queue
        #A short term memory of recent gestures
        self.stack = deque([])
        #A string literal containing the next task
        self.next_task = 'c'

    def cont(self):
        if self.next_task == 'w':
            self.watchful()
        elif self.next_task == 's':
            self.clear_stack()
        elif self.next_task == 'c':
            self.connect()
        elif self.next_task == 'h':
            self.say_hi()
        elif self.next_task == 'r':
            self.record_gesture()
        elif self.next_task == 'e':
            exit()
        else:
            pass

#The following methods are for the WATCHFUL state

    #The Application's default state
    def watchful(self):
        print("Watchful")
        self.record(GESTURE_CHECK_FREQUENCY)
        if len(self.queue) == MAX_QUEUE_LENGTH:
            print "\n\nQueue:  ", len(self.queue), "\n\n"
            path = gesture_to_path(list(self.queue))
            print "\n\nPath:  ", len(path), "\n\n"
            path_command = self.check_path(path)
            if path_command != None:
                self.stack.append(path_command)

        #NEEDS IMPROVEMENT: implement larger stacks
        if len(self.stack) > 0:
            self.next_task = 's'


    def record(self,no_of_snapshots):
        print("Recording...")
        for i in range(no_of_snapshots):
            #this method accounts for the fact that the ir camera occasionally
            #fails to record a state, in which case the camera returns 'None'
            state = self.wm.state
            if state['ir_src'][0] != None:
                print("State accepted:\t", state['ir_src'][0]['pos'])
                self.queue.append(state['ir_src'][0]['pos'])
            #if the camera returns 'None' then the method leaves a copy of the
            #previous position in the deque
            elif len(self.queue) > 0:
                print("State rejected, appending previous...")
                self.queue.append(self.queue[-1])
            #unless there is no previous position, in which case it defaults to
            #the origin
            else:
                print("State rejected, appending (0,0)...")
                self.queue.append((0,0))
            if len(self.queue) > MAX_QUEUE_LENGTH:
                print("Removing oldest state")
                junk = self.queue.popleft()
            #Note: Higher point-capture frequency
            time.sleep(.01)

    def check_path(self, path):
        print("Checking path")
        test_value = 0
        found = False

        #NEEDS WORK

        for gesture in self.memory:
            #print("Hi")
            for i in range(30):
                try:
                    if abs(gesture[1][i][0] - path[i][0]) <= TOLERANCE:
                        if abs(gesture[1][i][1] - path[i][1]) <= TOLERANCE:
                            test_value += 1
                except IndexError:
                    print "\n\n", i, "\t", len(gesture[1]), gesture,"\n\n", len(path),path, "\n\nOoops"
                    exit()
            if test_value >= STRENGTH:
                found = True
                return (gesture[0])
        if not found:
            return None

#The following methods relate to the STACK

    def clear_stack(self):
        print("Clearing Stack")
        task = self.stack.popleft()
        self.perform(task)
        if len(self.stack) == 0 and self.next_task == 's':
            self.next_task = 'w'

    def perform(self,task):
        print("Performing task:\t", task)
        if task == "F":
            os.system("firefox www.facebook.com")
            self.next_task = 'e'
        else:
            print("Task Unrecognised")

    #Method to check I can interact with the ui
    def say_hi(self):
        print("hi there!")


#The following methods relate to the Memory

    def record_gesture(self):
        print('Recording gesture')
        self.record(MAX_QUEUE_LENGTH)
        print('Here')
        #name = input('Name of gesture:\t')
        self.memory.append(['F',gesture_to_path(list(self.queue))])
        self.queue.clear()
        print(self.memory[0])
        self.next_task = 'w'
#The following methods relate to the Wiimote

    #Method to connect to the Wiimote
    def connect(self):
        print("Connecting")
        #connects
        self.wm = cwiid.Wiimote()
        #changes the report mode to include buttons, camera and accelerometer
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_IR | cwiid.RPT_ACC
        #prints state to indicate a successful connection
        print(self.wm.state)
        #Alerts the ui the wiimote is connected
        #self.vel_label["text"] = "Ready"
        self.connected = True
        #self.update()

    #prints state of wiimote
    def p(self):
        print(self.wm.state)

    #prints state of wiimote every 0.1 seconds for 5 seconds
    def log(self):
        for i in range(50):
            self.p()

    #Two methods to interact with the wiimote
    def yay(self):
        print("Yay")
        for i in range(16):
            self.wm.led = 2**(i % 4)
            time.sleep(0.1)
        for i in range(16):
            self.wm.led = 2**(-i % 4)
            time.sleep(0.1)
        for i in range(16):
            if i % 2 == 1:
                self.wm.led = 9
            else:
                self.wm.led = 6
            time.sleep(0.1)
        self.wm.led = 0

    def boo(self):
        print('boo')
        self.wm.led = 1
        time.sleep(2)
        self.wm.led = 0
        time.sleep(.1)

def gesture_to_path(a):
    print("Gesture to path")
    if len(a) != MAX_QUEUE_LENGTH:
        print("Failed attempt at gesture_to_path:  ", a)
        pass

    dist = [0]
    for i in range(len(a)-1):
        dist.append(dist[i] + ((a[i+1][0] - a[i][0])**2 + (a[i+1][0] - a[i][0])**2)**0.5)

    i = 0
    path_length = dist[-1]
    path = []
    for j in range(len(dist)):
        print(i)
        if dist[j] >= (path_length * i / 30) and len(path) < 30:
            path.append(a[j])
            i += 1
    if len(path) != 30:
        print("Path length wrong!", len(path))

    mean = [sum(path[i][0] for i in range(len(path))), sum(path[i][1] for i in range(len(path)))]
    #scale currently 10*(sum of all
    scale = sum((abs(path[i][0] - mean[0])**2 + abs(path[i][1] - mean[1])**2)**0.5 for i in range(len(path)))
    if scale != 0:
        path = [(int((path[i][0]-mean[0])*1000/scale), int((path[i][1]-mean[1])*1000/scale)) for i in range(len(path))]
    else:
        path = [(int((path[i][0]-mean[0])), int((path[i][1]-mean[1]))) for i in range(len(path))]

    return path

def main():
    print('start')
    iris = Iris()
    iris.cont()
    iris.next_task = 'r'
    time.sleep(1)
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print("Go!")
    iris.cont()
    print(iris.memory)

main()
##for i in range(50):
##    print(i)
##    #print(iris.next_task)
##    iris.cont()
##    print(i)
