''' Submission script for running the GIF Analysis code
Historammer and N-Tupler
'''
import sys,os
import commands


if __name__ == '__main__' and 'submit' in sys.argv:
    user = commands.getoutput('echo $USER')
    plotsDir = '/afs/cern.ch/work/'+user[0]+'/'+user+'/public/GIF/TestBeam5/'
    dryrun = 'dryrun' in sys.argv
    import Gif.TestBeamAnalysis.DualMeasurements as Meas
    #measurements = [Meas.meas[m] for m in ['2312','2095','2262','2064','2079','2224','2333']]
    #measList = [3084,3086,3088,3090,3092,3094,3095,3097,3099,3101,3103,3105,3107,3109,3111,3113,3115,3117,3119,3121,3123,3125,3127,3129,3131,3133]
    #measList = [3092, 3103, 3113, 3123, 2758, 3094, 3080, 2970, 2843, 2756]
    #measList = [3084,3086,3088,3090,3095,3097,3099,3101,3105,3107,3109,3111,3115,3117,3119,3121,3125,3127,3129,3131,3133]
    #3219,3220,
    '''
    measList = [3221,3222,3223,3224,3225,3226,3227,3228,3229,3230,3231,3232,3233,3234,3235,3236,3237,3238,3239,
                3240,3241,3242,3243,3244,3245,3246,3247,3248,3249,3250,3251,3252,3253,3254,3255,3256,3257,3284,3285,3286,
                3287,3288,3289,3290,3291,3295,3296,3297,3298,3299,3300,3301,3302,3303,3304,3305,3306,3307,3308,3309,3310,
                3311,3312,3313,3314,3315,3316,3317,3318,3319,3320,3321,3322,3323,3324,3325,3326,3327,3328,3334,3335,3336,
                3337,3338,3339,3340,3341,3342,3343,3344,3345,3346,3347,3348,3349,3350,3351,3352,3353,3354,3355,3356,3357,
                3358,3359,3360,3361,3367,3368,3369,3370,3371,3372,3373,3374,3375,3376,3377,3378,3379,3380,3381,3382,3383,
                3384,3385,3386,3387,3388,3389,3390,3391,3392,3393,3394,3395,3396,3397,3398,3399]
    '''

    measList = [3400,3401,3402,3403,3404,3405,3406,3407,3409,3410,3411,3412,3413,3414,3415,3416,3417,3418,3419,3420,3421,
                3422,3423,3424,3425,3426,3427,3428,3429,3430,3431,3432,3433,3434,3435,3436,3437,3438,3439,3440,3441,3442,
                3443,3444,3445,3446,3447,3448,3449,3450,3451,3452,3453,3454,3455,3456,3457,3458,3459,3460]

    measurements = [Meas.meas[str(m)] for m in measList]
    for TBM in measurements:
        # commented out since we only want trees (histos are chamber dependent)
        #chamber = TBM.cham
        test = TBM.runtype
        HV = TBM.HV
        beam = 'bOn' if TBM.beam else 'bOff'
        uAtt = 'uOff' if TBM.uAtt=='0' else 'u'+TBM.uAtt
        dAtt = 'dOff' if TBM.dAtt=='0' else 'd'+TBM.dAtt
        measNum = 'm'+TBM.meas
        fn = TBM.ROOTFile(prefix='/store/user/cschnaib/GIF/')
        #fn = TBM.fn
        # For Chris: # fn = TBM.fn
        ana_dataset = 'ana_%s.root'%(TBM.meas)
        #ana_dataset = 'ana_%(chamber)s_%(test)s_%(HV)s_%(beam)s_%(uAtt)s_%(dAtt)s_%(measNum)s.root'%locals()
        outPath = plotsDir+ana_dataset
        print TBM
        print "\033[1mINPUT:\033[m", fn
        print "\033[1mOUTPUT:\033[m", outPath
        print ""

        gif_py = open('GifAnalysis.py').read()
        # commented out since we only want trees (histos are chamber dependent)
        #if not 'noHistos' in sys.argv:
        #    gif_py += '\ndoHistos(process)\n'
        #if not 'noTree' in sys.argv:
        gif_py += '\ndoTree(process)\n'
        # commented out since we only want trees (histos are chamber dependent)
        #process.GIFHistos.chamberType = cms.untracked.string('%(chamber)s')
        gif_py += '''
process.source.fileNames  = cms.untracked.vstring('%(fn)s')
process.TFileService.fileName = cms.string('%(outPath)s')
''' % locals()

        open('submit_GifAnalysis.py','wt').write(gif_py)
        if dryrun:
            pass
        else: 
            cmd = 'cmsRun submit_GifAnalysis.py'
            print "\033[1mEXECUTING:\033[m", cmd
            os.system(cmd)

    if not dryrun:
        pass
        os.system('rm submit_GifAnalysis.py submit_GifAnalysis.pyc')
