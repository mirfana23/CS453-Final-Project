import re
import subprocess

REGEX_COV_REPORT = "([Tt][Oo][Tt][Aa][Ll])\s+(\d+)\s+(\d+)\s+(\d+)%"
COMPILED_REGEX_COV_REPORT = re.compile(REGEX_COV_REPORT)

class ScriptRunner():
    FAIL = 1
    PASS = 0

    def __init__(self, target_name):
        self.target = target_name
        self.total_cov = 0.0
        self.erase_cov_cmd = ["coverage", "erase"]
        self.check_cov_cmd = ["coverage", "report"]

    def erase_cov(self):
        erase_res = subprocess.run(self.erase_cov_cmd, capture_output=True, text=True)

    def run(self, args=[]):
        run_target_cmd = ["coverage", "run", "-a", self.target]
        for inp_arg in args:
            run_target_cmd.append(inp_arg)
        run_res = subprocess.run(run_target_cmd, capture_output=True, text=True)
        if run_res.returncode != 0:
            return self.FAIL
        return self.PASS
        
    def check_cov(self):
        check_res = subprocess.run(self.check_cov_cmd, capture_output=True, text=True)
        parse_cov = COMPILED_REGEX_COV_REPORT.findall(check_res.stdout.strip().split("\n")[-1])
        if parse_cov:
            new_cov = float(parse_cov[0][3])
            if new_cov > self.total_cov:
                self.total_cov = new_cov
                return (True, self.total_cov)
        return (False, self.total_cov)

    def run_check(self, args=[]):
        ret_code = self.run(args)
        (ret_cov, total_cov) = self.check_cov()
        return (ret_code, ret_cov, total_cov)
        
