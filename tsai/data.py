# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/001_data.ipynb (unless otherwise specified).

__all__ = ['decompress_from_url', 'get_UCR_univariate_list', 'get_UCR_multivariate_list', 'stack_padding',
           'get_UCR_data', 'np_convert', 'np_collate', 'np_str_obj_array_pattern', 'np_collate_err_msg_format']

# Cell
# import os
# from pathlib import Path
# from fastcore.test import *
# from fastai2.imports import *
# from fastai2.data.transforms import *

from .imports import *
from .utils import *

# Cell
import tempfile
try: from urllib import urlretrieve
except ImportError: from urllib.request import urlretrieve
import shutil
from pyunpack import Archive
from scipy.io import arff

# Cell
def decompress_from_url(url, target_dir=None, verbose=False):
    #Download
    try:
        fname = os.path.basename(url)
        tmpdir = tempfile.mkdtemp()
        local_comp_fname = os.path.join(tmpdir, fname)
        urlretrieve(url, local_comp_fname)
    except:
        shutil.rmtree(tmpdir)
        if verbose: sys.stderr.write("Could not download url. Please, check url.\n")

    #Decompress
    try:
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        Archive(local_comp_fname).extractall(target_dir)
        shutil.rmtree(tmpdir)
        return target_dir
    except:
        shutil.rmtree(tmpdir)
        if verbose: sys.stderr.write("Could not uncompress file, aborting.\n")
        return None

# Cell
def get_UCR_univariate_list():
    return [
        'ACSF1', 'Adiac', 'AllGestureWiimoteX', 'AllGestureWiimoteY',
        'AllGestureWiimoteZ', 'ArrowHead', 'Beef', 'BeetleFly', 'BirdChicken',
        'BME', 'Car', 'CBF', 'Chinatown', 'ChlorineConcentration',
        'CinCECGTorso', 'Coffee', 'Computers', 'CricketX', 'CricketY',
        'CricketZ', 'Crop', 'DiatomSizeReduction',
        'DistalPhalanxOutlineAgeGroup', 'DistalPhalanxOutlineCorrect',
        'DistalPhalanxTW', 'DodgerLoopDay', 'DodgerLoopGame',
        'DodgerLoopWeekend', 'Earthquakes', 'ECG200', 'ECG5000', 'ECGFiveDays',
        'ElectricDevices', 'EOGHorizontalSignal', 'EOGVerticalSignal',
        'EthanolLevel', 'FaceAll', 'FaceFour', 'FacesUCR', 'FiftyWords',
        'Fish', 'FordA', 'FordB', 'FreezerRegularTrain', 'FreezerSmallTrain',
        'Fungi', 'GestureMidAirD1', 'GestureMidAirD2', 'GestureMidAirD3',
        'GesturePebbleZ1', 'GesturePebbleZ2', 'GunPoint', 'GunPointAgeSpan',
        'GunPointMaleVersusFemale', 'GunPointOldVersusYoung', 'Ham',
        'HandOutlines', 'Haptics', 'Herring', 'HouseTwenty', 'InlineSkate',
        'InsectEPGRegularTrain', 'InsectEPGSmallTrain', 'InsectWingbeatSound',
        'ItalyPowerDemand', 'LargeKitchenAppliances', 'Lightning2',
        'Lightning7', 'Mallat', 'Meat', 'MedicalImages', 'MelbournePedestrian',
        'MiddlePhalanxOutlineAgeGroup', 'MiddlePhalanxOutlineCorrect',
        'MiddlePhalanxTW', 'MixedShapesRegularTrain', 'MixedShapesSmallTrain',
        'MoteStrain', 'NonInvasiveFetalECGThorax1',
        'NonInvasiveFetalECGThorax2', 'OliveOil', 'OSULeaf',
        'PhalangesOutlinesCorrect', 'Phoneme', 'PickupGestureWiimoteZ',
        'PigAirwayPressure', 'PigArtPressure', 'PigCVP', 'PLAID', 'Plane',
        'PowerCons', 'ProximalPhalanxOutlineAgeGroup',
        'ProximalPhalanxOutlineCorrect', 'ProximalPhalanxTW',
        'RefrigerationDevices', 'Rock', 'ScreenType', 'SemgHandGenderCh2',
        'SemgHandMovementCh2', 'SemgHandSubjectCh2', 'ShakeGestureWiimoteZ',
        'ShapeletSim', 'ShapesAll', 'SmallKitchenAppliances', 'SmoothSubspace',
        'SonyAIBORobotSurface1', 'SonyAIBORobotSurface2', 'StarLightCurves',
        'Strawberry', 'SwedishLeaf', 'Symbols', 'SyntheticControl',
        'ToeSegmentation1', 'ToeSegmentation2', 'Trace', 'TwoLeadECG',
        'TwoPatterns', 'UMD', 'UWaveGestureLibraryAll', 'UWaveGestureLibraryX',
        'UWaveGestureLibraryY', 'UWaveGestureLibraryZ', 'Wafer', 'Wine',
        'WordSynonyms', 'Worms', 'WormsTwoClass', 'Yoga'
    ]

