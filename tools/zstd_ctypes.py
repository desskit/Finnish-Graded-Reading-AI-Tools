import ctypes, ctypes.util, sys
lib = ctypes.CDLL(ctypes.util.find_library("zstd"))
lib.ZSTD_getFrameContentSize.restype = ctypes.c_ulonglong
lib.ZSTD_getFrameContentSize.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
lib.ZSTD_decompress.restype = ctypes.c_size_t
lib.ZSTD_decompress.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t]
lib.ZSTD_isError.restype = ctypes.c_uint
lib.ZSTD_DStreamOutSize.restype = ctypes.c_size_t

class Buf(ctypes.Structure):
    _fields_ = [("src", ctypes.c_void_p), ("size", ctypes.c_size_t), ("pos", ctypes.c_size_t)]

def decompress(data):
    n = lib.ZSTD_getFrameContentSize(data, len(data))
    if n not in (0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFE):   # UNKNOWN / ERROR
        out = ctypes.create_string_buffer(n)
        r = lib.ZSTD_decompress(out, n, data, len(data))
        if not lib.ZSTD_isError(r):
            return out.raw[:r]
    # streaming fallback
    lib.ZSTD_createDStream.restype = ctypes.c_void_p
    lib.ZSTD_initDStream.argtypes = [ctypes.c_void_p]
    lib.ZSTD_decompressStream.restype = ctypes.c_size_t
    lib.ZSTD_decompressStream.argtypes = [ctypes.c_void_p, ctypes.POINTER(Buf), ctypes.POINTER(Buf)]
    ds = lib.ZSTD_createDStream(); lib.ZSTD_initDStream(ds)
    osz = lib.ZSTD_DStreamOutSize()
    obuf = ctypes.create_string_buffer(osz)
    src = ctypes.create_string_buffer(data, len(data))
    inb = Buf(ctypes.cast(src, ctypes.c_void_p), len(data), 0)
    chunks = []
    while inb.pos < inb.size:
        outb = Buf(ctypes.cast(obuf, ctypes.c_void_p), osz, 0)
        r = lib.ZSTD_decompressStream(ds, ctypes.byref(outb), ctypes.byref(inb))
        if lib.ZSTD_isError(r): raise RuntimeError("zstd stream error")
        chunks.append(obuf.raw[:outb.pos])
        if r == 0 and inb.pos >= inb.size: break
    return b"".join(chunks)

if __name__ == "__main__":
    raw = open(sys.argv[1], "rb").read()
    out = decompress(raw)
    open(sys.argv[2], "wb").write(out)
    print(f"{len(raw)} -> {len(out)} bytes; header={out[:16]!r}")
