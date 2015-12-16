# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015, Yung-Yu Chen <yyc@solvcon.net>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""
Mesh I/O for HTML files based on THREE.js.
"""


from __future__ import absolute_import, division, print_function


from ..py3kcompat import NotADirectoryError
import warnings
import os
import shutil
import string

try:
    import jinja2
except ImportError: # not requiring jinja2 for now.
    pass

from .. import exception

from . import core as iocore


class WebVisual(object):

    def __init__(self, blk):
        self.blk = blk
        super(WebVisual, self).__init__()

    def _get_vertex(self):
        if self.blk.ndim == 2:
            tmpl = "new THREE.Vector3(%g,%g,0)"
        else:
            tmpl = "new THREE.Vector3(%g,%g,%g)"
        return ",\n".join(tmpl % tuple(pnt) for pnt in self.blk.ndcrd)

    def _get_face(self):
        tmpl = "new THREE.Face3(%d,%d,%d)"
        if self.blk.ndim == 2:
            return ",\n".join(
                tmpl % tuple(nds[1:nds[0]+1]) for nds in self.blk.clnds)
        else:
            return ",\n".join(
                tmpl % tuple(nds[1:nds[0]+1]) for nds in self.blk.fcnds)

    def write_jsfile(self, fname):
        with open(os.path.join(fname), 'w') as fobj:
            fobj.write("""function get_geometry() {
    var geom = new THREE.Geometry();
    geom.vertices.push(
""")
            fobj.write(self._get_vertex())
            fobj.write("""
    );
    geom.faces.push(
""")
            fobj.write(self._get_face())
            fobj.write("""
    );
    return geom;
}
""")


class HtmlIO(iocore.FormatIO):
    """
    Experimental HTML/THREE.js writer.
    """

    BASEDIR = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'three')

    def __init__(self, **kw):
        self.blk = kw.pop('blk', None)
        super(HtmlIO, self).__init__()

    @classmethod
    def _copy_basefile(cls, fname, dirname):
        shutil.copy(os.path.join(cls.BASEDIR, fname),
                    os.path.join(dirname, fname))

    def _generate_meshfile(self, fname, dirname):
        wv = WebVisual(self.blk)
        wv.write_jsfile(os.path.join(dirname, fname))

    def _save_directory(self, dirname, ball_radius):
        self._copy_basefile('TrackballControls.js', dirname)
        self._generate_meshfile('mesh.js', dirname)
        self._copy_basefile('main.js', dirname)

        with open(os.path.join(self.BASEDIR, 'index.html')) as fobj:
            template = jinja2.Template(fobj.read())
        with open(os.path.join(dirname, 'index.html'), 'wb') as fobj:
            htmldata = template.render(
                title=os.path.split(dirname.strip('/'))[-1],
                ball_radius=ball_radius,
                scripts=[
                    "https://cdnjs.cloudflare.com/ajax/libs/"
                        "three.js/r73/three.min.js",
                    "TrackballControls.js",
                    "mesh.js",
                    "main.js",
                ],
            )
            fobj.write(htmldata.encode())

    def save(self, stream, ball_radius=0.0):
        if not isinstance(stream, str):
            raise AssertionError("stream must be directory name")
        if os.path.exists(stream):
            if not os.path.isdir(stream):
                raise NotADirectoryError("stream is not a directory")
            else:
                warnings.warn("output directory (%s) already exists" % stream,
                              exception.IOWarning)
        else:
            os.mkdir(stream)
        self._save_directory(stream, ball_radius=ball_radius)
