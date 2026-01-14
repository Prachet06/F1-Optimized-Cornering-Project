from pydualsense import pydualsense
import time
import mss
import mss.tools

# TODO: Add logic so that times you hit the brakes in sector 1 counts and nothing else does
#       one way to enforce this would be having a button to mark to mark the end and start of ]
#       sector one.

# TODO: Ensure that the screenshots are not overwritten, maybe through the use of input each 
#       time you run the program

# TODO: Improve screenshot saves based on the inputs idea from above, so that each session's 
#       image data is saved in a separate folder

# TODO: Maybe add something to delete/ remove previous accidental screenshots
 
print('''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣶⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣤ ⣿⣿⣿⣿⡇⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣠⣤⣶⣾⣿⣿⡿⠀⣿⣿⣿⣿⡇⠀⢰⣶⣿⣿⣿⠿⠿⢿⣶⣦⣤⡀
⢰⣿⣿⣿⡿⠛⠉⢀⣀⠀⣿⣿⣿⣿⡇⠀⠘⠋⠉⠀⣀⣠⣴⣾⣿⣿⣿⠇
⠈⠻⠿⣿⣿⣿⣿⣿⠿⠀⣿⣿⣿⣿⡇⠀⢠⣶⣾⣿⣿⡿⠿⠟⠋⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠿⢿⡇⠀⠸⠟⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
''')
print("Running...... (press SHARE to exit)")


ds = pydualsense()
ds.init()

count = 0
was_pressed = False

try:
    

    while True:
        state = ds.state
        is_pressed = bool(state.L2)

        if is_pressed and not was_pressed:
            count += 1
            print(f"L2 press #{count}")
            # Triggering and saving screenshots below
            with mss.mss() as sct:
                # Get information for the laptop screen (monitor 1 at index 1)
                monitor = sct.monitors[1] 
                # Grab the data
                sct_img = sct.grab(monitor)
                # Save the picture 
                filename = f"Break hit #{count}.png"
                file_loc = f"../Data/Image Data/Break hit #{count}.png"
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=file_loc)
                print(f"Screenshot saved as: {filename}")

        was_pressed = is_pressed

        if state.share:
            print("Share pressed, exiting")
            break

        time.sleep(0.01)
finally:
    ds.close()

