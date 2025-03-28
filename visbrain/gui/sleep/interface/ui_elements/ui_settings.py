"""Main class for settings managment."""
import numpy as np
import datetime
from PyQt5.QtCore import QObjectCleanupHandler

import vispy.visuals.transforms as vist


class UiSettings(object):
    """Main class for settings managment."""

    def __init__(self):
        """Init."""
        # =====================================================================
        # SLIDER
        # =====================================================================
        self._slFrame.setMaximumHeight(100)
        # Step for slider
        self._SlStep = int(1)
        # Function applied when the slider move :
        self._slOnStart = False
        self._fcn_slider_settings()
        self._SlVal.valueChanged.connect(self._fcn_slider_move)
        # Function applied when the display window changed :
        self._SigWin.valueChanged.connect(self._fcn_sigwin_settings)
        self._SigWin.setKeyboardTracking(False)
        # Function applied when the scoring window changed :
        self._ScorWin.valueChanged.connect(self._fcn_scorwin_settings)
        self._ScorWin.setKeyboardTracking(False)
        # Function applied when the slider settings changed
        self._SigStep.valueChanged.connect(self._fcn_slider_settings)
        self._SigStep.setKeyboardTracking(False)
        # Spin box for window selection :
        self._SlGoto.valueChanged.connect(self._fcn_slider_win_selection)
        self._SlGoto.setKeyboardTracking(False)
        # Unit conversion :
        self._slRules.currentIndexChanged.connect(self._fcn_slider_move)
        # Grid toggle :
        self._slGrid.clicked.connect(self._fcn_grid_toggle)
        # Text format :
        self._slTxtFormat = (
            "Window : [ {start} ; {end} ] {unit} || " +
            "Scoring : [ {start_scor} ; {end_scor} ] {unit} || " +
            "Vigilance state : {state}"
        )
        # Absolute time :
        self._slAbsTime.clicked.connect(self._fcn_slider_move)
        # Magnify :
        self._slMagnify.clicked.connect(self._fcn_slider_magnify)
        # Visible scoring window indicator :
        self._ScorWinVisible.clicked.connect(
            self._fcn_scorwin_indicator_toggle
        )
        # Lock scoring window to the display window
        self._LockScorSigWins.clicked.connect(self._fcn_lock_scorwin_sigwin)
        # Annotation from the navigation bar :
        self._AnnotateRun.clicked.connect(self._fcn_annotate_nav)
        # "MouseScoring": select epochs with "click-and-drag" scoring
        # "mousescoring" means we clicked, dragged and await for scoring
        self._mouse_pressed = False  # Is the mouse still pressed
        self._mousescoring_active = False  # Are we in "MouseScoring" mode
        self._mouse_scorwin_xlim = (None, None)  # (orig, final)

    # =====================================================================
    # Properties and utility functions
    # =====================================================================

    @property
    def mouse_scorwin_xlim(self):
        """(start, end) for currently active MouseScoring window.

        (_mouse_scorwin_xlim = (click_pos, current_drag_pos))
        """
        if None in self._mouse_scorwin_xlim:
            return self._mouse_scorwin_xlim
        return sorted(self._mouse_scorwin_xlim)

    @property
    def _xlim(self):
        """Display window xlim: (start, end)."""
        val = self._SlVal.value()
        # step = self._SlVal.singleStep()
        step = self._SlStep
        win = self._SigWin.value()
        return (val * step, val * step + win)

    @property
    def _xlim_scor(self):
        """(start, end) of current scoring window.

        - Derived from SigWin and ScorWin in default mode
        - return start/end values of click-and-drag in "MouseScoring" mode
        """
        if self._mousescoring_active:
            return self.mouse_scorwin_xlim
        # Otherwise, scoring window of a certain size centered to the display
        # window
        scorwin = self._ScorWin.value()
        xlim = self._xlim
        xhalf = (xlim[1] - xlim[0]) / 2 + xlim[0]
        return (
            max(xlim[0], xhalf - scorwin / 2),
            min(xlim[1], xhalf + scorwin / 2),
        )  # Centered to display window

    def data_index(self, xlim):
        """Closest time index of data from xlim."""
        t = [0, 0]
        t[0] = int(round(np.abs(self._time - xlim[0]).argmin()))
        t[1] = int(round(np.abs(self._time - xlim[1]).argmin()))
        return t

    @property
    def _hypref(self):
        """Return ref value of "current" vigilance state."""
        # "Current" is at start of scoring window
        xlim_scor = self._xlim_scor
        t = self.data_index(xlim_scor)
        return int(self._hypno[t[0]])

    @property
    def _state_yrank(self):
        """Return y rank of "current" vigilance state."""
        return self._hYranks[np.where(self._hvalues == self._hypref)[0]][0]

    @property
    def _state_name(self):
        """Return name of "current" vigilance state."""
        return self._hstates[np.where(self._hvalues == self._hypref)[0]][0]

    @property
    def _state_color(self):
        """Return color of "current" vigilance state."""
        return self._hcolors[np.where(self._hvalues == self._hypref)[0]][0]

    # =====================================================================
    # SLIDER, DISPLAY WINDOW AND SCORING WINDOW
    # =====================================================================
    def _update_text_info(self):
        """Redraw the text info in the settings pane."""
        xlim = self._xlim
        xlim_scor = self._xlim_scor
        state = self._state_name
        hypcol = self._state_color
        # Get unit and convert:
        if self._slAbsTime.isChecked():
            xlim = np.asarray(xlim) + self._toffset

            def rounded_utc(timestamp):
                # Round to 2 digits
                tstring = str(
                    datetime.datetime.utcfromtimestamp(timestamp)
                ).split(' ')[1]  # hh:mm:ss or hh:mm:ss.xxx
                if '.' in tstring:
                    hhmmss, digits = tstring.split('.')
                else:
                    hhmmss, digits = tstring, '00'
                return '.'.join([hhmmss, digits[0:2]])

            start = rounded_utc(xlim[0])
            stend = rounded_utc(xlim[1])
            start_scor = rounded_utc(xlim_scor[0])
            stend_scor = rounded_utc(xlim_scor[1])
            txt = "Window : [ " + start + " ; " + stend + " ] || " + \
                "Scoring : [ " + start_scor + " ; " + stend_scor + " ] || " + \
                "Vigilance state : " + state
        else:
            unit = self._slRules.currentText()
            if unit == 'seconds':
                fact = 1.
                short_unit = 'sec'
            elif unit == 'minutes':
                fact = 60.
                short_unit = 'min'
            elif unit == 'hours':
                fact = 3600.
                short_unit = 'hs'
            xconv = np.round(1000. * np.array(xlim) / fact) / 1000.
            xconv_scor = np.round(1000. * np.array(xlim_scor) / fact) / 1000.
            # Format string :
            txt = self._slTxtFormat.format(
                start=np.round(xconv[0], 2), end=np.round(xconv[1], 2),
                start_scor=np.round(xconv_scor[0], 2),
                end_scor=np.round(xconv_scor[1], 2),
                unit=short_unit,
                state=state)
        # Set text :
        self._SlText.setText(txt)
        self._SlText.setFont(self._font)
        self._SlText.setStyleSheet("QLabel {color: " +
                                   hypcol + ";}")

    def _update_scorwin_indicator(self):
        """Change location and width of scoring window indicator."""
        # Get scoring window x_start x_end
        xlim_scor = self._xlim_scor

        # Change width of bars (so they don't become too small or too big) when
        # display window changes
        def barwidth():
            return min(
                self._SigWin.value() * 0.2 / 30.0,  # Constant apparent value
                max(
                    0.05,
                    (xlim_scor[1] - xlim_scor[0]) / 2 - 0.05
                ),  # Skinny bars if the scoring window is v small
            )
        # Redraw bars
        for i, _ in self._chan:
            # Get current ylims of channel cameras from their `rect`
            cam_rect = self._chanCam[i].rect
            ycam = (cam_rect.bottom, cam_rect.top)
            self._chan.scorwin_ind[i].set_data(xlim_scor[0], xlim_scor[1],
                                               ycam,
                                               barwidth=barwidth())

    def _fcn_slider_move(self):
        """Function applied when the slider move."""
        # ================= Scoring mode =================
        # If we stopped click-and-dragging, exit mousescoring mod
        # (ie revert to regular (centered) scoring window)
        # If we're still pressing the mouse, extend the click-and-drag
        # window for super-duper-fast scoring
        if not self._mouse_pressed:
            self._mousescoring_active = False
            # TODO: Fake mouse mouvement (Update cursor time and scoring window)

        # ================= INDEX =================
        # Get slider variables :
        win = self._SigWin.value()
        xlim = self._xlim
        iszoom = self.menuDispZoom.isChecked()
        unit = str(self._slRules.currentText())
        # Find closest data time index for display window start/end
        t = self.data_index(xlim)
        # Hypnogram info :
        hypYrank = self._state_yrank
        hypcol = self._state_color

        # ================= MESH UPDATES =================
        # ---------------------------------------
        # Update display signal :
        sl = slice(t[0], t[1])
        self._chan.set_data(self._sf, self._data, self._time, sl=sl,
                            ylim=self._ylims)
        # Redraw the scoring window indicators
        self._update_scorwin_indicator()

        # ---------------------------------------
        is_indic_checked = self.menuDispIndic.isChecked()
        # Update spectrogram indicator :
        if is_indic_checked and not iszoom:
            ylim = (self._PanSpecFstart.value(), self._PanSpecFend.value())
            self._specInd.set_data(xlim=xlim, ylim=ylim)

        # ---------------------------------------
        # Update hypnogram indicator :
        if is_indic_checked and not iszoom:
            self._hypInd.set_data(xlim=xlim, ylim=(-6., 2.))

        # ---------------------------------------
        # Update topoplot if visible :
        if self._topoW.isVisible():
            # Prepare data before plotting :
            data = self._topo._prepare_data(self._sf, self._data[:, sl],
                                            self._time[sl]).mean(1)
            # Set preprocessed sleep data :
            self._topo.set_sleep_topo(data)
            # Update title :
            fm, fh = self._PanTopoFmin.value(), self._PanTopoFmax.value()
            dispas = self._PanTopoDisp.currentText()
            txt = 'Mean ' + dispas + ' in\n[' + str(fm) + ';' + str(fh) + 'hz]'
            self._topoTitle.setText(txt)
            self._topoTitle.setStyleSheet("QLabel {color: " +
                                          hypcol + ";}")

        # ---------------------------------------
        # Update Time indicator :
        if is_indic_checked:
            self._TimeAxis.set_data(xlim[0], win, self._time, unit=unit,
                                    markers=self._annot_mark)

        # ================= GUI =================
        # Update Go to :
        self._SlGoto.setValue(xlim[0])

        # ================= ZOOMING =================
        if iszoom:
            xlim_diff = xlim[1] - xlim[0]
            # Histogram :
            self._hypcam.rect = (xlim[0], -len(self._hvalues),
                                 xlim_diff, len(self._hvalues) + 1)
            # Spectrogram :
            self._speccam.rect = (xlim[0], self._spec.freq[0], xlim_diff,
                                  self._spec.freq[-1] - self._spec.freq[0])
            # Time axis :
            self._TimeAxis.set_data(xlim[0], win, np.array([xlim[0], xlim[1]]),
                                    unit='seconds', markers=self._annot_mark)
            self._timecam.rect = (xlim[0], 0., win, 1.)

        # ================= TEXT INFO =================
        self._update_text_info()

        # ================= HYPNO LABELS =================
        for k in self._hypYLabels:
            k.setStyleSheet("QLabel")
        self._hypYLabels[hypYrank + 1].setStyleSheet("QLabel {color: " +
                                                     hypcol + ";}")

        # ================= VIDEO =================
        # Sync to start of current scoring window
        self._video.set_video_time(self._xlim_scor[0])

    def _fcn_slider_settings(self):
        """Function applied to change slider settings."""
        # Get current slider value :
        sl = self._SlVal.value()
        slmax = self._SlVal.maximum()
        win = self._SigWin.value()
        # Set minimum :
        self._SlVal.setMinimum(int(self._time.min()))
        # Set maximum :
        step = self._SlStep
        self._SlVal.setMaximum(int(((self._time.max() - win) / step) + 1))
        self._SlVal.setTickInterval(step)
        self._SlVal.setSingleStep(step)
        self._SlVal.setPageStep(int(self._SigStep.value()))
        self._SlGoto.setMaximum(int((self._time.max() - win)))
        # Re-set slider value :
        self._SlVal.setValue(int(sl * self._SlVal.maximum() / slmax))

        if self._slOnStart:
            self._fcn_slider_move()
            # Update grid :
            if self.menuDispZoom.isChecked():
                self._hyp.set_grid(self._time, self._SigStep.value())
            else:
                self._hyp.set_grid(self._time, win)
        else:
            self._slOnStart = True

    def _fcn_sigwin_settings(self):
        """Function applied when changing the display window size."""
        # Change maximum allowed value of the scoring window
        win = self._SigWin.value()
        self._ScorWin.setMaximum(win)
        # In "Lock" mode
        if self._LockScorSigWins.isChecked():
            # Change the scoring window value without unlocking
            self._ScorWin.blockSignals(True)
            self._ScorWin.setValue(win)
            self._ScorWin.blockSignals(False)
            # Change the slider step size
            self._SigStep.setValue(win)
        # Redraw stuff as if we were moving the slider
        self._fcn_slider_move()

    def _fcn_scorwin_settings(self):
        """Function applied when changing the scoring window size."""
        # Unlock the scoring window
        self._LockScorSigWins.setChecked(False)
        # Make the scoring window visible
        self._ScorWinVisible.setChecked(True)
        self._fcn_scorwin_indicator_toggle()
        # Change the text info:
        self._update_text_info()
        # Redraw the scoring window indicator bars
        self._update_scorwin_indicator()
        # If the scoring window size changed because user set it from the
        # settings, change slider step and update video frame.
        if not self._mouse_pressed:
            scorwin = self._ScorWin.value()
            self._SigStep.setValue(scorwin)
            # Sync vid to start of current scoring window
            self._video.set_video_time(self._xlim_scor[0])

    def _fcn_slider_win_selection(self):
        """Move slider using window spin."""
        self._SlVal.setValue(int(self._SlGoto.value() / self._SlStep))

    def _fcn_slider_magnify(self):
        """Magnify signals."""
        # Set transformation to each node parent :
        for k in self._chan.node:
            # Use either Magnify / Null transformation :
            if self._slMagnify.isChecked():
                transform = vist.nonlinear.Magnify1DTransform()
            else:
                transform = vist.NullTransform()
            k.transform = transform

    # =====================================================================
    # GRID
    # =====================================================================
    def _fcn_grid_toggle(self):
        """Toggle grid visibility."""
        viz = self._slGrid.isChecked()
        # Toggle hypno grid :
        self._hyp.grid.visible = viz
        # Toggle grid for each channel :
        for k in self._chan.grid:
            k.visible = viz

    # =====================================================================
    # DISPLAY SCORING WINDOW INDICATOR BARS
    # =====================================================================
    def _fcn_scorwin_indicator_toggle(self):
        """Toggle visibility of scoring window indicators."""
        viz = self._ScorWinVisible.isChecked()
        for i, chan in self._chan:
            self._chan.scorwin_ind[i].mesh_start.visible = viz
            self._chan.scorwin_ind[i].mesh_end.visible = viz

    # =====================================================================
    # LOCK SCORING WINDOW TO DISPLAY WINDOW
    # =====================================================================
    def _fcn_lock_scorwin_sigwin(self):
        """Toggle locking of scoring window to display window."""
        locked = self._LockScorSigWins.isChecked()
        # If locking
        if locked:
            # Set _ScorWin to _SigWin without unlocking
            self._ScorWin.blockSignals(True)
            self._ScorWin.setValue(self._SigWin.value())
            self._ScorWin.blockSignals(False)
            # Set stepsize to _SigWin
            self._SigStep.setValue(self._SigWin.value())
            # Hide the scoring window indicators
            self._ScorWinVisible.setChecked(False)
            self._fcn_scorwin_indicator_toggle()
        # If unlocking
        else:
            # Show the scoring window
            self._ScorWinVisible.setChecked(True)
            self._fcn_scorwin_indicator_toggle()

    # =====================================================================
    # RULER
    # =====================================================================
    def _get_fact_from_unit(self):
        """Get factor conversion from current selected unit."""
        unit = str(self._slRules.currentText())
        if unit == 'seconds':
            fact = 1.
        elif unit == 'minutes':
            fact = 60.
        elif unit == 'hours':
            fact = 3600.
        return fact

    def on_mouse_wheel(self, event):
        """Executed function on mouse wheel."""
        # Scroll in units of self._SigStep
        delta_n = int(event.delta[1] * 60 * 0.25)
        delta_sec = self._SigStep.value() * delta_n
        self._SlVal.setValue(int(self._SlVal.value() + delta_sec / self._SlStep))

    # =====================================================================
    # HYPNO
    # =====================================================================
    def _add_stage_on_scorwin(self, state):
        """Change the stage on the current scoring window."""
        # Get the scoring window xlim
        xlim_scor = self._xlim_scor
        # Find closest data time index from xlim
        t = self.data_index(xlim_scor)
        # Set the stage on the hypnogram
        self._hypno[t[0]:t[1]] = state
        self._hyp.set_state(t[0], t[1], state)
        # Set the stage on the hypno overlay on signal
        self._fcn_hypoverlay_update()
        # # Update info table :
        self._fcn_info_update()
        # Update scoring table :
        self._fcn_hypno_to_score()
        # self._fcn_score_to_hypno()

    def _fcn_hypoverlay_update(self):
        """Redraw the HypnoOverlay signal overlays."""
        viz = self.menuDispHypOverlay.isChecked()
        data_colors = None
        for i, _ in self._chan:
            hyp_overlay = self._chan.hyp_overlay[i]
            if viz:
                # Build color array once (again)
                if data_colors is None:
                    hcolors = self._hyp.hcolors
                    data_colors = np.array([hcolors[v] for v in self._hypno], dtype=np.float32).squeeze()
                    data_colors[:, 3] = hyp_overlay.alpha
                # Apply same color array to all
                hyp_overlay.set_data(data_colors)
            hyp_overlay.region.visible = viz

    # =====================================================================
    # Annotate
    # =====================================================================
    def _fcn_annotate_nav(self):
        """Annotate from the selected window."""
        # Set the current tab to the annotation tab :
        self.QuickSettings.setCurrentIndex(5)
        # Run annotation :
        self._fcn_annotate_add('')

    # =====================================================================
    # CLEAN / RESET GUI
    # =====================================================================
    def _fcn_clean_gui(self):
        """Clean the entire GUI."""
        # -------------- TABLES --------------
        # Info :
        self._infoTable.clear()
        self._infoTable.setRowCount(0)

        # Detection :
        self._DetectLocations.clear()
        self._DetectLocations.setRowCount(0)

        # -------------- LIST BOX --------------
        # Disconnect :
        self._PanSpecChan.currentIndexChanged.disconnect()
        # Clear items :
        self._PanSpecChan.clear()
        self._ToolDetectChan.clear()

        # -------------- VISUALS --------------
        # Channels :
        for k in range(len(self)):
            # Disconnect buttons :
            self._chanChecks[k].clicked.disconnect()
            self._yminSpin[k].valueChanged.disconnect()
            self._ymaxSpin[k].valueChanged.disconnect()
            # Delete elements :
            self._chanChecks[k].deleteLater()
            self._yminSpin[k].deleteLater(), self._ymaxSpin[k].deleteLater()
            self._chanWidget[k].deleteLater()
            self._chanLayout[k].deleteLater()
            self._chanLabels[k].deleteLater()
            self._amplitudeTxt[k].deleteLater()
            self._chanCanvas[k].parent = None
        QObjectCleanupHandler().add(self._chanGrid)
        QObjectCleanupHandler().clear()
        # Spectrogram :
        self._specCanvas.parent = None
        self._SpecW.deleteLater(), self._SpecLayout.deleteLater()
        self._specLabel.deleteLater()
        # Hypnogram :
        self._hypCanvas.parent = None
        self._HypW.deleteLater(), self._HypLayout.deleteLater()
        self._hypLabel.deleteLater()
        # Time axis :
        self._TimeAxis.parent = None
        self._TimeAxisW.deleteLater(), self._TimeLayout.deleteLater()
        self._timeLabel.deleteLater()

    def _fcn_reset_gui(self):
        """Reset the GUI."""
        from .uiElements import uiElements
        from ...visuals import visuals
        from ...tools import Tools
        uiElements.__init__(self)
        self._cam_creation()
        visuals.__init__(self)
        Tools.__init__(self)
        self._fcns_on_creation()
