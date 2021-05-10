import mock
import pytest

import acm

# TODO: the following patching is a hack, fix it.
# Importing PS_Functions requires connection to ADS,
# therefore needs to be patched. It cannot be patched directly,
# because mock.patch imports the module before patching it.
# So we patch sys.modules to make it work.
PS_Functions_mock = mock.MagicMock()
PS_TimeSeriesFunctions_mock = mock.MagicMock(GetExecutionPremiumRate=mock.Mock(return_value=1))
PS_BrokerFeesRates_mock = mock.MagicMock()
with mock.patch.dict(
        'sys.modules',
        PS_Functions=PS_Functions_mock,
        PS_TimeSeriesFunctions=PS_TimeSeriesFunctions_mock,
        PS_BrokerFeesRates=PS_BrokerFeesRates_mock):
    import PS_TradeFees
    from PS_TradeFees import (
        _CalculateFixedIncomeExecutionFee,
        get_execution_rate,
        MATRIX_FUNDS,
        FAIRTREE_FUNDS,
        SOUTHCHESTER_FUNDS,
        KADD_FUNDS,
        AAMAQUA_FUNDS,
    )


TIME_NOW = acm.Time().TimeNow()
MORE_THAN_FIVE_MONTHS = acm.Time().DateAddDelta(TIME_NOW, 0, 6, 0)
LESS_THAN_FIVE_MONTHS = acm.Time().DateAddDelta(TIME_NOW, 0, 4, 0)
MORE_THAN_FIVE_YEARS = acm.Time().DateAddDelta(TIME_NOW, 6, 0, 0)
LESS_THAN_FIVE_YEARS = acm.Time().DateAddDelta(TIME_NOW, 4, 0, 0)


def _patch_is_client_trade(mocker, funds_name):
    mocker.patch.object(
        PS_TradeFees, 'is_client_trade',
        side_effect=lambda tr, funds: funds == funds_name
    )


def _create_instrument_mock(ins_type, end_date):
    return mock.Mock(return_value=mock.Mock(
        InsType=mock.Mock(return_value=ins_type),
        EndDate=mock.Mock(return_value=end_date),
    ))


def _create_trade_mock(trade_time, ins_type, end_date):
    return mock.MagicMock(
        TradeTime=mock.Mock(return_value=trade_time),
        Instrument=_create_instrument_mock(ins_type, end_date),
    )


@pytest.mark.parametrize(('ins_type', 'end_date', 'expected'), [
    ('FRA', MORE_THAN_FIVE_MONTHS, 0.2),
    ('FRA', LESS_THAN_FIVE_MONTHS, 0.1),
    ('Swap', LESS_THAN_FIVE_YEARS, 0.20),
    ('Swap', MORE_THAN_FIVE_YEARS, 0.45),
    ('Bond', mock.ANY, 0.15),
    ('Cap', mock.ANY, 0.0),
    ('Floor', mock.ANY, 0.0),
    ('Option', mock.ANY, 0.0),
    ('ANYTHING_ELSE', mock.ANY, 1),
])
def test_matrix_execution_rate(mocker, ins_type, end_date, expected):
    trade = _create_trade_mock(TIME_NOW, ins_type, end_date)
    trade.Instrument.return_value.Underlying = _create_instrument_mock('FRA', mock.ANY)
    _patch_is_client_trade(mocker, MATRIX_FUNDS)

    execution_rate = get_execution_rate(trade)
    assert execution_rate == expected


@pytest.mark.parametrize(('ins_type', 'end_date', 'expected'), [
    ('FRA', mock.ANY, 0.25),
    ('Swap', LESS_THAN_FIVE_YEARS, 0.25),
    ('Swap', MORE_THAN_FIVE_YEARS, 1.50),
    ('Bond', mock.ANY, 0.15),
    ('Cap', mock.ANY, 0.0),
    ('Floor', mock.ANY, 0.0),
    ('Option', mock.ANY, 0.0),
    ('ANYTHING_ELSE', mock.ANY, 1),
])
def test_fairtree_execution_rate(mocker, ins_type, end_date, expected):
    trade = _create_trade_mock(TIME_NOW, ins_type, end_date)
    trade.Instrument.return_value.Underlying = _create_instrument_mock('FRA', mock.ANY)
    _patch_is_client_trade(mocker, FAIRTREE_FUNDS)

    execution_rate = get_execution_rate(trade)
    assert execution_rate == expected


@pytest.mark.parametrize(('ins_type', 'end_date', 'expected'), [
    ('Swap', LESS_THAN_FIVE_YEARS, 0.25),
    ('FRA', LESS_THAN_FIVE_YEARS, 1),
    ('Swap', MORE_THAN_FIVE_YEARS, 1.50),
    ('FRA', MORE_THAN_FIVE_YEARS, 1),
    ('ANYTHING_ELSE', mock.ANY, 1),
])
def test_southchester_execution_rate(mocker, ins_type, end_date, expected):
    trade = _create_trade_mock(TIME_NOW, ins_type, end_date)
    _patch_is_client_trade(mocker, SOUTHCHESTER_FUNDS)

    execution_rate = get_execution_rate(trade)
    assert execution_rate == expected


@pytest.mark.parametrize(('ins_type', 'end_date', 'expected'), [
    ('Swap', LESS_THAN_FIVE_YEARS, 0.25),
    ('FRA', LESS_THAN_FIVE_YEARS, 0.25),
    ('Swap', MORE_THAN_FIVE_YEARS, 0.45),
    ('FRA', MORE_THAN_FIVE_YEARS, 0.45),
    ('ANYTHING_ELSE', mock.ANY, 1),
])
def test_kadd_execution_rate(mocker, ins_type, end_date, expected):
    trade = _create_trade_mock(TIME_NOW, ins_type, end_date)
    _patch_is_client_trade(mocker, KADD_FUNDS)

    execution_rate = get_execution_rate(trade)
    assert execution_rate == expected


@pytest.mark.parametrize(('ins_type', 'end_date', 'expected'), [
    ('Swap', LESS_THAN_FIVE_YEARS, 0.25),
    ('FRA', LESS_THAN_FIVE_YEARS, 0.25),
    ('Swap', MORE_THAN_FIVE_YEARS, 0.55),
    ('FRA', MORE_THAN_FIVE_YEARS, 0.55),
    ('ANYTHING_ELSE', mock.ANY, 1),
])
def test_aamaqua_execution_rate(mocker, ins_type, end_date, expected):
    trade = _create_trade_mock(TIME_NOW, ins_type, end_date)
    _patch_is_client_trade(mocker, AAMAQUA_FUNDS)

    execution_rate = get_execution_rate(trade)
    assert execution_rate == expected


@pytest.mark.parametrize(('ins_type', 'end_date', 'expected'), [
    ('Swap', mock.ANY, 1),
])
def test_default_execution_rate(mocker, ins_type, end_date, expected):
    trade = _create_trade_mock(TIME_NOW, ins_type, end_date)
    _patch_is_client_trade(mocker, "ANY")

    execution_rate = get_execution_rate(trade)
    assert execution_rate == expected


def test_CalculateFixedIncomeExecutionFee(mocker):
    trade = _create_trade_mock(TIME_NOW, 'FRA', MORE_THAN_FIVE_YEARS)
    PS_Functions_mock.TradeYieldDelta.return_value = 1
    mocker.patch.object(PS_TradeFees, '_GetVATFactor', return_value=1)
    mocker.patch.object(PS_TradeFees, 'get_execution_rate', return_value=1)
    assert _CalculateFixedIncomeExecutionFee(trade) == -1
