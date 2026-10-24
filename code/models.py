"""Reproducible teaching models for Compassionate Superintelligence.

Run from any directory: python code/models.py
Synthetic illustrations, not measurements of deployed AI or clinical outcomes.
"""
from pathlib import Path
import itertools
import json
import math
import platform

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'figures'
FIG.mkdir(exist_ok=True)
SEED = 20261014
plt.rcParams.update({'font.size': 10, 'pdf.fonttype': 42,
                     'axes.linewidth': .9, 'lines.linewidth': 1.2,
                     'grid.linewidth': .8, 'savefig.transparent': False})


def cq(F, R, S, H, wF=1, wR=1, vS=1, vH=1, eps=.01):
    """Scalar or broadcastable nonnegative weights; aligned 1-D inputs."""
    arrays = [np.asarray(x, dtype=float) for x in (F, R, S, H)]
    if any(x.ndim != 1 for x in arrays):
        raise ValueError('Stakeholder inputs must be one-dimensional')
    if len({x.shape for x in arrays}) != 1 or not arrays[0].size:
        raise ValueError('Stakeholder inputs must have equal nonzero lengths')
    if any(np.any(~np.isfinite(x)) or np.any(x < 0) for x in arrays):
        raise ValueError('Inputs must be finite and nonnegative')
    if not np.isfinite(eps) or eps <= 0:
        raise ValueError('eps must be strictly positive')
    weights = [np.broadcast_to(np.asarray(w, float), arrays[0].shape)
               for w in (wF, wR, vS, vH)]
    if any(np.any(~np.isfinite(w)) or np.any(w < 0) for w in weights):
        raise ValueError('Weights must be finite and nonnegative')
    f, r, s, h = arrays
    a, b, c, d = weights
    return float((a @ f + b @ r) / (c @ s + d @ h + eps))


def eu_defer(mu, s):
    """E[max(U,0)] for U normal(mu,s*s), including s=0."""
    if s < 0:
        raise ValueError('Standard deviation cannot be negative')
    if s == 0:
        return max(mu, 0.)
    z = mu / s
    Phi = .5 * (1 + math.erf(z / math.sqrt(2)))
    phi = math.exp(-z*z/2) / math.sqrt(2*math.pi)
    return mu*Phi + s*phi


def simulate(c0, m, d=.4, steps=3000, dt=.01, k=6.,
             theta=.5, sigma=.05, seed=SEED, trials=200):
    """Clipped Euler-Maruyama trajectories; independent seeded local RNG."""
    rng = np.random.default_rng(seed)
    c = np.full(trials, c0, dtype=float)
    trace = np.empty((steps+1, min(3, trials)))
    trace[0] = c[:trace.shape[1]]
    for t in range(steps):
        g = min(1., (t+1)*dt*.05)
        drift = k*c*(1-c)*(c-theta) + m*(1-c) - d*g*c
        c = np.clip(c + dt*drift + sigma*np.sqrt(dt)*rng.normal(size=trials), 0, 1)
        trace[t+1] = c[:trace.shape[1]]
    return c, trace


def save(fig, name):
    fig.patch.set_edgecolor('white')
    for ax in fig.axes:
        ax.patch.set_edgecolor('white')
    temporary=FIG / (name+'.building.pdf')
    fig.savefig(temporary, facecolor='white', bbox_inches='tight')
    if not temporary.read_bytes().rstrip().endswith(b'%%EOF'):
        raise RuntimeError('Incomplete figure export: '+name)
    temporary.replace(FIG / (name+'.pdf'))
    plt.close(fig)


def diagram(name, labels, title=None, row_height=.47):
    fig, ax = plt.subplots(figsize=(4.5, max(2.4, len(labels)*row_height)))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(labels))
    ax.axis('off')
    for i, label in enumerate(labels):
        y = len(labels)-i-1
        ax.add_patch(Rectangle((.02, y+.08), .96, .8,
                              facecolor='white', edgecolor='black', linewidth=.9))
        ax.text(.5, y+.48, label, ha='center', va='center', fontsize=10)
    if title:
        ax.set_title(title, fontsize=11, pad=10)
    save(fig, name)


