from threading import Thread
import continues
from app_dash import app

def run():
    t_continues = Thread(target=continues.main, args=())
    t_continues.start()
    app.run_server(host='0.0.0.0', debug=False)
    t_continues.join()


if __name__ == '__main__':
    run()
