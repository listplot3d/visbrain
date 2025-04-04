"""Visual objects of sleep module.

This file contains and initialize visual objects (channel plot, spectrogram,
hypnogram, indicator, shortcuts)
"""
import itertools
import logging
from pathlib import Path

import numpy as np
import scipy.signal as scpsig
from scipy.stats import rankdata

import vispy.visuals.transforms as vist
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from visbrain.config import PROFILER
from visbrain.utils import PrepareData, cmap_to_glsl, color2vb
from visbrain.utils.sleep.event import _index_to_events
from visbrain.visuals import TFmapsMesh, TopoMesh
from vispy import scene

from .marker import Markers

logger = logging.getLogger('visbrain')

__all__ = ("Visuals")


"""
###############################################################################
# OBJECTS
###############################################################################
Classes below are used to create visual objects, display on sevral canvas :
- ChannelPlot : plot data (one signal per channel)
- Spectrogram : on a specific channel
- Hypnogram : sleep stages (can be optional)
"""


class Detection(object):
    """Create a detection object."""

    def __init__(self, channels, time, spincol=None, remcol=None,
                 kccol=None, swcol=None, peakcol=None, mtcol=None,
                 spinsym=None, remsym=None, kcsym=None, swsym=None,
                 peaksym=None, mtsym=None, parent=None, parent_hyp=None):
        """Init."""
        self.items = ['Spindles', 'REM', 'K-complexes', 'Slow waves', 'Peaks',
                      'Muscle twitches']
        self.chans = channels
        self.dict = {}
        self.line = {}
        self.peaks = {}
        self.seg = {}
        col = {'Spindles': spincol, 'REM': remcol, 'K-complexes': kccol,
               'Slow waves': swcol, 'Peaks': peakcol, 'Muscle twitches': mtcol}
        sym = {'Spindles': spinsym, 'REM': remsym, 'K-complexes': kcsym,
               'Slow waves': swsym, 'Peaks': peaksym, 'Muscle twitches': mtsym}
        self.time = time
        self.hyp = Markers(parent=parent_hyp)
        self.hyp.set_gl_state('translucent')
        for num, k in enumerate(self):
            self[k] = {'index': np.array([]), 'color': col[k[1]],
                       'connect': np.array([]), 'sym': sym[k[1]]}
            par = parent[self.chans.index(k[0])]
            if k[1] != 'Peaks':
                self.line[k] = scene.visuals.Line(method='gl', parent=par,
                                                  color=col[k[1]])
                self.line[k].set_gl_state('translucent')
            else:
                pos = np.full((1, 3), -10., dtype=np.float32)
                self.peaks[k] = Markers(pos=pos, parent=par,
                                        face_color=col[k[1]])
                self.peaks[k].set_gl_state('translucent')

    def __iter__(self):
        it = itertools.product(self.chans, self.items)
        for k in it:
            yield k

    def __bool__(self):
        return any([bool(self[k]['index'].size) for k in self])

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, key):
        return self.dict[key]

    def build_line(self, data):
        """Build detections reports.

        Parameters
        ----------
        data : array_like
            Data vector for a spcefic channel.
        """
        for num, k in enumerate(self):
            if self[k]['index'].size:
                # Get the channel number :
                nb = self.chans.index(k[0])
                # Send data :
                if k[1] == 'Peaks':
                    # Get index and channel number :
                    index = self[k]['index'][:, 0]
                    z = np.full(len(index), 2., dtype=np.float32)
                    pos = np.vstack((self.time[index], data[nb, index], z)).T
                    self.peaks[k].set_data(pos=pos, edge_width=0.,
                                           face_color=self[k]['color'])
                else:
                    # Get index and channel number :
                    index = _index_to_events(self[k]['index'])
                    z = np.full(index.shape, 2., dtype=np.float32)
                    # Build position vector :
                    pos = np.vstack((self.time[index], data[nb, index], z)).T
                    # Build connections :
                    connect = np.gradient(index) == 1.
                    connect[0], connect[-1] = True, False
                    self.line[k].set_data(pos=pos, width=4., connect=connect)

    def build_hyp(self, chan, types):
        """Build hypnogram report.

        Parameters
        ----------
        chan : str
            String name of the channel.
        types : str
            String name of the detection type.
        """
        # Get index :
        index = self[(chan, types)]['index']
        # Get only starting points :
        start = index[:, 0]
        y = np.full_like(start, 1.5, dtype=float)
        z = np.full_like(start, -2., dtype=float)
        pos = np.vstack((self.time[start], y, z)).T
        # Set hypnogram data :
        self.hyp.set_data(pos=pos, symbol=self[(chan, types)]['sym'],
                          face_color=self[(chan, types)]['color'],
                          edge_width=1.,
                          edge_color=self[(chan, types)]['color'])

    def visible(self, viz, chan, types):
        """Set channel visibility.

        Parameters
        ----------
        viz : bool
            Boolean value indicating if the plot have to be displayed.
        chan : str
            Channel name.
        types : str
            Detection type name.
        """
        self.hyp.visible = viz
        if types == 'Peaks':
            self.peaks[(chan, types)].visible = viz
        else:
            self.line[(chan, types)].visible = viz

    def delete(self, chan, types):
        """Delete data of a channel."""
        # Remove data from dict :
        self[(chan, types)]['index'] = np.array([])
        # Remove data from plot :
        pos = np.full((1, 3), -10., dtype=np.float32)
        if types == 'Peaks':
            self.peaks[(chan, types)].set_data(pos=pos)
        else:
            self.line[(chan, types)].set_data(pos=pos,
                                              connect=np.array([False]))
        # Remove data from hypnogram :
        self.hyp.set_data(pos=pos)

    def nonzero(self):
        """Return the list of channels with non-empty detections."""
        chans = {}
        for k in self.chans:
            types = []
            for i in self.items:
                if self[(k, i)]['index'].size:
                    types.append(i)
            if types:
                chans[k] = types
        return chans

    def update_keys(self, newkeys):
        """Update the keys of dictionaries."""
        # Get old keys :
        oldkeys = list(self.dict.keys())
        # Check that new keys lentgh has the same size as old keys :
        if len(newkeys) != len(self.chans):
            raise ValueError("The length of new keys must be the same as old"
                             "keys")
        for k in oldkeys:
            # Find index of channel :
            idx = self.chans.index(k[0])
            # Build new key :
            nkey = (newkeys[idx], k[1])
            # Update keys (if needed):
            if nkey not in oldkeys:
                # Update dict and line :
                self.dict[nkey] = self.dict[k]
                if k[1] == 'Peaks':
                    self.peaks[nkey] = self.peaks[k]
                    del self.peaks[k]
                else:
                    self.line[nkey] = self.line[k]
                    del self.line[k]
                # Remove old key :
                del self.dict[k]
        self.chans = newkeys

    def reset(self):
        """Reset all detections."""
        for k in self:
            self[k]['index'] = np.array([])


