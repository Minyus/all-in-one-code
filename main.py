import pandas as pd

import hello_package


print(hello_package.hello_message)

print(open("conf/base/parameters.yml").read())

out_path = "submission.csv"
pred_df = pd.DataFrame(
    {
        "image_id": ["00000d2a601c", "00001f7fc849"],
        "InChI": ["InChI=1S/H2O/h1H2", "InChI=1S/H2O/h1H2"],
    }
)
pred_df.to_csv(out_path, index=False)
