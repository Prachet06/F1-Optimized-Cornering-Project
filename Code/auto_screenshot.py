from pydualsense import pydualsense
import time

# TODO: Add logic so that times you hit the brakes in sector 1 counts and nothing else does
#       one way to enforce this would be having a button to mark to mark the end and start of ]
#       sector one.

# TODO: Add code for screenshotting using a library that allows that to happen fast 

ds = pydualsense()
ds.init()

count = 0
was_pressed = False

try:
    print("Running...... (press SHARE to exit)")

    while True:
        state = ds.state
        is_pressed = bool(state.L2)

        if is_pressed and not was_pressed:
            count += 1
            print(f"L2 press #{count}")
            # TODO: trigger screenshot here

        was_pressed = is_pressed

        if state.share:
            print("Share pressed, exiting")
            break

        time.sleep(0.01)
finally:
    ds.close()