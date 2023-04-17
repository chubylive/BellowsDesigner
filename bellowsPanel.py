import svgwrite
import math
import sys

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
def slopeLine (line):
	((x1, y1), (x2, y2)) = line
	return math.atan((y2 - y1)/(x2 - x1))
def lineToStr(line):
	((sx1,sy1),(ex1,ey1))  =  line
	strIntrLine = ((str(sx1) + "mm", str(sy1) + "mm"),(str(ex1) + "mm", str(ey1) + "mm") )
	return strIntrLine

def p1(line):
	((sx1,sy1),(ex1,ey1))  =  line
	return (sx1,sy1)

def p2(line):
	((sx1,sy1),(ex1,ey1))  =  line
	return (ex1,ey1)

def pointToStr(point):
	(sx1,sy1) = point
	return (str(sx1) + "mm", str(sy1) + "mm")

def pointAngleLine(point,angle,length_mm):
	# print("draw Slope: ", angle * 180/math.pi)
	(x1,y1) = point
	return(point,(x1 + length_mm * math.cos(angle), y1 + length_mm * math.sin(angle)))

def drawLine(line, dwgIn, r = 10, g = 10 , b = 16):
	((sx1,sy1),(ex1,ey1))  =  line
	strLine = ((str(sx1) + "mm", str(sy1) + "mm"),(str(ex1) + "mm", str(ey1) + "mm") )
	(pointA,pointB) = strLine
	dwgIn.add(dwg.line(pointA,pointB, stroke=svgwrite.rgb(r, g, b, '%')))

def drawStrLine(line, dwgIn):
	(pointA,pointB) = line
	dwgIn.add(dwg.line(pointA,pointB, stroke=svgwrite.rgb(10, 10, 16, '%')))

def drawLineUptoLine(line1, line2, dwgIn, opt = True):

	point = line_intersection(line1,line2)
	if opt == True : 
		dwgIn.add(dwg.line(pointToStr(line1[0]),pointToStr(point), stroke=svgwrite.rgb(10, 10, 16, '%')))
	else:
		dwgIn.add(dwg.line(pointToStr(line1[1]),pointToStr(point), stroke=svgwrite.rgb(10, 10, 16, '%')))
	return point
