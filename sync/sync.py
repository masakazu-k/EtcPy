#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# リストファイルから同期するリストを読み取り，指定先へコピー
# もしくは削除する
# python sync.py conf=list.txt #同期
# python sync.py conf=list.txt del #削除
# コメントアウトは#
# フォルダ名やファイル名以外のスペースは禁止
#
import os
import shutil
import sys
if __name__=='__main__':
    argvs = sys.argv
    f2f_flag = True
    f2d_flag = True
    d2d_flag = True
    cpy_flag = True
    cfile     = os.environ['HOME']+'/list.txt'
    if len(argvs) > 1:
        for r in argvs:
            if r =='nf2f':
                f2f_flag = False
            elif r =='nf2d':
                f2d_flag = False
            elif r =='nd2d':
                d2d_flag = False
            elif r =='del':
                cpy_flag = False
            elif r[0:5] =='conf=':
                r = r.split('=')
                r = r[1]
                print('confile=%s'%r)
                cfile = r
    l = 0
    f = open(cfile,'r')
    for line in f:
        l = l+1
        if line[0]=='#':
            continue
        if len(line)<=1:
            continue
        data = line.split(":>")
        if len(data)<2:
            print('定義が不明 %d行'%l)
            continue
        t = data[0]
        line = data[1]
        v = line.split(":=")
        if len(v)<2:
            print('定義が不明 %d行'%l)
            continue
        if len(v[0])>0 and len(v[1])>0:
            v[1] = v[1].strip('\n')
            if t=='f2f' and f2f_flag and cpy_flag:
                print('ファイル"%s"を"%s"にコピー'%(v[1],v[0]))
                shutil.copyfile(v[1],v[0])
            elif t=='f2d' and f2d_flag and cpy_flag:
                print('ファイル"%s"をディレクトリ"%s"にコピー'%(v[1],v[0]))
                shutil.copy(v[1],v[0])
            elif t=='d2d' and d2d_flag and cpy_flag:
                print('ディレクトリ"%s"の内容をディレクトリ"%s"にコピー'%(v[1],v[0]))
                if os.path.isdir(v[0]):
                    shutil.rmtree(v[0])
                    shutil.copytree(v[1],v[0])
                else:
                    shutil.copytree(v[1],v[0])
            elif t=='f2f' and f2f_flag and not cpy_flag:
                print('"%s"を削除'%(v[0]))
                os.remove(v[0])
            elif t=='f2d' and f2d_flag and not cpy_flag:
                v[1] = v[1].split('/')
                v[1] = v[1][len(v[1])-1]
                print('ファイル"%s"をディレクトリ"%s"から削除'%(v[1],v[0]))
                if v[0][len(v[0])-1] != '/':
                    v[0] = v[0] + '/'
                os.remove(v[0]+v[1])
            elif t=='d2d' and d2d_flag and not cpy_flag:
                print('ディレクトリ"%s"の内容をディレクトリ"%s"から削除'%(v[1],v[0]))
                if v[0][len(v[0])-1] != '/':
                    v[0] = v[0] + '/'
                fl = os.listdir(v[1])
                for ft in fl:
                    print('"%s"を削除'%(v[0]+ft))
                    if os.path.isfile(v[0]+ft):
                        os.remove(v[0]+ft)
                    elif os.path.isdir(v[0]+ft):
                        shutil.rmtree(v[0]+ft)

    print('終了')
    f.close()
