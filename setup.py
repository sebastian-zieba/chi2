from distutils.core import setup, Extension
import numpy.distutils.misc_util

import os
import sys
from distutils.ccompiler import new_compiler
import tempfile

"""
Check for OpenMP based on
https://github.com/MDAnalysis/mdanalysis/tree/develop/package/setup.py
retrieved 06/15/15
"""


def detect_openmp():
    """Does this compiler support OpenMP parallelization?"""
    compiler = new_compiler()
    print("Checking for OpenMP support... ")
    hasopenmp = hasfunction(compiler, 'omp_get_num_threads()')
    needs_gomp = hasopenmp
    if not hasopenmp:
        compiler.add_library('gomp')
    hasopenmp = hasfunction(compiler, 'omp_get_num_threads()')
    needs_gomp = hasopenmp
    if hasopenmp:
        print("Compiler supports OpenMP")
    else:
        print("Did not detect OpenMP support.")
    return hasopenmp, needs_gomp


def hasfunction(cc, funcname, include=None, extra_postargs=None):
    # From http://stackoverflow.com/questions/
    #            7018879/disabling-output-when-compiling-with-distutils
    tmpdir = tempfile.mkdtemp(prefix='hasfunction-')
    devnull = oldstderr = None
    try:
        try:
            fname = os.path.join(tmpdir, 'funcname.c')
            f = open(fname, 'w')
            if include is not None:
                f.write('#include %s\n' % include)
            f.write('int main(void) {\n')
            f.write('    %s;\n' % funcname)
            f.write('}\n')
            f.close()
            # Redirect stderr to /dev/null to hide any error messages
            # from the compiler.
            # This will have to be changed if we ever have to check
            # for a function on Windows.
            devnull = open('/dev/null', 'w')
            oldstderr = os.dup(sys.stderr.fileno())
            os.dup2(devnull.fileno(), sys.stderr.fileno())
            objects = cc.compile([fname], output_dir=tmpdir, extra_postargs=extra_postargs)
            cc.link_executable(objects, os.path.join(tmpdir, "a.out"))
        except Exception as e:
            return False
        return True
    finally:
        if oldstderr is not None:
            os.dup2(oldstderr, sys.stderr.fileno())
        if devnull is not None:
            devnull.close()


# checks whether OpenMP is supported
has_openmp, needs_gomp = detect_openmp()
parallel_args = ['-fopenmp', '-std=c99'] if has_openmp else ['-std=c99']
parallel_libraries = ['gomp'] if needs_gomp else []



_chi2 = Extension("_chi2", ["_chi2.c", "chi2.c"], extra_compile_args=parallel_args, libraries=parallel_libraries)

setup(
    ext_modules=[_chi2],
    include_dirs=[numpy.get_include()]
)
#final test
