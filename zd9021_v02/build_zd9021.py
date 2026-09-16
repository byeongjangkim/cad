"""ZD 9021-V3 reference reconstruction. Run with FreeCAD bundled Python.
Published dimensions are distinguished from estimated geometry in every component.
"""
import os, sys, json, math, csv
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as A
import Part
from FreeCAD import Vector as V
OUT=os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT+'/parts',exist_ok=True)
D={
 'Wheelbase':370.0,'OverallWidth':430.0,'TireDiameter':145.0,'TireWidth':69.0,
 'RimDiameter':87.0,'WheelHexAF':17.0,'ChassisLength':446.0,'ChassisWidth':132.0,
 'ChassisThickness':3.0,'GroundClearance':65.0,'FrontShockEyes':110.0,
 'RearShockEyes':132.0,'ShockDiameter':25.0,'ShockHole':3.0,
 'ShaftDiameter':5.0,'DeckLength':400.0,'DeckWidth':300.0,'DeckThickness':3.0,
 'DeckHeight':245.0,'LowerPivotY':36.0,'OuterPivotY':151.0,'LowerPivotZ':68.0,
 'UpperPivotZ':101.0,'ShockLowerY':122.0,'ShockLowerZ':74.0,'ShockUpperY':57.0,
 'FrontTowerThickness':4.0,'RearTowerThickness':4.0,'OverallLength':550.0,
 'ServoLength':40.0,'ServoWidth':20.0,'ServoHeight':42.0}
config=OUT+'/dimensions.json'
if os.path.exists(config): D.update(json.load(open(config)))
json.dump(D,open(config,'w'),indent=2)
doc=A.newDocument('ZD9021V3_ReferenceV02')
sheet=doc.addObject('Spreadsheet::Sheet','Dimensions')
sheet.Label='00 Dimension register - edit dimensions.json and rebuild'
for col,val in [('A1','Parameter'),('B1','mm'),('C1','Evidence')]:sheet.set(col,val)
for i,(k,v) in enumerate(D.items(),2):
 sheet.set('A'+str(i),k);sheet.set('B'+str(i),str(v));sheet.setAlias('B'+str(i),k)
 sheet.set('C'+str(i),'ESTIMATED / CUSTOM' if k.startswith(('Deck','Lower','Outer','Upper','ShockLower','ShockUpper','FrontTower','RearTower')) else 'PUBLISHED; see SOURCES.md')
sheet.set('C4','145 mm chosen within user range 140-145')
for i,k in enumerate(D,2):
 if k in ['OverallLength','GroundClearance']:sheet.set('C'+str(i),'USER TARGET / selected within requested range')
lib=doc.addObject('App::Part','ComponentLibrary');lib.Label='01 Component definitions - hidden'
assy=doc.addObject('App::Part','RollingChassis');assy.Label='02 ZD 9021-V3 rolling chassis - reconstructed'
custom=doc.addObject('App::Part','RobotDeck');custom.Label='03 Optional robot deck - custom, unverified mounts'
expl=doc.addObject('App::Part','Exploded');expl.Label='04 Exploded rolling chassis - toggle visibility'
groups={}
for name in ['Chassis','FrontSuspension','RearSuspension','Drivetrain','Wheels','BatteryTray','Steering']:
 g=doc.addObject('App::Part',name);assy.addObject(g);groups[name]=g
silver=(0.68,0.70,0.72); black=(0.13,0.15,0.18); orange=(0.94,0.29,0.045); steel=(0.45,0.48,0.52); rubber=(0.075,0.08,0.09)
parts=[];links=[];customlinks=[]
manual='references/manual.pdf pp.24-26 (PIRATES3; linked from 9021-V3 kit listing)'

def poly(points,h):
 wire=Part.makePolygon([V(x,y,0) for x,y in points]+[V(*points[0],0)])
 return Part.Face(wire).extrude(V(0,0,h))