test_eq(len(get_UCR_univariate_list()), 128)

# Cell
def get_UCR_multivariate_list():
    return [
        'ArticularyWordRecognition', 'AtrialFibrillation', 'BasicMotions',
        'CharacterTrajectories', 'Cricket', 'DuckDuckGeese', 'EigenWorms',
        'Epilepsy', 'ERing', 'EthanolConcentration', 'FaceDetection',
        'FingerMovements', 'HandMovementDirection', 'Handwriting', 'Heartbeat',
        'InsectWingbeat', 'JapaneseVowels', 'Libras', 'LSST', 'MotorImagery',
        'NATOPS', 'PEMS-SF', 'PenDigits', 'PhonemeSpectra', 'RacketSports',
        'SelfRegulationSCP1', 'SelfRegulationSCP2', 'SpokenArabicDigits',
        'StandWalkJump', 'UWaveGestureLibrary'
    ]

test_eq(len(get_UCR_multivariate_list()), 30)

# Cell
def stack_padding(arr):
    def resize(row, size):
        new = np.array(row)
        new.resize(size)
        return new
    row_length = max(arr, key=len).__len__()
    mat = np.array( [resize(row, row_length) for row in arr] )
    return mat


from sktime.utils.load_data import load_from_tsfile_to_dataframe
def get_UCR_data(dsid, path='.', parent_dir='data/UCR', verbose=False, drop_na=False, on_disk=True):
    if verbose: print('Dataset:', dsid)
    assert dsid in get_UCR_univariate_list() + get_UCR_multivariate_list(), f'{dsid} is not a UCR dataset'
    full_parent_dir = Path(path)/parent_dir
    full_tgt_dir = full_parent_dir/dsid
    if not all([os.path.isfile(f'{full_parent_dir}/{dsid}/{fn}.npy') for fn in ['X_train', 'X_valid', 'y_train', 'y_valid']]):
        if dsid in ['InsectWingbeat', 'DuckDuckGeese']:
            if verbose: print('There are problems with the original zip file and data cannot correctly downloaded')
            return None, None, None, None
        src_website = 'http://www.timeseriesclassification.com/Downloads'
        if not os.path.isdir(full_tgt_dir):
            if verbose: print(f'Downloading and decompressing data to {full_tgt_dir}...')
            decompress_from_url(f'{src_website}/{dsid}.zip', target_dir=full_tgt_dir, verbose=verbose)
            if verbose: print('...data downloaded and decompressed')
        X_train_df, y_train = load_from_tsfile_to_dataframe(full_tgt_dir/f'{dsid}_TRAIN.ts')
        X_valid_df, y_valid = load_from_tsfile_to_dataframe(full_tgt_dir/f'{dsid}_TEST.ts')
        X_train_ = []
        X_valid_ = []
        for i in range(X_train_df.shape[-1]):
            X_train_.append(stack_padding(X_train_df[f'dim_{i}'])) # stack arrays even if they have different lengths
            X_valid_.append(stack_padding(X_valid_df[f'dim_{i}']))
        X_train = np.transpose(np.stack(X_train_, axis=-1), (0, 2, 1)).astype(np.float32)
        X_valid = np.transpose(np.stack(X_valid_, axis=-1), (0, 2, 1)).astype(np.float32)
