import zipfile
import os
from tempfile import NamedTemporaryFile, TemporaryFile
from xml.etree import ElementTree

def unZip(dir, file ,tempfile_name):
    file_name = os.path.splitext(file)[0]
    zip_file = zipfile.ZipFile(tempfile_name)
    file_dir = dir + file_name + '_unzip_files'
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    for names in zip_file.namelist():
        zip_file.extract(names, file_dir)
    zip_file.close()
    return file_dir


def createTempFile(file,dir):
    # 读取OFD文件
    file1 = open(dir +file, 'rb')
    # 创建临时zip文件
    temp = NamedTemporaryFile(suffix='.zip', dir=dir, delete=False)
    # 获取临时文件完整路径
    temp_name = temp.name
    # print(temp_name)
    # 将OFD文件数据复制到临时zip文件中
    temp.write(file1.read())
    # 解压缩
    file_dir = unZip(dir, file, temp_name)
    # 删除临时文件
    temp.close()
    os.remove(temp_name)
    # 返回解压缩文件夹路径
    return file_dir
# 解析解压缩文件夹
def parseOFDFiles(file_dir):
    ofdTree = ElementTree.parse(file_dir + '/OFD.xml')
    ns = {'ofdns': 'http://www.ofdspec.org'}
    root = ofdTree.getroot()
    for docbody in root:
        docID = docbody.find('ofdns:DocInfo', ns).find('ofdns:DocID', ns).text
        print('DocID : ' + docID)
        docRoot = docbody.find('ofdns:DocRoot', ns).text
        print('DocRoot : ' + docRoot)
        docRoot_dir = file_dir + '/' + docRoot
        parseDocument(docRoot_dir)

def parseDocument(file_dir):
    docTree = ElementTree.parse(file_dir)
    ns = {'ofdns': 'http://www.ofdspec.org'}
    root = docTree.getroot()
    outLines = root.find('ofdns:Outlines', ns)
    for outlineElems in outLines:
        getOutLines(outlineElems)

def getOutLines(outlineElems):
    ns = {'ofdns': 'http://www.ofdspec.org'}
    # 如果没有子节点输出当前结点然后return
    if(len(outlineElems) == 0):
        for outlineElem in outlineElems:
            print(outlineElem.get('Title'))
        return
    else:
        #输出当前节点
        print(outlineElem.get('Title'))
        # 获取子节点
        sub_outlineElems = outlineElems.findall('ofdns:OutlineElem', ns)
        # 递归调用
        getOutLines(sub_outlineElems)

dir = 'C:/Users/dell/Desktop/ofd/test/'
f = '测试文档.ofd'
# file_dir = createTempFile(f, dir)
file_dir = 'C:/Users/dell/Desktop/ofd/test/测试文档_unzip_files'
# print(file_dir)
parseOFDFiles(file_dir)