def box(l,w,h,x=0,y=0,z=0):return Part.makeBox(l,w,h,V(x,y,z))
def cyl(r,h,x=0,y=0,z=0):return Part.makeCylinder(r,h,V(x,y,z))
def tube(ro,ri,h):return cyl(ro,h).cut(cyl(ri,h))
def shift(shape,x=0,y=0,z=0):
 s=shape.copy();s.translate(V(x,y,z));return s

def drill(shape,holes,h):
 for x,y,r in holes: shape=shape.cut(cyl(r,h+2,x,y,-1))
 return shape.removeSplitter()

def fuse(shapes):
 return shapes[0].multiFuse(shapes[1:]).removeSplitter() if len(shapes)>1 else shapes[0]

def rod(a,b,r):
 a,b=V(*a),V(*b);d=b-a;return Part.makeCylinder(r,d.Length,a,d)

def component(name,partno,label,shape,color,evidence='ESTIMATED: dimensions / holes / outline from reference images; not a replacement drawing',source=manual):
 assert not shape.isNull() and shape.isValid() and len(shape.Solids)>0 and shape.Volume>0,name
 o=doc.addObject('Part::Feature',name);o.Label=partno+' | '+label;lib.addObject(o);o.Shape=shape
 for prop,val in [('PartNumber',partno),('Evidence',evidence),('Source',source)]:
  o.addProperty('App::PropertyString',prop,'Provenance');setattr(o,prop,val)
 o.addProperty('App::PropertyColor','DisplayColor','Provenance');o.DisplayColor=color
 parts.append(o);return o

def inst(source,name,pos=(0,0,0),rot=None,group='Chassis',custompart=False):
 o=doc.addObject('App::Link',name);o.setLink(source);o.Label=name+' | '+source.PartNumber
 o.LinkPlacement=A.Placement(V(*pos),rot or A.Rotation()).multiply(source.Placement)
 (custom if custompart else groups[group]).addObject(o)
 (customlinks if custompart else links).append(o)
 return o

# 8264: tapered necks and wide central plate visible in underside photo and manual.
L=D['ChassisLength'];W=D['ChassisWidth'];t=D['ChassisThickness'];gc=D['GroundClearance']
outline=[(-223,-25),(-190,-25),(-175,-35),(-157,-35),(-139,-66),(139,-66),(157,-35),(190,-25),(223,-25),(223,25),(190,25),(157,35),(139,66),(-139,66),(-157,35),(-175,35),(-190,25),(-223,25)]
outline=[(x*L/446,y*W/132) for x,y in outline]
# Hole coordinates are explicitly provisional. No implication of measured pattern.
holes=[(x,y,1.7) for x in (-215,-199,199,215) for y in (-18,18)]
holes += [(x,y,1.7) for x in (-170,-156,156,170) for y in (-18,18)]
holes += [(x,y,1.7) for x in (-110,-58,35,108) for y in (-42,42)]
holes += [(x,y,1.7) for x in (-30,24) for y in (-15,15)]
base=component('P8264','8264','Tapered aluminium chassis',drill(poly(outline,t),holes,t),silver,
 'PUBLISHED overall 446 x 132 x 3 mm; ESTIMATED outline and all hole coordinates; end kick-up omitted',
 'SOURCES.md S1/S2; references/vehicle_15.jpg; manual p26')
inst(base,'Chassis8264',(0,0,gc))

# Lower arms: webbed trapezoid with triangular pockets and pivot bores along X.
span=D['OuterPivotY']-D['LowerPivotY']
def lower_arm(rear=False):
 root=30 if rear else 28; tip=19 if rear else 20
 s=poly([(-root,0),(root,0),(tip,span),(-tip,span)],7)
 pockets=[ [(-root+7,12),(-4,12),(-4,45)],[(4,12),(root-7,12),(4,45)],
 [(-root+9,25),(-7,53),(-20,74)],[(root-9,25),(20,74),(7,53)],
 [(-18,80),(-4,65),(-4,span-12)],[(4,65),(18,80),(4,span-12)] ]
 for p in pockets:s=s.cut(shift(poly(p,9),z=-1))
 for y,width in [(0,root*2),(span,tip*2)]:
  outer=Part.makeCylinder(5,width,V(-width/2,y,3.5),V(1,0,0));s=s.fuse(outer)
  s=s.cut(Part.makeCylinder(2,width+2,V(-width/2-1,y,3.5),V(1,0,0)))
 return s.removeSplitter()
