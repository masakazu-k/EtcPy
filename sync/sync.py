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
def f2f_copy(ff,tf,onlynew):
    if onlynew == False:
        print('ファイル"%s"を"%s"にコピー'%(ff,tf))
        shutil.copyfile(ff,tf)
    else:
        if(os.stat(ff) > os.stat(tf)):
            print('ファイル"%s"を"%s"にコピー'%(ff,tf))
            shutil.copyfile(ff,tf)

def f2d_copy(ff,td,onlynew,mkdir):
    f = ff.split('/')
    f = f[len(f)-1]
    if td[len(td)-1] != '/':
        td = td + '/'
    if( not os.path.exists(td) ):
        if mkdir:
            print('ディレクトリ"%s"を作成'%(td))
            os.mkdir(td)
        else:
            return
    tf = td + f
    f2f_copy(ff,tf,onlynew)

def d2d_copy(fd,td,onlynew,mkdir):
    if td[len(td)-1] != '/':
        td = td + '/'
    if fd[len(fd)-1] != '/':
        fd = fd + '/'
    fdl = os.listdir(fd)
    for ft in fdl:
        ff = fd + ft
        tf = td + ft
        if os.path.isfile(ff):
            #コピー元がファイルだった場合
            f2d_copy(ff,td,onlynew,mkdir)
        elif os.path.isdir(ff):
            #コピー元がディレクトリだった場合
            d2d_copy(ff,tf,onlynew,mkdir)

def f2f_delete(ff,tf):
    if os.path.exists(tf) and os.path.isfile(tf):
        print('ファイル"%s"を削除'%(tf))
        os.remove(tf)
    else:
        print('ファイル"%s"が存在しません'%(tf))

def f2d_delete(ff,td,rmdir):
    f = ff.split('/')
    f = f[len(f)-1]
    if td[len(td)-1] != '/':
        td = td + '/'
    if( not os.path.exists(td) ):
        print('ディレクトリ"%s"が存在しません'%(td))
        return
    tf = td + f
    f2f_delete(ff,tf)
    if rmdir and (len(os.listdir(td))==0):
        #空のディレクトリなら削除
        print('ディレクトリ"%s"を削除'%(td))
        os.rmdir(td)

def d2d_delete(fd,td,rmdir):
    if td[len(td)-1] != '/':
        td = td + '/'
    if fd[len(fd)-1] != '/':
        fd = fd + '/'
    fdl = os.listdir(fd)
    for ft in fdl:
        ff = fd + ft
        tf = td + ft
        if os.path.isfile(ff):
            #コピー元がファイルだった場合
            f2d_delete(ff,td,rmdir)
        elif os.path.isdir(ff):
            #コピー元がディレクトリだった場合
            d2d_delete(ff,tf,rmdir)

if __name__=='__main__':
    argvs = sys.argv
    f2f_flag = True
    f2d_flag = True
    d2d_flag = True
    cpy_flag = True
    oln_flag = False
    mkd_flag = True
    red_flag = True
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
            elif r =='onlynew':
                oln_flag = True
            elif r =='nmkdir':
                mkd_flag = False
            elif r =='nrmdir':
                red_flag = False
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
                f2f_copy(v[1],v[0],oln_flag)
            elif t=='f2d' and f2d_flag and cpy_flag:
                f2d_copy(v[1],v[0],oln_flag,mkd_flag)
            elif t=='d2d' and d2d_flag and cpy_flag:
                print('ディレクトリ"%s"の内容をディレクトリ"%s"にコピー'%(v[1],v[0]))
                d2d_copy(v[1],v[0],oln_flag,mkd_flag)

            elif t=='f2f' and f2f_flag and not cpy_flag:
                f2f_delete(v[1],v[0])
            elif t=='f2d' and f2d_flag and not cpy_flag:
                f2d_delete(v[1],v[0],red_flag)
            elif t=='d2d' and d2d_flag and not cpy_flag:
                print('ディレクトリ"%s"の内容をディレクトリ"%s"から削除'%(v[1],v[0]))
                d2d_delete(v[1],v[0],red_flag)

    print('終了')
    f.close()