def drawCreateVericalLine(startLine, dwgIn, foldDistIn, numFoldsIn, rightLineInner, leftLineInner, rightLineOuter, leftLineOuter,):
	foldDistIn = foldDistIn/2
	(((strSx),(strSy)),((strEx),(strEy))) = startLine
	((sx,sy),(ex,ey)) = ((float(strSx.replace("mm","")),float(strSy.replace("mm",""))),(float(strEx.replace("mm","")),float(strEy.replace("mm",""))))
	sign = 1
	((psx,psy),(pex,pey))  = ((sx,sy),(ex,ey)) 
	for x in range((2*numFoldsIn) - 4):
		intrLine = ((sx, sy - (foldDistIn*sign)) ,(ex ,ey - (foldDistIn*sign)))
		((sx1,sy1),(ex1,ey1))  =  intrLine
		strIntrLine = ((str(sx1) + "mm", str(sy1) + "mm"),(str(ex1) + "mm", str(ey1) + "mm") )
		(intrPA,intrPB) = strIntrLine
		# dwgIn.add(dwg.line(intrPA,intrPB, stroke=svgwrite.rgb(255, 10, 16, '%')))
		if(x % 2 == 0): #intersect even
			(((strSx2),(strSy2)),((strEx2),(strEy2))) = leftLineInner
			((sx2,sy2),(ex2,ey2)) = ((float(strSx2.replace("mm","")),float(strSy2.replace("mm",""))),(float(strEx2.replace("mm","")),float(strEy2.replace("mm",""))))
			lftInner = ((sx2,sy2),(ex2,ey2))
			(((strSx3),(strSy3)),((strEx3),(strEy3))) = rightLineInner
			((sx3,sy3),(ex3,ey3)) = ((float(strSx3.replace("mm","")),float(strSy3.replace("mm",""))),(float(strEx3.replace("mm","")),float(strEy3.replace("mm",""))))
			rgtInner = ((sx3,sy3),(ex3,ey3))
			lftPoint = line_intersection(lftInner,intrLine)
			rgtPoint = line_intersection(rgtInner,intrLine)
			dwgIn.add(dwg.line(pointToStr(lftPoint),pointToStr(rgtPoint), stroke=svgwrite.rgb(10, 10, 16, '%')))
			dwgIn.add(dwg.line(pointToStr(lftPoint),pointToStr((pex,pey)), stroke=svgwrite.rgb(10, 10, 16, '%')))
			dwgIn.add(dwg.line(pointToStr(rgtPoint),pointToStr((psx,psy)), stroke=svgwrite.rgb(10, 10, 16, '%')))
			((psx,psy),(pex,pey)) = (lftPoint,rgtPoint)
		else: 
			(((strSx2),(strSy2)),((strEx2),(strEy2))) = leftLineOuter
			((sx2,sy2),(ex2,ey2)) = ((float(strSx2.replace("mm","")),float(strSy2.replace("mm",""))),(float(strEx2.replace("mm","")),float(strEy2.replace("mm",""))))
			lftOuter = ((sx2,sy2),(ex2,ey2))
			(((strSx3),(strSy3)),((strEx3),(strEy3))) = rightLineOuter
			((sx3,sy3),(ex3,ey3)) = ((float(strSx3.replace("mm","")),float(strSy3.replace("mm",""))),(float(strEx3.replace("mm","")),float(strEy3.replace("mm",""))))
			rgtOuter = ((sx3,sy3),(ex3,ey3))
			lftPoint = line_intersection(lftOuter,intrLine)
			rgtPoint = line_intersection(rgtOuter,intrLine)
			dwgIn.add(dwg.line(pointToStr(lftPoint),pointToStr(rgtPoint), stroke=svgwrite.rgb(10, 10, 16, '%')))
			dwgIn.add(dwg.line(pointToStr(lftPoint),pointToStr((pex,pey)), stroke=svgwrite.rgb(10, 10, 16, '%')))
			dwgIn.add(dwg.line(pointToStr(rgtPoint),pointToStr((psx,psy)), stroke=svgwrite.rgb(10, 10, 16, '%')))
			((psx,psy),(pex,pey)) = (lftPoint,rgtPoint)

		((sx,sy),(ex,ey)) = intrLine

def lineStrToDouble(line):
	(((strSx),(strSy)),((strEx),(strEy))) = line
	return ((float(strSx.replace("mm","")),float(strSy.replace("mm",""))),(float(strEx.replace("mm","")),float(strEy.replace("mm",""))))

