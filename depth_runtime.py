import pygame
import ctypes
import numpy as np
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
from hand_sensor import HandSensor
from chuni_io import ChuniIO

class DepthRuntime:
    def __init__(self, depth_min, depth_max, sensor_pos, sensor_dimen):
        pygame.init()

        self._clock = pygame.time.Clock()
        self._done = False
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth)
        self._width = self._kinect.depth_frame_desc.Width
        self._height = self._kinect.depth_frame_desc.Height
        self._frame_surface = pygame.Surface((self._width, self._height), 0, 24)
        
        self._screen = pygame.display.set_mode(
            (self._width, self._height),
            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
        )

        pygame.display.set_caption("chuninect-kv2")
        
        self.depth_min = depth_min
        self.depth_max = depth_max
        
        self.sensors = self.create_sensors(sensor_pos, sensor_dimen)
        
        ChuniIO.initialize()

    def create_sensors(self, initial_pos, dimen):
        sensors = []
        
        for i in range(6):
            sensor = HandSensor(
                rect=pygame.Rect(initial_pos[0], initial_pos[1]+dimen[1]*i, dimen[0], dimen[1]),
                depth_min=self.depth_min,
                depth_max=self.depth_max,
                width=self._width,
                height=self._height,
                id=i+1
            )
            sensors.append(sensor)
        
        return sensors

    def draw_depth_frame(self, frame, target_surface):
        if frame is None:
            return
        
        mask = (frame < self.depth_min) | (frame > self.depth_max)
        
        f8 = np.zeros_like(frame, dtype=np.uint8)
        
        valid_mask = ~mask
        if np.any(valid_mask):
            f8[valid_mask] = np.uint8(
                (frame[valid_mask] - self.depth_min) * 255 / (self.depth_max - self.depth_min)
            )
        
        frame8bit = np.dstack((f8, f8, f8))
        
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame8bit.ctypes.data, frame8bit.size)
        del address
        target_surface.unlock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True
            elif event.type == pygame.VIDEORESIZE:
                self._screen = pygame.display.set_mode(
                    event.dict['size'],
                    pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
                )
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._done = True

    def run(self):
        print("Keyboard Controls:")
        print("  ESC: Exit")
        
        while not self._done:
            self.handle_events()

            if self._kinect.has_new_depth_frame():
                frame = self._kinect.get_last_depth_frame()
                self.draw_depth_frame(frame, self._frame_surface)
                for sensor in self.sensors:
                    sensor.update(frame)
                ChuniIO.send(self.sensors[::-1])
                frame = None

            self._screen.blit(self._frame_surface, (0, 0))
            
            for sensor in self.sensors:
                sensor.draw(self._screen)
            
            font = pygame.font.SysFont(None, 30)
            status_text = "Detected Sensors: " + ", ".join([
                str(i+1) for i, sensor in enumerate(self.sensors) if sensor.hand_detected
            ])
            status_surf = font.render(status_text, True, (255, 255, 255))
            self._screen.blit(status_surf, (10, 10))
            
            pygame.display.flip()
            self._clock.tick(60)

        ChuniIO.close()
        self._kinect.close()
        pygame.quit()