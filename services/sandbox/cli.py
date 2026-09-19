"""Interactive Terminal REPL for developer testing of the stateful sandbox engine."""

import argparse
import sys
from services.sandbox.client import LocalSandboxClient, RemoteSandboxClient, SandboxClient


def run_repl(client: SandboxClient) -> None:
    print("=" * 65)
    print("  data_speaker Stateful Sandbox Interactive REPL")
    print("  Commands: :state | :reset | :health | :exit")
    print("=" * 65)

    turn = 1
    multiline_buf = []

    while True:
        try:
            prompt = "... " if multiline_buf else f"In [{turn}]: "
            line = input(prompt)

            # Check for commands
            if not multiline_buf and line.strip().startswith(":"):
                cmd = line.strip().lower()
                if cmd in (":exit", ":quit"):
                    print("Exiting REPL.")
                    break
                elif cmd == ":reset":
                    client.reset()
                    print("[Sandbox reset: namespace cleared, baseline imports restored]")
                    turn = 1
                    continue
                elif cmd == ":state":
                    state = client.get_state()
                    print(f"DataFrames: {state.get('dataframes')}")
                    print(f"Variables:  {state.get('variables')}")
                    continue
                elif cmd == ":health":
                    print(client.health())
                    continue
                else:
                    print("Available commands: :state, :reset, :health, :exit")
                    continue

            # Handle multiline block input (empty line submits if buffered)
            if line.endswith("\\"):
                multiline_buf.append(line[:-1])
                continue
            elif multiline_buf:
                if line == "":
                    code = "\n".join(multiline_buf)
                    multiline_buf = []
                else:
                    multiline_buf.append(line)
                    continue
            else:
                code = line

            if not code.strip():
                continue

            result = client.execute(code)

            # Format and display results
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(f"[STDERR]\n{result.stderr}", file=sys.stderr)
            if result.figures:
                print(f"[FIGURES] Captured {len(result.figures)} Plotly chart(s).")
                for idx, fig in enumerate(result.figures, start=1):
                    title = fig.get("layout", {}).get("title", {}).get("text", "Untitled")
                    print(f"  Chart {idx}: title='{title}', traces={len(fig.get('data', []))}")

            status_flag = "✓" if result.status == "success" else "✗"
            mutation_note = f" (DataFrame mutated -> shape {result.df_shape})" if result.has_mutated_df else ""
            print(f"[{status_flag} {result.status.upper()} | {result.duration_ms}ms{mutation_note}]\n")

            if result.status == "success":
                turn += 1

        except (KeyboardInterrupt, EOFError):
            print("\nExiting REPL.")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="data_speaker Sandbox REPL")
    parser.add_argument(
        "--remote",
        type=str,
        default=None,
        help="Optional HTTP URL of remote container (e.g. http://localhost:8000). Defaults to local in-process.",
    )
    args = parser.parse_args()

    if args.remote:
        print(f"Connecting to remote sandbox at {args.remote}...")
        client: SandboxClient = RemoteSandboxClient(base_url=args.remote)
    else:
        print("Starting in-process local sandbox runner...")
        client = LocalSandboxClient()

    run_repl(client)


if __name__ == "__main__":
    main()
