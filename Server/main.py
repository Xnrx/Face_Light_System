import queue
import threading

import cv2

from CameraSelector import CameraSelector
from Database import Database
from FaceRecognitionSystem import FaceRecognitionSystem
from ThreadManager import ThreadManager
from UserManager import UserManager

frame_lock = threading.Lock()


def face_handle_thread(recognizerSys, frame, q):
    """
    人脸识别线程
    :param recognizerSys: 人脸识别系统类
    :param frame: 照片
    :param q:  传参队列
    """
    with frame_lock:
        user = recognizerSys.recognize_user(frame)
        q.put(user)


def serial_communication_thread(recognizerSys, q):
    """
    串口通信线程
    :param recognizerSys: 人脸识别系统类
    :param q: 传参队列
    """
    user = q.get()
    recognizerSys.receive_and_send_signal(user)
    print(user.username, user.RGB)


def main():
    global thread
    modelD_path = '../model/face_detection_yunet_2022mar.onnx'
    modelR_path = '../model/face_recognition_sface_2021dec.onnx'
    input_shape = (300, 300)
    port = 'COM7'
    rate = 115200
    users_path = '../user/'
    users_list = []
    camera_index = 0
    url = 'http://172.20.10.2/cam-hi.jpg'  # 改成自己的ip地址+/cam-hi.jpg

    # 用户管理初始化
    um = UserManager(users_path, users_list)
    um.load_images_and_features(modelD_path, modelR_path, input_shape)

    # 视频流初始化
    camera_select = CameraSelector('local', camera_index, url)
    camera = camera_select.camera

    # 人脸识别系统初始化
    recognizerSystem = FaceRecognitionSystem(modelD_path, modelR_path, input_shape, port, rate, um.list)

    # 数据库初始化
    db = Database(server='LAPTOP-NO19G1TG', user='sa', password='zhong5567', database='Python')
    db.connect()
    result = db.query('SELECT * FROM UserSettings')
    um.load_user_infos(result)

    while True:
        # 创建队列
        q = queue.Queue()

        # 获取图像模块
        frame = camera.get_frame()  # 获取摄像头的当前帧
        if frame is not None:
            # 在这里处理摄像头的当前帧
            with frame_lock:
                cv2.imshow('default', frame)
        else:
            break

        # 线程管理类初始化
        thread = ThreadManager()

        # 添加人脸识别线程
        thread.add_thread(face_handle_thread, args=(recognizerSystem, frame, q))

        # 添加串口通信线程
        thread.add_thread(serial_communication_thread, args=(recognizerSystem, q))

        # 启动所有线程
        thread.start_all_threads()

        # 用户管理模块
        k = cv2.waitKey(1)
        if k == 32:
            # 添加新用户
            um.add_new_user(frame, modelD_path, modelR_path, input_shape)
            recognizerSystem.set_user_lists(um.list)
            um.load_user_infos(result)
        # 退出
        if k == 27:
            break

    thread.join_all_threads()
    recognizerSystem.serial.close()
    recognizerSystem.serial.open()
    recognizerSystem.serial.close()
    cv2.destroyAllWindows()
    return


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()
