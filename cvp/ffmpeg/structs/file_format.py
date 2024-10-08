# -*- coding: utf-8 -*-

import os
from io import StringIO
from subprocess import check_output
from typing import Dict, Final, List, NamedTuple, Sequence
from urllib.parse import urlparse

# noinspection SpellCheckingInspection
_FFMPEG_FORMATS_STDOUT_SAMPLE = """
File formats:
 D. = Demuxing supported
 .E = Muxing supported
 --
 D  3dostr          3DO STR
  E 3g2             3GP2 (3GPP2 file format)
  E 3gp             3GP (3GPP file format)
 D  4xm             4X Technologies
  E a64             a64 - video for Commodore 64
 D  aa              Audible AA format files
 D  aac             raw ADTS AAC (Advanced Audio Coding)
 D  aax             CRI AAX
 DE ac3             raw AC-3
 D  ace             tri-Ace Audio Container
 D  acm             Interplay ACM
 D  act             ACT Voice file format
 D  adf             Artworx Data Format
 D  adp             ADP
 D  ads             Sony PS2 ADS
  E adts            ADTS AAC (Advanced Audio Coding)
 DE adx             CRI ADX
 D  aea             MD STUDIO audio
 D  afc             AFC
 DE aiff            Audio IFF
 D  aix             CRI AIX
 DE alaw            PCM A-law
 D  alias_pix       Alias/Wavefront PIX image
 DE alp             LEGO Racers ALP
 DE alsa            ALSA audio output
 DE amr             3GPP AMR
 D  amrnb           raw AMR-NB
 D  amrwb           raw AMR-WB
  E amv             AMV
 D  anm             Deluxe Paint Animation
 D  apc             CRYO APC
 D  ape             Monkey's Audio
 DE apm             Ubisoft Rayman 2 APM
 DE apng            Animated Portable Network Graphics
 DE aptx            raw aptX (Audio Processing Technology for Bluetooth)
 DE aptx_hd         raw aptX HD (Audio Processing Technology for Bluetooth)
 D  aqtitle         AQTitle subtitles
 DE argo_asf        Argonaut Games ASF
 D  argo_brp        Argonaut Games BRP
 DE asf             ASF (Advanced / Active Streaming Format)
 D  asf_o           ASF (Advanced / Active Streaming Format)
  E asf_stream      ASF (Advanced / Active Streaming Format)
 DE ass             SSA (SubStation Alpha) subtitle
 DE ast             AST (Audio Stream)
 DE au              Sun AU
 D  av1             AV1 Annex B
 DE avi             AVI (Audio Video Interleaved)
  E avm2            SWF (ShockWave Flash) (AVM2)
 D  avr             AVR (Audio Visual Research)
 D  avs             Argonaut Games Creature Shock
 DE avs2            raw AVS2-P2/IEEE1857.4 video
 D  avs3            raw AVS3-P2/IEEE1857.10
 D  bethsoftvid     Bethesda Softworks VID
 D  bfi             Brute Force & Ignorance
 D  bfstm           BFSTM (Binary Cafe Stream)
 D  bin             Binary text
 D  bink            Bink
 D  binka           Bink Audio
 DE bit             G.729 BIT file format
 D  bmp_pipe        piped bmp sequence
 D  bmv             Discworld II BMV
 D  boa             Black Ops Audio
 D  brender_pix     BRender PIX image
 D  brstm           BRSTM (Binary Revolution Stream)
 D  c93             Interplay C93
  E caca            caca (color ASCII art) output device
 DE caf             Apple CAF (Core Audio Format)
 DE cavsvideo       raw Chinese AVS (Audio Video Standard) video
 D  cdg             CD Graphics
 D  cdxl            Commodore CDXL video
  E chromaprint     Chromaprint
 D  cine            Phantom Cine
 DE codec2          codec2 .c2 muxer
 DE codec2raw       raw codec2 muxer
 D  concat          Virtual concatenation script
  E crc             CRC testing
 D  cri_pipe        piped cri sequence
 DE dash            DASH Muxer
 DE data            raw data
 DE daud            D-Cinema audio
 D  dcstr           Sega DC STR
 D  dds_pipe        piped dds sequence
 D  derf            Xilam DERF
 D  dfa             Chronomaster DFA
 D  dhav            Video DAV
 DE dirac           raw Dirac
 DE dnxhd           raw DNxHD (SMPTE VC-3)
 D  dpx_pipe        piped dpx sequence
 D  dsf             DSD Stream File (DSF)
 D  dsicin          Delphine Software International CIN
 D  dss             Digital Speech Standard (DSS)
 DE dts             raw DTS
 D  dtshd           raw DTS-HD
 DE dv              DV (Digital Video)
 D  dvbsub          raw dvbsub
 D  dvbtxt          dvbtxt
  E dvd             MPEG-2 PS (DVD VOB)
 D  dxa             DXA
 D  ea              Electronic Arts Multimedia
 D  ea_cdata        Electronic Arts cdata
 DE eac3            raw E-AC-3
 D  epaf            Ensoniq Paris Audio File
 D  exr_pipe        piped exr sequence
 DE f32be           PCM 32-bit floating-point big-endian
 DE f32le           PCM 32-bit floating-point little-endian
  E f4v             F4V Adobe Flash Video
 DE f64be           PCM 64-bit floating-point big-endian
 DE f64le           PCM 64-bit floating-point little-endian
 DE fbdev           Linux framebuffer
 DE ffmetadata      FFmpeg metadata in text
  E fifo            FIFO queue pseudo-muxer
  E fifo_test       Fifo test muxer
 DE film_cpk        Sega FILM / CPK
 DE filmstrip       Adobe Filmstrip
 DE fits            Flexible Image Transport System
 DE flac            raw FLAC
 D  flic            FLI/FLC/FLX animation
 DE flv             FLV (Flash Video)
  E framecrc        framecrc testing
  E framehash       Per-frame hash testing
  E framemd5        Per-frame MD5 testing
 D  frm             Megalux Frame
 D  fsb             FMOD Sample Bank
 D  fwse            Capcom's MT Framework sound
 DE g722            raw G.722
 DE g723_1          raw G.723.1
 DE g726            raw big-endian G.726 ("left-justified")
 DE g726le          raw little-endian G.726 ("right-justified")
 D  g729            G.729 raw format demuxer
 D  gdv             Gremlin Digital Video
 D  genh            GENeric Header
 DE gif             CompuServe Graphics Interchange Format (GIF)
 D  gif_pipe        piped gif sequence
 DE gsm             raw GSM
 DE gxf             GXF (General eXchange Format)
 DE h261            raw H.261
 DE h263            raw H.263
 DE h264            raw H.264 video
  E hash            Hash testing
 D  hca             CRI HCA
 D  hcom            Macintosh HCOM
  E hds             HDS Muxer
 DE hevc            raw HEVC video
 DE hls             Apple HTTP Live Streaming
 D  hnm             Cryo HNM v4
 DE ico             Microsoft Windows ICO
 D  idcin           id Cinematic
 D  idf             iCE Draw File
 D  iec61883        libiec61883 (new DV1394) A/V input device
 D  iff             IFF (Interchange File Format)
 D  ifv             IFV CCTV DVR
 DE ilbc            iLBC storage
 DE image2          image2 sequence
 DE image2pipe      piped image2 sequence
 D  ingenient       raw Ingenient MJPEG
 D  ipmovie         Interplay MVE
  E ipod            iPod H.264 MP4 (MPEG-4 Part 14)
 D  ipu             raw IPU Video
 DE ircam           Berkeley/IRCAM/CARL Sound Format
  E ismv            ISMV/ISMA (Smooth Streaming)
 D  iss             Funcom ISS
 D  iv8             IndigoVision 8000 video
 DE ivf             On2 IVF
 D  ivr             IVR (Internet Video Recording)
 D  j2k_pipe        piped j2k sequence
 D  jack            JACK Audio Connection Kit
 DE jacosub         JACOsub subtitle format
 D  jpeg_pipe       piped jpeg sequence
 D  jpegls_pipe     piped jpegls sequence
 D  jv              Bitmap Brothers JV
 D  kmsgrab         KMS screen capture
 D  kux             KUX (YouKu)
 DE kvag            Simon & Schuster Interactive VAG
  E latm            LOAS/LATM
 D  lavfi           Libavfilter virtual input device
 D  libcdio
 D  libdc1394       dc1394 v.2 A/V grab
 D  libgme          Game Music Emu demuxer
 D  libopenmpt      Tracker formats (libopenmpt)
 D  live_flv        live RTMP FLV (Flash Video)
 D  lmlm4           raw lmlm4
 D  loas            LOAS AudioSyncStream
 DE lrc             LRC lyrics
 D  luodat          Video CCTV DAT
 D  lvf             LVF
 D  lxf             VR native stream (LXF)
 DE m4v             raw MPEG-4 video
  E matroska        Matroska
 D  matroska,webm   Matroska / WebM
 D  mca             MCA Audio Format
 D  mcc             MacCaption
  E md5             MD5 testing
 D  mgsts           Metal Gear Solid: The Twin Snakes
 DE microdvd        MicroDVD subtitle format
 DE mjpeg           raw MJPEG video
 D  mjpeg_2000      raw MJPEG 2000 video
  E mkvtimestamp_v2 extract pts as timecode v2 format, as defined by mkvtoolnix
 DE mlp             raw MLP
 D  mlv             Magic Lantern Video (MLV)
 D  mm              American Laser Games MM
 DE mmf             Yamaha SMAF
 D  mods            MobiClip MODS
 D  moflex          MobiClip MOFLEX
  E mov             QuickTime / MOV
 D  mov,mp4,m4a,3gp,3g2,mj2 QuickTime / MOV
  E mp2             MP2 (MPEG audio layer 2)
 DE mp3             MP3 (MPEG audio layer 3)
  E mp4             MP4 (MPEG-4 Part 14)
 D  mpc             Musepack
 D  mpc8            Musepack SV8
 DE mpeg            MPEG-1 Systems / MPEG program stream
  E mpeg1video      raw MPEG-1 video
  E mpeg2video      raw MPEG-2 video
 DE mpegts          MPEG-TS (MPEG-2 Transport Stream)
 D  mpegtsraw       raw MPEG-TS (MPEG-2 Transport Stream)
 D  mpegvideo       raw MPEG video
 DE mpjpeg          MIME multipart JPEG
 D  mpl2            MPL2 subtitles
 D  mpsub           MPlayer subtitles
 D  msf             Sony PS3 MSF
 D  msnwctcp        MSN TCP Webcam stream
 D  msp             Microsoft Paint (MSP))
 D  mtaf            Konami PS2 MTAF
 D  mtv             MTV
 DE mulaw           PCM mu-law
 D  musx            Eurocom MUSX
 D  mv              Silicon Graphics Movie
 D  mvi             Motion Pixels MVI
 DE mxf             MXF (Material eXchange Format)
  E mxf_d10         MXF (Material eXchange Format) D-10 Mapping
  E mxf_opatom      MXF (Material eXchange Format) Operational Pattern Atom
 D  mxg             MxPEG clip
 D  nc              NC camera feed
 D  nistsphere      NIST SPeech HEader REsources
 D  nsp             Computerized Speech Lab NSP
 D  nsv             Nullsoft Streaming Video
  E null            raw null video
 DE nut             NUT
 D  nuv             NuppelVideo
 D  obu             AV1 low overhead OBU
  E oga             Ogg Audio
 DE ogg             Ogg
  E ogv             Ogg Video
 DE oma             Sony OpenMG audio
 D  openal          OpenAL audio capture device
  E opengl          OpenGL output
  E opus            Ogg Opus
 DE oss             OSS (Open Sound System) playback
 D  paf             Amazing Studio Packed Animation File
 D  pam_pipe        piped pam sequence
 D  pbm_pipe        piped pbm sequence
 D  pcx_pipe        piped pcx sequence
 D  pgm_pipe        piped pgm sequence
 D  pgmyuv_pipe     piped pgmyuv sequence
 D  pgx_pipe        piped pgx sequence
 D  photocd_pipe    piped photocd sequence
 D  pictor_pipe     piped pictor sequence
 D  pjs             PJS (Phoenix Japanimation Society) subtitles
 D  pmp             Playstation Portable PMP
 D  png_pipe        piped png sequence
 D  pp_bnk          Pro Pinball Series Soundbank
 D  ppm_pipe        piped ppm sequence
 D  psd_pipe        piped psd sequence
  E psp             PSP MP4 (MPEG-4 Part 14)
 D  psxstr          Sony Playstation STR
 DE pulse           Pulse audio output
 D  pva             TechnoTrend PVA
 D  pvf             PVF (Portable Voice Format)
 D  qcp             QCP
 D  qdraw_pipe      piped qdraw sequence
 D  r3d             REDCODE R3D
 DE rawvideo        raw video
 D  realtext        RealText subtitle format
 D  redspark        RedSpark
 D  rl2             RL2
 DE rm              RealMedia
 DE roq             raw id RoQ
 D  rpl             RPL / ARMovie
 D  rsd             GameCube RSD
 DE rso             Lego Mindstorms RSO
 DE rtp             RTP output
  E rtp_mpegts      RTP/mpegts output format
 DE rtsp            RTSP output
 DE s16be           PCM signed 16-bit big-endian
 DE s16le           PCM signed 16-bit little-endian
 DE s24be           PCM signed 24-bit big-endian
 DE s24le           PCM signed 24-bit little-endian
 DE s32be           PCM signed 32-bit big-endian
 DE s32le           PCM signed 32-bit little-endian
 D  s337m           SMPTE 337M
 DE s8              PCM signed 8-bit
 D  sami            SAMI subtitle format
 DE sap             SAP output
 DE sbc             raw SBC
 D  sbg             SBaGen binaural beats script
 DE scc             Scenarist Closed Captions
  E sdl,sdl2        SDL2 output device
 D  sdp             SDP
 D  sdr2            SDR2
 D  sds             MIDI Sample Dump Standard
 D  sdx             Sample Dump eXchange
  E segment         segment
 D  ser             SER (Simple uncompressed video format for astronomical capturing)
 D  sga             Digital Pictures SGA
 D  sgi_pipe        piped sgi sequence
 D  shn             raw Shorten
 D  siff            Beam Software SIFF
 D  simbiosis_imx   Simbiosis Interactive IMX
  E singlejpeg      JPEG single image
 D  sln             Asterisk raw pcm
 DE smjpeg          Loki SDL MJPEG
 D  smk             Smacker
  E smoothstreaming Smooth Streaming Muxer
 D  smush           LucasArts Smush
 DE sndio           sndio audio playback
 D  sol             Sierra SOL
 DE sox             SoX native
 DE spdif           IEC 61937 (used on S/PDIF - IEC958)
  E spx             Ogg Speex
 DE srt             SubRip subtitle
 D  stl             Spruce subtitle format
  E stream_segment,ssegment streaming segment muxer
  E streamhash      Per-stream hash testing
 D  subviewer       SubViewer subtitle format
 D  subviewer1      SubViewer v1 subtitle format
 D  sunrast_pipe    piped sunrast sequence
 DE sup             raw HDMV Presentation Graphic Stream subtitles
 D  svag            Konami PS2 SVAG
  E svcd            MPEG-2 PS (SVCD)
 D  svg_pipe        piped svg sequence
 D  svs             Square SVS
 DE swf             SWF (ShockWave Flash)
 D  tak             raw TAK
 D  tedcaptions     TED Talks captions
  E tee             Multiple muxer tee
 D  thp             THP
 D  tiertexseq      Tiertex Limited SEQ
 D  tiff_pipe       piped tiff sequence
 D  tmv             8088flex TMV
 DE truehd          raw TrueHD
 DE tta             TTA (True Audio)
  E ttml            TTML subtitle
 D  tty             Tele-typewriter
 D  txd             Renderware TeXture Dictionary
 D  ty              TiVo TY Stream
 DE u16be           PCM unsigned 16-bit big-endian
 DE u16le           PCM unsigned 16-bit little-endian
 DE u24be           PCM unsigned 24-bit big-endian
 DE u24le           PCM unsigned 24-bit little-endian
 DE u32be           PCM unsigned 32-bit big-endian
 DE u32le           PCM unsigned 32-bit little-endian
 DE u8              PCM unsigned 8-bit
  E uncodedframecrc uncoded framecrc testing
 D  v210            Uncompressed 4:2:2 10-bit
 D  v210x           Uncompressed 4:2:2 10-bit
 D  vag             Sony PS2 VAG
 DE vc1             raw VC-1 video
 DE vc1test         VC-1 test bitstream
  E vcd             MPEG-1 Systems / MPEG program stream (VCD)
 DE vidc            PCM Archimedes VIDC
 DE video4linux2,v4l2 Video4Linux2 output device
 D  vividas         Vividas VIV
 D  vivo            Vivo
 D  vmd             Sierra VMD
  E vob             MPEG-2 PS (VOB)
 D  vobsub          VobSub subtitle format
 DE voc             Creative Voice
 D  vpk             Sony PS2 VPK
 D  vplayer         VPlayer subtitles
 D  vqf             Nippon Telegraph and Telephone Corporation (NTT) TwinVQ
 DE w64             Sony Wave64
 DE wav             WAV / WAVE (Waveform Audio)
 D  wc3movie        Wing Commander III movie
  E webm            WebM
  E webm_chunk      WebM Chunk Muxer
 DE webm_dash_manifest WebM DASH Manifest
  E webp            WebP
 D  webp_pipe       piped webp sequence
 DE webvtt          WebVTT subtitle
 D  wsaud           Westwood Studios audio
 D  wsd             Wideband Single-bit Data (WSD)
 D  wsvqa           Westwood Studios VQA
 DE wtv             Windows Television (WTV)
 DE wv              raw WavPack
 D  wve             Psion 3 audio
 D  x11grab         X11 screen capture, using XCB
 D  xa              Maxis XA
 D  xbin            eXtended BINary text (XBIN)
 D  xbm_pipe        piped xbm sequence
 D  xmv             Microsoft XMV
 D  xpm_pipe        piped xpm sequence
  E xv              XV (XVideo) output device
 D  xvag            Sony PS3 XVAG
 D  xwd_pipe        piped xwd sequence
 D  xwma            Microsoft xWMA
 D  yop             Psygnosis YOP
 DE yuv4mpegpipe    YUV4MPEG pipe
"""

