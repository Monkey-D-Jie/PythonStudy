import urllib.request
import re

# 视频相关参数，需替换为实际要爬取的视频对应值
# 视频固定标识（需替换成你要爬取的真实视频 vid）
vid = "j6cgzhtkuonf6te"
# 初始评论标识（可从第一页接口返回拿到，也可固定初始值）
cid = "6233603654052033588"
# 每页获取的评论数量
page_size = 20
# 要爬取的总页数（可根据需求调整，-1 则一直爬到无更多评论）
total_pages = 5
num = "20"

# 构造评论请求网址
url = f"https://video.coral.qq.com/filmreviewr/c/upcomment/{vid}?commentid={cid}"
# 2025年8月8日11:10:13 更新
# 该域名已失效，毕竟视频是7年前的。只能说学习下这个程序里的思路。
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Content-Type": "application/javascript"
}

# 构建 opener 处理请求头
opener = urllib.request.build_opener()
headall = []
for key, value in headers.items():
    item = (key, value)
    headall.append(item)
opener.addheaders = headall
urllib.request.install_opener(opener)

try:
    # 爬取并解码评论页面内容---单页评论
    data = urllib.request.urlopen(url).read().decode("utf-8")
    # 定义正则表达式匹配标题和评论内容
    titlepat = '"title":"(.*?)"'
    commentpat = '"content":"(.*?)"'

    # 查找所有匹配的标题和评论
    titleall = re.compile(titlepat, re.S).findall(data)
    commentall = re.compile(commentpat, re.S).findall(data)

    # 输出结果
    for i in range(len(titleall)):
        print("标题：", titleall[i])
        print("评论：", commentall[i])
        print("-" * 30)

except urllib.error.URLError as e:
    print(f"网络请求错误：{e}")
except Exception as e:
    print(f"其他异常：{e}")





# 分页爬取视频评论
def crawl_comment_page(vid, cid):
    """
    爬取单页评论核心逻辑
    :param vid: 视频唯一标识
    :param cid: 评论分页标识（用于构造下一页请求）
    :return: 下一页评论标识（last）、标题列表、评论内容列表
    """
    # 构造评论接口 URL
    url = f"https://video.coral.qq.com/filmreviewr/c/upcomment/{vid}?commentid={cid}&num={page_size}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Content-Type": "application/javascript"
    }

    # 构建带请求头的 opener
    opener = urllib.request.build_opener()
    headall = []
    for key, value in headers.items():
        headall.append((key, value))
    opener.addheaders = headall
    urllib.request.install_opener(opener)

    try:
        # 发起请求并解码返回内容
        response = urllib.request.urlopen(url)
        data = response.read().decode("utf-8")

        # 正则提取标题、评论内容、下一页标识
        title_pat = '"title":"(.*?)","abstract":'
        comment_pat = '"content":"(.*?)"'
        last_pat = '"last":"(.*?)"'

        titles = re.compile(title_pat, re.S).findall(data)
        comments = re.compile(comment_pat, re.S).findall(data)
        next_cid = re.compile(last_pat, re.S).findall(data)[0] if re.compile(last_pat, re.S).findall(data) else ""

        return next_cid, titles, comments
    except Exception as e:
        print(f"爬取/解析页面失败: {e}")
        return "", [], []


if __name__ == "__main__":
    current_cid = cid
    for page in range(total_pages):
        print(f"===== 开始爬取第 {page + 1} 页评论 =====")
        # 爬取当前页
        current_cid, title_list, comment_list = crawl_comment_page(vid, current_cid)

        # 打印当前页结果
        for i in range(len(title_list)):
            try:
                # eval 用于处理字符串中的转义（如 \" 转成 " 等）
                print(f"评论标题: {eval('[' + title_list[i] + ']')}")
                print(f"评论内容: {eval('[' + comment_list[i] + ']')}")
                print("-" * 50)
            except Exception as err:
                print(f"解析评论出错: {err}")

        # 如果没有拿到下一页标识，说明已无更多评论，提前终止
        if not current_cid:
            print("已无更多评论，提前结束爬取")
            break

        # 准备爬取下一页（用当前页返回的 last 作为下一页的 cid）
        print(f"下一页评论标识: {current_cid}")

    print("全部评论爬取完毕！")