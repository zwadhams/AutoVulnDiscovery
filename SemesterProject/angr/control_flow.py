import angr

proj = angr.Project("afl-fuzz", auto_load_libs=False)

cfg = proj.analyses.CFGFast()

with open("control_flow.txt", "w") as f:
    for func in cfg.kb.functions.values():
        f.write(f"Function: {func.name} at {hex(func.addr)}\n")
        for call_site in func.get_call_sites():
            # Defensive check: ensure the call site has a corresponding callee
            if call_site in cfg.kb.functions:
                callee_func = cfg.kb.functions[call_site]
                f.write(f"  calls -> {callee_func.name} at {hex(callee_func.addr)}\n")
            else:
                f.write(f"  calls -> UNKNOWN FUNCTION at {hex(call_site)}\n")
    print("Control flow saved to control_flow.txt")
