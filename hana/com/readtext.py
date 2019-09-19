#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import  re
import io
import os
print("在模型文件中提取数据，用于服务测试")
import  time
import logging

def getTestdata_PMML(modelzipname):
    """
    测试数据范例：
       {"instances": [{"mean radius":6.2,
       "mean texture":2.2, "mean perimeter":1.1,
       "mean area":1., "mean smoothness":1., "mean compactness":1.,
       "mean concavity":1.,
       "mean concave points":1.
       }]}
    """
    datas = ''
    logging.info("下载的模型文件名:"+modelzipname)
    if os.path.exists (modelzipname)== True :
        z = zipfile.ZipFile(modelzipname, "r")
        des_filename = ""
        for filename in z.namelist ():
            reee = re.compile(r'(.+?\.txt$)').findall(str(filename))
            if reee != []:
                des_filename = reee[0]
                #print(des_filename)
                logging.info(des_filename)
        with zipfile.ZipFile(modelzipname) as myzip:
            with myzip.open(des_filename) as myfile:
                bytes_ty = myfile.read()
                print(type(myfile))
                aaaa=type(myfile.read())
                print(aaaa)
                tring = bytes_ty.decode()
                alllins = tring.split('\n')
                for lineone in alllins:
                    if lineone.__contains__("DataField"):
                        logging.info ("打印一行数据")
                        result = re.compile(r'(name=".+?")').findall(lineone)
                        logging.info (result)
                        if result==[]:
                            continue
                        else:
                            onedata= result[0].replace ("name=", "")
                        logging.info (onedata)
                        if datas=="":
                            datas=onedata+":6.1"
                        else:
                            datas=datas+","+onedata + ":6.1"
                testdata = '{\"instances\": [{'+datas+'}]}'
                logging.info("生成的测试数据："+testdata)
                print(testdata)
        return testdata
    else:
        return ""
def save_testdata(modelzipname,testdata):
    testdatatofile = modelzipname + time.strftime ("%Y%m%d%H%M%S",time.localtime())
    print(time.strftime ("%Y%m%d%H%M%S", time.localtime()))
    fo = open('TestServiceDatas' + ".txt", "a+")
    fo.write(testdatatofile + ":\n" + testdata + ":\n")
    print("文件名: ", fo.name)
    fo.close()

def TestallTestDataIn(dirname):
    #dirname = '../datas/PMMLzip'
    ziplist=[]
    for root, dirs, files in os.walk(dirname):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
        ziplist=files
    for zipname in ziplist:
        #zipname = '../datas/PMMLzip/model_54638.zip'
        zipname_one = zipname
        print("zipname_one:" + zipname_one)
        service_testdata = getTestdata_PMML(dirname+zipname_one)
        save_testdata(zipname_one, service_testdata)

TestallTestDataIn('../datas/PMMLzip/')