class ChannelPlot(PrepareData):
    """Plot each channel."""

    def __init__(self, channels, time, color=(.2, .2, .2), width=1.5,
                 color_detection='red', method='gl', camera=None,
                 parent=None, fcn=None):
        # Initialize PrepareData :
        PrepareData.__init__(self, axis=1)

        # Variables :
        self._camera = camera
        self._preproc_channel = -1
        self.rect = []
        self.width = width
        self.autoamp = False
        self._fcn = fcn
        self.visible = np.array([True] + [False] * (len(channels) - 1))
        self.consider = np.ones((len(channels),), dtype=bool)

        # Get color :
        self.color = color2vb(color)
        self.color_detection = color2vb(color_detection)

        # Create one line per channel :
        pos = np.zeros((1, 3), dtype=np.float32)
        self.mesh, self.report, self.grid, self.peak, self.scorwin_ind, self.hyp_overlay = \
            [], [], [], [], [], []
        self.loc, self.node = [], []
        for i, k in enumerate(channels):
            # ----------------------------------------------
            # Create a node parent :
            node = scene.Node(name=k + 'plot')
            node.parent = parent[i].wc.scene
            self.node.append(node)

            # ----------------------------------------------
            # Create main line (for channel plot) :
            mesh = scene.visuals.Line(pos, name=k + 'plot', color=self.color,
                                      method=method, parent=node)
            mesh.set_gl_state('translucent')
            self.mesh.append(mesh)

            # ----------------------------------------------
            # Create marker peaks :
            mark = Markers(pos=np.zeros((1, 3), dtype=np.float32),
                           parent=node)
            mark.set_gl_state('translucent')
            mark.visible = False
            self.peak.append(mark)

            # ----------------------------------------------
            # Locations :
            loc = scene.visuals.Line(pos, name=k + 'location', method=method,
                                     color=(.1, .1, .1, .3), parent=node,
                                     connect='segments')
            loc.set_gl_state('translucent')
            self.loc.append(loc)

            # ----------------------------------------------
            # Create a grid :
            grid = scene.visuals.GridLines(color=(.1, .1, .1, .5),
                                           scale=(1., .1),
                                           parent=parent[i].wc.scene)
            grid.set_gl_state('translucent')
            self.grid.append(grid)

            # ----------------------------------------------
            # Create a scoring window indicator :
            scorwin_ind = ScorWinIndicator(parent=node,
                                           name=k + '_scorwin_ind',
                                           visible=True)
            self.scorwin_ind.append(scorwin_ind)

            # ----------------------------------------------
            # Create a HypnoOverlay to display hypno colors onto signal :
            hyp_overlay = HypnoOverlay(
                parent=node,
                name=k + '_hyp_overlay',
                visible=True,
                time=time,
            )
            self.hyp_overlay.append(hyp_overlay)

    def __iter__(self):
        """Iterate over visible mesh."""
        for i, k in enumerate(self.mesh):
            if self.visible[i]:
                yield i, k

    def __len__(self):
        """Return the number of channels."""
        return len(self.mesh)

    def set_data(self, sf, data, time, sl=None, ylim=None, autoamp=True):
        """Set data to channels.

        Parameters
        ----------
        data: array_like
            Array of data of shape (n_channels, n_points)
        time: array_like
            The time vector.
        sl : slice | None
            A slice object for the time selection of data.
        ylim : array_like | None
            Y-limits of each channel. Must be a (n_channels, 2) array.
        """
        if ylim is None:
            ylim = np.array([data.min(1), data.max(1)]).T

        # Manage slice :
        sl = slice(0, data.shape[1]) if sl is None else sl

        # Slice selection (of time and data) :
        time_sl = time[sl]
        self.x = (time_sl.min(), time_sl.max())
        data_sl = data[self.visible, sl]
        z = np.full_like(time_sl, .5, dtype=np.float32)

        # Prepare the data (only if needed) :
        if self:
            if self._preproc_channel == -1:  # prepare all channels
                data_sl = self._prepare_data(sf, data_sl.copy(), time_sl)
            else:  # filt only one channel
                # Get on which visible channel to apply preprocessing :
                chan_lst_viz = list(np.arange(len(self))[self.visible])
                to_chan = chan_lst_viz.index(self._preproc_channel)
                data_sl[[to_chan], :] = self._prepare_data(sf, data_sl[
                    [to_chan], :].copy(), time_sl)

        # Set data to each plot :
        for l, (i, k) in enumerate(self):
            # ________ MAIN DATA ________
            # Select channel ;
            datchan = data_sl[l, :]

            # Concatenate time / data / z axis :
            dat = np.vstack((time_sl, datchan, z)).T

            # Set main ligne :
            k.set_data(dat, width=self.width)

            # ________ CAMERA ________
            # Use either auto / fixed adaptative camera :
            ycam = (datchan.min(), datchan.max()) if self.autoamp else ylim[i]

            # Get camera rectangle and set it:
            rect = (self.x[0], ycam[0], self.x[1] - self.x[0],
                    ycam[1] - ycam[0])
            self._camera[i].rect = rect
            k.update()
            self.rect.append(rect)

    def set_location(self, sf, data, channel, start, end, factor=100.):
        """Set vertical lines for detections."""
        # Get data limits :
        y = (data.min(), data.max())
        # # Build pos :
        pos = np.zeros((4, 3), dtype=np.float32)
        pos[0, 0:2] = [start, y[0]]
        pos[1, 0:2] = [start, y[1]]
        pos[2, 0:2] = [end, y[0]]
        pos[3, 0:2] = [end, y[1]]
        # Set data pos :
        self.loc[channel].set_data(pos=pos, width=2.)

    def clean(self):
        """Clean all the data."""
        # Empty position :
        pos = np.zeros((1, 3), dtype=np.float32)
        for k in range(len(self)):
            # Main mesh :
            self.mesh[k].set_data(pos=pos, color='gray')
            self.mesh[k].parent = None
            # Report :
            self.report[k].set_data(pos=pos, color='gray')
            self.report[k].parent = None
            # Grid :
            self.grid[k].parent = None
            # Peak locations :
            self.peak[k].set_data(pos=pos, face_color='gray')
            self.peak[k].parent = None
            # Vertical lines :
            self.loc[k].set_data(pos=pos, color='gray')
            self.loc[k].parent = None
        self.mesh, self.report, self.grid, self.peak = [], [], [], []
        self.loc = []

    # ----------- PARENT -----------
    @property
    def parent(self):
        """Get the parent value."""
        return self.mesh[0].parent

    @parent.setter
    def parent(self, value):
        """Set parent value."""
        for i, k, in zip(value, self.mesh):
            k.parent = i.wc.scene

    # ----------- AUTOAMP -----------
    @property
    def autoamp(self):
        """Get the autoamp value."""
        return self._autoamp

    @autoamp.setter
    def autoamp(self, value):
        """Set autoamp value."""
        self._autoamp = value


