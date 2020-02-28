#! /usr/bin/python3 -W all

import sys, argparse
from os import path
from mctools import fluka
from mctools.fluka.flair import Data
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

def main():
    """ Converts usbsuw output into a ROOT histogram """

    parser = argparse.ArgumentParser(description=main.__doc__,
                                     epilog="Homepage: https://github.com/kbat/mc-tools")
    parser.add_argument('usrbin', type=str, help='usrxxx binary output (produced by usbsuw)')
    parser.add_argument('root', type=str, nargs='?', help='output ROOT file name', default="")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose', help='Print some output')

    args = parser.parse_args()

    if not path.isfile(args.usrbin):
        print("usrbin2root: File %s does not exist." % args.usrbin, file=sys.stderr)
        return 1

    if args.root == "":
        rootFileName = "%s%s" % (args.usrbin,".root")
    else:
        rootFileName = args.root

    b = Data.Usrbin()
    b.readHeader(args.usrbin)

    ND = len(b.detector)

    if args.verbose:
        b.sayHeader()
        print("\n%d tallies found:" % ND)
        for i in range(ND):
            b.say(i)
            print("")

    fout = ROOT.TFile(rootFileName, "recreate")
    for i in range(ND):
        val = Data.unpackArray(b.readData(i))
        err = Data.unpackArray(b.readStat(i))
        det = b.detector[i]

        title = fluka.particle.get(det.score, "unknown")
        if det.type % 10 in (0, 3, 4, 5, 6):  # Fluka Manual, pages 250-251
            title = title +  ";x [cm];y [cm];z [cm]"

        h = ROOT.TH3F(det.name, title, det.nx, det.xlow, det.xhigh, det.ny, det.ylow, det.yhigh, det.nz, det.zlow, det.zhigh)

        for i in range(det.nx):
            for j in range(det.ny):
                for k in range(det.nz):
                    gbin = i + j * det.nx + k * det.nx * det.ny
                    h.SetBinContent(i+1, j+1, k+1, val[gbin])
                    h.SetBinError(i+1, j+1, k+1, err[gbin]*val[gbin])
        h.SetEntries(b.weight)
        h.Write()

    fout.Close()

if __name__=="__main__":
    sys.exit(main())
