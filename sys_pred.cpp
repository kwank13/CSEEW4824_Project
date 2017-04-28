#include <iostream>
#include <iomanip>
#include <fstream>
#include <assert.h>
#include <math.h>
#include <unistd.h>
#include <string>
#include <deque>
#include <vector>
#include "pin.H"

using namespace std;
typedef unsigned int uint;

deque<string> instr_queue; // Running queue of instructions
vector< vector<string> > calls; // Vector of sys calls and associated instrs
uint buf_size; // Queue size

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool", "o", "sys_call.out", "specify file name for branch predictor output");
KNOB<UINT32> KnobB(KNOB_MODE_WRITEONCE, "pintool", "b", "1", "Buffer size");


VOID Instruction(INS ins, VOID *v)
{

	// TODO: On system call, code should copy current queue into vector
	if (INS_IsSyscall(ins)) {
	}

	// If queue is filled, pop first element and insert new instruction
	if (instr_queue.size() == buf_size) {
		instr_queue.pop_front();
		instr_queue.push_back(INS_Disassemble(ins).c_str());
	} else
		instr_queue.push_back(INS_Disassemble(ins).c_str());

}

// TODO: Might need this to perform functions on sys call?
VOID SyscallEntry(THREADID tid, CONTEXT *ctx, SYSCALL_STANDARD std, void *v){
}

INT32 Usage() {
  cerr << "This pin tool captures system calls." << endl;
  cerr << KNOB_BASE::StringKnobSummary();
  cerr << endl;
  return -1;
}

// Called once upon program exit
VOID Fini(int code, VOID * v) {
//
	for (deque<string>::iterator it = instr_queue.begin(); it != instr_queue.end(); it++){
		cout << *it << endl;;
	}
//
}

// Called once prior to program execution
int main(int argc, CHAR *argv[]) {
    PIN_InitSymbols();

    if (PIN_Init(argc, argv)) {
        return Usage();
    }

	buf_size = (KnobB.Value()+1); //+1 to capture # instructions + syscall

    INS_AddInstrumentFunction(Instruction, 0);
	PIN_AddSyscallEntryFunction(SyscallEntry, 0);
    PIN_AddFiniFunction(Fini, 0);

    PIN_StartProgram();

    return 0;
}

