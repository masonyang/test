#!/usr/bin/env python
# coding: utf-8
import infoparsing
import	platform
import re
import sys
import direction
import jieba  
import networkx as nx  
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer 

reload(sys)
sys.setdefaultencoding('utf8')

def cut_sentence(sentence):  
    """ 
    分句 
    :param sentence: 
    :return: 
    """  
    if not isinstance(sentence, unicode):
        sentence = sentence.decode('utf-8')
    delimiters = frozenset(u'。！？')
    buf = []  
    for ch in sentence:  
        buf.append(ch)  
        if delimiters.__contains__(ch):  
            yield ''.join(buf)  
            buf = []  
    if buf:  
        yield ''.join(buf)  
  
  
def load_stopwords(path='/Users/yangminsheng/masonInPython/epaper_clock/stopwords.txt'):  
    """ 
    加载停用词 
    :param path: 
    :return: 
    """  
    with open(path) as f:  
        stopwords = filter(lambda x: x, map(lambda x: x.strip().decode('utf-8'), f.readlines()))  
    stopwords.extend([' ', '\t', '\n'])  
    return frozenset(stopwords)  
  
  
def cut_words(sentence):  
    """ 
    分词 
    :param sentence: 
    :return: 
    """  
    stopwords = load_stopwords()  
    return filter(lambda x: not stopwords.__contains__(x), jieba.cut(sentence))  
  
  
def get_abstract(content, size=3):  
    """ 
    利用textrank提取摘要 
    :param content: 
    :param size: 
    :return: 
    """  
    docs = list(cut_sentence(content))  
    tfidf_model = TfidfVectorizer(tokenizer=jieba.cut, stop_words=load_stopwords())  
    tfidf_matrix = tfidf_model.fit_transform(docs)  
    normalized_matrix = TfidfTransformer().fit_transform(tfidf_matrix)  
    similarity = nx.from_scipy_sparse_matrix(normalized_matrix * normalized_matrix.T)  
    scores = nx.pagerank(similarity)  
    tops = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)  
    size = min(size, len(docs))  
    indices = map(lambda x: x[0], tops)[:size]  
    return map(lambda idx: docs[idx], indices)  
  
  
# s = u'要说现在当红的90后男星，那就不得不提鹿晗、吴亦凡、杨洋、张艺兴、黄子韬、陈学冬、刘昊然，2016年他们带来不少人气爆棚的影视剧。这些90后男星不仅有颜值、有才华，还够努力，2017年他们又有哪些傲娇的作品呢？到底谁会成为2017霸屏男神，让我们拭目以待吧。鹿晗2016年参演《盗墓笔记》、《长城》、《摆渡人》等多部电影，2017年他将重心转到了电视剧。他和古力娜扎主演的古装奇幻电视剧《择天记》将在湖南卫视暑期档播出，这是鹿晗个人的首部电视剧，也是其第一次出演古装题材。该剧改编自猫腻的同名网络小说，讲述在人妖魔共存的架空世界里，陈长生(鹿晗饰演)为了逆天改命，带着一纸婚书来到神都，结识了一群志同道合的小伙伴，在国教学院打开一片新天地。吴亦凡在2017年有更多的作品推出。周星驰监制、徐克执导的春节档《西游伏魔篇》，吴亦凡扮演“有史以来最帅的”唐僧。师徒四人在取经的路上，由互相对抗到同心合力，成为无坚不摧的驱魔团队。吴亦凡还和梁朝伟、唐嫣合作动作片《欧洲攻略》，该片讲述江湖排名第一、第二的林先生(梁朝伟饰)和王小姐(唐嫣饰)亦敌亦友，二人与助手乐奇(吴亦凡饰)分别追踪盗走“上帝之手”地震飞弹的苏菲，不想却引出了欧洲黑帮、美国CIA、欧盟打击犯罪联盟特工们的全力搜捕的故事。吴亦凡2017年在电影方面有更大突破，他加盟好莱坞大片《极限特工3：终极回归》，与范·迪塞尔、甄子丹、妮娜·杜波夫等一众大明星搭档，为电影献唱主题曲《JUICE》。此外，他还参演吕克·贝松执导的科幻电影《星际特工：千星之城》，该片讲述一个发生在未来28世纪星际警察穿越时空的故事，影片有望2017年上映。'  

s = u'北京时间4月5日，76人在客场以115-108击败活塞。乔尔-恩比德的缺阵并没有使76人止步不前，球队近期在本-西蒙斯的带领下高歌猛进，如今已经豪取12连胜。“自乔尔（恩比德）受伤后，更衣室里的每个人都站了出来，我们知道队里即便没有他，也是有能力赢下比赛的，”西蒙斯赛后说道，“我们叫他为季后赛的到来做好准备，而其他的一切则交由我们处理即可，如今我们正在证明我们可以做到这一点。”今日来到汽车城，费城的两位老将JJ-雷迪克和马科-贝里内利皆有不俗发挥，两人在此役合力砍下了44分。“他们（76人）拥有全联盟最好的两位无球射手——雷迪克和贝里内利，”活塞主帅斯坦-范甘迪赛后说道，“他们在今晚击溃了我们。”76人今天几乎整场压制活塞，三节过后已经领先对手有17分之多。然而底特律人并没有就此缴械投降，他们在比赛最后时刻掀起猛烈反扑，一度在距离比赛结束还有19.3秒时将分差缩小到只差6分。“你总是想要在关键时刻避免失误，但与此同时，你也必须得表扬活塞队在此间的出色表现，”76人主帅布雷特-布朗赛后说道，“这是我们背靠背的第二场比赛，而且我们在今晚正试图终结对手的季后赛希望。在这样的形势下，你必须得通过扼杀对手的斗志来击败他们，这可并非是件容易的事。他们在比赛最后时刻命中了一些关键三分，并迫使我们出现了一些失误。”在此役结束之后，活塞与东部第八雄鹿之间的差距被拉大到5场，由于常规赛目前只剩下最后4场比赛，这意味着活塞逆袭闯入季后赛的希望已经彻底破灭。“这很难受，因为闯入季后赛是我们在去年九月集结时所许下的目标，”活塞前锋雷吉-布洛克赛后说道，“但事情终究已经发生了，总会有些球员要离开。”下一场比赛，76人将在后天主场迎战骑士；而活塞将在同一天主场迎战独行侠。'

for i in get_abstract(s):  
    print i
# if __name__=='__main__':
	# if platform.system() == 'Darwin':
	# 	# print('Mac')
	# 	# obj = infoparsing.textParsing('我打算买苹果手机')
	# 	obj = infoparsing.textParsing('视频搜索')
	# 	print obj.done()
	# elif platform.system() == 'Linux':
	# 	print('Linux')
	# else:
	# 	print('Windows')
	# pass
	# PATTERN = ur'([\u4e00-\u9fa5]{1,10}?(?:到))([\u4e00-\u9fa5]{1,10}?(?:怎么走)){0,3}'

	# data = '新疆维吾尔到伊犁州怎么走'

	# data_utf8 = data.decode('utf8')

	# pattern = re.compile(PATTERN)

	# m = pattern.search(data_utf8)

	# if m.lastindex >= 1:
	# 	origin = m.group(1).replace('到','')
	# if m.lastindex >= 2:
	# 	distine = m.group(2).replace('怎么走','')

	# out = '%s|%s' %(origin, distine)

	# print(out)
	# direct = direction.Direction()
	# de = direct.run('人民公园到淮海路怎么走')
	# print(de)