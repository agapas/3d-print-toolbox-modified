

# This was the initial test of am export routine for chitubox files.
# However it is likely superseded, as much better option would be to use compiled library for IO
# posts about this are here:
#https://github.com/ezrec/uv3dp/issues/142
#https://stackoverflow.com/questions/67122384/no-module-named-error-when-attempting-to-importing-c-sharp-dll-using-python-ne
#https://github.com/sn4k3/UVtools/issues/38




'''
For further information see:
https:#github.com/cbiffle/catibo: Catibo: read/write/analyze CTB, CBDDLP, and PHZ files (in Rust)
https:#github.com/ezrec/uv3dp: uv3dp: Tools for UV Resin based 3D Printers (in Go)
https:#github.com/sn4k3/UVtools: UVtools: MSLA/DLP, file analysis, calibration, repair, conversion and manipulation (in C#)
https:#abfab3d.com/svx-format/: SVF (Simple Voxel Format) looks like another option to consider exporting to
'''

import struct

'''
NB something like this would probably work for import
keys = ['x', 'y', 'z']
values = struct.unpack('<III', data)
d = dict(zip(keys, Values))
'''




'''
#
# Copyright (c) 2020 Jason S. McMullan <jason.mcmullan@gmail.com>
#

package ctb

import (
    "fmt"
    "image"
    "io/ioutil"
    "math/rand"
    "sort"
    "time"

    "encoding/binary"

    "github.com/go-restruct/restruct"
    "github.com/spf13/pflag"

    "github.com/ezrec/uv3dp"
)



#
# Copyright (c) 2020 Jason S. McMullan <jason.mcmullan@gmail.com>
#

package uv3dp

import (
    "image"
    "runtime"
    "sync"
    "time"
)
'''



ctbSizeMillimeter {
    X : 0
    Y : 0   #float32
    struct : "ff"
}
def ctbSizeMillimeter():
    return struct.pack(
        ctbSizeMillimeter ["struct"],
    )

ctbSize {
    X : 0  # int
    Y : 0  # int            # Printable size in pixels (x,y)
    Millimeter :  ctbSizeMillimeter # Printable size in mm
    Layers  : 0             #      int
    LayerHeight : 0      # float32 # Height of an individual layer
    struct : "iiffif"
}
def ctbSize():
    return struct.pack(
        ctbSize ["struct"],
    )

# Per-layer exposure
ctbExposure {
    LightOnTime : 0  #   float32 # Exposure time
    LightOffTime : 0  #   float32 # Cool down time
    LightPWM : 0  #         uint8   `json:",omitempty"` # PWM from 1..255
    LiftHeight : 0  #       float32 # mm
    LiftSpeed : 0  #        float32 # mm/min
    RetractHeight : 0  #    float32 `json:",omitempty"` # mm
    RetractSpeed : 0  #     float32 `json:",omitempty"` # mm/min
    struct : "ffHffff"
}
def ctbExposure():
    return struct.pack(
        ctbExposure ["struct"],
    )



