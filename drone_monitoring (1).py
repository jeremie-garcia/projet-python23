from NatNetClient import NatNetClient
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, pyqtSlot
from PyQt5.QtWidgets import QApplication


class ClientVoliere(QObject):
    # signal for voliere data (AC_ID, pos_x, pos_y,pos_z, quat_a, quat_b, quat_c, quat_d)
    drone_data = pyqtSignal(int, float, float, float, float, float, float, float)

    def __init__(self):
        super().__init__()

        # create NatNetClient to retrieve data from Motion Tracking
        self.natnet = NatNetClient(rigidBodyListListener=self.receive_rigid_body_list)
        # start the server
        self.natnet.run()

    def stop(self):
        self.natnet.stop()

    def receive_rigid_body_list(self, rigidBodyList, stamp):
        for (ac_id, pos, quat, valid) in rigidBodyList:
            if valid:
                self.drone_data.emit(ac_id, pos[0], pos[1], pos[2], quat[0], quat[1], quat[2], quat[3])


if __name__ == "__main__":
    import sys
    app = QApplication([])
    voliere = ClientVoliere()
    voliere.drone_data.connect(print)
    app.aboutToQuit.connect(voliere.stop)
    sys.exit(app.exec_())