class Spectrogram(PrepareData):
    """Create and manage a Spectrogram object.

    After object creation, use the set_data() method to pass new data, new
    color, new frequency / time range, new settings...
    """

    def __init__(self, camera, parent=None, fcn=None):
        # Initialize PrepareData :
        PrepareData.__init__(self, axis=0)

        # Keep camera :
        self._camera = camera
        self._rect = (0., 0., 0., 0.)
        self._fcn = fcn

        # Time-frequency map
        self.tf = TFmapsMesh(parent=parent)
        # Spectrogram
        self.mesh = scene.visuals.Image(np.zeros((2, 2)), parent=parent,
                                        name='Fourier transform')
        self.mesh.transform = vist.STTransform()

    def set_data(self, sf, data, time, method='Fourier transform',
                 cmap='rainbow', nfft=30., overlap=0., fstart=.5, fend=20.,
                 contrast=.5, interp='nearest', norm=0):
        """Set data to the spectrogram.

        Use this method to change data, colormap, spectrogram settings, the
        starting and ending frequencies.

        Parameters
        ----------
        sf: float
            The sampling frequency.
        data: array_like
            The data to use for the spectrogram. Must be a row vector.
        time: array_like
            The time vector.
        method: string | 'Fourier transform'
            Computation method.
        cmap : string | 'viridis'
            The matplotlib colormap to use.
        nfft : float | 30.
            Number of fft points for the spectrogram (in seconds).
        overlap : float | .5
            Ovelap proprotion (0 <= overlap <1).
        fstart : float | .5
            Frequency from which the spectrogram have to start.
        fend : float | 20.
            Frequency from which the spectrogram have to finish.
        contrast : float | .5
            Contrast of the colormap.
        interp : string | 'nearest'
            Interpolation method.
        norm : int | 0
            Normalization method for TF.
        """
        # =================== PREPARE DATA ===================
        # Prepare data (only if needed)
        if self:
            data = self._prepare_data(sf, data.copy(), time)

        nperseg = int(round(nfft * sf))

        # =================== TF // SPECTRO ===================
        if method == 'Wavelet':
            self.tf.set_data(data, sf, f_min=fstart, f_max=fend, cmap=cmap,
                             contrast=contrast, n_window=nperseg,
                             overlap=overlap, window='hamming', norm=norm)
            self.tf._image.interpolation = interp
            self.rect = self.tf.rect
            self.freq = self.tf.freqs
        else:
            # =================== CONVERSION ===================
            overlap = int(round(overlap * nperseg))

            if method == 'Multitaper':
                from lspopt import spectrogram_lspopt
                freq, _, mesh = spectrogram_lspopt(data, fs=sf,
                                                   nperseg=nperseg,
                                                   c_parameter=20,
                                                   noverlap=overlap)
            elif method == 'Fourier transform':
                freq, _, mesh = scpsig.spectrogram(data, fs=sf,
                                                   nperseg=nperseg,
                                                   noverlap=overlap,
                                                   window='hamming')
            mesh = 20 * np.log10(mesh)

            # =================== FREQUENCY SELECTION ===================
            # Find where freq is [fstart, fend] :
            f = [0., 0.]
            f[0] = np.abs(freq - fstart).argmin() if fstart else 0
            f[1] = np.abs(freq - fend).argmin() if fend else len(freq)
            # Build slicing and select frequency vector :
            sls = slice(f[0], f[1] + 1)
            freq = freq[sls]
            self._fstart, self._fend = freq[0], freq[-1]

            # =================== COLOR ===================
            # Get clim :
            _mesh = mesh[sls, :]
            is_finite = np.isfinite(_mesh)
            _mesh[~is_finite] = np.percentile(_mesh[is_finite], 5)
            contrast = 1. if contrast is None else contrast
            clim = (contrast * _mesh.min(), contrast * _mesh.max())
            # Turn mesh into color array for selected frequencies:
            self.mesh.set_data(_mesh)
            _min, _max = _mesh.min(), _mesh.max()
            _cmap = cmap_to_glsl(limits=(_min, _max), clim=clim, cmap=cmap)
            self.mesh.cmap = _cmap
            self.mesh.clim = 'auto'
            self.mesh.interpolation = interp

            # =================== TRANSFORM ===================
            tm, th = time.min(), time.max()
            # Re-scale the mesh for fitting in time / frequency :
            fact = (freq.max() - freq.min()) / len(freq)
            sc = (th / mesh.shape[1], fact, 1)
            tr = [0., freq.min(), 0.]
            self.mesh.transform.translate = tr
            self.mesh.transform.scale = sc
            # Update object :
            self.mesh.update()
            # Get camera rectangle :
            self.rect = (tm, freq.min(), th - tm, freq.max() - freq.min())
            self.freq = freq
        # Visibility :
        self.mesh.visible = 0 if method == 'Wavelet' else 1
        self.tf.visible = 1 if method == 'Wavelet' else 0

    def clean(self):
        """Clean indicators."""
        pos = np.zeros((3, 4), dtype=np.float32)
        self.mesh.set_data(pos)
        self.mesh.parent = None
        self.mesh = None

    # ----------- RECT -----------
    @property
    def rect(self):
        """Get the rect value."""
        return self._rect

    @rect.setter
    def rect(self, value):
        """Set rect value."""
        self._rect = value
        self._camera.rect = value

    # ----------- INTERP -----------
    @property
    def interp(self):
        """Get the interp value."""
        return self._interp

    @interp.setter
    def interp(self, value):
        """Set interp value."""
        self._interp = value
        self.mesh.interpolation = value
        self.mesh.update()
        self.tf.interpolation = value
        self.tf.update()


