from multiprocessing import Process
import os, signal
import nimporter, tinyhttp

# Need to run the http server in another process since Nimpy doesn't release GIL
proc = Process(
    target=tinyhttp.serve_static_files,
    args=('0.0.0.0', 9090, '..')
)
proc.start()
import time
time.sleep(10)
try:
    os.kill(proc.pid, signal.SIGINT)
except:
    proc.kill()
proc.join()
proc.close()
print('Done')
