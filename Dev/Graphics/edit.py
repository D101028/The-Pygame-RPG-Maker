import cv2
import os
from PIL import Image
import glob


def fill_to_length(string: str, length: int, ch: str = "0") -> str:
    if len(string) > length:
        raise RuntimeError("length of `string` shouldn't be greater than `length`")
    return ch*(length-len(string))+string

def split_img(path: str, 
              subwidth: int = 64, 
              subheight: int = 64, 
              output_folder: str = "./", 
              num_start: int = 0, 
              num_length: int = 2, 
              except_pos: list[tuple[int, int]] = []) -> None:
    """
    use height*width = 3*4 as the example, output order is (assume `num_start = 0`):\\
    0 1  2  3 \\
    4 5  6  7 \\
    8 9 10 11 \\
    every size must be divisible
    """
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    basename = path.split(".")[-1]
    height, width, channels = image.shape
    count = num_start
    for i in range(height // subheight):
        for j in range(width // subwidth):
            if (i, j) in except_pos:
                continue
            cropped_image = image[i*subheight:(i+1)*subheight, j*subwidth:(j+1)*subwidth]
            print(count)
            cv2.imwrite(os.path.join(output_folder, 
                                     fill_to_length(str(count), num_length) + "." + basename), 
                        cropped_image)
            count += 1

def crop_img(path, top_left, height, width, output_folder = "./", output_filename = "0"):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    basename = path.split(".")[-1]
    cropped_image = image[top_left[1]:(top_left[1]+height), top_left[0]:(top_left[0]+width)]
    cv2.imwrite(os.path.join(output_folder, output_filename + "." + basename), cropped_image)

def merge_images_horizontally(image_folder, output_file):
    # 找到所有 PNG 图片文件
    image_files = sorted(glob.glob(f"{image_folder}/*.png"))
    
    # 确保至少有一张图片
    if not image_files:
        print("No images found in the specified folder.")
        return
    
    # 加载所有图片并获取最大高度
    images = [Image.open(img).convert("RGBA") for img in image_files]
    widths, heights = zip(*(img.size for img in images))
    
    # 计算合并后的总宽度和最大高度
    total_width = sum(widths)
    max_height = max(heights)
    
    # 创建一个新的透明背景图片
    merged_image = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))
    
    # 把所有图片拼接到新的图片上
    x_offset = 0
    for img in images:
        merged_image.paste(img, (x_offset, 0))
        x_offset += img.width
    
    # 保存合并后的图片
    merged_image.save(output_file)
    print(f"Merged image saved as {output_file}")

if __name__ == "__main__":
    # output_folder = r"D:\Projects\Python\pygame\pygame-rpg-2\Dev\Graphics\objects"
    # file_path = r"D:\Projects\Python\pygame\pygame-rpg-2\Dev\Graphics\edit\Graphics-old\maptile\outside04_resized.png"
    # # split_img(file_path, subwidth=32, subheight=32, num_length=3, output_folder=output_folder)
    # crop_img(file_path, (448, 0), 128, 64, output_folder=output_folder, output_filename="46")

    merge_images_horizontally("./input", "output.png")

