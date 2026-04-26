import json
from datetime import datetime
import os


class ResultWriter:
    def __init__(self, output_dir="results"):
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"创建输出目录: {self.output_dir}")

    def write_posts_to_file(self, posts, filename=None, format="txt"):
        if not posts:
            print("没有帖子内容可写入。")
            return None

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xiaohongshu_posts_{timestamp}"

        filepath = os.path.join(self.output_dir, f"{filename}.{format}")

        try:
            if format == "txt":
                self._write_to_txt(posts, filepath)
            elif format == "json":
                self._write_to_json(posts, filepath)
            else:
                print(f"不支持的格式: {format}，默认使用txt格式")
                self._write_to_txt(posts, filepath)

            print(f"结果已成功写入到: {filepath}")
            return filepath

        except Exception as e:
            print(f"写入文件失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _write_to_txt(self, posts, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("小红书爬虫结果\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"共爬取 {len(posts)} 条帖子\n")
            f.write("=" * 80 + "\n\n")

            for i, post in enumerate(posts, 1):
                f.write("-" * 80 + "\n")
                f.write(f"【第 {i} 条帖子】\n")
                f.write("-" * 80 + "\n")
                f.write(f"标题: {post.get('title', '无标题')}\n")
                f.write(f"作者: {post.get('author', '未知作者')}\n")
                f.write(f"链接: {post.get('url', '无链接')}\n")
                f.write("\n【内容】\n")
                f.write(post.get('content', '无内容') + "\n")
                f.write("\n\n")

    def _write_to_json(self, posts, filepath):
        result = {
            "metadata": {
                "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total_posts": len(posts)
            },
            "posts": posts
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    def write_single_post(self, post, index, format="txt"):
        if not post:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"post_{index}_{timestamp}"
        filepath = os.path.join(self.output_dir, f"{filename}.{format}")

        try:
            if format == "txt":
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"标题: {post.get('title', '无标题')}\n")
                    f.write(f"作者: {post.get('author', '未知作者')}\n")
                    f.write(f"链接: {post.get('url', '无链接')}\n")
                    f.write("\n【内容】\n")
                    f.write(post.get('content', '无内容') + "\n")
            elif format == "json":
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(post, f, ensure_ascii=False, indent=2)

            print(f"单条帖子已写入到: {filepath}")
            return filepath

        except Exception as e:
            print(f"写入单条帖子失败: {e}")
            return None
