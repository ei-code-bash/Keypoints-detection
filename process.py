import os

def process_folder(source_dir, output_dir):
    """
    遍历源文件夹中的所有txt文件，提取每个文件第一行的后四位字符，
    并将其保存到目标文件夹的新文件中。

    参数:
    source_dir (str): 包含源txt文件的文件夹路径。
    output_dir (str): 用于存放结果文件的文件夹路径。
    """
    # 1. 检查并创建输出文件夹
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"📁 成功创建目标文件夹: '{output_dir}'")
        except OSError as e:
            print(f"❌ 错误：无法创建文件夹 '{output_dir}'. 错误信息: {e}")
            return # 如果无法创建文件夹，则退出函数

    # 2. 遍历源文件夹中的所有文件
    print(f"\n🚀 开始处理文件夹: '{source_dir}'...")
    for filename in os.listdir(source_dir):
        # 确保我们只处理 .txt 文件
        if filename.endswith(".txt"):
            input_filepath = os.path.join(source_dir, filename)
            output_filepath = os.path.join(output_dir, filename)

            try:
                # 使用 'with' 语句安全地打开文件
                with open(input_filepath, 'r', encoding='utf-8') as infile:
                    # 读取第一行
                    first_line = infile.readline()

                    # 3. 检查第一行是否存在
                    if not first_line:
                        print(f"⚠️  跳过 '{filename}': 文件为空。")
                        continue  # 跳到下一个文件

                    # 4. 清理并提取后四位字符
                    cleaned_line = first_line.strip()  # 移除末尾的换行符等空白
                    
                    if len(cleaned_line) < 4:
                        print(f"⚠️  跳过 '{filename}': 第一行内容不足4个字符。")
                        continue # 跳到下一个文件

                    last_four = cleaned_line[-4:]

                    # 5. 将提取的内容写入新文件
                    with open(output_filepath, 'w', encoding='utf-8') as outfile:
                        outfile.write(last_four)
                    
                    print(f"✅  成功处理 '{filename}' -> 提取内容: '{last_four}'")

            except Exception as e:
                print(f"❌ 处理 '{filename}' 时发生错误: {e}")
    
    print("\n✨ 全部处理完成！")


# --- 主程序入口 ---
if __name__ == "__main__":
    # --- 请在这里修改您的文件夹路径 ---

    # 1. 指定您的源文件夹路径
    # 例如: "C:/Users/YourUser/Desktop/label_data"
    source_folder = "labelimg" 
    
    # 2. 指定您想生成的目标文件夹名称
    output_folder = "processed_results"
    
    # --- 修改结束 ---

    # 检查源文件夹是否存在
    if not os.path.isdir(source_folder):
        print(f"❌ 错误：源文件夹 '{source_folder}' 不存在。请检查路径是否正确。")
    else:
        # 调用函数，开始执行任务
        process_folder(source_folder, output_folder)
