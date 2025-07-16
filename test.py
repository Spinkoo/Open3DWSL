import open3d as o3d, numpy as np, open3d.core as o3c
print(o3c.cuda.is_available())

device = o3d.core.Device("cuda:0")
#device = o3d.core.Device("cpu:0")
pcd = o3d.t.geometry.PointCloud(device)
pcd.point["positions"] = o3c.Tensor(np_array = np.random.rand(10000,3), dtype=o3c.Dtype.Float32, device=device)
from time import time
start_time = time()
for i in range(1000):    
    pcd_ds = pcd.voxel_down_sample(
                voxel_size=0.05,
    )
end_time = time()
print(f"Time taken: {end_time - start_time} seconds")