frontarm=component('P8170','8170','Front lower webbed arm',lower_arm(),black)
reararm=component('P8169','8169','Rear lower webbed arm',lower_arm(True),black)
def upper_arm():
 s=poly([(-18,0),(18,0),(6,span),(-6,span)],6)
 s=s.cut(shift(poly([(-11,10),(11,10),(0,span-18)],8),z=-1))
 return s.fuse(Part.makeCylinder(4,36,V(-18,0,3),V(1,0,0))).removeSplitter()
fu=component('P8160','8160','Front upper A arm',upper_arm(),black)
ru=component('P8162','8162','Rear upper A arm',upper_arm(),black)
# Different front/rear shock towers, flattened local XY then placed into YZ plane.
def tower(rear=False):
 eye=D['RearShockEyes' if rear else 'FrontShockEyes']
 rise=math.sqrt(eye**2-(D['ShockLowerY']-D['ShockUpperY'])**2)
 top=D['ShockLowerZ']+rise-gc-3
 p=[(-30,0),(-35,16),(-32,top-31),(-65,top-1),(-65,top+7),(-55,top+8),(-40,top),(40,top),(55,top+8),(65,top+7),(65,top-1),(32,top-31),(35,16),(30,0),(20,0),(18,18),(-18,18),(-20,0)]
 thick=D['RearTowerThickness' if rear else 'FrontTowerThickness']
 s=poly(p,thick)
 s=s.cut(shift(poly([(-18,top-13),(18,top-13),(13,top-40),(-13,top-40)],thick+2),z=-1))
 hs=[(sg*y,top+(y-57)*0.35,1.6) for sg in (-1,1) for y in (43,50,57,61)]
 hs +=[(sg*26,z,2.1) for sg in (-1,1) for z in (8,23)]
 return drill(s,hs,thick),top
