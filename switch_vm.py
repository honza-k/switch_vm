#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *


class SwitchVM:
    def __init__(self, master):
        # configure the below listed variables:
        self.config_file = "/home/honza/zoom_git_repos/r2d2/custom_global_variables.py"
        self.virtual_machines = ["qa026.qa.zoomint.com",
                                 "qa056.qa.zoomint.com"]
        self.configured_keys = ["SUT_ADDRESS",
                                "CALLREC_ADDRESS",
                                "POSTGRESQL_ENCOURAGE_HOST",
                                "POSTGRESQL_CALLREC_HOST",
                                "POSTGRESQL_SCORECARD_HOST",
                                "POSTGRESQL_AUDITLOG_HOST"]

        # don't touch the rest
        self.master = master
        self.vm = StringVar()
        master.title("VM Switcher")

        self.label = Label(master,
                           text="VM Switcher")
        self.label.pack()

        for machine in self.virtual_machines:
            self.radio = Radiobutton(master,
                                     text=machine,
                                     variable=self.vm,
                                     value=machine,
                                     command=self.set_vm)
            self.radio.pack()

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


root = Tk()
gui = SwitchVM(root)
root.wm_attributes("-topmost", 1)
root.mainloop()
