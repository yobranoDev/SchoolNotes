import pandas as pd
import numpy as np

def EBCT1(claim_data):
    # Generate a df with the claims
    claim_data = np.array(claim_data) if(type(claim_data)==list)else(claim_data)
    N, n = claim_data.shape
    df = pd.DataFrame(claim_data, columns= [ f"year-{i}" for i in range(1, n + 1)])
    df["risks"] = [i for i in range(1, N + 1)]
    df.set_index("risks", inplace= True)

    # dummy df for calculations
    stats_df = pd.DataFrame()
    stats_df["risks"] = df.index
    stats_df.set_index("risks", inplace= True)

    # mean and varince within each risk
    claims =df[ [f"year-{i}" for i in range(1, 6)]].copy()
    stats_df["risk-mean"] = claims.apply(np.mean, axis=1)
    stats_df["risk-var"] = claims.apply(np.var, axis= 1, ddof= 1)

    # average of the above mean and variance
    X_bar = stats_df["risk-mean"].mean()
    expected_var = stats_df["risk-var"].mean()


    var_means = stats_df["risk-mean"].var() - (1/n) * expected_var 

    # credibiliy factor
    cred_factor = n/(n+ (expected_var/ var_means))
    print(f"Credibility factor: {cred_factor:.4f}")
    print("Variance of risk claims\n",stats_df["risk-var"])
    df["credibility-premium"] = (cred_factor * stats_df["risk-mean"]) + ((1 - cred_factor) * X_bar)
    
    return df

    


if __name__ == "__main__":
    claims = [ [48, 53, 42, 50, 49], 
            [64, 71, 64, 73, 70],
            [85, 54, 76, 65, 90],
            [44, 52, 69, 55, 71],
            ]
    print(EBCT1(claims))