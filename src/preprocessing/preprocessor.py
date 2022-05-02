import numpy as np
import cv2
import pandas as pd
import os
from tqdm import tqdm


# preprocesses data by converting to grayscale, inverting, finding bounding boxes, then resizing to 28x28
def load_images_from_folder(folder,img_w,img_h):
    train_data=[]
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),cv2.IMREAD_GRAYSCALE)
        img=~img
        if img is not None:
            _, thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
            _, ctrs, _ =cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            cnt=sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
            w=int(img_w)
            h=int(img_h)
            maxi=0
            for c in cnt:
                x,y,w,h=cv2.boundingRect(c)
                maxi=max(w*h,maxi)
                if maxi==w*h:
                    x_max=x
                    y_max=y
                    w_max=w
                    h_max=h
            im_crop= thresh[y_max:y_max+h_max+10, x_max:x_max+w_max+10]
            im_resize = cv2.resize(im_crop,(img_w,img_h))
            im_resize=np.reshape(im_resize,(img_w*img_h,1))
            train_data.append(im_resize)
    return train_data


# determines how to sort the dir list
def sortby(x):
    try:
        return int(x[0].split(' ')[0])
    except ValueError:
        return float('inf')


# sorted dir list
sorted_dir = [dir for dir in sorted(os.listdir('data'),key=sortby) if not dir.startswith('.')]


# creating a dictionary of (dir_name,label) pairs
def create_label_map(dataset_path):
    label = 0
    label_map = {}
    for dir in sorted_dir:
        label_map[dir] = label
        label+=1
    return label_map


# creates the csv file for the image data
def main(path, img_w,img_h,csv_name):
    size = img_h*img_w
    label_map = create_label_map(path)
    initial_data = ['pixel' + str(i) for i in range(size)]
    initial_data.append('class')
    initial_data = np.reshape(initial_data,(1,size+1))

    for dir in tqdm(sorted_dir,bar_format='{l_bar}{bar:20}'):
        img_data = load_images_from_folder(os.path.join(path,dir),img_w,img_h)
        for i in range(0,len(img_data)):
            img_data[i] = np.append(img_data[i],[label_map.get(dir)])
        initial_data = np.concatenate((initial_data,img_data))

    df = pd.DataFrame(initial_data,index=None)
    df.columns = df.iloc[0]
    df = df[1:]
    df.to_csv(csv_name,index=False)


if __name__ == '__main__':
    img_w = 32
    img_h = 32
    csv_name = 'final.csv'
    main('data',img_w,img_h,csv_name)
