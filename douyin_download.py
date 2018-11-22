import os
import re
import json
import click
import random
import requests
from contextlib import closing
from ipaddress import ip_address
from subprocess import Popen, PIPE
import warnings
warnings.filterwarnings("ignore")
from xpinyin import Pinyin


# http://v.douyin.com/dBWkjr/分享用户链接获得UID
# 根据uid下载视频文件
# 抖音视频下载类
# 视频下载后保存在抖音号对应的昵称名文件夹下
# 脚本运行需先安装nodejs: https://nodejs.org/
class Change_str(object):
    def code_lis(self):
        lis1 = [i for i in range(97, 123)]
        lis2 = [i for i in range(65, 91)]
        b_lis2 = []
        s_lis = []
        num_lis = [i for i in range(0, 10)]
        for i in map(lambda x: chr(x), lis1):
            b_lis2.append(i)
        for i in map(lambda x: chr(x), lis2):
            s_lis.append(i)
        totle_str = b_lis2 + s_lis + num_lis
        totle_str.append('_')
        return totle_str

    def change_name(self, name):  # 转换中文为拼音
        p = Pinyin()
        str_lis = self.code_lis()
        new_p = p.get_pinyin(name).replace('-', '_')
        new_lis = list(new_p)
        for n in range(len(new_lis)):
            if new_lis[n] not in str_lis:
                new_lis[n] = 'c'
        new_p = ''.join(new_lis)
        return new_p

class douyin():
    msg_lis=[]
    flag_all_down = False
    base_path='./res/video/'
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'cache-control': 'max-age=0',
            'accept-language': 'zh-CN,zh;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
            'X-Real-IP': None,
            'X-Forwarded-For': None
        }
        while True:
            ip = ip_address('.'.join(map(str, (random.randint(0, 255) for _ in range(4)))))
            if ip.is_private:
                self.headers['X-Real-IP'], self.headers['X-Forwarded-For'] = str(ip), str(ip)
                break
        self.share_url = 'https://www.amemv.com/share/user/{}'
        self.user_url = 'https://www.amemv.com/aweme/v1/aweme/post/?user_id={}&max_cursor={}&count=21&aid=1128&_signature={}&dytk={}'

    def show_msg(self,msg):
        print(msg)
        return msg

    # 下载
    def _download(self, Vurlinfos, savepath=''):
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        name = Vurlinfos[0]
        download_url = Vurlinfos[1]
        print(download_url)
        with closing(requests.get(download_url, headers=self.headers, stream=True, verify=False)) as res:
            total_size = int(res.headers['content-length'])
            if res.status_code == 200:
                label = '文件大小:%0.2f MB' % (total_size / (1024 * 1024))
                with click.progressbar(length=total_size, label=label) as progressbar:
                    with open(os.path.join(savepath, name), "wb") as f:
                        print(savepath)
                        print(os.path.abspath(savepath))
                        print(os.path.join(savepath, name))
                        for chunk in res.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                progressbar.update(1024)
            else:
                print('链接错误')
            return res.status_code

    # 外部调用运行
    def run(self,user_id,watermark):
        # user_id = input('清输入userID:')
        msg=''
        name_list=[]
        if user_id == 'q' or user_id == 'Q':
            return None
        # watermark = input('要不要水印(0=要 or 1=不要):')
        if watermark == 'q' or watermark == 'Q':
            return None
        # if watermark == '1':#有水印
        #     watermark = True
        # elif watermark=='2':#无水印
        #     watermark = False
        video_names, video_urls, nickname = self._get_urls_by_userid(user_id)
        print(video_names)
        print(video_urls)
        print(nickname)
        if video_names is None:
            return None
        num_url = len(video_urls)
        msg='找到 %d 个视频' % num_url
        self.msg_lis.append(msg)
        print(msg)#52616983119
        for i in range(num_url):
            video_name = video_names[i]
            video_url = video_urls[i]
            if watermark==False:
                video_url = video_url.replace('playwm', 'play')
            # 视频不存在就下载
            print('res/video/'+os.path.join(nickname, video_name))
            if not os.path.exists('res/video/'+os.path.join(nickname, video_name)):
                msg = '正在下载第{}个视频...'.format(i + 1)
                self.show_msg(msg)
                self.msg_lis.append(msg)
                self._download([video_name, video_url], savepath=self.base_path+nickname)
                name_list.append(video_name)
            else:
                msg='视频{}已存在'.format(video_name)
                self.msg_lis.append(msg)
                self.show_msg(msg)
        msg='全部下完'
        self.show_msg(msg)
        self.flag_all_down=True
        return self.flag_all_down,nickname,name_list

    # def change_name(self,name):#转换中文为拼音
    #     p=Pinyin()
    #     new_p=p.get_pinyin(name).replace('-','_').replace('、','')
    #     return new_p

    # 根据抖音号获得账号所有视频下载地址
    def _get_urls_by_userid(self, user_id):
        uid = user_id
        try:
            process = Popen(['node', 'fuck-byted-acrawler.js', str(uid)], stdout=PIPE, stderr=PIPE)
        except:
            print('需要加载nodejs')
            exit(-1)
        signature = process.communicate()[0].decode().strip('\n')
        res = requests.get(self.share_url.format(uid), headers=self.headers)
        try:
            dytk = re.findall(r"dytk: '(.+)'", res.text)[0]
        except:
            print('[Error]: User Id error...')
            return None, None, None
        try:
            nickname = re.findall(r'"nickname"\>(.+?)\<', res.text)[0].replace(' ', '').replace('\\', '').replace('/','')
            ci=Change_str()
            nickname=ci.change_name(nickname)
            # nickname = self.change_name(nickname)
            print(nickname)
        except:
            nickname = str(uid)
        max_cursor = 0
        video_names = []
        video_urls = []
        while True:
            res = requests.get(self.user_url.format(uid, max_cursor, signature, dytk), headers=self.headers)
            res_json = json.loads(res.text)
            for aweme in res_json['aweme_list']:
                aweme_id = aweme['aweme_id']
                video_url = aweme['video']['play_addr']['url_list'][0]
                video_names.append('aweme_id' + '_' + aweme_id + '.mp4')
                video_urls.append(video_url)
            max_cursor = res_json['max_cursor']
            if not res_json['has_more']:
                break
        return video_names, video_urls, nickname


if __name__ == '__main__':
    dy = douyin()
    while True:
        flag_all_down,nickname,name_list= dy.run('58958068057',False)
        if flag_all_down is True:
            break