class Hypnogram(object):
    """Create a hypnogram object."""

    def __init__(self, time, camera, width=2., hcolors=None, hvalues=None,
                 hYranks=None, parent=None):
        # Keep camera :
        self._camera = camera
        # Display Y position for each of the vigilance state values:
        # 0 (first, top) to -(n-1) (last, bottom)
        self.hYpos = {
            value: -float(rank)
            for value, rank in zip(
                hvalues,
                rankdata(hYranks) - 1  # rankdata is 1-indexed
            )
        }
        # Camera rectangle. yPos are 0 to -(nstates - 1)
        self._rect = (0., 0., 0., 0.)
        self.rect = (time.min(), -len(hvalues),
                     time.max() - time.min(), len(hvalues) + 1)
        self.width = width
        self.n = len(time)
        # Color for each of the vigilance state value
        self._hcolors = {
            value: color2vb(color=col)
            for value, col in zip(hvalues, hcolors)
        }  # Display color per vigilance state: {int: (1,4)-nparray}
        # Create a default line :
        pos = np.array([[0, 0], [0, 100]])
        self.mesh = scene.visuals.Line(pos, name='hypnogram', method='gl',
                                       parent=parent, width=width)
        self.mesh._width = width
        self.mesh.set_gl_state('translucent')
        # Create a default marker (for edition):
        self.edit = Markers(parent=parent)
        # self.mesh.set_gl_state('translucent', depth_test=True)
        self.edit.set_gl_state('translucent')
        # Add grid :
        self.grid = scene.visuals.GridLines(color=(.7, .7, .7, 1.),
                                            scale=(30. * time[-1] / len(time),
                                                   1.),
                                            parent=parent)
        self.grid.set_gl_state('translucent')

    def __len__(self):
        """Return the time length."""
        return self.n

    # -------------------------------------------------------------------------
    # SETTING METHODS
    # -------------------------------------------------------------------------
    def set_data(self, sf, data, time):
        """Set data to the hypnogram.

        Parameters
        ----------
        sf: float
            The sampling frequency.
        data: array_like
            Vigilance state values to sent. Must be a row vector.
        time: array_like
            The time vector
        """
        data_pos = np.array([self.hYpos[v] for v in data])
        # Build color array: (nsamples, 4)-nparray
        data_colors = np.array([self.hcolors[v] for v in data]).squeeze()
        # Set data to the mesh :
        self.mesh.set_data(pos=np.vstack((time, data_pos)).T,
                           width=self.width, color=data_colors)
        self.mesh.update()

    def set_state(self, stfrom, stend, value):
        """Add a vigilance state in a specific interval.

        This method only set the vigilance state without updating the entire
        hypnogram.

        Parameters
        ----------
        stfrom : int
            The index where the state start.
        stend : int
            The index where the state end.
        value : int
            State value.
        """
        state_ypos = self.hYpos[value]
        # Update color :
        self.mesh.color[stfrom + 1:stend + 1, :] = self.hcolors[value]
        # Only update the needed part :
        self.mesh.pos[stfrom:stend, 1] = state_ypos
        self.mesh.update()

    def set_grid(self, time, length=30., y=1.):
        """Set grid lentgh."""
        # Get scaling factor :
        sc = (length * time[-1] / len(time), y)
        # Set to the grid :
        self.grid._grid_color_fn['scale'].value = sc
        self.grid.update()

    # -------------------------------------------------------------------------
    # CONVERSION METHODS
    # -------------------------------------------------------------------------
    def hyp_to_gui(self, data):
        """Convert hypnogram data to Y position on the GUI

        Parameters
        ----------
        data : array_like
            The data to send. Must be a row vector.

        Returns
        -------
        data_rank : array_like
        """
        return np.array([self.hYpos[v] for v in data])

    def gui_to_hyp(self):
        """Convert GUI hypnogram Y positions into hypnogram state values.

        Returns
        -------
        data : array_like
            The converted data.
        """
        # Get latest data version :
        data_ypos = self.mesh.pos[:, 1]
        # Value from Y position
        hYpos_inv = {
            pos: value for value, pos in self.hYpos.items()
        }
        return np.array([hYpos_inv[r] for r in data_ypos])

    def clean(self, sf, time):
        """Clean indicators."""
        # Mesh :
        posmesh = np.zeros((len(self),), dtype=np.float32)
        self.set_data(sf, posmesh, time)
        # Edit :
        posedit = np.full((1, 3), -10., dtype=np.float32)
        self.edit.set_data(pos=posedit, face_color='gray')

    # ----------- Properties -----------
    @property
    def rect(self):
        """Get the rect value."""
        return self._rect

    @rect.setter
    def rect(self, value):
        """Set rect value."""
        self._rect = value
        self._camera.rect = value

    @property
    def hcolors(self):
        """Return {value: (4,1)-array} hypnogram colors map."""
        return self._hcolors

    @hcolors.setter
    def hcolors(self, value):
        """Set new {value: (4,1)-array} hypnogram colors map and redraw hyp"""
        self._hcolors = value
        # Redraw hypnogram
        hdata = self.gui_to_hyp()  # (nsamples,1) array
        data_colors = np.array([self.hcolors[v] for v in hdata]).squeeze()
        self.mesh.set_data(color=data_colors)
        self.mesh.update()


"""
###############################################################################
# TOPOPLOT
###############################################################################
Topoplot class that inherit from the visual TopoMesh and PrepareData for
filetring, de-meaning...
"""


class TopoSleep(TopoMesh, PrepareData):
    """Topoplot for sleep data."""

    def __init__(self, **kwargs):
        # Initialize TopoMesh and PrepareData :
        TopoMesh.__init__(self, **kwargs)
        PrepareData.__init__(self, axis=1)
        # Initialize data, clim, cmap and cblabel :
        self._data = None
        self._clim = None
        self._cmap = None
        self._cblabel = None

    def set_sleep_topo(self, data=None, clim=None, cmap=None, cblabel=None):
        """Send data to TopoGraphic plot."""
        # Data :
        if data is None:
            data = self._data
        self._data = data
        # Clim :
        if clim is None:
            clim = self._clim
        self._clim = clim
        # Cmap :
        if cmap is None:
            cmap = self._cmap
        self._cmap = cmap
        # Cblabel :
        if cblabel is None:
            cblabel = self._cblabel
        self._cblabel = cblabel

        if data is not None:
            self.set_data(data, cmap=cmap, cblabel=cblabel, clim=clim)


