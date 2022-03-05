import pandas as pd
from run import get_data,  get_exchange_rate

def test_get_exchange_rate():
    unpickled_df = pd.read_pickle("df_get_exchange_rate.pkl")
    result_df = get_exchange_rate("GBP", "EUR")
    pd.testing.assert_frame_equal(result_df, unpickled_df)

def test_get_data():
    identifier = "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"
    target_currency = "GBP"
    result_df = get_data(identifier, target_currency)
    unpickled_df = pd.read_pickle("df_get_data.pkl")
    pd.testing.assert_frame_equal(result_df, unpickled_df)

def test_get_data_without_conversion():
    identifier = "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"
    result_df = get_data(identifier)
    unpickled_df = pd.read_pickle("get_data_without_conversion.pkl")
    pd.testing.assert_frame_equal(result_df, unpickled_df)