ft,fheight=tower();rt,rheight=tower(True)
fronttower=component('P8261','8261','Front shock tower',ft,black)
reartower=component('P8262','8262','Rear shock tower',rt,black)
# Gearbox outer envelope only: differential internals intentionally absent.
gears=fuse([box(40,54,23,-20,-27,0),Part.makeCylinder(24,44,V(0,-22,22),V(0,1,0)),box(12,46,22,-6,-23,28)])
gears=gears.cut(Part.makeCylinder(6,60,V(0,-30,22),V(0,1,0)))
gears=gears.cut(Part.makeCylinder(22.5,40,V(0,-20,22),V(0,1,0)))
gearcase=component('P8025','8025','Differential gearbox envelope',gears,black)
mount=component('P8046','8046','Front lower pivot mount',drill(box(12,84,10,-6,-42),[(0,-28,1.7),(0,28,1.7)],10),orange)
rmount=component('P8045','8045','Rear lower pivot mount',mount.Shape.copy(),orange)
# Hub carriers and front C mount, using bearing size 16 x 8 x 5 from manual.
hubshape=fuse([tube(13,8,14),box(10,38,8,-5,-19,3)])
hubshape=hubshape.cut(cyl(8,16,z=-1))
rearhub=component('P8051','8051','Rear hub carrier',hubshape,orange)
fronthub=component('P8052','8052','Front steering cup',hubshape.copy(),orange)
cshape=box(28,13,48,-14,-6.5,-24).cut(box(22,15,34,-11,-7.5,-17))
cmount=component('P8037','8037','Front C mount',cshape,orange)
hexradius=D['WheelHexAF']/math.sqrt(3)
hexshape=poly([(hexradius*math.cos(i*math.pi/3),hexradius*math.sin(i*math.pi/3)) for i in range(6)],7).cut(cyl(4,7))
hexpart=component('P8068','8068','17 mm wheel hex',hexshape,orange,'PUBLISHED 17 mm across flats; assumed thickness 7 mm; axle hole 8 mm from bearing interface')
bearing=component('P8073','8073','16 x 8 x 5 bearing',tube(8,4,5),steel,'MANUAL p25: 16 x 8 x 5 mm')
# Shock bodies, shafts, eyelets and actual helical springs, separate service parts.
def shock_set(rear=False):
 code='8318' if rear else '8317';eye=D['RearShockEyes' if rear else 'FrontShockEyes'];cap=eye-13
 body=component('P'+code+'Body',code,'Shock body / cap',fuse([cyl(9,eye*.53,z=eye*.38),cyl(12.5,9,z=cap-2),cyl(11,5,z=eye-8)]),orange,
 'PUBLISHED eye spacing '+str(eye)+' mm, max diameter 25 mm; internal proportions estimated; source S4')
 shaft=component('P'+code+'Shaft',code+'-shaft','Shock shaft',cyl(2,eye*.60,z=5),steel)
 # eyes point through local X, so they align with tower thickness after placement
 eye_shape=Part.makeCylinder(5,8,V(-4,0,0),V(1,0,0)).cut(Part.makeCylinder(D['ShockHole']/2,10,V(-5,0,0),V(1,0,0)))
 eyes=component('P'+code+'Eyes',code+'-eyes','Shock eyelets',Part.makeCompound([eye_shape,shift(eye_shape,z=eye)]),black,
 'PUBLISHED eye centre spacing '+str(eye)+' mm / hole diameter 3 mm; end shape simplified')
 h=eye-30;helix=Part.makeHelix(h/9,h,10.6)
 profile=Part.Wire([Part.makeCircle(1.1,V(10.6,0,0),V(0,1,0))])
 spring=Part.Wire(helix.Edges).makePipeShell([profile],True,True);spring.translate(V(0,0,12))
 sp=component('P'+code+'Spring','8320' if rear else '8319','Shock coil spring',spring,(0.45,0.09,0.07),'ESTIMATED wire diameter / pitch; visual representation, no spring-rate specification')
 seat=component('P'+code+'Seat',code+'-seats','Spring seats',Part.makeCompound([tube(12.5,2,3),shift(tube(12.5,9,3),z=eye-21)]),black)
 return [body,shaft,eyes,sp,seat]
fshock=shock_set();rshock=shock_set(True)
# Wheels are smooth envelope tires; circumferential grooves represent tread, not molded tread reproduction.
r=D['TireDiameter']/2;tw=D['TireWidth'];rimr=D['RimDiameter']/2
profile=[(rimr,-tw/2),(r-9,-tw/2),(r-3,-tw/2+6),(r,-tw/2+12),(r,tw/2-12),(r-3,tw/2-6),(r-9,tw/2),(rimr,tw/2)]
wire=Part.makePolygon([V(rad,0,z) for rad,z in profile]+[V(profile[0][0],0,profile[0][1])])
tire=Part.Face(wire).revolve(V(0,0,0),V(0,0,1),360)
for z in (-16,-8,0,8,16):tire=tire.cut(shift(tube(r+1,r-1.7,1.6),z=z-.8))
tirepart=component('P8175','8175','145 x 69 tire envelope',tire,rubber,'PUBLISHED OD145 / width69 mm; ID87 from hub spec; tread simplified')
rim=tube(rimr,rimr-4,tw-8);rim.translate(V(0,0,-(tw-8)/2))
rim=rim.fuse(shift(tube(rimr-4,4,5),z=-2.5)).removeSplitter()
for i in range(8):
 a=i*math.pi/4;rim=rim.cut(cyl(9,7,25*math.cos(a),25*math.sin(a),-3.5))
