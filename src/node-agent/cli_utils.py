import subprocess


class CLIUtils:
    @staticmethod
    def run(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding='UTF-8')
        (out, err) = proc.communicate()
        return out, err
    @staticmethod
    def run_nb(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding='UTF-8')
