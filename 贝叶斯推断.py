import re,collections
# 读取所有单词
def words(text):
	return re.findall('[a-z]+',text.lower())

# 所有单词出现频率存储
def train(features):
	model =collections.defaultdict(lambda:1)
	for f in features:
		model[f] += 1
	return model

NWORDS=train(words(file('big.txt').read()))

# 相邻顺序字典
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# 生成所有与输入参数word的'编辑距离'为1的词(编辑距离:hello写成hallo,被视为编辑距离为1, 如果写成了haallo,那编辑距离是2)
def edits1(word):#abc
	#输入单词按照每一位分割成前后两半
	# [('','abc'),('a','bc'),('ab','c'),('abc','')]
	splits = [(word[:i],word[i:]) for i in range(len(word)+1)]
	# 依次删除一个单词,组成新的词(在splits循环.如果b是空,排除掉)
	#('','abc') -> 'bc'
	#['bc','ac','ab']
	beletes = [a+b[1:] for a,b in splits if b]
	#互换相邻两个字母
	#['bac','acb']
	transposes = [a+b[1]+b[0]+b[2:] for a,b in splits if len(b)>1]
	#每一位依次替换成26个字母
	#['abc','aac','aba','bbc','abc','abb'...]  26X3个
	replaces = [a+c+b[1:] for a,b in splits for c in alphabet if b]
	#每一位中间加入一个字母
	#['aabc','aabc','abac','abca','babc','abbc','abcb'...] 26X4
	inserts =[a+c+b for a,b in splits for c in alphabet]
	print('count:'+str(len(beletes))+' t:'+str(len(transposes))+' r:'+str(len(replaces))+' i:'+str(len(inserts)))
	#有54*n+25个数量,但是我认为,有重复数据
	return set(beletes+transposes+replaces+inserts)

# 生成编辑距离为2的词语.?? 这样会返回一个巨量数组,需要优化
def edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

#优化后
def know_edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

# 从所有备选的词中,选出用户最可能想要拼写的词
def known(words):
	set(w for w in words if w in NWORDS)

def correct(word):
	candidates = known([word]) or known(edits1(word)) or know_edits2(word) or [word]
	return max(candidates, key=NWORDS.get)

edits1('abc')

