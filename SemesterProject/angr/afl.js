// Log the start of AFL++ Frida mode configuration
Afl.print(`[*] Starting FRIDA configuration for PID: ${Process.id}`);

// Create a Frida CModule with the persistent hook function to handle input injection
const cm = new CModule(`
  #include <string.h>
  #include <gum/gumdefs.h>

  #define BUF_LEN 256

  void afl_persistent_hook(GumCpuContext *regs, uint8_t *input_buf, uint32_t input_buf_len) {
    uint32_t length = (input_buf_len > BUF_LEN) ? BUF_LEN : input_buf_len;
    memcpy((void *)regs->rdi, input_buf, length);  // Inject input into the first argument register
    regs->rsi = length;  // Set length as the second argument register
}

  `,
  {
    memcpy: Module.getExportByName(null, "memcpy")
  }
);

// Get the address of the persistent fuzzing function `fuzz_one_input`
const pStartAddr = DebugSymbol.fromName("fuzz_one_input").address;
console.log("Persistent function address:", pStartAddr);


// Set up AFL++ persistent mode configurations
Afl.setPersistentHook(cm.afl_persistent_hook);   // Set the persistent hook
Afl.setPersistentAddress(pStartAddr);            // Set the persistent function address
Afl.setEntryPoint(pStartAddr);                   // Use the same function as the entry point
Afl.setInMemoryFuzzing();                        // Enable in-memory fuzzing
Afl.setInstrumentLibraries();                    // Instrument any libraries

Afl.done();
Afl.print("[*] FRIDA configuration complete!");
