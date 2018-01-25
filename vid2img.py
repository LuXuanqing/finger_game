import imageio
from PIL import Image
import os

def ImageGenerator(fp, fps, target_size):
    '''a generator, convert video file to PIL Image
    '''
    reader = imageio.get_reader(fp)
    meta = reader.get_meta_data()
    sampling_rate = meta['fps'] / fps
    indices = filter(lambda i: 0<= i%sampling_rate < 1, range(meta['nframes']))
    for index in indices:
        im = reader.get_data(index)
        # convert to PIL Image
        im = Image.fromarray(im)
        # resize to target_size
        if target_size:
            im = im.resize(target_size)
        yield im

def saveImageFile(images, dir, fname_base, fname_ext):
    for index, image in enumerate(images):
        fname = '{}_{}.{}'.format(fname_base, index, fname_ext)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fp = os.path.join(dir, fname)
        image.save(fp)
        print('image saved. {}'.format(fp))


def main(src_dir, dst_dir, fps, target_size, fname_ext):
    for dirpath, dirnames, filenames in os.walk(src_dir):
        if filenames:
            for filename in filenames:
                fp = os.path.join(dirpath, filename)
                images = ImageGenerator(fp, fps, target_size)
                fname_base, _ = os.path.splitext(filename)
                dst_dirname = dirpath.replace(src_dir, dst_dir)
                saveImageFile(images, dst_dirname, fname_base, fname_ext)


if __name__ == '__main__':
    main(src_dir='videos', dst_dir='images', fps=8, target_size=(320,240), fname_ext='jpg')