import sys
import os
import subprocess

# Built-in command handlers
def handle_exit(args):
    exit_code = 0
    if args:
        try:
            exit_code = int(args[0])
        except ValueError:
            print(f"exit: {args[0]}: numeric argument required", file=sys.stderr)
            exit_code = 255
    sys.exit(exit_code)

def handle_echo(args):
    print(' '.join(args))

def handle_type(args):
    if not args:
        print("type: missing argument")
        return

    cmd_to_check = args[0]
    if cmd_to_check in builtins:
        print(f"{cmd_to_check} is a shell builtin")
    else:
        executable = locate_executable(cmd_to_check)
        if executable:
            print(f"{cmd_to_check} is {executable}")  # Print the full path
        else:
            print(f"{cmd_to_check}: not found")

def handle_pwd(args):
    if args:
        print("pwd : too many arguments", file=sys.stderr)
    else:
        print(os.getcwd())

def handle_cd(args):
    if not args:
        # If no argument is provided, change to the home directory
        home_dir = os.path.expanduser("~")
        os.chdir(home_dir)
    else:
        target_dir = args[0]
        try:
            os.chdir(target_dir)
        except FileNotFoundError:
            print(f"cd: {target_dir}: No such file or directory", file=sys.stderr)
        except NotADirectoryError:
            print(f"cd: {target_dir}: Not a directory", file=sys.stderr)
            
            def handle_cd(args):
            if not args:
                home_dir = os.path.expanduser("~")
                os.chdir(home_dir)
            else:
                target_dir = args[0]
                if target_dir == "~":
                    target_dir = os.path.expanduser("~")
                    try:
                        os.chdir(target_dir)
                    except FileNotFoundError:
                        print(f"cd: {target_dir}: No such File or directory",file=sys.stderr)
                    except NotADirectoryError:
                        print(f"cd:{target_dir}: Not a directory", file=sys.stderr)

# Function to locate executables in PATH
def locate_executable(command):
    path_dirs = os.environ.get("PATH", "").split(":")
    for directory in path_dirs:
        executable_path = os.path.join(directory, command)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path
    return None

# Dictionary of built-in commands
builtins = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
    "cd": handle_cd,
}

# Main shell loop
def main():
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            user_input = input().strip()
        except EOFError:
            print()
            sys.exit(0)

        if not user_input:
            continue

        parts = user_input.split()
        command, args = parts[0], parts[1:]

        if command in builtins:
            builtins[command](args)
        else:
            executable = locate_executable(command)
            if executable:
                try:
                    # Pass only the executable name (without the full path) as the first argument
                    subprocess.run([command, *args], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running command {command}: {e}", file=sys.stderr)
                except Exception as e:
                    print(f"Error running command {command}: {e}", file=sys.stderr)
            else:
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()