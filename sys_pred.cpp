#include <iostream>
#include <iomanip>
#include <fstream>
#include <assert.h>
#include <math.h>
#include <unistd.h>
#include <string>
#include "pin.H"

typedef unsigned int uint;

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool", "o", "sys_call.out", "specify file name for branch predictor output");
KNOB<UINT32> KnobB(KNOB_MODE_WRITEONCE, "pintool", "b", "1", "Buffer size");

// Invoked once per dynamic branch instruction
// pc: The address of the branch
/* taken: Non zero if a branch is taken
VOID DoBranch(ADDRINT pc, BOOL taken) {
 
}

// Called once per runtime image load
VOID Image(IMG img, VOID * v) {
  // find and instrument branches
  for (SEC sec = IMG_SecHead(img); SEC_Valid(sec); sec = SEC_Next(sec)) {
    for (RTN rtn = SEC_RtnHead(sec); RTN_Valid(rtn); rtn = RTN_Next(rtn)) {
      RTN_Open(rtn);
      for (INS ins = RTN_InsHead(rtn); INS_Valid(ins); ins = INS_Next(ins)) {
	if (INS_IsBranch(ins) && INS_HasFallThrough(ins)) {
	  INS_InsertCall( ins, IPOINT_BEFORE, (AFUNPTR)DoBranch, IARG_INST_PTR, IARG_BRANCH_TAKEN, IARG_END);
	}
      }
      RTN_Close(rtn);
    }
  }
}
*/

VOID Instruction(INS ins, VOID *v)
{
	//std::string instr = INS_Disassemble(ins) + "\n";
	//INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)ins_queue, IARG_PTR, instr, IARG_END);
	cout << INS_Disassemble(ins).c_str() << endl;
}

INT32 Usage() {
  cerr << "This pin tool simulates an (m,n,k) branch predictor." << endl;
  cerr << KNOB_BASE::StringKnobSummary();
  cerr << endl;
  return -1;
}

// Called once upon program exit
VOID Fini(int, VOID * v) {
}

// Called once prior to program execution
int main(int argc, CHAR *argv[]) {
    PIN_InitSymbols();

    if (PIN_Init(argc, argv)) {
        return Usage();
    }


    IMG_AddInstrumentFunction(Instruction, 0);
    PIN_AddFiniFunction(Fini, 0);

    PIN_StartProgram();

    return 0;
}