rimpart=component('P8174','8174','Wheel rim',rim,black,'PUBLISHED 87 mm nominal hub/rim interface; rim offset and spoke pattern estimated')
# Layout: track derived from overall width minus tire width, not conflicting 270 mm listing field.
wb=D['Wheelbase'];wy=(D['OverallWidth']-tw)/2;wz=r
wheelrot=A.Rotation(V(0,0,1),V(0,1,0));towerrot=A.Rotation(V(1,1,1),120)
for front in (True,False):
 x=wb/2 if front else -wb/2;tag='F' if front else 'R';group='FrontSuspension' if front else 'RearSuspension'
 inst(gearcase,tag+'_GearCase',(x,0,gc+3),group=group)
 towerx=x+(-13 if front else 13)
 inst(fronttower if front else reartower,tag+'_ShockTower',(towerx,0,gc+3),towerrot,group)
 for dx in (-31,31):inst(mount if front else rmount,tag+'_PivotMount_'+str(int(dx)),(x+dx,0,gc+3),group=group)
 for side in (-1,1):
  lab=tag+('L' if side>0 else 'R');armrot=A.Rotation(V(0,0,1),0 if side>0 else 180)
  inst(frontarm if front else reararm,lab+'_LowerArm',(x,side*D['LowerPivotY'],D['LowerPivotZ']),armrot,group)
  inst(fu if front else ru,lab+'_UpperArm',(x,side*D['LowerPivotY'],D['UpperPivotZ']),armrot,group)
  inst(fronthub if front else rearhub,lab+'_Hub',(x,side*D['OuterPivotY'],wz),wheelrot,group)
  if front:inst(cmount,lab+'_CMount',(x,side*D['OuterPivotY'],wz),group=group)
  inst(hexpart,lab+'_Hex',(x,side*(wy-10),wz),wheelrot,'Wheels')
  inst(bearing,lab+'_Bearing',(x,side*D['OuterPivotY'],wz),wheelrot,group)
  inst(tirepart,lab+'_Tire',(x,side*wy,wz),wheelrot,'Wheels')
  inst(rimpart,lab+'_Rim',(x,side*wy,wz),wheelrot,'Wheels')
  # Shock mounted at published eye spacing, tower height follows geometry.
  eye=D['FrontShockEyes' if front else 'RearShockEyes'];dy=D['ShockUpperY']-D['ShockLowerY'];dz=math.sqrt(eye*eye-dy*dy)
  bottom=(towerx+6,side*D['ShockLowerY'],D['ShockLowerZ']);rotation=A.Rotation(V(0,0,1),V(0,side*dy,dz))
  for j,part in enumerate(fshock if front else rshock):inst(part,lab+'_Shock_'+str(j),bottom,rotation,group)
  a=(x,side*26,gc+25);b=(x,side*(wy-8),wz)
  shaft=component('Drive_'+lab,'8158' if front else '8159',lab+' wheel drive shaft',rod(a,b,D['ShaftDiameter']/2),steel,'PUBLISHED diameter5; length/placement estimated')
  inst(shaft,lab+'_Drive',group='Drivetrain')
# Center differential and longitudinal shafts, simplified outer shapes.
center=component('P8156','8156','Center differential envelope',fuse([Part.makeCylinder(17,37,V(-18.5,0,0),V(1,0,0)),Part.makeCylinder(24,4,V(14.5,0,0),V(1,0,0))]),steel,'ESTIMATED envelope; 46T spur represented as blank disk; gear teeth/internals omitted')
inst(center,'CenterDifferential',(0,0,gc+30),group='Drivetrain')
supportshape=box(4,44,42,-2,-22).cut(Part.makeCylinder(8,6,V(-3,0,27),V(1,0,0)))
support=component('P8428','8428','Center differential support plate',supportshape,black,
 'MANUAL p26 part identification; support profile, height and hole placement estimated')
