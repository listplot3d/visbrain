:orphan:

.. _general_examples:

.. warning::
    - Some Visbrain's examples are based on data that need to be downloaded. Those data are downloaded inside the folder *~/visbrain_data/example_data*
    - You may encounter a window transparency error. This is a known issue of the Vispy package (see https://github.com/vispy/vispy/pull/1394)

Examples
========

.. contents:: Contents
   :local:
   :depth: 2


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. thumbnail-parent-div-close

.. raw:: html

    </div>

SceneObj : combine objects into subplots
----------------------------------------

Each Visbrain's object inherits a method called `preview` which basically
display the object. The SceneObj object can be used to combine objects into
subplots.

The following examples illustrate how to combine those objects into a grid of
subplots.


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate how to animate objects inside the scene. Note that animations can only be used with 3D objects.">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_animate_scene_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_animate_scene.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Animate objects in the scene</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate the main functionalities and inputs of the brain object i.e :">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_brain_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_brain_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Brain object (BrainObj) : complete tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate the feasibility to combine multiple objects in the same scene.">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_combine_objects_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_combine_objects.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Combine multiple objects</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Illustration of the main functionalities and inputs of the connectivity object:">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_connectivity_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_connectivity_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Connectivity object (ConnectObj) : complete tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate the main functionalities and inputs of the grid of time-series object i.e :">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_gridsignals_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_gridsignals_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Grid of signals object (GridSignalsObj) : complete tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Use and control image, time-frequency maps and spectrogram.">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_im_tf_spec_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_im_tf_spec_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Image, time-frequency map and spectrogram objects</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="The PAC measure the degree of coupling between the phase of slow oscillations and the amplitude of fatser oscillations. To compute PAC, you&#x27;ll need to install the tensorpac package (see https://github.com/EtienneCmb/tensorpac).">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_pac_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_pac_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Phase-Amplitude Coupling (PAC)  object</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate the main functionalities and inputs of the roi object i.e :">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_roi_object_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_roi_object.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Region Of Interest object (RoiObj) : complete tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate the main functionalities and inputs of the source object i.e :">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_source_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_source_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Source object (SourceObj) : complete tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate the main functionalities and inputs of the topoplot object i.e :">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_topo_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_topo_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Topoplot object (TopoObj) : complete tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Illustration of the main features of 3d time-series and pictures. This include :">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_tspic_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_tspic_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Time-series and pictures 3D (TimeSeries3DObj & Picture3DObj): complete tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Illustration of the main functionalities and inputs of the volume object :">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_volume_obj_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_volume_obj.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Volume object (VolumeObj) : complete tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate how to plot .x3d files. 6 brain templates are going to be downloaded (total of 26.3Mo). Additional templates can be downloaded from : https://scalablebrainatlas.incf.org">

.. only:: html

  .. image:: /auto_examples/objects/images/thumb/sphx_glr_plot_x3d_files_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_objects_plot_x3d_files.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot x3d files</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>

Graphical user interface : Brain
--------------------------------

Examples demonstrating visualizations on a standard 3D-MNI brain.

.. contents:: Contents
   :local:
   :depth: 2


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Control the brain i.e the brain template to use, the transparency and the hemisphere.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_00_brain_control_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_00_brain_control.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Brain control</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Control the cross-section panel and the volume using a Nifti file. The nibabel package should also be installed.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_01_cross_sections_and_volume_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_01_cross_sections_and_volume.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Cross-sections and volume control</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate how to define a custom brain template using your own vertices and faces.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_02_brain_using_vertices_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_02_brain_using_vertices.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Define a brain template using vertices and faces</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Add sources to the scene. This script also illustrate most of the controls for sources. Each source is defined by a (x, y, z) MNI coordinate. Then, we can attach some data to sources and project this activity onto the surface (cortical projection). Alternatively, you can run the cortical repartition which is defined as the number of contributing sources per vertex.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_03_sources_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_03_sources.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Add deep sources</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Display and customize connectivity. To this end, we define some deep sources and connect them.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_04_connectivity_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_04_connectivity.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Connect deep sources</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrate how to display Region Of Interest (ROI).">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_05_region_of_interest_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_05_region_of_interest.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Add Region of interest (ROI)</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to display time-series attached to sources. The time-series can then be controlled from the GUI in the Sources/Time-series tab.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_06_add_time_series_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_06_add_time_series.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Add time series</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to display small pictures attached to sources. The pictures can then be controlled from the GUI in the Sources/Pictures tab.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_07_add_pictures_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_07_add_pictures.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Add pictures</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Offline rendering of selected canvas.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_08_screenshot_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_08_screenshot.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Screenshot example</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Add multiple source&#x27;s and connectivity object to the scene.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_09_add_multiple_objects_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_09_add_multiple_objects.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Add multiple objects to the scene</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Import a custom Nifti volume that can be then used in the cross-section or volume tab. To this end, the python package nibabel must be installed and custom Nifti volume must be downloaded. When the volume is loaded into the GUI, it&#x27;s accessible from the Brain/Cross-sections and Brain/Volume tab.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_10_add_nifti_volume_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_10_add_nifti_volume.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Add Nifti volume</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Add vectors to the scene. This example demonstrate the two methods to defined vectors :">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_11_add_vectors_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_11_add_vectors.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Add vectors</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Parcellize the brain surface using .annot files. This example use Nibabel to read the .annot file.">

.. only:: html

  .. image:: /auto_examples/gui_brain/images/thumb/sphx_glr_12_parcellize_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_brain_12_parcellize.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Parcellize brain surface</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>

Graphical user interface : Sleep
--------------------------------

Examples demonstrating how to use Sleep and how to load files.

.. contents:: Contents
   :local:
   :depth: 2


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to open Sleep.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_basic_sleep_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_basic_sleep.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Basic configuration</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to load a BrainVision file.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_load_brainvision_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_load_brainvision.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Load a BrainVision file</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to load an EDF file.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_load_edf_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_load_edf.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Load EDF file</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to specify custom configuration for vigilance states.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_load_edf_user_states_cfg_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_load_edf_user_states_cfg.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Load EDF file with custom vigilance state configuration</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to load an ELAN file.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_load_elan_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_load_elan.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Load ELAN files</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to load an ELAN file.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_load_matlab_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_load_matlab.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Load a Matlab file</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrate how to load a .rec file.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_load_rec_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_load_rec.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Load REC files</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how to load data using MNE-Python package. https://martinos.org/mne/stable/index.html">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_load_using_mne_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_load_using_mne.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Load a file using MNE-python</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Get sleep statictics such as sleep stages duration, duration of the hypnogram.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_plot_get_sleep_statistics_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_plot_get_sleep_statistics.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Get sleep statistics</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Plot a hypnogram using matplotlib.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_plot_hypnogram_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_plot_hypnogram.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Matplotlib plot of an hypnogram</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrates how to replace the default detection algorithm.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_replace_detection_basic_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_replace_detection_basic.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Replace detection algorithm : basic example</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example illustrates how to replace the default spindle detection algorithm with those implemented inside wonambi.">

.. only:: html

  .. image:: /auto_examples/gui_sleep/images/thumb/sphx_glr_replace_detection_wonambi_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_sleep_replace_detection_wonambi.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Replace detection with wonambi algorithm</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>

Graphical user interface : Signal
---------------------------------

Examples demonstrating how to use the Signal module.

.. contents:: Contents
   :local:
   :depth: 2


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Plot a basic vector. Then, you can visualize this vector as a continuous line, markers, histogram or compute the time-frequency map or power spectrum density (PSD).">

.. only:: html

  .. image:: /auto_examples/gui_signal/images/thumb/sphx_glr_00_1d_signal_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_signal_00_1d_signal.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot a 1D signal</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Dispose a two dimensional array of data into a grid.">

.. only:: html

  .. image:: /auto_examples/gui_signal/images/thumb/sphx_glr_01_2d_signals_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_signal_01_2d_signals.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot a 2D array of data</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Plot and inspect a 3D array of data.">

.. only:: html

  .. image:: /auto_examples/gui_signal/images/thumb/sphx_glr_02_3d_signals_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_signal_02_3d_signals.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot a 3D array of data</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Use custom color, font size...">

.. only:: html

  .. image:: /auto_examples/gui_signal/images/thumb/sphx_glr_03_interface_customization_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_signal_03_interface_customization.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Interface customization</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Import annotations from a text file and annotate trials.">

.. only:: html

  .. image:: /auto_examples/gui_signal/images/thumb/sphx_glr_04_annotations_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_signal_04_annotations.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Import, save and add annotations</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Export all of the time-frequency maps, psd of a dataset.">

.. only:: html

  .. image:: /auto_examples/gui_signal/images/thumb/sphx_glr_05_screenshot_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_signal_05_screenshot.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Screenshot tutorial</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Superimposition of all the signals.">

.. only:: html

  .. image:: /auto_examples/gui_signal/images/thumb/sphx_glr_06_butterfly_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_gui_signal_06_butterfly.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Butterfly plot</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>

EEG/MEG Examples
----------------

EEG/MEG examples (reproduction of MNE and PySurfer examples).

.. contents:: Contents
   :local:
   :depth: 2


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Display a conjunction map from a nii.gz file (NiBabel required).">

.. only:: html

  .. image:: /auto_examples/eeg_meg/images/thumb/sphx_glr_conjunction_map_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_eeg_meg_conjunction_map.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Display conjunction map</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Display fMRI activations from a nii.gz file (NiBabel required).">

.. only:: html

  .. image:: /auto_examples/eeg_meg/images/thumb/sphx_glr_fmri_activation_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_eeg_meg_fmri_activation.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Display fMRI activation</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Plot source estimation.">

.. only:: html

  .. image:: /auto_examples/eeg_meg/images/thumb/sphx_glr_forward_solution_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_eeg_meg_forward_solution.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot forward solution</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Plot MEG inverse solution.">

.. only:: html

  .. image:: /auto_examples/eeg_meg/images/thumb/sphx_glr_meg_inverse_solution_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_eeg_meg_meg_inverse_solution.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot MEG inverse solution</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Plot from a .fif file using the visbrain.mne.mne_plot_source_space function">

.. only:: html

  .. image:: /auto_examples/eeg_meg/images/thumb/sphx_glr_source_space_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_eeg_meg_source_space.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot source space</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Plot vector-valued MEG inverse solution.">

.. only:: html

  .. image:: /auto_examples/eeg_meg/images/thumb/sphx_glr_vector_based_meg_inverse_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_eeg_meg_vector_based_meg_inverse.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Plot vector-valued MEG inverse solution</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>

Figure Examples
---------------

Examples demonstrating figure layout.


.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This script generate some figures using the Brain module. Those exported pictures are going to be set in a layout in the 1_LayoutExample.py script.">

.. only:: html

  .. image:: /auto_examples/figure/images/thumb/sphx_glr_0_GeneratePictures_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_figure_0_GeneratePictures.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Generate pictures</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Arange pictures in a grid.">

.. only:: html

  .. image:: /auto_examples/figure/images/thumb/sphx_glr_1_LayoutExample_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_figure_1_LayoutExample.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Page layout example</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>


.. toctree::
   :hidden:
   :includehidden:


   /auto_examples/objects/index.rst
   /auto_examples/gui_brain/index.rst
   /auto_examples/gui_sleep/index.rst
   /auto_examples/gui_signal/index.rst
   /auto_examples/eeg_meg/index.rst
   /auto_examples/figure/index.rst


.. only:: html

  .. container:: sphx-glr-footer sphx-glr-footer-gallery

    .. container:: sphx-glr-download sphx-glr-download-python

      :download:`Download all examples in Python source code: auto_examples_python.zip </auto_examples/auto_examples_python.zip>`

    .. container:: sphx-glr-download sphx-glr-download-jupyter

      :download:`Download all examples in Jupyter notebooks: auto_examples_jupyter.zip </auto_examples/auto_examples_jupyter.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
