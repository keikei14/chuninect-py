from depth_runtime import DepthRuntime

# In millimeters
depth_min = 550
depth_max = 950

# Sensor dimensions (width, height)
sensor_dimen = (100, 15)

# Middle of screen by default (in x,y)
sensor_pos = (512//2, 424//2)

if __name__ == "__main__":
    game = DepthRuntime(depth_min, depth_max, sensor_pos, sensor_dimen)
    game.run()