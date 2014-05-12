#!/usr/bin/python
#
# 1D Sod Tube Test
#
# Warning: The data generated by this program has not
#          been validated very well.
#

import numpy as np


it = 100 # iteration, which is integer
dt = 0.004
dx = 0.01
ga = 1.4

rhol = 1.0
ul = 0.0
pl = 1.0
rhor = 0.125
ur = 0.0
pr = 0.1

ia = 1

q = np.zeros(shape=(3,1000))
qn = np.zeros(shape=(3,1000))
qx = np.zeros(shape=(3,1000))
qt = np.zeros(shape=(3,1000))
qtdbg = np.zeros(shape=(3,1000)) # Debug for dev, remove me later
s = np.zeros(shape=(3,1000))
vxl = np.zeros(shape=(3))
vxr = np.zeros(shape=(3))
xx = np.zeros(shape=(1000))

hdt = dt/2.0
qdt = dt/4.0 #q:quad
hdx = dx/2.0
qdx = dx/4.0

tt = hdt*it
dtx = dt/dx

a1 = ga - 1.0
a2 = 3.0 - ga
a3 = a2/2.0
a4 = 1.5*a1
q[0][0] = rhol
q[1][0] = rhol*ul
q[2][0] = pl/a1 + 0.5*rhol*ul**2.0
itp = it + 1
for i in xrange(itp):
    q[0][i+1] = rhor
    q[1][i+1] = rhor*ur
    q[2][i+1] = pr/a1 + 0.5*rhor*ur**2.0
    # this was done by qx = np.zeros(shape=(3,1000))
    # for j in xrange(3):
    #     qx[j][i] = 0.0

m = 2
f = np.zeros(shape=(3,3))
for i in xrange(it):
    for j in xrange(m):
        w2 = q[1][j]/q[0][j]
        w3 = q[2][j]/q[0][j]
        f[0][1] = 1.0
        f[1][0] = -a3*w2**2
        f[1][1] = a2*w2
        f[1][2] = ga - 1.0
        f[2][0] = a1*w2**3 - ga*w2*w3
        f[2][1] = ga*w3 - a1*w2**2
        f[2][2] = ga*w2
        qt[0][j] = -qx[1,j]
        qt[1][j] = -(f[1][0]*qx[0][j] + f[1][1]*qx[1][j] + a1*qx[2][j])
        qt[2][j] = -(f[2][0]*qx[0][j] + f[2][1]*qx[1][j] + f[2][2]*qx[2][j])
        s[0][j] = qdx*qx[0][j] + dtx*(q[1][j] + qdt*qt[1][j])
        s[1][j] = qdx*qx[1][j] + dtx*(f[1][0]*(q[0][j] + qdt*qt[0][j]) +
                  f[1][1]*(q[1][j] + qdt*qt[1][j]) + a1*(q[2][j] + qdt*qt[2][j]))
        s[2][j] = qdx*qx[2][j] + dtx*(f[2][0]*(q[0][j] + qdt*qt[0][j]) +
                  f[2][1]*(q[1][j] + qdt*qt[1][j]) + f[2][2]*(q[2][j] + qdt*qt[2][j]))

        qtdbg = np.asarray(-(np.asmatrix(f)*np.asmatrix(qx))) # Dbg, remove me later

    mm = m - 1
    for j in xrange(mm):
        for k in xrange(3):
            qn[k][j+1] = 0.5*(q[k][j] + q[k][j+1] + s[k][j] - s[k][j+1])
            ############## MAY FIX ME BEGIN #####################
            vxl[k] = (qn[k][j+1] + hdt*qt[k][j+1] - qn[k][j+1])/hdx # TYPO???
            #vxl[k] = (qn[k][j+1] - q[k][j] - hdt*qt[k][j])/hdx # seems to be this, need validating
            ############## MAY FIX ME END #######################
            vxr[k] = (q[k][j+1] + hdt*qt[k][j+1] - qn[k][j+1])/hdx
            qx[k][j+1] = (vxl[k]*((abs(vxr[k]))**ia) + vxr[k]*((abs(vxl[k]))**ia))/(((abs(vxl[k]))**ia) + ((abs(vxr[k]))**ia) + 1.0E-60)

    for j in xrange(1,m):
        for k in xrange(3):
            q[k][j] = qn[k][j]

    m = m + 1

t2 = dx*float(itp)
xx[0] = -0.5*t2
for i in xrange(itp):
    xx[i+1] = xx[i] + dx

for i in xrange(m):
    x = q[1][i]/q[0][i]
    z = a1*(q[2][i] - 0.5*(x**2)*q[0][i])
    print('%f  %f  %f  %f' % (xx[i],q[0][i],x,z))

