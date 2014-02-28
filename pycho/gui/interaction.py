from PyQt5.QtCore import Qt as Q

QT_KEYS = {k[4:]: Q.__getattribute__(Q, k) for k in dir(Q) if k.startswith('Key_')}