"""
###############################################################################
# INDICATORS
###############################################################################
Visual indicators can be used to help the user to see in which time window the
signal is currently plotted. Those indicators are two vertical lines displayed
on the spectrogram and hypnogram.
"""


class Indicator(object):
    """Create a visual indicator (for spectrogram and hypnogram)."""

    def __init__(self, name='indicator', alpha=.3, visible=True, parent=None):
        # Create a vispy image object :
        image = color2vb('gray', alpha=alpha)[np.newaxis, ...]
        self.mesh = scene.visuals.Image(data=image, name=name,
                                        parent=parent)
        self.mesh.transform = vist.STTransform()
        self.mesh.visible = visible

    def set_data(self, xlim, ylim):
        """Move the visual indicator.

        Parameters
        ----------
        xlim : tuple
            A tuple of two float indicating where xlim start and xlim end.
        ylim : tuple
            A tuple of two floats indicating where ylim start and ylim end.
        """
        tox = (xlim[0], ylim[0], -1.)
        sc = (xlim[1] - xlim[0], ylim[1] - ylim[0], 1.)
        # Move the square
        self.mesh.transform.translate = tox
        self.mesh.transform.scale = sc

    def clean(self):
        """Clean indicators."""
        self.mesh.parent = None
        self.mesh = None


"""
###############################################################################
# SCORING WINDOW INDICATOR
###############################################################################
The scoring window indicators can be used to show the limits of the current
scoring window on each of the channel plots. On each of the channel plots, the
scoring window indicator consists in two vertical bars marking the start and
end of the window
"""


class ScorWinIndicator(object):
    """Create a visual indicator of scoring window (for channel plots)."""

    def __init__(self, name='scorwinindicator', alpha=.75, visible=True,
                 parent=None, color='red', barwidth=.20):
        # width of the vertical bars
        self.barwidth = barwidth
        # Create two vispy image object for the start and end of window
        # "Start mesh" : first vertical bar
        image_start = color2vb(color, alpha=alpha)[np.newaxis, ...]
        self.mesh_start = scene.visuals.Image(data=image_start, name=name,
                                              parent=parent)
        self.mesh_start.transform = vist.STTransform()
        self.mesh_start.visible = visible
        # "End mesh" : second vertical bar
        image_end = color2vb(color, alpha=alpha)[np.newaxis, ...]
        self.mesh_end = scene.visuals.Image(data=image_end, name=name,
                                            parent=parent)
        self.mesh_end.transform = vist.STTransform()
        self.mesh_end.visible = visible

    def set_data(self, x_start, x_end, ylim, barwidth=None):
        """Redraw the vertical bars

        Parameters
        ----------
        x_start: float
            A float indicating where the "start" bar is centered
        x_end: float
            A float indicating where the "end" bar is centered
        ylim : tuple
            A tuple of two floats indicating the vertical limits of both bars
        barwidth: float
            A float indicating the new width of the indicator bars
        """
        # Change barwidth
        if barwidth is not None:
            self.barwidth = barwidth
        # xlim of each bar
        xlim_start = (x_start - self.barwidth / 2, x_start + self.barwidth / 2)
        xlim_end = (x_end - self.barwidth / 2, x_end + self.barwidth / 2)
        # Displacement for each bar
        tox_start = (xlim_start[0], ylim[0], -1.)
        sc_start = (xlim_start[1] - xlim_start[0], ylim[1] - ylim[0], 1.)
        tox_end = (xlim_end[0], ylim[0], -1.)
        sc_end = (xlim_end[1] - xlim_end[0], ylim[1] - ylim[0], 1.)
        # Move the two bars
        self.mesh_start.transform.translate = tox_start
        self.mesh_start.transform.scale = sc_start
        self.mesh_end.transform.translate = tox_end
        self.mesh_end.transform.scale = sc_end

    def clean(self):
        """Clean indicators."""
        self.mesh_start.parent = None
        self.mesh_start = None
        self.mesh_end.parent = None
        self.mesh_end = None


"""
###############################################################################
# Hypno overlay
###############################################################################
Display hypnogram colors onto signal data.
"""


class HypnoOverlay(object):
    """Create a colored overlay on signal data."""

    def __init__(self, time=None, name='hyp_overlay', alpha=.3, visible=True, parent=None):

        self.alpha = alpha

        # Create a vispy image object :
        assert time is not None
        pos = np.zeros((len(time), 1), dtype=np.float32)
        pos[:, 0] = time
        color = np.zeros((len(time), 4), dtype=np.float32)
        self.region = scene.visuals.LinearRegion(
            pos=time, color=color,
            vertical=True,
            name=name, parent=parent,
        )
        self.region.visible = visible
        self.region.update()

    def set_data(self, data_colors):
        """Set data to the hypnogram indicator.

        Parameters
        ----------
        data_colors (ndarray): (nsamples, 4) array of RGBA colors
        """
        assert data_colors.shape[1] == 4
        self.region.set_data(
            color=data_colors
        )
        self.region.update()
    
    def clean(self):
        """Clean indicators."""
        self.region.parent = None
        self.region = None


"""
###############################################################################
# VIDEO
###############################################################################
Display synced video
"""


