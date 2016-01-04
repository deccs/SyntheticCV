import vapory
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imsave

class AmbientLight(vapory.POVRayElement):
    def __init__(self,color):
        self.color=color
    def __str__(self):
        return 'ambient_light rgb <%d,%d,%d>'%(self.color[0], self.color[1],self.color[2])       


def generateStereoPair(scene_left,scene_right,useRadiosity):
    
    #camera_left = vapory.Camera( 'location', [0-delta,0,-5], 'look_at', [0-delta,0,0] ,'focal_point', [0, 0, 0],'aperture', 0.4,'blur_samples', 50) # <= Increase for better quality
    #camera_right = vapory.Camera( 'location', [0+delta,0,-5], 'look_at', [0+delta,0,0],'focal_point', [0, 0, 0],'aperture', 0.4, 'blur_samples', 50) # <= Increase for better quality
    
    if useRadiosity:
        radiosity = vapory.Radiosity(
            'brightness', 2.0,
            'count', 100,
            'error_bound', 0.15,
            'gray_threshold', 0.0,
            'low_error_factor', 0.2,
            'minimum_reuse', 0.015,
            'nearest_count', 10,
            'recursion_limit', 5,
            'adc_bailout', 0.01,
            'max_sample', 0.5,
            'media off',
            'normal off',
            'always_sample', 1,
            'pretrace_start', 0.08,
            'pretrace_end', 0.01)        
        scene_left.global_settings=[radiosity]
        scene_right.global_settings=[radiosity]
    else:
        scene_left.global_settings=[]
        scene_right.global_settings=[]
        
    print str(scene_left)
    image_left  = scene_left.render ( width=300, height=200,antialiasing = 0.001,quality=10)
    image_right = scene_right.render( width=300, height=200,antialiasing = 0.001,quality=10)
    return image_left,image_right


def generateScenes():
    delta=0.1
    nbcubes=100
    
    light = vapory.LightSource( [2,4,-7], 'color', [2,2,2] )
    ambientlight=AmbientLight([1,1,1])
    

    
    objects=[light]
    rotation=[np.random.rand()*180,np.random.rand()*180,np.random.rand()*180]

    
    for k in range(nbcubes):   
        center=[0+np.random.randn()*3,0+np.random.randn()*2,0+np.random.rand()*2]
        #sphere=vapory.Sphere( center, 0.5, vapory.Pigment( 'color', [1,1,1]))
        #sphere=vapory.Sphere( center, 0.5, vapory.Pigment( 'color', np.random.rand(3) ),vapory.Finish('phong', 0.8,'reflection', 0.5)) 
        #objects.append(sphere) 
        #center=[0+np.random.randn()*2,0+np.random.randn()*2,0+np.random.rand()*2]
        
        #objects.append(vapory.Box( [-0.5,-0.5,-0.5], [ 0.5,0.5,0.5 ], 'rotate',rotation , 'translate',center ,vapory.Pigment( 'color', np.random.rand(3) ),vapory.Finish('phong', 0.8,'reflection', 0.0)))
    
    
        #center=[0+np.random.randn()*2,0+np.random.randn()*2,0+np.random.rand()*1.0]
    
        #sphere=vapory.Sphere( center, 0.5, vapory.Pigment( 'color', [1,1,1]))
        #sphere=vapory.Sphere( center, 0.5, vapory.Pigment( 'color', np.random.rand(3) ),vapory.Finish('phong', 0.8,'reflection', 0.5)) 
        #objects.append(sphere) 
        center=[0+np.random.randn()*3,0+np.random.randn()*2,0+np.random.rand()*2]
        
        #objects.append(vapory.Box( [-0.5,-0.5,-0.5], [ 0.5,0.5,0.5 ], 'rotate',rotation , 'translate',center ,vapory.Pigment( 'color', np.random.rand(3) ),vapory.Finish('phong', 0.8,'reflection', 0.1)))
        #objects.append(vapory.Box( [-0.5,-0.5,-0.5], [ 0.5,0.5,0.5 ], 'rotate',rotation , 'translate',center ,vapory.Pigment( 'color',[1,1,1] )))
        #objects.append(vapory.Box( [-0.5,-0.5,-0.5], [ 0.5,0.5,0.5 ], 'rotate',rotation , 'translate',center,vapory.Texture('Rosewood')))
        objects.append(vapory.Box( [-0.5,-0.5,-0.5], [ 0.5,0.5,0.5 ], 'rotate',rotation , 'translate',center,vapory.Texture('White_Marble')))
    #ground = vapory.Plane([0,1,0],0, vapory.Texture('Rosewood'))
    #objects.append(ground)
    camera_left = vapory.Camera( 'location', [0-delta,0,-5], 'look_at', [0-delta,0,0] ) # <= Increase for better quality
    camera_right = vapory.Camera( 'location', [0+delta,0,-5], 'look_at', [0+delta,0,0]) # <= Increase for better quality
    
    scene_left  = vapory.Scene( camera_left, objects= objects,included = ["colors.inc", "textures.inc"],)
    scene_right = vapory.Scene( camera_right, objects= objects,included = ["colors.inc", "textures.inc"],)
    return scene_left,scene_right

