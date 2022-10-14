import jittor as jt
import jrender as jr
jt.flags.use_cuda = 1
import os
import numpy as np
import imageio
import argparse

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_dir, 'data')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--filename-input', type=str, 
        default=os.path.join(data_dir, 'head2/Head.OBJ'))
    parser.add_argument('-o', '--output-dir', type=str, 
        default=os.path.join(data_dir, 'results/output_render'))
    args = parser.parse_args()
    # other settings
    camera_distance = 1.8
    elevation = 20
    azimuth = 45

    # load from Wavefront .obj file
    mesh = jr.Mesh.from_obj(args.filename_input, load_texture=True, texture_res=15, texture_type='surface', dr_type='softras',normalization=True,with_SSS = False)

    # create renderer with SoftRas
    renderer = jr.Renderer(dr_type='softras',image_size=2048,light_intensity_ambient=0.5, light_color_ambient=[1,1,1],
                 light_intensity_directionals=1.4, light_color_directionals=[1.0,1.0,1.0],
                 light_directions=[-0.7,0.1,1],dist_func="barycentric",aggr_func_rgb='hard',camera_mode="look",eye=[-0.8,0.3,1.65],camera_direction=[0.5,-0.1,-1])
    '''
        # create renderer with SoftRas
    renderer = jr.Renderer(dr_type='softras',image_size=2048,light_intensity_ambient=0.4, light_color_ambient=[1,1,1],
                 light_intensity_directionals=0.7, light_color_directionals=[1.0,1.0,1.0],
                 light_directions=[0,0,1],dist_func="barycentric",aggr_func_rgb='hard',camera_mode="look",eye=[0,0,1],camera_direction=[0,0,-1])
    '''
    os.makedirs(args.output_dir, exist_ok=True)

    # draw object
    writer = imageio.get_writer(os.path.join(args.output_dir, 'noSSS2.jpg'))
    #renderer.transform.set_eyes_from_angles(camera_distance, elevation, azimuth)
    rgb = renderer.render_mesh(mesh, mode='rgb')
    image = rgb.numpy()[0].transpose((1, 2, 0))
    writer.append_data((255*image).astype(np.uint8))
    writer.close()

if __name__ == '__main__':
    main()
