import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import imutils
import uuid

# Chuyển RGB sang tên
import webcolors
import time
start = time.time()
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def color_of_image(filepath):
  clusters = 3 # try changing it
  img = cv2.imread(filepath)
  org_img = img
  img = imutils.resize(img,height=200)
  flat_img = np.reshape(img,(-1,3))
  kmeans = KMeans(n_clusters=clusters,random_state=0)
  kmeans.fit(flat_img)
  dominant_colors = np.array(kmeans.cluster_centers_,dtype='uint')
  percentages = (np.unique(kmeans.labels_,return_counts=True)[1])/flat_img.shape[0]

  p_and_c = zip(percentages,dominant_colors)
  p_and_c = sorted(p_and_c,reverse=True)

  image=[]
  for i in range(len(p_and_c)):
    image.append(p_and_c[i][1])
    image[i]=(image[i].tolist())
    image[i].reverse()

  rows = 1000
  cols = int((org_img.shape[0]/org_img.shape[1])*rows)
  img = cv2.resize(org_img,dsize=(rows,cols),interpolation=cv2.INTER_LINEAR)

  copy = img
  cv2.rectangle(copy,(rows//2-250,cols//2-90),(rows//2+100,cols//2+110),(255,255,255),-1)

  final = cv2.addWeighted(img,0.1,copy,0.9,0)
  cv2.putText(final,'Most Dominant Colors',(rows//2-230,cols//2-40),cv2.FONT_HERSHEY_DUPLEX,0.8,(0,0,0),1,cv2.LINE_AA)


  start = rows//2-220
  for i in range(3):
      end = start+70
      final[cols//2:cols//2+70,start:end] = p_and_c[i][1]
      cv2.putText(final,str(i+1),(start+25,cols//2+45),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),1,cv2.LINE_AA)
      start = end+20

  target_img = os.path.join(os.getcwd() , 'static\images')
  unique_filename = str(uuid.uuid4())
  filename = unique_filename+".jpg"
  img_path_kmean = os.path.join(target_img , filename)

#   cv2.imshow("oke",final)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  cv2.imwrite(img_path_kmean,final)
  
  
  return image, filename

def name_main_color(list):
    """
    find color near (Euclidean distance)
    input: code RGB
    output: RGB near
    """
    
    RED= ["lighsalmon","salmon","darksalmon","LightCoral","IndianRed","Crimson","Red","FireBrick","DarkRed"]
    ORANGE= ["Orange","DarkOrange","Coral","Tomato","OrangeRed"]
    YELLOW= ["Gold","Yellow","LightYellow","LemonChiffon","LightGoldenRodYellow","PapayaWhip","Moccasin","PeachPuff","PaleGoldenRod","Khaki","DarkKhaki"]
    GREEN= ["GreenYellow","Chartreuse","LawnGreen", "Lime","LimeGreen","PaleGreen","LightGreen","MediumSpringGreen","SpringGreen","MediumSeaGreen","SeaGreen","ForestGreen","Green","DarkGreen","YellowGreen","OliveDrab","DarkOliveGreen","MediumAquaMarine","DarkSeaGreen","LightSeaGreen","DarkCyan","Teal" ]
    
    
    res="UNKNOWN"
    for i in list:
        color=get_colour_name(i)[1]
        if color.capitalize() in RED or color.capitalize() in ORANGE or color.capitalize() in YELLOW : 
            res="CHÍN"
            break
        if color in GREEN: 
            res="XANH"
            break
    
    
    return res