for xx in (-22,22):inst(support,'CenterDiffSupport'+str(xx).replace('-','N'),(xx,0,gc+3),group='Drivetrain')
fdiffshape=fuse([cyl(15.5,32,z=-16),cyl(22,3,z=15),cyl(5,56,z=-28)])
fdiff=component('P8008','8008','Front/rear differential assembly',fdiffshape,steel,
 'MANUAL p24 identifies 8008; outer geometry estimated; bevel and planetary teeth omitted')
for x,tag in [(wb/2,'Front'),(-wb/2,'Rear')]:
 inst(fdiff,tag+'Differential',(x,0,gc+25),wheelrot,'Drivetrain')
for side in (-1,1):
 s=component('CenterShaft'+str(side).replace('-','N'),'8157','Longitudinal shaft',rod((side*22,0,gc+30),(side*(wb/2-20),0,gc+25),2.5),steel,'PUBLISHED diameter5; shaft length estimated')
 inst(s,'CenterDrive'+str(side).replace('-','N'),group='Drivetrain')
 # shaped chassis brace above centerline
 p=[(side*45,0,gc+42),(side*140,0,gc+62),(side*170,0,gc+50)]
 s=component('Brace'+str(side).replace('-','N'),'8267' if side>0 else '8266','Chassis support brace',fuse([rod(p[0],p[1],4.5),rod(p[1],p[2],4.5)]),black)
 inst(s,'SupportBrace'+str(side).replace('-','N'))
# stock tray, no invented electronics in bare-kit model.
tray=box(155,54,3,-77.5,-27).fuse(box(155,3,18,-77.5,-27)).fuse(box(3,54,18,-77.5,-27)).fuse(box(3,54,18,74.5,-27)).removeSplitter()
traypart=component('P8426','8426','Open battery tray',tray,black,'ESTIMATED 155 x 54 envelope from photo; exact battery fit unknown')
inst(traypart,'BatteryTray8426',(-15,45,gc+3),group='BatteryTray')
# 35 kgf.cm waterproof steel-gear servo: manufacturer DS-R003B package size.
servobody=box(D['ServoLength'],D['ServoWidth'],D['ServoHeight'],-20,-10)
servobody=servobody.fuse(box(54,20,3,-27,-10,29)).fuse(cyl(6,4,10,0,42))
for xx in (-24,24):
 for yy in (-5,5):servobody=servobody.cut(cyl(2,5,xx,yy,28))
servo=component('Servo35kg','DS-R003B','35 kgf.cm waterproof metal-gear steering servo',servobody,(0.10,0.26,0.52),
 'MANUFACTURER 40 x 20 x 42 mm body; 35 kgf.cm stall torque, waterproof, steel gear; mounting ears/holes estimated',
 'https://www.dspowerservo.com/ds-r003b-35kg-waterproof-servo-metal-gear-digital-servo-product/')
