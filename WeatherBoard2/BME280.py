import time
import smbus

to_s16 = lambda x: (x + 2**15) % 2**16 - 2**15
to_u16 = lambda x: x % 2**16

BME280_I2C_ADDR = 0x76
BME280_CHIP_ID = 0x60

power_mode = {
        "BME280_SLEEP_MODE"         : 0x00,
        "BME280_FORCED_MODE"        : 0x01,
        "BME280_NORMAL_MODE"        : 0x03,
        "BME280_SOFT_RESET_CODE"    : 0xB6,
}

regs = {
        "BME280_CHIP_ID_REG"            : 0xD0,
        "BME280_RST_REG"                : 0xE0,
        "BME280_STAT_REG"               : 0xF3,
        "BME280_CTRL_MEAS_REG"          : 0xF4,
        "BME280_CTRL_HUMIDITY_REG"      : 0xF2,
        "BME280_CONFIG_REG"             : 0xF5,
        "BME280_PRESSURE_MSB_REG"       : 0xF7,
        "BME280_PRESSURE_LSB_REG"       : 0xF8,
        "BME280_PRESSURE_XLSB_REG"      : 0xF9,
        "BME280_TEMPERATURE_MSB_REG"    : 0xFA,
        "BME280_TEMPERATURE_LSB_REG"    : 0xFB,
        "BME280_TEMPERATURE_XLSB_REG"   : 0xFC,
        "BME280_HUMIDITY_MSB_REG"       : 0xFD,
        "BME280_HUMIDITY_LSB_REG"       : 0xFE,
}

cali_regs = {
        "BME280_TEMPERATURE_CALIB_DIG_T1_LSB_REG"   : 0x88,
        "BME280_TEMPERATURE_CALIB_DIG_T1_MSB_REG"   : 0x89,
        "BME280_TEMPERATURE_CALIB_DIG_T2_LSB_REG"   : 0x8A,
        "BME280_TEMPERATURE_CALIB_DIG_T2_MSB_REG"   : 0x8B,
        "BME280_TEMPERATURE_CALIB_DIG_T3_LSB_REG"   : 0x8C,
        "BME280_TEMPERATURE_CALIB_DIG_T3_MSB_REG"   : 0x8D,
        "BME280_PRESSURE_CALIB_DIG_P1_LSB_REG"      : 0x8E,
        "BME280_PRESSURE_CALIB_DIG_P1_MSB_REG"      : 0x8F,
        "BME280_PRESSURE_CALIB_DIG_P2_LSB_REG"      : 0x90,
        "BME280_PRESSURE_CALIB_DIG_P2_MSB_REG"      : 0x91,
        "BME280_PRESSURE_CALIB_DIG_P3_LSB_REG"      : 0x92,
        "BME280_PRESSURE_CALIB_DIG_P3_MSB_REG"      : 0x93,
        "BME280_PRESSURE_CALIB_DIG_P4_LSB_REG"      : 0x94,
        "BME280_PRESSURE_CALIB_DIG_P4_MSB_REG"      : 0x95,
        "BME280_PRESSURE_CALIB_DIG_P5_LSB_REG"      : 0x96,
        "BME280_PRESSURE_CALIB_DIG_P5_MSB_REG"      : 0x97,
        "BME280_PRESSURE_CALIB_DIG_P6_LSB_REG"      : 0x98,
        "BME280_PRESSURE_CALIB_DIG_P6_MSB_REG"      : 0x99,
        "BME280_PRESSURE_CALIB_DIG_P7_LSB_REG"      : 0x9A,
        "BME280_PRESSURE_CALIB_DIG_P7_MSB_REG"      : 0x9B,
        "BME280_PRESSURE_CALIB_DIG_P8_LSB_REG"      : 0x9C,
        "BME280_PRESSURE_CALIB_DIG_P8_MSB_REG"      : 0x9D,
        "BME280_PRESSURE_CALIB_DIG_P9_LSB_REG"      : 0x9E,
        "BME280_PRESSURE_CALIB_DIG_P9_MSB_REG"      : 0x9F,
        "BME280_HUMIDITY_CALIB_DIG_H1_REG"          : 0xA1,
        "BME280_HUMIDITY_CALIB_DIG_H2_LSB_REG"      : 0xE1,
        "BME280_HUMIDITY_CALIB_DIG_H2_MSB_REG"      : 0xE2,
        "BME280_HUMIDITY_CALIB_DIG_H3_REG"          : 0xE3,
        "BME280_HUMIDITY_CALIB_DIG_H4_MSB_REG"      : 0xE4,
        "BME280_HUMIDITY_CALIB_DIG_H4_LSB_REG"      : 0xE5,
        "BME280_HUMIDITY_CALIB_DIG_H5_MSB_REG"      : 0xE6,
        "BME280_HUMIDITY_CALIB_DIG_H6_REG"          : 0xE7,
}

