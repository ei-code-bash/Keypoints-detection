import os

def convert_to_yolov8_pose_format(input_file_path, output_file_path):
    """
    yolov8-pose中2表示可见点
    读取原始标注文件，并将其转换为YOLOv8-Pose格式。

    原始格式: <class> <x_center> <y_center> <w> <h> <kpt1_x> <kpt1_y> <kpt2_x> <kpt2_y> ...
    目标格式: <class> <x_center> <y_center> <w> <h> <kpt1_x> <kpt1_y> 2 <kpt2_x> <kpt2_y> 2 ...

    Args:
        input_file_path (str): 输入的原始标注文件路径。
        output_file_path (str): 输出的YOLOv8-Pose格式标注文件路径。
    """
    try:
        with open(input_file_path, 'r') as f_in, open(output_file_path, 'w') as f_out:
            for line in f_in:
                parts = line.strip().split()
                if not parts:
                    continue

                # 前5个值是 class, x, y, w, h
                class_and_bbox = parts[:5]
                
                # 后面的值是成对出现的关键点坐标
                keypoints = parts[5:]
                
                new_keypoints = []
                # 检查关键点坐标是否是成对的
                if len(keypoints) % 2 != 0:
                    print(f"警告: 文件 {input_file_path} 中的行存在奇数个关键点坐标，已跳过: {line.strip()}")
                    continue
                
                # 遍历所有关键点对 (x, y)
                for i in range(0, len(keypoints), 2):
                    kpt_x = keypoints[i]
                    kpt_y = keypoints[i+1]
                    visibility = '2'  # 假设所有标注的关键点都是可见的
                    new_keypoints.extend([kpt_x, kpt_y, visibility])
                
                # 拼接成新的一行
                new_line = " ".join(class_and_bbox + new_keypoints)
                f_out.write(new_line + '\n')
        
        print(f"转换成功！已将结果保存到: {output_file_path}")

    except FileNotFoundError:
        print(f"错误: 输入文件未找到 -> {input_file_path}")
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
input_dir = "output_final(base)"
output_dir = "pingjie"

if not os.path.exists(output_dir):
     os.makedirs(output_dir)

for filename in os.listdir(input_dir):
     if filename.endswith(".txt"):
         input_path = os.path.join(input_dir, filename)
         output_path = os.path.join(output_dir, filename)
         convert_to_yolov8_pose_format(input_path, output_path)
print("所有文件批量转换完成！")