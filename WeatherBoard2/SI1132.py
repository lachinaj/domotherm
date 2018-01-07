import smbus
import time

SI1132_I2C_ADDR = 0x60
SI1132_PARTID = 0x32

cmds = {
        'Si1132_PARAM_QUERY'    : 0x80,
        'Si1132_PARAM_SET'      : 0xA0,
        'Si1132_NOP'            : 0x00,
        'Si1132_RESET'          : 0x01,
        'Si1132_BUSADDR'        : 0x02,
        'Si1132_GET_CAL'        : 0x12,
        'Si1132_ALS_FORCE'      : 0x06,
        'Si1132_ALS_PAUSE'      : 0x0A,
        'Si1132_ALS_AUTO'       : 0x0E,
}

params = {
        'Si1132_PARAM_I2CADDR'              : 0x00,
        'Si1132_PARAM_CHLIST'               : 0x01,
        'Si1132_PARAM_CHLIST_ENUV'          : 0x80,
        'Si1132_PARAM_CHLIST_ENAUX'         : 0x40,
        'Si1132_PARAM_CHLIST_ENALSIR'       : 0x20,
        'Si1132_PARAM_CHLIST_ENALSVIS'      : 0x10,
        'Si1132_PARAM_ALSENCODING'          : 0x06,
        'Si1132_PARAM_ALSIRADCMUX'          : 0x0E,
        'Si1132_PARAM_AUXADCMUX'            : 0x0F,
        'Si1132_PARAM_ALSVISADCCOUNTER'     : 0x10,
        'Si1132_PARAM_ALSENCODING'          : 0x06,
        'Si1132_PARAM_ALSIRADCMUX'          : 0x0E,
        'Si1132_PARAM_AUXADCMUX'            : 0x0F,
        'Si1132_PARAM_ALSVISADCCOUNTER'     : 0x10,
        'Si1132_PARAM_ALSVISADCGAIN'        : 0x11,
        'Si1132_PARAM_ALSVISADCMISC'        : 0x12,
        'Si1132_PARAM_ALSVISADCMISC_VISRANGE' : 0x20,
        'Si1132_PARAM_ALSIRADCCOUNTER'      : 0x1D,
        'Si1132_PARAM_ALSIRADCGAIN'         : 0x1E,
        'Si1132_PARAM_ALSIRADCMISC'         : 0x1F,
        'Si1132_PARAM_ALSIRADCMISC_RANGE'   : 0x20,
        'Si1132_PARAM_ADCCOUNTER_511CLK'    : 0x70,
        'Si1132_PARAM_ADCMUX_SMALLIR'       : 0x00,
        'Si1132_PARAM_ADCMUX_LARGEIR'       : 0x03,
}

regs = {
        'Si1132_REG_PARTID'         : 0x00,
        'Si1132_REG_REVID'          : 0x01,
        'Si1132_REG_SEQID'          : 0x02,
        'Si1132_REG_INTCFG'         : 0x03,
        'Si1132_REG_INTCFG_INTOE'   : 0x01,
        'Si1132_REG_IRQEN'          : 0x04,
        'Si1132_REG_IRQEN_ALSEVERYSAMPLE' : 0x01,
        'Si1132_REG_IRQMODE1'       : 0x05,
        'Si1132_REG_IRQMODE2'       : 0x06,
        'Si1132_REG_HWKEY'          : 0x07,
        'Si1132_REG_MEASRATE0'      : 0x08,
        'Si1132_REG_MEASRATE1'      : 0x09,
        'Si1132_REG_UCOEF0'         : 0x13,
        'Si1132_REG_UCOEF1'         : 0x14,
        'Si1132_REG_UCOEF2'         : 0x15,
        'Si1132_REG_UCOEF3'         : 0x16,
        'Si1132_REG_PARAMWR'        : 0x17,
        'Si1132_REG_COMMAND'        : 0x18,
        'Si1132_REG_RESPONSE'       : 0x20,
        'Si1132_REG_IRQSTAT'        : 0x21,
        'Si1132_REG_ALSVISDATA0'    : 0x22,
        'Si1132_REG_ALSVISDATA1'    : 0x23,
        'Si1132_REG_ALSIRDATA0'     : 0x24,
        'Si1132_REG_ALSIRDATA1'     : 0x25,
        'Si1132_REG_UVINDEX0'       : 0x2C,
        'Si1132_REG_UVINDEX1'       : 0x2D,
        'Si1132_REG_PARAMRD'        : 0x2E,
        'Si1132_REG_CHIPSTAT'       : 0x30,
}