class BME280:
    param = {}

    def __init__(self, i2c_dev, p_mode, h_samp, p_samp, t_samp):
        self.bus = smbus.SMBus(int(i2c_dev.split('-')[-1]))
        self.chip_id = self.read(regs['BME280_CHIP_ID_REG'], 1)[0]
        if self.chip_id != BME280_CHIP_ID:
            print "Wrong Device ID [", hex(self.chip_id), "]"
            exit()

        self.config_reg = 0
        self.ctrl_meas_reg = 0
        self.ctrl_hum_reg = 0
        self.oversamp_humidity = 0
        self.oversamp_pressure = 0

        self.get_cal_param()
        self.set_power_mode(p_mode)
        self.set_oversamp_humidity(h_samp)
        self.set_oversamp_pressure(p_samp)
        self.set_oversamp_temperature(t_samp)
        time.sleep(0.01)
        self.t_fine = 0.0

    def read(self, reg, cnt):
        val = [0 for x in xrange(cnt)]
        for i in xrange(cnt):
            val[i] = self.bus.read_byte_data(BME280_I2C_ADDR, reg + i)
	return val

    def write(self, reg, val):
        for i in xrange(len(val)):
            self.bus.write_byte_data(BME280_I2C_ADDR, reg + i, val[i])

    def get_cal_param(self):
        params = self.read(cali_regs['BME280_TEMPERATURE_CALIB_DIG_T1_LSB_REG'], 26)
        self.param['dig_T1'] = to_u16((params[1] << 8) | params[0])
        self.param['dig_T2'] = to_s16((params[3] << 8) | params[2])
        self.param['dig_T3'] = to_s16((params[5] << 8) | params[4])
        self.param['dig_P1'] = to_u16((params[7] << 8) | params[6])
        self.param['dig_P2'] = to_s16((params[9] << 8) | params[8])
        self.param['dig_P3'] = to_s16((params[11] << 8) | params[10])
        self.param['dig_P4'] = to_s16((params[13] << 8) | params[12])
        self.param['dig_P5'] = to_s16((params[15] << 8) | params[14])
        self.param['dig_P6'] = to_s16((params[17] << 8) | params[16])
        self.param['dig_P7'] = to_s16((params[19] << 8) | params[18])
        self.param['dig_P8'] = to_s16((params[21] << 8) | params[20])
        self.param['dig_P9'] = to_s16((params[23] << 8) | params[22])
        self.param['dig_H1'] = params[25]

        params = self.read(cali_regs['BME280_HUMIDITY_CALIB_DIG_H2_LSB_REG'], 7)
        self.param['dig_H2'] = to_s16((params[1] << 8) | params[0])
        self.param['dig_H3'] = params[2]
        self.param['dig_H4'] = to_s16((params[3] << 4) | (params[4] & 0x0f))
        self.param['dig_H5'] = to_s16((params[5] << 4) | (params[4] >> 4))
        self.param['dig_H6'] = params[6]

    def get_power_mode(self):
        return self.read(regs['BME280_CTRL_MEAS_REG'], 1)[0] & 0x03

    def set_power_mode(self, p_mode):
        if p_mode <= power_mode['BME280_NORMAL_MODE']:
            v_mode = (self.ctrl_meas_reg & ~0x03) | (p_mode & 0x03)

            if self.get_power_mode() != power_mode['BME280_SLEEP_MODE']:
                self.soft_rst()
                time.sleep(0.003)
                self.write(regs['BME280_CONFIG_REG'], [self.config_reg])
                self.write(regs['BME280_CTRL_HUMIDITY_REG'], [self.ctrl_hum_reg])
                self.write(regs['BME280_CTRL_MEAS_REG'], [v_mode])
            else:
                self.write(regs['BME280_CTRL_MEAS_REG'], [v_mode])

            self.ctrl_meas_reg = self.read(regs['BME280_CTRL_MEAS_REG'], 1)[0]
            self.ctrl_hum_reg = self.read(regs['BME280_CTRL_HUMIDITY_REG'], 1)[0]
            self.config_reg = self.read(regs['BME280_CONFIG_REG'], 1)[0]
        else:
            print "Wrong Power Mode [", hex(p_mode), "]"
            exit()

    def soft_rst(self):
        self.write(regs['BME280_RST_REG'], [power_mode['BME280_SOFT_RESET_CODE']])

    def set_oversamp_humidity(self, sampling):
        v_data = (self.ctrl_hum_reg & ~0x07) | (sampling & 0x07)

        if self.get_power_mode() != power_mode['BME280_SLEEP_MODE']:
            self.soft_rst()
            time.sleep(0.003)
            self.write(regs['BME280_CONFIG_REG'], [self.config_reg])
            self.write(regs['BME280_CTRL_HUMIDITY_REG'], [v_data])
            self.write(regs['BME280_CTRL_MEAS_REG'], [self.ctrl_meas_reg])
        else:
            self.write(regs['BME280_CTRL_HUMIDITY_REG'], [v_data])
            self.write(regs['BME280_CTRL_MEAS_REG'], [self.ctrl_hum_reg])

        self.oversamp_humidity = sampling
        self.ctrl_meas_reg = self.read(regs['BME280_CTRL_MEAS_REG'], 1)[0]
        self.ctrl_hum_reg = self.read(regs['BME280_CTRL_HUMIDITY_REG'], 1)[0]
        self.config_reg = self.read(regs['BME280_CONFIG_REG'], 1)[0]

    def set_oversamp_pressure(self, sampling):
        v_data = (self.ctrl_meas_reg & ~0x1c) | ((sampling << 2) & 0x1c)

        if self.get_power_mode != power_mode['BME280_SLEEP_MODE']:
            self.soft_rst()
            time.sleep(0.003)
            self.write(regs['BME280_CONFIG_REG'], [self.config_reg])
            self.write(regs['BME280_CTRL_HUMIDITY_REG'], [self.ctrl_hum_reg])
            self.write(regs['BME280_CTRL_MEAS_REG'], [v_data])
        else:
            self.write(regs['BME280_CTRL_MEAS_REG'], [v_data])

        self.oversamp_pressure = sampling
        self.ctrl_meas_reg = self.read(regs['BME280_CTRL_MEAS_REG'], 1)[0]
        self.ctrl_hum_reg = self.read(regs['BME280_CTRL_HUMIDITY_REG'], 1)[0]
        self.config_reg = self.read(regs['BME280_CONFIG_REG'], 1)[0]

    def set_oversamp_temperature(self, sampling):
        v_data = (self.ctrl_meas_reg & ~0xe0) | ((sampling << 5) & 0xe0)

        if self.get_power_mode != power_mode['BME280_SLEEP_MODE']:
            self.soft_rst()
            time.sleep(0.003)
            self.write(regs['BME280_CONFIG_REG'], [self.config_reg])
            self.write(regs['BME280_CTRL_HUMIDITY_REG'], [self.ctrl_hum_reg])
            self.write(regs['BME280_CTRL_MEAS_REG'], [v_data])
        else:
            self.write(regs['BME280_CTRL_MEAS_REG'], [v_data])

        self.oversamp_temperature = sampling
        self.ctrl_meas_reg = self.read(regs['BME280_CTRL_MEAS_REG'], 1)[0]
        self.ctrl_hum_reg = self.read(regs['BME280_CTRL_HUMIDITY_REG'], 1)[0]
        self.config_reg = self.read(regs['BME280_CONFIG_REG'], 1)[0]

    def read_humidity(self):
        vals = self.read(regs['BME280_PRESSURE_MSB_REG'], 8)
        raw_val = float((vals[6] << 8) | vals[7])
        """
        x1 = self.t_fine - 76800
        x1 = ((((raw_val << 14) - (self.param['dig_H4'] << 20) - (self.param['dig_H5'] * x1)) + 16384) >> 15) * \
            (((((((x1 * self.param['dig_H6']) >> 10) * (((x1 * self.param['dig_H3']) >> 11) + 32768)) >> 10) + 2097152) * \
            self.param['dig_H2'] + 8192) >> 14)
        x1 = x1 - (((((x1 >> 15) ** 2) >> 7) * self.param['dig_H1']) >> 4)
        if x1 < 0:
            x1 = 0
        if x1 > 419430400:
            x1 = 419430400

        return (x1 >> 12) / 1024.0
        """
        h = float(self.t_fine) - 76800.0
        h = (raw_val - (float(self.param['dig_H4']) * 64.0 + float(self.param['dig_H5']) / 16384.0 * h)) * (
        float(self.param['dig_H2']) / 65536.0 * (1.0 + float(self.param['dig_H6']) / 67108864.0 * h * (
        1.0 + float(self.param['dig_H3']) / 67108864.0 * h)))
        h = h * (1.0 - float(self.param['dig_H1']) * h / 524288.0)
        if h > 100:
            h = 100
        elif h < 0:
            h = 0
        return h

    def read_pressure(self):
        vals = self.read(regs['BME280_PRESSURE_MSB_REG'], 8)
        raw_val = float((vals[0] << 12) | (vals[1] << 4) | (vals[2] >> 4))
        """
        x1 = (self.t_fine >> 1) - 64000
        x2 = (((x1 >> 2) ** 2) >> 11) * self.param['dig_P6']
        x2 = x2 + ((x1 * self.param['dig_P5']) << 1)
        x2 = (x2 >> 2) + (self.param['dig_P4'] << 16)
        x1 = ((self.param['dig_P3'] * (((x1 >> 2) ** 2) >> 13)) >> 3 + \
             ((self.param['dig_P2'] * x1) >> 1)) >> 18
        x1 = ((32768 + x1) * self.param['dig_P1']) >> 15
        p = ((1048576 - raw_val) - (x2 >> 12)) * 3125
        if x1 == 0:
            return 0
        if p < 0x80000000:
            p = (p << 1) / x1
        else:
            p = (p / x1) * 2

        x1 = (self.param['dig_P9'] * (((p >> 3) ** 2) >> 13)) >> 12
        x2 = ((p >> 2) * self.param['dig_P8']) >> 13
        p = p + ((x1 + x2 + self.param['dig_P7']) >> 4)
        return p / 100.0
        """
        var1 = float(self.t_fine) / 2.0 - 64000.0
        var2 = var1 * var1 * float(self.param['dig_P6']) / 32768.0
        var2 = var2 + var1 * float(self.param['dig_P5']) * 2.0
        var2 = var2 / 4.0 + float(self.param['dig_P4']) * 65536.0
        var1 = (
             float(self.param['dig_P3']) * var1 * var1 / 524288.0 + float(self.param['dig_P2']) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * float(self.param['dig_P1'])
        if var1 == 0:
            return 0
        p = 1048576.0 - raw_val
        p = ((p - var2 / 4096.0) * 6250.0) / var1
        var1 = float(self.param['dig_P9']) * p * p / 2147483648.0
        var2 = p * float(self.param['dig_P8']) / 32768.0
        p = p + (var1 + var2 + float(self.param['dig_P7'])) / 16.0
        return p

    def read_temperature(self):
        vals = self.read(regs['BME280_PRESSURE_MSB_REG'], 8)
        raw_val = float((vals[3] << 12) | (vals[4] << 4) | (vals[5] >> 4))
        """
        x1 = (((raw_val >> 3) - (self.param['dig_T1'] << 1)) * self.param['dig_T2']) >> 11
        x2 = (((((raw_val >> 4) - self.param['dig_T1']) * ((raw_val >> 4) - self.param['dig_T1'])) >> 12) * self.param['dig_T3']) >> 14
        self.t_fine = x1 + x2
        temp = (self.t_fine * 5 + 128) >> 8

        return temp / 100.0
        """
        var1 = (raw_val / 16384.0 - float(self.param['dig_T1']) / 1024.0) * float(self.param['dig_T2'])
        var2 = ((raw_val / 131072.0 - float(self.param['dig_T1']) / 8192.0) * (
        raw_val / 131072.0 - float(self.param['dig_T1']) / 8192.0)) * float(self.param['dig_T3'])
        self.t_fine = int(var1 + var2)
        temp = (var1 + var2) / 5120.0
        return temp
