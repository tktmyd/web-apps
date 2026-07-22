import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell
def _(plt):
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{newpxmath, newpxtext} \usepackage{bm}'
    #plt.rcParams['text.latex.preamble'] = r'\usepackage{sfmath} \usepackage{bm}'
    plt.rcParams['font.family'] = 'Palatino'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 津波の分散曲線と振動パターン
    """)
    return


@app.cell
def _(np, plt):
    def tsunami_dispersion_motion(L): 
        """
        Parameters
        ----------
        L: h / lambda

        """

        ## 分散曲線
        LL = np.logspace(-3, 1, 501)
        cn = np.tanh(2 * np.pi * LL) / (2 * np.pi * LL)    

        fig = plt.figure(figsize=[8, 6])
        ax1 = fig.add_axes([0.1, 0.1, 0.5, 0.8])
        ax2 = fig.add_axes([0.6, 0.15, 0.3, 0.78])
        ax1.plot(1/LL, cn, lw=2, color='darkblue')
        ax1.set_xscale('log')
        ax1.set_xlabel(r'$\lambda\,/\,h$')
        ax1.set_ylabel(r'$c(\lambda)\,/\,\sqrt{g_0 h}$')
        ax1.set_xticks([0.1, 1, 10, 100, 1000])
        ax1.set_yticks([0, 0.5, 1])
        ax1.set_aspect(4)
        ax1.grid(alpha=0.5)
        ax1.plot([1/L, 1/L], [-0.1, 1.1], color='lightblue', alpha=0.5, lw=4)
        ax1.set_ylim(0., 1.05)
        ax1.set_xlim(0.1, 1000)

        ## Partile motion
        kh = 2 * np.pi * L
        # scale length defined by sqrt of area of particle motion
        A0 = max(np.sqrt(np.pi * np.cosh(kh) * np.sinh(kh)) * 2, np.cosh(kh))

        cr = np.sqrt(np.tanh(kh) / kh) 

        for zc in np.arange(0.95, 0.04, -0.15):
            kz = zc * kh

            Ax = np.cosh(kh-kz) / A0
            Az = np.sinh(kh-kz) / A0

            theta = np.arange(0, 2*np.pi, 2 * np.pi / 360)
            xx =   Ax * np.sin(theta)
            zz = - Az * np.cos(theta) + zc

            ax2.plot(xx, zz, clip_on = False, color=(zc/2, zc/2, zc/2))

            for angle in np.pi/4, 5*np.pi/4: 
                if max(Ax, Ax) < 0.1: 
                    continue
                xya1 = (Ax * np.sin(angle), -Az * np.cos(angle)+ zc)
                xya2 = (Ax * np.sin(angle+0.1), -Az * np.cos(angle+0.1)+ zc)
                ax2.annotate("", xy=xya2, xytext=xya1, 
                            arrowprops=dict(
                            arrowstyle="-|>",
                            color=(zc/2, zc/2, zc/2), 
                            mutation_scale=15,
                            shrinkA=0,
                            shrinkB=0,),)

        ax2.text(-1.05, -0.05, rf'$\lambda \, /  \, h={1/L:.1f}$', va = 'top', ha='left', 
               bbox={'facecolor': 'white', 'alpha': 0.8, 'linewidth': 0})
        ax2.text(1.0, 1.05, rf'$c = {cr:.2f} \sqrt{{g_0 h}}$', va='center', ha='right')

        ax2.set_xlim(-1.1, 1.1)
        ax2.set_ylim(-0.1, 1.1)
        ax2.set_aspect(4)
        ax2.fill_between(np.arange(-1.1, 1.2, 0.1), 0, 1, color=(0.8, 0.85, 1), alpha=.5)
        ax2.fill_between(np.arange(-1.1, 1.2, 0.1), 1, 2, color=(0.5, 0.5, 0.5), alpha=.5)
        ax2.set_xlim(-1.1, 1.1)
        ax2.set_ylim(-0.2, 1.1)
        ax2.invert_yaxis()
        ax2.axis('off')
        plt.subplots_adjust(top=0.8, bottom=0.2)

    #    fig.tight_layout()

        return fig

    return (tsunami_dispersion_motion,)


@app.cell
def _(mo, np):
    slider_Linv = mo.ui.slider(steps=np.logspace(-1, 3, 25), value=10)
    return (slider_Linv,)


@app.cell
def _(mo, slider_Linv):
    mo.md(fr"""
    $\lambda\,/\,h$ : {slider_Linv} {slider_Linv.value:.1f}
    """)
    return


@app.cell
def _(slider_Linv, tsunami_dispersion_motion):
    tsunami_dispersion_motion(1/slider_Linv.value)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
