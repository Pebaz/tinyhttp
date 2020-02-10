import sys, os, signal
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
    ver = '%(prog)s ' + (Path(__file__).parent / 'VERSION.txt').read_text()
    parser.add_argument(
        '--version',
        action='version',
        version=ver
    )

    args = parser.parse_args(args or sys.argv[1:])
    server = HttpServer(folder=args.dir, host=args.host, port=args.port)
    server.start()

if __name__ == '__main__':
    main()
