from typing import Iterable

import json
import time
import random
import tqdm
import collections

from baidu import translate


translator = translate.Dict()

# Mapping from standard lang id (see README.md for more details)
# to target (baidu) lang id
_LANG_MAPPING = {
    "zh-CN": "zh",
    "en": "en",
    "ja": "jp",
    "ko": "kor",
    "fr": "fra",
    "es": "spa",
    "th": "th",
    "de": "de",
    "zh-TW": "cht"
}


def trans(text: str,
          src: str,
          dst: str,
          sleep_mean: float = 1.0,
          sleep_dev: float = 0.3) -> str:
    """
    调用百度翻译接口进行单次翻译。

    参数：
    ------
    text: ``str``
        要翻译的文本
    src: ``str``
        源语言代码，详见``README.md``
    dst: ``str``
        目标语言代码，详见``README.md``
    sleep_mean: ``float``, optional, default=``1.0``
        延迟均值（为了防止ip被封，需要延迟）
    sleep_dev: ``float``, optional, default=``0.3``
        延迟标准差
    """
    # TODO: 设计一个自适应的算法来控制延迟
    time.sleep(max(0.1, random.gauss(sleep_mean, sleep_dev)))
    res = translator.dictionary(text, dst=_LANG_MAPPING[dst], src=_LANG_MAPPING[src])
    return res['trans_result']['data'][0]['dst']

def back_translate(text: str,
                   lang_list: Iterable[str],
                   sleep_mean: float = 1.0,
                   sleep_dev: float = 0.3) -> str:
    """
    调用百度翻译接口进行单次回译。

    参数：
    ------
    text: ``str``
        要回译的文本
    lang_list: ``Iterable[str]``
        要回译的语言代码列表。例如要将一句话从中文翻译到英文再翻译回中文，则指定：
        ``lang_list=("zh-CN", "en", "zh-CN"])``
    sleep_mean: ``float``, optional, default=``1.0``
        延迟均值（为了防止ip被封，需要延迟）
    sleep_dev: ``float``, optional, default=``0.3``
        延迟标准差
    """
    assert len(lang_list) >= 2
    current_text = text
    for i in range(len(lang_list) - 1):
        current_text = trans(current_text, src=lang_list[i], dst=lang_list[i+1],
                             sleep_mean=sleep_mean, sleep_dev=sleep_dev)
    return current_text

def main():
    input_file = "../input/questions.json"
    output_file = "../output/baidu.json"
    schemas = [
        ('zh-CN', 'en', 'zh-CN'),
        ('zh-CN', 'ja', 'zh-CN'),
        ('zh-CN', 'ko', 'zh-CN'),
        ('zh-CN', 'fr', 'zh-CN'),
        ('zh-CN', 'es', 'zh-CN'),
        ('zh-CN', 'th', 'zh-CN'),
        ('zh-CN', 'de', 'zh-CN'),
        ('zh-CN', 'zh-TW', 'zh-CN')
    ]

    input_json = json.load(open(input_file, "r", encoding="utf-8"))
    output_json = collections.OrderedDict()
    for i in tqdm.tqdm(range(102)):
        key = str(i + 1)
        text = input_json[key]
        item_result = collections.OrderedDict()
        item_result["origin"] = text
        for schema in schemas:
            try:
                item_result[" -> ".join(schema)] = back_translate(text, lang_list=schema)
            except Exception as e:
                print("您的请求速度过快")
        output_json[key] = item_result
    json.dump(output_json, open(output_file, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

def test():
    schemas = [
        ('zh-CN', 'en', 'zh-CN'),
        ('zh-CN', 'ja', 'zh-CN'),
        ('zh-CN', 'ko', 'zh-CN'),
        ('zh-CN', 'fr', 'zh-CN'),
        ('zh-CN', 'es', 'zh-CN'),
        ('zh-CN', 'th', 'zh-CN'),
        ('zh-CN', 'de', 'zh-CN'),
        ('zh-CN', 'zh-TW', 'zh-CN')
    ]
    origin = "什么是研发项目"
    for schema in schemas:
        print(" -> ".join(schema), ":", back_translate(text=origin, lang_list=schema))


if __name__ == "__main__":
    test()
    # main()