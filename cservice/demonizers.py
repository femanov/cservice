import daemon
import signal
import sys
import pid
from datetime import datetime
import builtins


class Service:
    def __init__(self, name, **kwargs):
        self.name = name
        self.f_log = open('/var/tmp/' + self.name + '.log', 'ab', 0)
        self.f_err = open('/var/tmp/' + self.name + '.err', 'ab', 0)
        self.dcontext = daemon.DaemonContext(pidfile=pid.PidFile(self.name, '/var/tmp',), stdout=self.f_log, stderr=self.f_err)

        self.dcontext.signal_map = {
            signal.SIGTERM: self.exit_proc,
        }

        redef_print = kwargs.get('redef_print', False)
        self.print = builtins.print
        if redef_print:
            builtins.print = self.log_str

        # may be argparse later
        if '-not-daemonize' in sys.argv:
            print('runnind without forking demonization')
            self.pre_run()
            self.main()
            self.run_main_loop()
        else:
            with self.dcontext:
                self.log_str('starting service: ' + self.name)
                self.pre_run()
                self.main()
                self.run_main_loop()

    def exit_proc(self, signum, frame):
        self.log_str('signal recieved: %d, %s' % (signum, frame))
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
        cda.main_loop()

    def quit_main_loop(self):
        global cda
        import pycx4.pycda as cda
        cda.break_()
