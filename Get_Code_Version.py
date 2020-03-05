import urllib.request
import re
from lxml import etree
from tkinter import *

class searchcode():
    def __init__(self,title):
        """initialize the window"""
        self.basicwin=Tk()
        self.basicwin.title(title)
        self.makewidgets()
        self.basicwin.mainloop()

    def makewidgets(self):
        """to make the windows"""
        row=Frame(self.basicwin)
        lab = Label(row, text='Input Code Name', width=14, font=('Times New Roman', 12, 'normal'))
        self.var=StringVar()
        ent=Entry(row,width=40)
        ent.bind('<Return>', self.oneventsearch)
        ent.config(textvariable=self.var,font=('华文宋体 常规', 12, 'normal'))
        btn1=Button(row, text='search', font=('Times New Roman', 12, 'normal'),command=self.onsearch)
        btn2=Button(row, text='clear', font=('Times New Roman', 12, 'normal'),command=self.onclearall)
        row.pack(side=TOP,fill=BOTH)
        lab.pack(side=LEFT)
        ent.pack(side=LEFT)
        btn1.pack(side=LEFT)
        btn2.pack(side=LEFT)
        self.outtext=Text(self.basicwin, width=68, height=10)
        self.outtext.config(font=('华文宋体 常规', 12, 'normal'))
        self.outtext.pack(side=TOP)
            
    def onsearch(self):
        """to search the code name or code number on the internet"""
        self.keyname=self.var.get()
        headers=('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36')
        opener=urllib.request.build_opener()
        opener.addheaders=[headers]
        urllib.request.install_opener(opener)
        urlfirst='http://www.csres.com/s.jsp?keyword='+urllib.request.quote(self.keyname.encode(encoding='gbk'))
        data=urllib.request.urlopen(urlfirst).read().decode('gbk','ignore')
        treedata=etree.HTML(data)
        page=treedata.xpath('//span[@class="hei14"]/text()')[0]
        pagepat='，共(.*?)页'
        try:
            pagenum=int(re.compile(pagepat).findall(page)[0])
        except:
            pagenum=0
        self.onprocessdata(treedata,data)
        if pagenum>1:
            for i in range(1,pagenum):
                newurl = 'http://www.csres.com/s.jsp?keyword=' + urllib.request.quote(self.keyname.encode(encoding='gbk'))+'&pageNum='+str(i+1)
                newdata = urllib.request.urlopen(newurl).read().decode('gbk', 'ignore')
                newtreedata = etree.HTML(newdata)
                self.onprocessdata(newtreedata,newdata)

    def onprocessdata(self,treedata,data):
        """to process the data got from internet"""
        version=treedata.xpath('//tr[@bgcolor="#FFFFFF"]/td/a/font/text()')
        name=treedata.xpath('//tr[@bgcolor="#FFFFFF"]/td[@align="left"]/font/text()')
        pat='<td ><.*?>(.*?)</font></td>'
        others=re.compile(pat).findall(data)
        condition=[others[i] for i in range(1,len(others),2)]
        #others like ['2018-06-01','现行','2015-05-01','作废']
        if name:
            num = 0
            for ver,na,con in zip(version,name,condition):
                if con != '作废' and con != '废止':
                    self.outtext.insert(INSERT,ver+'  '+na+'  '+con+'\n')
                    num+=1
            if num==0:
                self.outtext.insert(INSERT,self.keyname+' has no current version\n')
        else:
            self.outtext.insert(INSERT,'there is no such code'+'\n')

    def oneventsearch(self,event):
        self.onsearch()

    def onclearall(self):
        """to clear the windows"""
        self.outtext.delete('1.0','end')
        

    def onwritetoword(self):
        """to save the result, now not used"""
        content=self.outtext.get('1.0',END+'-1c')
        file=open('.\\codecontent.txt','w')
        file.write(content)
        file.close()

basicwin=searchcode('Search Code Version(From "http://www.csres.com/")')

        
        




    
    

    
    
