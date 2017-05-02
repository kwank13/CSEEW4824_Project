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

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool", "o", "trace.out", "specify file name for branch predictor output");
// TODO: Test for all values of b
KNOB<UINT32> KnobB(KNOB_MODE_WRITEONCE, "pintool", "b", "5", "Buffer size");

// Prints system call # + arguments
VOID PrintSys(ADDRINT ip, ADDRINT num, ADDRINT arg0, ADDRINT arg1, ADDRINT arg2, ADDRINT arg3, ADDRINT arg4, ADDRINT arg5)
{
	printf("0x%lx: %ld (0x%lx, 0x%lx, 0x%lx, 0x%lx, 0x%lx, 0x%lx)\n",
			(unsigned long) ip,
			(long) num,
			(unsigned long) arg0,
			(unsigned long) arg1,
			(unsigned long) arg2,
			(unsigned long) arg3,
			(unsigned long) arg4,
			(unsigned long) arg5);
}

// Adds system call # + args and current instructions in queue to a vector
VOID GetSys(ADDRINT ip, ADDRINT num, ADDRINT arg0, ADDRINT arg1, ADDRINT arg2, ADDRINT arg3, ADDRINT arg4, ADDRINT arg5)
{
	char buf[200];
	vector<string> temp;
	// Formats system call to put into vector
	snprintf(buf, 200, "0x%lx: %ld (0x%lx, 0x%lx, 0x%lx, 0x%lx, 0x%lx, 0x%lx)",
			(unsigned long) ip,
			(long) num,
			(unsigned long) arg0,
			(unsigned long) arg1,
			(unsigned long) arg2,
			(unsigned long) arg3,
			(unsigned long) arg4,
			(unsigned long) arg5);

	// Adds instructions in queue to vector
	for (deque<string>::iterator it = instr_queue.begin(); it != instr_queue.end(); it++){
		temp.push_back(*it);
	}
	temp.push_back(buf);
	calls.push_back(temp); // Adds vector to vector of all sys calls
}

VOID Instruction(INS ins, VOID *v)
{
	// If not a system call, put instruction into queue
	// If queue is filled, pop first element and insert new instruction
	if (!INS_IsSyscall(ins)){
		if (instr_queue.size() == buf_size) {
			instr_queue.pop_front();
			instr_queue.push_back(INS_Disassemble(ins).c_str());
		} else

			instr_queue.push_back(INS_Disassemble(ins).c_str());
	}
}

// Functions called on system call
VOID SyscallEntry(THREADID tid, CONTEXT *ctxt, SYSCALL_STANDARD std, void *v){
/*
	PrintSys(PIN_GetContextReg(ctxt, REG_INST_PTR),
			PIN_GetSyscallNumber(ctxt, std),
			PIN_GetSyscallArgument(ctxt, std, 0),
			PIN_GetSyscallArgument(ctxt, std, 1),
			PIN_GetSyscallArgument(ctxt, std, 2),
			PIN_GetSyscallArgument(ctxt, std, 3),
			PIN_GetSyscallArgument(ctxt, std, 4),
			PIN_GetSyscallArgument(ctxt, std, 5));
*/
		GetSys(PIN_GetContextReg(ctxt, REG_INST_PTR),
			PIN_GetSyscallNumber(ctxt, std),
			PIN_GetSyscallArgument(ctxt, std, 0),
			PIN_GetSyscallArgument(ctxt, std, 1),
			PIN_GetSyscallArgument(ctxt, std, 2),
			PIN_GetSyscallArgument(ctxt, std, 3),
			PIN_GetSyscallArgument(ctxt, std, 4),
			PIN_GetSyscallArgument(ctxt, std, 5));
}

INT32 Usage() {
  cerr << "This pin tool captures system calls." << endl;
  cerr << KNOB_BASE::StringKnobSummary();
  cerr << endl;
  return -1;
}

// Called once upon program exit
VOID Fini(int code, VOID * v) {
	string filename;
	ofstream out;
	filename = KnobOutputFile.Value();
	out.open(filename.c_str());
/*
	// Prints queue
	for (deque<string>::iterator it = instr_queue.begin(); it != instr_queue.end(); it++){
		cout << *it << endl;
	}
*/
	// Prints calls vector
	for (vector< vector<string> >::iterator it = calls.begin(); it != calls.end(); it++){
		for (vector<string>::iterator it2 = it->begin(); it2 != it->end(); it2++){
			out << *it2 << "|";
		}
		out << endl;
	}
	out.close();

}

// Called once prior to program execution
int main(int argc, CHAR *argv[]) {
    PIN_InitSymbols();

    if (PIN_Init(argc, argv)) {
        return Usage();
    }

	buf_size = (KnobB.Value()); // Gets buffer size from user flag

    INS_AddInstrumentFunction(Instruction, 0);
	PIN_AddSyscallEntryFunction(SyscallEntry, 0);
    PIN_AddFiniFunction(Fini, 0);

    PIN_StartProgram();

    return 0;
}

