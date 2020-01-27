import cv2
import pandas as pd
import numpy as np
import os

#get the image path
img_path = input("Enter the image file path including extension: ")
if(img_path == ""):
    img_path = os.path.join(os.getcwd(), 'bg.jpg')
#read the image
img = cv2.imread(img_path)
clicked = False
r = g = b = xpos = ypos = 0
index=["color","color_name","hex","R","G","B"]
# read the csv that downloaded from https://github.com/codebrainz/color-names
colors_df = pd.read_csv('colors.csv', names=index, header=None) 
    
def getColorName(R, G, B):
    """
    if r, g, b is given find the nearest color name possible
    """
    minimum = 10000
    for i in range(len(colors_df)):
        d = abs(R- int(colors_df.loc[i,"R"])) + abs(G- int(colors_df.loc[i,"G"]))+ abs(B- int(colors_df.loc[i,"B"]))
        if(d <= minimum):
            minimum = d
            cname = colors_df.loc[i,"color_name"]
    #following is the formula to find the nearest name possible
    #d = abs(Red – ithRedColor) + (Green – ithGreenColor) + (Blue – ithBlueColor)
    print(cname)
    return cname
        

def draw_function(event, x, y, flags, param):
    """
    from the place of mouse click extract the required data and return bgr colors of that location 
    """
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

    return r, g, b
    
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)
    
while(1):        
    cv2.imshow("image", img)
    if (clicked):

        # draw the rectange on top left 
        # cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle.
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
        # get the color name and rgb values 
        # Creating text string to display ( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)
        #put text is used to display the text
        #cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        #For very light colours we will display text in black colour because light will not display properly in light color bg
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False
    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