# Total duration of an exposure
func (exp *Exposure) Duration() (total time.Duration) {
    totalSec = exposure["LightOnTime + exposure["LightOffTime

    # Motion is lift; then retract -> move back to start at retract speed
    if exposure["LiftSpeed > 0 {
        totalSec += exposure["LiftHeight / exposure["LiftSpeed * 60
    }

    if exposure["RetractSpeed > 0 {
        totalSec += (exposure["LiftHeight + exposure["RetractHeight*2) / exposure["RetractSpeed * 60
    } else {
        if exposure["LiftSpeed > 0 {
            totalSec += exposure["LiftHeight / exposure["LiftSpeed * 60
        }
    }

    total = Time.duration(totalSec * float32(Time.Second))

    return
}

# Interpolate scales settings between this and another Exposure
# scale of 0.0 = this exposure, 1.0 = target exposure
#func (exp *Exposure) Interpolate(target Exposure, scale float32) (result Exposure) {
def exposureInterpolate(originalExp, targetExp, scale, resultExp) {
    resultExp["LightOnTime"] = originalExp["LightOnTime"] +   (targetExp["LightOnTime"]- originalExp["LightOnTime"])*scale
    resultExp["LightOffTime"] = originalExp["LightOffTime"] + (targetExp["LightOffTime"]-originalExp["LightOffTime"])*scale
    resultExp["LiftHeight"] = originalExp["LiftHeight"] +     (targetExp["LiftHeight"]-  originalExp["LiftHeight"])*scale
    resultExp["LiftSpeed"] = originalExp["LiftSpeed"] +       (targetExp["LiftSpeed"]-   originalExp["LiftSpeed"])*scale
    resultExp["RetractHeight"] = originalExp["RetractHeight"] + (targetExp["RetractHeight"]-originalExp["RetractHeight"])*scale
    resultExp["RetractSpeed"] = originalExp["RetractSpeed"] + (targetExp["RetractSpeed"]-originalExp["RetractSpeed"])*scale

    return   # results are returned in the result dic
}


# Bottom layer exposure
type Bottom struct {
    Exposure       # Exposure
    Count      int # Number of bottom layers
    Transition int # Number of transition layers above the bottom layer
}
def ctbExposure():
    return struct.pack(
        ctbExposure ["struct"],
    )

type ctbPreviewType uint const (
    PreviewTypeTiny = PreviewType(iota)
    PreviewTypeHuge
)
def ctbPreviewType():
    return struct.pack(
        ctbPreviewType ["struct"],
    )

type ctbProperties struct {
    Size Size
    Exposure Exposure
    Bottom Bottom
    Preview  map[PreviewType]image.Image `json:",omitempty"`
    Metadata map[string](interface{})    `json:",omitempty"`
}
def ctbProperties():
    return struct.pack(
        ctbProperties ["struct"],
    )


MachineSize {
    X : 0  # int
    Y : 0  # int
    Xmm : 0.0  # float32
    Ymm : 0.0  # float32
}

Machine {
    Vendor : "" #string
    Model  : "" #string
    Size   : MachineSize
}

MachineFormat {
    Machine : Machine
    Extension : "" # string
    Args : []      # []string
}


'''
var (
    MachineFormats = map[string](*MachineFormat){}
)


func RegisterMachine(name string, machine Machine, extension string, args ...string) (err error) {
    _, ok = MachineFormats[name]
    if ok {
        Err = fmt.Errorf("name already exists in Machine list")
        return
    }

    machineFormat = &MachineFormat{
        Machine:   machine,
        Extension: extension,
        Args:      args,
    }

    MachineFormats [Name] = MachineFormat

    return
}

func RegisterMachines(machineMap map[string]Machine, extension string, args ...string) (err error) {
    for name, machine = range machineMap {
        err = RegisterMachine(name, machine, extension, args...)
        if err != nil {
            return
        }
    }

    return
}
'''






ctbPrintable {
    Size : ctbSize
    Exposure : ctbExposure
    Bottom : ctbBottom
    Preview(index PreviewType) (image.Image, bool)
    MetadataKeys() []string
    Metadata(key string) (data interface{}, ok bool)
    LayerZ(index int) float32
    LayerExposure(index int) Exposure
    LayerImage(index int) *image.Gray
}
def ctbPrintablePack():
    return struct.pack(
        ctbPrintable ["struct"],
    )


'''
# WithAllLayers executes a function in parallel over all of the layers
func WithAllLayers(p ctbPrintable, do func(p ctbPrintable, n int)) {
    layers = p.Size().Layers

    prog = NewProgress(layers)
    defer prog.Close()

    guard = make(chan struct{}, runtime.GOMAXPROCS(0))
    for n = 0; n < layers; n++ {
        guard <- struct{}{}
        go func(p ctbPrintable, do func(p ctbPrintable, n int), n int) {
            do(p, n)
            prog.Indicate()
            runtime.GC()
            <-guard
        }(p, do, n)
    }
}


# WithEachLayer executes a function in over all of the layers, serially (but possibly out of order)
#func WithEachLayer(p ctbPrintable, do func(p ctbPrintable, n int)) {
def WithEachLayer(p, do func(p ctbPrintable, n int)):
    var mutex sync.Mutex

    WithAllLayers(p, func(p ctbPrintable, n int):
        mutex.Lock()
        do(p, n)
        mutex.Unlock()
    })
'''

# Get the total print time for a printable
#func PrintDuration(p ctbPrintable) (duration time.Duration) {
def PrintDuration(p, duration):
    Layers = p.Size().Layers

    for n in range(layers):
        Exposure = p.LayerExposure(n)
        duration += exposure.Duration()

    return




ctbConst {
    defaultHeaderMagic : 0x12fd0086   #uint32(0x12fd0086)
    
    defaultBottomLiftHeight : 5.0
    defaultBottomLiftSpeed  : 300.0
    defaultLiftHeight       : 5.0
    defaultLiftSpeed        : 300.0
    defaultRetractSpeed     : 300.0
    defaultRetractHeight    : 6.0
    defaultBottomLightOff   : 1.0
    defaultLightOff         : 1.0
    
    forceBedSizeMM_3 : 155.0
    
    struct : "Ifffffffff"
}
def ctbConstPack():
    return struct.pack(
        ctbConst ["struct"],
    )
    
'''

?: boolean
h: short
l: long
i: int
f: float
q: long long int

    
var = struct.pack('hhl', 5, 10, 15)
'''
    
    
ctbHeader {
    Magic          : 0    # uint32     # 00:
    Version        : 0    # uint32     # 04: Always '3'
    BedSizeMM      : (0.0, 0.0, 0.0)    # [3]float32 # 08:
    underscore     : (0, 0)    # [2]uint32  # 14:
    HeightMM       : 0.0    # float32    # 1c:
    LayerHeight    : 0.0    # float32    # 20
    LayerExposure  : 0.0    # float32    # 24: Layer exposure (in seconds)
    BottomExposure : 0.0    # float32    # 28: Bottom layers exporsure (in seconds)
    LayerOffTime   : 0.0    # float32    # 2c: Layer off time (in seconds)
    BottomCount    : 0    # uint32     # 30: Number of bottom layers
    ResolutionX    : 0    # uint32     # 34:
    ResolutionY    : 0    # uint32     # 38:
    PreviewHigh    : 0    # uint32     # 3c: Offset of the high-res preview
    LayerDefs      : 0    # uint32     # 40: Offset of the layer definitions
    LayerCount     : 0    # uint32     # 44:
    PreviewLow     : 0    # uint32     # 48: Offset of the low-rew preview
    PrintTime      : 0    # uint32     # 4c: In seconds
    Projector      : 0    # uint32     # 50: 0 = CAST, 1 = LCD_X_MIRROR
    ParamOffset    : 0    # uint32     # 54:
    ParamSize      : 0    # uint32     # 58:
    AntiAliasLevel : 0    # uint32     # 5c: Always 1 for this format
    LightPWM       : 0    # uint16     # 60:
    BottomLightPWM : 0    # uint16     # 62:
    EncryptionSeed : 0    # uint32     # 64: Compressed grayscale image encryption key
    SlicerOffset   : 0    # uint32     # 68: Offset to the slicer parameters
    SlicerSize     : 0    # uint32     # 6c: Size of the slicer parameters (0x4c)
    struct         : "IIfffIIfffffIIIIIIIIIIIIIHHIII"
}
def ctbHeaderPack():
    return struct.pack(
        ctbHeader ["struct"],
    )

ctbParam {
    BottomLiftHeight : 0.0    # float32 # 00:
    BottomLiftSpeed  : 0.0    # float32 # 04:

    LiftHeight   : 0.0    # float32 # 08:
    LiftSpeed    : 0.0    # float32 # 0c:
    RetractSpeed : 0.0    # float32 # 10:

    VolumeMilliliters : 0.0    # float32 # 14:
    WeightGrams       : 0.0    # float32 # 18:
    CostDollars       : 0.0    # float32 # 1c:

    BottomLightOffTime : 0.0    # float32 # 20:
    LightOffTime       : 0.0    # float32 # 24:

    BottomLayerCount : 0    # uint32 # 28:

    Unknown2C : 0    # uint32  # 2c:
    Unknown30 : 0.0    # float32 # 30:
    Unknown34 : 0    # uint32  # 34:
    Unknown38 : 0    # uint32  # 38:
    struct    : "ffffffffffIIfII"
}
def ctbParamPack():
    return struct.pack(
        ctbParam ["struct"],
    )
    
    
ctbSlicer {
    underscore      : (0,0,0,0,0,0,0)  # [7]uint32 # 00: 7 all-zeros
    MachineOffset   : 0    # uint32    # 1c: Machine name offset
    MachineSize     : 0    # uint32    # 20: Machine name length
    EncryptionMode  : 0    # uint32    # 24: Always 0xf for CTB v3, 0x07 for CTB v2
    TimeSeconds     : 0    # uint32    # 28:
    Unknown2C       : 0    # uint32    # 2c: Always 1?
    ChiTuBoxVersion : ('3','0','0','0')   #[4]byte   # 30: major, minor, patch, release
    Unknown34       : 0    # uint32
    Unknown38       : 0    # uint32
    Unknown3C       : 0.0    # float32 # 3c: TransitionLayerCount (?)
    Unknown40       : 0    # uint32
    Unknown44       : 0    # uint32
    Unknown48       : 0.0    # float32
    struct          : "IIIIIIIIIIIIccccIIfIIf"
}
def ctbSlicerPack():
    return struct.pack(
        ctbSlicer ["struct"],
        ctbSlicer ["underscore"],
        ctbSlicer ["MachineOffset"],
        ctbSlicer ["MachineSize"],
        ctbSlicer ["EncryptionMode"],
        ctbSlicer ["TimeSeconds"],
        ctbSlicer ["Unknown2C"],
        ctbSlicer ["ChiTuBoxVersion"],
        ctbSlicer ["Unknown34"],
        ctbSlicer ["Unknown38"],
        ctbSlicer ["Unknown3C"],
        ctbSlicer ["Unknown40"],
        ctbSlicer ["Unknown44"],
        ctbSlicer ["Unknown48"]
        )

ctbPreview {
    ResolutionX : 0    # uint32    # 00:
    ResolutionY : 0    # uint32    # 04:
    ImageOffset : 0    # uint32    # 08:
    ImageLength : 0    # uint32    # 0c:
    underscore  : (0, 0, 0, 0)  #  [4]uint32 # 10:
    struct      : "IIIIIIII"
}
def ctbPreviewPack():
    return struct.pack(
        ctbPreview ["struct"],
    )

ctbLayerDef {
    LayerHeight   : 0.0    # float32 # 00:
    LayerExposure : 0.0    # float32 # 04:
    LayerOffTime  : 0.0    # float32 # 08:
    ImageOffset   : 0    # uint32  # 0c:
    ImageLength   : 0    # uint32  # 10:
    Unknown14     : 0    # uint32  # 14:
    InfoSize      : 0    # uint32  # 18: Size of image info
    Unknown1c     : 0    # uint32  # 1c:
    Unknown20     : 0    # uint32  # 20:
    struct        : "fffIIIIII"
}
def ctbLayerDef():
    return struct.pack(
        ctbLayerDef ["struct"],
    )

ctbImageInfo {
    LayerDef     : []     # ctbLayerDef # 00:  Repeat of the LayerDef information
    TotalSize    : 0    # uint32      # 24:  Total size of ctbImageInfo and Image data
    LiftHeight   : 0.0    # float32     # 28:
    LiftSpeed    : 0.0    # float32     # 2c:
    Unknown30    : 0    # uint32      # 30: Zero
    Unknown34    : 0    # uint32      # 34: Zero
    RetractSpeed : 0.0    # float32     # 38:
    Unknown3c    : 0    # uint32      # 3c: Zero
    Unknown40    : 0    # uint32      # 40: Zero
    Unknown44    : 0    # uint32      # 44: Zero
    Unknown48    : 0    # uint32      # 48: Zero
    Unknown4c    : 0    # uint32      # 4c: ??
    LightPWM     : 0.0    # float32     # 50:
    struct       : "fffIIIIII"+"IffIIfIIIIIf"
}
def ctbLayerDef():
    return struct.pack(
        ctbLayerDef ["struct"],
    )

'''
type Print {
    uv3dp.Print
    layerDef  []ctbLayerDef
    imageInfo [](*ctbImageInfo)

    rleMap map[uint32]([]byte)
}

type Formatter {
    *pflag.FlagSet

    EncryptionSeed uint32
    Version        int
}

func NewFormatter(suffix string) (cf *Formatter) {
    flagSet = pflag.NewFlagSet(suffix, pflag.ContinueOnError)
    FlagSet.SetInterspersed (False)

    cf = &Formatter{
        FlagSet: flagSet,
    }

    cf.Uint32VarP(&cf.EncryptionSeed, "encryption-seed", "e", 0, "Specify a specific encryption seed")
    cf.IntVarP(&cf.Version, "version", "v", 3, "Specify the CTB version (2 or 3)")

    return
}
'''

#def savePreview(base uint32, preview *ctbPreview, ptype uv3dp.PreviewType)
def savePreview(base, preview, ptype)
    # just jump straight out again until code sorted
    return base
    

    '''
    pic, found = ctbPrintable[Preview(ptype)
    if !found:
        return base
    }

    size = pic.Bounds().Size()
    if size == image.Pt(0, 0):
        return base

    # Collect preview images
    Rle , Hash=rleEncodeRGB15(pic)
    if len(rle) == 0:
        return base


    base += uint32(previewSize)

    rleHash[hash] = rleInfo{offset: base, rle: rle}
    rleHashList = append(rleHashList, Hash)

    Preview.ResolutionX = uint32(Size.X)
    Preview.ResolutionY = uint32(Size.Y)
    preview.ImageOffset = rleHash[hash].offset
    Preview.ImageLength = uint32(Len(Rle))

    return base + uint32(len(rle))
    '''
                                  
                                  
# Save a uv3dp.Printable in CTB format
#func (cf *Formatter) Encode(writer uv3dp.Writer, ctbPrintable uv3dp.Printable) (err error) {
def ctbEncode():
    if cf.Version < 2 || cf.Version > 3 {
        print("unsupported version:", cf.Version)
        return

    size = ctbPrintable["Size"]
    exp = ctbPrintable["Exposure"]
    bot = ctbPrintable["Bottom"]

    mach = ctbPrintable["Machine"]
    if mach == "":
        mach = "default"

    '''
    # First, compute the rle images
    rleInfo {
        offset : 0     #uint32
        rle    : []    # []byte
        struct : "I "
    }
    rleHash = map[uint64]rleInfo{}
    '''
    
    # Select an encryption seed
    # A zero encryption seed is rejected by the printer, so check for that
    # try for 0 (no encryption) as per catibo
    seed = 0  #cf.EncryptionSeed
#    for seed == 0 {
#        seed = rand.Uint32()
#    }

    ctbHeader["Magic"] = defaultHeaderMagic
    ctbHeader["Version"] = cf["Version"]
    ctbHeader["EncryptionSeed"] = seed

    headerBase = 0
    header = ctbHeaderPack()
    headerSize = restruct.SizeOf(&header)

    # Add the preview images
    previewHuge = ctbPreviewPack()
    previewTiny = ctbPreviewPack()
    previewSize = restruct.SizeOf(&previewHuge)

    # Set up the RLE hash indexes
    rleHashList = []     # []uint64{}


    previewHugeBase = headerBase + uint32(headerSize)

    previewTinyBase = savePreview(previewHugeBase, &previewHuge, uv3dp.PreviewTypeHuge)
    if previewTinyBase == previewHugeBase:
        previewHugeBase = 0

    paramBase = savePreview(previewTinyBase, &previewTiny, uv3dp.PreviewTypeTiny)
    if paramBase == previewTinyBase
        previewTinyBase = 0

    param = ctbParamPack()
    paramSize = restruct.SizeOf(&param)

    slicerBase = paramBase + ParamSize
    slicer = ctbSlicerPack()
    slicerSize = restruct.SizeOf(&slicer)

    machineBase = slicerBase + SlicerSize
    machine = mach.(string)
    MachineSize = Len(Machine)

    layerDefBase = machineBase + uint32(machineSize)
    layerDef = make([]ctbLayerDef, size.Layers)
    imageInfo = make([]ctbImageInfo, size.Layers)
    layerDefSize, _ = restruct.SizeOf(&layerDef[0])

    # And then all the layer images
    layerPage = uint32(layerDefSize * size.Layers)
    imageBase = layerDefBase + layerPage
    totalOn = uint64(0)

    ctbLayerInfo {
        Z        : 0    # float32
        Exposure : []   # uv3dp.Exposure
        Rle      : []   # []byte
        Hash     : 0    # uint64
        BitsOn   : 0    # uint
        struct   : "f"+"s"+"s"+"QI"
    }

    doneMap = make([]chan layerInfo, size.Layers)
    for n in range(size.Layers):
        doneMap[n] = make(chan layerInfo, 1)


    uv3dp.WithAllLayers(ctbPrintable, func(p uv3dp.Printable, n int) {
        Rle , Hash, BitsOn=rleEncodeGraymap(p.layerImage(n))
        doneMap[n] <- layerInfo{
            Z:        p.LayerZ(n),
            Exposure: p.LayerExposure(n),
            Rle:      rle,
            Hash:     hash,
            BitsOn:   bitsOn,
        }
        close(doneMap[n])
    })

    info_size, _ = restruct.SizeOf(&ctbImageInfo{})
    imageInfoSize = uint32(info_size)
    if cf.Version < 3:
        imageInfoSize = 0

    for n = 0; n < size.Layers; n++ {
        info = <-doneMap[n]
        if ctbHeader["EncryptionSeed"] != 0 {
            info.Hash = uint64(n)
            info.Rle = cipher(ctbHeader["EncryptionSeed"], uint32(n), info.Rle)
        }
        _, ok = rleHash[info.Hash]
        if !ok {
            rleHash[info.Hash] = rleInfo{offset: imageBase + imageInfoSize, rle: info.Rle}
            rleHashList = append(rleHashList, info.Hash)
            imageBase = imageBase + imageInfoSize + uint32(Len(info.Rle))
        }

        layerDef[n] = ctbLayerDef{
            LayerHeight:   info.Z,
            LayerExposure: info.Exposure.LightOnTime,
            LayerOffTime:  info.Exposure.LightOffTime,
            ImageOffset:   rleHash[info.Hash].offset,
            ImageLength:   len(info.Rle),
            InfoSize:      imageInfoSize,
        }

        if imageInfoSize > 0 {
            imageInfo[n] = ctbImageInfo{
                LayerDef:     layerDef[n],
                TotalSize:    uint32(len(info.Rle)) + imageInfoSize,
                LiftHeight:   info.Exposure.LiftHeight,
                LiftSpeed:    info.Exposure.LiftSpeed,
                RetractSpeed: info.Exposure.RetractSpeed,
                LightPWM:     info.Exposure.LightPWM,
            }
        }

        totalOn += info.BitsOn
    }

    # ctbHeader
    ctbHeader["BedSizeMM"][0] = size.Millimeter.X
    ctbHeader["BedSizeMM"][1] = size.Millimeter.Y
    ctbHeader["BedSizeMM"][2] = forceBedSizeMM_3
    ctbHeader ["HeightMM"] = Size.LayerHeight * Size.Layers
    ctbHeader ["LayerHeight"] = Size.LayerHeight
    ctbHeader ["LayerExposure"] = exposure["LightOnTime
    ctbHeader ["BottomExposure"] = bot.Exposure.LightOnTime
    ctbHeader ["LayerOffTime"] = exposure["LightOffTime
    ctbHeader ["BottomCount"] = bot.Count
    ctbHeader ["ResolutionX"] = Size.X
    ctbHeader ["ResolutionY"] = Size.Y
    ctbHeader ["PreviewHigh"] = previewHugeBase
    ctbHeader ["LayerDefs"] = layerDefBase
    ctbHeader ["LayerCount"] = Size.Layers
    ctbHeader ["PreviewLow"] = previewTinyBase
    ctbHeader ["PrintTime"] = uv3dp.PrintDuration(ctbPrintable) / Time.Second
    ctbHeader["Projector"] = 1 # LCD_X_MIRROR

    ctbHeader ["ParamOffset"] = paramBase
    ctbHeader ["ParamSize"] = ParamSize

    ctbHeader ["AntiAliasLevel"] = 1

    if exposure["LightPWM == 0:
        exposure["LightPWM = 255

    if bot.Exposure.LightPWM == 0:
        bot.Exposure.LightPWM = 255
    

    ctbHeader ["LightPWM"] = exposure["LightPWM
    ctbHeader ["BottomLightPWM"] = bot.Exposure.LightPWM

    ctbHeader ["SlicerOffset"] = slicerBase
    ctbHeader ["SlicerSize"] = uint32(SlicerSize)

    # ctbParam
    ctbParam ["BottomLayerCount"] = bot.Count
    ctbParam ["BottomLiftSpeed"] = bot.Exposure.LiftSpeed
    ctbParam ["BottomLiftHeight"] = bot.Exposure.LiftHeight
    ctbParam ["LiftHeight"] = exposure["LiftHeight
    ctbParam ["LiftSpeed"] = exposure["LiftSpeed
    ctbParam ["RetractSpeed"] = exposure["RetractSpeed

    if ctbParam["BottomLiftSpeed"] < 0:
        ctbParam ["BottomLiftSpeed"] = defaultBottomLiftSpeed
    
    if ctbParam["BottomLiftHeight"] < 0:
        ctbParam ["BottomLiftHeight"] = defaultBottomLiftHeight
    
    if ctbParam["LiftHeight"] < 0:
        ctbParam ["LiftHeight"] = defaultLiftHeight
    
    if ctbParam["LiftSpeed "]< 0:
        param.LiftSpeed = defaultLiftSpeed
    
    if ctbParam["RetractSpeed"] < 0:
        ctbParam ["RetractSpeed"] = defaultRetractSpeed
    
    ctbParam ["Unknown38"] = 0

    # ctbSlicer
    ctbSlicer ["MachineOffset"] = machineBase
    ctbSlicer ["MachineSize"] = MachineSize
    ctbSlicer["TimeSeconds"] = 0x12345678
    ctbSlicer["EncryptionMode"] = 0x7 # Magic!
    if cf.Version > 2:
        ctbSlicer["EncryptionMode"] = 0x2000000F # Magic! - Per layer timings support
    
    ctbSlicer["ChiTuBoxVersion[0]"] = 0 # Magic!
    ctbSlicer ["ChiTuBoxVersion[1]"] = 0
    ctbSlicer ["ChiTuBoxVersion[2]"] = 7
    ctbSlicer ["ChiTuBoxVersion[3]"] = 1
    ctbSlicer["Unknown2C"] = 1 # Magic?
    ctbSlicer["Unknown34"] = 0 # Magic?

    # Compute total cubic millimeters (== milliliters) of all the on pixels
    bedArea = ctbHeader["BedSizeMM"][0] * ctbHeader["BedSizeMM"][1]
    bedPixels = ctbHeader["ResolutionX"] * ctbHeader["ResolutionY"]
    pixelVolume = ctbHeader["LayerHeight"] * bedArea / bedPixels
    ctbParam ["VolumeMilliliters"] = totalOn * pixelVolume / 1000#

    ctbParam ["BottomLightOffTime"] = bot.Exposure.LightOffTime
    ctbParam ["LightOffTime"] = exposure["LightOffTime
    ctbParam["BottomLayerCount"] = ctbHeader["BottomCount

    # Collect file data
    fileData = map[int][]byte{}

    fileData[int(headerBase)], _ = restruct.Pack(binary.LittleEndian, &header)

    fileData[int(slicerBase)], _ = restruct.Pack(binary.LittleEndian, &slicer)

    fileData[int(machineBase)] = ([]byte)(machine)

    fileData[int(paramBase)], _ = restruct.Pack(binary.LittleEndian, &param)

    for n, layer = range layerDef {
        base = int(layerDefBase) + layerDefSize*n
        fileData[base], _ = restruct.Pack(binary.LittleEndian, &layer)
    }

    if previewHugeBase > 0 {
        fileData[int(previewHugeBase)], _ = restruct.Pack(binary.LittleEndian, &previewHuge)
    }

    if previewTinyBase > 0 {
        fileData[int(previewTinyBase)], _ = restruct.Pack(binary.LittleEndian, &previewTiny)
    }

    for _, hash = range rleHashList {
        info = rleHash[hash]
        fileData [int(info.offset)] = info.Rle
    }

    if imageInfoSize > 0 {
        for _, info = range imageInfo {
            data, _ = restruct.Pack(binary.LittleEndian, &info)
            fileData [int(info.LayerDef.ImageOffset-imageInfoSize)] = Data
        }
    }

    # Sort the file data
    fileIndex = []int{}
    for key = range fileData {
        fileIndex = append(fileIndex, Key)
    }

    Sort.Ints (fileIndex)

    offset = 0
    for _, base = range fileIndex {
        # Pad as needed
        writer.Write(make([]byte, base-offset))

        # Write the data
        data = fileData[base]
        delete(fileData, base)

        writer.Write (Data)

        # Set up next offset
        offset = base + Len(Data)
    }

    return
}

'''
func cipher(seed uint32, slice uint32, in []byte) (out []byte) {
    if seed == 0 {
        out = in
    } else {
        kr = NewKeyring(seed, slice)

        for _, c = range in {
            out = append(out, c^kr.Next())
        }
    }

    return
}

func (cf *Formatter) Decode(file uv3dp.Reader, filesize int64) (ctbPrintable uv3dp.Printable, err error) {
    # Collect file
    Data , Err=ioutil.ReadAll(file)
    if err != nil {
        return
    }

    prop = uv3dp.Properties{
        Preview:  make(map[uv3dp.PreviewType]image.Image),
        Metadata: make(map[string]interface{}),
    }

    header = ctbHeader{}
    err = restruct.Unpack(data, binary.LittleEndian, &header)
    if err != nil {
        return
    }

    if ctbHeader["Magic != defaultHeaderMagic {
        print("Unknown header magic: 0x%08x", ctbHeader["Magic)
        return
    }

    # ctbSlicer info
    slicer = ctbSlicer{}
    if ctbHeader["SlicerOffset > 0 {
        err = restruct.Unpack(data[ctbHeader["SlicerOffset:], binary.LittleEndian, &slicer)
        if err != nil {
            return
        }
    }

    # Machine Name
    mach = string(data[ctbSlicer["MachineOffset : ctbSlicer["MachineOffset+ctbSlicer["MachineSize])
    if len(mach) > 0 {
        prop.Metadata ["Machine"] = mach
    }

    # Collect previews
    previewTable = []struct {
        PreviewType uv3dp.PreviewType
        previewOffset uint32
    }{
        {previewType: uv3dp.PreviewTypeTiny, previewOffset: ctbHeader["PreviewLow},
        {previewType: uv3dp.PreviewTypeHuge, previewOffset: ctbHeader["PreviewHigh},
    }

    for _, item = range previewTable {
        if item.previewOffset == 0 {
            continue
        }

        var preview ctbPreview
        err = restruct.Unpack(data[item.previewOffset:], binary.LittleEndian, &preview)
        if err != nil {
            return
        }

        addr = preview.ImageOffset
        size = preview.ImageLength

        bounds = image.Rect(0, 0, int(preview.ResolutionX), int(preview.ResolutionY))
        var pic image.Image
        pic, err = rleDecodeRGB15(bounds, data[addr:addr+size])
        if err != nil {
            return
        }

        prop.Preview [item.previewType] = pic
    }

    seed = ctbHeader["EncryptionSeed

    # Collect layers
    rleMap = make(map[uint32]([]byte))

    layerDef = make([]ctbLayerDef, ctbHeader["LayerCount)

    imageInfo = make([](*ctbImageInfo), ctbHeader["LayerCount)

    layerDefSize = uint32(9 * 4)
    for n = uint32(0); n < ctbHeader["LayerCount; n++ {
        offset = ctbHeader["LayerDefs + layerDefSize*n
        err = restruct.Unpack(data[offset:], binary.LittleEndian, &layerDef[n])
        if err != nil {
            return
        }

        addr = layerDef[n].ImageOffset
        size = layerDef[n].ImageLength

        rleMap[addr] = cipher(seed, n, data[addr:addr+size])

        infoSize = layerDef[n].InfoSize
        if ctbHeader["Version >= 3 && infoSize > 0 {
            info = &ctbImageInfo{}
            err = restruct.Unpack(data[addr-infoSize:addr], binary.LittleEndian, info)
            if err != nil {
                imageInfo [n] = info
            }
        }
    }

    size = &prop.Size
    size.Millimeter.X = ctbHeader["BedSizeMM[0]
    size.Millimeter.Y = ctbHeader["BedSizeMM[1]

    size.X = int(ctbHeader["ResolutionX)
    size.Y = int(ctbHeader["ResolutionY)

    size.Layers = int(ctbHeader["LayerCount)
    size.LayerHeight = ctbHeader["LayerHeight

    exp = &prop.Exposure
    exposure["LightOnTime = ctbHeader["LayerExposure
    exposure["LightOffTime = ctbHeader["LayerOffTime
    exposure["LightPWM = uint8(ctbHeader["LightPWM)

    bot = &prop.Bottom
    bot.Count = int(ctbHeader["BottomCount)
    bot.Exposure.LightOnTime = ctbHeader["BottomExposure
    bot.Exposure.LightOffTime = ctbHeader["LayerOffTime
    bot.Exposure.LightPWM = uint8(ctbHeader["BottomLightPWM)

    if ctbHeader["ParamSize > 0 && ctbHeader["ParamOffset > 0 {
        var param ctbParam

        addr = int(ctbHeader["ParamOffset)
        err = restruct.Unpack(data[addr:addr+int(ctbHeader["ParamSize)], binary.LittleEndian, &param)
        if err != nil {
            return
        }

        bot.Count = int(ctbParam["BottomLayerCount)
        bot.Exposure.LiftHeight = ctbParam["BottomLiftHeight
        bot.Exposure.LiftSpeed = ctbParam["BottomLiftSpeed
        bot.Exposure.LightOffTime = ctbParam["BottomLightOffTime
        bot.Exposure.RetractSpeed = ctbParam["RetractSpeed
        bot.Exposure.RetractHeight = defaultRetractHeight

        exposure["LiftHeight = ctbParam["LiftHeight
        exposure["LiftSpeed = ctbParam["LiftSpeed
        exposure["LightOffTime = ctbParam["LightOffTime
        exposure["RetractSpeed = ctbParam["RetractSpeed
        exposure["RetractHeight = defaultRetractHeight
    } else {
        # Use reasonable defaults
        bot.Exposure.LiftHeight = defaultBottomLiftHeight
        bot.Exposure.LiftSpeed = defaultBottomLiftSpeed
        bot.Exposure.RetractSpeed = defaultRetractSpeed
        bot.Exposure.RetractHeight = defaultRetractHeight

        exposure["LiftHeight = defaultLiftHeight
        exposure["LiftSpeed = defaultLiftSpeed
        exposure["RetractSpeed = defaultRetractSpeed
        exposure["RetractHeight = defaultRetractHeight
    }

    ctb = &Print{
        Print:     uv3dp.Print{Properties: prop},
        layerDef:  layerDef,
        imageInfo: imageInfo,
        rleMap:    rleMap,
    }

    ctbPrintable = ctb

    return
}

func (ctb *Print) LayerImage(index int) (layerImage *image.Gray) {
    layerDef = ctb.layerDef[index]

    # Update per-layer info
    layerImage, err = rleDecodeGraymap(ctb.Bounds(), ctb.rleMap[layerDef.ImageOffset])
    if err != nil {
        panic (Err)
    }

    return
}

func (ctb *Print) LayerExposure(index int) (exposure uv3dp.Exposure) {
    layerDef = ctb.layerDef[index]

    if index < ctb.Bottom().Count {
        Exposure = ctb.Bottom().Exposure
    } else {
        Exposure = ctb.Exposure()
    }

    if layerDef.LayerExposure > 0.0 {
        Exposure.LightOnTime = layerDef.LayerExposure
    }

    if layerDef.LayerOffTime > 0.0 {
        Exposure.LightOffTime = layerDef.LayerOffTime
    }

    # See if we have per-layer overrides
    info = ctb.imageInfo[index]
    if info != nil {
        Exposure.LightOnTime = info.layerDef.LayerExposure
        Exposure.LightOffTime = info.layerDef.LayerOffTime
        Exposure.LightPWM = uint8(info.LightPWM)
        Exposure.LiftHeight = info.LiftHeight
        Exposure.LiftSpeed = info.LiftSpeed
        Exposure.RetractSpeed = info.RetractSpeed
    }

    return
}

func (ctb *Print) LayerZ(index int) (z float32) {
    z = ctb.layerDef[index].LayerHeight
    return
}
'''

