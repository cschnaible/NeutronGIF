import ROOT as R
import Gif.TestBeamAnalysis.Plotter as Plotter
import numpy as np
import array as array

# makes a plot of the captured neutron energy spectrum
# note that the x axis is log scale, and the bins are equally spaced on a log scale

f = open('../files/pos_final')
xnotdeut = array.array('f',[])
ynotdeut = array.array('f',[])
znotdeut = array.array('f',[])
rnotdeut = array.array('f',[])
xdeut = array.array('f',[])
ydeut = array.array('f',[])
zdeut = array.array('f',[])
rdeut = array.array('f',[])
x = array.array('f',[])
y = array.array('f',[])
z = array.array('f',[])
r = array.array('f',[])
hxyz = R.TH3F('hxyz','',100,-1000,1000,100,-1300,1300,100,-1000,1000)
hTotxyz = R.TH3F('hTotxyz','',100,-1000,1000,100,-1300,1300,100,-1000,1000)
hNotTotxyz = R.TH3F('hTotxyz','',100,-1000,1000,100,-1300,1300,100,-1000,1000)
hDeutxyz = R.TH3F('hDeutxyz','',100,-1000,1000,100,-1300,1300,100,-1000,1000)
hNotDeutxyz = R.TH3F('hNotDeutxyz','',100,-1000,1000,100,-1300,1300,100,-1000,1000)
for line in f:
    l = line.strip('\n').split()
    if np.fabs(float(l[2])) > 1200: continue
    if np.fabs(float(l[0])) > 800: continue
    if np.fabs(float(l[1])) > 800: continue
    x.append(float(l[0]))
    y.append(float(l[1]))
    z.append(float(l[2]))
    r.append( ( (float(l[0]))**2 + (float(l[1]))**2 )**(0.5) )
    hxyz.Fill(float(l[0]),float(l[2]),float(l[1]))
    if l[3]=='deuteron':
        xdeut.append(float(l[0]))
        ydeut.append(float(l[1]))
        zdeut.append(float(l[2]))
        rdeut.append( ( (float(l[0]))**2 + (float(l[1]))**2 )**(0.5) )
        hDeutxyz.Fill(float(l[0]),float(l[2]),float(l[1]))
    else:
        xnotdeut.append(float(l[0]))
        ynotdeut.append(float(l[1]))
        znotdeut.append(float(l[2]))
        rnotdeut.append( ( (float(l[0]))**2 + (float(l[1]))**2 )**(0.5) )
        hNotDeutxyz.Fill(float(l[0]),float(l[2]),float(l[1]))
nNeutrons = len(x)
nDeut = len(xdeut)
nNotDeut = len(xnotdeut)

# Total caputred plots

hxy = R.TGraph(nNeutrons,x,y)
hxyplot = Plotter.Plot(hxy, 'Position', 'f', 'ap')
canvasxy = Plotter.Canvas('Neutron Capture Position', False, 0., 'Internal', 950, 600)
canvasxy.makeLegend()
canvasxy.addMainPlot(hxyplot,True,False)
# cosmetics
hxy.GetYaxis().SetTitle('y position [cm]')
hxy.GetXaxis().SetTitle('x position [cm]')
hxy.GetYaxis().SetTitleOffset(hxy.GetYaxis().GetTitleOffset()*1.2)
hxy.GetXaxis().SetTitleOffset(hxy.GetXaxis().GetTitleOffset()*1.2)
hxy.SetMaximum(800)
hxy.SetMinimum(-800)
hxy.GetXaxis().SetLimits(-800,800)
hxyplot.scaleTitles(0.8)
hxyplot.scaleLabels(0.8)
canvasxy.finishCanvas()
canvasxy.c.SaveAs('../pdfs/hxy.pdf')

hxz = R.TGraph(nNeutrons,z,x)
hxzplot = Plotter.Plot(hxz, 'Position', 'f', 'ap')
canvasxz = Plotter.Canvas('Neutron Capture Position', False, 0., 'Internal', 950, 600)
canvasxz.makeLegend()
canvasxz.addMainPlot(hxzplot,True,False)
# cosmetics
hxz.GetYaxis().SetTitle('x position [cm]')
hxz.GetXaxis().SetTitle('z position [cm]')
hxz.GetYaxis().SetTitleOffset(hxz.GetYaxis().GetTitleOffset()*1.2)
hxz.GetXaxis().SetTitleOffset(hxz.GetXaxis().GetTitleOffset()*1.2)
hxz.SetMaximum(800)
hxz.SetMinimum(-800)
hxz.GetXaxis().SetLimits(-1200,1200)
hxzplot.scaleTitles(0.8)
hxzplot.scaleLabels(0.8)
canvasxz.finishCanvas()
canvasxz.c.SaveAs('../pdfs/hxz.pdf')

