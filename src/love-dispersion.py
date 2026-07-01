import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2層構造のLove波分散曲線
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy.optimize as so

    return np, plt


@app.function
def fig_default_style(ax):
    """
        Matplotlib の axes オブジェクト ax に対して標準的な設定を行う
    """

    ax.tick_params(axis='both', direction='in', length=5, pad=7)
    ax.spines['top'   ].set_visible(False)
    ax.spines['right' ].set_visible(False)
    ax.spines['left'  ].set_position(('outward', 10))
    ax.spines['bottom'].set_position(('outward', 10))
    ax.grid(linestyle = 'dashed', linewidth = 1., color = (220/255,220/255,220/255), alpha=0.8)
    ax.set_xlabel(ax.get_xlabel(), fontsize = 'large', fontname='Helvetica Neue')
    ax.set_ylabel(ax.get_ylabel(), fontsize = 'large', fontname='Helvetica Neue')
    ax.set_title(ax.get_title(), fontsize = 'xx-large', fontname='Helvetica Neue')
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Helvetica Neue')
        label.set_fontsize(10)


@app.cell
def _(np):
    ## parameters
    fmin = 0.05 # Hz
    fmax = 0.5  # Hz
    Hmin = 5    # km
    Hmax = 30   # km
    beta2 = 3.5 # deep layer
    vrmin = 0.2 # beta1 = vr * beta2
    vrmax = 0.9 # 
    nfreq = 5001
    π = np.pi
    return Hmax, Hmin, beta2, fmax, fmin, vrmax, vrmin, π


@app.cell
def _(np, π):
    def love_dispersion_solution_data(β1, β2, H, f):
        """
            2層構造のLove波の分散曲線推定の左辺と右辺の可視化用データを準備する
        """
        # 密度は変わらないと仮定

        ω = 2 * π * f
        nx = 2000
        xmax = ω * H * np.sqrt(1/β1**2 - 1/β2**2)
        xx = np.linspace(xmax/nx, xmax, nx)

        xtmp = xx / (ω * H)

        # tanが不連続になるところをマスクする
        lhs = np.tan(xx)
        msk = np.abs(np.cos(xx))  < 0.01
        lhs[msk] = np.nan

        rhs = (β2/β1)**2 * np.sqrt(1/β1**2 - 1/β2**2 - xtmp**2) / xtmp

        return xx, lhs, rhs


    return (love_dispersion_solution_data,)


