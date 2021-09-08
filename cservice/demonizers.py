import daemon
import signal
import socket
import sys
import pid
from datetime import datetime
import builtins
from systemd.daemon import notify


class Service:
    def __init__(self, name, **kwargs):
        self.name = name
        # may be argsparse later?
        self.systemd = True if '-systemd' in sys.argv else False
        self.not_daemonize = True if '-not-daemonize' in sys.argv else False

        self.detach_process = False if self.systemd or self.not_daemonize else True

        if self.not_daemonize:
            self.f_log = sys.stdout
            self.f_err = sys.stderr
        else:
            self.f_log = open('/var/tmp/' + self.name + '.log', 'ab', 0)
            self.f_err = open('/var/tmp/' + self.name + '.err', 'ab', 0)

        self.dcontext = daemon.DaemonContext(pidfile=pid.PidFile(self.name, '/var/tmp',),
                                             detach_process=self.detach_process,
                                             stdout=self.f_log,
                                             stderr=self.f_err)
        self.dcontext.signal_map = {
            signal.SIGTERM: self.exit_proc,  #
            signal.SIGINT: self.exit_proc,  # Ctrl + c reaction
        }

        self.print = builtins.print
        builtins.print = self.log_str

        with self.dcontext:
            print('starting service: ' + self.name)
            self.pre_run()
            self.main()
            if self.systemd:
                notify('READY=1')
            print('data loaded, going to main loop')
            self.run_main_loop()

    def exit_proc(self, signum, frame):
        self.log_str('signal recieved: %d, %s' % (signum, frame))
        if self.systemd:
            notify('STOPPING=1')
        self.clean_proc()
        self.quit_main_loop()

    def log_str(self, *args):
        self.print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), ': ', *args, flush=True)

    def run_main_loop(self):
        pass

    def quit_main_loop(self):
        pass

    def pre_run(self):
        #function to initialize context here
        pass

    def main(self):
        pass

    def clean_proc(self):
        pass


class QtService(Service):
    def __init__(self, name, **kwargs):
        self.app = None
        super().__init__(name, **kwargs)

    def pre_run(self):
        global QtCore
        import cxwidgets.aQt.QtCore as QtCore

        self.app = QtCore.QCoreApplication(sys.argv)

    def run_main_loop(self):
        self.app.exec_()

    def quit_main_loop(self):
        self.app.quit()


class CothreadQtService(Service):
    def __init__(self, name, **kwargs):
        self.app = None
        super().__init__(name, **kwargs)

    def run_main_loop(self):
        global cothread
        cothread.WaitForQuit()

    def quit_main_loop(self):
        self.app.quit()

    def pre_run(self):
        global QtCore, cothread
        from cxwidgets.aQt import QtCore
        import cothread

        self.app = QtCore.QCoreApplication(sys.argv)
        cothread.iqt()


class CXService(Service):
    def run_main_loop(self):
        global cda
        import pycx4.pycda as cda

        # Create a socket pair for waking up from cda's select()
        self.wsock, self.rsock = socket.socketpair(type=socket.SOCK_DGRAM)
        self.wsock.setblocking(False) # required by signal library
        self.old_fd = signal.set_wakeup_fd(self.wsock.fileno())
        # Create Fd event fpr CX scheduler main loop
        self.wakeup_ev = cda.FdEvent(self.rsock)
        # call to self.wakeup_proc will return execution to python interpriter
        # on tests after that python's signal processing called first, then
        # self.wakeup_proc
        self.wakeup_ev.ready.connect(self.wakeup_proc)
        # may be change to dummy handler lake that:
        #self.wakeup_ev.ready.connect(lambda : None)
        # since really not required to processsignals in wakeup proc

        cda.main_loop()

    def quit_main_loop(self):
        global cda
        import pycx4.pycda as cda
        cda.break_()

    def wakeup_proc(self, ev):
        data = self.rsock.recv(1)
        print('wake up with:', data)
