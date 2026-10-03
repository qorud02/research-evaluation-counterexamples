"""Compare the NumPy image fixture with pinned PyTorch SSIM functions."""
import contextlib
import io
import json
import math
from pathlib import Path
import runpy
import numpy as np
import torch
import torch.nn.functional as F
from torch.autograd import Variable
from pinned_functions import load_functions

torch.set_num_threads(1)
load_functions("https://raw.githubusercontent.com/aailab-kaist/DBAE/533f5648a3a1ca419c402c656e305536267c14c8/eval_reconstruction.py", "7e6504144916f3db6d03a23336125ab7eb6b96bd60cba8228c32fa6eea64885b", ["gaussian", "create_window", "_ssim", "ssim"], globals())
# gaussian in the pinned source imports exp from math.
exp = math.exp
with contextlib.redirect_stdout(io.StringIO()):
    fixture = runpy.run_path(str(Path(__file__).parent / "DBAE_SSIM_axes_reproducer.py"))
x, y = fixture["x"], fixture["y"]
variants = [("NHWC", x, y), ("NCHW", x.transpose(0,3,1,2), y.transpose(0,3,1,2)), ("NHWC_HW_transposed", x.transpose(0,2,1,3), y.transpose(0,2,1,3)), ("NCHW_HW_transposed", x.transpose(0,3,2,1), y.transpose(0,3,2,1))]
checks = []
for layout, a, b in variants:
    original = float(ssim(torch.tensor(a, dtype=torch.float64), torch.tensor(b, dtype=torch.float64), size_average=False).mean().item())
    translated = float(fixture["ssim_axes"](a,b))
    checks.append({"layout":layout, "torch_float64":original, "numpy_float64":translated, "absolute_difference":abs(original-translated)})
assert all(row["absolute_difference"] <= 1e-6 for row in checks)
print(json.dumps({"torch":torch.__version__, "numpy":np.__version__, "tolerance":1e-6, "checks":checks}, indent=2))
