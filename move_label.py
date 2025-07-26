import json
import os
input_folder = 'path_to_your_json_files'  # 请将此路径更改为你的转换后的文件夹路径
output_folder = 'path_to_output_txt_files'  # 请将此路径更改为拼接后的文件夹路径
if not os.path.exists(output_floder):
    os.makedirs(output_floder)
for filename in os.listdir(imput_floder):
    if filename.endwith('.txt'):
        txt_path=os.path.join(input_floder,filename)
        with open(txt_path,'r',encoding='utf-8') as txt_file:
            lines=txt_file.readlines()
        # 获取输出txt文件的路径
        output_filename=os.path.splitext(filename)[0] + '_output.txt'
        output_path=os.path.join(output_folder,output_filename)
        with open(output_path,'w',encoding='utf-8') as output_file:
            
            for line in lines:
                if 'Label:' in line:
                    label = line.split(':')[1].strip()
                    output_file.write(f"{label} ")
                elif 'Points:' in line:
                    points = line.split(':')[1].strip()
                    output_file.write(f"{points}\n")
print("拼接完成！")