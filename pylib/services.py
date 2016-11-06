def __run_celery_server():
    # celery - A tasks worker - -loglevel = info
    import subprocess
    args = ['celery', '-A', 'tasks', 'worker', '--loglevel=debug']
    pipe = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = pipe.communicate()
    code = pipe.returncode

def run_services():
    from multiprocessing import Process
    celery_server = Process(target=__run_celery_server)
    celery_server.start()
    print "Celery pid={}".format(celery_server.pid)