hyz = R.TGraph(nNeutrons,z,y)
hyzplot = Plotter.Plot(hyz, 'Position', 'f', 'ap')
canvasyz = Plotter.Canvas('Neutron Capture Position', False, 0., 'Internal', 950, 600)
canvasyz.makeLegend()
canvasyz.addMainPlot(hyzplot,True,False)
# cosmetics
hyz.GetYaxis().SetTitle('y position [cm]')
hyz.GetXaxis().SetTitle('z position [cm]')
hyz.GetYaxis().SetTitleOffset(hyz.GetYaxis().GetTitleOffset()*1.2)
hyz.GetXaxis().SetTitleOffset(hyz.GetXaxis().GetTitleOffset()*1.2)
hyz.SetMaximum(800)
hyz.SetMinimum(-800)
hyz.GetXaxis().SetLimits(-1200,1200)
hyzplot.scaleTitles(0.8)
hyzplot.scaleLabels(0.8)
canvasyz.finishCanvas()
canvasyz.c.SaveAs('../pdfs/hyz.pdf')

hrz = R.TGraph(nNeutrons,z,r)
hrzplot = Plotter.Plot(hrz, 'Position', 'f', 'ap')
canvasrz = Plotter.Canvas('Neutron Capture Position', False, 0., 'Internal', 950, 600)
canvasrz.makeLegend()
canvasrz.addMainPlot(hrzplot,True,False)
# cosmetics
hrz.GetYaxis().SetTitle('r position [cm]')
hrz.GetXaxis().SetTitle('z position [cm]')
hrz.GetYaxis().SetTitleOffset(hrz.GetYaxis().GetTitleOffset()*1.2)
hrz.GetXaxis().SetTitleOffset(hrz.GetXaxis().GetTitleOffset()*1.2)
hrz.SetMinimum(0)
hrz.SetMaximum(800)
hrz.GetXaxis().SetLimits(-1200,1200)
hrzplot.scaleTitles(0.8)
hrzplot.scaleLabels(0.8)
canvasrz.finishCanvas()
canvasrz.c.SaveAs('../pdfs/hrz.pdf')

cxyz = R.TCanvas()
hxyz.Draw('scat')
cxyz.SaveAs('../pdfs/hxyz.pdf')
cxyz.SaveAs('../pdfs/hxyz.root')

# Captured neutrons that make deuteron

hDeutxy = R.TGraph(nDeut,xdeut,ydeut)
hDeutxyplot = Plotter.Plot(hDeutxy, 'Position', 'f', 'ap')
canvasDeutxy = Plotter.Canvas('Neutron Capture Position (deuteron)', False, 0., 'Internal', 950, 600)
canvasDeutxy.makeLegend()
canvasDeutxy.addMainPlot(hDeutxyplot,True,False)
# cosmetics
hDeutxy.GetYaxis().SetTitle('y position [cm]')
hDeutxy.GetXaxis().SetTitle('x position [cm]')
hDeutxy.GetYaxis().SetTitleOffset(hDeutxy.GetYaxis().GetTitleOffset()*1.2)
hDeutxy.GetXaxis().SetTitleOffset(hDeutxy.GetXaxis().GetTitleOffset()*1.2)
hDeutxy.SetMaximum(800)
hDeutxy.SetMinimum(-800)
hDeutxy.GetXaxis().SetLimits(-800,800)
hDeutxyplot.scaleTitles(0.8)
hDeutxyplot.scaleLabels(0.8)
canvasDeutxy.finishCanvas()
canvasDeutxy.c.SaveAs('../pdfs/hDeutxy.pdf')

