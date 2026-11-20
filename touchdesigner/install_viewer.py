"""Run in TD with ROTATIONAL_TD_DIR set to this source directory.

Only /project1/RotationalSeeds is created/updated. The current .toe project is
never saved and project.folder is never changed. The exported .tox is self-contained.
"""
from pathlib import Path
import json

HERE=Path(ROTATIONAL_TD_DIR)
SELECTED=[
 ('open_link','borromean-m3-q1_2-a1_3-overlap-c1_8-ax6','Open Borromean · H < 17/8'),
 ('thin_link','borromean-m6-q1_2-a1_3-overlap-c1_8-ax6','Fine Borromean · topological dimension 1'),
 ('dense_link','borromean-m1-q1_2-a1_3-overlap-c1_8-ax6','Dense Borromean · H < 3'),
]

def install():
    preserved=(project.folder,project.name)
    root=op('/project1');b=root.op('RotationalSeeds') or root.create(baseCOMP,'RotationalSeeds')
    b.nodeX=600;b.nodeY=-500
    b.comment='Rotational seeds research. Deterministic finite point previews; historical novelty unresolved.'
    def node(kind,name,parent=b):return parent.op(name) or parent.create(kind,name)
    recipes={}
    for key,ident,label in SELECTED:
        d=json.loads((HERE.parent/'survey'/(ident+'.json')).read_text(encoding='utf-8'))
        d['viewer_label']=label;recipes[key]=d
    node(textDAT,'recipes').text=json.dumps(recipes)
    node(textDAT,'actions').text=(HERE/'viewer_actions.py').read_text(encoding='utf-8')
    page=b.appendCustomPage('Explore') if not b.pars('Candidate') else b.par.Candidate.page
    if not b.pars('Candidate'):
        p=page.appendMenu('Candidate',label='Candidate')[0]
        p.menuNames=list(recipes);p.menuLabels=[x['viewer_label'] for x in recipes.values()]
        p.default=p.val='open_link'
        for name,label,default,mn,mx in [('Yaw','Turn',0.,-180.,180.),('Pitch','Tilt',0.,-90.,90.),('Zoom','Magnification',1.,.5,4.),('Pointsize','Point size',1.4,.6,3.)]:
            p=page.appendFloat(name,label=label)[0];p.min=mn;p.max=mx;p.default=p.val=default
        p=page.appendToggle('Orbit',label='Slow orbit')[0];p.default=p.val=False
        p=page.appendInt('Pointcount',label='Finite samples')[0]
        p.min=50000;p.max=300000;p.clampMin=p.clampMax=True;p.default=p.val=200000
        page.appendPulse('Rebuild',label='Regenerate samples')
        page.appendPulse('Resetview',label='Reset view')
        page.appendPulse('Openstudio',label='Open viewer')
        page.appendPulse('Snapshot',label='Save preview PNG')
        p=page.appendStr('Outputfolder',label='Preview folder')[0];p.default=p.val=HERE.as_posix()
        page.appendStr('Status')[0].readOnly=True
    geo=node(geometryCOMP,'geometry')
    if geo.op('torus1'):geo.op('torus1').destroy()
    sop=node(scriptSOP,'points',geo)
    callback=node(textDAT,'points_callbacks',geo)
    callback.text='''def onCook(scriptOp):
    data=parent(2).fetch('point_data',None)
    if data is None:return
    scriptOp.clear()
    scriptOp.pointAttribs.create('Cd')
    positions,colours=data
    for xyz,rgb in zip(positions,colours):
        p=scriptOp.appendPoint()
        p.P=(float(xyz[0]),float(xyz[1]),float(xyz[2]))
        p.Cd=(float(rgb[0]),float(rgb[1]),float(rgb[2]),1.)
'''
    sop.par.callbacks=callback;sop.display=sop.render=False
    sprites=node(convertSOP,'sprites',geo);sprites.inputConnectors[0].connect(sop)
    sprites.par.totype='particlesperpoint';sprites.par.prtype='pointsprites'
    sprites.display=sprites.render=True
    mat=node(pointspriteMAT,'point_material');mat.par.pointsize.expr='parent().par.Pointsize';mat.par.attenpscale=0.
    geo.par.material=mat
    geo.par.rx.expr='parent().par.Pitch'
    geo.par.ry.expr='parent().par.Yaw + (absTime.seconds*4 if parent().par.Orbit else 0)'
    camera=node(cameraCOMP,'camera');camera.par.tz=5;camera.par.projection='orthographic'
    camera.par.orthowidth.expr='3.35 / parent().par.Zoom';camera.par.near=.01;camera.par.far=100
    render=node(renderTOP,'render');render.par.camera=camera;render.par.geometry=geo
    render.par.resolutionw=1280;render.par.resolutionh=1024;render.par.resmult=False
    out=node(outTOP,'out1');out.inputConnectors[0].connect(render);b.par.opviewer=out
    studio=node(containerCOMP,'studio');studio.par.w=1220;studio.par.h=720
    preview=node(containerCOMP,'preview',studio);preview.par.w=900;preview.par.h=720
    preview.par.top=render;preview.par.topfill='best';preview.par.bgalpha=1
    settings=node(parameterCOMP,'settings',studio);settings.par.x=900;settings.par.w=320;settings.par.h=720
    settings.par.op=b;settings.par.builtin=False;settings.par.custom=True;settings.par.header=False;settings.par.pagenames=False
    win=node(windowCOMP,'studio_window');win.par.winop=studio;win.par.title='Rotational Seeds · finite IFS previews'
    win.par.justifyh='center';win.par.justifyv='center';win.par.borders=True
    events=node(parameterexecuteDAT,'events');events.par.op=b
    events.par.pars='Candidate Rebuild Resetview Openstudio Snapshot';events.par.valuechange=True;events.par.onpulse=True
    events.text='''def onValueChange(par,prev):
    if par.name=='Candidate':parent().op('actions').module.rebuild()

def onPulse(par):
    a=parent().op('actions').module
    {'Rebuild':a.rebuild,'Resetview':a.reset_view,'Openstudio':a.open_studio,'Snapshot':a.snapshot}.get(par.name,lambda:None)()
'''
    for i,n in enumerate(b.children):n.nodeX=(i%4)*190;n.nodeY=-(i//4)*130
    receipt=b.op('actions').module.rebuild()
    b.save((HERE/'RotationalSeeds.tox').as_posix())
    assert preserved==(project.folder,project.name)
    receipt.update({'component':b.path,'tox':str(HERE/'RotationalSeeds.tox'),
                    'project_folder':project.folder,'project_name':project.name,'project_saved':False})
    print(json.dumps(receipt));return receipt

if __name__=='__main__':install()