#         unique_cats = np.sort(np.unique(y_train))
#         o2i = dict(zip(unique_cats, np.arange(len(unique_cats))))
#         y_train = np.vectorize(o2i.get)(y_train)
#         y_valid = np.vectorize(o2i.get)(y_valid)
        np.save(f'{full_tgt_dir}/X_train.npy', X_train)
        np.save(f'{full_tgt_dir}/y_train.npy', y_train)
        np.save(f'{full_tgt_dir}/X_valid.npy', X_valid)
        np.save(f'{full_tgt_dir}/y_valid.npy', y_valid)
        delete_all_in_dir(full_tgt_dir, exception='.npy')

    if on_disk: mmap_mode='r+'
    else: mmap_mode=None
    X_train = np.load(f'{full_tgt_dir}/X_train.npy', mmap_mode=mmap_mode)
    y_train = np.load(f'{full_tgt_dir}/y_train.npy', mmap_mode=mmap_mode)
    X_valid = np.load(f'{full_tgt_dir}/X_valid.npy', mmap_mode=mmap_mode)
    y_valid = np.load(f'{full_tgt_dir}/y_valid.npy', mmap_mode=mmap_mode)

    if verbose:
        print('X_train:', X_train.shape)
        print('y_train:', y_train.shape)
        print('X_valid:', X_valid.shape)
        print('y_valid:', y_valid.shape, '\n')

    return X_train, y_train, X_valid, y_valid

# Cell
r""""Contains definitions of the methods used by the _BaseDataLoaderIter workers to
collate samples fetched from dataset into Tensor(s).
These **needs** to be in global scope since Py2 doesn't support serializing
static methods.
"""

import torch
import re
from torch._six import container_abcs, string_classes, int_classes

np_str_obj_array_pattern = re.compile(r'[SaUO]')


def np_convert(data):
    r"""Converts each NumPy array data field into a tensor"""
    elem_type = type(data)
    if isinstance(data, torch.Tensor):
        return data
    elif elem_type.__module__ == 'numpy' and elem_type.__name__ != 'str_' \
            and elem_type.__name__ != 'string_':
        # array of string classes and object
        if elem_type.__name__ in ['ndarray', 'memmap'] \
                and np_str_obj_array_pattern.search(data.dtype.str) is not None:
            return data
        return torch.as_tensor(data)
    elif isinstance(data, container_abcs.Mapping):
        return {key: default_convert(data[key]) for key in data}
    elif isinstance(data, tuple) and hasattr(data, '_fields'):  # namedtuple
        return elem_type(*(default_convert(d) for d in data))
    elif isinstance(data, container_abcs.Sequence) and not isinstance(data, string_classes):
        return [default_convert(d) for d in data]
    else:
        return data


np_collate_err_msg_format = (
    "np_collate: batch must contain tensors, numpy arrays, numbers, "
    "dicts or lists; found {}")


def np_collate(batch):
    r"""Puts each data field into a tensor with outer dimension batch size"""

    elem = batch[0]
    elem_type = type(elem)
    if isinstance(elem, torch.Tensor):
        out = None
        if torch.utils.data.get_worker_info() is not None:
            # If we're in a background process, concatenate directly into a
            # shared memory tensor to avoid an extra copy
            numel = sum([x.numel() for x in batch])
            storage = elem.storage()._new_shared(numel)
            out = elem.new(storage)
        return torch.stack(batch, 0, out=out)
    elif elem_type.__module__ == 'numpy' and elem_type.__name__ != 'str_' \
            and elem_type.__name__ != 'string_':
        elem = batch[0]
        if elem_type.__name__ in ['ndarray', 'memmap']:
            # array of string classes and object
            if np_str_obj_array_pattern.search(elem.dtype.str) is not None:
                raise TypeError(np_collate_err_msg_format.format(elem.dtype))
            return np_collate([torch.as_tensor(b) for b in batch])
        elif elem.shape == ():  # scalars
            return torch.as_tensor(batch)
    elif isinstance(elem, float):
        return torch.tensor(batch, dtype=torch.float64)
    elif isinstance(elem, int_classes):
        return torch.tensor(batch)
    elif isinstance(elem, string_classes):
        return batch
    elif isinstance(elem, container_abcs.Mapping):
        return {key: np_collate([d[key] for d in batch]) for key in elem}
    elif isinstance(elem, tuple) and hasattr(elem, '_fields'):  # namedtuple
        return elem_type(*(np_collate(samples) for samples in zip(*batch)))
    elif isinstance(elem, container_abcs.Sequence): # tuple
        transposed = zip(*batch)
        return [np_collate(samples) for samples in transposed]

    raise TypeError(np_collate_err_msg_format.format(elem_type))