hDeutxz = R.TGraph(nDeut,zdeut,xdeut)
hDeutxzplot = Plotter.Plot(hDeutxz, 'Position', 'f', 'ap')
canvasDeutxz = Plotter.Canvas('Neutron Capture Position (deuteron)', False, 0., 'Internal', 950, 600)
canvasDeutxz.makeLegend()
canvasDeutxz.addMainPlot(hDeutxzplot,True,False)
# cosmetics
hDeutxz.GetYaxis().SetTitle('x position [cm]')
hDeutxz.GetXaxis().SetTitle('z position [cm]')
hDeutxz.GetYaxis().SetTitleOffset(hDeutxz.GetYaxis().GetTitleOffset()*1.2)
hDeutxz.GetXaxis().SetTitleOffset(hDeutxz.GetXaxis().GetTitleOffset()*1.2)
hDeutxz.SetMaximum(800)
hDeutxz.SetMinimum(-800)
hDeutxz.GetXaxis().SetLimits(-1200,1200)
hDeutxzplot.scaleTitles(0.8)
hDeutxzplot.scaleLabels(0.8)
canvasDeutxz.finishCanvas()
canvasDeutxz.c.SaveAs('../pdfs/hDeutxz.pdf')

hDeutyz = R.TGraph(nDeut,zdeut,ydeut)
hDeutyzplot = Plotter.Plot(hDeutyz, 'Position', 'f', 'ap')
canvasDeutyz = Plotter.Canvas('Neutron Capture Positions (deuteron)', False, 0., 'Internal', 950, 600)
canvasDeutyz.makeLegend()
canvasDeutyz.addMainPlot(hDeutyzplot,True,False)
# cosmetics
hDeutyz.GetYaxis().SetTitle('y position [cm]')
hDeutyz.GetXaxis().SetTitle('z position [cm]')
hDeutyz.GetYaxis().SetTitleOffset(hDeutyz.GetYaxis().GetTitleOffset()*1.2)
hDeutyz.GetXaxis().SetTitleOffset(hDeutyz.GetXaxis().GetTitleOffset()*1.2)
hDeutyz.SetMaximum(800)
hDeutyz.SetMinimum(-800)
hDeutyz.GetXaxis().SetLimits(-1200,1200)
hDeutyzplot.scaleTitles(0.8)
hDeutyzplot.scaleLabels(0.8)
canvasDeutyz.finishCanvas()
canvasDeutyz.c.SaveAs('../pdfs/hDeutyz.pdf')

hDeutrz = R.TGraph(nDeut,zdeut,rdeut)
hDeutrzplot = Plotter.Plot(hDeutrz, 'Position', 'f', 'ap')
canvasDeutrz = Plotter.Canvas('Neutron Capture Position (deuteron)', False, 0., 'Internal', 950, 600)
canvasDeutrz.makeLegend()
canvasDeutrz.addMainPlot(hDeutrzplot,True,False)
# cosmetics
hDeutrz.GetYaxis().SetTitle('r position [cm]')
hDeutrz.GetXaxis().SetTitle('z position [cm]')
hDeutrz.GetYaxis().SetTitleOffset(hDeutrz.GetYaxis().GetTitleOffset()*1.2)
hDeutrz.GetXaxis().SetTitleOffset(hDeutrz.GetXaxis().GetTitleOffset()*1.2)
hDeutrz.SetMinimum(0)
hDeutrz.SetMaximum(800)
hDeutrz.GetXaxis().SetLimits(-1200,1200)
hDeutrzplot.scaleTitles(0.8)
hDeutrzplot.scaleLabels(0.8)
canvasDeutrz.finishCanvas()
canvasDeutrz.c.SaveAs('../pdfs/hDeutrz.pdf')

cDeutxyz = R.TCanvas()
hDeutxyz.Draw('scat')
cDeutxyz.SaveAs('../pdfs/hDeutxyz.pdf')
cDeutxyz.SaveAs('../pdfs/hDeutxyz.root')

# Captured neutrons that do not make notdeuteron

hNotDeutxy = R.TGraph(nNotDeut,xnotdeut,ynotdeut)
hNotDeutxyplot = Plotter.Plot(hNotDeutxy, 'Position', 'f', 'ap')
canvasNotDeutxy = Plotter.Canvas('Neutron Capture Position (not deuteron)', False, 0., 'Internal', 950, 600)
canvasNotDeutxy.makeLegend()
canvasNotDeutxy.addMainPlot(hNotDeutxyplot,True,False)
# cosmetics
hNotDeutxy.GetYaxis().SetTitle('y position [cm]')
hNotDeutxy.GetXaxis().SetTitle('x position [cm]')
hNotDeutxy.GetYaxis().SetTitleOffset(hNotDeutxy.GetYaxis().GetTitleOffset()*1.2)
hNotDeutxy.GetXaxis().SetTitleOffset(hNotDeutxy.GetXaxis().GetTitleOffset()*1.2)
hNotDeutxy.SetMaximum(800)
hNotDeutxy.SetMinimum(-800)
hNotDeutxy.GetXaxis().SetLimits(-800,800)
hNotDeutxyplot.scaleTitles(0.8)
hNotDeutxyplot.scaleLabels(0.8)
canvasNotDeutxy.finishCanvas()
canvasNotDeutxy.c.SaveAs('../pdfs/hNotDeutxy.pdf')

