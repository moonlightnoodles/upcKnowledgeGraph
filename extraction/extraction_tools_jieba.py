import jieba.analyse
import jieba.posseg as pseg

def extract_entity(user_input, top_k=10):
    try:
        # 打开并读取文件内容

        content = user_input

        # 使用jieba库提取关键词
        tags = jieba.analyse.extract_tags(content, topK=top_k,withWeight=True)
        return tags
        # result = " ".join(tags)
        # return result

    except Exception as e:
        print(f"发生错误: {e}")
        return []


def extract_relation(user_input, top_k=10):
    try:
        words = pseg.cut(user_input)
        s_list = []
        s_dict = {}
        for word, flag in words:

            if flag == 'v':
                if flag in s_dict:
                    s_dict[flag] += word
                else:
                    s_dict[flag] = word
            elif s_dict != {}:
                s_list.append(s_dict['v'])
                s_dict.clear()

        result = " ".join(s_list)

        return result
    except Exception as e:
        print(f"发生错误: {e}")
        return []
# 示例用法
if __name__ == "__main__":
    # 这里仅作为示例调用，实际使用时应根据需要调用此函数
    userinput = '我爱喝橙汁,我爱天安门'  # 替换为你的文件名
    # top_keywords = extract_entity(user_input=userinput, top_k=5)
    # # print("提取的关键词:", ", ".join(top_keywords))
    # print(top_keywords)

    result = extract_relation(userinput,3)
    print(result)