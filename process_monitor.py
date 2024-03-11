import sys


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/tmp/process_monitor.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


sys.stdout = Logger()
sys.stderr = sys.stdout

import os
import time
import logging
import subprocess
import rumps


class ProcessMonitor(rumps.App):
    def __init__(self):
        super(ProcessMonitor, self).__init__("")
        self.process_name = "/Users/zdwiel/src/drives-watcher/run_drives.sh"
        self.check_interval = 1
        self.tmux_session = "process_monitor"
        self.green_icon = "green_circle.png"
        self.red_icon = "red_circle.png"
        self.kill_tmux_on_exit = True
        self.logger = self.setup_logging()
        self.start_monitoring()
        self.menu = ["Open iTerm2"]

    def setup_logging(self):
        logger = logging.getLogger("process_monitor")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("process_monitor.log")
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def start_monitoring(self):
        self.logger.info("Starting process monitoring...")
        try:
            subprocess.check_output(["tmux", "has-session", "-t", self.tmux_session])
        except subprocess.CalledProcessError:
            subprocess.Popen(
                [
                    "tmux",
                    "new-session",
                    "-d",
                    "-s",
                    self.tmux_session,
                    "-n",
                    "monitoring",
                ]
            )
        else:
            subprocess.Popen(
                ["tmux", "new-window", "-t", self.tmux_session + ":monitoring"]
            )

    @rumps.clicked("Open iTerm2")
    def open_iterm2(self, _):
        # subprocess.Popen(["osascript", "-e", 'tell application "iTerm" to activate', "-e", 'tell application "System Events" to tell process "iTerm" to keystroke "t" using command down', "-e", 'tell application "System Events" to tell process "iTerm" to keystroke "tmux attach -t {}"'.format(self.tmux_session), "-e", 'tell application "System Events" to tell process "iTerm" to key code 52'])
        self.open_iterm2_and_attach(_)

    def open_iterm2_and_attach(self, _):
        # Create a new iTerm2 window with default profile and attach to the tmux session
        subprocess.Popen(
            [
                "osascript",
                "-e",
                'tell application "iTerm2" to create window with default profile command'
                '"/opt/homebrew/bin/tmux attach-session -t ' + self.tmux_session + '"',
            ]
        )

    @rumps.timer(1)
    def monitor_process(self, _):
        if self.is_process_running():
            self.icon = self.green_icon
        else:
            self.icon = self.red_icon
            self.restart_process()

    def is_process_running(self):
        try:
            subprocess.check_output(["pgrep", "-f", self.process_name])
            print("process is running")
            return True
        except subprocess.CalledProcessError:
            return False

    def restart_process(self):
        if not self.is_process_running():
            self.logger.info("Starting process: %s", self.process_name)
            subprocess.Popen(
                [
                    "tmux",
                    "send-keys",
                    "-t",
                    self.tmux_session + ":monitoring",
                    self.process_name,
                    "Enter",
                ]
            )
        else:
            self.logger.info("Process is already running: %s", self.process_name)

    def cleanup(self):
        print("cleanup")
        if self.kill_tmux_on_exit:
            self.logger.info("Killing tmux session: %s", self.tmux_session)
            subprocess.Popen(["tmux", "kill-session", "-t", self.tmux_session])


if __name__ == "__main__":
    process_monitor = ProcessMonitor()
    process_monitor.run()
