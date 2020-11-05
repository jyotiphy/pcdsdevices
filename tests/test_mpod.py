import logging

import pytest
from ophyd.sim import make_fake_device
from pcdsdevices.device_types import MPODChannelHV, MPODChannelLV, MPOD

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def fake_mpod_lv_channel():
    FakeMPODChannel = make_fake_device(MPODChannelLV)
    mpod_lv_channel = FakeMPODChannel('TEST:MPOD:CHANNEL', name='test')
    # switch Off
    mpod_lv_channel.state.sim_put('Off')
    mpod_lv_channel.voltage.sim_put(20)
    mpod_lv_channel.current.sim_put(4)
    mpod_lv_channel.voltage_rise_rate.sim_put(100)
    mpod_lv_channel.voltage_fall_rate.sim_put(100)
    return mpod_lv_channel


@pytest.fixture(scope='function')
def fake_mpod_hv_channel():
    FakeMPODChannel = make_fake_device(MPODChannelHV)
    mpod_hv_channel = FakeMPODChannel('TEST:MPOD:CHANNEL:HV', 'TEST:MPOD:CARD',
                                      name='test')
    # switch Off
    mpod_hv_channel.state.sim_put('On')
    mpod_hv_channel.voltage.sim_put(20)
    mpod_hv_channel.voltage_rise_rate.sim_put(60)
    mpod_hv_channel.voltage_fall_rate.sim_put(60)
    return mpod_hv_channel


def test_switch_on_off(fake_mpod_lv_channel, fake_mpod_hv_channel):
    logger.debug('Testing MPOD Channel Switching')
    assert fake_mpod_lv_channel.state.get() == 'Off'
    fake_mpod_lv_channel.on()
    assert fake_mpod_lv_channel.state.get() == 'On'
    fake_mpod_lv_channel.off()
    assert fake_mpod_lv_channel.state.get() == 'Off'
    fake_mpod_lv_channel.reset()
    assert fake_mpod_lv_channel.state.get() == 'Reset'
    fake_mpod_hv_channel.emer_off()
    assert fake_mpod_hv_channel.state.get() == 'EmerOff'
    fake_mpod_hv_channel.clr_evnt()
    assert fake_mpod_hv_channel.state.get() == 'ClrEvnt'


def test_set_voltage(fake_mpod_lv_channel):
    logger.debug('Testing MPOD Channel Setting Voltage')
    assert fake_mpod_lv_channel.voltage.get() == 20
    fake_mpod_lv_channel.set_voltage(0)
    assert fake_mpod_lv_channel.voltage.get() == 0
    fake_mpod_lv_channel.set_voltage(23)
    assert fake_mpod_lv_channel.voltage.get() == 23


def test_set_current(fake_mpod_lv_channel):
    logger.debug('Testing MPOD Channel Setting Voltage')
    assert fake_mpod_lv_channel.current.get() == 4
    fake_mpod_lv_channel.set_current(0)
    assert fake_mpod_lv_channel.current.get() == 0
    fake_mpod_lv_channel.set_current(7)
    assert fake_mpod_lv_channel.current.get() == 7


def test_rise_fall_rate_hv(fake_mpod_lv_channel):
    logger.debug('Testing MPOD Channel Setting Voltage')
    assert fake_mpod_lv_channel.voltage_fall_rate.get() == 100
    assert fake_mpod_lv_channel.voltage_rise_rate.get() == 100
    fake_mpod_lv_channel.set_voltage_fall_rate(43)
    fake_mpod_lv_channel.set_voltage_rise_rate(43)
    assert fake_mpod_lv_channel.voltage_fall_rate.get() == 43
    assert fake_mpod_lv_channel.voltage_rise_rate.get() == 43


def test_rise_fall_rate_lv(fake_mpod_hv_channel):
    logger.debug('Testing MPOD Channel Setting Voltage')
    assert fake_mpod_hv_channel.voltage_fall_rate.get() == 60
    assert fake_mpod_hv_channel.voltage_rise_rate.get() == 60
    fake_mpod_hv_channel.set_voltage_fall_rate(23)
    fake_mpod_hv_channel.set_voltage_rise_rate(23)
    assert fake_mpod_hv_channel.voltage_fall_rate.get() == 23
    assert fake_mpod_hv_channel.voltage_rise_rate.get() == 23


def test_mpod_channel_factory():
    m = MPOD('TST:MY:MMS:CH:100', name='test_hv_mpod')
    assert isinstance(m, MPODChannelHV)
    m = MPOD('TST:RANDOM:MTR:CH:7', name='test_lv_mpod')
    assert isinstance(m, MPODChannelLV)
    m = MPOD('TST:RANDOM:MTR:NOTHING', name='test_unknown_ch')
    assert m is None


@pytest.mark.timeout(5)
def test_mpod_hv_channel_disconnected():
    MPODChannelHV('tst', 'card', name='tst')


@pytest.mark.timeout(5)
def test_mpod_lv_channel_disconnected():
    MPODChannelLV('tst', name='tst')