@app.cell
def _(np, π):
    def disp_lhs(c, β1, β2, H, f):

        lhs = np.tan(2 * π * f * H * np.sqrt(1/β1**2 - 1/c**2))

        return lhs

    def disp_rhs(c, β1, β2, H, f):

        rhs = (β2 / β1)**2 * np.sqrt(1/c**2 - 1/β2**2) / np.sqrt(1/β1**2 - 1/c**2)

        return rhs

    def disp_eq(c, β1, β2, H, f):

        return disp_lhs(c, β1, β2, H, f) - disp_rhs(c, β1, β2, H, f)

    return disp_eq, disp_lhs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Love波分散方程式の$x$軸は
    $$
    x = \omega H \sqrt{1/\beta_1^2 - 1/c^2}
    $$
    なので，その最大値は
    $$
    x_{\mathrm{max}} = \omega H \sqrt{1/\beta_1^2 - 1/\beta_2^2}
    $$

    解は$\tan(x)$が正になる
    - $[0, \pi/2)$
    - $[\pi, 3\pi/2)$
    - $[2\pi, 5\pi/2)$
    - $[3\pi, 7\pi/2)$

    に存在するから，解の個数は
    $$
    n = \left\lceil \frac{x_\mathrm{max}}{\pi} \right\rceil
    $$
    となる．
    解は上記の範囲で探索するが，$\tan$が発散するところを避けて，$0, \pi, 2\pi \dots$を初期値にするとよさそう．
    初期値を$c_0$とすると，$k$次モードでは

    $$
    \omega H \sqrt{1/\beta_1^2 - 1/c_0^2} = k \pi
    $$
    から
    $$
    c_0 = \left(
        \frac{1}{\beta_1^2} - \frac{k^2 \pi^2 }{\omega^2 H ^2}
    \right)^{-1/2}
    $$
    """)
    return


@app.cell
def _(np, π):
    def nmode(beta1, beta2, H, f): 
        xmax = 2 * π * f * H * np.sqrt( 1/beta1**2 - 1/beta2**2 )
        return int(np.ceil(xmax / π))

    return (nmode,)


@app.cell
def _(disp_eq, nmode, np, π):
    def get_love_c(β1, β2, H, f, debug=False): 

        n = nmode(β1, β2, H, f)
        c = np.zeros(n) * np.nan
        for k in range(n):

            cb = max((1/β1**2 - ((k*π)/(2*π*f*H))**2)**(-1./2.) + 1e-7, β1)
            ce = min((1/β1**2 - min( (((k+0.5)*π)/(2*π*f*H))**2, 1/β1**2-1e-7))**(-1./2.) - 1e-7, β2)
            v0 = 0
            c0p=0
            if debug:
                print(cb, ce)
            for c0 in np.linspace(cb, ce, 2000):
                v1 = disp_eq(c0, β1, β2, H, f)
                if v0 * v1 < 0: 
                    c[k] = (c0+c0p)/2
                    break
                else:
                    v0 = v1
                    c0p = c0

            #_ = so.fsolve(disp_eq, c0, args=(β1, β2, H, f))
            #c[k] = _[0]
        return c

    return (get_love_c,)


@app.cell
def _(np, π):
    def love_eigen(c, β1, β2, H, f, z): 

        ω = 2 * π * f
        b1c = np.sqrt(1/β1**2 - 1/c**2)
        b2c = np.sqrt(1/c**2 - 1/β2**2)
        l1 = []
        for zz in z: 
            if zz <= H:
                l1.append(np.cos(ω * b1c * zz))
            else: 
                l1.append(np.cos(ω * b1c * H) * np.exp(-ω * b2c * (zz-H)))

        return l1

    return (love_eigen,)


@app.cell
def _(
    disp_lhs,
    fmax,
    fmin,
    get_love_c,
    love_dispersion_solution_data,
    love_eigen,
    nmode,
    np,
    plt,
    π,
):
    def love_plot(β2, vr, H, f):    

        β1 = β2 * vr

        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(222)

        _ = love_dispersion_solution_data(β1, β2, H, f)
        c = get_love_c(β1, β2, H, f)

        ymax = disp_lhs(c[0], β1, β2, H, f) * 1.2

        ax1.set_xlabel(r'$\omega H \sqrt{1/\beta_1^2 - 1/c^2}$')
        ax1.plot(_[0], _[1], label='LHS', color=(250/255, 50/255, 100/255))
        ax1.plot(_[0], _[2], label='RHS', color=(50/255, 150/255, 250/255))
        ax1.set_ylim([0, ymax])
        ax1.set_xlim([0, _[0][-1]])
        ax1.legend(loc='upper right')

        _xx = 2 * π * f * H * np.sqrt(1/β1**2 - 1/c**2)
        _yy = disp_lhs(c, β1, β2, H, f)
        ax1.plot(_xx, _yy, 'o', color='black')

        fig_default_style(ax1)

        ax2 = fig.add_subplot(221)

        freq = np.linspace(fmin, fmax, 101)[::-1]
        nmax = nmode(β1, β2, H, freq[0])
        cc = np.zeros([nmax, len(freq)]) * np.nan
        for i, ff in enumerate(freq): 
            _cc = get_love_c(β1, β2, H, ff)
            for j, c_ in enumerate(_cc): 
                cc[j,i] = _cc[j]

        ax2.plot([f, f], [β1, β2], alpha=0.4, linewidth=2.5, color='gray' )

        for i, _c in enumerate(cc):
            ax2.plot(freq, _c, color='darkorange')

        ax2.set_ylim([β1, β2])
        ax2.set_xlim([fmin, fmax])
        ax2.set_xlabel('Frequency [Hz]')
        ax2.set_ylabel('Phase speed [km/s]')
        #ax2.legend(loc='upper left')
        fig_default_style(ax2)

        z = np.linspace(0, 60, 601)

        for k in range(6):
            try:
                l1 = love_eigen(c[k], β1, β2, H, f, z)
            except: 
                l1 = np.zeros(len(z)) * np.nan
            axe = fig.add_subplot(2, 6, 7 + k)
            axe.plot(l1, z, color=(0.4, 0.8, 0.4))
            axe.set_xlim([-1.1, 1.1])
            axe.set_ylim([0, 60])
            axe.invert_yaxis()
            axe.set_title(f'mode = {k}')
            axe.spines['top'   ].set_visible(False)
            axe.spines['right' ].set_visible(False)
            if k == 0 :
                axe.spines['left'  ].set_position(('outward', 10))
                axe.set_ylabel("depth [km]")
            else:
                axe.tick_params(axis='y', labelleft=False, left=False)
                axe.spines['left'  ].set_visible(False)            
            axe.spines['bottom'  ].set_position(('outward', 10))
            axe.grid(linestyle = 'dashed', linewidth = 1., color = (220/255,220/255,220/255), alpha=0.8)

        plt.subplots_adjust(wspace=0.2, hspace=0.6)

        fig.tight_layout()

        return fig

    return (love_plot,)


@app.cell
def _(Hmax, Hmin, fmax, fmin, mo, vrmax, vrmin):
    slider_H = mo.ui.slider(start=Hmin, stop=Hmax, step=1, value = 20)
    slider_f = mo.ui.slider(start=fmin, stop=fmax, step=0.05, value = 0.1)
    slider_vr = mo.ui.slider(start=vrmin, stop=vrmax, step=0.1, value=0.8)
    return slider_H, slider_f, slider_vr


@app.cell(hide_code=True)
def _(beta2, mo, slider_H, slider_f, slider_vr):
    mo.md(rf"""
    ## 計算パラメタ

    | パラメタ名 | 値 | 調整 |
    | ------- | --- | --- |
    | 下層速度 | $\beta_2 = {beta2}$ km/s |（固定値）|
    | 密度比 | $\rho_1 / \rho_2 = 1$ | （固定値）|
    | 速度比 | $\beta_1 / \beta_2 = {slider_vr.value}$ | {slider_vr} |
    | 層厚 | $H = {slider_H.value}$ km | {slider_H} |
    | 周波数 | $f = {slider_f.value}$ Hz | {slider_f} |

    """)
    return


@app.cell
def _(love_plot, slider_H, slider_f, slider_vr):
    love_plot(3.5, slider_vr.value, slider_H.value, slider_f.value)

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
