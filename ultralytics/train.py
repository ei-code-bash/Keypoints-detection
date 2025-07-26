#!/usr/bin/env python3
import os
import yaml
from ultralytics import YOLO
def train_pose_model():
    # 加载预训练模型
    model = YOLO('yolov8s-pose.pt')  # 使用小尺寸模型
    
    # 训练参数配置
    train_args = {
        'data': f'{data}/armor.yaml',
        'epochs': 100,
        'batch': 16,
        'imgsz': 640,
        'device': '0',  # 使用GPU 0, 设为'cpu'使用CPU
        'workers': 4,
        'optimizer': 'auto',
        'lr0': 0.01,  # 初始学习率
        'lrf': 0.01,  # 最终学习率 = lr0 * lrf
        'weight_decay': 0.0005,
        'warmup_epochs': 3,
        'box': 7.5,    # 边界框损失权重
        'cls': 0.5,    # 分类损失权重
        'dfl': 1.5,    # 分布焦点损失权重
        'pose': 12.0,  # 姿态损失权重
        'kobj': 2.0,   # 关键点对象性损失权重
        'name': 'armor_pose_v1',  # 实验名称
        'exist_ok': True,  # 允许覆盖现有输出目录
        'resume': False,   # 是否从上次检查点恢复
        'save_period': 10  # 每10个epoch保存一次模型
    }
    
    # 开始训练
    results = model.train(**train_args)
    
    return results

print("开始训练姿态估计模型...")
training_results = train_pose_model()
print("训练完成!")