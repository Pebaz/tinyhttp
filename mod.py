import os, signal
from multiprocessing import Process
import nimporter, tinyhttp


class HttpServer:
    """
    Runs a fast HTTP server for static files in another process. Seperate
    process is needed because Nimpy doesn't release the GIL.
    """
    def __init__(self, folder='.', host='localhost', port=9090):
        self.get_host = lambda self: host
        self.get_port = lambda self: port
        self.get_folder = lambda self: folder
        self.proc = Process(
            target=tinyhttp.serve_static_files,
            args=(host, port, folder)
        )
        
    def start(self):
        proc.start()

    def stop(self):
        try:
            os.kill(self.proc.pid, signal.SIGINT)
        except:
            self.proc.kill()
        finally:
            self.proc.join()
            self.proc.close()


def main():
    import sys
    pass
