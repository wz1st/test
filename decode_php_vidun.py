import base64, re, os

def devidun(base, a, b):
	table = ''.maketrans(a, b)
	base=str(base,encoding='utf8')
	list1 = str(base64.b64decode(base.translate(table)),encoding='utf8').split('\n')
	list1[0] = '<?php'
	code = bytes('\n'.join(list1), encoding = "utf8")
	return code

def codewrite(filename):
	pass
	with open(filename, 'rb') as f:
		code = f.readlines()
	r = rb'eval.*?\(\'(.*?)\'\)\)'
	base1 = re.findall(r, code[1])[0]
	text = base64.b64decode(base1)
	r1 = str(re.findall(rb'\'([a-zA-Z0-9+\/]{64})=\'', text)[0])
	r2 = str(re.findall(rb'\'([a-zA-Z0-9+\/]{64})\'', text)[0])
	os.rename(filename, filename+'.bak')
	with open(filename, 'wb') as f:
		f.write(devidun(code[2], r1, r2))
# codewrite('admin.php')
def path(path):
	parents = os.listdir(path)
	for parent in parents:
		child = os.path.join(path,parent)
		if os.path.isdir(child):
			gci(child)
		else:
			if child.split('.')[-1] == 'php':
				try:
					print('decoding file->'+child)
					codewrite(child)
					print('\t\tok')
				except IndexError:
					pass

path('.')
