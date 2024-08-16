# -*- coding: utf-8 -*-

from shlex import split
from typing import List, Literal, Optional


class FFmpegGlobalOptions:
    _globals: List[str]

    def __init__(self) -> None:
        self._globals = list()

    def clear_globals(self):
        self._globals.clear()

    def append_global_options(self, *args):
        self._globals += tuple(str(a) for a in args if a is not None)
        return self

    def append_global_options_with_text(self, text: str, *, comments=False, posix=True):
        return self.append_global_options(*split(text, comments=comments, posix=posix))

    # ==================================================================================
    # Print help / information / capabilities:
    # ==================================================================================

    def license(self):
        """Show license"""
        return self.append_global_options("-L")

    def help(self, topic: Optional[str | Literal["long", "full"]] = None):
        """Show help"""
        return self.append_global_options("-help", topic)

    def help_long(self):
        """Print more options"""
        return self.help("long")

    def help_full(self):
        """Print all options
        (including all format and codec specific options, very long)
        """
        return self.help("full")

    def help_decoder(self, name: str):
        """Print detailed information about the decoder.
        Use the -decoders option to get a list of all decoders.
        """
        return self.help(f"decoder={name}")

    def help_encoder(self, name: str):
        """Print detailed information about the encoder.
        Use the -encoders option to get a list of all encoders.
        """
        return self.help(f"encoder={name}")

    def help_demuxer(self, name: str):
        """Print detailed information about the demuxer.
        Use the -formats option to get a list of all demuxers and muxers.
        """
        return self.help(f"demuxer={name}")

    def help_muxer(self, name: str):
        """Print detailed information about the muxer.
        Use the -formats option to get a list of all muxers and demuxers.
        """
        return self.help(f"muxer={name}")

    def help_filter(self, name: str):
        """Print detailed information about the filter.
        Use the -filters option to get a list of all filters.
        """
        return self.help(f"filter={name}")

    def help_bitstream_filter(self, name: str):
        """Print detailed information about the bitstream filter.
        Use the -bsfs option to get a list of all bitstream filters.
        """
        return self.help(f"bsf={name}")

    def help_protocol(self, name: str):
        """Print detailed information about the protocol.
        Use the -protocols option to get a list of all protocols.
        """
        return self.help(f"protocol={name}")

    def version(self):
        """Show version"""
        return self.append_global_options("-version")

    def buildconf(self):
        """Show build configuration"""
        return self.append_global_options("-buildconf")

    def formats(self):
        """Show available formats"""
        return self.append_global_options("-formats")

    def muxers(self):
        """Show available muxers"""
        return self.append_global_options("-muxers")

    def demuxers(self):
        """Show available demuxers"""
        return self.append_global_options("-demuxers")

    def devices(self):
        """Show available devices"""
        return self.append_global_options("-devices")

    def codecs(self):
        """Show available codecs"""
        return self.append_global_options("-codecs")

    def decoders(self):
        """Show available decoders"""
        return self.append_global_options("-decoders")

    def encoders(self):
        """Show available encoders"""
        return self.append_global_options("-encoders")

    def bsfs(self):
        """Show available bit stream filters"""
        return self.append_global_options("-bsfs")

    def protocols(self):
        """Show available protocols"""
        return self.append_global_options("-protocols")

    def filters(self):
        """Show available filters"""
        return self.append_global_options("-filters")

    def pix_fmts(self):
        """Show available pixel formats"""
        return self.append_global_options("-pix_fmts")

    def layouts(self):
        """Show standard channel layouts"""
        return self.append_global_options("-layouts")

    def sample_fmts(self):
        """Show available audio sample formats"""
        return self.append_global_options("-sample_fmts")

    def colors(self):
        """Show available color names"""
        return self.append_global_options("-colors")

    def sources(self, device: Optional[str] = None):
        """List sources of the input device"""
        return self.append_global_options("-sources", device)

    def sinks(self, device: Optional[str] = None):
        """List sinks of the output device"""
        return self.append_global_options("-sinks", device)

    def hwaccels(self):
        """Show available HW acceleration methods"""
        return self.append_global_options("-hwaccels")

    # ==================================================================================
    # Global options (affect whole program instead of just one file):
    # ==================================================================================

    def loglevel(self, loglevel: str):
        """Set logging level"""
        return self.append_global_options("-loglevel", loglevel)

    def v(self, loglevel: str):
        """Set logging level"""
        return self.append_global_options("-v", loglevel)

    def report(self):
        """Generate a report"""
        return self.append_global_options("-report")

    def max_alloc(self, size: int):
        """Set maximum size of a single allocated block"""
        return self.append_global_options("-max_alloc", size)

    def y(self):
        """Overwrite output files"""
        return self.append_global_options("-y")

    def n(self):
        """Never overwrite output files"""
        return self.append_global_options("-n")

    def ignore_unknown(self):
        """Ignore unknown stream types"""
        return self.append_global_options("-ignore_unknown")

    def filter_threads(self):
        """Number of non-complex filter threads"""
        return self.append_global_options("-filter_threads")

    def filter_complex_threads(self):
        """Number of threads for -filter_complex"""
        return self.append_global_options("-filter_complex_threads")

    def stats(self):
        """Print progress report during encoding"""
        return self.append_global_options("-stats")

    def max_error_rate(self, rate: float):
        """Ratio of decoding errors
        (0.0: no errors, 1.0: 100% errors)
        above which ffmpeg returns an error instead of success.
        """
        assert 0.0 <= rate <= 1.0
        return self.append_global_options("-max_error_rate", rate)

    def bits_per_raw_sample(self, number: int):
        """Set the number of bits per raw sample"""
        return self.append_global_options("-bits_per_raw_sample", number)

    def vol(self, volume: int):
        """Change audio volume (256=normal)"""
        return self.append_global_options("-vol", volume)

    # ==================================================================================
    # Advanced global options:
    # ==================================================================================

    def cpuflags(self, flags: str):
        """Force specific cpu flags"""
        return self.append_global_options("-cpuflags", flags)

    def hide_banner(self, hide_banner=None):
        """Do not show program banner"""
        return self.append_global_options("-hide_banner", hide_banner)

    def copy_unknown(self):
        """Copy unknown stream types"""
        return self.append_global_options("-copy_unknown")

    def benchmark(self):
        """Add timings for benchmarking"""
        return self.append_global_options("-benchmark")

    def benchmark_all(self):
        """Add timings for each task"""
        return self.append_global_options("-benchmark_all")

    def progress(self, url: str):
        """Write program-readable progress information"""
        return self.append_global_options("-progress", url)

    def stdin(self):
        """Enable or disable interaction on standard input"""
        return self.append_global_options("-stdin")

    def timelimit(self, duration: int | float):
        """Set max runtime in seconds in CPU user time"""
        return self.append_global_options("-timelimit", duration)

    def dump(self):
        """Dump each input packet"""
        return self.append_global_options("-dump")

    def hex(self):
        """When dumping packets, also dump the payload"""
        return self.append_global_options("-hex")

    def vsync(self, parameter: str):
        """Video sync method"""
        return self.append_global_options("-vsync", parameter)

    def frame_drop_threshold(self):
        """Frame drop threshold"""
        return self.append_global_options("-frame_drop_threshold")

    def async_(self):
        """Audio sync method"""
        return self.append_global_options("-async")

    def adrift_threshold(self, threshold: int | float):
        """Audio drift threshold"""
        return self.append_global_options("-adrift_threshold", threshold)

    def copyts(self):
        """Copy timestamps"""
        return self.append_global_options("-copyts")

    def start_at_zero(self):
        """Shift input timestamps to start at 0 when using copyts"""
        return self.append_global_options("-start_at_zero")

    def copytb(self, mode: Optional[int | Literal[1, 0, -1]] = None):
        """Copy input stream time base when stream copying"""
        return self.append_global_options("-copytb", mode)

    def dts_delta_threshold(self, threshold: int):
        """Timestamp discontinuity delta threshold"""
        return self.append_global_options("-dts_delta_threshold", threshold)

    def dts_error_threshold(self, threshold: int):
        """Timestamp error delta threshold"""
        return self.append_global_options("-dts_error_threshold", threshold)

    def xerror(self, error=None):
        """Exit on error"""
        return self.append_global_options("-xerror", error)

    def abort_on(self, flags: str | Literal["empty_output", "empty_output_stream"]):
        """Abort on the specified condition flags"""
        return self.append_global_options("-abort_on", flags)

    def filter_complex(self, graph_description: str):
        """Create a complex filtergraph"""
        return self.append_global_options("-filter_complex", graph_description)

    def lavfi(self, graph_description: str):
        """Create a complex filtergraph. Equivalent to -filter_complex"""
        return self.append_global_options("-lavfi", graph_description)

    def filter_complex_script(self, filename: str):
        """Read complex filtergraph description from a file"""
        return self.append_global_options("-filter_complex_script", filename)

    def auto_conversion_filters(self):
        """Enable automatic conversion filters globally"""
        return self.append_global_options("-auto_conversion_filters")

    def stats_period(self, time: Optional[int | float] = 0.5):
        """Set period at which encoding progress/statistics are updated.
        Default is 0.5 seconds.
        """
        return self.append_global_options("-stats_period", time)

    def debug_ts(self):
        """Print timestamp debugging info"""
        return self.append_global_options("-debug_ts")

    def intra(self):
        """Deprecated, use -g 1"""
        return self.append_global_options("-intra")

    def sameq(self):
        """Removed"""
        return self.append_global_options("-sameq")

    def same_quant(self):
        """Removed"""
        return self.append_global_options("-same_quant")

    def deinterlace(self):
        """This option is deprecated, use the yadif filter instead"""
        return self.append_global_options("-deinterlace")

    def psnr(self):
        """Calculate PSNR of compressed frames"""
        return self.append_global_options("-psnr")

    def vstats(self):
        """Dump video coding statistics to file"""
        return self.append_global_options("-vstats")

    def vstats_file(self, file: str):
        """Dump video coding statistics to file"""
        return self.append_global_options("-vstats_file", file)

    def vstats_version(self):
        """Version of the vstats format to use"""
        return self.append_global_options("-vstats_version")

    def qphist(self):
        """Show QP histogram"""
        return self.append_global_options("-qphist")

    def vc(self, channel: str):
        """Deprecated, use -channel"""
        return self.append_global_options("-vc", channel)

    def tvstd(self, standard: str):
        """Deprecated, use -standard"""
        return self.append_global_options("-tvstd", standard)

    def isync(self):
        """This option is deprecated and does nothing"""
        return self.append_global_options("-isync")

    def sdp_file(self, file: str):
        """Specify a file in which to print sdp information"""
        return self.append_global_options("-sdp_file", file)

    def vaapi_device(self, device: str):
        """Set VAAPI hardware device (DRM path or X11 display name)"""
        return self.append_global_options("-vaapi_device", device)

    def qsv_device(self, device: str):
        """Set QSV hardware device
        (DirectX adapter index, DRM path or X11 display name)
        """
        return self.append_global_options("-qsv_device", device)

    def init_hw_device(self, args: str):
        """Initialise hardware device"""
        return self.append_global_options("-init_hw_device", args)

    def filter_hw_device(self, device: str):
        """Set hardware device used when filtering"""
        return self.append_global_options("-filter_hw_device", device)
