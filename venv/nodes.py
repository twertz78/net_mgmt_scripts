datacenterdevices = [
    ['switch-b0695aw23nx6001-01.tele.iastate.edu', 'B06AW23'],
    ['switch-b0695az23nx6001-01.tele.iastate.edu', 'B06AZ23'],
    ['switch-b0695bg27nx56128.tele.iastate.edu', 'B06BG27'],
    ['switch-b0695bm27nx56128.tele.iastate.edu', 'B06BM27'],
    ['switch-b0695au36nx5596-01.tele.iastate.edu', 'B06AU365596'],
    ['switch-b0695ay36u26nx56128.tele.iastate.edu', 'B06AY3656128'],
    ['switch-b0695au36u26nx56128.tele.iastate.edu', 'B06AU3656128'],
    ['switch-b0695ax46nx56128-01.tele.iastate.edu', 'B06AX46'],
    ['switch-b0695at46nx56128-01.tele.iastate.edu', 'B06AT46'],
    ['switch-b0695bb46nx56128.tele.iastate.edu', 'B06BB46'],
    ['switch-b0695bf46nx56128.tele.iastate.edu', 'B06BF46'],
    ['switch-b0695az49nx56128-01.tele.iastate.edu', 'B06AZ49'],
    ['switch-b0695at49nx56128-01.tele.iastate.edu', 'B06AT49'],
    ['switch-b0695bb49nx56128.tele.iastate.edu', 'B06BB49'],
    ['switch-b0695bf49nx56128.tele.iastate.edu', 'B06BF49'],
    ['switch-m222175nx6001-01.tele.iastate.edu', 'M2201'],
    ['switch-m222175nx6001-02.tele.iastate.edu', 'M2202'],
    ['switch-m222175ag26nx56128.tele.iastate.edu', 'M22AG26'],
    ['switch-m222175ag28nx56128.tele.iastate.edu', 'M22AG28'],
    ['m22dc1.tele.iastate.edu', 'M22DC1'],
    ['b06dc1.tele.iastate.edu', 'B06DC1'],
]

# -------------------------------------------------------
# node room pairs

b31e63 = [
    ['b31nx1.tele.iastate.edu', 'b31nx1'],
    ['e63nx2.tele.iastate.edu', 'e63nx2'],
]
e63b31 = [
    ['b31nx2.tele.iastate.edu', 'b31nx2'],
    ['e63nx1.tele.iastate.edu', 'e63nx1'],
]
b11c12 = [
    ['b11nx1.tele.iastate.edu', 'b11nx1'],
    ['c12nx2.tele.iastate.edu', 'c12nx2'],
]
c12b11 = [
    ['b11nx2.tele.iastate.edu', 'b11nx2'],
    ['c12nx1.tele.iastate.edu', 'c12nx1'],
]
m22e01 = [
    ['m22nx1.tele.iastate.edu', 'm22nx1'],
    ['e01nx2.tele.iastate.edu', 'e01nx2'],
]
e01m22 = [
    ['m22nx2.tele.iastate.edu', 'm22nx2'],
    ['e01nx1.tele.iastate.edu', 'e01nx1'],
]
s07h13 = [
    ['h13nx1.tele.iastate.edu', 'h13nx1'],
    ['s07nx1.tele.iastate.edu', 's07nx1'],
]
b31nx3e63nx3 = [
    ['b31nx3.tele.iastate.edu', 'b31nx3'],
    ['e63nx3.tele.iastate.edu', 'e63nx3'],
]
b31nx5 = [
    ['b31nx5.tele.iastate.edu', 'b31nx5'],
]
be = [
    ['b31-be.tele.iastate.edu', 'b31be'],
    ['e63-be.tele.iastate.edu', 'e63be'],
]
core = [
    ['b31core.tele.iastate.edu', 'b31core'],
    ['e63core.tele.iastate.edu', 'e63core'],
]

# -------------------------------------------------------

admin_VDC = [
    ['b31nx0.tele.iastate.edu', 'b31nx0'],
    ['e63nx0.tele.iastate.edu', 'e63nx0'],
    ['b11nx0.tele.iastate.edu', 'b11nx0'],
    ['c12nx0.tele.iastate.edu', 'c12nx0'],
    ['m22nx0.tele.iastate.edu', 'm22nx0'],
    ['e01nx0.tele.iastate.edu', 'e01nx0'],
    ['b31core0.tele.iastate.edu', 'b31core0'],
    ['e63core0.tele.iastate.edu', 'e63core0'],
]

# -------------------------------------------------------

noderoomdevices = e63b31 + b31e63 + b11c12 + c12b11 + m22e01 + e01m22 + s07h13 + b31nx3e63nx3 + b31nx5 + be + core

alldevices = noderoomdevices + datacenterdevices