class SI1132:
    def __init__(self, i2c_dev):
        self.bus = smbus.SMBus(int(i2c_dev.split('-')[-1]))
	self.id = self.read_reg8(0x00)
        if self.id != SI1132_PARTID:
            print "Wrong Device ID [", hex(self.id), "]"
            exit()

        self.reset()

        self.write_reg8(regs['Si1132_REG_UCOEF0'], 0x7B)
        self.write_reg8(regs['Si1132_REG_UCOEF1'], 0x6B)
        self.write_reg8(regs['Si1132_REG_UCOEF2'], 0x01)
        self.write_reg8(regs['Si1132_REG_UCOEF3'], 0x00)

        param = params['Si1132_PARAM_CHLIST_ENUV'] | params['Si1132_PARAM_CHLIST_ENALSIR'] | params['Si1132_PARAM_CHLIST_ENALSVIS']
        self.writeParam(params['Si1132_PARAM_CHLIST'], param)

        self.write_reg8(regs['Si1132_REG_INTCFG'], regs['Si1132_REG_INTCFG_INTOE'])
        self.write_reg8(regs['Si1132_REG_IRQEN'], regs['Si1132_REG_IRQEN_ALSEVERYSAMPLE'])

        self.writeParam(params['Si1132_PARAM_ALSIRADCMUX'], params['Si1132_PARAM_ADCMUX_SMALLIR'])
        time.sleep(0.01)
        self.writeParam(params['Si1132_PARAM_ALSIRADCGAIN'], 0)
        time.sleep(0.01)
        self.writeParam(params['Si1132_PARAM_ALSIRADCCOUNTER'], params['Si1132_PARAM_ADCCOUNTER_511CLK'])
        self.writeParam(params['Si1132_PARAM_ALSIRADCMISC'], params['Si1132_PARAM_ALSIRADCMISC_RANGE'])
        time.sleep(0.01)
        self.writeParam(params['Si1132_PARAM_ALSIRADCGAIN'], 0)
        time.sleep(0.01)
        self.writeParam(params['Si1132_PARAM_ALSIRADCCOUNTER'], params['Si1132_PARAM_ADCCOUNTER_511CLK'])
        self.writeParam(params['Si1132_PARAM_ALSVISADCMISC'], params['Si1132_PARAM_ALSVISADCMISC_VISRANGE'])
        time.sleep(0.01)
        self.write_reg8(regs['Si1132_REG_MEASRATE0'], 0xFF)
        self.write_reg8(regs['Si1132_REG_COMMAND'], cmds['Si1132_ALS_AUTO'])

    def reset(self):
        self.write_reg8(regs['Si1132_REG_MEASRATE0'], 0)
        self.write_reg8(regs['Si1132_REG_MEASRATE1'], 0)
        self.write_reg8(regs['Si1132_REG_IRQEN'], 0)
        self.write_reg8(regs['Si1132_REG_IRQMODE1'], 0)
        self.write_reg8(regs['Si1132_REG_IRQMODE2'], 0)
        self.write_reg8(regs['Si1132_REG_INTCFG'], 0)
        self.write_reg8(regs['Si1132_REG_IRQSTAT'], 0xFF)
        self.write_reg8(regs['Si1132_REG_COMMAND'], cmds['Si1132_RESET'])
        time.sleep(0.01)
        self.write_reg8(regs['Si1132_REG_HWKEY'], 0x17)
        time.sleep(0.01)

    def read_reg8(self, reg):
	return self.bus.read_byte_data(SI1132_I2C_ADDR, reg)

    def read_reg16(self, reg):
	return self.bus.read_word_data(SI1132_I2C_ADDR, reg)

    def write_reg8(self, reg, val):
	self.bus.write_byte_data(SI1132_I2C_ADDR, reg, val)

    def write_reg16(self, reg, val):
	self.bus.write_word_data(SI1132_I2C_ADDR, reg, val)

    def writeParam(self, param, val):
        self.write_reg8(regs['Si1132_REG_PARAMWR'], val)
        self.write_reg8(regs['Si1132_REG_COMMAND'], param | cmds['Si1132_PARAM_SET'])

    def readVisible(self):
        time.sleep(0.01)
        return ((self.read_reg16(0x22) - 256) / 0.282) * 14.5

    def readIR(self):
        time.sleep(0.01)
        return ((self.read_reg16(0x24) - 250) / 2.44) * 14.5

    def readUV(self):
        time.sleep(0.01)
        return self.read_reg16(0x2c)