inst(servo,'SteeringServo35kg',(80,-43,gc+5),group='Steering')
bracketshape=box(60,26,3,-30,-13).fuse(box(3,26,29,-30,-13)).fuse(box(3,26,29,27,-13)).removeSplitter()
bracket=component('ServoBracket','CUSTOM-S01','Servo mounting cradle',bracketshape,silver,'CUSTOM mounting proposal; body clearance provided; OEM chassis attachment not resolved')
inst(bracket,'ServoCradle',(80,-43,gc+3),group='Steering')
horn=component('ServoHorn','CUSTOM-S02','Servo horn',drill(poly([(-5,-5),(23,-5),(28,0),(23,5),(-5,5)],3),[(0,0,1.5),(22,0,1.5)],3),orange,'ESTIMATED arm shape; spline and linkage geometry unverified')
inst(horn,'ServoHorn',(90,-43,gc+51),group='Steering')
bell=component('P8028','8028','Steering bellcrank envelope',fuse([cyl(7,34),box(30,8,4,-4,-4,30)]),black)
for yy in (-18,18):inst(bell,'Bellcrank'+str(yy).replace('-','N'),(140,yy,gc+3),group='Steering')
steerlink=component('SteerLink','8161','Steering tie rods',Part.makeCompound([rod((140,side*18,gc+37),(wb/2+12,side*D['OuterPivotY'],wz+7),2) for side in (-1,1)]),steel)
inst(steerlink,'SteeringTieRods',group='Steering')
drag=component('ServoDragLink','8020','Servo drag link',rod((112,-43,gc+52),(151,-18,gc+37),2),steel)
inst(drag,'ServoDragLink',group='Steering')
# Custom protective extensions define requested overall length, not an OEM chassis claim.
for sign,tag in [(1,'Front'),(-1,'Rear')]:
 end=D['OverallLength']/2
 rails=[box(end-L/2,10,5,L/2,yy-5,gc) for yy in (-22,22)]
 rails.append(box(8,120,20,end-8,-60,gc))
 bshape=fuse(rails)
 if sign<0:bshape.rotate(V(),V(0,0,1),180)
 bumper=component('Bumper'+tag,'CUSTOM-B'+str(sign).replace('-','N'),tag+' protective extension',bshape,black,
 'CUSTOM extensions to overall length550; not ZD original bumper; attachment design provisional')
 inst(bumper,tag+'ProtectiveExtension')
# Proposed robot platform is a separately hidden assembly, all mounts provisional.
deckpoints=[(-200,-140),(-190,-150),(190,-150),(200,-140),(200,140),(190,150),(-190,150),(-200,140)]
deckpoints=[(x*D['DeckLength']/400,y*D['DeckWidth']/300) for x,y in deckpoints]
dholes=[(x,y,2.25) for x in (-125,125) for y in (-55,55)]
dholes +=[(x,y,2.25) for x in (-175,-125,-75,-25,25,75,125,175) for y in (-125,125)]
deck=component('CustomDeck','CUSTOM-D01','400 x 300 sensor deck',drill(poly(deckpoints,D['DeckThickness']),dholes,D['DeckThickness']),silver,'CUSTOM: reference image deck length/width; thickness, heights and holes provisional','User reference image; no OEM part number')
inst(deck,'OptionalSensorDeck',(0,0,D['DeckHeight']),custompart=True)
postheight=D['DeckHeight']-gc-3
post=component('CustomPost','CUSTOM-D02','Deck standoff',tube(6,2.25,postheight),steel,'CUSTOM: geometry only; attachment to OEM holes not resolved','User reference image')
for i,(x,y,_) in enumerate(dholes[:4]):inst(post,'OptionalStandoff'+str(i),(x,y,gc+3),custompart=True)
# Exploded fixed-placement links, by subassembly; not solver joints.
for link in links:
 ex=doc.addObject('App::Link',link.Name+'_EX');ex.setLink(link.LinkedObject);expl.addObject(ex)
 p=link.LinkPlacement.copy();b=p.Base
 b.x += 95 if b.x>100 else -95 if b.x<-100 else 0
 b.y += 100 if b.y>80 else -100 if b.y<-80 else 0
 b.z += 90 if 'Tower' in link.Name else 35 if 'Arm' in link.Name else 0
 p.Base=b;ex.LinkPlacement=p

doc.recompute()
# Save local-origin individual parts as STEP and standalone FCStd.
exportdoc=A.newDocument('PartExports')
for part in parts:
 obj=exportdoc.addObject('Part::Feature',part.Name);obj.Shape=part.Shape.copy();obj.Label=part.Label
 Part.export([obj],OUT+'/parts/'+part.Name+'.step')
 exportdoc.saveAs(OUT+'/parts/'+part.Name+'.FCStd');exportdoc.removeObject(obj.Name)
