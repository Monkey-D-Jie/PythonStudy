import requests
import json
import time
import random
from typing import List, Dict


class TencentVideoCommentSpider:
    def  __init__(self, vid: str):
        self.vid = vid  # 视频唯一标识
        self.base_url = "https://video.coral.qq.com/varticle/{}/comment/v2".format(vid)  # 评论接口（需根据抓包更新）
        self.headers = self._get_headers()  # 初始化请求头
        self.comments: List[Dict] = []  # 存储所有评论

    def _get_headers(self) -> Dict:
        """生成随机请求头，模拟不同浏览器"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
        ]
        return {
            "User-Agent": random.choice(user_agents),
            "Referer": f"https://v.qq.com/x/cover/{self.vid}.html",  # 模拟从视频页跳转
            "Accept": "application/json, text/plain, */*",
            "Connection": "keep-alive"
        }

    def _get_params(self, cursor: int = 0, count: int = 20) -> Dict:
        """生成请求参数（根据抓包结果调整）"""
        return {
            "orinum": count,  # 每页评论数
            "oriorder": "n",  # 排序：n=新到旧，o=旧到新
            "cursor": cursor,  # 分页标识（下一页的cursor由当前页返回）
            "source": "132",  # 固定值，可能代表客户端类型
            "_": int(time.time() * 1000)  # 时间戳，防止缓存
        }

    def _parse_comment(self, response_data: Dict) -> tuple[List[Dict], int]:
        """解析单页评论数据，返回评论列表和下一页cursor"""
        comments = []
        # 从JSON中提取评论列表（结构需根据实际返回调整）
        if response_data.get("code") != 0:
            print(f"接口返回错误：{response_data.get('message')}")
            return comments, -1  # -1表示无下一页

        comment_list = response_data.get("data", {}).get("commentid", [])
        for item in comment_list:
            comment = {
                "id": item.get("id"),  # 评论ID
                "username": item.get("userinfo", {}).get("nick", "未知用户"),  # 用户名
                "content": item.get("content", ""),  # 评论内容
                "time": item.get("time", ""),  # 评论时间
                "upvote": item.get("up", 0),  # 点赞数
                "reply_count": item.get("rep", 0)  # 回复数
            }
            comments.append(comment)

        # 获取下一页cursor（关键分页参数）
        next_cursor = response_data.get("data", {}).get("last", -1)
        return comments, next_cursor

    def crawl(self, max_pages: int = 5) -> List[Dict]:
        """
        分页爬取评论
        :param max_pages: 最大爬取页数（防止无限爬取）
        :return: 所有评论列表
        """
        current_cursor = 0  # 初始分页标识
        page = 1

        while page <= max_pages:
            print(f"爬取第 {page} 页评论...")
            try:
                # 发送请求
                params = self._get_params(cursor=current_cursor)
                response = requests.get(
                    url=self.base_url,
                    params=params,
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()  # 触发HTTP错误（如403、500）
                data = response.json()

                # 解析数据
                page_comments, next_cursor = self._parse_comment(data)
                if not page_comments:
                    print("当前页无评论，终止爬取")
                    break

                self.comments.extend(page_comments)
                print(f"第 {page} 页爬取完成，共 {len(page_comments)} 条评论")

                # 检查是否有下一页
                if next_cursor == -1 or next_cursor == current_cursor:
                    print("已无更多评论")
                    break

                current_cursor = next_cursor
                page += 1
                # 随机休眠1-3秒，降低反爬风险
                time.sleep(random.uniform(1, 3))

            except requests.exceptions.RequestException as e:
                print(f"请求错误：{e}")
                break
            except json.JSONDecodeError:
                print("JSON解析失败，可能接口返回格式变更")
                break
            except Exception as e:
                print(f"未知错误：{e}")
                break

        print(f"爬取结束，共获取 {len(self.comments)} 条评论")
        return self.comments

    def save_to_json(self, filename: str = "comments.json") -> None:
        """将评论保存到JSON文件"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.comments, f, ensure_ascii=False, indent=2)
        print(f"评论已保存到 {filename}")


if __name__ == "__main__":
    # 使用示例
    video_vid = "mzc00200tjkzeps/y4101qnn3jo"  # 替换为目标视频的vid
    spider = TencentVideoCommentSpider(vid=video_vid)

    # 爬取最多3页评论
    all_comments = spider.crawl(max_pages=3)

    # 保存到文件
    spider.save_to_json()
