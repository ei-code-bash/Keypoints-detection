##将labelme生成的json文件转换为txt文件，并将与labelimg生成的txt文件进行一一对应的拼接
import os
import json
import numpy as np
import argparse

label_list = ['B1', 'B2', 'B3', 'B4', 'B7', 'R1', 'R2', 'R3', 'R4', 'R7', 'base','ignore']


def run(path_json, path_txt, img_size):
    # 规范化路径并确保以分隔符结尾
    path_json = os.path.normpath(path_json) + os.sep
    path_txt = os.path.normpath(path_txt) + os.sep

    # 创建输出目录
    os.makedirs(path_txt, exist_ok=True)

    # 获取JSON文件列表
    list_json = [f for f in os.listdir(path_json) if f.endswith('.json')]

    if not list_json:
        print(f"警告: 没有找到JSON文件 - {path_json}")
        return

    print(f"开始转换: 共发现 {len(list_json)} 个JSON文件")

    for cnt, json_name in enumerate(list_json):
        input_path = os.path.join(path_json, json_name)
        output_path = os.path.join(path_txt, json_name.replace('.json', '.txt'))

        print(f"处理 [{cnt + 1}/{len(list_json)}]: {input_path}")
        change_json(input_path, output_path, img_size)

    print("转换完成!")


def change_json(json_path, txt_path, img_size):
    # 验证输入文件
    if not os.path.exists(json_path):
        print(f"错误: 文件不存在 - {json_path}")
        return
    if not os.path.isfile(json_path):
        print(f"错误: 路径不是文件 - {json_path}")
        return

    try:
        rows = img_size[1]
        cols = img_size[0]

        # 确保输出目录存在
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)

        # 尝试不同编码
        encodings = ['utf-8', 'gb18030', 'latin-1']
        json_data = None
        for encoding in encodings:
            try:
                with open(json_path, 'r', encoding=encoding) as f:
                    json_data = json.load(f)
                break
            except UnicodeDecodeError:
                continue

        if json_data is None:
            print(f"错误: 无法解码文件 - {json_path}")
            return

        with open(txt_path, 'w', encoding='utf-8') as ftxt:
            for shape in json_data['shapes']:
                xy = np.array(shape['points'])
                try:
                    label_idx = label_list.index(shape['label'])
                except ValueError:
                    print(f"警告: 未知标签 '{shape['label']}' - {json_path}")
                    continue

                line = str(label_idx)
                for m, n in xy:
                    # 归一化坐标
                    x_norm = m / cols
                    y_norm = n / rows
                    line += f' {x_norm:.6f} {y_norm:.6f}'
                ftxt.write(line + "\n")

    except Exception as e:
        print(f"处理文件 {json_path} 时出错: {str(e)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json_dir', type=str, help='JSON文件目录路径')
    parser.add_argument('txt_dir', type=str, help='TXT输出目录路径')
    parser.add_argument('img_size', nargs=2, type=int, help='图像尺寸 [宽度 高度]')

    args = parser.parse_args()

    # 打印参数信息
    print(f"输入目录: {args.json_dir}")
    print(f"输出目录: {args.txt_dir}")
    print(f"图像尺寸: {args.img_size[0]}x{args.img_size[1]}")

    run(args.json_dir, args.txt_dir, args.img_size)


