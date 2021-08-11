import svgwrite
import math


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
#line ((sx1,sx2),(ex1,ex2))
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




cameraFocalDist = 350	#mm
frontStdSize = 200		#mm
rearStdSize = 200 		#mm
foldDist = 30			#mm
flexFactor = 1.7
numFolds = math.ceil((cameraFocalDist * flexFactor)/foldDist)
bellowsLength = numFolds*foldDist
dash = 5
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

# dwg.add(dwg.line(frontStrRgt,frontStrLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
# dwg.add(dwg.line(frontStrRgt,frtDwnRgt, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
# dwg.add(dwg.line(frontStrLft,frtDwnLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(frtDwnRgt,frtDwnLft, stroke=svgwrite.rgb(10, 10, 16, '%')))

#Read standard flap pre
rearStrCtr = (str(canvasWidth/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
rearStrLft = (str((canvasWidth/2) - rearStdSize/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
rearStrRgt = (str((canvasWidth/2) + rearStdSize/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
rDwnLft = (str((canvasWidth/2) - rearStdSize/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2) - foldDist) + 'mm')
rDwnRgt = (str((canvasWidth/2) + rearStdSize/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2) - foldDist) + 'mm')


# dwg.add(dwg.line(rearStrRgt,rearStrLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
# dwg.add(dwg.line(rearStrRgt,rDwnRgt, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
# dwg.add(dwg.line(rearStrLft,rDwnLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(rDwnRgt,rDwnLft, stroke=svgwrite.rgb(10, 10, 16, '%')))


# side lines inner
dwg.add(dwg.line(rDwnRgt,frtDwnRgt, stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line(rDwnLft,frtDwnLft, stroke=svgwrite.rgb(10, 10, 16, '%')))

#side lines outer
sideFrtLft = (str((canvasWidth/2) - frontStdSize/2 - foldDist/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2) + foldDist) + 'mm')
sideRearLft = (str((canvasWidth/2) - rearStdSize/2 - foldDist/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2) - foldDist) + 'mm')
dwg.add(dwg.line(frtDwnLft,sideFrtLft, stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line(rDwnLft,sideRearLft, stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line(sideFrtLft,sideRearLft, stroke=svgwrite.rgb(10, 10, 16, '%')))

sideFrtRgt = (str((canvasWidth/2) + frontStdSize/2 + foldDist/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2) + foldDist) + 'mm')
sideRearRgt = (str((canvasWidth/2) + rearStdSize/2 + foldDist/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2) - foldDist) + 'mm')
dwg.add(dwg.line(frtDwnRgt,sideFrtRgt, stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line(rDwnRgt,sideRearRgt, stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line(sideFrtRgt,sideRearRgt, stroke=svgwrite.rgb(10, 10, 16, '%')))

newFrontStrLft = (str((canvasWidth/2) - frontStdSize/2 - foldDist/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2)) + 'mm')
newFrontStrRgt = (str((canvasWidth/2) + frontStdSize/2 + foldDist/2) + 'mm', str((canvasHeight/2) - (bellowsLength/2)) + 'mm')
newRearStrLft =  (str((canvasWidth/2) - rearStdSize/2 - foldDist/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
newRearStrRgt =  (str((canvasWidth/2) + rearStdSize/2 + foldDist/2) + 'mm', str((canvasHeight/2) + (bellowsLength/2)) + 'mm')
dwg.add(dwg.line(sideFrtLft,newFrontStrLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(sideRearLft,newRearStrLft, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(sideFrtRgt,newFrontStrRgt, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(sideRearRgt,newRearStrRgt, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(newFrontStrLft,newFrontStrRgt, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])
dwg.add(dwg.line(newRearStrLft,newRearStrRgt, stroke=svgwrite.rgb(10, 10, 16, '%'))).dasharray([dash,dash])

drawCreateVericalLine((sideRearRgt,sideRearLft),dwg, foldDist, numFolds, (rDwnRgt,frtDwnRgt), (rDwnLft,frtDwnLft,), (sideFrtLft,sideRearLft), (sideFrtRgt,sideRearRgt))
# print line_intersection((A, B), (C, D))

dwg.save()

