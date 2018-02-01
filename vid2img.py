import imageio
from PIL import Image
import os
import random
import argparse


def ImageGenerator(fp, fps, target_size):
    '''a generator, convert video file to PIL Image
    '''
    reader = imageio.get_reader(fp)
    meta = reader.get_meta_data()
    sampling_rate = meta['fps'] / fps
    indices = filter(lambda i: 0 <= i % sampling_rate < 1,
                     range(meta['nframes']))
    for index in indices:
        im = reader.get_data(index)
        # convert to PIL Image
        im = Image.fromarray(im)
        # resize to target_size
        if target_size:
            im = im.resize(target_size)
        yield im


def saveImageFile(images, dir, fname_base, fname_ext, verbose):
    for index, image in enumerate(images):
        fname = '{}_{}.{}'.format(fname_base, index, fname_ext)
        # check if dir exists
        if not os.path.exists(dir):
            os.makedirs(dir)
        fp = os.path.join(dir, fname)
        image.save(fp)
        if verbose:
            print('image saved. {}'.format(fp))


def shuffleFiles(dir):
    for dirpath, dirnames, filenames in os.walk(dir):
        if filenames:
            # 重构文件名为 'category_i.fname_ext'
            category = dirpath.split(os.path.sep)[-1]
            _, fname_ext = os.path.splitext(filenames[0])
            # 乱序
            nfiles = len(filenames)
            random_indicex = list(range(1, nfiles + 1))
            random.shuffle(random_indicex)
            # 命名池
            name_pool = ('{}_{}{}'.format(category, i, fname_ext)
                         for i in random_indicex)
            # 遍历filenames和命名池
            for filename, filename_new in zip(filenames, name_pool):
                fp = os.path.join(dirpath, filename)
                fp_new = os.path.join(dirpath, filename_new)
                os.rename(fp, fp_new)


def main(src_dir, dst_dir, fps, target_size, fname_ext, shuffle, verbose):
    for dirpath, dirnames, filenames in os.walk(src_dir):
        if filenames:
            for filename in filenames:
                print('processing {}...'.format(filename))
                fp = os.path.join(dirpath, filename)
                images = ImageGenerator(fp, fps, target_size)
                fname_base, _ = os.path.splitext(filename)
                dst_dirname = dirpath.replace(src_dir, dst_dir)
                saveImageFile(images, dst_dirname, fname_base, fname_ext, verbose)
    if shuffle:
        shuffleFiles(dst_dir)
    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'convert videos to image files while keep the folder structure')
    parser.add_argument('src', help='input dir')
    parser.add_argument('dst', help='output dir')
    parser.add_argument('fps', help='sampling rate', type=int)
    parser.add_argument('--target_size', help='tuple(width, height)')
    parser.add_argument(
        '--shuffle',
        help='shuffle and rename the image files by dir',
        action='store_true')
    parser.add_argument(
        '--format',
        help='the format of image files, default to ".jpg"',
        default='jpg')
    parser.add_argument('--verbose', help='print more info', action='store_true')
    args = parser.parse_args()

    main(
        src_dir=args.src,
        dst_dir=args.dst,
        fps=args.fps,
        target_size=args.target_size,
        fname_ext=args.format,
        shuffle=args.shuffle,
        verbose = args.verbose)