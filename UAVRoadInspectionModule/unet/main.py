import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import numpy as np
import cv2
import matplotlib.pyplot as plt
from os.path import split
from os.path import splitext
from jpg2png import jpg2png
from resize import resize
from PIL import Image

DATA_DIR = './D90/'

#resize(DATA_DIR);
'''
jpg2png(DATA_DIR);
'''
x_test_dir = os.path.join(DATA_DIR)
os.system("rm -rf  predict")
os.system("mkdir predict")

from torch.utils.data import DataLoader
from torch.utils.data import Dataset as BaseDataset


class Dataset(BaseDataset):
    """CamVid Dataset. Read images, apply augmentation and prep
essing transformations.
    
    Args:
        images_dir (str): path to images folder
        masks_dir (str): path to segmentation masks folder
        class_values (list): values of classes to extract from segmentation mask
        augmentation (albumentations.Compose): data transfromation pipeline 
            (e.g. flip, scale, etc.)
        preprocessing (albumentations.Compose): data preprocessing 
            (e.g. noralization, shape manipulation, etc.)
    
    """
    
    CLASSES = ['background','surface_defect']
    
    def __init__(
            self, 
            images_dir,
            masks_dir,
            classes=None, 
            augmentation=None, 
            preprocessing=None,
    ):
        self.ids = os.listdir(images_dir)
        self.images_fps = [os.path.join(images_dir, image_id) for image_id in self.ids]
        
        # convert str names to class values on masks
        self.class_values = [self.CLASSES.index(cls.lower()) for cls in classes]
        
        self.augmentation = augmentation
        self.preprocessing = preprocessing
    
    def __getitem__(self, i):
        
        # read data
        image = cv2.imread(self.images_fps[i])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        name = self.images_fps[i]
        

        # apply augmentations
        if self.augmentation:
            sample = self.augmentation(image=image)
            image = sample['image']
        
        # apply preprocessing
        if self.preprocessing:
            sample = self.preprocessing(image=image)
            image = sample['image']
            
        return image, name
        
    def __len__(self):
        return len(self.ids)


# Lets look at data we have


import albumentations as albu

def get_training_augmentation():
    train_transform = [

        albu.HorizontalFlip(p=0.5),

        albu.ShiftScaleRotate(scale_limit=0.5, rotate_limit=0, shift_limit=0.1, p=1, border_mode=0),

        albu.PadIfNeeded(min_height=320, min_width=320, always_apply=True, border_mode=0),
        albu.RandomCrop(height=320, width=320, always_apply=True),

        albu.IAAAdditiveGaussianNoise(p=0.2),
        albu.IAAPerspective(p=0.5),

        albu.OneOf(
            [
                albu.CLAHE(p=1),
                albu.RandomBrightness(p=1),
                albu.RandomGamma(p=1),
            ],
            p=0.9,
        ),

        albu.OneOf(
            [
                albu.IAASharpen(p=1),
                albu.Blur(blur_limit=3, p=1),
                albu.MotionBlur(blur_limit=3, p=1),
            ],
            p=0.9,
        ),

        albu.OneOf(
            [
                albu.RandomContrast(p=1),
                albu.HueSaturationValue(p=1),
            ],
            p=0.9,
        ),
    ]
    return albu.Compose(train_transform)


def get_validation_augmentation():
    """Add paddings to make image shape divisible by 32"""
    test_transform = [
        albu.PadIfNeeded(320, 480)
    ]
    return albu.Compose(test_transform)


def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')


def get_preprocessing(preprocessing_fn):
    """Construct preprocessing transform
    
    Args:
        preprocessing_fn (callbale): data normalization function 
            (can be specific for each pretrained neural network)
    Return:
        transform: albumentations.Compose
    
    """
    
    _transform = [
        albu.Lambda(image=preprocessing_fn),
        albu.Lambda(image=to_tensor, mask=to_tensor),
    ]
    return albu.Compose(_transform)

#### Visualize resulted augmented images and masks


import torch
import numpy as np
import segmentation_models_pytorch as smp

ENCODER = 'se_resnext50_32x4d'
ENCODER_WEIGHTS = 'imagenet'
CLASSES = ['surface_defect']

ACTIVATION = 'sigmoid' # could be None for logits or 'softmax2d' for multicalss segmentation

DEVICE = 'cuda'



preprocessing_fn = smp.encoders.get_preprocessing_fn(ENCODER, ENCODER_WEIGHTS)


best_model = torch.load('./best_model.pth')

# create test dataset
test_dataset = Dataset(
    x_test_dir, 
    'null',
    augmentation=get_validation_augmentation(), 
    preprocessing=get_preprocessing(preprocessing_fn),
    classes=CLASSES,
)



# test dataset without transformations for image visualization
test_dataset_vis = Dataset(
    x_test_dir, 'null', 
    classes=CLASSES,
)
import matplotlib
def addTransparency(img, factor = 0.7 ):
    img = img.convert('RGBA')
    img_blender = Image.new('RGBA', img.size, (0,0,0,0))
    img = Image.blend(img_blender, img, factor)
    return img
def addImage(img1_path, img2_path,path):
    img1 = cv2.imread(img1_path)
    img = cv2.imread(img2_path)
    h, w, _ = img1.shape
    img2 = cv2.resize(img, (w,h), interpolation=cv2.INTER_AREA)
    alpha = 1
    beta = 0.2
    gamma = 0
    img_add = cv2.addWeighted(img1, alpha, img2, beta, gamma)
    cv2.imwrite(path, img_add)
    #cv2.namedWindow('addImage')
    #cv2.imshow('img_add',img_add)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

np.set_printoptions(threshold=np.inf)
for i in range(len(test_dataset)):
    image_vis = test_dataset_vis[i][0]
    image = test_dataset[i][0]
   

    x_tensor = torch.from_numpy(image).to(DEVICE).unsqueeze(0)
    pr_mask = best_model.predict(x_tensor)
    pr_mask = (pr_mask.squeeze().cpu().numpy().round())

    im=Image.fromarray((pr_mask*255).astype(np.uint8))
    print(im.size)
    
    #im.convert('RGBA')
    
    # x=320
    # y=480
    #image.size

    im_source=Image.fromarray((image_vis*255).astype(np.uint8))
    print(im_source.size)

    #im_source.convert('RGBA')
    
    #addImage(image_vis,pr_mask)

    #im=addTransparency(im,0.5)
    #im.save("./predict/"+split(test_dataset[i][1])[1])
    
    #im_opencv1 = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    #im_opencv2 = cv2.cvtColor(np.array(im_source), cv2.COLOR_RGB2BGR)

	#cv2.add(im_opencv1,im_opencv2)
    #gray1 = cv2.cvtColor(im_opencv1, cv2.COLOR_BGR2GRAY)
    #gray2 = cv2.cvtColor(im_opencv2, cv2.COLOR_BGR2GRAY)

    #image = np.concatenate((gray1, gray2)) 
    #cv2.imshow('image', image)

    im.save("./predict/"+"mask_"+split(test_dataset[i][1])[1])
    im_source.save("./predict/"+"source_"+split(test_dataset[i][1])[1])
    addImage("./D90/"+split(test_dataset[i][1])[1],"./predict/"+"mask_"+split(test_dataset[i][1])[1],"./predict/"+split(test_dataset[i][1])[1])

