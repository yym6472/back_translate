from typing import Dict, List, Callable, Any

import json
import random


def back_translate(text: str,
                   schemas: Dict[str, List[List[str]]],
                   keywords: List[str] = None,
                   handle_func: Callable[[Dict[str, str]], Any] = lambda x: x) -> Any:
    """
    输入一句话，使用不同翻译平台、翻译模式（中间语言）进行数据增强，生成多个回复句子。

    参数：
    ------
    text: ``str``
        输入的句子
    schemas: ``Dict[str, List[List[str]]]``
        定义了翻译平台和翻译模式（中间语言），见``input/schemas.json``
    keywords: ``List[str]``, optional, default=``None``
        如果指定了keywords，则使用keyword mask的方法，否则不使用
    handle_func: ``Callable[[Dict[str, str]], Any]``, optional, default=``lambda x: x``
        对结果（res）进行处理，例如：
        过滤掉重复的生成结果、改变输出结构、限制最大生成个数、使用匹配模型进行过滤等
    """
    res = {"origin": text}
    for platform, schema_list in schemas.items():
        trans_func = __import__(f"{platform}.main", fromlist=platform).back_translate
        for schema in schema_list:
            try:
                schema_key = "->".join(schema)
                res[f"{platform}    {schema_key}"] = trans_func(text, lang_list=schema)
            except Exception:
                pass

            if keywords:  # 使用keyword mask
                keywords = list(set(keywords))  # 过滤重复keywords
                hit_keywords = [keyword for keyword in keywords if keyword in text]
                for selected_keyword in hit_keywords:
                    try:
                        replaced_text = text.replace(selected_keyword, "UNK")
                        back_translate_res = trans_func(replaced_text, lang_list=schema)
                        if "UNK" in back_translate_res or "unk" in back_translate_res:
                            back_translate_res = back_translate_res.replace("UNK", selected_keyword)
                            back_translate_res = back_translate_res.replace("unk", selected_keyword)
                            res[f"{platform}    {schema_key}    kw_mask{selected_keyword}"] = back_translate_res
                    except Exception:
                        pass

    return handle_func(res)

def test():
    def handle_res(res):
        no_repeat = list(set(res.values()))
        for item in no_repeat:
            print(item)
        return no_repeat
    schemas = json.load(open("./input/schemas.json", "r"))
    keywords = [line.strip() for line in open("./input/keywords.txt", "r")]
    result = back_translate("后评估工作如何开展？", schemas, keywords)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print(json.dumps(handle_res(result), indent=4, ensure_ascii=False))


if __name__ == "__main__":
    test()