hNotDeutxz = R.TGraph(nNotDeut,znotdeut,xnotdeut)
hNotDeutxzplot = Plotter.Plot(hNotDeutxz, 'Position', 'f', 'ap')
canvasNotDeutxz = Plotter.Canvas('Neutron Capture Position (not deuteron)', False, 0., 'Internal', 950, 600)
canvasNotDeutxz.makeLegend()
canvasNotDeutxz.addMainPlot(hNotDeutxzplot,True,False)
# cosmetics
hNotDeutxz.GetYaxis().SetTitle('x position [cm]')
hNotDeutxz.GetXaxis().SetTitle('z position [cm]')
hNotDeutxz.GetYaxis().SetTitleOffset(hNotDeutxz.GetYaxis().GetTitleOffset()*1.2)
hNotDeutxz.GetXaxis().SetTitleOffset(hNotDeutxz.GetXaxis().GetTitleOffset()*1.2)
hNotDeutxz.SetMaximum(800)
hNotDeutxz.SetMinimum(-800)
hNotDeutxz.GetXaxis().SetLimits(-1200,1200)
hNotDeutxzplot.scaleTitles(0.8)
hNotDeutxzplot.scaleLabels(0.8)
canvasNotDeutxz.finishCanvas()
canvasNotDeutxz.c.SaveAs('../pdfs/hNotDeutxz.pdf')

hNotDeutyz = R.TGraph(nNotDeut,znotdeut,ynotdeut)
hNotDeutyzplot = Plotter.Plot(hNotDeutyz, 'Position', 'f', 'ap')
canvasNotDeutyz = Plotter.Canvas('Neutron Capture Positions (not deuteron)', False, 0., 'Internal', 950, 600)
canvasNotDeutyz.makeLegend()
canvasNotDeutyz.addMainPlot(hNotDeutyzplot,True,False)
# cosmetics
hNotDeutyz.GetYaxis().SetTitle('y position [cm]')
hNotDeutyz.GetXaxis().SetTitle('z position [cm]')
hNotDeutyz.GetYaxis().SetTitleOffset(hNotDeutyz.GetYaxis().GetTitleOffset()*1.2)
hNotDeutyz.GetXaxis().SetTitleOffset(hNotDeutyz.GetXaxis().GetTitleOffset()*1.2)
hNotDeutyz.SetMaximum(800)
hNotDeutyz.SetMinimum(-800)
hNotDeutyz.GetXaxis().SetLimits(-1200,1200)
hNotDeutyzplot.scaleTitles(0.8)
hNotDeutyzplot.scaleLabels(0.8)
canvasNotDeutyz.finishCanvas()
canvasNotDeutyz.c.SaveAs('../pdfs/hNotDeutyz.pdf')

hNotDeutrz = R.TGraph(nNotDeut,znotdeut,rnotdeut)
hNotDeutrzplot = Plotter.Plot(hNotDeutrz, 'Position', 'f', 'ap')
canvasNotDeutrz = Plotter.Canvas('Neutron Capture Position (not deuteron)', False, 0., 'Internal', 950, 600)
canvasNotDeutrz.makeLegend()
canvasNotDeutrz.addMainPlot(hNotDeutrzplot,True,False)
# cosmetics
hNotDeutrz.GetYaxis().SetTitle('r position [cm]')
hNotDeutrz.GetXaxis().SetTitle('z position [cm]')
hNotDeutrz.GetYaxis().SetTitleOffset(hNotDeutrz.GetYaxis().GetTitleOffset()*1.2)
hNotDeutrz.GetXaxis().SetTitleOffset(hNotDeutrz.GetXaxis().GetTitleOffset()*1.2)
hNotDeutrz.SetMinimum(0)
hNotDeutrz.SetMaximum(800)
hNotDeutrz.GetXaxis().SetLimits(-1200,1200)
hNotDeutrzplot.scaleTitles(0.8)
hNotDeutrzplot.scaleLabels(0.8)
canvasNotDeutrz.finishCanvas()
canvasNotDeutrz.c.SaveAs('../pdfs/hNotDeutrz.pdf')

