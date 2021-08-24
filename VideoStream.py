import open3d as o3d
import numpy as np
import cv2
import matplotlib.pyplot as plt


class VideoCamera:
    def __init__(self, config, device, align_depth_to_color):
        """

        :param config: Hazırlanan config dosyasıdır. Open3d ile okunmalıdır.
        :param device: Birden fazla cihaz varsa hangisini çalıştırmak istediğimizi belirtiriz.
        :param align_depth_to_color: Renkli görüntü ile Derinlik görüntüsünün align edilmesidir.
        Bu class yapısı input parametrelerini aldıktan sonra cihazın sensörüne bağlanır.
        Sensör, derinlik ve renkkli görüntüleri hizalar ve geri dönüş sağlar.
        """
        self.align_depth_to_color = align_depth_to_color
        self.config = config
        self.device = device
        self.sensor = o3d.io.AzureKinectSensor(self.config)
        if not self.sensor.connect(self.device):
            raise RuntimeError('Failed to connect to sensor')

    def get_frame(self):
        while True:
            rgbd = self.sensor.capture_frame(self.align_depth_to_color)
            if rgbd is None:
                continue

            color_array = np.array(rgbd.color)
            color_array = cv2.cvtColor(color_array, cv2.COLOR_BGR2RGB)

            depth_array = np.array(rgbd.depth)

            return color_array, depth_array


if __name__ == '__main__':
    config = o3d.io.read_azure_kinect_sensor_config('config.json')
    device = 0
    align_depth_to_color = True
    cam = VideoCamera(config, device, align_depth_to_color)

    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2, sharex=ax1, sharey=ax1)
    plot_azure = True

    while True:
        frame, depth = cam.get_frame()
        if plot_azure:
            fig1 = ax1.imshow(depth)
            fig2 = ax2.imshow(frame)
            plot_azure = False
        else:
            fig1.set_data(depth)
            fig2.set_data(frame[:, :, ::-1])
            plt.pause(0.001)
