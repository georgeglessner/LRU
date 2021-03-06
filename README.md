An LRU simulation that runs in the terminal.  
Project for GVSU CIS 452.

# Overview
The main purpose of this assignment is to increase your understanding of paging, virtual memory, and memory management protocols.  A secondary objective is to enhance your appreciation of the complexity of operating system data structures and to discover some of the issues involved in kernel design decisions.  

# Program specifications
You are to develop a system that uses memory management and page replacement to implement virtual memory.  Structure your program to simulate the memory management mechanisms (hardware and software) as realistically as possible.  This means that your program should use appropriate data structures, such as PCBs, page tables and free frame lists.  

### Details of the simulated physical system:

* process logical address space is 64 KB  
* system physical memory is 16 KB  
* page / frame size is 1 KB

###  Details of the simulated virtual memory manager:

* global frame allocation  
* pure demand-paging  
* global LRU page replacement

### Format of the input file:

* your program should execute by reading an input file of logical memory references and performing the appropriate actions on simulated physical memory.  The input file consists of a stream of page references generated by active processes (think of it as a "trace tape" -- a recording of the logical memory addresses generated by the CPU during process execution).  Each referenced page should be brought into memory on demand, replacing other pages as necessary according to the Least-Recently-Used algorithm..

* all addresses in the input file are in binary.  Each logical memory reference occurs on a separate line.  The format of each memory reference is:  
  * ProcessID:  PageReference

A page reference consists of the 6 high-order bits of a logical address (make sure you understand why).  So, for example:

* the line `"P1:    000000"` indicates that process P1 needs to access a memory location on its logical page 0  
* the line `"P2:    000011"` indicates that process P2 needs to access a memory location on its logical page 3
