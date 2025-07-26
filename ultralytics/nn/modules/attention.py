import cv2
import torch
import torch.nn as nn
import numpy as np
from ultralytics.nn.modules import Conv
class ArmorAttention(nn.Module):
    """
    abab一个为装甲板检测优化的、结合了通道和空间注意力的模块 (类CBAM实现)。
    该模块首先应用通道注意力，然后应用空间注意力，并通过残差连接增强特征。
    """
    def __init__(self, c1, c2=None, reduction=16, kernel_size=7):
        """
        初始化函数。
        c1 (int): 输入通道数。
        c2 (int, optional): 输出通道数。如果为None，则输出通道数与输入通道数相同。
        reduction (int): 通道注意力中MLP的通道缩减率。
        kernel_size (int): 空间注意力中卷积核的大小。
        """
        super().__init__()
        # 如果没有指定输出通道c2，则默认等于输入通道c1
        c2 = c2 or c1
        
        # --- 1. 通道注意力 (Channel Attention) ---
        # 为输入的c1个通道，生成c1个权重,永远都要注意维度的问题
        hidden_channels = max(c1 // reduction, 16) # 计算MLP的隐藏层通道数，保证最小值
        self.channel_att = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),  # 全局平均池化  [B, C, 1, 1]
            Conv(c1, hidden_channels, 1, act=nn.SiLU()), # 第一次全连接 (用1x1卷积实现)
            Conv(hidden_channels, c1, 1, act=False), # 第二次全连接
            nn.Sigmoid()  # Sigmoid激活，得到0-1之间的权重
        )

        # --- 2. 空间注意力 (Spatial Attention) ---
        self.spatial_att = nn.Sequential(
            # 使用7x7卷积核来捕捉大范围的空间关系
            Conv(2, 1, kernel_size, padding=(kernel_size - 1) // 2, act=False),
            nn.Sigmoid()
        )
        self.channel_adjust = Conv(c1, c2, 1) if c1 != c2 else nn.Identity()

    def forward(self, x):
        """
        前向传播函数。
        采用串联方式
        """
        # 1. 应用通道注意力
        channel_weights = self.channel_att(x)
        x_channel_att = x * channel_weights  # [B, C, H, W] * [B, C, 1, 1] -> 广播机制

        # 2. 应用空间注意力
        # 沿着通道维度取最大值和平均值，并拼接
        max_out, _ = torch.max(x_channel_att, dim=1, keepdim=True)
        avg_out = torch.mean(x_channel_att, dim=1, keepdim=True)
        spatial_input = torch.cat([max_out, avg_out], dim=1) # -> [B, 2, H, W]
        
        spatial_weights = self.spatial_att(spatial_input) # -> [B, 1, H, W]
        x_spatial_att = x_channel_att * spatial_weights # [B, C, H, W] * [B, 1, H, W]

        # 3. 残差连接与通道调整
        # 将注意力输出与原始输入相加，并通过1x1卷积调整通道
        return self.channel_adjust(x_spatial_att + x)

    def forward_fuse(self, x):
        """为模型融合（fuse）提供的优化版前向传播。"""
        # 在fuse模式下，逻辑通常与常规forward保持一致，这个地方我也不是很懂^_^
        # 但为了兼容性，直接调用forward方法
        return self.forward(x)
    def register_attention_modules():
        from ultralytics.nn.tasks import attempt_load_weights
        from ultralytics.nn import modules
        modules.ArmorAttention = ArmorAttention


