import time
from bs4 import BeautifulSoup

def original_parse(content_bytes):
    # Reference parsing logic
    soup = BeautifulSoup(content_bytes, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text_out = '\n'.join(chunk for chunk in chunks if chunk)
    return text_out

def optimized_parse(content_bytes):
    # Our optimized parsing logic
    try:
        soup = BeautifulSoup(content_bytes, 'lxml')
    except Exception:
        soup = BeautifulSoup(content_bytes, 'html.parser')

    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()

    chunks = []
    for line in text.splitlines():
        line_stripped = line.strip()
        if not line_stripped:
            continue
        for phrase in line_stripped.split("  "):
            phrase_stripped = phrase.strip()
            if phrase_stripped:
                chunks.append(phrase_stripped)
    return "\n".join(chunks)

def run_tests_and_benchmark():
    html_sample = """
    <html>
    <head><title>Academic Analysis of Multi-agent Systems</title></head>
    <body>
        <h1>Section 1: Introduction</h1>
        <p>In this section, we discuss the context of multi-agent orchestration.
           Our framework leverages specialized sub-agents that communicate asynchronously.</p>

        <h2>Methodology and Simulation Details</h2>
        <p>We configure the environment with 5 distinct nodes.   Each node has a maximum queue depth of 50.
           The agents are deployed on a cluster using Docker containers.</p>

        <script>
            console.log("This script should be discarded from final parsed content");
            var x = 42;
        </script>

        <style>
            h1 { color: blue; }
            body { margin: 10px; }
        </style>

        <p>In conclusion, our results demonstrate a ~30% improvement in resource allocation times.</p>
    </body>
    </html>
    """ * 150 # Larger document to simulate real academic papers

    content_bytes = html_sample.encode('utf-8')

    # 1. Correctness Check
    print("--- CORRECTNESS TEST ---")
    orig_res = original_parse(content_bytes)
    opt_res = optimized_parse(content_bytes)

    if orig_res == opt_res:
         print("SUCCESS: The optimized parser produces the EXACT same output as the original parser!")
    else:
         print("FAILURE: Divergence in output!")
         # Print some mismatch
         orig_lines = orig_res.splitlines()
         opt_lines = opt_res.splitlines()
         print(f"Original lines count: {len(orig_lines)}, Optimized lines count: {len(opt_lines)}")
         for i in range(min(len(orig_lines), len(opt_lines))):
              if orig_lines[i] != opt_lines[i]:
                  print(f"Mismatch at line {i}:")
                  print(f"  Orig: {repr(orig_lines[i])}")
                  print(f"  Opt:  {repr(opt_lines[i])}")
                  break
         return

    # 2. Performance Benchmark
    print("\n--- BENCHMARK ---")
    iterations = 200
    print(f"Running each parser {iterations} times with a ~350KB HTML document...")

    # Benchmark Original
    start_orig = time.perf_counter()
    for _ in range(iterations):
        _ = original_parse(content_bytes)
    end_orig = time.perf_counter()
    orig_duration = end_orig - start_orig
    print(f"Original Parser Duration : {orig_duration:.4f} seconds")

    # Benchmark Optimized
    start_opt = time.perf_counter()
    for _ in range(iterations):
        _ = optimized_parse(content_bytes)
    end_opt = time.perf_counter()
    opt_duration = end_opt - start_opt
    print(f"Optimized Parser Duration: {opt_duration:.4f} seconds")

    # Speedup calculation
    if opt_duration < orig_duration:
        speedup = (orig_duration - opt_duration) / orig_duration * 100
        print(f"\n⚡ Bolt Speedup: {speedup:.2f}% faster!")
    else:
        print("\nNo speedup detected in this iteration.")

if __name__ == "__main__":
    run_tests_and_benchmark()
