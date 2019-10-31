import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os, os.path
import argparse


def main():
    parser = argparse.ArgumentParser("imshow")
    parser.add_argument(
        "-i",
        "--interpolation",
        choices=["nearest", "bilinear", "bicubic"],
        default="nearest",
        help="style of interpolation. default: nearest")
    parser.add_argument(
        "-g",
        "--grid",
        action="store_true",
        default=False,
        help="display grid overlay. default: False.")
    parser.add_argument(
        "-b",
        "--colorbar",
        action="store_true",
        default=False,
        help="add a color bar. default: False.")
    parser.add_argument(
        "-m", "--cmap", help="color map. Default: matplotlib default")
    parser.add_argument(
        "array",
        metavar="array.txt",
        help="input file, loadable by np.loadtxt()")
    parser.add_argument(
        "image",
        metavar="image.png",
        nargs="?",
        help="output image. format is specified by extension (pdf|png|jpg). "
        "default: array.txt.png")
    args = parser.parse_args()

    A = np.loadtxt(args.array)
    plt.imshow(A, interpolation=args.interpolation, cmap=args.cmap)
    plt.grid(args.grid)
    if args.colorbar:
        plt.colorbar()
    if args.image is None:
        if args.array.endswith(".txt"):
            args.image = args.array[:-4] + ".png"
        else:
            args.image = args.array + ".png"
    plt.savefig(args.image)


if __name__ == "__main__":
    main()
