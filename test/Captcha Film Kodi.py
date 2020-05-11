class cInputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):

        self.cptloc = kwargs.get('captcha')
        # self.img = xbmcgui.ControlImage(250, 110, 780, 499, '')
        # xbmc.sleep(500)
        i = 0
        u = 100
        pos = []

        self.img = [0]*5
        for img in self.cptloc:
            self.img[i] = xbmcgui.ControlImage(u, 400, 200, 200, img)
            i = i + 1
            pos.append(u)
            u = u + 200

        i = 0
        bg_image = os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + 'background.png'
        check_image = os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + 'trans_checked.png'

        self.ctrlBackground = xbmcgui.ControlImage(0, 0, 1280, 720, bg_image)
        self.cancelled = False
        self.addControl (self.ctrlBackground)

        self.strActionInfo = xbmcgui.ControlLabel(250, 20, 724, 400, 'Veuillez sélectionnez les images correspondants au thème.\nIl devrait y en avoir 3 ou 4 à sélectionner.', 'font40', '0xFFFF00FF')
        self.addControl(self.strActionInfo)

        self.msg = kwargs.get('msg')
        self.roundnum = kwargs.get('roundnum')
        self.strActionInfo = xbmcgui.ControlLabel(250, 70, 700, 300, 'Le thème est: ' + self.msg, 'font13', '0xFFFF00FF')
        self.addControl(self.strActionInfo)

        self.addControl(self.img[0])
        self.addControl(self.img[1])
        self.addControl(self.img[2])
        self.addControl(self.img[3])
        self.addControl(self.img[4])

        self.chk = [0]*9
        self.chkbutton = [0]*9
        self.chkstate = [False]*9

        if 1 == 2:
            self.chk[0] = xbmcgui.ControlCheckMark(pos[0], 400, 200, 200, '1', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[1] = xbmcgui.ControlCheckMark(pos[1], 400, 200, 200, '1', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[2] = xbmcgui.ControlCheckMark(pos[2], 400, 200, 200, '1', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[3] = xbmcgui.ControlCheckMark(pos[3], 400, 200, 200, '1', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[4] = xbmcgui.ControlCheckMark(pos[4], 400, 200, 200, '1', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)

            self.chk[5] = xbmcgui.ControlCheckMark(250 + 520, 110 + 166, 260, 166, '6', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[6] = xbmcgui.ControlCheckMark(250, 110 + 332, 260, 166, '7', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[7] = xbmcgui.ControlCheckMark(250 + 260, 110 + 332, 260, 166, '8', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[8] = xbmcgui.ControlCheckMark(250 + 520, 110 + 332, 260, 166, '9', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)

        else:
            self.chk[0] = xbmcgui.ControlImage(pos[0], 400, 200, 200, check_image)
            self.chk[1] = xbmcgui.ControlImage(pos[1], 400, 200, 200, check_image)
            self.chk[2] = xbmcgui.ControlImage(pos[2], 400, 200, 200, check_image)
            self.chk[3] = xbmcgui.ControlImage(pos[3], 400, 200, 200, check_image)
            self.chk[4] = xbmcgui.ControlImage(pos[4], 400, 200, 200, check_image)

            self.chk[5] = xbmcgui.ControlImage(250 + 520, 110 + 166, 260, 166, check_image)
            self.chk[6] = xbmcgui.ControlImage(250, 110 + 332, 260, 166, check_image)
            self.chk[7] = xbmcgui.ControlImage(250 + 260, 110 + 332, 260, 166, check_image)
            self.chk[8] = xbmcgui.ControlImage(250 + 520, 110 + 332, 260, 166, check_image)

            self.chkbutton[0] = xbmcgui.ControlButton(pos[0], 400, 200, 200, '1', font = 'font1')
            self.chkbutton[1] = xbmcgui.ControlButton(pos[1], 400, 200, 200, '1', font = 'font1')
            self.chkbutton[2] = xbmcgui.ControlButton(pos[2], 400, 200, 200, '1', font = 'font1')
            self.chkbutton[3] = xbmcgui.ControlButton(pos[3], 400, 200, 200, '1', font = 'font1')
            self.chkbutton[4] = xbmcgui.ControlButton(pos[4], 400, 200, 200, '1', font = 'font1')

            self.chkbutton[5] = xbmcgui.ControlButton(250 + 520, 110 + 166, 260, 166, '6', font = 'font1')
            self.chkbutton[6] = xbmcgui.ControlButton(250, 110 + 332, 260, 166, '7', font = 'font1')
            self.chkbutton[7] = xbmcgui.ControlButton(250 + 260, 110 + 332, 260, 166, '8', font = 'font1')
            self.chkbutton[8] = xbmcgui.ControlButton(250 + 520, 110 + 332, 260, 166, '9', font = 'font1')

        for obj in self.chk:
            self.addControl(obj)
            obj.setVisible(False)
        for obj in self.chkbutton:
            self.addControl(obj)

        self.cancelbutton = xbmcgui.ControlButton(250 + 260 - 70, 620, 140, 50, 'Cancel', alignment = 2)
        self.okbutton = xbmcgui.ControlButton(250 + 520 - 50, 620, 100, 50, 'OK', alignment = 2)
        self.addControl(self.okbutton)
        self.addControl(self.cancelbutton)

        self.chkbutton[6].controlDown(self.cancelbutton);  self.chkbutton[6].controlUp(self.chkbutton[3])
        self.chkbutton[7].controlDown(self.cancelbutton);  self.chkbutton[7].controlUp(self.chkbutton[4])
        self.chkbutton[8].controlDown(self.okbutton);      self.chkbutton[8].controlUp(self.chkbutton[5])

        self.chkbutton[6].controlLeft(self.chkbutton[8]);  self.chkbutton[6].controlRight(self.chkbutton[7]);
        self.chkbutton[7].controlLeft(self.chkbutton[6]);  self.chkbutton[7].controlRight(self.chkbutton[8]);
        self.chkbutton[8].controlLeft(self.chkbutton[7]);  self.chkbutton[8].controlRight(self.chkbutton[6]);

        self.chkbutton[3].controlDown(self.chkbutton[6]);  self.chkbutton[3].controlUp(self.chkbutton[0])
        self.chkbutton[4].controlDown(self.chkbutton[7]);  self.chkbutton[4].controlUp(self.chkbutton[1])
        self.chkbutton[5].controlDown(self.chkbutton[8]);  self.chkbutton[5].controlUp(self.chkbutton[2])

        self.chkbutton[3].controlLeft(self.chkbutton[5]);  self.chkbutton[3].controlRight(self.chkbutton[4]);
        self.chkbutton[4].controlLeft(self.chkbutton[3]);  self.chkbutton[4].controlRight(self.chkbutton[5]);
        self.chkbutton[5].controlLeft(self.chkbutton[4]);  self.chkbutton[5].controlRight(self.chkbutton[3]);

        self.chkbutton[0].controlDown(self.chkbutton[3]);  self.chkbutton[0].controlUp(self.cancelbutton)
        self.chkbutton[1].controlDown(self.chkbutton[4]);  self.chkbutton[1].controlUp(self.cancelbutton)
        self.chkbutton[2].controlDown(self.chkbutton[5]);  self.chkbutton[2].controlUp(self.okbutton)

        self.chkbutton[0].controlLeft(self.chkbutton[2]);  self.chkbutton[0].controlRight(self.chkbutton[1]);
        self.chkbutton[1].controlLeft(self.chkbutton[0]);  self.chkbutton[1].controlRight(self.chkbutton[2]);
        self.chkbutton[2].controlLeft(self.chkbutton[1]);  self.chkbutton[2].controlRight(self.chkbutton[0]);

        self.cancelled = False
        self.setFocus(self.okbutton)
        self.okbutton.controlLeft(self.cancelbutton);      self.okbutton.controlRight(self.cancelbutton);
        self.cancelbutton.controlLeft(self.okbutton);      self.cancelbutton.controlRight(self.okbutton);
        self.okbutton.controlDown(self.chkbutton[2]);      self.okbutton.controlUp(self.chkbutton[8]);
        self.cancelbutton.controlDown(self.chkbutton[0]);  self.cancelbutton.controlUp(self.chkbutton[6]);

    def get(self):
        self.doModal()
        self.close()
        if not self.cancelled:
            retval = ""
            for objn in range(9):
                if self.chkstate[objn]:
                    retval += ("" if retval == "" else ",") + str(objn)
            return retval

        else:
            return ""

    def anythingChecked(self):
        for obj in self.chkstate:
            if obj:
                return True
        return False

    def onControl(self, control):
        if control == self.okbutton:
            if self.anythingChecked():
                self.close()
        elif control == self.cancelbutton:
            self.cancelled = True
            self.close()
        try:
            if 'xbmcgui.ControlButton' in repr(type(control)):
                index = control.getLabel()
                if index.isnumeric():
                    self.chkstate[int(index)-1] = not self.chkstate[int(index)-1]
                    self.chk[int(index)-1].setVisible(self.chkstate[int(index)-1])

        except:
            pass

    def onAction(self, action):
        if action == 10:
            self.cancelled = True
            self.close()
