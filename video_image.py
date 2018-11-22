"""
将视频文件截取一帧图做封面

"""
import cv2,os

def cut_pic(user_name,vio,n):
    cap = cv2.VideoCapture('res/video/'+user_name+"/"+vio)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps =cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #size=(960,544)
    i=0
    while(cap.isOpened()):
        i+=1
        print('ok')
        ret, frame = cap.read()
        if ret==True:
            path='res/image/'+user_name
            if not os.path.exists(path):
                os.makedirs(path)
            file_path=path+'/'+str(vio.split('.')[0])+str(i)+'.jpg'
            if not os.path.exists(file_path):
                cv2.imwrite(file_path,frame)
                print(path+str(vio.split('.')[0])+'.jpg')
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if i==n:
                    break
            else:
                print('视频{}已截图'.format(vio))
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


# cut_pic('yijun','aweme_id_6597331710369598733.mp4')
if __name__ == '__main__':
    cut_pic('yijun/','aweme_id_6568383422568336654.mp4',2)

