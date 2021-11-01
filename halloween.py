#!/usr/bin/python3

from Raspi_MotorHAT import Raspi_MotorHAT
from gpiozero import MotionSensor
import gpiozero
import atexit
import time
import random
import subprocess

command = 'vlc --x11-display :0 --no-osd --play-and-exit --no-video-deco --no-embedded-video -f --one-instance --no-playlist-enqueue '
pir = MotionSensor(4)
mh = Raspi_MotorHAT(0x6F)
RELAY_PIN = 17

video = [
    'BC_DancingDead_Win_Black_V.mp4',
    'BC_FearTheReaper_Holl_V.mp4',
    'BC_GatheringGhouls_Holl_V.mp4',
    'BC_SkeletonSurprise_Holl_V.mp4',
    'BC_PopUpPanic_Holl_V.mp4',
    'BC_JitteryBones_Holl_V.mp4',
    'BC_Numskulls_Holl_V.mp4'
]

# Triggered by the output pin going high: active_high=True
# Initially off: initial_value=False
relay = gpiozero.OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

myStepper1 = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper1.setSpeed(60)                 # 30 RPM


# recommended for auto-disabling motors on shutdown
def turnOffMotors():
    mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)


atexit.register(turnOffMotors)


def fog_status(relay_stat):
    if relay_stat == 0:
        fog = 'off'
    else:
        fog = 'on'
    return fog


def shoot_fog(seconds):
    relay.on()  # switch on
    time.sleep(seconds)
    relay.off()  # switch off


def main():
    while True:
        if pir.motion_detected:
            vid = '/home/pi/static/' + random.choice(video)
            print("Motion Detected - Playing " + str(vid))
            shoot_fog(2)
            subprocess.run(command + vid, shell=True)
            myStepper1.step(500, Raspi_MotorHAT.FORWARD,
                            Raspi_MotorHAT.DOUBLE)
            myStepper1.step(500, Raspi_MotorHAT.BACKWARD,
                            Raspi_MotorHAT.DOUBLE)
        else:
            print("Motion Not Detected - Fog is " + fog_status(relay.value))
            relay.off()  # switch off


if __name__ == "__main__":
    main()
