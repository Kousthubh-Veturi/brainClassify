import tensorflow as tf
import os
import numpy as np
import nibabel as nib
import cv2
from tqdm import tqdm
from sklearn.model_selection import train_test_split


DATASET_PATH = "model/data/BRATS2021_Training_Data"
modalities = ["flair", "t1", "t1ce", "t2"]

def load_and_preprocess_data():
    images, labels = [], []
    patient_list = [p for p in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, p))]
    
    PATCH_SIZE = (64, 64)
    STRIDE = 32
    
    for patient in tqdm(patient_list):
        patient_path = os.path.join(DATASET_PATH, patient)
        
        modality_files = [os.path.join(patient_path, f"{patient}_{m}.nii.gz") for m in modalities]
        if not all(os.path.exists(f) for f in modality_files):
            missing = [f for f in modality_files if not os.path.exists(f)]
            raise FileNotFoundError(f"Modality files not found: {missing}")
            
        seg_file = os.path.join(patient_path, f"{patient}_seg.nii.gz")
        if not os.path.exists(seg_file):
            raise FileNotFoundError(f"Segmentation file not found: {seg_file}")
        
        mask = nib.load(seg_file).get_fdata()
        has_tumor = np.max(mask) > 0
            
        modality_volumes = []
        for file in modality_files:
            img = nib.load(file).get_fdata()
            normalized = (img - np.min(img)) / (np.max(img) - np.min(img))
            modality_volumes.append(normalized)
            
        volume = np.stack(modality_volumes, axis=-1)
        
        relevant_slices = []
        if has_tumor:
            tumor_slices = np.where(np.max(mask, axis=(0,1)) > 0)[0]
            for s in tumor_slices:
                relevant_slices.extend([s-1, s, s+1])
        else:
            relevant_slices = range(0, volume.shape[2], 3)
            
        relevant_slices = [s for s in relevant_slices 
                          if s >= 0 and s < volume.shape[2]]
        
        for slice_idx in relevant_slices:
            slice_data = volume[:, :, slice_idx, :]
            
            for y in range(0, slice_data.shape[0] - PATCH_SIZE[0] + 1, STRIDE):
                for x in range(0, slice_data.shape[1] - PATCH_SIZE[1] + 1, STRIDE):
                    patch = slice_data[y:y+PATCH_SIZE[0], 
                                     x:x+PATCH_SIZE[1], :]
                    
                    if np.mean(patch) > 0.1:
                        images.append(patch)
                        labels.append(1 if has_tumor else 0)
                        
                        if has_tumor:
                            images.append(np.flip(patch, axis=1))
                            labels.append(1)
                            
                            images.append(np.rot90(patch))
                            labels.append(1)
                            
                            contrast_patch = patch * np.random.uniform(0.8, 1.2)
                            contrast_patch = np.clip(contrast_patch, 0, 1)
                            images.append(contrast_patch)
                            labels.append(1)

    images = np.array(images)
    labels = np.array(labels)
    
    pos_samples = np.sum(labels == 1)
    neg_samples = np.sum(labels == 0)
    if neg_samples > pos_samples * 2:
        neg_indices = np.where(labels == 0)[0]
        remove_indices = np.random.choice(neg_indices, 
                                        size=neg_samples - pos_samples * 2, 
                                        replace=False)
        keep_indices = np.array([i for i in range(len(labels)) 
                               if i not in remove_indices])
        images = images[keep_indices]
        labels = labels[keep_indices]

    X_train, X_test, y_train, y_test = train_test_split(
        images, 
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )
    
    return X_train, X_test, y_train, y_test





