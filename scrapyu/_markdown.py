from itertools import count

from path import Path
from html2text import HTML2Text


class MarkdownPipeline(object):
    index = count(1)

    def open_spider(self, spider):
        folder_name = spider.settings.get('MARKDOWNS_STORE', 'markdowns')
        folder = Path(folder_name)
        folder.isdir() or folder.mkdir()    # 如果保存文件不存在,创建
        self.folder = folder
        self.handle = HTML2Text().handle    # 将html文件转换为markdown格式文件的方法

    def process_item(self, item, spider):
        html = item['html']
        text = self.handle(html)        # 将html文本转换markdown格式
        # 如果没有设置文件名则将文件名设置为从1开始增长的数字
        filename = item.get('filename', str(next(self.index)))
        f = self.folder / '{}.md'.format(filename)
        f.write_text(text)
        return item