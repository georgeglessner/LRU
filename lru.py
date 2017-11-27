import time, random

input = ""
frameList = []
processPageList = []
pageTable = []
freeFrames = range(0,16)


def start():
    global input, frameList, processPageList

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


    #run through each process in list
    for process in processPageList:
        restart = True
        print process
        #timestamp increment
        ts += 1
        print ts
        #variable to denote whether in frame list or not
        inFrame = 0

        #variable to assign random frame
        randomFrame = random.randint(0,15)

        #if list is empty (base case)
        if not frameList:
            frameList.append([process[0], process[1], randomFrame, ts])
            pageTable.append([process[0], process[1], randomFrame])
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
                            frameList.append([process[0], process[1], randomFrame, ts])
                            pageTable.append([process[0], process[1], randomFrame])
                            restart = False
                            break
                inFrame = 1


            #if frame list full, find least recently used
            #TODO
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
                print frameList
                frameList.remove(frameList[count])
                pageTable.remove(pageTable[count])
                frameList.insert(count, [process[0], process[1], frame, ts])
                pageTable.insert(count, [process[0], process[1], count])

                print frameList

    #TODO implement a way to print status with space bar

def printStatus():
    global pageTable

    for x in processPageList:
        # time.sleep(.5)
        proc = x[0]

        #print output
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


if __name__ == '__main__':
    start()
    run()
    printStatus()
