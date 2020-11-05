import json
import requests


class Translator:
    @staticmethod
    def translate(text, src, dst):
        src = src.replace("-", "_")
        dst = dst.replace("-", "_")
        tp = src.upper() + "2" + dst.upper()
        url = f"http://fanyi.youdao.com/translate?&doctype=json&type={tp}&i={text}"
        resp = requests.get(url)
        return json.loads(resp.content)


def test():
    translator = Translator()
    print(translator.translate("你叫什么名字", "zh-CN", "en"))


if __name__ == "__main__":
    test()