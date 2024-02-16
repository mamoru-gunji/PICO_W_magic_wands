from wifi import wifi
from MPU6050 import MPU6050
import global_value as g
import time
from multi_thread import ThreadManager
from time import sleep
from memory_usage import free
from LSTM_np import LSTM
from ulab import numpy as np

class DataManager:
    def __init__(self, train=False, ssid=None,password=None,port=0):
        self.train = train
        self.init = True
        self.limit = 1
        self.num = 0
        self.input_data = []
        self.sequence = 30
        self.buff = 1.5
        self.ssid = ssid
        self.password = password
        self.port = port
        g.thread = ThreadManager()
        g.MPU = MPU6050(once = False)
        g.LSTM = LSTM()
        g.sleep_0 = self.sleep_time = 0.02
        g.process0 = self.data_input
        if self.train:
            try:
                g.wifi
            except Exception:
                g.wifi = wifi()
                if ssid:
                    g.wifi.ssid = self.ssid
                if password:
                    g.wifi.password = self.password
                if port:
                    g.wifi.port = self.port
            if not g.wifi.isconnected():
                    g.wifi.server_init()
            if not g.wifi.foundclient():
                g.wifi.find_client()
 
            g.process1 = self.data_serve
        else:
            g.process1 = self.data_predict
        pass
    
    def data_input(self):
        next_data = self.data_gen()
        with g.lock():
            self.input_data += next_data
        print('process finish: core0')

    def data_gen(self):
        g.mpu_data = []
        if self.init:
            g.t =  [time.ticks_ms()]
            self.init = False
        print('data generating...')
        for i in range(self.sequence):
            g.t +=  [(time.ticks_ms() - g.t[0])/1000]
            g.mpu_datum = g.MPU.data()
            g.mpu_data += [[g.t[-1]] + g.mpu_datum]
            time.sleep(self.sleep_time)
        g.t = [g.t[0]]
        return [g.mpu_data]



    def data_serve(self):
        if not len(self.input_data):
            sleep(self.buff)
        try:
            while len(self.input_data):
                send_data = '[' + ', '.join(map(str, self.input_data[0])) + ']'
                
                with g.lock():
                    self.input_data = self.input_data[1:]
                g.wifi.send(value=send_data)
        except Exception as e:
            print(e)
            pass
        finally:
            free()
            print('process finish: core1')
            
    def data_predict(self):
        if not len(self.input_data):
            sleep(1.5)
        try:
            while len(self.input_data):
                print(self.input_data[0])
                g.LSTM.input_data = np.array(self.input_data[0])
                with g.lock():
                    self.input_data = self.input_data[1:]           
                try:
                    g.y_hat = np.concatenate((g.y_hat, g.LSTM.main()))
                except Exception as e:
                    g.y_hat = g.LSTM.main()
                    print(g.y_hat)
        except Exception as e:
            print(e)
            pass
        finally:
            free()
            print('process finish: core1')
            
    def run(self,once=False,num=0):
        g.MPU.on()
        self.num += 1
        g.thread.multi_thread()
        if once or self.limit <= max(self.num,num):
            g.MPU.off()
            self.init = True
            self.num = 0
            g.mpu_data = g.mpu_data[0]
        
    def main(self):  
        try:
            g.MPU.on()
            for i in range(5):
                self.run(once=not self.train)

                while g.thread.state:
                    time.sleep_ms(1)
                print(g.y_hat)
                y_hat_mean = np.mean(g.y_hat, axis=0)
                y_hat_std = np.std(g.y_hat, axis=0)
                pre_label_fst = np.argmax(y_hat_mean)
                pre_label_sec = y_hat_mean.tolist().index(sorted(y_hat_mean)[-2])
                
                print(y_hat_mean[pre_label_fst] - y_hat_std[pre_label_fst] - y_hat_mean[pre_label_sec] - y_hat_std[pre_label_sec])
                if y_hat_mean[pre_label_fst] - y_hat_std[pre_label_fst] > y_hat_mean[pre_label_sec] + y_hat_std[pre_label_sec]:
                    label_hat = pre_label_fst
                else:
                    label_hat = None
                print(label_hat)
                g.y_hat = []
        except Exception as e:
            print(e)
        finally:
            pass
            
