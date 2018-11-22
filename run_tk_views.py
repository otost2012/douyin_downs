from tkinter.ttk import Button,Entry,Radiobutton
from tkinter import Tk,Listbox,messagebox,filedialog,StringVar,END,Label,X,Scrollbar,HORIZONTAL,VERTICAL
import os,requests
from douyin_downs.get_share_uid import get_uid
from douyin_downs.douyin_download import douyin
from douyin_downs.video_image import cut_pic
from xpinyin import Pinyin



class App(object):
    def __init__(self):
        self.w=Tk()
        self.w.title('抖音下载器')
        self.w.geometry('400x320')
        self.w.iconbitmap('res/image/logo.ico')
        self.creat_res()
        self.w.mainloop()

    def creat_res(self):
        self.temp=StringVar()
        self.num=StringVar()#截图数量
        self.water=StringVar()#是否水印
        self.pics=StringVar()#是否截图
        self.L_enter=Label(self.w,text='请输入抖音分享链接',fg='#32CD32')
        self.L_res=Label(self.w,text='信息',bg='#F0FFF0',fg="#B452CD")
        self.L_message=Label(self.w,text='',bg='#71C671')
        self.E_enter=Entry(self.w,textvariable=self.temp)
        self.B_go=Button(self.w,text='GO')
        self.L_box=Listbox(self.w)
        self.S_bal=Scrollbar(self.w,orient=VERTICAL,bg='red')
        self.S_x_bal=Scrollbar(self.w,orient=HORIZONTAL,bg='red')
        self.R_water1=Radiobutton(self.w,text='有水印',variable=self.water,value='1')
        self.R_water2=Radiobutton(self.w,text='无水印',variable=self.water,value='2')
        self.R_savepic1=Radiobutton(self.w,text='截图张数',variable=self.pics,value='1')
        self.R_savepic2=Radiobutton(self.w,text='不截图',variable=self.pics,value='2')
        self.E_num_pics=Entry(self.w,textvariable=self.num)
        self.res_place()
        self.res_config()

    def res_place(self):
        self.L_enter.place(x=10,y=10,width=150,height=30)
        self.E_enter.place(x=10,y=50,width=200,height=30)
        self.B_go.place(x=220,y=50,width=40,height=30)
        self.L_message.place(x=180,y=10,width=200,height=30)
        self.L_box.place(x=10,y=120,width=200,height=170)
        self.L_res.place(x=260,y=140,width=100,height=100)
        self.S_bal.place(x=210,y=120,width=15,height=170)
        self.R_water1.place(x=10,y=85,width=60,height=30)
        self.R_water2.place(x=100,y=85,width=60,height=30)
        self.R_savepic1.place(x=180,y=85,width=80,height=30)
        self.E_num_pics.place(x=260,y=88,width=30,height=25)
        self.R_savepic2.place(x=295,y=85,width=60,height=30)
        self.S_x_bal.place(x=10,y=280,width=200,height=15)

    def res_config(self):
        self.S_bal.config(command=self.L_box.yview)
        self.L_box["yscrollcommand"] = self.S_bal.set
        self.S_x_bal.config(command=self.L_box.xview)
        self.L_box["xscrollcommand"] = self.S_x_bal.set
        self.B_go.config(command=self.get_user_uid)
        self.water.set('2')#默认无水印
        self.pics.set('1')#默认截图
        self.num.set(1)

    def pics_num_set(self):
        if int(self.num.get())>5:
            messagebox.showwarning(title='提示',message='只允许截图5张')
        elif int(self.num.get())<1:
            messagebox.showwarning(title='提示',message='如果不需要，请选择不截图')

    def get_user_uid(self):
        self.pics_num_set()#设置截图数量
        self.clear_box()#清空box
        d=douyin()
        d.msg_lis.clear()#清空列表
        try:
            uid=get_uid(self.temp.get())
            print(uid)
            print(self.water.get())
            self.L_message.config(text='用户ID：{}'.format(uid))
            if uid:
                print(self.water.get(),type(self.water.get()))
                if self.water.get()=='1':#有水印
                    watermark=True
                elif self.water.get()=='2':#无水印
                    watermark=False
                print(uid,type(uid),watermark)
                self.get_uid_vdo(str(uid),watermark)
            elif uid==False:
                messagebox.showerror(title='错误',message='未解析出uid')
        except Exception:
            messagebox.showerror(title='友情提示',message='请输入分享链接')

    def clear_box(self):
        self.L_box.delete(0,END)

    def box_show(self,msg):
        self.L_box.insert(END,msg)

    def show_res(self):
        msg_video_water=''
        msg_pics=''
        if self.water.get()=='2':
            msg_video_water='选择:无水印'
        elif self.water.get()=='1':
            msg_video_water='选择:有水印'
        if self.pics.get()=='1':
            msg_pics='每个视频截图{}张'.format(self.num.get())
        elif self.pics.get()=='2':
            msg_pics='选择:无截图'
        print('提示',msg_video_water,msg_pics)
        msg='当前信息：'+'\n'+msg_video_water+'\n'+msg_pics+'\n'
        self.L_res.config(text=msg)

    def get_uid_vdo(self,uid,watermark):
        print('test-ok')
        print('jietu',self.pics.get())
        d=douyin()
        while True:
            flag,nickname,name_list=d.run(uid,watermark)
            print(name_list)
            n = int(self.num.get())
            for i in name_list:
                self.down_pics(nickname,i,n)
            for m in d.msg_lis:
                self.box_show(m)
            if flag is True:
                self.L_message.config(text='视频已全部下载完')
                self.show_res()#显示爬虫结果
                break


    def down_pics(self,nickname,video_name,n):
        print('down')
        print(self.pics.get())
        if self.pics.get()=='1':#选择下载
            print('截图 ')
            cut_pic(nickname,video_name,n)#三个参数 用户名，视频文件名，数量
        elif self.pics.get()=='2':
            print('不截图')

if __name__ == '__main__':
    a=App()