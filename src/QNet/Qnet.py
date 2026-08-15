# ──────────────────────────────────────────────────────────────────────
from typing import TYPE_CHECKING

from torch.nn.modules import padding

if TYPE_CHECKING:
    from QNet.Agent import Agent
# ──────────────────────────────────────────────────────────────────────

import torch
import torch.nn as nn

KERNEL_SIZE        = 3
BOARD_OUT_CHANNELS = 16
INV_OUT_CHANNELS   = 16
COMBINE_OUT_CHANNELS = 256

BOARD_OUT_SIZE = 10 * 10 * (BOARD_OUT_CHANNELS * 2) # since second board layer outputs 2*out_channels
INV_OUT_SIZE   = 5 * 5 * INV_OUT_CHANNELS

class QNet(nn.Module):
    def __init__(self, agent: "Agent"):
        super().__init__()
        self._agent = agent

        self.inv_lyrs = nn.Sequential(
                nn.Conv2d(in_channels=agent.inventory_size, out_channels=INV_OUT_CHANNELS, kernel_size=KERNEL_SIZE, padding=1),
                nn.ReLU(),
                )
        
        self.board_lyrs = nn.Sequential(
                nn.Conv2d(in_channels=1, out_channels=BOARD_OUT_CHANNELS, kernel_size=KERNEL_SIZE, padding=1),
                nn.ReLU(),
                nn.Conv2d(in_channels=BOARD_OUT_CHANNELS, out_channels=BOARD_OUT_CHANNELS*2, kernel_size=KERNEL_SIZE, padding=1),
                nn.ReLU(),
                )

        self.combine_lyrs = nn.Sequential(
                nn.Linear(BOARD_OUT_SIZE + INV_OUT_SIZE, COMBINE_OUT_CHANNELS),
                nn.ReLU(),
                nn.Linear(COMBINE_OUT_CHANNELS, agent.gai.get_size()),
                )


    def forward(self, board_tensor = None, inv_tensor = None):
        if board_tensor is None:
            board_tensor = self._agent.get_board_tensor().unsqueeze(0) # add batch dim @ ind0 (10, 10) -> (1, 10, 10)
        if inv_tensor is None:
            inv_tensor = self._agent.get_inventory_tensor()

        board_feats = self.board_lyrs(board_tensor)
        inv_feats = self.inv_lyrs(inv_tensor)

        board_feats = board_feats.flatten(start_dim=1)
        inv_feats = inv_feats.flatten(start_dim=1)

        combined = torch.cat([board_feats, inv_feats], dim=1)
        q_vals = self.combine_lyrs(combined)

        return q_vals
