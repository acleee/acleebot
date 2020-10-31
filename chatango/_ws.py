import collections
import os
import struct
import sys

CONTINUATION = 0
TEXT = 1
BINARY = 2
CLOSE = 8
PING = 9
PONG = 10

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

FrameInfo = collections.namedtuple(
    "FrameInfo", ["fin", "opcode", "masked", "payload_length"]
)


def check_frame(buff):
    """
    returns False if the buffer doesn't starts with a valid frame
    returns the size of the frame in success
    """
    buff = bytearray(buff)
    if len(buff) < 2:
        return False

    min_size = 2
    masked = False
    payload_length = 0

    if buff[1] & 128:
        min_size += 4
        masked = True

    if (buff[1] & 127) <= 125:
        payload_length = buff[1] & 127
    elif (buff[1] & 127) == 126:
        min_size += 2
        if len(buff) < 4:
            return False
        payload_length += struct.unpack_from(">H", buff, 2)[0]
    elif (buff[1] & 127) == 127:
        min_size += 8
        if len(buff) < 10:
            return False
        payload_length += struct.unpack_from(">Q", buff, 2)[0]
    if len(buff) < (min_size + payload_length):
        return False
    return min_size + payload_length


def frame_info(buff):
    """
    returns a tuple that describes a frame
    """
    buff = bytearray(buff)
    r = check_frame(buff)
    if not r:
        raise ValueError("buff is not a valid frame")
    payload_length = 0
    if (buff[1] & 127) <= 125:
        payload_length = buff[1] & 127
    elif (buff[1] & 127) == 126:
        payload_length += struct.unpack_from(">H", buff, 2)[0]
    elif (buff[1] & 127) == 127:
        payload_length += struct.unpack_from(">Q", buff, 2)[0]

    return FrameInfo(
        bool(buff[0] & 128), buff[0] & 15, bool(buff[1] & 128), payload_length
    )


def get_frames(buff):
    frames = []

    begin = 0
    end = check_frame(buff)
    while end:
        frames.append(buff[begin:end])
        begin = end
        end = check_frame(buff[end:])

    return frames


def check_msg(buff):
    """
    returns True  if the buffer starts with a full fragmented message, or a
    unfragmented frame
    returns where the last frame ends
    """
    r = check_frame(buff)
    s = 0
    while r:
        s += r
        if frame_info(buff)[0]:
            return s
    return False


def mask_buff(buff):
    """
    masks buff with a random mask
    retunrs mask + masked buff
    """
    buff = bytearray(buff)
    mask = bytearray(os.urandom(4))
    return bytes(mask + bytearray(x ^ mask[i % 4] for i, x in enumerate(buff)))


def unmask_buff(buff):
    """
    unmask buff, using the firsts 4 bytes as the mask
    """
    buff = bytearray(buff)
    mask = buff[:4]
    return bytes(bytearray(x ^ mask[i % 4] for i, x in enumerate(buff[4:])))


def encode_frame(fin=True, opcode=TEXT, mask=False, payload=None):
    if not fin:
        opcode = CONTINUATION
    if mask:
        mask = os.urandom(4)

    if isinstance(payload, str):
        payload = payload.encode("utf-8", "replace")
    if sys.version_info[0] < 3 and isinstance(payload, unicode):
        paylod = payload.encode("utf-8", "replace")
    if payload is None:
        payload = b""
    elif not isinstance(payload, (bytes, bytearray)):
        raise ValueError("payload must be None, a str object or a bytes like object")

    frame = bytearray()
    if fin:
        frame.append(opcode | 128)
    else:
        frame.append(opcode)
    if mask:
        if len(payload) <= 125:
            frame.append(len(payload) | 128)
        elif len(payload) <= 65535:
            frame.append(126 | 128)
            frame += struct.pack(">H", len(payload))
        else:
            frame.append(127 | 128)
            frame += struct.pack(">Q", len(payload))
    else:
        if len(payload) <= 125:
            frame.append(len(payload))
        elif len(payload) <= 65535:
            frame.append(126)
            frame += struct.pack(">H", len(payload))
        else:
            frame.append(127)
            frame += struct.pack(">Q", len(payload))

    if mask:
        frame += mask_buff(payload)
    else:
        frame += payload

    return bytes(frame)


def get_payload(buff):
    """
    gets the payload of a frame
    if the payload is masked, it will unmask it
    if the opcode is text and fin is True, a str is returned
    if opcode is close, a tuple of code and message is returned
        (if the frame doens't contains a payload, (0, "") is returned)
    returns a bytes object otherwise
    """
    info = frame_info(buff)
    if not info.payload_length:
        payload = b""

    if info.payload_length <= 125:
        start_payload = 2
    elif info.payload_length <= 65535:
        start_payload = 4
    else:
        start_payload = 10

    if info.masked:
        payload = unmask_buff(
            buff[start_payload : info.payload_length + start_payload + 4]
        )
    else:
        payload = buff[start_payload : info.payload_length + start_payload]

    if info.opcode == TEXT and info.fin:
        return payload.decode("utf-8", "replace")
    elif info.opcode == CLOSE:
        return (
            struct.unpack_from(">H", buff)[0],
            payload[2:].decode("utf-8", "replace"),
        )

    return payload


def check_headers(headers):
    """
    returns False if the headers are invalid for a websocket handshake
    returns the key
    """
    version = None

    if isinstance(headers, (bytes, bytearray)):
        if b"\r\n\r\n" in headers:
            headers, _ = headers.split(b"\r\n\r\n", 1)
        headers = headers.decode()
    if sys.version_info[0] < 3 and isinstance(headers, unicode):
        headers = str(headers)
    if isinstance(headers, str):
        headers = headers.splitlines()
    if isinstance(headers, list):
        if ": " not in headers[0]:
            version, _ = headers[0].split(" ", 1)
            headers = headers[1:]
        headers = {y.lower(): z for y, z in map(lambda x: x.split(": ", 1), headers)}

    if version:
        version = version.split("/")[1]
        version = tuple(int(x) for x in version.split("."))
        if version < (1, 1):
            return False
    if headers.get("upgrade", "").lower() != "websocket":
        return False
    elif headers.get("connection", "").lower() != "upgrade":
        return False

    return headers.get("sec-websocket-accept", False)
