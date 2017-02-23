from PIL import Image
from PIL import PSDraw
from PIL import ImageFont
from PIL import ImageDraw

# mon should be a dictionary containing the
# name, hunger, and happiness.
def generate_mon_badge(owner, mon):
    name = mon["name"]
    hunger = ("#" * int(mon["hunger"])).ljust(12)
    happy = ("#" * int(mon["happy"])).ljust(12)
    
    #WxH, template background
    base = Image.new("RGB", (410, 170))
    
    #color background
    base.paste((100,100,100), [0,0,base.size[0],base.size[1]])
    
    #draw avatar frame
    draw = ImageDraw.Draw(base)
    draw.rectangle([(15,15),(154,154)], fill=(0,0,0))
    
    #draw text
    font = ImageFont.truetype("font/joystix.ttf", 20)
    draw.text((170, 12), "NAME: {0}".format(name),(0,0,0),font=font)
    draw.text((170, 42), "HAPPINESS",(0,0,0),font=font)
    draw.text((170, 72),"[{0}]".format(happy),(0,0,255),font=font)
    draw.text((170, 102), "HUNGER",(0,0,0),font=font)
    draw.text((170, 132),"[{0}]".format(hunger),(0,255,0),font=font)
    
    #avatar image, currently 32x32
    face = Image.open("res/faro.png")
    #scaled x4 (resize can take a second argument for AA)
    face = face.resize((128,128))
    #paste face onto background (x,y)
    base.paste(face, (21,21))
    #save picture
    base.save("out/" + owner + ".png")
    #show picture for testing purposes.
    #base.show()
