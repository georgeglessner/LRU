#!/usr/bin/env python

""" A simple LRU simulation """

import time, random, keyboard, itertools
from Tkinter import *

input = ""
frameList = []
processPageList = []
pageTable = []
displayTable = []
pfList = []
freeFrames = range(0,16)


def start():
    global input, frameList, processPageList

    print "\n******************************************************************"
    print "\tThis is a simulation for LRU replacement."
    print "\tAt any time you may choose to quit('q') this program."
    print "******************************************************************"
    #Open File
    with open ("input.txt") as f:
        original = f.readlines()

        #Remove ":", "\n"
        for line in original:
            input = line.replace(":", "")
            input = input.replace('\n', "")

            # Split by tab, add to processList
            output = input.partition('\t')

            #convert process to number
            pid = output[0]
            proc = int(pid[1])

            #conver binary page # to decimal
            page = int(str(output[2]),2)

            #add process and page # to list
            processPageList.append([proc, page])

def run():
    global frameList, pageTable, processPageList, freeFrames
    inFrame = 0
    ts = 0
    run = 0

    #run through each process in list
    for process in processPageList:

        #intial flag for reloop
        restart = True

        #timestamp increment
        ts += 1

        #variable to denote whether in frame list or not
        inFrame = 0

        #variable to assign random frame
        randomFrame = random.randint(0,15)

        #if list is empty (base case)
        if not frameList:
            pageFault(process[0])
            frameList.append([process[0], process[1], randomFrame, ts])
            pageTable.append([process[0], process[1], randomFrame])
            displayTable.append([process[0], process[1], randomFrame])
            for frame in freeFrames:
                if frame == randomFrame:
                    freeFrames.remove(frame)

        #run through each entry in frame list
        for entries in frameList:
            #if process id and page # are in frame list, set inFrame to 1
            if process[0] == entries[0] and process[1] == entries[1]:
                ts += 1
                entries[3] = ts
                inFrame = 1
                break

        #if not in frame
        if inFrame == 0:
            if freeFrames:
                while restart:
                    randomFrame = random.randint(0,15)

                    #check through list of free frames
                    for frame in freeFrames:
                        #if frame is available, remove from free frames, append to frame list
                        if frame == randomFrame:
                            freeFrames.remove(randomFrame)
                            ts += 1
                            pageFault(process[0])
                            frameList.append([process[0], process[1], randomFrame, ts])
                            pageTable.append([process[0], process[1], randomFrame])
                            displayTable.append([process[0], process[1], randomFrame])
                            restart = False
                            break
                inFrame = 1


            #if frame list full, find least recently used
            elif not freeFrames:

                #initial values for LRU, index count, and frame to replace
                lru = 99999999
                count = -1
                frame = 0

                #set LRU for values in framelist
                for entries in frameList:
                    if entries[3] < lru:
                        lru = entries[3]

                #increase index, set frame for LRU
                for entries in frameList:
                    count += 1
                    if entries[3] == lru:
                        frame = entries[2]
                        break

                #remove least recently used from frame list, replace with new process
                ts += 1
                frameList.remove(frameList[count])
                pageTable.remove(pageTable[count])
                displayTable.remove(displayTable[count])
                pageFault(process[0])
                frameList.insert(count, [process[0], process[1], frame, ts])
                pageTable.insert(count, [process[0], process[1], count])
                displayTable.append([process[0], process[1], count])

        #accept user input to step through or run to completion
        if run != 1:
            rinput = raw_input("\nEnter 'S' to step or 'R' to run: ")
            if rinput == 's':
                printStatus()
            if rinput == 'r':
                run = 1
            if rinput == 'q':
                exit(1)

def pageFault(proc):
    global pfList

    pfList.append([proc,1])

def printStatus():
    global pageTable, displayTable
    count = 0
    for x in displayTable:

        #page fault count
        pfcount = 0

        # time.sleep(.5)
        proc = x[0]

        #print output
        print "\n-----------------------------"
        print "Process / Page referenced"
        print "Process: " + str(x[0])
        print "Page: " + str(x[1])
        print "\n"

        print "Page Table"
        print "Process " + str(x[0]) + ":"
        print "Page\tFrame"

        #get current process, print page+frame
        for x in pageTable:
            if x[0] == proc:
                # print str(int(str(x[1]),2)) + "\t" + str(x[2])
                print str(x[1]) + "\t" + str(x[2])

        #print page faults for process
        for x in pfList:
            if x[0] == proc:
                pfcount += x[1]
        print "Page Faults: ", pfcount

        print "\nPhysical Memory / Frame Table"
        print "Frame#\tProcID\tPage#"

        #Check to see what process is in frame # and print
        for x in range(16):
            for frame in frameList:
                if frame[2] == x:
                    print str(x) + "\t" + str(frame[0]) + "\t" + str(frame[1])
                    break
            else:
                print str(x) + "\t\t"


        print "-----------------------------"

    print "Final Page Faults [process, # of faults]"

    #calculate page faults
    pflist = []
    for x in processPageList:
        count = 0
        for y in pfList:
            if x[0] == y[0]:
                count += y[1]
        pflist.append([x[0], count])

    #sort page fault list
    pfset = set(map(tuple,pflist))
    pf = map(list,pfset)
    pf.sort(key = lambda x: pflist.index(x))
    print pf

if __name__ == '__main__':
    start()
    run()
    printStatus()
