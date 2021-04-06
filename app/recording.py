import continues
import camera
import time

continues.start_thread()
time.sleep(3)
continues.stop_recording()
camera.set_config({
        "rotation":0, 
        "resolution":"1024x768", 
        "framerate":21
        })
camera.save_config()
continues.start_thread()