#!/bin/sh

./configure --prefix=$SCROOT \
	--disable-fortran \
	--disable-dap \
	--enable-shared \
> configure.log 2>&1
	#--with-hdf5=$HDF5_HOME \
	#--enable-netcdf4 \

make -j $NP > make.log 2>&1
