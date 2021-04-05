import continues
import camera

def save_config(config):
    """
    process of saving configuration

    1. stop the continues and recording service
    2. apply the configuration
    3. start the continues and recording service again
    """
    continues.stop_recording()
    camera.set_config(config)
    camera.save_config()
    continues.start_thread()
    return config