def bilinear_interpolate(im, x, y):
    """standard bilinear interpolation of an image over a set of non integer coordinates, 
    might be found"""
    x = np.asarray(x)
    y = np.asarray(y)

    x0 = np.floor(x).astype(int)
    x1 = x0 + 1
    y0 = np.floor(y).astype(int)
    y1 = y0 + 1

    x0 = np.clip(x0, 0, im.shape[1]-1);
    x1 = np.clip(x1, 0, im.shape[1]-1);
    y0 = np.clip(y0, 0, im.shape[0]-1);
    y1 = np.clip(y1, 0, im.shape[0]-1);

    Ia = im[ y0, x0 ]
    Ib = im[ y1, x0]
    Ic = im[ y0, x1 ]
    Id = im[ y1, x1 ]

    wa = (x1-x) * (y1-y)
    wb = (x1-x) * (y-y0)
    wc = (x-x0) * (y1-y)
    wd = (x-x0) * (y-y0)

    return wa*Ia + wb*Ib + wc*Ic + wd*Id

def estimateDisparity(image_left,image_right,method='SGBM'):
    if method=='SGBM':
        import cv2
        
        disparityrange=[0,15]
        
        ndisparities=int(np.ceil(disparityrange[1]-disparityrange[0])	)
        ndisparities=16*int(np.ceil(float(ndisparities)/16))
        minDisparity=int(np.floor(disparityrange[0]))
        #stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=ndisparities, SADWindowSize=15)
        #stereo = cv2.StereoSGBM(minDisparity=mindisparity,numDisparities=ndisparities, SADWindowSize=15,P1=10000,P2=0)
        stereo = cv2.StereoSGBM(minDisparity=minDisparity,numDisparities=ndisparities, SADWindowSize=3,P1=30,P2=30)
        
        right_disparity = stereo.compute(image_left[:,:,0],image_right[:,:,0])# does not work in color...
        right_disparity=right_disparity/16.
    elif method=='BM':
  
    
    
        stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=ndisparities,  SADWindowSize=5)
        right_disparity = stereo.compute(image_left[:,:,0],image_right[:,:,0],disptype=cv2.CV_32F)# does not work in color...
    return right_disparity
 
    
def  disparityEvaluation(image_right,right_disparity): 
    # wrap images
    
    x,y=np.meshgrid(np.arange(right_disparity.shape[1]),np.arange(right_disparity.shape[0]))
    x2=-right_disparity+ x
    image_left2=bilinear_interpolate(image_right[:,:,0], x2,y)
    image_left2=np.tile(image_left2[:,:,None],(1,1,3)).astype(np.uint8)
    plt.figure()
    print "done"
    return {'image_left2':image_left2}

    


if __name__ == "__main__":
    
    scene_left,scene_right=generateScenes()
    image_left,image_right=generateStereoPair(scene_left,scene_right,useRadiosity=True)
    right_disparity=estimateDisparity(image_left,image_right,method='SGBM')
    plt.ion()
    plt.figure()
    plt.imshow(right_disparity,'gray')
    plt.show()
        
    d=disparityEvaluation(image_right,right_disparity) 
    plt.imshow(d['image_left2'])
    imsave("image_left2.png",d['image_left2'])
    print "done"            
    imsave('image_left2.png',image_left)
    imsave('image_right2.png',image_right )

    plt.ion()
    plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(image_left)
    plt.subplot(2,2,2)
    plt.imshow(image_right)
    plt.subplot(2,2,4)
    plt.imshow(right_disparity)
    plt.subplot(2,2,3)
    plt.imshow(d['image_left2'])