def drawPleats(startLine, dwgIn, foldDistIn, numFoldsIn, rightLineInner, leftLineInner, slope, sign):
	(((strSx),(strSy)),((strLeftx),(strLefty))) = startLine
	# dwgIn.add(dwg.line(((strSx),(strSy)),((strLeftx),(strLefty)), stroke=svgwrite.rgb(255, 10, 16, '%')))
	((sx,sy),(ex,ey)) = ((float(strSx.replace("mm","")),float(strSy.replace("mm",""))),(float(strLeftx.replace("mm","")),float(strLefty.replace("mm",""))))
	((right_x,right_y),(left_x,left_y)) = ((sx,sy),(ex,ey))
	leftPrevIntrLine = {}
	leftPrevIntrLineOther = {}
	rightPrevIntrLine = {}
	rightPrevIntrLineOther = {}
	leftPoint = {}
	rightPoint = {}
	isUpPleat = False
	for x in range((2*numFoldsIn) +1):
		intrLine = ((sx, sy - (foldDistIn*0.5)) ,(ex ,ey - (foldDistIn*0.5)))
		((sx1,sy1),(ex1,ey1))  =  intrLine
		strIntrLine = ((str(sx1) + "mm", str(sy1) + "mm"),(str(ex1) + "mm", str(ey1) + "mm") )
		
		lftPoint = line_intersection(lineStrToDouble(leftLineInner),intrLine)
		rgtPoint = line_intersection(lineStrToDouble(rightLineInner),intrLine)
		(intrPA,intrPB) = (pointToStr(lftPoint), pointToStr(rgtPoint))
		
		
		# if(x % 2 == 0 or x % 2 != 0): #intersect even
		if(x % 2 == 0 ):
				# dwgIn.add(dwg.line(intrPA,intrPB, stroke=svgwrite.rgb(255, 10, 16, '%')))
			# line at angle to intrLine
				#calc line at angle from bottom left
				if isUpPleat == False:
					leftPleatLine = pointAngleLine(((left_x),(left_y)), (-slope + math.pi/4) * sign, 10000)
					leftPleatLineOther = pointAngleLine(((left_x),(left_y)), -(slope + math.pi/4) * sign, -10000)
					rightPleatLine = pointAngleLine(((right_x),(right_y)), -(-slope + math.pi/4) * sign, -10000)
					rightPleatLineOther = pointAngleLine(((right_x),(right_y)), (slope + math.pi/4) * sign, -10000)

					isUpPleat = True
				else:
					leftPleatLine = pointAngleLine(((left_x),(left_y)), -(slope + math.pi/4) * sign, 10000)
					leftPleatLineOther = pointAngleLine(((left_x),(left_y)), (-slope + math.pi/4) * sign, -10000)
					rightPleatLine = pointAngleLine(((right_x),(right_y)), (slope + math.pi/4) * sign, -10000)
					rightPleatLineOther = pointAngleLine(((right_x),(right_y)), -(-slope + math.pi/4) * sign, -10000)
					isUpPleat = False
				
				if(leftPrevIntrLine != {} ):
					if isUpPleat == False:
						drawLineUptoLine(leftPrevIntrLine,leftPleatLine, dwgIn)
						leftPoint = drawLineUptoLine(leftPleatLine,leftPrevIntrLine, dwgIn)
						drawLineUptoLine(rightPrevIntrLine,rightPleatLine, dwgIn)
						rightPoint = drawLineUptoLine(rightPleatLine,rightPrevIntrLine, dwgIn)
					if isUpPleat == True:
						drawLineUptoLine(leftPrevIntrLineOther,leftPleatLineOther, dwgIn)
						leftPoint = drawLineUptoLine(leftPleatLineOther,leftPrevIntrLineOther, dwgIn)
						drawLineUptoLine(rightPrevIntrLineOther,rightPleatLineOther, dwgIn)
						rightPoint = drawLineUptoLine(rightPleatLineOther,rightPrevIntrLineOther, dwgIn)
					dwg.add(dwg.line(pointToStr(leftPoint),pointToStr(rightPoint), stroke=svgwrite.rgb(10, 100, 170, '%'))).dasharray([dash,dash])
		else:
			dwgIn.add(dwg.line(intrPA,intrPB, stroke=svgwrite.rgb(10, 100, 170, '%'))).dasharray([dash,dash])
		
		((sx,sy),(ex,ey)) = intrLine
		(left_x),(left_y) = (lftPoint[0],lftPoint[1])
		(right_x),(right_y) = (rgtPoint[0],rgtPoint[1])
		# print(leftPleatLine)
		leftPrevIntrLine = leftPleatLine
		leftPrevIntrLineOther = leftPleatLineOther
		rightPrevIntrLine = rightPleatLine
		rightPrevIntrLineOther = rightPleatLineOther

cameraFocalDist = 120	#mm this defines the length of the side without flexfactor
frontStdSize =	53 - 19.1 #mm 53 37  # 53 + 15.8
rearStdSize =  70.5 - 17.70  #114 	 # 114 + 20.7mm
foldDist = 18.5 			#mm
flexFactor = 2
flexPanelSideLength = cameraFocalDist *flexFactor
cSqr = flexPanelSideLength * flexPanelSideLength
aSqr = (rearStdSize/2 - frontStdSize/2) * (rearStdSize/2 - frontStdSize/2)
panelLength = math.sqrt(cSqr - aSqr)
numFolds = math.ceil((panelLength )/foldDist)