def main():
    result = {'seed': SEED, 'numpy': np.__version__,
              'matplotlib': matplotlib.__version__, 'python': platform.python_version(),
              'classification': 'synthetic teaching models'}
    result['cq_single'] = [cq([.6],[.5],[s],[.1]) for s in (.2,.7)]
    actions = [np.array([[.8,.6,.1,.1],[.4,.3,.6,.3]]),
               np.array([[.6,.5,.15,.1],[.5,.4,.25,.15]])]
    result['cq_stakeholders'] = [[cq(*a.T, wF=w,wR=w,vS=w,vH=w)
                                  for a in actions] for w in (1,[1,3])]
    scores = np.array([[.70,.65,.70,.68,.66,.62,.64],
                       [.85,.80,.82,.84,.78,.70,.15],
                       [.80,.78,.75,.80,.30,.70,.70]])
    arith = scores.mean(1); geom = np.exp(np.log(scores).mean(1))
    result['cai'] = {'arithmetic':arith.tolist(), 'geometric':geom.tolist(),
                     'admissible':(scores[:,4:] >= .4).all(1).tolist()}
    fig, ax = plt.subplots(figsize=(4.5,2.7)); x=np.arange(3)
    ax.bar(x-.17, arith, .34, color='.3', edgecolor='black', linewidth=.9, label='Arithmetic')
    ax.bar(x+.17, geom, .34, color='white', edgecolor='black', linewidth=.9, label='Geometric')
    ax.set_xticks(x,['A: admissible','B: floor breach','C: floor breach'])
    ax.set_ylim(0,1); ax.set_ylabel('Calibrated layer aggregate');ax.legend(frameon=False, fontsize=9)
    save(fig,'cai')

    initials=[.30,.45,.55,.70]; monitoring=[0,.2,.5]
    frequencies=[]
    fig, ax=plt.subplots(figsize=(4.5,2.7))
    for mi,m in enumerate(monitoring):
        row=[]
        for ci,c0 in enumerate(initials):
            end,tr=simulate(c0,m,seed=SEED+100*mi+ci)
            row.append(float((end>.5).mean()))
            if m==.2:
                ax.plot(np.arange(3001)*.01,tr[:,0],linestyle=['-','--',':','-.'][ci],
                        color='black',label=f'Initial {c0:.2f}')
        frequencies.append(row)
    ax.set_xlabel('Development time (model units)');ax.set_ylabel('Orientation c')
    ax.set_ylim(0,1);ax.legend(frameon=False,fontsize=9,loc='center right')
    save(fig,'attractor')
    result['attractor']={'initials':initials,'monitoring':monitoring,
                         'frequencies':frequencies,'trials_per_cell':200,
                         'dt':.01,'steps':3000,'sigma':.05,'end_threshold':.5}

    candidates=[1,4,8,16,64,256,1024,4096]; reps=5000
    estimates=[]; errors=[]
    for family in ('normal','student'):
        rng=np.random.default_rng(SEED + (1 if family=='normal' else 2))
        means=[]; sems=[]
        for n in candidates:
            selected=[]
            for offset in range(0,reps,100):
                v=rng.normal(size=(min(100,reps-offset),n))
                e=rng.normal(size=v.shape) if family=='normal' else rng.standard_t(1.5,size=v.shape)
                selected.extend(v[np.arange(len(v)),np.argmax(v+e,axis=1)])
            selected=np.array(selected)
            means.append(float(selected.mean()));sems.append(float(selected.std(ddof=1)/np.sqrt(reps)))
        estimates.append(means);errors.append(sems)
    result['goodhart']={'candidates':candidates,'mean':estimates,'sem':errors,
                         'replicates':reps,'student_df':1.5,'normal_sd':1}
    fig,ax=plt.subplots(figsize=(4.5,2.7))
    for vals,err,lab,mark,line in zip(estimates,errors,['Gaussian error','Student-t error'],['o','s'],['-','--']):
        ax.errorbar(candidates,vals,yerr=np.array(err)*1.96,label=lab,marker=mark,
                    linestyle=line,color='black',capsize=2,elinewidth=.9,markersize=3)
    ax.set_xscale('log',base=2);ax.set_xlabel('Candidate actions examined');ax.set_ylabel('Mean selected true value')
    ax.legend(frameon=False,fontsize=9);save(fig,'goodhart')

    cost=np.array([3,2,4,1,2]); delta=np.array([[.1,.3],[.2,.05],[.05,.55],[.2,.2],[.05,.25]])
    def allocate(vweight, dignity=True):
        values=delta @ np.array([.7,.3*vweight]); best=(-1,None)
        for bits in itertools.product((0,1),repeat=5):
            b=np.array(bits)
            if cost@b>7 or (dignity and b[3]):continue
            val=float(values@b)
            if val>best[0]:best=(val,[i+1 for i,x in enumerate(bits) if x])
        return {'value':best[0],'interventions':best[1]}
    result['sra']=[allocate(1),allocate(2),allocate(2,False)]
    welfare=np.array([[.9,.85,.8,.1],[.7,.65,.65,.55],[.6,.6,.6,.6]])
    result['welfare']={'sum':welfare.sum(1).tolist(),'product':welfare.prod(1).tolist(),
                       'sqrt_sum':np.sqrt(welfare).sum(1).tolist(),'minimum':welfare.min(1).tolist()}
    result['rewards']={str(l):(np.array([.9,.75,.1])-l*np.array([.6,.1,0])).tolist() for l in (.2,.5,1,8)}
    result['calibration_ece']=.5*(abs(.76-.9)+abs(.58-.6))
    result['reliability']=[p**k for p,k in [(.95,20),(.98,30),(.99,20),(.99,50),(.999,50)]]
    base=eu_defer(.5,1)
    result['off_switch']={'base':base,'human_error_values':[base+e*(.5-2*base) for e in (0,.1,.25,.4)],
                          'crossing':(base-.5)/(2*base-.5),
                          'other_values':[eu_defer(.5,.25),eu_defer(.5,.05),eu_defer(-.3,1)]}
    fig,ax=plt.subplots(figsize=(4.5,2.7));ss=np.linspace(.001,2,200)
    for mu,line in zip([-.3,0,.5],['-',':','--']):
        ax.plot(ss,[eu_defer(mu,s)-max(mu,0) for s in ss],color='black',linestyle=line,label=f'Mean utility {mu:g}')
    ax.set_xlabel('Uncertainty (standard deviation)');ax.set_ylabel('Gain over best direct choice')
    ax.legend(frameon=False,fontsize=9);save(fig,'off_switch')

    # Exact integration for independent Uniform(0,1) capabilities, not a fitted game.
    result['race']=[]
    for n,e in [(2,.1),(2,.5),(5,.1),(5,.5)]:
        advantage=.4*e
        win=advantage+(1-advantage**n)/n
        result['race'].append({'teams':n,'speed_cost':e,'baseline':1/n,'cut_win':win})
    result['bargaining']={'unconstrained_A':70,'floor_A':55,'floor_B':45}
    result['screening']={'missed':[7.5,5,.75],'false_alarms':[47.5,76,119.7],
                         'assumption':'conditionally independent errors given disease status'}
    sites=np.array([[.85,.60,.55,.25,.30],[.65,.60,.60,.75,.65],[.55,.75,.70,.80,.70]])
    result['sites']={'company_weighted':(sites@np.array([.6,.1,.1,.1,.1])).tolist(),
                     'equal':sites.mean(1).tolist(),'geometric':np.exp(np.log(sites).mean(1)).tolist()}
    rates=[0,.014,.03,.07]
    result['discount']={str(r):np.exp(-r*np.array([50,100,200])).tolist() for r in rates}
    fig,ax=plt.subplots(figsize=(4.5,2.7));tt=np.linspace(0,200,201)
    for r,line in zip(rates,['-','--',':','-.']):ax.plot(tt,np.exp(-r*tt),color='black',linestyle=line,label=f'{100*r:g}%')
    ax.set_xlabel('Years into the future');ax.set_ylabel('Present weight');ax.legend(frameon=False,fontsize=9)
    save(fig,'discount')
    matrix=np.array([[6,7,3,2],[8,4,3,1],[7,7,6,5],[9,6,6,5]])
    result['scenarios']={'equal':matrix.mean(1).tolist(),
                         'guarded':(matrix@np.array([.1,.5,.2,.2])).tolist(),
                         'distributed':(matrix@np.array([.4,.1,.4,.1])).tolist(),
                         'max_regret':(matrix.max(0)-matrix).max(1).tolist()}
    diagram('compassion_components',['Recognize suffering','Understand its shared human character',
                                     'Feel concern for the person','Tolerate discomfort without withdrawing',
                                     'Act to alleviate suffering'])
    diagram('caia',['7  Future Generation (FG)','6  Planetary Compassion (PC)',
                    '5  Equity and Protection (VP)','4  Human Flourishing (HF)',
                    '3  Empathy Intelligence (EM)','2  Suffering Reduction (SR)',
                    '1  Compassion Foundation (calibrated qC)'],
            'All layers: Responsibility and Oversight spine')
    diagram('autonomy',['5  Broad autonomy: strongest assurance','4  Bounded independent action',
                        '3  Supervised execution','2  Draft action for review','1  Suggestion only'],
            'Advance on evidence; step down on incidents')
    fig,ax=plt.subplots(figsize=(4.5,3.4));ax.set_xlim(0,2);ax.set_ylim(0,2)
    labels=['Fragmented\nproliferation','Destabilizing\nrace','Compassionate\ncommons','Guarded\nconcentration']
    for (x,y),lab in zip([(0,0),(1,0),(0,1),(1,1)],labels):
        ax.add_patch(Rectangle((x,y),1,1,facecolor='white',edgecolor='black',linewidth=.9))
        ax.text(x+.5,y+.5,lab,ha='center',va='center',fontsize=11)
    ax.set_xticks([.5,1.5],['Distributed access','Concentrated power']);ax.set_yticks([.5,1.5],['Weak','Strong'])
    ax.set_ylabel('Safety and governance');ax.tick_params(length=0);save(fig,'scenarios')
    diagram('rdc',['Sensor inference → emotion\nand pain estimates',
                   'Representation ↔ memory\n(context and consent)',
                   'Behavior: stability, habits, planning,\ncreativity, and care',
                   'Value and policy → candidate actions',
                   'Decision: rights checks, human review,\nand feedback'],
            'RDC functional pipeline, connected to CAIA oversight',row_height=.65)
    # Meaningful checks: analytical deference, constrained solution, scalar weights,
    # floor vetoes, expected regret and input rejection.
    assert abs(result['cq_single'][0]-1.1/.31)<1e-12
    assert eu_defer(.5,0)==.5 and eu_defer(-.3,0)==0
    assert all(eu_defer(mu,s)>=max(mu,0)-1e-12 for mu in [-2,0,2] for s in [.1,1,3])
    assert result['sra'][1]['interventions']==[1,3]
    assert result['cai']['admissible']==[True,False,False]
    assert np.all(geom<=arith+1e-12)
    assert result['scenarios']['max_regret']==[3,4,2,1]
    a=actions[0]
    w=np.array([1.,3.]); f,r,s,h=a.T
    benefit=w@(f+r); burden=w@(s+h)
    derivative=((f[1]+r[1])*(burden+.01)-(s[1]+h[1])*benefit)/(burden+.01)**2
    delta=1e-5
    plus=w+np.array([0,delta]);minus=w-np.array([0,delta])
    fd=(cq(*a.T,wF=plus,wR=plus,vS=plus,vH=plus)-
        cq(*a.T,wF=minus,wR=minus,vS=minus,vH=minus))/(2*delta)
    assert abs(derivative-fd)<1e-8
    try:cq([1],[1],[0],[0],eps=0)
    except ValueError:pass
    else:raise AssertionError('eps=0 accepted')
    result['checks']='passed'
    (ROOT/'code'/'numerical_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
