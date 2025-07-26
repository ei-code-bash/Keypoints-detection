from moviepy.editor import VideoFileClip#适用与将视频切片处理

def split_video(input_video_path, output_folder, slice_duration):
    # 读取视频文件
    video = VideoFileClip(input_video_path)
    
    # 获取视频的总时长（单位：秒）
    video_duration = video.duration
    
    # 计算切片的数量
    num_slices = int(video_duration // slice_duration) + 1
    
    # 按照指定的时长切割视频
    for i in range(num_slices):
        # 计算每个片段的起始时间和结束时间
        start_time = i * slice_duration
        end_time = min((i + 1) * slice_duration, video_duration)
        
        # 提取视频片段
        video_slice = video.subclip(start_time, end_time)
        
        # 输出每个视频片段
        output_video_path = f"{output_folder}/slice_{i + 1}.mp4"
        video_slice.write_videofile(output_video_path, codec='libx264')

    print("视频切割完成！")

# 使用示例
input_video_path = 'path_to_your_video.mp4'  # 输入视频文件路径
output_folder = 'path_to_output_folder'      # 输出文件夹路径
slice_duration = 10  # 每个视频片段的时长，单位秒

split_video(input_video_path, output_folder, slice_duration)
