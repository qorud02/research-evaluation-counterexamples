"""Retrieve fixed source and execute a named set of top-level functions."""
import ast
import hashlib
import urllib.request

def load_functions(url, expected_sha256, names, namespace):
    request = urllib.request.Request(url, headers={"User-Agent": "Computational evaluation reproducibility supplement"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
    observed = hashlib.sha256(data).hexdigest()
    if observed != expected_sha256:
        raise RuntimeError("Pinned source SHA-256 mismatch: " + observed)
    parsed = ast.parse(data.decode("utf-8-sig"))
    selected = [node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name in names]
    found = {node.name for node in selected}
    if found != set(names):
        raise RuntimeError("Pinned source does not contain all requested functions")
    module = ast.Module(body=selected, type_ignores=[])
    exec(compile(module, url, "exec"), namespace)
    return namespace