AUTOMATIC_DETECT_FILE_FORMAT: Final[str] = "autodect"

WELL_KNOWN_SCHEME_FORMAT: Final[Dict[str, str]] = {
    "rtmp": "flv",
    "rtsp": "rtsp",
}

FFMPEG_FILE_FORMATS_HEADER_LINES: Final[Sequence[str]] = (
    "File formats:",
    " D. = Demuxing supported",
    " .E = Muxing supported",
    " --",
)
"""Skip unnecessary header lines in `ffmpeg -hide_banner -formats` command."""


class FileFormat(NamedTuple):
    supported_demuxing: bool
    supported_muxing: bool
    name: str
    description: str

    def __repr__(self):
        buffer = StringIO()
        buffer.write("D" if self.supported_demuxing else ".")
        buffer.write("E" if self.supported_muxing else ".")
        buffer.write(f" {self.name}")
        return buffer.getvalue()

    @classmethod
    def from_format_line(cls, line: str):
        supported_demuxing = line[1] == "D"
        supported_muxing = line[2] == "E"
        name_desc = line[4:].split(maxsplit=1)
        name = name_desc[0]
        desc = name_desc[1] if len(name_desc) == 2 else str()
        return cls(
            supported_demuxing=supported_demuxing,
            supported_muxing=supported_muxing,
            name=name,
            description=desc,
        )


