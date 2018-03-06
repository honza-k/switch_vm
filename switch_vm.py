#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *


class SwitchVM:
    def __init__(self, master):
        # configure the below listed variables:
        self.config_file = "/home/honza/zoom_git_repos/r2d2/custom_global_variables.py"
        self.virtual_machines = ["qa026.qa.zoomint.com",
                                 "qa056.qa.zoomint.com",
                                 "lab-enc-callrec1.lab.zoomint.com",
                                 "lab-enc-callrec2.lab.zoomint.com"]
        self.configured_keys = ["SUT_ADDRESS",
                                "CALLREC_ADDRESS",
                                "POSTGRESQL_ENCOURAGE_HOST",
                                "POSTGRESQL_CALLREC_HOST",
                                "POSTGRESQL_SCORECARD_HOST",
                                "POSTGRESQL_AUDITLOG_HOST"]

        # don't touch the rest
        self.master = master
        self.frame = Frame(master)
        self.frame.pack()
        self.vm = StringVar()
        self.browser = StringVar()
        self.setup = BooleanVar()
        self.teardown = BooleanVar()
        master.title("RF Configuration")

        self.label = Label(self.frame,
                           text="RF Configuration",
                           font="Helvetica 11 bold")
        self.label.pack()

        current_vm, current_browser, setup_enabled, teardown_enabled = self.read_current_configuration(self.config_file)

        for machine in self.virtual_machines:
            self.machine_button = Radiobutton(self.frame,
                                              text=machine,
                                              variable=self.vm,
                                              value=machine,
                                              command=self.set_vm,
                                              indicatoron=0)
            self.machine_button.pack(expand=True)
            if machine == current_vm:
                self.machine_button.select()

        for browser in ["IE", "chrome", "firefox"]:
            self.browser_radio = Radiobutton(self.frame,
                                             text=browser,
                                             variable=self.browser,
                                             value=browser,
                                             command=self.set_browser)
            self.browser_radio.pack(side=LEFT, anchor=W)
            if browser == current_browser:
                self.browser_radio.select()

        self.setup_teardown_frame = Frame(master)
        self.setup_teardown_frame.pack(side=BOTTOM)

        self.setup_checkbutton = Checkbutton(self.setup_teardown_frame,
                                             text="ENABLE_FE_SETUP",
                                             variable=self.setup,
                                             onvalue=1,
                                             offvalue=0,
                                             command=self.set_setup)
        self.setup_checkbutton.pack()
        if not setup_enabled:
            self.setup_checkbutton.deselect()
        else:
            self.setup_checkbutton.select()

        self.teardown_checkbutton = Checkbutton(self.setup_teardown_frame,
                                                text="ENABLE_FE_TEARDOWN",
                                                variable=self.teardown,
                                                onvalue=1,
                                                offvalue=0,
                                                command=self.set_teardown)
        self.teardown_checkbutton.pack()
        if not teardown_enabled:
            self.setup_checkbutton.deselect()
        else:
            self.teardown_checkbutton.select()

    def read_current_configuration(self, config_file):
        with open(config_file, 'r') as f:
            lines = f.readlines()
            current_vm = None
            current_browser = 'chrome'
            setup_enabled = True
            teardown_enabled = True

            for line in lines:
                if re.match(r'^SUT_ADDRESS = ', line):
                    current_vm = re.search('^SUT_ADDRESS = \'(.+?)\'', line).group(1)
                if re.match(r'^BROWSER', line):
                    current_browser = re.search('^BROWSER = \'(.+?)\'', line).group(1)
                if re.match(r'^ENABLE_FE_SETUP = False', line):
                    setup_enabled = False
                if re.match(r'^ENABLE_FE_TEARDOWN = False', line):
                    teardown_enabled = False

        return current_vm, current_browser, setup_enabled, teardown_enabled

    def set_vm(self):
        vm = str(self.vm.get())
        with open(self.config_file, 'r+') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                for key in self.configured_keys:
                    if re.match(r'^{} = '.format(key), lines[i]):
                        lines[i] = "{} = \'{}\'\n".format(key, vm)
            f.seek(0)
            f.truncate()
            f.write(''.join(lines))

    def set_browser(self):
        browser = str(self.browser.get())
        with open(self.config_file, 'r+') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if re.match(r'^BROWSER = ', lines[i]):
                    lines[i] = "BROWSER = \'{}\'\n".format(browser)
            f.seek(0)
            f.truncate()
            f.write(''.join(lines))

    def set_setup(self):
        setup = "True" if self.setup.get() else "False"
        with open(self.config_file, 'r+') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if re.match(r'^ENABLE_FE_SETUP = ', lines[i]):
                    lines[i] = "ENABLE_FE_SETUP = {}\n".format(setup)
            f.seek(0)
            f.truncate()
            f.write(''.join(lines))

    def set_teardown(self):
        teardown = "True" if self.teardown.get() else "False"
        with open(self.config_file, 'r+') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if re.match(r'^ENABLE_FE_TEARDOWN = ', lines[i]):
                    lines[i] = "ENABLE_FE_TEARDOWN = {}\n".format(teardown)
            f.seek(0)
            f.truncate()
            f.write(''.join(lines))


root = Tk()
gui = SwitchVM(root)
root.wm_attributes("-topmost", 1)
root.mainloop()