class VideoSleep(object):

    def __init__(self, filepath, offset, playerW=None, titleW=None, playW=None,
                 sliderW=None, infoW=None, offsetW=None, loadW=None):

        self._filepath = filepath
        # Inherit
        self._videoPlayerW = playerW
        self._videoTitleW = titleW
        self._videoPlayW = playW
        self._videoSliderW = sliderW
        self._videoInfoW = infoW
        self._videoOffsetW = offsetW
        self._videoLoadW = loadW

        self._duration = None  # (s). Set once loaded
        self._offset = offset if offset is not None else 0
        self._videoOffsetW.setValue(self._offset)

        self._loaded = False

        if self.filepath is None:
            self._videoTitleW.setText("No video file provided.")
            self._disable_widgets()
            return

        # Initialize media player
        self._mediaPlayer = QMediaPlayer()
        self._mediaPlayer.durationChanged.connect(self._on_loaded)
        self._mediaPlayer.error.connect(self._on_error)
        self._mediaPlayer.setVideoOutput(self._videoPlayerW)
        self._mediaPlayer.positionChanged.connect(self._on_positionChanged)
        self._mediaPlayer.setNotifyInterval(500)
        self._videoSliderW.valueChanged.connect(self._on_sliderMoved)
        self._videoPlayW.clicked.connect(self.toggle_play_pause)
        self._videoLoadW.clicked.connect(self._on_load_click)

        # Set proper aspect ratio (works only with hack https://stackoverflow.com/a/51736245/7355898) # noqa
        self._videoPlayerW.setAspectRatioMode(Qt.KeepAspectRatio)

        # Load vid
        self._load_file()
        self._mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(filepath))
        )

    def _on_load_click(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setWindowTitle('Select video file.')
        dialog.setNameFilter('Video files (*.*)')
        if self.filepath is None:
            dialog.setDirectory(QDir.currentPath())
        else:
            dialog.setDirectory(str(Path(self.filepath).parent))
        dialog.setFileMode(dialog.ExistingFile)
        if dialog.exec_() == dialog.Accepted:
            self.filepath = str(dialog.selectedFiles()[0])
            self._load_file()

    def _load_file(self):
        self._loaded = False
        self._videoOffsetW.setEnabled(True)
        self._videoPlayW.setEnabled(True)
        self._videoSliderW.setEnabled(False)
        self._mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(self.filepath))
        )
        dir = Path(self.filepath).parents[0].name
        name = Path(self.filepath).name
        self._videoTitleW.setText(f"{dir} / {name}")
        self._on_positionChanged()
        # I don't know why this is not called
        if not self._mediaPlayer.duration() == 0:
            self._on_loaded()

    def _disable_widgets(self):
        self._videoOffsetW.setEnabled(False)
        self._videoPlayW.setEnabled(False)
        self._videoSliderW.setEnabled(False)
        self._videoInfoW.setText("")

    def _on_loaded(self):
        # Update file info once the file is loaded
        self._loaded = True
        self._duration = self._mediaPlayer.duration() / 1000  # 0 before loaded
        self._videoSliderW.setMaximum(self._duration)
        self._videoSliderW.setEnabled(True)
        # Update txt info
        self._on_positionChanged()

    def _on_error(self):
        self._disable_widgets()
        error_msg = (
            f"Error loading video at {self.filepath} in QMediaPlayer, "
            f"error_code={self._mediaPlayer.error()}, "
            f"error_string: {self._mediaPlayer.errorString()}"
        )
        self._videoTitleW.setText(error_msg)
        import warnings
        import sys
        warnings.warn(error_msg)
        sys.stderr.flush()

    def _on_sliderMoved(self):
        assert self._loaded  # Slider should be disabled before then
        # It's user who's moving the slider
        # if self._videoSliderW.isSliderDown():
        self._mediaPlayer.setPosition(self._videoSliderW.value() * 1000)

    def _on_positionChanged(self):
        # Info
        currentTime = round(self._mediaPlayer.position() / 1000, 1)
        if not self._loaded:
            txt = f"{currentTime} / ??? (s) (Loading)"
        else:
            txt = f"{currentTime} / {round(self._duration, 1)} (s)"
        self._videoInfoW.setText(txt)
        # Update cursor once we know total run time
        if self._loaded:
            # Don't call callback to avoid being pulled back
            self._videoSliderW.blockSignals(True)
            self._videoSliderW.setValue(
                self._mediaPlayer.position() / 1000
            )
            self._videoSliderW.blockSignals(False)

    def toggle_play_pause(self):
        # Currently playing:
        if self._mediaPlayer.state() == self._mediaPlayer.PlayingState:
            self.pause()
        # Currently not playing
        else:
            self.play()

    def play(self):
        # Resize after play ( https://stackoverflow.com/a/51736245/7355898 )
        from PyQt5.QtCore import QSize
        s1 = self._videoPlayerW.size()
        s2 = s1 + QSize(1, 1)
        self._mediaPlayer.play()
        self._videoPlayerW.resize(s2)  # enlarge by one pixel
        self._videoPlayerW.resize(s1)  # return to original size
        self._videoPlayW.setText('Pause')

    def pause(self):
        # Resize after play ( https://stackoverflow.com/a/51736245/7355898 )
        from PyQt5.QtCore import QSize
        s1 = self._videoPlayerW.size()
        s2 = s1 + QSize(1, 1)
        self._mediaPlayer.pause()
        self._videoPlayerW.resize(s2)  # enlarge by one pixel
        self._videoPlayerW.resize(s1)  # return to original size
        self._videoPlayW.setText('Play')

    @property
    def offset(self):
        return self._videoOffsetW.value()

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value
        self._load_file()
        self.pause()

    def set_video_time(self, gui_time):
        if self._loaded:
            video_time = (gui_time + self.offset)  # (s)
            if video_time >= 0 and video_time <= self._duration:
                self.play()
                self._mediaPlayer.setPosition(
                    video_time * 1000
                )
                self.pause()


"""
###############################################################################
# SHORTCUTS
###############################################################################
Shortcuts applied on each canvas.
"""


