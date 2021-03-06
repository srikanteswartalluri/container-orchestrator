from cli_utils import CLIUtils

out, err = CLIUtils.run("docker stop test-nginx")
print(out)