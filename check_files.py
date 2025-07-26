#NEXTE ei
import os
from pathlib import Path
from typing import Set, List

# --- 配置区 ---
# 建议将路径和扩展名等配置信息放在脚本的开头，方便修改
IMAGE_DIR = Path("F:/Pictures/data/robotmaster/原始数据/base")
LABEL_DIR = Path("output_final(base)")
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
LABEL_EXTENSIONS = ['.txt', '.json', '.xml']

def get_filenames_in_dir(directory: Path, extensions: List[str]) -> Set[str]:
    """
    获取指定目录中具有特定扩展名的所有文件的基本名（不含扩展名）。

    Args:
        directory (Path): 要扫描的目录路径 (使用 pathlib.Path 对象)。
        extensions (List[str]): 一个包含文件扩展名的列表 (例如 ['.jpg', '.png'])。

    Returns:
        Set[str]: 一个包含所有匹配文件基本名的集合。如果目录不存在，则返回一个空集合。
    """
    if not directory.is_dir():
        print(f"❌ 错误: 目录 '{directory}' 不存在或不是一个有效的目录。")
        return set() # 直接返回空集合，让调用方继续处理

    filenames = set()
    for f in directory.iterdir():
        # f.suffix 用于获取文件扩展名，统一转为小写以进行不区分大小写的比较
        if f.suffix.lower() in extensions:
            # f.stem 直接获取不带扩展名的文件名
            filenames.add(f.stem)
    return filenames

def run_check(image_dir: Path, label_dir: Path, image_ext: List[str], label_ext: List[str]):
    """
    检查图像目录和标注目录中的文件，并生成一份匹配报告。

    Args:
        image_dir (Path): 图像文件的目录。
        label_dir (Path): 标注文件的目录。
        image_ext (List[str]): 有效的图像文件扩展名列表。
        label_ext (List[str]): 有效的标注文件扩展名列表。
    """
    print("🚀 开始检查文件...")

    # 1. 获取文件名集合
    image_names = get_filenames_in_dir(image_dir, image_ext)
    label_names = get_filenames_in_dir(label_dir, label_ext)

    print(f"🔍 找到 {len(image_names)} 个图像文件和 {len(label_names)} 个标注文件。")
    print("-" * 40)

    # 2. 使用集合运算进行比较
    matched_files = image_names.intersection(label_names)
    missing_labels = image_names - label_names  # 图像有，但标注没有
    missing_images = label_names - image_names  # 标注有，但图像没有

    # 3. 生成并打印报告
    print("✅ 检查报告 ✅")
    print("-" * 40)

    # 打印匹配成功的文件
    print(f"🎉 匹配成功: {len(matched_files)} 个")
    if matched_files and len(matched_files) < 20:
        # 为了防止刷屏，只在数量不多时打印具体文件名
        print("   " + ", ".join(sorted(list(matched_files))))
    print("-" * 40)

    # 打印缺少标注的文件
    if missing_labels:
        print(f"⚠️ 缺少标注文件: {len(missing_labels)} 个 (以下图像没有对应的标注)")
        for name in sorted(list(missing_labels)):
            print(f"   -> {name}")
    else:
        print("👍 所有图像文件都有对应的标注文件。")
    print("-" * 40)

    # 打印缺少图像的文件
    if missing_images:
        print(f"⚠️ 缺少图像文件: {len(missing_images)} 个 (以下标注没有对应的图像)")
        for name in sorted(list(missing_images)):
            print(f"   -> {name}")
    else:
        print("👍 所有标注文件都有对应的图像文件。")

    print("\n🏁 检查完成！")


if __name__ == "__main__":
    run_check(IMAGE_DIR, LABEL_DIR, IMAGE_EXTENSIONS, LABEL_EXTENSIONS)