cNotDeutxyz = R.TCanvas()
hNotDeutxyz.Draw('scat')
cNotDeutxyz.SaveAs('../pdfs/hNotDeutxyz.pdf')
cNotDeutxyz.SaveAs('../pdfs/hNotDeutxyz.root')

# Plot Deuteron and not Deuteron together

hxzTot = R.TMultiGraph()
hDeutxz.SetMarkerColor(R.kGreen)
hxzTot.Add(hDeutxz)
hxzTot.Add(hNotDeutxz)
hxzTotPlot = Plotter.Plot(hxzTot,'Position','p','ap')
canvasTotxz = Plotter.Canvas('Neutron Capture Position',False,0.,'Internal',950,600)
canvasTotxz.makeLegend()
canvasTotxz.addMainPlot(hxzTotPlot,True,False)
hxzTot.GetXaxis().SetLimits(-1200,1200)
hxzTot.SetMaximum(800)
hxzTot.SetMinimum(0)
hxzTot.GetXaxis().SetTitle('z position [cm]')
hxzTot.GetYaxis().SetTitle('x position [cm]')
canvasTotxz.finishCanvas()
canvasTotxz.c.SaveAs('../pdfs/hxzTot.pdf')

hyzTot = R.TMultiGraph()
hDeutyz.SetMarkerColor(R.kGreen)
hyzTot.Add(hDeutyz)
hyzTot.Add(hNotDeutyz)
hyzTotPlot = Plotter.Plot(hyzTot,'Position','p','ap')
canvasTotyz = Plotter.Canvas('Neutron Capture Position',False,0.,'Internal',950,600)
canvasTotyz.makeLegend()
canvasTotyz.addMainPlot(hyzTotPlot,True,False)
hyzTot.GetXaxis().SetLimits(-1200,1200)
hyzTot.SetMaximum(800)
hyzTot.SetMinimum(0)
hyzTot.GetXaxis().SetTitle('z position [cm]')
hyzTot.GetYaxis().SetTitle('y position [cm]')
canvasTotyz.finishCanvas()
canvasTotyz.c.SaveAs('../pdfs/hyzTot.pdf')

hrzTot = R.TMultiGraph()
hDeutrz.SetMarkerColor(R.kGreen)
hrzTot.Add(hDeutrz)
hrzTot.Add(hNotDeutrz)
hrzTotPlot = Plotter.Plot(hrzTot,'Position','p','ap')
canvasTotrz = Plotter.Canvas('Neutron Capture Position',False,0.,'Internal',950,600)
canvasTotrz.makeLegend()
canvasTotrz.addMainPlot(hrzTotPlot,True,False)
hrzTot.GetXaxis().SetLimits(-1200,1200)
hrzTot.SetMaximum(800)
hrzTot.SetMinimum(0)
hrzTot.GetXaxis().SetTitle('z position [cm]')
hrzTot.GetYaxis().SetTitle('r position [cm]')
canvasTotrz.finishCanvas()
canvasTotrz.c.SaveAs('../pdfs/hrzTot.pdf')

hxyTot = R.TMultiGraph()
hDeutxy.SetMarkerColor(R.kGreen)
hxyTot.Add(hDeutxy)
hxyTot.Add(hNotDeutxy)
hxyTotPlot = Plotter.Plot(hxyTot,'Position','p','ap')
canvasTotxy = Plotter.Canvas('Neutron Capture Position',False,0.,'Internal',950,600)
canvasTotxy.makeLegend()
canvasTotxy.addMainPlot(hxyTotPlot,True,False)
hxyTot.GetXaxis().SetLimits(-800,800)
hxyTot.SetMaximum(800)
hxyTot.SetMinimum(-800)
hxyTot.GetXaxis().SetTitle('x position [cm]')
hxyTot.GetYaxis().SetTitle('y position [cm]')
canvasTotxy.finishCanvas()
canvasTotxy.c.SaveAs('../pdfs/hxyTot.pdf')

cTotxyz = R.TCanvas()
hTotxyz.Draw('scat')
hNotTotxyz.Draw('scatsame')
cTotxyz.SaveAs('../pdfs/hTotxyz.pdf')
cTotxyz.SaveAs('../pdfs/hDeutxyz.root')

print 'done'