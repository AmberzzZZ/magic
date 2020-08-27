import wordcloud
import cv2


if __name__ == '__main__':

    mk = cv2.imread("bg.png", 0)

    # 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            mask=mk,
                            stopwords={},
                            font_path="/System/Library/Fonts/Avenir.ttc",
                            prefer_horizontal=1)

    # generate from string
    w.generate('of the people, by the people, for the people, shall not perish from the earth.')

    # generate from txt
    f = open('xxx.txt', encoding='utf-8')
    txt = f.read()
    w.generate(txt)

    # generate from list
    wordlst = ['A', 'A', 'B']
    w.generate(' '.join(wordlst))

    # generate from dict
    worddict = {'A':25, 'B':16}
    w.generate_from_frequencies(worddict)

    # generate
    w.to_file('wc.png')

