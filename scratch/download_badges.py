import urllib.request
import os

urls = {
    "tier1_new": "https://yt3.googleusercontent.com/_dpDna9tL1QCQTbvYywctOA9Xvy5DZphdn7EIvHcLd9CtcIV43oD8cGPKi9jyWtUJTgpdTgH42U=s64-k-nd",
    "tier2_2_5m": "https://yt3.googleusercontent.com/SqlEzIx7yEmd85A621B7kdK4zlK2D7xMNeA20714gh5r019cEibVJNycM-AvqCRzC2fvwVKMwVo=s64-k-nd",
    "tier3_6_11m": "https://yt3.googleusercontent.com/Ttgy6rr2oUDq8vp47r-tUeNzgnQ8YT2hPSLDE_dkay6C-c5lU-RxLK29qAU1p6VpsMdzoVe9LQ=s64-k-nd",
    "tier4_12_23m": "https://yt3.googleusercontent.com/VuezLnJqdG6HLTIX3SihAvbkf-8OFPb__sY_8dxUapA-f7uR7ZIFs4p5MyOhu187eZUZBCwLyw=s64-k-nd",
    "tier5_24m": "https://yt3.googleusercontent.com/2GTPUHO1EM2l-D5Bfuzxc_UvWmfVXZtBylHf_bmd02CFSCGM6z_a_Bd3TFNHdtql6HPrIA3S=s64-k-nd"
}

os.makedirs("/Users/lap/Code/css/scratch/badges", exist_ok=True)

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(f"/Users/lap/Code/css/scratch/badges/{name}.png", "wb") as f:
                f.write(response.read())
        print(f"Downloaded {name}.png")
    except Exception as e:
        print(f"Error downloading {name}: {e}")