# bellowsLength = 

bellowsLength = (panelLength )
dash = 6
# print("calulated number of folds: ", numFolds)
print("Bellows Paramerters: Front Standard: ", frontStdSize, " Read Standard: ", 
	rearStdSize, " Number of Folds: " , numFolds, " Bellows Length: ", bellowsLength)
if (rearStdSize > frontStdSize):
	canvasWidth = 2 * rearStdSize
else:
	canvasWidth = 1.5 * frontStdSize

canvasHeight = 1.5 * bellowsLength

dwg = svgwrite.Drawing('test.svg', size=(str(canvasWidth) + 'mm', str(canvasHeight) + 'mm'), profile='tiny')

# Midline
center = (str(canvasWidth/2) + 'mm', str(canvasHeight/2) + 'mm')
bellowsMidTop = (str(canvasWidth/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2)) + 'mm')
bellowsMidBtm = (str(canvasWidth/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
dwg.add(dwg.line(bellowsMidBtm,bellowsMidTop, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])

#Front standard flap pre
frontStrCtr = (str(canvasWidth/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2)) + 'mm')
frontStrLft = (str((canvasWidth/2) - frontStdSize/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2)) + 'mm')
frontStrRgt = (str((canvasWidth/2) + frontStdSize/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2)) + 'mm')
frtDwnLft = (str((canvasWidth/2) - frontStdSize/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2) + foldDist) + 'mm')
frtDwnRgt = (str((canvasWidth/2) + frontStdSize/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2) + foldDist) + 'mm')

#top flap
# dwg.add(dwg.line(frontStrRgt,frontStrLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
# dwg.add(dwg.line(frontStrRgt,frtDwnRgt, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
# dwg.add(dwg.line(frontStrLft,frtDwnLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(frontStrLft,frontStrRgt, stroke=svgwrite.rgb(10, 10, 16, '%')))

#Read standard flap pre
rearStrCtr = (str(canvasWidth/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
rearStrLft = (str((canvasWidth/2) - rearStdSize/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
rearStrRgt = (str((canvasWidth/2) + rearStdSize/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
rDwnLft = (str((canvasWidth/2) - rearStdSize/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2) - foldDist) + 'mm')
rDwnRgt = (str((canvasWidth/2) + rearStdSize/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2) - foldDist) + 'mm')

#bottom flap
# dwg.add(dwg.line(rearStrRgt,rearStrLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
# dwg.add(dwg.line(rearStrRgt,rDwnRgt, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
# dwg.add(dwg.line(rearStrLft,rDwnLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(rearStrLft,rearStrRgt, stroke=svgwrite.rgb(10, 10, 16, '%')))

# side lines inner
dwg.add(dwg.line(frontStrRgt,rearStrRgt, stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line(frontStrLft,rearStrLft, stroke=svgwrite.rgb(10, 10, 16, '%')))
 

slope = slopeLine(lineStrToDouble((rearStrRgt,frontStrRgt)))
print("Slope right line deg: ", -90 + (slope * 180/math.pi))

# drawCreateVericalLine((sideRearRgt,sideRearLft),dwg, foldDist, numFolds, (rDwnRgt,frtDwnRgt), (rDwnLft,frtDwnLft,), (sideFrtLft,sideRearLft), (sideFrtRgt,sideRearRgt))
# drawPleats((rearStrRgt, rearStrLft), dwg, bellowsLength/numFolds, numFolds, (rearStrRgt,frontStrRgt), (rearStrLft,frontStrLft), slope, 1)
drawPleats((rearStrRgt, rearStrLft), dwg, bellowsLength/numFolds, numFolds, (rearStrRgt,frontStrRgt), (rearStrLft,frontStrLft), -slope, -1)

# print line_intersection((A, B), (C, D))

dwg.save()

