import numpy as np
import open3d as o3d
import os

default_path = '/home/alekappe/catkin_ws/src/my_package/src/'
pointcloud_filename = f'{default_path}pointcloud.txt'

def load_point_cloud(pointcloud_filename):
    if os.path.exists(pointcloud_filename):
        try:
            points = np.loadtxt(pointcloud_filename, delimiter=',', unpack=False)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points[:, :3])
            if points.shape[1] >= 3:
                # colors = np.tile([0, 0, 1], (points.shape[0], 1))
                # pcd.colors = o3d.utility.Vector3dVector(colors)
                return pcd
            if points.shape[1] >= 3:
                # Split points into two groups and assign different colors
                colors = np.zeros((points.shape[0], 3))
                midpoint = points.shape[0] // 2
                colors[:midpoint] = [1, 0, 0]  # First half: Red
                colors[midpoint:] = [0, 0, 1]  # Second half: Blue
                pcd.colors = o3d.utility.Vector3dVector(colors)
                return pcd
            else:
                print(f"Unexpected number of columns in the point cloud file: {points.shape[1]}")
        except Exception as e:
            print(f"Error loading point cloud: {e}")
    return o3d.geometry.PointCloud()

def update_bounding_box_text(bbox):
    min_bound = bbox.get_min_bound()
    max_bound = bbox.get_max_bound()
    dimensions = max_bound - min_bound
    dimension_text = f"Dimensions: {dimensions[0]:.2f} x {dimensions[1]:.2f} x {dimensions[2]:.2f} cm"
    print(dimension_text)
    return dimension_text

# Initial load
pcd = load_point_cloud(pointcloud_filename)

# Visualization
vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()

# Add the point cloud
vis.add_geometry(pcd)

# Add coordinate axes
coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
vis.add_geometry(coordinate_frame)

def update(vis):
    new_pcd = load_point_cloud(pointcloud_filename)
    pcd.points = new_pcd.points
    vis.update_geometry(pcd)
    
    print('-------------------------')
    print(f'Updating {pcd}')

    # Update bounding box
    bbox = pcd.get_axis_aligned_bounding_box()
    bbox.color = (1, 0, 0)
    vis.clear_geometries()
    vis.add_geometry(pcd)
    vis.add_geometry(coordinate_frame)
    vis.add_geometry(bbox)

    # Print bounding box dimensions
    update_bounding_box_text(bbox)

    vis.poll_events()
    vis.update_renderer()
    return False

# Add update callback
vis.register_key_callback(ord(" "), lambda vis: update(vis))  # Press space to update
update(vis)

# Run the visualizer
vis.run()

# Close the visualizer
vis.destroy_window()