import os
import torch
import subprocess
import sys

from xcmd import XCMD

CHECKPOINT_DIR = "/home/ansonmau/dev/1010AI/checkpoints"

class Checkpoint:
    def __init__(self) -> None:
        self.ignore_warnings = False
        self.folder_name = ""
        self.save_folder = ""
        self.data = {
                "qnet_state": None,
                "optimizer_state": None,
                "stats": None,
                "ep": None,
                }
    # ──────────────────────────────────────────────────────────────────────

    def save(self, folder_name, prefix="c"):
        ep = self.data["ep"]

        save_folder = "/".join([CHECKPOINT_DIR, folder_name])
        save_file = "/".join( [save_folder, f"{prefix}_{ep}.pth"] )

        self.folder_check(save_folder)
        torch.save(self.data, save_file)

        self.save_folder = save_folder
        self.folder_name = folder_name

    def update(self, data):
        def match(l1,l2):
            for i in l1:
                if i not in l2:
                    return False
            return True

        if not match(data.keys(), self.data.keys()):
            raise ValueError("Keys do not match. Bad dict passed to checkpoint")

        self.data.update(data)

    def upload(self):
        cmd = XCMD()
        u = f"/home/ansonmau/dev/pth_plot/venv/bin/python3 /home/ansonmau/dev/pth_plot/plot.py {self.save_folder}/ -o /home/ansonmau/dev/pth_plot/{self.folder_name}.html"
        cmd.x_async(u)

    # ──────────────────────────────────────────────────────────────────────
    def folder_check(self, save_folder):
        try:
            os.makedirs(save_folder)
            self.ignore_warnings = True
        except FileExistsError:
            if ( not self.ignore_warnings ) and ( save_folder.split("/")[-1] != "temp" ):
                print(f"[WARNING] Save folder already exists. continue? ({save_folder})")
                input()
                self.ignore_warnings = True




