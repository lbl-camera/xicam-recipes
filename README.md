# xicam-recipes

Preperation:
------------
1. Make sure xicam works with anaconda
2. Add conda-forge to channels
`conda config --add conda-forge`
3. `conda install conda-build`
4. Install anconda-client (optional)
`conda install anaconda-client`

Build
-----
1. Make appropriate changes to **meta.yaml**  and **build.sh**
2. Run `conda build .` from the same directory as **meta.yaml** and **build.sh**

Upload
------
1. `anconda login`
2. `anaconda upload xicam-<name>.tar.bz2`