A.closeDocument(exportdoc.Name)
# STEP export requires resolved feature shapes (Part.export can drop App::Links).
e=A.newDocument('AssemblyExport');resolved=[]
for link in links:
 o=e.addObject('Part::Feature',link.Name);o.Shape=link.Shape.copy();o.Label=link.Label;resolved.append(o)
e.recompute();Part.export(resolved,OUT+'/ZD9021V3_rolling_chassis.step')
check=Part.Shape();check.read(OUT+'/ZD9021V3_rolling_chassis.step')
expected=sum(len(o.Shape.Solids) for o in resolved)
assert len(check.Solids)==expected and check.isValid(),'STEP roundtrip failed'
for link in customlinks:
 o=e.addObject('Part::Feature',link.Name);o.Shape=link.Shape.copy();o.Label=link.Label;resolved.append(o)
e.recompute();Part.export(resolved,OUT+'/ZD9021V3_platform.step')
platform_check=Part.Shape();platform_check.read(OUT+'/ZD9021V3_platform.step')
assert platform_check.isValid() and len(platform_check.Solids)==sum(len(o.Shape.Solids) for o in resolved)
A.closeDocument(e.Name);A.setActiveDocument(doc.Name)
# Ensure envelope constraints survive export and wheel placements.
assert abs(base.Shape.BoundBox.XLength-D['ChassisLength'])<1e-6
assert abs(base.Shape.BoundBox.YLength-D['ChassisWidth'])<1e-6
assert abs(tirepart.Shape.BoundBox.XLength-D['TireDiameter'])<1e-6
envelope=Part.makeCompound([l.Shape for l in links]).BoundBox
assert abs(envelope.XLength-D['OverallLength'])<1e-5
assert abs(envelope.YLength-D['OverallWidth'])<1e-5
post_checks=[]
for postlink in customlinks[1:]:
 for vehiclelink in links:
  if postlink.Shape.BoundBox.intersect(vehiclelink.Shape.BoundBox):
   overlap=postlink.Shape.common(vehiclelink.Shape).Volume
   assert overlap<0.01,'Deck post interference: '+postlink.Name+' / '+vehiclelink.Name
 post_checks.append(postlink.Name)
report={'status':'PASS shape and STEP roundtrip checks','unique_components':len(parts),'rolling_instances':len(links),'custom_instances':len(customlinks),'step_solids':expected,
 'deck_post_clearance_check':{'passed':post_checks,'scope':'static solid overlap against rolling chassis only; does not validate mounting or motion'},
 'assembly_envelope_mm':[envelope.XLength,envelope.YLength,envelope.ZLength],
 'published_dimensions_applied':{k:D[k] for k in ['ChassisLength','ChassisWidth','ChassisThickness','Wheelbase','TireDiameter','TireWidth','WheelHexAF','FrontShockEyes','RearShockEyes']},
 'limitations':['No OEM dimensional CAD available. Estimated shapes and all mounting coordinates remain unverified.','Fixed placement; no assembly joints or suspension kinematics.','No full interference certification: envelopes, springs and simplified interfaces may overlap.','Wheel envelope length515; custom protective extensions bring overall length to550.'],
 'parts':[{'name':p.Name,'part_number':p.PartNumber,'valid':p.Shape.isValid(),'solids':len(p.Shape.Solids),'evidence':p.Evidence} for p in parts]}
json.dump(report,open(OUT+'/validation.json','w'),indent=2)
with open(OUT+'/BOM.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Object','Part number','Description','Rolling quantity','Custom quantity','Evidence'])
 for p in parts:w.writerow([p.Name,p.PartNumber,p.Label,sum(l.LinkedObject==p for l in links),sum(l.LinkedObject==p for l in customlinks),p.Evidence])
doc.saveAs(OUT+'/ZD9021V3_assembly.FCStd')
print('COMPLETE:',len(parts),'components;',len(links),'rolling instances;',expected,'STEP solids')
