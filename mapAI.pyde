
import Bot

w=400
h=400
sizeP=7
gameOver = 0
score = 100
start = 0
startTime = 0

screenMatrix = list()

player = None
bot = None

class Player:
    def __init__(self,x,y):    
        self.size = 5
        self.view = 3*self.size
        self.speed = 0.02
        self.x = x
        self.y = y
        self.xh = x-self.view 
        self.yh = y-self.view
        
    def draw(self):
        fill(255,0,0)
        circle(self.x,self.y,self.size)
        line(self.x,self.y,self.xh,self.yh)
        noFill()

    def update(self):
        self.x = self.x + (-self.x+self.xh)*self.speed
        self.y = self.y +  (-self.y+self.yh)*self.speed
        vx = -self.x + mouseX
        vy = -self.y + mouseY
        vn = sqrt(vx*vx+vy*vy)
        calibration = 30
        self.xh = self.x + calibration*vx/vn 
        self.yh = self.y + calibration*vy/vn
                
    def increaseSpeed(self):
        self.speed = self.speed + 0.01        
    def decreaseSpeed(self):
        self.speed = self.speed - 0.01   
        if self.speed < 0:
            self.speed = 0.1     

class Bot:
    def __init__(self,x,y):    
        self.size = 5
        self.view = 3*self.size
        self.speed = 0.02
        self.x = x
        self.y = y
        self.xh = x-self.view 
        self.yh = y-self.view
        
    def draw(self):
        fill(255,0,0)
        circle(self.x,self.y,self.size)
        line(self.x,self.y,self.xh,self.yh)
        noFill()

    def checkNorth(self):
        global screenMatrix
        distance = self.view
        j = int(self.y)
        for i in range(int(self.x),int(self.xh)):
            if screenMatrix[i][j] == 1:
                return sqrt(pow(self.x - self.xh,2)+pow(self.y - self.yh,2))
            if self.y - self.yh < 0:
                j = j-1
            else:
                j = j +1
        return distance

    def update(self):
        self.x = self.x + (-self.x+self.xh)*self.speed
        self.y = self.y +  (-self.y+self.yh)*self.speed
        self.xh = self.x + self.view
        self.yh = self.y + self.view        
        # vx = -self.x + mouseX
        # vy = -self.y + mouseY
        # vn = sqrt(vx*vx+vy*vy)
        # calibration = 30
        # self.xh = self.x + calibration*vx/vn 
        # self.yh = self.y + calibration*vy/vn
                
    def increaseSpeed(self):
        self.speed = self.speed + 0.01        
    def decreaseSpeed(self):
        self.speed = self.speed - 0.01   
        if self.speed < 0:
            self.speed = 0.1 

def saveMap():
    global screenMatrix
    writer = createWriter('map.txt')
    for i in range(w):
        for j in range(h):    
            writer.print(screenMatrix[i][j])
    writer.flush()
    writer.close()
            
def loadMap():
    global screenMatrix,w,h
    reader = createReader('map.txt')
    l = str(reader.readLine())
    print(l)
    print(len(l))
    for i in range(w):
        for j in range(h):
            screenMatrix[i][j] = int(l[j+i*w])
        

def setup():
    global w,h,screenMatrix
    
    size(w,h)
    background(100)
    
    for i in range(w):
        screenMatrix.append(range(h))
    for i in range(w):
        for j in range(h):
            screenMatrix[i][j]=0
    
def draw():

    global screenMatrix
    background(100)
    
    global w,h,sizeP,player,gameOver,start,startTime,score,bot

    if gameOver == 0:

        if keyPressed:
            if key == ' ':
                global player
                player = Player(mouseX,mouseY)
            if keyCode == UP:
                player.increaseSpeed()
            elif keyCode == DOWN:
                player.decreaseSpeed()
            if key == 's':
                saveMap()
            elif key == 'l':
                loadMap()
            if key == 'b':
                bot = Bot(mouseX,mouseY)
                        
        
        if mousePressed:        
            for i in range(-int(sizeP/2),int(sizeP/2)):
                for j in range(-int(sizeP/2),int(sizeP/2)):
                    screenMatrix[mouseX+i][mouseY+j]=1
        
    
        for i in range(w):
            for j in range(h):
                if screenMatrix[i][j]==1:
                    if player != None:
                        threshold = 5
                        if player.x <= i+threshold and player.x >= i-threshold and player.y >= j-threshold and player.y <= j+threshold:
                            gameOver = 1
                            print('game over')
                    fill(255)
                    # square(i-sizeP/2,j-sizeP/2,sizeP)
                    point(i,j)
                    noFill()
        
        if bot != None:
            bot.draw()
            bot.update()
            if bot.checkNorth() < bot.view:
                print('detected wall')
        
        if player != None:
            if start ==  0:
                start = 1
                startTime = millis()
            dt = (millis()-startTime)/1000
            if dt > 0:
                startTime = millis()
                score = score-dt
                if score < 0:
                    score = 0
                # pass
            player.draw()
            player.update()
            
    else:
        textSize(40)
        fill(255,0,0)
        text('GAME OVER', 10,h/2)
        noFill()        
            
         
    textSize(20)
    fill(255)
    text('fps: '+str(frameRate), 10,h/10)
    if player != None:
        dt = millis()-startTime
        if dt > 0:
            text('score: '+str(score), w-w/3, h/10)
    noFill()
