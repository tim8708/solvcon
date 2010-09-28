# -*- coding: UTF-8 -*-

from unittest import TestCase
from ...testing import get_blk_from_oblique_neu, get_blk_from_sample_neu

class CheckDomainIO(TestCase):
    def _check_shape(self, newblk, blk):
        # shape.
        self.assertEqual(newblk.ndim, blk.ndim)
        self.assertEqual(newblk.nnode, blk.nnode)
        self.assertEqual(newblk.nface, blk.nface)
        self.assertEqual(newblk.ncell, blk.ncell)
        self.assertEqual(newblk.nbound, blk.nbound)
        self.assertEqual(newblk.ngstnode, blk.ngstnode)
        self.assertEqual(newblk.ngstface, blk.ngstface)
        self.assertEqual(newblk.ngstcell, blk.ngstcell)
        # serial number.
        self.assertEqual(newblk.blkn, blk.blkn)
    def _check_group(self, newblk, blk):
        # group names.
        self.assertEqual(len(newblk.grpnames), len(blk.grpnames))
        for igrp in range(len(blk.grpnames)):
            self.assertEqual(newblk.grpnames[igrp], blk.grpnames[igrp])
    def _check_bc(self, newblk, blk):
        self.assertTrue((newblk.bndfcs == blk.bndfcs).all())
        self.assertEqual(len(newblk.bclist), len(blk.bclist))
        for ibc in range(len(newblk.bclist)):
            newbc = newblk.bclist[ibc]
            bc = blk.bclist[ibc]
            # meta data.
            self.assertEqual(newbc.sern, bc.sern)
            self.assertEqual(newbc.name, bc.name)
            self.assertNotEqual(newbc.blk, bc.blk)
            self.assertEqual(newbc.blkn, bc.blkn)
            self.assertTrue(newbc.svr == None)
            # faces.
            self.assertTrue((newbc.facn[:,:2] == bc.facn[:,:2]).all())
            # values.
            self.assertEqual(newbc.value.shape[1], bc.value.shape[1])
            if newbc.value.shape[1] > 0:
                self.assertTrue((newbc.value == bc.value).all())
    def _check_array(self, newblk, blk):
        # metrics.
        self.assertTrue((newblk.ndcrd == blk.ndcrd).all())
        self.assertTrue((newblk.fccnd == blk.fccnd).all())
        self.assertTrue((newblk.fcnml == blk.fcnml).all())
        self.assertTrue((newblk.fcara == blk.fcara).all())
        self.assertTrue((newblk.clcnd == blk.clcnd).all())
        self.assertTrue((newblk.clvol == blk.clvol).all())
        # type.
        self.assertTrue((newblk.fctpn == blk.fctpn).all())
        self.assertTrue((newblk.cltpn == blk.cltpn).all())
        self.assertTrue((newblk.clgrp == blk.clgrp).all())
        # connectivity.
        self.assertTrue((newblk.fcnds == blk.fcnds).all())
        self.assertTrue((newblk.fccls == blk.fccls).all())
        self.assertTrue((newblk.clnds == blk.clnds).all())
        self.assertTrue((newblk.clfcs == blk.clfcs).all())
        # ghost metrics.
        self.assertTrue((newblk.gstndcrd == blk.gstndcrd).all())
        self.assertTrue((newblk.gstfccnd == blk.gstfccnd).all())
        self.assertTrue((newblk.gstfcnml == blk.gstfcnml).all())
        self.assertTrue((newblk.gstfcara == blk.gstfcara).all())
        self.assertTrue((newblk.gstclcnd == blk.gstclcnd).all())
        self.assertTrue((newblk.gstclvol == blk.gstclvol).all())
        # ghost type.
        self.assertTrue((newblk.gstfctpn == blk.gstfctpn).all())
        self.assertTrue((newblk.gstcltpn == blk.gstcltpn).all())
        self.assertTrue((newblk.gstclgrp == blk.gstclgrp).all())
        # ghost connectivity.
        self.assertTrue((newblk.gstfcnds == blk.gstfcnds).all())
        self.assertTrue((newblk.gstfccls == blk.gstfccls).all())
        self.assertTrue((newblk.gstclnds == blk.gstclnds).all())
        self.assertTrue((newblk.gstclfcs == blk.gstclfcs).all())
        # shared metrics.
        self.assertTrue((newblk.shndcrd == blk.shndcrd).all())
        self.assertTrue((newblk.shfccnd == blk.shfccnd).all())
        self.assertTrue((newblk.shfcnml == blk.shfcnml).all())
        self.assertTrue((newblk.shfcara == blk.shfcara).all())
        self.assertTrue((newblk.shclcnd == blk.shclcnd).all())
        self.assertTrue((newblk.shclvol == blk.shclvol).all())
        # shared type.
        self.assertTrue((newblk.shfctpn == blk.shfctpn).all())
        self.assertTrue((newblk.shcltpn == blk.shcltpn).all())
        self.assertTrue((newblk.shclgrp == blk.shclgrp).all())
        # shared connectivity.
        self.assertTrue((newblk.shfcnds == blk.shfcnds).all())
        self.assertTrue((newblk.shfccls == blk.shfccls).all())
        self.assertTrue((newblk.shclnds == blk.shclnds).all())
        self.assertTrue((newblk.shclfcs == blk.shclfcs).all())

class TestReloadTrivial(CheckDomainIO):
    def _check_reload(self, blk, compressor):
        from cStringIO import StringIO
        from ..block import BlockIO
        # save.
        bio = BlockIO(blk=blk, flag_compress=compressor)
        dataio = StringIO()
        bio.save(stream=dataio)
        value = dataio.getvalue()
        # load.
        bio = BlockIO()
        dataio = StringIO(value)
        newblk = bio.load(stream=dataio)
        # check
        self._check_shape(newblk, blk)
        self._check_group(newblk, blk)
        self._check_bc(newblk, blk)
        self._check_array(newblk, blk)
class TestLoadTrivial(CheckDomainIO):
    def _check_load(self, blk, stream):
        from ..block import BlockIO
        bio = BlockIO()
        # check version of stream.
        meta = bio.read_meta(stream=stream)
        self.assertEqual(meta.FORMAT_REV, '0.0.0.1')
        # load from steam.
        blkl = bio.load(stream=stream)
        # check.
        self._check_shape(blk, blkl)
        self._check_group(blk, blkl)
        self._check_bc(blk, blkl)
        self._check_array(blk, blkl)