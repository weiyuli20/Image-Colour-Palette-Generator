from flask import Flask,render_template,request
import numpy as np
from PIL import Image,ImageOps
import base64
from io import BytesIO
from collections import Counter


app = Flask(__name__)


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        f = request.files['file']
        colour_code = request.form['color_code']
        colours = give_most_hex(f.stream,colour_code)
        return render_template('index.html',colors_list=colours,code = colour_code)
    
    return render_template("index.html")

def give_most_hex(file_path,code):
    '''
    1、预处理 缩小图片
    2、
    '''
    
    my_image = Image.open(file_path).convert('RGB')
    size = my_image.size
    img = my_image
    
    if size[0] >= 1200 or size[1] >= 1200:
        my_image = ImageOps.scale(image=my_image, factor=0.6)
    elif size[0] >= 800 or size[1] >= 800:
        my_image = ImageOps.scale(image=my_image, factor=0.5)
    elif size[0] >= 600 or size[1] >= 600:
        my_image = ImageOps.scale(image=my_image, factor=0.4)
    elif size[0] >= 400 or size[1] >= 400:
        my_image = ImageOps.scale(image=my_image, factor=0.2)
    
    #对图片进行色调分离处理
    '''第二个参数 2 表示将每个颜色通道（红、绿、蓝）的颜色位数减少到 2 位。
    每个颜色通道原本有 8 位（取值范围是 0 - 255），减少到 2 位后，每个通道只有 4 种可能的取值（），这样整个图像的颜色数量就会大大减少。'''
    my_image = ImageOps.posterize(my_image,2) 
    output_path = 'posterized_example.jpg'
    my_image.save(output_path)


    #making the matrix of colours   from our image
    image_array = np.array(my_image)
    print(image_array.shape)

    #统计像素出现次数，记录在字典中
    trgb = [tuple(rgb)  for column in image_array  for rgb in column]
    unique_colors = Counter(trgb)
    
    # unique_colors = {}
    # for column in image_array:
    #     for rgb in column:
    #         t_rgb = tuple(rgb)
    #         # print("trgb:",t_rgb)
    #         if t_rgb not in unique_colors:
    #             unique_colors[t_rgb] = 1
    #         if t_rgb in unique_colors:
    #             unique_colors[t_rgb]+=1

    sorted_unique_colors = sorted(unique_colors.items(), key= lambda x: x[1],reverse=True)  #返回列表
    converted_dict  =dict(sorted_unique_colors)

    values  =list(converted_dict.keys())
    top_10 = values[:10]

    if code =='hex':
        hex_list = []
        for key  in top_10:
            hex = rgb_to_hex(key)
            hex_list.append(hex)
        return hex_list
    else:
        converted_top_10 = [tuple(int(num) for num in tup) for tup in top_10]
        return converted_top_10

# def base64encode(image):
#     buffered = BytesIO()
#     image.save(buffered, format="JPEG")
#     img_str = base64.b64encode(buffered.getvalue()).decode()
#     image_base64 = f'data:image/jpeg;base64,{img_str}'
#     return image_base64

if __name__ == '__main__':
    app.run(debug=True)