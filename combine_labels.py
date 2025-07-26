#本脚本不存在可以换行失败的问题，生成的txt文件可以自动换行
import os

def merge_label_data(labelme_dir, labelimg_dir, output_dir):
    """
    主播太难了，太jb抽象了
    合并来自 labelme 和 labelimg 的标注数据。

    具体逻辑:
    将 labelimg 文件中的最后四个数值，插入到 labelme 文件中
    的类别号和原始坐标数据之间。

    参数:
    labelme_dir (str): labelme 标注文件（.txt）所在的文件夹。
    labelimg_dir (str): labelimg 标注文件（.txt）所在的文件夹。
    output_dir (str): 用于存放合并后结果的文件夹。
    """
    # 1. 检查并创建输出文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 成功创建目标文件夹: '{output_dir}'")

    print(f"\n🚀 开始处理文件夹: '{labelme_dir}'...")

    # 2. 遍历 labelme 文件夹中的所有文件
    for filename in os.listdir(labelme_dir):
        if not filename.endswith(".txt"):
            continue

        labelme_filepath = os.path.join(labelme_dir, filename)
        labelimg_filepath = os.path.join(labelimg_dir, filename)
        output_filepath = os.path.join(output_dir, filename)

        # 3. 检查 labelimg 中是否存在同名文件
        if not os.path.exists(labelimg_filepath):
            print(f"⚠️  跳过 '{filename}': 在 '{labelimg_dir}' 中未找到对应文件。")
            continue

        try:
            # 4. 读取两个文件中的内容
            with open(labelme_filepath, 'r', encoding='utf-8') as f_me:
                line_me = f_me.readline().strip()

            with open(labelimg_filepath, 'r', encoding='utf-8') as f_img:
                line_img = f_img.readline().strip()

            if not line_me or not line_img:
                print(f"⚠️  跳过 '{filename}': 文件内容为空。")
                continue

            # 5. 分割数据
            parts_me = line_me.split()
            parts_img = line_img.split()

            # 确保数据足够进行操作
            if len(parts_me) < 2 or len(parts_img) < 4:
                print(f"⚠️  跳过 '{filename}': 文件内容格式不正确，数据不足。")
                continue

            # 提取所需部分
            labelme_class_id = parts_me[0]          # labelme 的类别号
            labelme_coords = parts_me[1:]           # labelme 的其余坐标
            labelimg_insertion_data = parts_img[-4:] # labelimg 的后四个坐标

            # 6. 重新拼接成新的数据列表
            new_parts = [labelme_class_id] + labelimg_insertion_data + labelme_coords
            
            # 将列表转换回空格分隔的字符串
            new_line = " ".join(new_parts)

            # 7. 将结果写入新文件
            with open(output_filepath, 'w', encoding='utf-8') as f_out:
                f_out.write(new_line)
            
            print(f"✅  成功处理 '{filename}'")

        except Exception as e:
            print(f"❌ 处理 '{filename}' 时发生错误: {e}")

    print("\n✨ 全部处理完成！")


# --- 主程序入口 ---
if __name__ == "__main__":
    # --- 请在这里配置您的文件夹路径 ---

    # 源文件夹1: 包含 labelme txt 文件的路径
    labelme_folder = "output_txt"
    
    # 源文件夹2: 包含 labelimg txt 文件的路径
    labelimg_folder = "labelimg"
    
    # 目标文件夹: 用于存放最终生成文件的路径
    output_folder = "output_final"
    
    # --- 配置结束 ---

    # 调用主函数执行任务
    merge_label_data(labelme_folder, labelimg_folder, output_folder)