def parse_file_formats_output(text: str) -> List[FileFormat]:
    lines = text.splitlines()
    for i, header_line in enumerate(FFMPEG_FILE_FORMATS_HEADER_LINES):
        if lines[i] != header_line:
            raise ValueError(f"This is not the expected header line #{i}: '{lines[i]}'")

    begin = len(FFMPEG_FILE_FORMATS_HEADER_LINES)
    lines = lines[begin:]

    # [IMPORTANT] Do not use strip
    return [FileFormat.from_format_line(line) for line in lines]


def inspect_file_formats(ffmpeg="ffmpeg") -> List[FileFormat]:
    cmds = (ffmpeg, "-hide_banner", "-formats")
    output = check_output(cmds).decode("utf-8")
    return parse_file_formats_output(output)


def detect_file_format(url: str, ffmpeg="ffmpeg") -> str:
    if os.path.exists(url):
        ext = os.path.splitext(url)[1]
        return ext[1:] if ext[0] == "." else ext
    else:
        file_formats = inspect_file_formats(ffmpeg)
        o = urlparse(url)
        if o.scheme:
            if o.scheme in WELL_KNOWN_SCHEME_FORMAT:
                return WELL_KNOWN_SCHEME_FORMAT[o.scheme]
            try:
                file_format = next(filter(lambda f: f.name == o.scheme, file_formats))
            except StopIteration:
                raise IndexError(f"Unsupported URL scheme: {o.scheme}")
            else:
                return file_format.name
        else:
            raise NotImplementedError("URL scheme is required")
