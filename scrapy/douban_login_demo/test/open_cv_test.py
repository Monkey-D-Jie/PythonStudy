# 注意需要 pip install opencv-python
import cv2
import numpy as np
'''
2025年9月2日14:01:48 更新
这个方法的目的，
根据背景图片和缺口图片，
找到对应缺口的所在位置。
目前的一个难点在于：
缺口图片获取不到
至少在该demo中是没有拿到的，
思路的话，就是背景图片+缺口图片，
传入到方法中，以获取到缺口所在的坐标为止。
然后让滑块移动到对应的位置即可。
'''

def identify_gap(bg_path, tp_path, output_path=None):
    """
    识别滑块验证码缺口位置
    :param bg_path: 背景图片路径
    :param tp_path: 缺口图片路径
    :param output_path: 结果输出图片路径（可选，用于调试）
    :return: 缺口左上角的x坐标
    """
    # 1. 读取图片
    # 以灰度模式读取背景图和滑块图
    bg_gray = cv2.imread(bg_path, 0)
    tp_gray = cv2.imread(tp_path, 0)

    # 2. 边缘检测
    # 使用Canny算子进行边缘检测，阈值可根据实际情况调整
    bg_edge = cv2.Canny(bg_gray, 100, 200)
    tp_edge = cv2.Canny(tp_gray, 100, 200)

    # 3. 模板匹配
    # 使用标准化的相关系数匹配方法
    result = cv2.matchTemplate(bg_edge, tp_edge, cv2.TM_CCOEFF_NORMED)
    # 获取最佳匹配位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # TM_CCOEFF_NORMED方法下，最大值位置是最佳匹配
    top_left = max_loc # 左上角坐标 (x, y)

    # 4. （可选）绘制矩形并保存结果用于调试
    if output_path:
        # 获取滑块图片的宽高
        th, tw = tp_gray.shape
        # 计算右下角坐标
        bottom_right = (top_left[0] + tw, top_left[1] + th)
        # 读取背景图（彩色模式，用于绘制）
        bg_img = cv2.imread(bg_path)
        # 在背景图上绘制红色矩形框标记缺口位置
        cv2.rectangle(bg_img, top_left, bottom_right, (0, 0, 255), 2)
        # 保存结果图片
        cv2.imwrite(output_path, bg_img)
        # 也可以显示结果（通常在脚本调试时使用，生产环境可注释掉）
        # cv2.imshow('Matched Result', bg_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # 5. 返回缺口位置的x坐标
    return top_left[0]

# 使用示例
if __name__ == "__main__":
    background_image_path = "./jpg/img_2.png"  # 请替换为你的背景图路径
    slider_image_path = "./jpg/img.png"         # 请替换为你的滑块图路径
    output_image_path = "./jpg/result.jpg"         # 输出结果图片路径

    x_coordinate = identify_gap(background_image_path, slider_image_path, output_image_path)
    print(f"识别出的缺口位置横坐标x为: {x_coordinate}")