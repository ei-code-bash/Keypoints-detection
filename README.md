# Keypoints-detection
NEXTE-Vison-Group
## 依赖和环境
- ultralytics的依赖环境
- 训练设备RTX 4090
## 标注说明（😊）
>使用labelme 和labelimg,共17位标注数据，分别为class_id,x_center,y_center,width,height,x1,y1,2,x2,y2,2,x3,y3,2,x4,y4,2
>以上脚本可以完成所有数据的转换
-----
## 具体实现
labelme->json文件，放入到input_changejson的文件夹中，使用new_txt.py脚本转换为txt文件，这样就得到了角点坐标
  使用combine_lables.py实现labelimg与转换后的文件进行拼接得到13为标注格式
  **值得注意的是**本项目基于yolov8-pose开发，在每个keypoints后面必须包含其visibility,使用topose.py转换为17位标注数据😊

  同时，由于数据的庞大性，会存在图片与标注文件不对应的问题，check_files脚本可实现图片与脚本之间一一对应的问题，并找出少的图片位置
如![https://youke1.picui.cn/s1/2025/07/26/6884f92e3ceff.png]  
## 训练
注意kpt_shape[4,3],mAP和mAP95值之间的变换，建议前50个epoches  lr=0.0001,基本收敛，后20抽调整学习率为其0.2呗，可以在配置文件定义标注点的顺序  
如必须是顺时针或者是逆时针，建议imgzs=640,batch=10,关注模型的mAP在训练过程中有没有上升，以及关键的pose-loss👍  
建议加入混合光照变换。mix_hsv和数据的旋转    

对于装甲板的部分：加入通道注意力机制（红蓝），加入旋转注意力机制，以极坐标进行换算，同时加强装甲板的局部空间注意力机制(使用attention层)
！[https://youke1.picui.cn/s1/2025/07/27/6884fc78097be.png]  
## 后续的操作
- yolov8-pose模型的量化，  
- openvino的int8的量化
- openvino异步推理池的实现