class CanvasShortcuts(object):
    """This class add some shortcuts to the main canvas.

    It's also use to initialize to panel of shortcuts.

    Parameters
    ----------
    axiscanvas : `AxisCanvas`
        `AxisCanvas` object with embedded axis.
        Must contain `canvas` attribute containing the vispy canvas to add the
        shortcuts to.
    """

    def __init__(self, axiscanvas):
        """Init."""
        # Get axiscanvas as arg because we also need axiscanvas.wc
        canvas = axiscanvas.canvas

        # Hardcoded shortcuts
        sh = [
            ('n', 'Go to the next window'),
            ('b', 'Go to the previous window'),
            ('-', 'Decrease amplitude'),
            ('+', 'Increase amplitude'),
            ('s', 'Display / hide spectrogram'),
            ('t', 'Display / hide topoplot'),
            ('h', 'Display / hide hypnogram'),
            ('p', 'Display / hide navigation bar'),
            ('x', 'Display / hide time axis'),
            ('g', 'Display / hide time grid'),
            ('v', 'Display / hide video'),
            ('z', 'Enable / disable zooming'),
            ('i', 'Enable / disable indicators'),
            ('Double clik', 'Insert annotation'),
            ('CTRL + left click', 'Magnify signal under the cursor'),
            ('CTRL + Num', 'Display the channel Num'),
            ('CTRL + s', 'Save hypnogram'),
            ('CTRL + t', 'Display shortcuts'),
            ('CTRL + e', 'Display documentation'),
            ('CTRL + d', 'Display / hide setting panel'),
            ('CTRL + n', 'Take a screenshot'),
            ('CTRL + q', 'Close Sleep graphical interface'),
        ]
        # Check and add flexible scoring shortcuts
        other_sh = [s for s, _ in sh]
        if any([scoring_sh in other_sh for scoring_sh in self._hshortcuts]):
            raise ValueError(
                "One of the user-defined shortcuts for scoring is reserved. "
                "Please select another key in vigilance state config. \n\n"
                f"User-defined scoring keys: {self._hshortcuts}\n"
                f"Reserved keys: {other_sh}"
            )
        if not all([len(sh) == 1 for sh in self._hshortcuts]):
            raise ValueError(
                "Please use only simple keys as scoring shortcuts. \n\n"
                f"User-defined scoring keys: {self._hshortcuts}\n"
            )
        self.sh = [
            (f"'{sh}'", f"Scoring: set current window to {state} ({value})")
            for sh, state, value in zip(
                self._hshortcuts, self._hstates, self._hvalues
            )
        ] + sh

        # Add shortcuts to vbCanvas :
        @canvas.events.key_press.connect
        def on_key_press(event):
            """Executed function when a key is pressed on a keyboard over canvas.

            :event: the trigger event
            """
            if event.text == ' ':
                pass

            # ------------ SLIDER ------------
            elif event.text.lower() == 'n':  # Next (slider)
                self._SlGoto.setValue(
                    self._SlGoto.value() + self._SigStep.value())
            elif event.text.lower() == 'b':  # Before (slider)
                self._SlGoto.setValue(
                    self._SlGoto.value() - self._SigStep.value())

            # ------------ AMPLITUDE ------------
            elif event.text in ['-', '+']:  # Decrease / increase amplitude
                delta = 2.5
                sign = 2 * ['-', '+'].index(event.text) - 1
                if self._PanAmpSym.isChecked():  # Symetric amplitudes :
                    val_sym = self._PanAllAmpMax.value() - 2 * sign * delta
                    self._PanAllAmpMax.setValue(val_sym)
                else:  # non-symetrical amplitudes
                    for mi, ma in zip(self._yminSpin, self._ymaxSpin):
                        mi.setValue(mi.value() + sign * delta)
                        ma.setValue(ma.value() - sign * delta)

            # ------------  GRID/MAGNIFY ------------
            elif event.text.lower() == 'm':  # Magnify
                viz = self._slMagnify.isChecked()
                self._slMagnify.setChecked(not viz)
                self._fcn_slider_magnify()

            elif event.text.lower() == 'g':  # Grid
                viz = self._slGrid.isChecked()
                self._slGrid.setChecked(not viz)
                self._fcn_grid_toggle()

            # ------------ SCORING ------------
            else:
                for sh, state, value in zip(
                    self._hshortcuts, self._hstates, self._hvalues
                ):
                    if event.text.lower() == sh.lower():
                        self._add_stage_on_scorwin(value)
                        # Move window so that next ScorWin starts where we left off
                        tgt = self._xlim_scor[1]
                        res = tgt - (self._SigWin.value() - self._ScorWin.value())/2
                        self._SlGoto.setValue(res) # scorwin starts at tgt
                        logger.info(
                            f"`{state}` vigilance state inserted ({value})"
                        )

        def get_cursor_time(event):
            """Cursor location in seconds.

            Accounts for the offset between the whole AxisCanvas scene and
            the viewbox containing data (due to the axis and padding)"""

            # ViewBox object containing data
            viewbox = axiscanvas.wc
            vb_pos = viewbox.pos  # (x_bottomleft, y_bottomleft)
            vb_size = viewbox.size  # (width, height)
            assert viewbox.parent.size == canvas.size  # Sanity check
            # X pos in pixel in whole grid
            x_orig, _ = event.pos
            # X pos in pixels in camera viewbox
            x_vb = x_orig - vb_pos[0]
            # out of camera viewbox
            if x_vb < 0 or x_vb > vb_size[0]:
                return -999
            # axis time range: whole recording or display window
            whole_range = (
                canvas.title in ['Hypnogram', 'Spectrogram']
                and not self.menuDispZoom.isChecked()  # noqa
            )
            if whole_range:
                cursor = self._time[0] + self._time[-1] * x_vb / vb_size[0]
            else:
                val = self._SlVal.value()
                step = self._SlStep
                win = self._SigWin.value()
                tm, th = (val * step, val * step + win)
                cursor = tm + ((th - tm) * x_vb / vb_size[0])
            return cursor

        @canvas.events.mouse_double_click.connect
        def on_mouse_double_click(event):
            """Executed function when double click mouse over canvas.

            :event: the trigger event
            """
            # Get canvas title :
            is_sp_hyp = canvas.title in ['Hypnogram', 'Spectrogram']
            title = canvas.title if is_sp_hyp else canvas.title.split('_')[1]
            # Annotate the timing :
            cursor = get_cursor_time(event)
            # Set the current tab to the annotation tab :
            self.QuickSettings.setCurrentIndex(5)
            # Run annotation :
            self._fcn_annotate_add('', (cursor, cursor), title)

        @canvas.events.mouse_press.connect
        def on_mouse_press(event):
            """Executed function when single click mouse over canvas.

            - CTRL + click: Magnigy the signal under the mouse cursor
            - Enter click-and-drag scoring mode
            """
            # Get cursor position :
            cursor = get_cursor_time(event)
            # ------------- MAGNIFY : CTRL + left click -------------
            name = canvas.title
            is_left = self._is_left_click(event)
            is_ctrl = self._is_modifier(event, 'Control')
            condition = bool(name.find('Canvas') + 1) and is_left and is_ctrl
            if condition and not self._slMagnify.isChecked():
                # Get channel name :
                chan = name.split('Canvas_')[1]
                print(chan)
                # Get index :
                #idx = self._channels.index(chan)
                idx = [chan in channel for channel in self._channels].index(True) 
                # Build transformation :
                kwargs = {'center': (cursor, 0.), 'radii': (3, 15), 'mag': 10}
                transform = vist.nonlinear.Magnify1DTransform(**kwargs)
                self._chan.node[idx].transform = transform
            # ------------- Start drawing click-and-drag window -------------
            # Enter mousescoring mode if the cursor is on the channel/spec/hyp
            # axis & within the display window
            if (
                cursor >= 0
                and (  # noqa
                    any([name[7::] in channel for channel in self._channels])
                    or (canvas.title in ['Spectrogram', 'Hypnogram']  # noqa
                        and self.menuDispZoom.isChecked())  # noqa
                 )
            ):
                self._mouse_pressed = True
                self._mousescoring_active = False  # Active once actually drags
                self._mouse_scorwin_xlim = (cursor, None)
            # ------------- Video -------------
            # Sync vid to start of current scoring window
            self._video.set_video_time(cursor)


        @canvas.events.mouse_move.connect
        def on_mouse_move(event):
            """Executed function when the mouse move over canvas.

            - Update cursor text
            - Magnify for all channels under cursor locations.
            - Extend click-and-drag scoring window if mouse is pressed
            """
            if 'topo' in canvas.title.lower():
                return
            # Get mouse cursor position for the specified canvas :
            cursor = get_cursor_time(event)
            # Enable/Disable magnify :
            if (
                canvas.title not in ['Hypnogram', 'Spectrogram']
                and self._slMagnify.isChecked()  # noqa
            ):
                for i, k in self._chan:
                    self._chan.node[i].transform.center = (cursor, 0.)
                    k.update()
            # Set time position to the cursor text :
            cursor = np.round(cursor * 1000.) / 1000.
            self._txtCursor.setText(f'Cursor: {np.round(cursor, 2)}s')
            # Click-and-drag scoring window
            if self._mouse_pressed and cursor >= 0:
                # Enter mouse-scoring mode if not already the case
                self._mousescoring_active = True
                self._mouse_scorwin_xlim = (
                    self._mouse_scorwin_xlim[0],  # "Click" position
                    cursor,  # Current mouse position
                )
                self._fcn_scorwin_settings()

        @canvas.events.mouse_release.connect
        def on_mouse_release(event):
            """Executed function when the mouse is released over canvas.

            - Set the transformation to the canvas to NullTransform.
            - Stop drawing scoring window or exit mouse-scoring mode
            """
            # Get canvas name :
            name = canvas.title
            condition = bool(name.find('Canvas') + 1)
            if condition and not self._slMagnify.isChecked():
                # Get channel name :
                chan = name.split('Canvas_')[1]
                # Get index :
                #idx = self._channels.index(chan)
                idx = [chan in channel for channel in self._channels].index(True)
                # Build transformation :
                self._chan.node[idx].transform = vist.NullTransform()
            # Quit mouse-scoring mode if no window was drawn/we clicked
            # without drag
            self._mouse_pressed = False
            mouse_xlim = self._mouse_scorwin_xlim
            min_xdrag = 0.05
            if (
                None in mouse_xlim
                or abs(mouse_xlim[1] - mouse_xlim[0]) <= min_xdrag  # noqa
            ):
                self._mousescoring_active = False
            self._update_scorwin_indicator()
            self._video.set_video_time(self._xlim_scor[0])


