import sys, os, signal
from multiprocessing import Process
import nimporter
from tinyhttp import tinyhttp


class HttpServer:
    """
    Runs a fast HTTP server for static files in another process. Seperate
    process is needed because Nimpy doesn't release the GIL.
    """
    def __init__(self, folder='.', host='localhost', port=8080, log=False, autostop=False):
        self.get_host = lambda self: host
        self.get_port = lambda self: port
        self.get_folder = lambda self: folder
        self.proc = Process(
            target=tinyhttp.serve_static_files,
            args=(host, port, folder, log)
        )
        self.autostop = autostop

    def __del__(self):
        if self.autostop: self.stop()
        
    def start(self):
        self.proc.start()

    def stop(self):
        try:
            os.kill(self.proc.pid, signal.SIGINT)
        except:
            self.proc.kill()
        finally:
            self.proc.join()
            self.proc.close()


def main(args=None):
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Fast Static File HTTP Server')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8080, type=int)
    parser.add_argument('--dir', default='.')
    __ver_str = (Path(__file__).parent.parent / 'VERSION.txt').read_text()
    ver = '%(prog)s ' + __ver_str
    parser.add_argument(
        '--version',
        action='version',
        version=ver
    )

    args = parser.parse_args(args or sys.argv[1:])
    server = HttpServer(args.dir, args.host, args.port, True)
    server.start()

if __name__ == '__main__':
    main()