class Visuals(CanvasShortcuts):
    """Create the visual objects to be added to the scene."""

    def __init__(self):
        """Init."""
        # =================== VARIABLES ===================
        sf, data, time = self._sf, self._data, self._time
        channels, hypno, cameras = self._channels, self._hypno, self._allCams

        # =================== CHANNELS ===================
        self._chan = ChannelPlot(channels, time, camera=cameras[0],
                                 color=self._chancolor, width=self._lw,
                                 color_detection=self._indicol,
                                 parent=self._chanCanvas,
                                 fcn=self._fcn_slider_move)
        PROFILER('Channels', level=1)

        # =================== SPECTROGRAM ===================
        # Create a spectrogram object :
        self._spec = Spectrogram(camera=cameras[1],
                                 fcn=self._fcn_spec_set_data,
                                 parent=self._specCanvas.wc.scene)
        self._spec.set_data(sf, data[0, ...], time, cmap=self._defcmap)
        PROFILER('Spectrogram', level=1)
        # Create a visual indicator for spectrogram :
        self._specInd = Indicator(name='spectro_indic', visible=True, alpha=.3,
                                  parent=self._specCanvas.wc.scene)
        self._specInd.set_data(xlim=(0, 30), ylim=(0, 20))
        PROFILER('Spectrogram indicator', level=1)

        # =================== HYPNOGRAM ===================
        # Create a hypnogram object :
        self._hyp = Hypnogram(time, camera=cameras[2], width=self._lwhyp,
                              hcolors=self._hcolors, hvalues=self._hvalues,
                              hYranks=self._hYranks,
                              parent=self._hypCanvas.wc.scene)
        self._hyp.set_data(sf, hypno, time)
        PROFILER('Hypnogram', level=1)
        # Create a visual indicator for hypnogram :
        self._hypInd = Indicator(name='hypno_indic', visible=True, alpha=.3,
                                 parent=self._hypCanvas.wc.scene)
        self._hypInd.set_data(xlim=(0., 30.), ylim=(-6., 2.))
        PROFILER('Hypnogram indicator', level=1)

        # =================== DETECTIONS ===================
        self._detect = Detection(self._channels.copy(), self._time,
                                 self._defspin, self._defrem, self._defkc,
                                 self._defsw, self._defpeaks, self._defmt,
                                 self._spinsym, self._remsym, self._kcsym,
                                 self._swsym, self._peaksym, self._mtsym,
                                 self._chan.node, self._hypCanvas.wc.scene)
        PROFILER('Detections', level=1)

        # =================== TOPOPLOT ===================
        self._topo = TopoSleep(channels=self._channels, margin=.2,
                               parent=self._topoCanvas.wc.scene)
        # Set camera properties :
        cameras[3].rect = self._topo.rect
        cameras[3].aspect = 1.
        self._pan_pick.model().item(3).setEnabled(any(self._topo._keeponly))
        PROFILER('Topoplot', level=1)

        # =================== VIDEO ===================
        self._video = VideoSleep(
            self._video_file, self._video_offset,
            playerW=self._videoPlayerW, titleW=self._videoTitleW,
            playW=self._videoPlayW, sliderW=self._videoSliderW,
            infoW=self._videoInfoW, offsetW=self._videoOffsetW,
            loadW=self._videoLoadW,
        )
        PROFILER("Videoplot", level=1)

        # =================== SHORTCUTS ===================
        axiscanvas = self._chanCanvas + [self._specCanvas, self._hypCanvas]
        for axiscan in axiscanvas:
            CanvasShortcuts.__init__(self, axiscan)
        self._shpopup.set_shortcuts(self.sh)
        PROFILER('Shortcuts', level=1)
